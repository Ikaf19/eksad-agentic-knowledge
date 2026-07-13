# TIA Reporting — Domain Knowledge File
# For: System Analyst GPT (TIA Team Extension)

**Version:** 1.0
**Date:** 2026-04-24
**Owner:** EKSAD Platform Team / TIA Project
**Audience:** SA GPT (upload as additional knowledge file alongside SA base files)
**Based on:** BRD_TIA_v2.md · FSD_TIA_v2.2.md · TSD_TIA_v2.md

> This file extends the **SA GPT** with TIA-specific technical context — microservice responsibilities,
> DB schema ownership, RabbitMQ event contracts, API routing, and key design decisions.
> For business rules and domain terminology, see the BA variant (`business-analyst/teams/tia/TIA_DOMAIN_KNOWLEDGE.md`).

---

## Part 1 — System Identity

| Item | Value |
|------|-------|
| System Name | `tia-reporting-v2` |
| Group ID | `com.tia` |
| Quarkus Version | `3.9.4` |
| Java Version | `21` |
| Shared Library | `tia-common` (version `1.0.0-SNAPSHOT`) |
| Parent POM | `com.tia:tia-reporting-v2:2.0.0-SNAPSHOT` |

---

## Part 2 — Microservice Registry & Ownership

### 2.1 Service Map

| Service Module | Port | DB Schema | Responsibility |
|----------------|------|-----------|----------------|
| `tia-gateway` | 8080 | — | JWT filter, rate limiting, Vert.x HTTP reverse proxy |
| `tia-auth-service` | 8081 | `auth` | Login, JWT RS256 issuance, refresh, password reset |
| `tia-master-data-service` | 8082 | `masterdata` | Companies, BUs, users, roles, report items, currencies, settings, approval matrix, email templates |
| `tia-submission-service` | 8083 | `submission` | MB, MR, OPA, RO report headers + detail values, Excel import |
| `tia-approval-service` | 8084 | `approval` | Unified approval engine for all 4 report types |
| `tia-aggregation-service` | 8085 | `aggregation` | Consolidated analytics, YTD calculations, dashboard KPIs |
| `tia-notification-service` | 8086 | `notification` | Scheduled email reminders, overdue alerts, deadline tracking |
| `tia-file-service` | 8087 | `filestore` | Report attachments, Excel export generation, 3-day TTL cleanup |
| `tia-audit-service` | 8088 | MongoDB `tia_audit` | Audit trail consumer (RabbitMQ → MongoDB write-only) |
| `tia-cafrm-service` | 8089 | `cafrm` | Corporate Audit, Fraud & Risk Management module |

### 2.2 Shared Module

**`tia-common`** — internal shared library:
- `BaseEntity` (fields: `tenant_id`, `created_at BIGINT`, `created_by VARCHAR`, `updated_at BIGINT`, `updated_by VARCHAR`, `deleted_at BIGINT`, `deleted_by VARCHAR`)
- Common request/response DTOs
- JWT context extractor (`TiaJwtContext`)
- Audit event publisher (fires to RabbitMQ channel `tia.audit.event`)
- Formula engine wrapper (GraalVM JS sandbox)

---

## Part 3 — Architecture Principles (TIA-specific)

1. **No business logic in `tia-gateway`** — JWT validation and routing only
2. **Each service owns its PostgreSQL schema** — no cross-schema JOINs
3. **RabbitMQ for all inter-service communication** — HTTP only for gateway → service
4. **`tenant_id` on every DB row, every JWT claim, every event message**
5. **Flyway only** — all DDL in `V{N}__{description}.sql`, never `ddl-auto=update`
6. **Timestamps as `BIGINT` epoch milliseconds** — all `created_at`, `updated_at`, `deleted_at`
7. **Soft delete** — `deleted_at` + `deleted_by`; never hard-delete
8. **Audit trail is automatic** — services publish to RabbitMQ; `tia-audit-service` consumes and stores in MongoDB

---

## Part 4 — RabbitMQ Event Contracts

### 4.1 Exchanges & Queues

| Exchange | Type | Published By | Consumed By |
|----------|------|-------------|------------|
| `exc-tia-audit` | direct | All services | `tia-audit-service` |
| `exc-tia-approval` | direct | `tia-submission-service` | `tia-approval-service` |
| `exc-tia-notification` | direct | `tia-approval-service` | `tia-notification-service` |
| `exc-tia-aggregation` | direct | `tia-approval-service` | `tia-aggregation-service` |

### 4.2 Core Event Schemas

**Audit Event** (published by all services on any CRUD/state change):
```json
{
  "tenantId": "string",
  "transactionId": "string",
  "action": "string (e.g., MONTHLY_REPORT_SUBMITTED)",
  "activity": "string (human-readable sentence)",
  "createdBy": "user@email.com",
  "createdAt": 1714000000000,
  "role": "user_subco",
  "requestUri": "/api/v2/submission/monthly-report",
  "requestTime": 1714000000000,
  "responseTime": 1714000000050,
  "status": "SUCCESS | FAILED",
  "dataBefore": {},
  "dataAfter": {},
  "dataChanges": [{ "attribute": "current_status", "before": "SUBMITTED", "after": "APPROVAL_REVIEW" }],
  "requestServices": {},
  "logActivityType": 10
}
```

**Approval Requested Event** (`tia-submission-service` → `tia-approval-service`):
```json
{
  "tenantId": "string",
  "reportId": "string",
  "reportType": "MONTHLY_REPORT | MASTER_BUDGET | OUTLOOK_PA | ROLLING_OUTLOOK",
  "companyId": "string",
  "period": "string",
  "revision": 1,
  "submittedBy": "user@email.com",
  "submittedAt": 1714000000000
}
```

**Approval Status Changed Event** (`tia-approval-service` → `tia-notification-service` + `tia-aggregation-service`):
```json
{
  "tenantId": "string",
  "reportId": "string",
  "reportType": "string",
  "companyId": "string",
  "newStatus": "APPROVED | REVISION_REQUIRED",
  "approvedBy": "user@email.com",
  "approvedAt": 1714000000000
}
```

---

## Part 5 — Key Database Schemas

### 5.1 `auth` Schema — `tia-auth-service`

| Table | Key Columns | Notes |
|-------|------------|-------|
| `users` | `id`, `tenant_id`, `email`, `password_hash`, `role`, `is_active` | All BaseEntity columns |
| `refresh_tokens` | `id`, `tenant_id`, `user_id`, `token_hash`, `expires_at BIGINT`, `revoked_at BIGINT` | |

### 5.2 `masterdata` Schema — `tia-master-data-service`

| Table | Key Columns | Notes |
|-------|------------|-------|
| `company` | `id`, `tenant_id`, `company_name`, `business_unit_id`, `parent_id`, `level`, `total_report`, `start_date BIGINT`, `end_date BIGINT` | |
| `business_unit` | `id`, `tenant_id`, `unit_name` | |
| `users` | `id`, `tenant_id`, `email`, `role`, `photo_url` | Profile data (credentials in auth schema) |
| `user_company` | `user_id`, `company_id`, `tenant_id` | M:N mapping |
| `role` | `id`, `tenant_id`, `role_code`, `role_name` | |
| `role_privileges` | `role_id`, `menu_id`, `button_id`, `tenant_id` | Permission control |
| `report_item` | `id`, `tenant_id`, `item_code`, `item_name`, `report_id`, `company_id`, `parent_id`, `formula`, `formula_ytd`, `uom`, `weight`, `kpi_type`, `is_can_convert_value` | |
| `currency` | `id`, `tenant_id`, `code`, `name`, `symbol` | |
| `settings` | `id`, `tenant_id`, `company_id`, `setting_group`, `setting_type`, `value` | |
| `approval_matrix` | `id`, `tenant_id`, `approval_type_id`, `user_id`, `operator_type`, `order_level`, `start_date BIGINT`, `end_date BIGINT` | |
| `email_template` | `id`, `tenant_id`, `template_code`, `subject`, `body_html` | |

### 5.3 `submission` Schema — `tia-submission-service`

| Table | Key Columns | Notes |
|-------|------------|-------|
| `mb_report` | `id`, `tenant_id`, `company_id`, `period`, `revision`, `current_status` | Master Budget header |
| `mb_report_detail` | `id`, `mb_report_id`, `sub_report_type` | PL/BS/TP/FAM/CF/LOCF/CAT/OI |
| `mb_report_value` | `id`, `mb_detail_id`, `item_report_id`, `attribute`, `year`, `value NUMERIC(20,4)`, `currency_id` | **NUMERIC not TEXT** |
| `mr_report` | same pattern | Monthly Report |
| `opa_report` | same pattern | Outlook PA |
| `ro_report` | same pattern | Rolling Outlook |

> **Critical:** All `value` columns are `NUMERIC(20,4)`. Tax Planning reports additionally use `value_tbf` (MB) and `mtd_tbf` (MR) columns.

### 5.4 `approval` Schema — `tia-approval-service`

| Table | Key Columns | Notes |
|-------|------------|-------|
| `approval_request` | `id`, `tenant_id`, `report_id`, `report_type`, `current_level`, `status` | One per report |
| `approval_step` | `id`, `approval_request_id`, `approver_id`, `order_level`, `operator_type`, `status`, `actioned_at BIGINT` | Per approver per level |
| `approval_history` | `id`, `approval_request_id`, `action`, `actioned_by`, `actioned_at BIGINT`, `notes`, `is_bypass` | Full audit history |

### 5.5 MongoDB `tia_audit` — `tia-audit-service`

Collection: `audit_trail`

| Field | Type | Notes |
|-------|------|-------|
| `_id` | ObjectId | |
| `tenantId` | String | |
| `transactionId` | String | ID of the affected record |
| `action` | String | e.g., `MONTHLY_REPORT_SUBMITTED` |
| `activity` | String | Human-readable sentence |
| `createdBy` | String | User email |
| `createdAt` | Long | Epoch milliseconds |
| `role` | String | |
| `requestUri` | String | |
| `status` | String | SUCCESS or FAILED |
| `dataBefore` | Object | JSON snapshot before change |
| `dataAfter` | Object | JSON snapshot after change |
| `dataChanges` | Array | `[{attribute, before, after}]` |
| `logActivityType` | Integer | Numeric category code |

Indexes: `(tenantId, transactionId)`, `(tenantId, createdBy)`, `(tenantId, createdAt)`, `(tenantId, action)`

---

## Part 6 — API Gateway Routing

All external traffic enters via `tia-gateway:8080`. Routes:

| Path Prefix | Downstream Service |
|-------------|-------------------|
| `/api/v2/auth/**` | `tia-auth-service:8081` |
| `/api/v2/masterdata/**` | `tia-master-data-service:8082` |
| `/api/v2/submission/**` | `tia-submission-service:8083` |
| `/api/v2/approval/**` | `tia-approval-service:8084` |
| `/api/v2/aggregation/**` | `tia-aggregation-service:8085` |
| `/api/v2/notifications/**` | `tia-notification-service:8086` |
| `/api/v2/files/**` | `tia-file-service:8087` |
| `/api/v2/audit/**` | `tia-audit-service:8088` |
| `/api/v2/cafrm/**` | `tia-cafrm-service:8089` |

Authentication: The gateway validates JWT RS256 signature and injects `tenant_id`, `role`, `companies` claims into downstream requests. No business logic in the gateway.

---

## Part 7 — Key Technical Decisions (ADRs)

| Decision | Choice | Reason |
|----------|--------|--------|
| Formula evaluation engine | GraalVM JS sandboxed engine | Replaced deprecated `ScriptEngine` from v1; safe, isolated evaluation |
| Financial value type | `NUMERIC(20,4)` | Fixed v1 bug where TEXT storage caused runtime failures |
| Timestamps | `BIGINT` epoch ms | Fast B-tree index, no timezone ambiguity |
| Audit storage | MongoDB Atlas | Schema-less for flexible diff capture; append-only audit log pattern |
| Schema migration | Flyway only | Prevents `ddl-auto=update` risk in production |
| Approval engine | Single unified service | Replaced 4 copy-paste implementations in v1 |
| Excel generation | Apache POI 5.2.5 | Industry standard for Java Excel manipulation |

---

## Part 8 — Domain Glossary (Technical)

| Term | Definition |
|------|-----------|
| `tia-common` | Internal shared Java library — BaseEntity, common DTOs, JWT extractor, audit publisher |
| `BaseEntity` | Common superclass for all TIA entities — includes tenant_id, soft-delete fields, epoch timestamps |
| `value_tbf` | Tax Planning-specific value column for Master Budget (separate from standard `value`) |
| `mtd_tbf` | Tax Planning-specific value column for Monthly Report |
| `approval_type_id` | FK linking an approval matrix entry to a report type definition |
| `operator_type` | AND / OR — determines whether one or all approvers at a level must act |
| `order_level` | Integer — approval levels are processed in ascending order |
| `item_code` | Unique line item identifier, e.g., `PL_001` — referenced in formula expressions |
| `report_type` | Enum: `MASTER_BUDGET`, `MONTHLY_REPORT`, `OUTLOOK_PA`, `ROLLING_OUTLOOK` |
| `sub_report_type` | Enum: `PL`, `BS`, `TP`, `FAM`, `CF`, `LOCF`, `CAT`, `OI` |
| `current_status` | Enum: `DRAFT`, `SUBMITTED`, `APPROVAL_REVIEW`, `APPROVED`, `REVISION_REQUIRED` |
| `logActivityType` | Integer code categorizing the audit action type |
| `H+1` | Business rule term — one working day after the configured submission due date |

---

## Part 9 — Flyway DDL Conventions for TIA

All migration files follow:
```
src/main/resources/db/migration/V{N}__{description}.sql
```

Standard columns every TIA entity table must have (from `BaseEntity`):
```sql
  tenant_id        VARCHAR(100) NOT NULL,
  created_at       BIGINT       NOT NULL,
  created_by       VARCHAR(255),
  updated_at       BIGINT,
  updated_by       VARCHAR(255),
  deleted_at       BIGINT,
  deleted_by       VARCHAR(255)
```

Standard indexes on every table:
```sql
CREATE INDEX idx_{table}_tenant_id ON {table} (tenant_id);
CREATE INDEX idx_{table}_tenant_deleted ON {table} (tenant_id, deleted_at);
```

---

*End of TIA SA Domain Knowledge v1.0*
*Upload alongside: `EKSAD_BASE_PRINCIPLES.md`, `EKSAD_GENERIC_TSD_TEMPLATE.md`, `EKSAD_SYSTEM_DESIGN_PATTERNS.md`*
