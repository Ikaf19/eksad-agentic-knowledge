# Business Requirements Document (BRD)
# {PROJECT_NAME} — Version {VERSION}

**Document Version:** {VERSION}
**Date:** {DATE}
**Prepared by:** {PREPARED_BY}
**System:** `{ARTIFACT_ID}` (`{SERVICE_NAME}`)
**Organization:** PT EKSAD / {BUSINESS_UNIT}
**Classification:** Internal — Confidential
**Status:** 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)*

> **Related Documents:**
> - `FSD_{PROJECT_CODE}_v{VERSION}.md` — Functional specification
> - `TSD_{PROJECT_CODE}_v{VERSION}.md` — Technical specification

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Background & Problem Statement](#2-business-background--problem-statement)
3. [Objectives](#3-objectives)
4. [Scope](#4-scope)
5. [Stakeholders](#5-stakeholders)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Business Rules](#8-business-rules)
9. [Data Model Summary](#9-data-model-summary)
10. [System Architecture Overview](#10-system-architecture-overview)
11. [Multi-Tenant & SaaS Considerations](#11-multi-tenant--saas-considerations)
12. [Assumptions & Dependencies](#12-assumptions--dependencies)
13. [Risks & Mitigations](#13-risks--mitigations)
14. [Appendix A — Glossary](#appendix-a--glossary)
15. [Appendix B — Change Log](#appendix-b--change-log)

---

## 1. Executive Summary

> *Write 2–4 paragraphs summarizing: what the system is, why it exists, who uses it, and what the key improvements are over the previous version or current manual process.*

**{PROJECT_NAME}** is a **{SHORT_DESCRIPTION}** built on the EKSAD microservices platform (Java 21 + Quarkus 3.30.6).

**Key capabilities:**
- {CAPABILITY_1}
- {CAPABILITY_2}
- {CAPABILITY_3}

**Key improvements over {PREVIOUS_SYSTEM / manual process}:**

| Area | Before | After |
|------|--------|-------|
| {AREA_1} | {BEFORE_1} | {AFTER_1} |
| {AREA_2} | {BEFORE_2} | {AFTER_2} |
| Audit Trail | Manual / none | Automatic via `eksad-core-audittrail` (MongoDB) |
| Multi-Tenant | Single tenant | `tenant_id` isolation on all data |

---

## 2. Business Background & Problem Statement

### 2.1 Business Background

> *Describe the business context: what organization/team uses this system, what process it supports, and why it matters.*

{ORGANIZATION_NAME} is responsible for {BUSINESS_FUNCTION}. Currently, {N} {BUSINESS_PROCESS_TYPE}s are managed:

| Type | Frequency | Description |
|------|-----------|-------------|
| {TYPE_1} | {FREQUENCY_1} | {DESCRIPTION_1} |
| {TYPE_2} | {FREQUENCY_2} | {DESCRIPTION_2} |

### 2.2 Problem Statement

The current system / process suffers from the following problems:

| # | Problem | Impact |
|---|---------|--------|
| P1 | {PROBLEM_1} | {IMPACT_1} |
| P2 | {PROBLEM_2} | {IMPACT_2} |
| P3 | {PROBLEM_3} | {IMPACT_3} |

> **Tip for BA:** Each problem should link to at least one Functional Requirement in Section 6.
> Use the pattern: *"P{N} is addressed by FR-{MODULE}-{NNN}"*

---

## 3. Objectives

> *Use SMART format: Specific, Measurable, Achievable, Relevant, Time-bound.*

| # | Objective | Measurable Success Criteria | Target Date |
|---|-----------|----------------------------|-------------|
| O1 | {OBJECTIVE_1} | {SUCCESS_CRITERIA_1} | {DATE_1} |
| O2 | {OBJECTIVE_2} | {SUCCESS_CRITERIA_2} | {DATE_2} |
| O3 | {OBJECTIVE_3} | {SUCCESS_CRITERIA_3} | {DATE_3} |

---

## 4. Scope

### 4.1 In Scope

| # | Feature / Module | Description |
|---|-----------------|-------------|
| 1 | {FEATURE_1} | {DESCRIPTION_1} |
| 2 | {FEATURE_2} | {DESCRIPTION_2} |
| 3 | {FEATURE_3} | {DESCRIPTION_3} |
| 4 | Audit Trail | All CRUD operations automatically audited via `eksad-core-audittrail` |
| 5 | Multi-Tenant Isolation | All data scoped by `tenant_id` from JWT |

### 4.2 Out of Scope

| # | Item | Reason |
|---|------|--------|
| 1 | {ITEM_1} | {REASON_1} |
| 2 | {ITEM_2} | {REASON_2} |
| 3 | Mobile application | Web-only in this version |

### 4.3 Future Scope (Backlog)

- {FUTURE_ITEM_1}
- {FUTURE_ITEM_2}

---

## 5. Stakeholders

| Role | Name / Team | Responsibility | Type |
|------|-------------|----------------|------|
| Product Owner | {NAME} | Final sign-off on requirements and priorities | Internal |
| Business Analyst | {NAME} | Requirements elicitation, document ownership | Internal |
| Tech Lead | {NAME} | Architecture decisions, code review | Internal |
| Backend Developer | {TEAM} | Service implementation | Internal |
| QA Engineer | {NAME} | Test case design, UAT coordination | Internal |
| {EXTERNAL_ROLE} | {NAME} | {RESPONSIBILITY} | External |
| End User | {USER_GROUP} | {USER_RESPONSIBILITY} | {TYPE} |

---

## 6. Functional Requirements

> **ID Format:** `FR-{MODULE}-{NNN}` (three-digit zero-padded number)
> **Priority:** P1 = Must Have, P2 = Should Have, P3 = Nice to Have

### 6.1 {MODULE_1_NAME} Module

| ID | Requirement | Priority | Related BR | Addresses Problem |
|----|-------------|----------|------------|-------------------|
| FR-{MODULE1}-001 | {REQUIREMENT_1} | P1 | BR-{N} | P{N} |
| FR-{MODULE1}-002 | {REQUIREMENT_2} | P1 | BR-{N} | P{N} |
| FR-{MODULE1}-003 | {REQUIREMENT_3} | P2 | — | — |

### 6.2 {MODULE_2_NAME} Module

| ID | Requirement | Priority | Related BR | Addresses Problem |
|----|-------------|----------|------------|-------------------|
| FR-{MODULE2}-001 | {REQUIREMENT_1} | P1 | BR-{N} | P{N} |
| FR-{MODULE2}-002 | {REQUIREMENT_2} | P2 | — | — |

### 6.3 Authentication & Authorization

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-AUTH-001 | All APIs must require a valid JWT Bearer token (RS256) | P1 | Via `eksad-core-common` SmallRye JWT |
| FR-AUTH-002 | JWT must carry `tenant_id`, `user_id`, `role`, and `permissions` claims | P1 | Enforced by auth service |
| FR-AUTH-003 | Role-based access control (RBAC) must be enforced per endpoint | P1 | Via `@RolesAllowed` annotation |

### 6.4 Audit Trail

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-AUDIT-001 | All CREATE, UPDATE, DELETE operations must be automatically logged | P1 | Auto via `BaseRepository.createFlow/updateFlow/deleteFlow` |
| FR-AUDIT-002 | Audit log must capture: actor, timestamp, data before, data after, action, module type | P1 | `LogActivityDTO` schema |
| FR-AUDIT-003 | Audit logs must be queryable by module type, actor, and date range | P2 | Via `eksad-core-audittrail` REST API |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | API response time (p95) for read operations | ≤ 200ms |
| NFR-002 | API response time (p95) for write operations | ≤ 500ms |
| NFR-003 | System must handle concurrent users | {N} concurrent users |
| NFR-004 | Audit log write must not block main transaction | Async fire-and-forget via RabbitMQ |

### 7.2 Security

| ID | Requirement |
|----|-------------|
| NFR-005 | All endpoints must use HTTPS in production |
| NFR-006 | JWT RS256 validation on every request |
| NFR-007 | No credentials hard-coded — all via environment variables |
| NFR-008 | Sensitive data (passwords, tokens) must be hashed or encrypted at rest |
| NFR-009 | `tenant_id` isolation: users must never access data from another tenant |
| NFR-010 | File uploads must be routed through `eksad-core-storage` only — domain services must not call S3/R2 directly |
| NFR-011 | Domain services must store only `file_id` (BIGINT) referencing `eksad-core-storage` — never raw S3 keys or CDN URLs |

### 7.3 Availability & Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-012 | Service uptime | ≥ 99.5% (excluding planned maintenance) |
| NFR-013 | RabbitMQ message delivery for audit events | At-least-once delivery |
| NFR-014 | Database schema changes via Flyway only | Zero manual DDL in production |

### 7.4 Scalability

| ID | Requirement |
|----|-------------|
| NFR-015 | Service must be horizontally scalable (stateless) |
| NFR-016 | No session state stored in-process — all state in DB |

### 7.5 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-017 | All services must expose OpenAPI / Swagger UI at `/q/swagger-ui` |
| NFR-018 | All services must expose health endpoint at `/q/health` |
| NFR-019 | Unit test coverage ≥ 70% for service layer |

---

## 8. Business Rules

> **ID Format:** `BR-{NNN}`

| ID | Rule | Module | Priority |
|----|------|--------|----------|
| BR-001 | {RULE_1} | {MODULE} | P1 |
| BR-002 | {RULE_2} | {MODULE} | P1 |
| BR-003 | A record must never be hard-deleted. Use `deleted_at` + `deleted_by` (soft delete). | All | P1 |
| BR-004 | Every data-modifying operation must produce an audit log entry with `tenant_id`. | All | P1 |
| BR-005 | {RULE_5} | {MODULE} | P2 |
| BR-PLATFORM-006 | Files must be uploaded through `eksad-core-storage` only. Domain services store `file_id` (BIGINT), never raw S3 keys or CDN URLs. | All | P1 |
| BR-PLATFORM-007 | PUBLIC files are served via permanent CDN URL. PRIVATE files are served via short-lived signed CDN URL generated at request-time (TTL = `STORAGE_SIGNED_URL_TTL_SECONDS`, default 300 seconds). | All | P1 |
| BR-PLATFORM-008 | Thumbnail visibility inherits from its parent file. A PRIVATE file always has a PRIVATE thumbnail. | All | P1 |
| BR-PLATFORM-009 | File size and MIME type are enforced at upload by `eksad-core-storage`. Domain services must not re-validate these. | All | P1 |

---

## 9. Data Model Summary

> *High-level entity list — detailed DDL goes in TSD.*

| Entity | Table Name | Key Fields | Relationships |
|--------|------------|------------|---------------|
| {ENTITY_1} | `{TABLE_1}` | `id`, `tenant_id`, `{KEY_FIELD_1}`, `{KEY_FIELD_2}` | {RELATIONSHIP} |
| {ENTITY_2} | `{TABLE_2}` | `id`, `tenant_id`, `{KEY_FIELD_1}` | belongs to {ENTITY_1} |
| Audit Log | `log_activity` (MongoDB) | `_id`, `transaction_id`, `action`, `tenant_id` | standalone |

### 9.1 Standard Base Fields (All Entities)

Every entity extends `BaseEntity` from `eksad-core-common` which provides:

| Column | Type | Description |
|--------|------|-------------|
| `created_at` | `BIGINT` | Epoch milliseconds — creation timestamp |
| `created_by` | `VARCHAR` | Username from JWT |
| `updated_at` | `BIGINT` | Epoch milliseconds — last update timestamp |
| `updated_by` | `VARCHAR` | Username from JWT |
| `deleted_at` | `BIGINT` | Epoch milliseconds — soft delete timestamp (NULL = active) |
| `deleted_by` | `VARCHAR` | Username who deleted |

---

## 10. System Architecture Overview

```
                      ┌─────────────────────────────────┐
                      │        eksad-gateway :8080        │
                      │   JWT filter · routing · CORS     │
                      └───────────────┬─────────────────┘
                                      │ HTTP routes to
              ┌──────────────────────┼───────────────────┐
              │                      │                   │
       :{PORT} │               :{PORT}│            :{PORT}│
   eksad-auth  │  {SERVICE_NAME_2}   │  {SERVICE_NAME_3} │
              │                      │                   │
              └──────────────────────┴───────────────────┘
                                      │
                            RabbitMQ  │  (exc-log-activity · exc-file-processing)
                                      │
              ┌───────────────────────┼──────────────────┐
              │                       │                  │
       :8089  │                :8090  │           :{PORT}│
 eksad-core-audittrail   eksad-core-storage  {OTHER_SERVICE}
     (MongoDB)           (PostgreSQL + S3/R2)
```

### 10.1 Design Principles

1. **No business logic in gateway** — only JWT auth + routing
2. **Each service owns its schema** — no cross-schema JOINs
3. **Events over synchronous calls** — async via RabbitMQ; only gateway→service is HTTP
4. **`tenant_id` everywhere** — every row, every JWT claim, every event message
5. **Flyway only** — no `ddl-auto=update`; all schema changes in versioned SQL
6. **Auto audit trail** — all CRUD through `BaseRepository` flows; no manual RabbitMQ wiring needed

---

## 11. Multi-Tenant & SaaS Considerations

| Aspect | Implementation |
|--------|---------------|
| Tenant identification | `tenant_id` claim in JWT, validated on every request |
| Data isolation | Hibernate `@Filter` on all entities: `WHERE tenant_id = :tenantId` |
| Tenant provisioning | Via `eksad-auth` service master data |
| Cross-tenant access | Forbidden by default — requires explicit super-admin role |
| Configuration per tenant | Stored in `tenant_config` table, loaded at startup |
| {CUSTOM_TENANT_RULE} | {IMPLEMENTATION} |

---

## 12. Assumptions & Dependencies

### 12.1 Assumptions

| # | Assumption |
|---|------------|
| A1 | `eksad-core-audittrail` service is running and accessible via RabbitMQ |
| A2 | JWT RS256 key pair is provisioned and public key is distributed to all services |
| A3 | RabbitMQ cluster is available with exchange `exc-log-activity` declared |
| A4 | *(If service handles file uploads)* `eksad-core-storage` is running and accessible at `:8090`; RabbitMQ exchange `exc-file-processing` is declared |
| A5 | {CUSTOM_ASSUMPTION} |

### 12.2 Dependencies

| Dependency | Type | Owner | Version / Notes |
|------------|------|-------|-----------------|
| `eksad-core-common` | Maven Library | EKSAD Platform Team | `1.0.0-SNAPSHOT` |
| `eksad-core-audittrail` | Running Service | EKSAD Platform Team | Must be deployed first |
| RabbitMQ | Infrastructure | DevOps | `>= 3.12` |
| PostgreSQL | Infrastructure | DevOps | `>= 15` |
| MongoDB | Infrastructure | DevOps | `>= 6.0` (Atlas or self-hosted) |
| `eksad-core-storage` | Running Service | EKSAD Platform Team | *(Conditional)* Required only if this service handles file uploads. Runs at `:8090`. AWS S3 or Cloudflare R2 must be provisioned. |
| {CUSTOM_DEPENDENCY} | {TYPE} | {OWNER} | {VERSION} |

---

## 13. Risks & Mitigations

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| R1 | RabbitMQ unavailable — audit events lost | Low | Medium | Fire-and-forget; queue has durability enabled; dead-letter queue configured |
| R2 | `tenant_id` filter bypass due to missing annotation | Medium | High | Code review checklist; `BaseRepository` enforces filter automatically |
| R3 | {CUSTOM_RISK_1} | {PROBABILITY} | {IMPACT} | {MITIGATION} |
| R4 | {CUSTOM_RISK_2} | {PROBABILITY} | {IMPACT} | {MITIGATION} |
| R5 | Scope creep from undocumented business rules | High | Medium | All rules must be captured in BR-{N} before development starts |

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| Tenant | An isolated organizational unit within the EKSAD multi-tenant platform |
| `tenant_id` | Unique identifier for a tenant, present in every JWT and every DB row |
| BaseEntity | Superclass from `eksad-core-common` providing audit columns (created_at, updated_at, deleted_at, etc.) |
| Soft Delete | Marking a record as deleted via `deleted_at` timestamp instead of removing the row |
| `CrudFlows` | Generic interface in `eksad-core-common` providing auto-audited CRUD operations |
| `BaseRepository` | Abstract class implementing `CrudFlows`, extended by every service repository |
| Module Type | String identifier for audit log categorization in format `<PROJECT>.<MODULE>.<ACTION>` |
| JWT | JSON Web Token — RS256 signed bearer token for authentication and authorization |
| Flyway | Database migration tool — all schema changes versioned in SQL files |
| `file_id` | A `BIGINT` stored in a domain entity referencing a file record in `eksad-core-storage`. Never store raw S3 keys or CDN URLs — store only `file_id`. |
| File Visibility | Every file in `eksad-core-storage` is either `PUBLIC` (permanent CDN URL) or `PRIVATE` (short-lived signed URL, TTL default 300 s). |
| Signed URL | A time-limited, tamper-proof URL granting temporary access to a PRIVATE file. Generated per request by `eksad-core-storage`. |
| `eksad-core-storage` | Dedicated EKSAD core service (`:8090`) handling all file uploads, metadata, CDN URL resolution, and thumbnail generation. |
| {DOMAIN_TERM_1} | {DEFINITION_1} |
| {DOMAIN_TERM_2} | {DEFINITION_2} |

---

## Appendix B — Change Log

| Version | Date | Author | Summary of Changes |
|---------|------|--------|-------------------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `eksad-core-storage` to architecture, NFR-010/011, BR-PLATFORM-006–009, dependency, assumption, and glossary entries |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |
