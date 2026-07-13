# EKSAD BA Domain Glossary
# Business Analysis Terms & Process Reference

**Version:** 1.1
**Date:** 2026-05-23
**Owner:** EKSAD Platform Team
**Audience:** Business Analysts (via BA GPT Knowledge)

> This file is uploaded as a **Custom GPT knowledge file** for the **BA GPT only**.
> It defines approved BA terminology, document pipeline stages, requirement ID formats,
> and EKSAD-specific business rules that apply to all BA documentation.

---

## Part A — Document Types & Pipeline

### A.1 Document Types

| Term | Definition | Abbreviation | Notes |
|---|---|---|---|
| **User Requirement** | A structured statement of a business need, derived from User Stories or stakeholder input. Forms the foundation of the BRD. Must be confirmed by the user before BRD work begins. | UR | ID format: `UR-[DOMAIN]-[NNN]` |
| **Business Requirement Document** | A document capturing what a system must achieve and why, written at the business level without technical implementation detail. Produced after User Requirements are confirmed. | BRD | Must be baselined before FSD begins. |
| **Functional Specification Document** | A document defining how the system must behave in response to user and business needs, at a level sufficient for development and QA. Produced after BRD is baselined. | FSD | Includes flows, state machines, data requirements, NFRs. |
| **Technical Specification Document** | A document defining how the system will be built — architecture, APIs, database schema, infrastructure. Produced by System Analyst or Technical Lead. **Outside BA scope.** | TSD | BA must never produce or reference TSD content. |

---

### A.2 The Document Pipeline — Sequence Is Enforced

```
[User Stories]  ←  optional raw input
      │
      ▼
[User Requirements (UR)]  ←  MUST be confirmed before BRD
      │
      ▼
[Business Requirement Document (BRD)]  ←  MUST be baselined before FSD
      │
      ▼
[Functional Specification Document (FSD)]
```

This sequence **cannot be skipped, reversed, or compressed** without explicit user acknowledgement and a version history note.

---

## Part B — Requirement Types & ID Formats

### B.1 Requirement ID Standards

All requirement IDs must follow this format exactly. No ID may be reused or skipped.

| Type | Format | Example | Notes |
|---|---|---|---|
| User Requirement | `UR-[DOMAIN]-[NNN]` | `UR-AUTH-001` | Derived from User Stories |
| Business Requirement | `BR-[NNN]` | `BR-012` | Must map to at least one UR |
| Feature | `F-[NNN]` | `F-005` | Groups related FRs; bridges BRD → FSD |
| Functional Requirement | `FR-[MODULE]-[NNN]` | `FR-LEAVE-003` | Must map to exactly one Feature |
| Non-Functional Requirement | `NFR-[NNN]` | `NFR-007` | Must be quantified and testable |
| Business Rule | `RULE-[NNN]` | `RULE-012` | Governing constraint or policy |
| User Story | `US-[MODULE]-[NNN]` | `US-AUTH-001` | Input; converted to URs |
| UI Element | `UI-[NNN]` | `UI-014` | Maps to FR in UI Mapping section |

---

### B.2 Traceability Chain

Every element in a BRD or FSD must be traceable upward:

```
UR-[DOMAIN]-[NNN]
    └── BR-[NNN]  (Business Requirement)
            └── F-[NNN]  (Feature)
                    └── FR-[MODULE]-[NNN]  (Functional Requirement)
```

**Rules:**
- Every BR must map to at least one UR. **No orphan BRs.**
- Every Feature must map to at least one BR. **No orphan Features.**
- Every FR must map to exactly one Feature. **No orphan FRs.**

---

## Part C — Process & Flow Terms

| Term | Definition | Notes |
|---|---|---|
| **Main Flow** | The step-by-step happy path through a process — the sequence of actions when everything goes as expected. | Every feature must have exactly one main flow. |
| **Alternative Flow** | A valid deviation from the main path that still results in a successful outcome. | Minimum one per feature. |
| **Exception Flow** | An error or failure path — what happens when a condition is not met or something goes wrong. | Minimum one per feature. |
| **Precondition** | The state that must be true before a process flow can begin. | Documented per feature. |
| **Postcondition** | The state that is true after the main flow completes successfully. | Documented per feature. |
| **State Machine** | A model of all valid statuses an entity can have, and all the transitions between those statuses — including triggers, actors, and conditions. | Required for any entity with a status field. |
| **Approval Workflow** | A structured multi-step human review process where a record moves through states (e.g., DRAFT → SUBMITTED → APPROVED / REJECTED) via authorised actors. | Requires: state table + transition table + ASCII diagram + BRs. |
| **As-Is Process** | How the business currently operates before the proposed system or change is in place. | Documented in BRD Section 6.1. |
| **To-Be Process** | How the business will operate after the solution is delivered. | Documented in BRD Section 6.2. |
| **Guard** | A condition that must be true for a state transition to be allowed. Example: *"can only APPROVE if current status is SUBMITTED."* | Part of every state machine transition definition. |

---

## Part D — Actors & Roles

| Term | Definition | Notes |
|---|---|---|
| **Actor** | Any human role or system that interacts with the solution. | Must appear in at least one process flow. |
| **Human Actor** | A person in a specific role who performs actions within the system. | e.g., Manager, Admin, Employee |
| **System Actor** | An automated process or external system that exchanges data or triggers events. | e.g., Notification Service, Payment Gateway |
| **Stakeholder** | Any individual or group with an interest in the outcome of the project. | Broader than actors — includes decision-makers who may not use the system directly. |

---

## Part E — Quality & Validation Terms

| Term | Definition | Notes |
|---|---|---|
| **Acceptance Criteria** | Testable conditions that define when a requirement is satisfied. Written in Given / When / Then format. | Required for every FR. |
| **Gap** | A missing requirement, undefined rule, incomplete flow, or unresolved ambiguity in a document. | Classified as Critical or Non-Critical. |
| **Critical Gap** | A gap that blocks document approval — missing core business logic, undefined main flow, or missing key requirement. | Must be resolved before approval. Stop and ask the user. |
| **Non-Critical Gap** | A minor missing detail or low-impact edge case. | Document may proceed; gap must be annotated with `⚠️ GAP [NON-CRITICAL]:` and assigned an owner. |
| **Traceability** | The ability to link every requirement back to its source (UR → BR → F → FR). | No orphan elements permitted at any level. |
| **Definition of Done** | The complete checklist of conditions a document must satisfy before it is considered finished. | See `GPT_BA_SYSTEM_INSTRUCTIONS.md` Part D §17 for the full checklist. |

---

## Part F — EKSAD Platform Business Rules

The following business rules apply **automatically to every EKSAD project**. The BA must include these in all BRDs without prompting from the user.

| ID | Rule | Business Rationale |
|---|---|---|
| BR-PLATFORM-001 | Records must never be permanently deleted. Use soft delete (`deleted_at` timestamp). | Data integrity and auditability — deleted records must be recoverable by admins. |
| BR-PLATFORM-002 | Every data-modifying action must be automatically recorded in the audit trail. | Compliance, traceability, and dispute resolution across all tenants. |
| BR-PLATFORM-003 | Users must only access data belonging to their own tenant. | Multi-tenant data isolation — a tenant must never see another tenant's data. |
| BR-PLATFORM-004 | All API access requires authentication (valid JWT token). | Security — unauthenticated access is forbidden on all endpoints. |
| BR-PLATFORM-005 | Access to features is controlled by user roles (RBAC). | Authorization — users can only perform actions their role explicitly permits. |

---

## Part G — EKSAD Business Context Terms

| Term | Business Meaning | Notes |
|---|---|---|
| **EKSAD / PT EKSAD** | The company. Also referred to as "Eksad Group". Builds and operates a multi-tenant SaaS platform for enterprise clients. | |
| **Tenant** | An independent client organisation using the EKSAD platform. All their data is fully isolated from other tenants. | Sourced from JWT claim `eksad_tenant_id` at the system level. |
| **Multi-Tenant** | One system serving many tenants simultaneously, each with complete data isolation. | A core EKSAD architecture principle. |
| **Microservice** | An independent application handling one specific business domain (e.g., transactions, HR, reporting). | Each service has its own database — no cross-service DB joins. |
| **Audit Trail** | A complete, tamper-proof log of every action taken in the system — who did what, when, and on what data. Automatic in EKSAD. | Stored externally in `eksad-core-audittrail` (MongoDB). BA documents must state audit trail as a requirement; BA does not design how it is stored. |
| **Soft Delete** | Records are never permanently erased. They are "archived" with a timestamp and invisible to normal users but recoverable by admins. | Maps to BR-PLATFORM-001. BA documents must use the phrase "soft delete" consistently. |
| **RBAC (Role-Based Access Control)** | Authorisation model where permissions are assigned to roles, and users are assigned roles. EKSAD standard roles: `ROLE_SUPER_ADMIN`, `ROLE_ADMIN`, `ROLE_VIEWER`, plus domain-specific roles. | Maps to BR-PLATFORM-005. All modules must define a role access matrix. |
| **Module Type** | A string label categorising audit log entries by business module and action. Format: `<PROJECT>.<MODULE>.<ACTION>`. Example: `EKSAD_SVC_LEADS.TRANSACTION.CREATE`. | Referenced in FSD audit requirements. BA documents the label string; SA/Dev implements it. |
| **SaaS (Software as a Service)** | EKSAD platform delivery model — software hosted and provided as a service, multi-tenant, white-label ready. | |
| **Approval Workflow** | Any process where a record moves through human-reviewed states before reaching a final status. Core EKSAD pattern. | Always document with: state table + transition table + ASCII diagram + BRs. |

---

## Part H — Abbreviations Reference

| Abbreviation | Full Term |
|---|---|
| BA | Business Analyst |
| BR | Business Requirement |
| BRD | Business Requirement Document |
| FR | Functional Requirement |
| FSD | Functional Specification Document |
| NFR | Non-Functional Requirement |
| RBAC | Role-Based Access Control |
| SA | System Analyst |
| SDD | System Design Document |
| TL | Technical Lead |
| TSD | Technical Specification Document |
| UR | User Requirement |
| US | User Story |
| QA | Quality Assurance |
| JWT | JSON Web Token |
| SaaS | Software as a Service |
| MDS | Master Data Service (`svc-master-data`) |
| MFA / 2FA | Multi-Factor Authentication / Two-Factor Authentication |
| TSD | Technical Solution Design |
| FSD | Functional Specification Document |
| BRD | Business Requirements Document |
| SLA | Service Level Agreement |
| SLO | Service Level Objective |
| CDC | Change Data Capture |
| ETL | Extract, Transform, Load |
| MDM | Master Data Management |
| IdP | Identity Provider |
| JWKS | JSON Web Key Set |
| OTP | One-Time Password |
| TOTP | Time-based One-Time Password (RFC 6238) |

---

## Multi-Tenancy & Hierarchy Terms (NEW)

| Term | Definition |
|------|------------|
| **Tenant** | An organizational unit (company, subsidiary, branch) with isolated data. Identified by `tenant_id`. |
| **Tenant Hierarchy** | N-level parent-child structure: Group → Company → Division → Branch → … |
| **Group Tenant** | Top-level tenant representing a corporate group (e.g., Astra International). Has children. |
| **Child Tenant** | Tenant with a parent (e.g., AHM under Astra). Inherits parent's config unless overridden. |
| **Platform Tenant** | Reserved `tenant_id = "platform"` for system administrators. Not a real business tenant. |
| **Tenant Scope** | Access level in JWT: `platform` (all tenants), `group` (descendants only), `tenant` (single tenant). |
| **Tenant Provisioning** | Process of creating a new tenant, default admin user, and credentials. Phase 1: manual via API. |
| **Tenant Suspension** | Status change blocking new JWT issuance. Existing JWTs remain valid until expiry. |
| **Tenant Archival** | Final lifecycle state — data moved to cold storage, cannot be reactivated without platform admin. |
| **Materialized Path** | Storage pattern using a `path` string (e.g., `/tenant-astra/tenant-ahm`) for fast hierarchy queries. |
| **Config Inheritance** | Child tenant inherits all config from parent unless explicitly overridden. Child overrides win. |
| **Effective Config** | Resolved configuration after merging child + ancestor chain + platform defaults. |
| **Domain Profile** | Schema-less per-domain user attributes stored in `users` collection (e.g., `branch_id` for Automotive, `employee_id` for HRIS). |

---

## Auth & Security Terms (NEW)

| Term | Definition |
|------|------------|
| **`eksad-core-auth`** | Core infrastructure service for credentials, JWT signing, JWKS. Not visible to business users. |
| **`svc-user-management`** | Business-facing user CRUD service. Calls `eksad-core-auth` via SDK. |
| **JWKS** | Public endpoint exposing JWT signing public keys. Used by all services for token verification. |
| **Key Rotation** | Generating a new JWT signing key while keeping old ones valid until expiry. Zero downtime. |
| **Session Limit** | Maximum concurrent active sessions per user (default 3). When exceeded, oldest session is auto-revoked (kick-oldest). |
| **Lockout** | Temporary block on login after N failed attempts (default 5 → 15 min). Auto-unlocks. |
| **Refresh Token** | Long-lived (30-day) token stored as BCrypt hash. Used to obtain new access tokens. HTTP-only Secure SameSite=Strict cookie. |
| **Device ID** | Client-generated UUID identifying a specific device/browser. Stored with refresh tokens. Enables per-device logout. |
| **Impersonation** | Admin acting on behalf of another user. Audit log records actor + impersonated. |
| **Auth Event** | Log entry for security-relevant actions (login, logout, password change). Stored in `auth_events`, separate from business audit trail. Retention: 90 days. |

---

## Master Data & Cache Terms (NEW)

| Term | Definition |
|------|------------|
| **Master Data** | Catalog/reference data shared across multiple business domains — such as brand/model/type catalog, branch/dealer list, color options, departments/positions. Managed centrally in `svc-master-data` per business domain. Changes propagate automatically to consuming modules. NOT to be confused with inventory data (actual stock/units). |
| **Source of Truth** | The single authoritative system where a specific data entity is created, updated, and validated. For master data, `svc-master-data` is the source of truth — no other service may modify it. |
| **Data Sync** | Automatic propagation of data changes from the source of truth to consuming services. In EKSAD this uses event-driven messaging (RabbitMQ topic exchange `exc-{domain}-master-data`). |
| **Catalog Entity** | Synonym for master data entity. Examples: brands, models, departments, positions. |
| **Reference ID** | Foreign-key-like ID stored in domain entity that points to a master data entity (e.g., `brand_id`). |
| **Cache Sync** | Event-driven process keeping local cache tables up-to-date with master data changes. |
| **Cache Table** | Local denormalized copy of master data in a domain service DB (e.g., `brand_cache`). |
| **Stale Event** | Event older than the last sync timestamp. Must be skipped to prevent regression. |
| **Startup Sync** | Bulk REST fetch on service startup when cache table is empty. |

---

## Reserved Field Terms (NEW)

| Term | Definition |
|------|------------|
| **Reserved Field** | Pre-allocated entity column (5 string, 3 numeric, 2 date, 2 boolean, 1 JSONB) usable for tenant-specific custom fields without DDL changes. |
| **Reserved Field Config** | Database table (`reserved_field_config`) mapping reserved fields to human-readable labels, visibility rules, and validation per tenant. |
| **Config Cascade** | Resolution order for reserved field config: tenant → domain → global defaults. Tenant always wins. |
| **JSONB Overflow** | `reserved_ext JSONB` column for storing additional ad-hoc custom fields beyond the 12 typed slots. |
| **Reserved Field Discovery** | BA workflow step that proactively asks the user about tenant-specific custom fields during FSD creation. |

---

## Resilience Terms (NEW)

| Term | Definition |
|------|------------|
| **Timeout** | Maximum time to wait for an external call before failing. Mandatory for every REST client (default 5s). |
| **Retry** | Re-attempt a failed call with delay/backoff. Only for transient failures (5xx, network). |
| **Circuit Breaker** | Pattern that stops calls to a failing dependency for a cool-down period. States: CLOSED → OPEN → HALF_OPEN. |
| **Fallback** | Alternative response when primary call fails (e.g., return cached data). NEVER used for security-critical ops. |
| **Bulkhead** | Isolating thread pools so one slow dependency doesn't block all requests. |
| **DLQ (Dead Letter Queue)** | RabbitMQ queue capturing messages that failed processing after max retries. |
| **Graceful Degradation** | System continues operating with reduced functionality when a dependency is down. |

---

## Observability Terms (NEW)

| Term | Definition |
|------|------------|
| **Correlation ID** | UUID propagated across services to trace one logical request through all hops. |
| **Structured Logging** | Logs in machine-parseable format (JSON) with standard fields (`correlation_id`, `tenant_id`, etc.). |
| **MDC** | Mapped Diagnostic Context — thread-local key-value store automatically included in log output. |
| **Distributed Tracing** | Capturing spans across services for end-to-end visibility (OpenTelemetry → Jaeger). |
| **Span** | A single operation within a trace (e.g., HTTP request, DB query). |
| **Metrics** | Numeric measurements over time (counters, gauges, histograms). Collected by Micrometer → Prometheus. |
| **Health Check** | Endpoint returning UP/DOWN status. Quarkus: `/q/health/live`, `/q/health/ready`. |

---

*End of EKSAD BA Domain Glossary — Version 1.1*