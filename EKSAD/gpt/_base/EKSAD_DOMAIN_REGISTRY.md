# EKSAD Domain Registry

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | ALL (Developers, Architects, BA, SA, AI/Claude) |
| **Priority** | 🔴 P0 — AI/Claude MUST read this file FIRST before any task |
| **Status** | Active |

---

## Table of Contents

1. [Purpose & Usage](#1-purpose--usage)
2. [Domain Detection Rules (for AI/Claude)](#2-domain-detection-rules-for-aiclaude)
3. [Active Domains](#3-active-domains)
4. [Shared Core Services (ALL domains)](#4-shared-core-services-all-domains)
5. [How to Add a New Business Domain (Step-by-step)](#5-how-to-add-a-new-business-domain-step-by-step)
6. [Cross-Domain Integration Rules](#6-cross-domain-integration-rules)
7. [Naming Conventions per Domain](#7-naming-conventions-per-domain)
8. [Port Registry (Consolidated)](#8-port-registry-consolidated--single-source-of-truth)

---

## 1. Purpose & Usage

This file is the **"map"** of all EKSAD business domains.

- **AI/Claude MUST read this file BEFORE generating BRDs, code, or documentation.**
- Patterns in `_base/` are **universal** — this file tells you **WHICH entities** to use per domain.
- When new domains are added, only this file + new domain services are needed — `_base/` patterns stay unchanged.

> 🔑 **Key Principle:** Knowledge files describe HOW (patterns). This registry describes WHAT (entities, services, exchanges per domain).

---

## 2. Domain Detection Rules (for AI/Claude)

When the user mentions business context, detect the domain using these keyword patterns:

| Keywords (Indonesian/English) | Domain |
|-------------------------------|--------|
| vehicle, car, mobil, brand, model, SPK, dealer, showroom, kendaraan, otomotif | **Automotive** |
| employee, karyawan, attendance, absensi, payroll, gaji, leave, cuti, shift, HR, recruit, lamaran | **HRIS** |
| invoice, faktur, budget, GL, vendor, procurement, accounting, akuntansi, jurnal | **Finance** |

### Detection Workflow
1. Scan user input for domain keywords.
2. If **ambiguous** → ask the user explicitly: *"Domain mana yang dimaksud — Automotive, HRIS, atau Finance?"*
3. **Cross-domain requests** → identify primary domain, reference secondary as integration point.
4. Once domain identified → load this registry's section + apply universal `_base/` patterns.

---

## 3. Active Domains

### 🚗 Automotive (`eksad-automotive`) — [Sprint 1 Active]

| Field | Value |
|-------|-------|
| **Status** | ✅ Active (Sprint 1+) |
| **Namespace** | `eksad-automotive/` |
| **Master Data Service** | `svc-master-data` (:8086) — database `eksad_master` |
| **Master Exchange** | `exc-master-data` (topic) |
| **Business Context** | Used-car / new-car dealer management system |
| **Key Pipeline** | Lead → Order → Payment → Fulfillment |

**Domain Services** (names are EXAMPLES — decided per project by BA→SA workflow, see Decision 9):

| Service (example) | Port | Database (example) | Purpose |
|-------------------|------|---------------------|---------|
| `svc-pipeline` | :8082 | `eksad_pipeline` | Lead / prospect management |
| `svc-orders` | :8083 | `eksad_orders` | Sales order management |
| `svc-payment` | :8084 | `eksad_payment` | Payment tracking |
| `svc-fulfillment` | :8085 | `eksad_fulfillment` | Delivery / fulfillment management |

**Catalog Entities** (master data):
- `brands` — vehicle brands (Toyota, Honda, …)
- `models` — vehicle models, **parent: brand**
- `types` / `variants` — variants/trims, **parent: model**
- `colors` — color catalog
- `branches` — dealer branches / showrooms

**Hierarchy:** `brand → model → type/variant`

**Events** (published to `exc-master-data`):
- `BRAND.CREATED`, `BRAND.UPDATED`, `BRAND.DELETED`
- `MODEL.CREATED`, `MODEL.UPDATED`, `MODEL.DELETED` (payload includes `brand_id`)
- `TYPE.CREATED`, `TYPE.UPDATED`, `TYPE.DELETED` (payload includes `model_id`)
- `COLOR.*`, `BRANCH.*`

**Cache Tables** (per domain service):
`brand_cache`, `model_cache`, `type_cache`, `color_cache`, `branch_cache`

**Future Services:** `svc-inventory` (actual vehicle units — VIN, stock, unit pricing — distinct from catalog).

> ⚠️ **Note:** Service names above are **EXAMPLES**. Actual names are decided per project (see Decision 9). Master data service name and entities are **fixed for the domain**.

---

### 👥 HRIS (`eksad-hris`) — [PLANNED]

| Field | Value |
|-------|-------|
| **Status** | 🟡 Planned |
| **Namespace** | `eksad-hris/` |
| **Master Data Service** | `svc-master-data` (separate instance) — database `eksad_hris_master` |
| **Master Exchange** | `exc-hris-master-data` (topic) |
| **Business Context** | Human Resource Information System |

**Domain Services** (examples):

| Service (example) | Purpose |
|-------------------|---------|
| `svc-attendance` | Clock in/out, shift scheduling |
| `svc-payroll` | Salary calculation, payslip generation |
| `svc-leave` | Leave request, approval, balance tracking |
| `svc-recruitment` | Job posting, applicant tracking, interview scheduling |

**Catalog Entities:**
- `departments`, `positions`, `grades`
- `leave_types`, `shift_types`
- `allowance_types`, `deduction_types`

**Hierarchy:** `department → sub_department`, `position → grade`

**Events:**
- `DEPARTMENT.*`, `POSITION.*` (payload includes `department_id`)
- `GRADE.*` (payload includes `position_id`)
- `LEAVE_TYPE.*`, `SHIFT_TYPE.*`

**Cache Tables:** `department_cache`, `position_cache`, `grade_cache`, etc.

**Key Pipelines:**
- Employee lifecycle: recruit → onboard → active → offboard
- Attendance → Payroll
- Leave request → approval → balance update

---

### 💰 Finance (`eksad-finance`) — [FUTURE]

| Field | Value |
|-------|-------|
| **Status** | 🔵 Future consideration |
| **Namespace** | `eksad-finance/` |
| **Master Data Service** | `svc-master-data` (separate instance) |
| **Master Exchange** | `exc-finance-master-data` (topic) |

**Domain Services (planned):** `svc-accounting`, `svc-budgeting`, `svc-procurement`

**Catalog Entities:** `chart_of_accounts`, `cost_centers`, `vendors`, `tax_codes`

---

## 4. Shared Core Services (ALL domains)

These services are **shared across every business domain** — names are **FIXED and NEVER renamed**:

| Service | Port | Database | Tier | Purpose |
|---------|------|----------|------|---------|
| `eksad-core-auth` | :8090 | `eksad_core_auth` (PostgreSQL) | 🔒 Core | Credential storage, JWT signing (RS256), token refresh/revoke, JWKS. **Internal API only**. See Decision 11. |
| `eksad-core-audittrail` | — (consumer) | MongoDB | 🔒 Core | Audit logging via `exc-log-activity` |
| `eksad-core-storage` | — | — | 🔒 Core | File upload, thumbnail generation |
| `eksad-gateway` | :8080 | — | 🔒 Core | API gateway — routing, rate limiting, JWT validation via JWKS. **Optional** (see Decision 13) |
| `svc-user-management` | :8087 | `eksad_users` (MongoDB) | 🔒 Fixed-name | User CRUD, RBAC, roles/permissions, JWT claim packaging. See Decision 12. |
| `svc-tenant-management` | :8091 | `eksad_tenants` (MongoDB) | 🔒 Fixed-name | Tenant registry, N-level hierarchy (materialized path), config inheritance, provisioning. See T-20. |
| `svc-master-data` | :8086 | `eksad_master*` (PostgreSQL) | 🔒 Fixed-name | Catalog/reference entities per domain (entities vary, name fixed). |

**Shared Infrastructure:**
- **RabbitMQ** — single broker, separate exchanges per domain
- **PostgreSQL** — shared instance Phase 1 (see `EKSAD_DB_DEPLOYMENT_STRATEGY.md`)
- **MongoDB** — for user-mgmt, tenant-mgmt, audittrail

---

## 5. How to Add a New Business Domain (Step-by-step)

1. **Register domain** in this file (copy an existing domain block as template).
2. **Define master data entities** for the domain.
3. **Create namespace folder:** `eksad-{domain}/`.
4. **Create `svc-master-data` instance** with domain-specific catalog (database `eksad_{domain}_master`).
5. **Create domain services** following EKSAD patterns from `_base/` (names decided by BA→SA per project).
6. **Create domain-specific exchange:** `exc-{domain}-master-data` (topic).
7. **Setup databases** in PostgreSQL (same phased approach — see `EKSAD_DB_DEPLOYMENT_STRATEGY.md`).
8. **NO changes** needed to `_base/` pattern files — they are universal.
9. **Update** `EKSAD_EVENT_CATALOG.md` with new exchange + events.

---

## 6. Cross-Domain Integration Rules

Domains are **ISOLATED by default** — no direct service-to-service calls across domains.

If cross-domain data is needed (e.g., HRIS employee referenced in Automotive leads):

| Option | Approach | When to use |
|--------|----------|-------------|
| **A. Shared Identity** | `eksad-core-auth` + `svc-user-management` holds base user/employee info | Default — user identity is universal |
| **B. Cross-Domain Event Bridge** | Future — careful design needed (separate exchange per direction) | Async data propagation only |
| **C. API Gateway Composition** | Frontend merges from both domains | Read-only cross-domain views |

### Forbidden
- ❌ **NEVER** share databases across domains
- ❌ **NEVER** share master data exchanges across domains
- ❌ **NEVER** make direct synchronous REST calls from Domain A service to Domain B service

---

## 7. Naming Conventions per Domain

| Artifact | Pattern | Example (Automotive) | Example (HRIS) |
|----------|---------|----------------------|-----------------|
| Service name | `svc-{function}` | `svc-pipeline` | `svc-attendance` |
| Database name | `eksad_{function}` | `eksad_pipeline` | `eksad_attendance` |
| Master DB | `eksad_{domain}_master` | `eksad_master` | `eksad_hris_master` |
| Exchange (master) | `exc-{domain}-master-data` | `exc-master-data` | `exc-hris-master-data` |
| Queue (cache sync) | `q-{domain}-master-sync-{service}` | `q-master-sync-pipeline` | `q-hris-master-sync-attendance` |
| Routing key | `r.{entity}.{action}` | `r.brand.created` | `r.department.created` |
| Module type | `EKSAD_{DOMAIN}.{ENTITY}.{ACTION}` | `EKSAD_MASTER.BRAND.CREATE` | `EKSAD_HRIS_MASTER.DEPARTMENT.CREATE` |
| Cache table | `{entity}_cache` | `brand_cache` | `department_cache` |

### Rules
- Service names must be **domain-agnostic** (universal terms like `pipeline`, `orders` — never business jargon like `svc-spk`, `svc-leads`).
- `svc-user-management`, `svc-master-data`, `svc-tenant-management` are **fixed names** — never renamed.
- Core service names (`eksad-core-*`, `eksad-gateway`) are **never changed**.

---

## 8. Port Registry (Consolidated — Single Source of Truth)

All port assignments for the EKSAD platform. Services across all projects MUST use these ports. AI/Claude references this table when generating `docker-compose`, K8s manifests, or configs.

### 8.1 Core Infrastructure (fixed, every project)

| Port | Service | Database | Protocol | Notes |
|------|---------|----------|----------|-------|
| :8080 | `eksad-gateway` | — | HTTP | Optional (Decision 13), reverse proxy + JWT validation |
| :8090 | `eksad-core-auth` | `eksad_core_auth` (PG) | HTTP | Internal API only (except JWKS endpoint) |
| — | `eksad-core-audittrail` | MongoDB | AMQP | Consumer only (no HTTP port) |
| — | `eksad-core-storage` | — | HTTP | File upload / thumbnail |

### 8.2 Fixed-Name Services (every project, content varies)

| Port | Service | Database | Protocol | Notes |
|------|---------|----------|----------|-------|
| :8086 | `svc-master-data` | `eksad_master*` (PG) | HTTP | Catalog/reference entities |
| :8087 | `svc-user-management` | `eksad_users` (Mongo) | HTTP | User CRUD, RBAC, JWT claims |
| :8091 | `svc-tenant-management` | `eksad_tenants` (Mongo) | HTTP | Tenant hierarchy, config inheritance |

### 8.3 Domain Services (BA/SA decide per project, ports sequential)

| Port | Service (EXAMPLE) | Database (EXAMPLE) | Notes |
|------|-------------------|---------------------|-------|
| :8082 | `svc-pipeline` | `eksad_pipeline` (PG) | [Automotive example] |
| :8083 | `svc-orders` | `eksad_orders` (PG) | [Automotive example] |
| :8084 | `svc-payment` | `eksad_payment` (PG) | [Automotive example] |
| :8085 | `svc-fulfillment` | `eksad_fulfillment` (PG) | [Automotive example] |
| :8092+ | (next services) | `eksad_{function}` (PG) | Expand as needed |

### 8.4 Infrastructure

| Port | Service | Notes |
|------|---------|-------|
| :5432 | PostgreSQL | Shared instance (Phase 1), separate DBs per service |
| :27017 | MongoDB | User-mgmt, tenant-mgmt, audittrail |
| :5672 | RabbitMQ (AMQP) | Event messaging |
| :15672 | RabbitMQ Management UI | Admin panel (dev/staging only) |

### 8.5 Observability (Sprint 2+)

| Port | Service | Notes |
|------|---------|-------|
| :16686 | Jaeger UI | Distributed tracing |
| :4317 | Jaeger OTLP collector | OpenTelemetry ingestion |
| :9090 | Prometheus | Metrics scraping |
| :3001 | Grafana | Dashboards (mapped from 3000 to avoid FE conflicts) |

### 8.6 Port Range Convention

| Range | Category | Assignment Rule |
|-------|----------|-----------------|
| :8080 | Gateway | Fixed |
| :8082–8085 | Domain services | Sequential per project |
| :8086–8089 | Fixed-name services | :8086 master, :8087 user-mgmt, :8091 tenant-mgmt |
| :8090–8091 | Core infrastructure | :8090 core-auth, :8091 tenant-mgmt |
| :8092+ | Expansion | New domain services get next available port |
| :5432 / :27017 / :5672 | Infrastructure | Fixed |

### 8.7 Rules

- Port assignments are **PERMANENT** — once assigned, never change.
- Domain services get ports in **order of creation** (:8082, :8083, :8084…).
- Each project's SA documents final port assignments in **TSD Service Registry**.
- `docker-compose` and K8s manifests MUST reference this registry.
- If a port conflicts with the host machine, use **PORT_MAPPING** (e.g., `-p 18082:8082`).

---

## Glossary (registry-local)

| Term | Definition |
|------|------------|
| **Domain** | A business vertical (Automotive, HRIS, Finance) with its own services, master data, and exchange. |
| **Namespace** | Folder/grouping `eksad-{domain}/` containing all services for a domain. |
| **Core service** | Platform infrastructure shared across all domains — fixed name, never renamed. |
| **Fixed-name service** | Standard service with fixed name but content adapts to domain (e.g., `svc-master-data`). |
| **Domain service** | Business logic service whose name is decided per project by BA→SA workflow. |

---

*End of file. Maintained by the EKSAD Platform Team. When adding a new domain, see Section 5.*
