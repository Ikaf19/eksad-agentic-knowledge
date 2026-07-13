# EKSAD Architecture Document Template

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Architects, Tech Leads, SA |
| **Priority** | 🟢 P2 |
| **Purpose** | Skeleton for per-project `ARCHITECTURE.md` documents |

---

> Use this template when creating a new project's `docs/ARCHITECTURE.md`. Copy this file, then fill in the bracketed `[...]` placeholders.

---

# {Project Name} — Architecture Document

| Meta | Value |
|------|-------|
| **Project** | [Project name, e.g., EKSAD Used-Car Sales Platform] |
| **Domain** | [Automotive / HRIS / Finance / ...] |
| **Version** | 1.0 |
| **Date** | [YYYY-MM-DD] |
| **Author** | [SA name] |
| **Status** | Draft / In Review / Approved |

---

## 1. Project Overview

### 1.1 Purpose
[1–2 sentences describing the business purpose.]

### 1.2 Scope
- **In scope:** [list]
- **Out of scope:** [list]

### 1.3 Stakeholders
| Role | Name | Responsibility |
|------|------|----------------|
| Product Owner | | |
| BA | | |
| SA | | |
| Tech Lead | | |

---

## 2. Domain & Business Context

### 2.1 Business Domain
[Reference `EKSAD_DOMAIN_REGISTRY.md` — which domain, which entities apply.]

### 2.2 Key Business Rules
[Numbered list of top-level rules, referencing BR-* IDs from BRD.]

### 2.3 Glossary (Project-Specific)
[Project-specific terms not in `EKSAD_DOMAIN_GLOSSARY.md`.]

---

## 3. System Architecture (C4 Model)

> This section follows the **C4 model** (Context → Container → Component → Code). Fill each level with diagrams (ASCII / Mermaid / PlantUML / draw.io export) and annotations. Reference: https://c4model.com

### 3.1 L1 — System Context Diagram

**Purpose:** Show the system as a single black box, its users (personas), and external systems it integrates with.

```
[ASCII / Mermaid: System Context]

         ┌──────────────┐         ┌──────────────────┐
         │  End User    │         │  Admin / SA      │
         │  (Customer)  │         │  (Internal)      │
         └──────┬───────┘         └────────┬─────────┘
                │ HTTPS                    │ HTTPS
                ▼                          ▼
         ┌────────────────────────────────────────┐
         │   {Project Name} Platform              │
         │   (EKSAD)                              │
         └──────┬─────────────┬─────────────┬─────┘
                │             │             │
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────────┐
         │ Payment  │  │ SMS / WA │  │  External    │
         │ Gateway  │  │ Provider │  │  Master Data │
         └──────────┘  └──────────┘  └──────────────┘
```

| Actor / External System | Direction | Protocol | Purpose |
|-------------------------|-----------|----------|---------|
| End User | In | HTTPS | Primary platform users |
| Admin / SA | In | HTTPS | System administration |
| [Payment Gateway] | Out | REST | [purpose] |
| [SMS/WA Provider] | Out | REST/Webhook | [purpose] |

---

### 3.2 L2 — Container Diagram

**Purpose:** Zoom into the system; show containers (services, databases, message brokers) and the tech stack of each.

```
[ASCII / Mermaid: Container view]

   Client ──▶ [eksad-gateway :8080] ──▶ [eksad-core-auth :8090]
                       │
                       ├──▶ [svc-user-mgmt :8087] ──▶ MongoDB
                       ├──▶ [svc-tenant-mgmt :8091] ──▶ MongoDB
                       ├──▶ [svc-master-data :8086] ──▶ PostgreSQL
                       └──▶ [svc-{domain} :808X] ──▶ PostgreSQL
                                  │
                                  ▼
                            RabbitMQ (events)
                                  │
                                  ▼
                       [eksad-core-audittrail] ──▶ MongoDB
```

#### 3.2.1 Services Inventory (Containers)
| Service | Type | Port | Tech Stack | DB | Purpose |
|---------|------|------|------------|------|---------|
| `eksad-gateway` | Core | :8080 | Quarkus 3.30 reactive | — | Optional gateway (JWT validation + routing only) |
| `eksad-core-auth` | Core | :8090 | Quarkus reactive | PG `eksad_core_auth` | Auth/JWT issuance |
| `eksad-core-audittrail` | Core | :8089 | Quarkus reactive | MongoDB | Audit consumer |
| `svc-user-management` | Fixed | :8087 | Quarkus reactive | Mongo `eksad_users` | User CRUD |
| `svc-tenant-management` | Fixed | :8091 | Quarkus reactive | Mongo `eksad_tenants` | Tenant CRUD |
| `svc-master-data` | Fixed | :8086 | Quarkus reactive | PG `eksad_master` | Catalog |
| `svc-[domain]` | Domain | :808X | Quarkus reactive | PG `eksad_[domain]` | [purpose] |

#### 3.2.2 Infrastructure Containers
| Container | Tech | Purpose |
|-----------|------|---------|
| RabbitMQ | RabbitMQ 3.x | Async messaging (audit, cache sync, domain events) |
| PostgreSQL | PG 15+ | Transactional store (per-service schema) |
| MongoDB | Mongo 6+ | Document store (users, tenants, audit) |
| Redis (Phase 2+) | Redis 7+ | Distributed cache / rate-limit |

---

### 3.3 L3 — Component Diagram (per Service)

**Purpose:** Zoom into a single container (service); show internal components and their layering (Resource → Service → Repository → DB).

> Provide one L3 diagram per critical service. Below is the canonical EKSAD service layering template.

```
[ASCII / Mermaid: Component view for svc-{domain}]

   ┌─────────────────────────────────────────────────────┐
   │  svc-{domain}                                       │
   │                                                     │
   │  ┌──────────────┐    ┌──────────────────────────┐  │
   │  │ {X}Resource  │───▶│  {X}Service              │  │
   │  │ (JAX-RS)     │    │  (@ApplicationScoped     │  │
   │  │ @RolesAllowed│    │   @WithSession)          │  │
   │  └──────────────┘    └──────────┬───────────────┘  │
   │                                 │                  │
   │                                 ▼                  │
   │                      ┌──────────────────────────┐  │
   │                      │ {X}Repository            │  │
   │                      │ (extends BaseRepository) │  │
   │                      │  createFlow/updateFlow   │  │
   │                      └──────────┬───────────────┘  │
   │                                 │                  │
   │                                 ▼                  │
   │                      ┌──────────────────────────┐  │
   │                      │ AuditTrailEmitter        │  │
   │                      │ (MutinyEmitter→RabbitMQ) │  │
   │                      └──────────────────────────┘  │
   └─────────────────────────────────────────────────────┘
```

| Component | Responsibility | EKSAD Pattern Reference |
|-----------|----------------|-------------------------|
| `{X}Resource` | JAX-RS endpoints, RBAC, request DTO validation | `EKSAD_CODING_STANDARDS.md` §Resource |
| `{X}Service` | Business orchestration, `@WithSession`, `@ReactiveTransactional` on writes | `EKSAD_CODING_STANDARDS.md` §Service |
| `{X}Repository` | Persistence + audit emission via `createFlow/updateFlow/deleteFlow` | `EKSAD_CODING_STANDARDS.md` §Repository |
| `{X}ModuleType` | Action constants (interface, never enum) | `EKSAD_BASE_PRINCIPLES.md` §Module Type Convention |
| `AuditTrailEmitter` | Reactive emitter to RabbitMQ exchange `eksad.audit.exchange` | `EKSAD_BASE_PRINCIPLES.md` §Audit Trail Flow |

> Repeat this subsection (L3) per critical domain service if internal components differ materially.

---

### 3.4 L4 — Code / Sequence Diagrams (Critical Flows)

**Purpose:** Zoom into the most important runtime flows; show class/sequence-level interactions for flows that drive architectural risk.

> Pick 3–6 flows that exercise cross-service / async / approval paths. Use sequence diagrams (Mermaid/PlantUML) — not full UML class diagrams.

#### 3.4.1 Flow Inventory
| # | Flow Name | Type | Services Involved | Priority |
|---|-----------|------|-------------------|----------|
| F1 | Auth login + JWT issuance | Sync | gateway → core-auth | 🔴 P0 |
| F2 | Domain entity create (with audit) | Sync + Async | svc-{domain} → RabbitMQ → audittrail | 🔴 P0 |
| F3 | Master data change → cache sync | Async | svc-master-data → RabbitMQ → svc-{domain} | 🟠 P1 |
| F4 | [Approval workflow] | Sync + Async | [list] | 🟠 P1 |
| F5 | [Cross-service query via REST] | Sync | [list] | 🟡 P2 |

#### 3.4.2 Example — F2: Domain Entity Create
```
[Mermaid sequenceDiagram placeholder]

Client → {X}Resource: POST /api/v1/{x}
{X}Resource → {X}Service: create(dto)
{X}Service → {X}Repository: createFlow(dto, MODULE_TYPE.CREATE)
{X}Repository → DB: persist (tenant_id, created_at epoch ms)
{X}Repository → AuditTrailEmitter: sendAndForget(event)
AuditTrailEmitter → RabbitMQ: publish (exchange=eksad.audit.exchange)
RabbitMQ → eksad-core-audittrail: consume → Mongo write
{X}Resource ← {X}Service ← {X}Repository: entity
Client ← {X}Resource: 201 CREATED
```

> Add one diagram block per flow listed in 3.4.1.

---

### 3.5 Architecture Principles Applied
Cross-reference `EKSAD_BASE_PRINCIPLES.md`:
- [✅/❌] No logic in gateway
- [✅/❌] Service owns its schema
- [✅/❌] Events over sync calls
- [✅/❌] `tenant_id` everywhere
- [✅/❌] Flyway only
- [✅/❌] Auto audit trail
- [✅/❌] Long epoch timestamps
- [✅/❌] Soft delete
- [✅/❌] File reference by ID only
- [✅/❌] Right DB for right job
- [✅/❌] Master data via dedicated service
- [✅/❌] Denormalized cache via events
- [✅/❌] Tenant-configurable reserved fields

---

## 4. Data Architecture

### 4.1 Database Strategy
[Phase 1 / 2 / 3 — reference `EKSAD_DB_DEPLOYMENT_STRATEGY.md`]

### 4.2 Per-Service Schemas
[ER diagrams or table lists per service]

### 4.3 Master Data Entities (this domain)
[List entities — reference `EKSAD_DOMAIN_REGISTRY.md`]

### 4.4 Cache Tables (per domain service)
[Which services maintain which `*_cache` tables]

### 4.5 Reserved Field Adoption
| Entity | Opt-in? | Reserved fields used | Tenant configs |
|--------|---------|----------------------|----------------|
| | | | |

---

## 5. Integration Architecture

### 5.1 REST API Inventory
[Per service, key endpoints — reference FSD/TSD]

### 5.2 Event Catalog (Project-Specific)
[Domain events published/consumed — reference `EKSAD_EVENT_CATALOG.md`]

### 5.3 External Integrations
| System | Direction | Protocol | Auth |
|--------|-----------|----------|------|
| | | | |

---

## 6. Security Architecture

### 6.1 Auth Flow
[Reference `EKSAD_CORE_AUTH_PATTERNS.md` §9]

### 6.2 RBAC Roles & Permissions
[Project-specific role matrix]

### 6.3 Multi-Tenancy Model
[Tenant hierarchy used by this project — reference `EKSAD_MULTI_TENANCY_PATTERNS.md`]

### 6.4 Data Isolation
[Code-level / DB-level (RLS) — reference `EKSAD_MULTI_TENANCY_PATTERNS.md` §6]

---

## 7. Resilience & Observability

### 7.1 Sprint Phasing
[Which resilience/observability features per sprint — reference `EKSAD_RESILIENCE_PATTERNS.md` §2, `EKSAD_OBSERVABILITY_PATTERNS.md` §2]

### 7.2 Health Checks
[Per-service health check dependencies]

### 7.3 Metrics & Alerts
[Custom business metrics; alert thresholds]

---

## 8. Deployment Architecture

### 8.1 Environments
| Env | Infra | URL | Purpose |
|-----|-------|-----|---------|
| Dev | Docker Compose | http://localhost | Local development |
| Staging | K8s namespace | https://staging.eksad.com | UAT |
| Prod | K8s | https://app.eksad.com | Production |

### 8.2 CI/CD Pipeline
[Reference `EKSAD_CICD_CONTAINER_PATTERNS.md`]

### 8.3 Docker / K8s
[Image registry, manifests location, secrets management]

---

## 9. Non-Functional Requirements

### 9.1 Performance Targets
| Metric | Target |
|--------|--------|
| API p95 latency | < 200 ms |
| Throughput | [X req/s per service] |
| Cache sync lag | < 5 s |

### 9.2 Scalability Plan
[Horizontal scaling strategy per service]

### 9.3 Availability
[SLA target: 99.9% etc.]

### 9.4 Disaster Recovery
[RPO / RTO targets — reference `EKSAD_DB_DEPLOYMENT_STRATEGY.md` §8]

---

## 10. Sprint Plan & Roadmap

| Sprint | Scope |
|--------|-------|
| Sprint 1 | [services + features] |
| Sprint 2 | [services + features] |
| Sprint 3+ | [roadmap] |

---

## 11. Architecture Decision Records (ADR)

> Use a lightweight ADR format (Michael Nygard style) for every significant architectural decision. One ADR per decision. Keep ADRs immutable — supersede instead of editing.

### 11.1 ADR Index
| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| ADR-001 | [e.g., Use PostgreSQL for transactional store] | Accepted | YYYY-MM-DD | — |
| ADR-002 | [e.g., MongoDB for audit trail] | Accepted | YYYY-MM-DD | — |
| ADR-003 | | Proposed | | |

**Status values:** `Proposed` · `Accepted` · `Deprecated` · `Superseded by ADR-NNN`

---

### 11.2 ADR Template (Copy per Decision)

```markdown
#### ADR-NNN — {Decision Title}

| Field | Value |
|-------|-------|
| **Status** | Proposed / Accepted / Deprecated / Superseded by ADR-MMM |
| **Date** | YYYY-MM-DD |
| **Deciders** | [names / roles] |
| **Consulted** | [names / roles] |
| **Informed** | [names / roles] |

**Context**
[What is the issue motivating this decision? What forces are at play (business, technical, political, social)? Reference relevant constraints and EKSAD base principles.]

**Decision**
[The change we are proposing or have agreed to implement. Use active voice: "We will ...".]

**Consequences**
- ✅ **Positive:** [what becomes easier]
- ⚠️ **Negative:** [what becomes harder / trade-offs]
- 🔁 **Neutral:** [side-effects that are neither good nor bad]

**Alternatives Considered**
1. **{Alt A}** — [rejected because ...]
2. **{Alt B}** — [rejected because ...]

**References**
- `EKSAD_BASE_PRINCIPLES.md` §[N]
- [Link to TSD / spike / benchmark]
```

---

### 11.3 ADR Entries

> Fill one block per accepted ADR using the template above. Example below.

#### ADR-001 — [Example: Adopt Reactive Quarkus over Imperative]

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | YYYY-MM-DD |
| **Deciders** | [Tech Lead, SA] |

**Context**
[Throughput requirement of N req/s per service with low memory footprint; existing team familiarity; need for non-blocking I/O for downstream RabbitMQ + Mongo.]

**Decision**
We will use Quarkus reactive (Mutiny `Uni`/`Multi`) with Hibernate Reactive Panache for all new services. Imperative Spring Boot is permitted only for legacy integrations explicitly listed in §1.2.

**Consequences**
- ✅ Better throughput per pod; lower memory; native-image friendly.
- ⚠️ Steeper learning curve for new joiners; `@WithSession` / `@ReactiveTransactional` discipline mandatory.
- 🔁 All EKSAD coding patterns assume reactive by default (see `EKSAD_CODING_STANDARDS.md`).

**Alternatives Considered**
1. **Spring Boot imperative** — rejected: higher memory, requires more pods at target throughput.
2. **Vert.x raw** — rejected: too low-level; team productivity loss.

**References**
- `EKSAD_BASE_PRINCIPLES.md` §Tech Stack
- `EKSAD_CODING_STANDARDS.md`

---

## 12. References

- `EKSAD_BASE_PRINCIPLES.md`
- `EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- `EKSAD_DOMAIN_REGISTRY.md`
- `EKSAD_DOMAIN_GLOSSARY.md`
- `EKSAD_CODING_STANDARDS.md`
- `EKSAD_MASTER_DATA_PATTERNS.md`
- `EKSAD_CACHE_SYNC_PATTERNS.md`
- `EKSAD_EVENT_CATALOG.md`
- `EKSAD_MULTI_TENANCY_PATTERNS.md`
- `EKSAD_CORE_AUTH_PATTERNS.md`
- `EKSAD_RESILIENCE_PATTERNS.md`
- `EKSAD_OBSERVABILITY_PATTERNS.md`
- `EKSAD_DB_DEPLOYMENT_STRATEGY.md`
- `EKSAD_RESERVED_FIELD_PATTERNS.md`
- `EKSAD_TESTING_GUIDE.md`
- `EKSAD_CICD_CONTAINER_PATTERNS.md`

---

*End of template. Fill in `[...]` placeholders per project.*
