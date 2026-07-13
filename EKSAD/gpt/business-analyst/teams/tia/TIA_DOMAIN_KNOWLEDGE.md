# TIA Reporting — Domain Knowledge File
# For: Business Analyst GPT (TIA Team Extension)

**Version:** 1.0
**Date:** 2026-04-24
**Owner:** EKSAD Platform Team / TIA Project
**Audience:** BA GPT, SA GPT (upload as additional knowledge file)
**Based on:** BRD_TIA_v2.md · FSD_TIA_v2.2.md · TSD_TIA_v2.md

> This file is uploaded as a **Custom GPT knowledge file** alongside the standard BA GPT files.
> It extends the GPT with TIA-specific domain knowledge — business context, modules, roles, business rules, and data structures.

---

## Part 1 — Project & Business Context

### 1.1 What is TIA Reporting?

**TIA Reporting** is a financial consolidation and reporting platform for **Triputra Group** — an Indonesian conglomerate. The platform is operated by **Triputra Investment Authority (TIA)**, the group's holding company headquarters. TIA collects, reviews, approves, and analyzes periodic financial reports from all **subsidiary companies (SubCo)**.

**System codename:** `tia-reporting-v2`
**Architecture:** Java 21 + Quarkus 3.9.4, event-driven microservices (10 services)
**Database:** PostgreSQL per service + MongoDB Atlas (audit trail)
**Multi-tenant:** `tenant_id` isolation — designed as a licensable SaaS product for other Indonesian holding companies

### 1.2 Why v2 Exists (Legacy Problems Solved)

The v1 system was a Spring Boot monolith with critical problems:

| Problem | Impact | v2 Fix |
|---------|--------|--------|
| God-controller ~19,800 lines, no service layer | Impossible to maintain | Split into 10 independent microservices |
| `getytdoutlookpa` hardcoded `company_id=3583677, year=2023` | All Outlook PA YTD data was wrong for all companies | Fixed with proper parameterized queries |
| Financial values stored as TEXT | Runtime aggregation failures | Changed to `NUMERIC(20,4)` |
| `ddl-auto=update` in production | Schema altered on every deploy | Flyway-only schema management |
| 4 copy-paste approval implementations | Bugs must be fixed 4 times | Single unified Approval Engine service |
| No structured audit trail | Cannot trace who changed what | MongoDB-backed dedicated audit service |
| CAFRM partially implemented | No proper domain model | Standalone `tia-cafrm-service` |
| Single tenant | Not licensable | Multi-tenant with `tenant_id` everywhere |

---

## Part 2 — Report Cycles & Sub-Report Types

### 2.1 Four Report Cycles

| Cycle | Code | Frequency | Purpose |
|-------|------|-----------|---------|
| **Master Budget** | MB | Annual | Budget plan for the upcoming fiscal year |
| **Monthly Report** | MR | Monthly | Actual financial results for the previous month |
| **Outlook PA** | OPA | Annual | Performance Appraisal outlook and annual targets |
| **Rolling Outlook** | RO | Quarterly (Q1, Q2, Q3) | Rolling forecasts (no Q4) |

### 2.2 Eight Sub-Report Types

| Code | Full Name | MB | MR | OPA | RO |
|------|-----------|----|----|-----|----|
| PL | Profit & Loss | ✓ | ✓ | ✓ | ✓ |
| BS | Balance Sheet | ✓ | ✓ | ✓ | ✓ |
| TP | Tax Planning | ✓ | ✓ | ✓ | ✓ |
| FAM | Fixed Assets Movement | ✓ | ✓ | ✓ | ✓ |
| CF | Cash Flow | ✓ | ✓ | ✓ | ✓ |
| LOCF | List of Credit Facilities | ✓ | ✓ | ✓ | ✓ |
| CAT | Corporate Annual Target | ✓ | ✓ | ✓ | ✓ |
| OI | Operating Indicator | ✗ | ✓ | ✗ | ✗ |

> **Note:** OI (Operating Indicator) is only used in Monthly Report, not in MB, OPA, or RO.

### 2.3 Period Rules (BR-2)

| Cycle | Period Calculation |
|-------|--------------------|
| Master Budget | Current year. If current month = December → next year |
| Monthly Report | Current month − 1. If January → December of previous year |
| Rolling Outlook Q1 | Submitted in April |
| Rolling Outlook Q2 | Submitted in July |
| Rolling Outlook Q3 | Submitted in October |
| Rolling Outlook Q4 | **Does not exist** |

---

## Part 3 — User Roles & Access

### 3.1 Core Roles

| Role Code | Category | Description |
|-----------|----------|-------------|
| `superadmin` | System Admin | Full system control. Can bypass approval workflow. Access all companies in their tenant. |
| `user_tia` | HQ Finance | TIA headquarters staff. Views consolidated reports and approves submissions. |
| `user_subco` | SubCo Finance | Subsidiary finance staff. Prepares and submits reports for their assigned companies only. |
| `view_only` | Observer | Read-only access. Cannot edit or submit. |
| `bod` | Board of Directors | High-level dashboard and summary report access only. |
| `stakeholder` | External Viewer | Limited read-only for external parties. |
| `role_reports` | Report Viewer | Report-specific view access only. |

### 3.2 CAFRM Roles (Corporate Audit, Fraud & Risk Management)

| Role Code | Area |
|-----------|------|
| `user_subco_cafrm_internal_audit` | SubCo Internal Audit |
| `user_subco_cafrm_anti_fraud` | SubCo Anti Fraud |
| `user_subco_cafrm_risk_management` | SubCo Risk Management |
| `user_subco_cafrm_ia_af` | SubCo IA + Anti Fraud combined |
| `user_subco_cafrm_ia_rm` | SubCo IA + Risk Management combined |
| `user_subco_cafrm_all` | SubCo all three CAFRM areas |
| `user_tia_cafrm_internal_audit` | HQ Internal Audit viewer/approver |
| `user_tia_cafrm_anti_fraud` | HQ Anti Fraud viewer/approver |
| `user_tia_cafrm_risk_management` | HQ Risk Management viewer/approver |
| `bod_tia_cafrm` | BOD CAFRM read-only |
| `superadmin_cafrm` | Full CAFRM admin |

### 3.3 Key Access Rules

- `user_subco` can **only** view and submit reports for their **assigned companies** (via `user_company` relationship)
- `user_tia` and `superadmin` can view **all companies** within their tenant
- Permissions are data-driven via `role_privileges` (menu + button level)
- All reports, data, and users are isolated by `tenant_id` from the JWT token

---

## Part 4 — Report Submission Lifecycle

### 4.1 Status Flow (All Report Types)

```
[DRAFT] --> [SUBMITTED] --> [APPROVAL_REVIEW] --> [APPROVED]
                                    |
                                    v
                              [REVISION_REQUIRED] --> back to [DRAFT] (new revision)
```

| Status | Description |
|--------|-------------|
| `DRAFT` | Being prepared by SubCo. Editable. |
| `SUBMITTED` | Submitted by SubCo, awaiting completeness check |
| `APPROVAL_REVIEW` | Under approval workflow. Not editable. |
| `APPROVED` | Fully approved. Included in consolidated analytics. |
| `REVISION_REQUIRED` | Rejected by approver. Triggers new revision cycle. |

### 4.2 Submission Pre-conditions (BR-3.7)

Before a report can be submitted:
1. All required sub-report types for the cycle must have at least one detail record saved
2. No existing active approval already in progress for this report
3. The reporting period must be within the valid submission window

### 4.3 Revision Management

- When rejected → new revision is created (revision number incremented)
- Previous revisions are **never deleted** (historical record)
- Only the **latest revision** is used in consolidated analytics (BR-1.1)
- Revision history is viewable per report

### 4.4 3-Tier Data Structure

```
Report Header (Parent)
  └── Report Detail (per sub-report type: PL, BS, TP, etc.)
        └── Detail Values (per line item per month/period)
```

**Header fields:** `company_id`, `period`, `revision`, `current_status`, `created_by`, `created_at`, `approved_at`

**Value fields:** `report_type_code`, `item_report_id`, `attribute`, `year`, `actual_year`, `value`, `currency_id`, `value_format`

---

## Part 5 — Approval Engine

### 5.1 How the Approval Matrix Works

- Each report type has an **approval matrix** defining who approves and in what order
- Matrix entries: `approval_type_id`, `user_id`, `operator_type` (AND/OR), `order_level`, `start_date`, `end_date`
- Approvers are only active within their configured date range (BR-3.1)

### 5.2 AND vs OR at Each Level

| Operator | Behavior |
|----------|----------|
| **AND** | All approvers at this level must individually approve before advancing |
| **OR** | Any single approver approving causes all others at that level to be auto-approved |

### 5.3 Approval Rules (BR-3)

| Rule | Description |
|------|-------------|
| BR-3.1 | Expired matrix entries (past `end_date`) are ignored |
| BR-3.2 | OR operator: one approval auto-completes all peers at that level |
| BR-3.3 | AND operator: all must approve individually |
| BR-3.4 | Levels advance in ascending `order_level` order |
| BR-3.5 | Superadmin can bypass all levels — bypass is recorded in history |
| BR-3.6 | Duplicate submission blocked — if active approval exists, new one cannot be created |

---

## Part 6 — Analytics & Data Rules

### 6.1 What Gets Included in Analytics (BR-1)

| Rule | Description |
|------|-------------|
| BR-1.1 | Only **latest revision** used in consolidated views |
| BR-1.2 | Only status = **APPROVED** included in consolidated views |
| BR-1.3 | Tax Planning uses separate column: `value_tbf` (MB) and `mtd_tbf` (MR). All other types use `value`. |
| BR-1.4 | Tax Planning in Master Budget filters: attribute IN ('actual', 'periode') AND month ≤ target month |

### 6.2 YTD Calculation Rules (BR-2.4, BR-2.5)

| Report Type | YTD Calculation |
|-------------|----------------|
| Monthly Report YTD | Sum months 1 through target month (inclusive) |
| Rolling Outlook YTD | Sum all 12 named month columns (january through december) per quarter record |

> **Critical legacy bug fixed:** In v1, `getytdoutlookpa` was hardcoded with `company_id=3583677` and `year=2023` — meaning ALL companies received the same wrong YTD data. This is fully fixed in v2 with proper parameterized queries.

### 6.3 Formula Evaluation

- Report items (line items) can have formula strings referencing other items by `item_code`
- Formulas are evaluated at query time using a **sandboxed GraalVM JS engine** (replacing deprecated ScriptEngine from v1)
- Items have both `formula` (standard) and `formula_ytd` (YTD variant)

---

## Part 7 — Microservices Architecture

### 7.1 Service Registry

| Service | Port | Responsibility | DB |
|---------|------|---------------|-----|
| `tia-gateway` | 8080 | JWT validation, rate limiting, reverse proxy | None |
| `tia-auth-service` | 8081 | Login, JWT issuance, user credentials, password reset | PostgreSQL `auth` |
| `tia-master-data-service` | 8082 | Companies, BUs, users, roles, report items, currencies, settings, approval matrix | PostgreSQL `masterdata` |
| `tia-submission-service` | 8083 | MB, MR, OPA, RO report submission, Excel import | PostgreSQL `submission` |
| `tia-approval-service` | 8084 | Approval workflow engine (unified for all 4 report types) | PostgreSQL `approval` |
| `tia-aggregation-service` | 8085 | Consolidated analytics, dashboard KPIs, YTD calculations | PostgreSQL `aggregation` |
| `tia-notification-service` | 8086 | Email reminders, scheduling, overdue alerts | PostgreSQL `notification` |
| `tia-file-service` | 8087 | Report attachments, Excel export generation, file lifecycle | PostgreSQL `filestore` |
| `tia-audit-service` | 8088 | Audit trail (write-only), RabbitMQ consumer → MongoDB | MongoDB Atlas `tia_audit` |
| `tia-cafrm-service` | 8089 | Corporate Audit, Fraud & Risk Management module | PostgreSQL `cafrm` |

### 7.2 Shared Module

**`tia-common`** — internal shared library providing:
- `BaseEntity` (common fields: `tenant_id`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`)
- Common DTOs and mappers
- JWT context extraction utilities
- Audit event publisher (RabbitMQ emitter)

### 7.3 Inter-Service Communication Patterns

| Pattern | When Used |
|---------|-----------|
| **HTTP (REST)** | Only gateway → downstream services for user-facing requests |
| **RabbitMQ (async events)** | Service-to-service: audit trail, approval status changes, notifications |
| **No cross-service JOINs** | Each service owns its schema — data is duplicated or fetched via events |

---

## Part 8 — Master Data Entities

### 8.1 Company Hierarchy

Companies are organized in a 3-level hierarchy:
- **Level 1:** Business Unit (BU) — grouping of related subsidiaries
- **Level 2:** Company — legal entity under a BU
- **Level 3:** SubCo — operational subsidiary

Fields: `company_id`, `company_name`, `business_unit_id`, `parent_id`, `level`, `total_report`, `start_date`, `end_date`

### 8.2 Report Item (Line Item) Structure

Each financial report template is built from **report items** (line items):

| Field | Description |
|-------|-------------|
| `item_code` | Unique code, e.g., `PL_001` |
| `item_name` | Display label |
| `report_id` | Which report (PL, BS, TP, etc.) |
| `company_id` | NULL = applies to all companies; value = company-specific override |
| `parent_id` | Parent item for hierarchy grouping |
| `formula` | Formula expression for computed ratio rows |
| `formula_ytd` | YTD formula variant |
| `uom` | Unit of measure (e.g., IDR billion, %) |
| `weight` | Weight for CAT KPI scoring |
| `kpi_type` | KPI type for CAT items |
| `is_can_convert_value` | Whether currency conversion is supported for this item |

### 8.3 Settings

| Setting Group | Types | Purpose |
|--------------|-------|---------|
| `report_submit_period_due_date` | mb, mr, opa, ro_q1, ro_q2, ro_q3 | Submission due date (day of month) per report type per company |
| `day_off` | date list | Configured public holidays for deadline shifting |

---

## Part 9 — Notification Rules (BR-4)

| Rule | Description |
|------|-------------|
| BR-4.1 | Reminders sent on **H+1** (one day after configured due date) |
| BR-4.2 | If H+1 falls on Sunday → shift to Monday |
| BR-4.3 | If shifted date is a configured public holiday → shift by one more day |
| BR-4.4 | Reminders only sent if report is still in DRAFT or SUBMITTED (not APPROVED) |
| BR-4.5 | For SUBMITTED: if not all sub-report types are complete/approved → still send reminder |
| BR-4.6 | Generated Excel export files are auto-deleted after **3 days** |

Email templates are **per-tenant configurable** (not hardcoded). Template variables: `{{company_name}}`, `{{report_type}}`, `{{due_date}}`, `{{period}}`

---

## Part 10 — CAFRM Module

**CAFRM = Corporate Audit, Fraud & Risk Management**

The governance module that tracks:
- **Internal Audit** — audit plans, findings, corrective actions per company
- **Anti-Fraud** — fraud incident reports and monitoring
- **Risk Management** — risk assessments and mitigation tracking

Key rules:
- Each company can be mapped to one or more CAFRM categories
- SubCo CAFRM users only access data for their assigned companies
- TIA CAFRM users can view all companies
- Documents attached to CAFRM activities go through `tia-file-service` (100MB limit)

---

## Part 11 — Financial Data Rules (BR-5)

| Rule | Description |
|------|-------------|
| BR-5.1 | Financial values stored as `NUMERIC` type (not TEXT as in v1) |
| BR-5.2 | Each value record has `currency_id` and `value_format` |
| BR-5.3 | Items with `is_can_convert_value = true` support multi-currency import conversion |
| BR-5.4 | Ratio formulas reference other items by `item_code`, evaluated at query time |
| BR-5.5 | Items may have validation rules: `condition_it_should_be` (expression) and `condition_if_wrong` (error message) |

---

## Part 12 — Multi-Tenant Rules (BR-6)

| Rule | Description |
|------|-------------|
| BR-6.1 | All data isolated by `tenant_id`. Tenant A cannot see Tenant B data. |
| BR-6.2 | `tenant_id` extracted from JWT token on every request |
| BR-6.3 | Superadmin within a tenant is limited to their tenant's data. Platform-level admin can cross tenants. |

**JWT Token Claims:**
| Claim | Description |
|-------|-------------|
| `sub` | User ID |
| `email` | User email |
| `role` | Role code (e.g., `user_subco`) |
| `tenant_id` | Tenant identifier |
| `companies` | Array of company IDs user can access |
| `is_superadmin` | Boolean superadmin bypass flag |
| `exp` | Token expiry timestamp |

Token lifetime: **access token = 15 minutes**, **refresh token = 7 days**

---

## Part 13 — TIA Domain Glossary

| Term | Definition |
|------|-----------|
| **TIA** | Triputra Investment Authority — holding company HQ function |
| **SubCo** | Subsidiary Company |
| **BU** | Business Unit — grouping of related SubCos |
| **MB** | Master Budget — annual budget plan |
| **MR** | Monthly Report — monthly actuals |
| **OPA** | Outlook PA — Performance Appraisal outlook |
| **RO** | Rolling Outlook — quarterly rolling forecast (Q1, Q2, Q3 only) |
| **YTD** | Year-to-Date — cumulative from January to target month |
| **MTD** | Month-to-Date — single month figures |
| **CPSM** | Company Performance Summary Monthly |
| **PL** | Profit & Loss |
| **BS** | Balance Sheet |
| **CF** | Cash Flow |
| **TP** | Tax Planning |
| **FAM** | Fixed Assets Movement |
| **LOCF** | List of Credit Facilities |
| **CAT** | Corporate Annual Target |
| **OI** | Operating Indicator (MR only) |
| **CAFRM** | Corporate Audit, Fraud & Risk Management |
| **KPI** | Key Performance Indicator |
| **H+1** | One day after the configured submission deadline |
| **Revision** | A new version of a rejected report (revision number incremented) |
| **Approval Matrix** | Configuration table defining approvers per report type, order, and date range |
| **AND/OR Operator** | Approval level behavior — AND = all must approve; OR = any one approves auto-completes level |
| **Report Item** | A line item (row) in a financial report template, identified by `item_code` |
| **value_tbf** | Tax Planning column used for Master Budget values (replaces `value`) |
| **mtd_tbf** | Tax Planning column used for Monthly Report values (replaces `value`) |
| **tia-common** | Internal shared library for TIA services (BaseEntity, common DTOs, JWT utilities) |

---

*End of TIA Domain Knowledge v1.0*
*Upload alongside: `EKSAD_BASE_PRINCIPLES.md`, `EKSAD_GENERIC_BRD_TEMPLATE.md`, `EKSAD_GENERIC_FSD_TEMPLATE.md`*
