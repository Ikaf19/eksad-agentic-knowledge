# EKSAD Multi-Tenancy Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | ALL (Developers, Architects, SA, AI/Claude) |
| **Priority** | 🟡 P1 |
| **Related** | Decisions 8, 9, 11, 12; `EKSAD_CORE_AUTH_PATTERNS.md` (T-17); `EKSAD_DOMAIN_REGISTRY.md` |

---

## Table of Contents

1. [Overview — Multi-Tenancy Strategy](#1-overview--multi-tenancy-strategy)
2. [Tenant Hierarchy — N-Level Materialized Path](#2-tenant-hierarchy--n-level-materialized-path)
3. [Tenant Registry — `svc-tenant-management`](#3-tenant-registry--svc-tenant-management)
4. [Config Inheritance Pattern](#4-config-inheritance-pattern)
5. [Tenant Context Propagation (Cross-Service)](#5-tenant-context-propagation-cross-service)
6. [Data Isolation Enforcement](#6-data-isolation-enforcement)
7. [Platform Admin & Role Hierarchy](#7-platform-admin--role-hierarchy)
8. [Tenant Provisioning Flow](#8-tenant-provisioning-flow)
9. [Tenant Suspension & Archival](#9-tenant-suspension--archival)
10. [Database Strategy Migration Path](#10-database-strategy-migration-path-shared--dedicated)
11. [Impact on Existing Services](#11-impact-on-existing-services)
12. [`svc-tenant-management` API](#12-svc-tenant-management-api)
13. [Testing](#13-testing)

---

## 1. Overview — Multi-Tenancy Strategy

- **Target market:** enterprise / large companies (group with subsidiaries).
- **Tenancy model:** Shared DB + Shared Schema (Sprint 1) → migration path to Dedicated DB per tenant.
- **N-level hierarchy:** Group → Company → Division → Branch → … (unlimited depth, configurable max).
- Every table/collection in every service MUST have `tenant_id`.
- **Platform admin model:** **Option C — Hybrid** (platform tenant + scope flag).
- `database_strategy` flag per tenant — `shared` (Sprint 1 default) → `dedicated` (future).

---

## 2. Tenant Hierarchy — N-Level (Materialized Path)

```
[PLATFORM] (scope: platform, reserved)
├── Group A — Astra International       (depth: 0)
│   ├── AHM                              (depth: 1)
│   ├── TAM                              (depth: 1)
│   └── Astra Financial                  (depth: 1)
│       ├── ACC                          (depth: 2)
│       └── FIF                          (depth: 2)
├── Group B — Sinar Mas                 (depth: 0)
│   └── Smart Tbk                        (depth: 1)
└── Standalone Company C                 (depth: 0, no children)
```

### Materialized Path Pattern

| Query | Implementation |
|-------|----------------|
| All descendants | `{ path: { $regex: "^/tenant-astra" } }` |
| Direct children | `{ parent_tenant_id: "tenant-astra" }` |
| Ancestors | Split `path` by `/`, look up each segment |

- `path` is **auto-computed** on create/move — never set manually.
- Max depth: configurable (default 5), enforced at creation.

---

## 3. Tenant Registry — `svc-tenant-management`

| Field | Value |
|-------|-------|
| **Service** | `svc-tenant-management` |
| **Port** | :8091 |
| **Database** | MongoDB — `eksad_tenants` |
| **Tier** | Fixed-name (same as `svc-user-management`, `svc-master-data`) |

### Collections

#### `tenants`

```javascript
{
  _id: ObjectId,
  tenant_id: "tenant-astra",           // unique slug, immutable after creation
  tenant_code: "ASTRA",                // short code, unique
  name: "PT Astra International Tbk",
  type: "group",                       // platform | group | company | division | branch
  parent_tenant_id: null,              // null = root (or "platform" for top-level groups)
  path: "/tenant-astra",               // materialized path
  depth: 0,                            // 0 = root group
  config: {
    locale: "id_ID",
    password_min_length: 10,
    mfa_enforcement: "optional",
    max_sessions: 3,
    database_strategy: "shared",       // "shared" | "dedicated"
    features: {
      audit_trail: true,
      gateway: false
    }
  },
  status: "active",                    // active | suspended | archived
  contact: { email, phone, address },
  metadata: { industry, size, notes },
  created_at: ISODate,
  updated_at: ISODate
}
```

#### `tenant_config_history`

```javascript
{
  tenant_id, changed_by, old_config, new_config, changed_at
}
```

### Indexes

- `{ tenant_id: 1 }` unique
- `{ tenant_code: 1 }` unique
- `{ parent_tenant_id: 1 }`
- `{ path: 1 }`
- `{ status: 1 }`

---

## 4. Config Inheritance Pattern

- Child tenant inherits ALL config from parent **unless explicitly overridden**.
- Resolution order: child → parent → grandparent → … → platform defaults.

```pseudo
function resolveEffectiveConfig(tenantId):
    tenant = findTenant(tenantId)
    if tenant.parent_tenant_id == null:
        return merge(PLATFORM_DEFAULTS, tenant.config)
    parentConfig = resolveEffectiveConfig(tenant.parent_tenant_id)  // recursive
    return merge(parentConfig, tenant.config)                       // child wins
```

- **Caching:** resolved config cached (Redis/local) with 5-min TTL.
- **Cache invalidation:** on config update → invalidate self + ALL descendants.

### Example

| Tenant | Config |
|--------|--------|
| Group Astra | `locale=id_ID, password_min=10, mfa=optional` |
| AHM (override) | `password_min=12, mfa=required` |
| **AHM effective** | `locale=id_ID (inherited), password_min=12, mfa=required` |
| TAM (no override) | — |
| **TAM effective** | `locale=id_ID, password_min=10, mfa=optional` (all inherited) |

---

## 5. Tenant Context Propagation (Cross-Service)

### JWT Claims

| User type | Sample claims |
|-----------|---------------|
| Tenant user | `{ sub, tenant_id: "tenant-ahm", scope: "tenant", roles: [...] }` |
| Group admin | `{ sub, tenant_id: "tenant-astra", scope: "group", roles: ["GROUP_ADMIN"] }` |
| Platform admin | `{ sub, tenant_id: "platform", scope: "platform", roles: ["PLATFORM_ADMIN"] }` |

### Propagation Chain

1. Client sends JWT in `Authorization` header.
2. `TenantContextFilter` (JAX-RS filter) extracts `tenant_id` + `scope` from JWT.
3. Stores in `TenantContext` (CDI `@RequestScoped` bean): `tenantId`, `scope`, `path`.
4. All repository queries use `TenantContext.tenantId`.
5. RabbitMQ events include `tenant_id` in envelope **and** message headers.
6. Downstream consumers extract `tenant_id` from event headers.
7. Logging MDC includes `tenant_id` (see `EKSAD_OBSERVABILITY_PATTERNS.md`).

### Code Sketch — `TenantContextFilter`

```java
@Provider
@Priority(Priorities.AUTHENTICATION + 100)
public class TenantContextFilter implements ContainerRequestFilter {
    @Inject JsonWebToken jwt;
    @Inject TenantContext tenantContext;

    @Override
    public void filter(ContainerRequestContext ctx) {
        String tenantId = jwt.getClaim("tenant_id");
        String scope    = jwt.getClaim("scope");
        if (tenantId == null) throw new ForbiddenException("Missing tenant_id");
        tenantContext.set(tenantId, scope);
        MDC.put("tenant_id", tenantId);
    }
}
```

---

## 6. Data Isolation Enforcement

### Sprint 1 — Code-Level (Mandatory)

- `TenantAwareRepository<T>` abstract base:
  - ✅ `findByIdAndTenant(id, tenantId)` — ALWAYS use this
  - ❌ `findById(id)` — **FORBIDDEN** (throws `TenantContextMissingException`)
  - ✅ `findAllByTenant(tenantId, filters)` — filtered query
  - ✅ `save(entity)` — auto-sets `tenant_id` from `TenantContext` before persist
- Every MongoDB collection: compound index `{ tenant_id: 1, ... }`.
- Every PostgreSQL table: index `(tenant_id, ...)`.
- **Code review checklist:** *"Is `tenant_id` filter present in EVERY query?"*

### Sprint 2+ — PostgreSQL Row Level Security (RLS) (Optional)

```sql
ALTER TABLE credentials ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON credentials
    USING (tenant_id = current_setting('app.tenant_id')::text);
```

- DB-level enforcement as **safety net** (even if code misses a filter).
- Recommended when handling financial / healthcare / PII data or under strict compliance.

### Scope-Based Access

| Scope | Behavior |
|-------|----------|
| `tenant` | Strict `tenant_id` filter |
| `group` | Filter by **path prefix** (all descendants): `{ path: { $regex: "^" + currentTenantPath } }` |
| `platform` | No tenant filter (all data) |

> **SA Instructions Note:** Code-level isolation is enforced in Sprint 1. If the project handles sensitive data (financial, healthcare, PII) or regulatory requirements demand DB-level isolation, flag this and enable PostgreSQL RLS. Document the decision in the TSD.

---

## 7. Platform Admin & Role Hierarchy

**Option C Hybrid** — platform admin has `tenant_id = "platform"`, `scope = "platform"`.

| Role | Access |
|------|--------|
| `PLATFORM_ADMIN` | All tenants, CRUD tenants, impersonate, system config |
| `PLATFORM_SUPPORT` | Read-only across all tenants |
| `GROUP_ADMIN` | All descendants of their group, manage child tenants |
| `GROUP_VIEWER` | Read-only across group descendants |
| `TENANT_ADMIN` | Single tenant, manage users/roles |
| `TENANT_USER` | Single tenant, assigned permissions |

### Impersonation

- Platform/Group admin can "switch" to a child tenant.
- Issues new JWT with target `tenant_id` + `scope = "impersonated"`.
- All actions logged with **original admin identity** + impersonated tenant.
- Audit trail: `{ actor: "admin-001", impersonating: "tenant-ahm", action: ... }`.

> ⚠️ Reserved `tenant_id = "platform"` cannot be used for real tenants.
> Business reports must filter `WHERE tenant_id != 'platform'` to exclude platform data.

---

## 8. Tenant Provisioning Flow

### Sprint 1 — Manual (API call by platform admin)

**Create Group:**
1. `POST /api/v1/tenants { name, type: "group", config: {...} }`
2. `svc-tenant-management` creates tenant record.
3. Calls `svc-user-management` → create default `GROUP_ADMIN` user.
4. `svc-user-management` calls `eksad-core-auth-client` SDK → register credential.
5. Returns `{ tenant_id, admin_credentials }`.

**Create Child Tenant:**
1. `POST /api/v1/tenants { name, type: "company", parent_tenant_id: "tenant-astra" }`
2. Auto-compute: `path = parent.path + "/" + tenant_id`, `depth = parent.depth + 1`.
3. Validate `depth <= max_depth` (default 5).
4. Inherit config from parent (merge).
5. Create default `TENANT_ADMIN` user.

### Future
Self-service signup → auto-provision → billing integration.

---

## 9. Tenant Suspension & Archival

### Suspend Tenant
- `status: "active" → "suspended"`.
- All JWT **issuance** blocked for this tenant.
- Existing JWTs still valid until expiry (30 min max).
- Data preserved, accessible by platform admin.

### Suspend Group (Cascading)
- All child tenants also suspended:
  ```sql
  UPDATE tenants SET status='suspended' WHERE path LIKE '/tenant-astra%';
  ```

### Archive Tenant
- `status: "suspended" → "archived"`.
- Data soft-deleted or moved to cold storage (future).
- Cannot be reactivated without platform admin action.

---

## 10. Database Strategy Migration Path (Shared → Dedicated)

- **Sprint 1:** ALL tenants use shared DB (`database_strategy: "shared"`).
- **Flag per tenant:** `config.database_strategy = "shared" | "dedicated"`.

### Migration Steps (Future, per tenant)
1. Set `database_strategy = "dedicated"` on tenant.
2. Provision new DB instance (PostgreSQL / MongoDB).
3. Run data migration: extract tenant's data → insert into dedicated DB.
4. Update service routing: `TenantDatabaseRouter` reads strategy flag.
5. Verify data integrity.
6. Remove tenant data from shared DB.

### Sprint 1 Preparation
- ALWAYS include `tenant_id` in every table/collection (enables future extraction).
- ALWAYS use `TenantAwareRepository` (enables future routing).
- `database_strategy` flag in tenant config (flag only, no routing logic yet).

---

## 11. Impact on Existing Services

| Service | Changes |
|---------|---------|
| `svc-user-management` | Add `tenant_id` to all docs; `roles`/`role_assignments` scoped per tenant; `jwt_claim_templates` per tenant; `domain_profile` already flexible |
| `svc-master-data` | All master data collections get `tenant_id`. Platform-level master data = `tenant_id = "platform"` (visible to all). Tenant-specific master data = specific `tenant_id`. |
| `eksad-core-auth` | `credentials`, `refresh_tokens`, `auth_events` all get `tenant_id` column. JWKS shared (one signing key for all tenants). |
| Domain services | Every table/collection: `tenant_id` mandatory. `TenantAwareRepository` enforced. |
| `eksad-core-audittrail` | Audit events include `tenant_id`. Platform admin can query across tenants. |

---

## 12. `svc-tenant-management` API

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/v1/tenants` | Create tenant (platform/group admin) |
| `GET` | `/api/v1/tenants` | List tenants (filtered by scope) |
| `GET` | `/api/v1/tenants/{id}` | Get tenant details |
| `PUT` | `/api/v1/tenants/{id}` | Update tenant (name, config) |
| `PATCH` | `/api/v1/tenants/{id}/config` | Partial config update (merge) |
| `POST` | `/api/v1/tenants/{id}/suspend` | Suspend tenant (+ cascade children) |
| `POST` | `/api/v1/tenants/{id}/activate` | Reactivate tenant |
| `POST` | `/api/v1/tenants/{id}/archive` | Archive tenant |
| `GET` | `/api/v1/tenants/{id}/children` | List direct children |
| `GET` | `/api/v1/tenants/{id}/descendants` | List all descendants (tree) |
| `GET` | `/api/v1/tenants/{id}/effective-config` | Resolved config with inheritance |
| `DELETE` | `/api/v1/tenants/{id}` | **FORBIDDEN** — use archive instead |

All endpoints require appropriate scope (platform / group / tenant).

---

## 13. Testing

| Test Type | Scenario |
|-----------|----------|
| Unit | Config inheritance resolution (3+ levels deep) |
| Unit | Materialized path computation on create/move |
| Unit | `TenantAwareRepository` rejects queries without `tenant_id` |
| Integration | Create group → child → grandchild → verify hierarchy |
| Integration | Tenant A creates data → Tenant B queries → empty result |
| Integration | Group admin queries → sees all descendant data |
| Integration | Platform admin queries → sees all data |
| Integration | Suspend group → all children blocked from JWT issuance |
| Integration | Config override → child effective config correct |

See `EKSAD_TESTING_GUIDE.md` Section "Multi-Tenancy Testing" for full test patterns.

---

*End of file. Cross-references: `EKSAD_CORE_AUTH_PATTERNS.md`, `EKSAD_DOMAIN_REGISTRY.md`, `EKSAD_DB_DEPLOYMENT_STRATEGY.md`.*
