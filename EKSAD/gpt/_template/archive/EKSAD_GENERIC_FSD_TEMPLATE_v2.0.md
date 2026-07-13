# Functional Specification Document (FSD)
# {PROJECT_NAME} — Version {VERSION}

**Document Version:** {VERSION}
**Date:** {DATE}
**Prepared by:** {PREPARED_BY}
**System:** `{ARTIFACT_ID}` (`{SERVICE_NAME}`)
**Organization:** PT EKSAD / {BUSINESS_UNIT}
**Classification:** Internal — Confidential
**Status:** 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)*
**Supersedes:** `FSD_{PROJECT_CODE}_v{PREV_VERSION}.md` *(if applicable)*

> **Audience:** Business Analysts, Product Owners, QA Engineers, Frontend Developers.
> This document describes **WHAT** the system does — user flows, business rules, API behavior, and use cases.
> For **HOW** it is built (schemas, tech stack, event contracts), see `TSD_{PROJECT_CODE}_v{VERSION}.md`.

> **Related Documents:**
> - `BRD_{PROJECT_CODE}_v{VERSION}.md` — Business requirements
> - `TSD_{PROJECT_CODE}_v{VERSION}.md` — Technical specification

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [User Roles & Access Matrix](#2-user-roles--access-matrix)
3. [Authentication & Session Management](#3-authentication--session-management)
4. [Module Specifications](#4-module-specifications)
5. [Approval Workflow Engine](#5-approval-workflow-engine)
6. [Audit Trail](#6-audit-trail)
7. [Notification & Scheduling](#7-notification--scheduling)
8. [Business Rules — Master Reference](#8-business-rules--master-reference)
9. [API Endpoint Catalog](#9-api-endpoint-catalog)
10. [Error Code Catalog](#10-error-code-catalog)
11. [Glossary](#11-glossary)
12. [Appendix — Change Log](#appendix--change-log)

---

## 1. System Overview

### 1.1 What This System Does

> *2–3 sentences: what the system is, what business process it automates, and who uses it.*

**{PROJECT_NAME}** is a **{SHORT_DESCRIPTION}** that enables **{PRIMARY_USER_GROUP}** to **{PRIMARY_ACTION}**.

### 1.2 What Has Changed

| Area | Before (v{PREV_VERSION} / Manual) | After (v{VERSION}) |
|------|---------------------------------|-------------------|
| Architecture | {OLD_ARCHITECTURE} | Quarkus microservice on EKSAD platform |
| Authentication | {OLD_AUTH} | Stateless JWT RS256 Bearer token |
| Audit Trail | {OLD_AUDIT} | Automatic via `eksad-core-audittrail` (MongoDB) |
| Multi-Tenant | {OLD_TENANT} | `tenant_id` isolation on all data |
| {CUSTOM_AREA} | {OLD_WAY} | {NEW_WAY} |

### 1.3 Key Modules

| Module | Description | Module Type Prefix |
|--------|-------------|-------------------|
| {MODULE_1} | {DESCRIPTION_1} | `{PROJECT_CODE}.{MODULE1}` |
| {MODULE_2} | {DESCRIPTION_2} | `{PROJECT_CODE}.{MODULE2}` |
| Auth | JWT validation, session management | `{PROJECT_CODE}.AUTH` |
| Audit | Automatic CRUD audit logging | `{PROJECT_CODE}.AUDIT` |

---

## 2. User Roles & Access Matrix

### 2.1 Role Definitions

| Role | Code | Description | Tenant Scope |
|------|------|-------------|-------------|
| Super Admin | `ROLE_SUPER_ADMIN` | Full access across all tenants | Cross-tenant |
| Admin | `ROLE_ADMIN` | Full access within own tenant | Single tenant |
| {ROLE_1} | `ROLE_{ROLE1_CODE}` | {ROLE1_DESCRIPTION} | {SCOPE} |
| {ROLE_2} | `ROLE_{ROLE2_CODE}` | {ROLE2_DESCRIPTION} | {SCOPE} |
| Viewer | `ROLE_VIEWER` | Read-only access | Single tenant |

### 2.2 Access Matrix

> ✅ Allowed | ❌ Forbidden | 🔒 Allowed with restriction

| Feature | Super Admin | Admin | {ROLE_1} | {ROLE_2} | Viewer |
|---------|-------------|-------|----------|----------|--------|
| Create {ENTITY_1} | ✅ | ✅ | ✅ | ❌ | ❌ |
| Update {ENTITY_1} | ✅ | ✅ | 🔒 Own only | ❌ | ❌ |
| Delete {ENTITY_1} | ✅ | ✅ | ❌ | ❌ | ❌ |
| View {ENTITY_1} | ✅ | ✅ | ✅ | ✅ | ✅ |
| Approve / Reject | ✅ | ✅ | ❌ | ✅ | ❌ |
| View Audit Trail | ✅ | ✅ | ❌ | ❌ | ❌ |
| Manage Users | ✅ | ✅ | ❌ | ❌ | ❌ |
| Cross-tenant view | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 3. Authentication & Session Management

### 3.1 Authentication Flow

```
Client
  │
  ├── POST /api/v1/auth/login  { username, password }
  │         │
  │         └── eksad-auth-service validates credentials
  │                   │
  │                   └── Returns { access_token, refresh_token, expires_in }
  │
  ├── All subsequent requests: Authorization: Bearer {access_token}
  │         │
  │         └── Each service validates JWT RS256 signature locally (no round-trip to auth)
  │
  └── POST /api/v1/auth/refresh  { refresh_token }
            │
            └── Returns new { access_token }
```

### 3.2 JWT Payload Structure

```json
{
  "iss": "eksad-auth-service",
  "sub": "{user_email_or_username}",
  "jti": "{uuid}",
  "iat": {epoch_ms},
  "exp": {epoch_ms},
  "groups": ["ROLE_{ROLE_CODE}"],
  "eksad_tenant_id": "{tenant_id}",
  "eksad_user_id": "{user_id}",
  "eksad_role": "{role_code}",
  "eksad_permissions": [
    "{MODULE}_READ",
    "{MODULE}_WRITE",
    "{MODULE}_APPROVE"
  ]
}
```

### 3.3 Token Lifecycle

| Token Type | Expiry | Storage Recommendation |
|------------|--------|----------------------|
| Access Token | 24 hours | Memory only (never localStorage) |
| Refresh Token | 7 days | HttpOnly Secure cookie |

### 3.4 Error Responses for Auth Failures

| Scenario | HTTP Status | Error Code |
|----------|-------------|------------|
| Missing token | 401 | `AUTH_TOKEN_MISSING` |
| Expired token | 401 | `AUTH_TOKEN_EXPIRED` |
| Invalid signature | 401 | `AUTH_TOKEN_INVALID` |
| Insufficient role | 403 | `AUTH_ACCESS_FORBIDDEN` |
| Wrong tenant | 403 | `AUTH_TENANT_MISMATCH` |

---

## 4. Module Specifications

> *Repeat Section 4.x for each module. Copy the block below.*

---

### 4.1 {MODULE_1_NAME} Module

**Purpose:** {MODULE_1_PURPOSE}
**Module Type Prefix:** `{PROJECT_CODE}.{MODULE1_CODE}`

#### 4.1.1 User Stories

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|------------|----------|---------------------|
| US-{MODULE1}-001 | {ROLE} | {ACTION} | {BENEFIT} | P1 | {ACCEPTANCE_CRITERIA} |
| US-{MODULE1}-002 | {ROLE} | {ACTION} | {BENEFIT} | P1 | {ACCEPTANCE_CRITERIA} |
| US-{MODULE1}-003 | {ROLE} | {ACTION} | {BENEFIT} | P2 | {ACCEPTANCE_CRITERIA} |

#### 4.1.2 Entity Lifecycle / State Machine

> *Fill in if this module has stateful records (e.g., a submission, an order, an approval).*
> *Remove if simple CRUD.*

| State | Description | Allowed Transitions | Who Can Trigger |
|-------|-------------|---------------------|-----------------|
| `DRAFT` | Record created but not submitted | → `SUBMITTED` | {ROLE} |
| `SUBMITTED` | Awaiting review | → `REVIEWED`, → `REJECTED` | {APPROVER_ROLE} |
| `REVIEWED` | Under approval | → `APPROVED`, → `REJECTED` | {APPROVER_ROLE} |
| `APPROVED` | Final approved state | — (terminal) | — |
| `REJECTED` | Rejected — can be revised | → `DRAFT` | {ROLE} |

```
DRAFT ──→ SUBMITTED ──→ REVIEWED ──→ APPROVED
                │              │
                └──────────────┴──→ REJECTED ──→ DRAFT (revise)
```

#### 4.1.3 Field Validation Rules

| Field | Type | Required | Validation Rules | Error Message |
|-------|------|----------|-----------------|---------------|
| `{FIELD_1}` | `String` | Yes | Max {N} chars, not blank | `{MODULE1}_FIELD1_INVALID` |
| `{FIELD_2}` | `Long` | Yes | Must be positive epoch ms | `{MODULE1}_FIELD2_INVALID` |
| `{FIELD_3}` | `BigDecimal` | No | Scale ≤ 4, ≥ 0 | `{MODULE1}_FIELD3_INVALID` |
| `tenant_id` | `String` | Yes | Auto-injected from JWT | — |
| `status` | `String` (enum-like) | Yes | One of: `DRAFT`, `SUBMITTED`, `APPROVED`, `REJECTED` | `{MODULE1}_STATUS_INVALID` |
| `{field}_file_id` | `Long` | *(if applicable)* | Must reference a valid file in `eksad-core-storage`; stored as FK by convention (no DB constraint). Set by passing `fileId` returned from `POST /api/v1/storage/upload`. | `{MODULE1}_FILE_INVALID` |

#### 4.1.4 Business Rules for This Module

| ID | Rule |
|----|------|
| BR-{MODULE1}-001 | {RULE_1} |
| BR-{MODULE1}-002 | {RULE_2} |
| BR-{MODULE1}-003 | Once `APPROVED`, a record cannot be modified without creating a new revision. |

#### 4.1.5 Audit Log Actions

| Action | Module Type String | Trigger |
|--------|--------------------|---------|
| Create | `{PROJECT_CODE}.{MODULE1_CODE}.CREATE` | `POST /...` |
| Update | `{PROJECT_CODE}.{MODULE1_CODE}.UPDATE` | `PUT /...` |
| Delete | `{PROJECT_CODE}.{MODULE1_CODE}.DELETE` | `DELETE /...` |
| Submit | `{PROJECT_CODE}.{MODULE1_CODE}.SUBMIT` | `PATCH /.../submit` |
| Approve | `{PROJECT_CODE}.{MODULE1_CODE}.APPROVE` | `PATCH /.../approve` |
| Reject | `{PROJECT_CODE}.{MODULE1_CODE}.REJECT` | `PATCH /.../reject` |

---

### 4.2 {MODULE_2_NAME} Module

> *(Copy block from 4.1 and fill in)*

---

## 5. Approval Workflow Engine

> *Use this section for any module that has multi-step human approval.*
> *Skip if the system has no approval flows.*

### 5.1 Overview

The approval engine is a **generic, configurable state machine** shared across modules. It supports:
- Single-level approval
- Multi-level approval (sequential or parallel — specify which)
- Approval delegation
- Rejection with required reason

### 5.2 Generic Approval States

```
DRAFT → SUBMITTED → [LEVEL_1_REVIEW] → ... → [LEVEL_N_REVIEW] → APPROVED
                                                                  REJECTED (any level)
```

### 5.3 Approval Configuration per Module

| Module | Approval Levels | Level 1 Approver Role | Level 2 Approver Role | Auto-Approve Condition |
|--------|-----------------|-----------------------|-----------------------|----------------------|
| {MODULE_1} | {N} | `ROLE_{APPROVER_1}` | `ROLE_{APPROVER_2}` | {CONDITION or "None"} |
| {MODULE_2} | {N} | `ROLE_{APPROVER_1}` | — | {CONDITION or "None"} |

### 5.4 Approval Actions

| Action | Description | Allowed Roles | Required Fields |
|--------|-------------|---------------|-----------------|
| `submit` | Move from DRAFT → SUBMITTED | Record owner | — |
| `approve` | Advance to next level or APPROVED | Level approver role | `comment` (optional) |
| `reject` | Move to REJECTED | Level approver role | `reason` (required) |
| `revise` | Move from REJECTED → DRAFT | Record owner | `revision_notes` |
| `delegate` | Assign approval to another user | Approver | `delegatee_user_id` |

### 5.5 Notification Triggers

| Event | Recipient | Channel | Template |
|-------|-----------|---------|----------|
| SUBMITTED | Level 1 Approver | Email + In-App | `{TEMPLATE_SUBMITTED}` |
| APPROVED | Record Owner | Email + In-App | `{TEMPLATE_APPROVED}` |
| REJECTED | Record Owner | Email + In-App | `{TEMPLATE_REJECTED}` |
| {CUSTOM_EVENT} | {RECIPIENT} | {CHANNEL} | `{TEMPLATE}` |

---

## 6. Audit Trail

### 6.1 What Gets Logged

Every CRUD operation performed via `BaseRepository` is automatically captured with:

| Field | Source | Example |
|-------|--------|---------|
| `transaction_id` | Entity ID after persist | `"txn-00123"` |
| `action` | Method name passed to flow | `"CREATE"`, `"UPDATE"` |
| `username` | JWT `sub` claim | `"john.doe@eksad.com"` |
| `role` | JWT `eksad_role` claim | `"ROLE_ADMIN"` |
| `status` | Flow outcome | `"SUCCESS"` or `"FAIL"` |
| `fail_reason` | Exception message on failure | `"Data not found"` |
| `request_uri` | Full request URL | `"/api/v1/transactions/create"` |
| `request_services` | Serialized request DTO | JSON string |
| `request_time` | `Instant.now().toEpochMilli()` at entry | `1745280000000` |
| `response_time` | `Instant.now().toEpochMilli()` at exit | `1745280150000` |
| `data_before` | Serialized entity before change | JSON string |
| `data_after` | Serialized entity after change | JSON string |
| `log_activity_type` | Module type string | `"EKSAD_SVC_LEADS.TRANSACTION.CREATE"` |
| `tenant_id` | JWT `eksad_tenant_id` claim | `"eksad-group"` |

### 6.2 Viewing Audit Logs

Audit logs are queryable via `eksad-core-audittrail` REST API:

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/audit?moduleType={type}&page={n}` | List logs by module type |
| `GET /api/v1/audit?actor={username}&page={n}` | List logs by actor |
| `GET /api/v1/audit?from={epoch}&to={epoch}` | List logs by date range |

---

## 7. Notification & Scheduling

> *Skip if the system has no scheduled jobs or notifications.*

### 7.1 Notification Channels

| Channel | Implementation | Config |
|---------|---------------|--------|
| In-App | RabbitMQ event → notification service | Exchange: `exc-notification` |
| Email | SMTP via notification service | Template-based per tenant |

### 7.2 Scheduled Jobs

| Job Name | Trigger | Description | Module Type |
|----------|---------|-------------|-------------|
| {JOB_1} | Cron: `{CRON_EXPRESSION}` | {DESCRIPTION} | `{PROJECT_CODE}.SCHEDULER.{JOB1}` |
| {JOB_2} | Cron: `{CRON_EXPRESSION}` | {DESCRIPTION} | `{PROJECT_CODE}.SCHEDULER.{JOB2}` |

> ⚠️ **Warning:** Quarkus scheduled jobs are NOT thread-safe when using mutable state.
> All scheduler methods must be stateless. Use injected services only.

---

## 8. Business Rules — Master Reference

> *Consolidate all BR-{N} from all modules here for quick reference.*

| ID | Rule | Module | Priority | Source FR |
|----|------|--------|----------|-----------|
| BR-001 | Records must never be hard-deleted (soft delete only) | All | P1 | FR-ALL |
| BR-002 | Every data operation must produce an audit log with `tenant_id` | All | P1 | FR-AUDIT-001 |
| BR-003 | Users cannot access data outside their `tenant_id` | All | P1 | FR-AUTH-009 |
| BR-004 | Financial amounts must use `NUMERIC(20,4)` — never String | {MODULE} | P1 | {FR_ID} |
| BR-PLATFORM-006 | Files must be uploaded through `eksad-core-storage` only. Domain services store `file_id` (BIGINT), never raw S3 keys or CDN URLs. | All | P1 | FR-ALL |
| BR-PLATFORM-007 | PUBLIC files are served via permanent CDN URL. PRIVATE files are served via short-lived signed CDN URL (TTL = `STORAGE_SIGNED_URL_TTL_SECONDS`, default 300 s). | All | P1 | FR-ALL |
| BR-PLATFORM-008 | Thumbnail visibility inherits from its parent file. A PRIVATE file always has a PRIVATE thumbnail. | All | P1 | FR-ALL |
| BR-PLATFORM-009 | File size and MIME type are enforced at upload by `eksad-core-storage`. Domain services must not re-validate these. | All | P1 | FR-ALL |
| BR-{N} | {RULE} | {MODULE} | {PRIORITY} | {FR_ID} |

---

## 9. API Endpoint Catalog

> **Authentication:** All endpoints require `Authorization: Bearer {JWT}` unless marked as `PUBLIC`.
> **Base URL:** `https://{HOST}/api/v{VERSION}`

### 9.1 {MODULE_1_NAME}

| Method | Path | Auth | Request Body / Params | Response | Module Type | Description |
|--------|------|------|-----------------------|----------|-------------|-------------|
| `POST` | `/v1/{module1}` | `ROLE_{X}` | `{Entity1CreateDTO}` | `201 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.CREATE` | Create new {entity1} |
| `GET` | `/v1/{module1}/{id}` | `ROLE_{X}` | Path: `id` | `200 {Entity1ResponseDTO}` | — | Get {entity1} by ID |
| `GET` | `/v1/{module1}` | `ROLE_{X}` | Query: `page`, `size`, `tenantId` | `200 Page<{Entity1ResponseDTO}>` | — | List all {entity1} (paginated) |
| `PUT` | `/v1/{module1}/{id}` | `ROLE_{X}` | `{Entity1UpdateDTO}` | `200 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.UPDATE` | Update {entity1} |
| `DELETE` | `/v1/{module1}/{id}` | `ROLE_{X}` | Path: `id` | `200 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.DELETE` | Soft-delete {entity1} |
| `PATCH` | `/v1/{module1}/{id}/submit` | `ROLE_{X}` | — | `200 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.SUBMIT` | Submit for approval |
| `PATCH` | `/v1/{module1}/{id}/approve` | `ROLE_{APPROVER}` | `{ "comment": "..." }` | `200 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.APPROVE` | Approve record |
| `PATCH` | `/v1/{module1}/{id}/reject` | `ROLE_{APPROVER}` | `{ "reason": "..." }` | `200 {Entity1ResponseDTO}` | `{PROJECT}.{MODULE1}.REJECT` | Reject record |

### 9.2 Authentication

| Method | Path | Auth | Request Body | Response | Description |
|--------|------|------|-------------|----------|-------------|
| `POST` | `/v1/auth/login` | PUBLIC | `{ username, password }` | `200 { access_token, refresh_token, expires_in }` | Login |
| `POST` | `/v1/auth/refresh` | PUBLIC | `{ refresh_token }` | `200 { access_token }` | Refresh token |
| `POST` | `/v1/auth/logout` | Bearer | — | `200 { message }` | Logout |

### 9.3 File Storage *(include only if this service handles file uploads)*

> These endpoints belong to `eksad-core-storage` (`:8090`), **not** this domain service.
> The client calls `eksad-core-storage` directly to upload a file and receives a `fileId`.
> The domain service API then receives that `fileId` as part of its own create/update request body.

| Method | Path (on `eksad-core-storage`) | Auth | Request Body / Params | Response | Description |
|--------|-------------------------------|------|-----------------------|----------|-------------|
| `POST` | `/api/v1/storage/upload` | Bearer | Multipart: `file`, `visibility` (`PUBLIC`/`PRIVATE`), `refEntityType`, `refEntityId` | `201 { fileId, cdnUrl? }` | Upload file. `cdnUrl` returned for PUBLIC files only. Store the returned `fileId` in the domain entity. |
| `GET` | `/api/v1/storage/{fileId}/url` | Bearer | Path: `fileId` | `200 { url, expiresAt? }` | Resolve file URL. Permanent for PUBLIC; short-lived signed URL for PRIVATE. Call at render-time — do not cache signed URLs. |
| `GET` | `/api/v1/storage/{fileId}/thumbnail-url` | Bearer | Path: `fileId` | `200 { url, expiresAt? }` | Resolve thumbnail URL. Falls back to original file URL if thumbnail generation failed or is pending. |
| `DELETE` | `/api/v1/storage/{fileId}` | Bearer | Path: `fileId` | `200 { message }` | Soft-delete file metadata and remove from object storage. |

---

## 10. Error Code Catalog

### 10.1 Standard Error Response Format

```json
{
  "status": "FAIL",
  "code": "{ERROR_CODE}",
  "message": "{Human readable message}",
  "timestamp": {epoch_ms},
  "path": "{request_path}"
}
```

### 10.2 Error Codes

| Code | HTTP Status | Message | Trigger |
|------|-------------|---------|---------|
| `AUTH_TOKEN_MISSING` | 401 | Authentication token is required | No Authorization header |
| `AUTH_TOKEN_EXPIRED` | 401 | Token has expired | JWT `exp` passed |
| `AUTH_TOKEN_INVALID` | 401 | Token signature is invalid | Bad JWT signature |
| `AUTH_ACCESS_FORBIDDEN` | 403 | You do not have permission to perform this action | Wrong role |
| `AUTH_TENANT_MISMATCH` | 403 | Access to this tenant is not allowed | `tenant_id` mismatch |
| `{MODULE1}_NOT_FOUND` | 404 | {Entity1} not found | `findById` returns empty |
| `{MODULE1}_INVALID_STATE` | 422 | Cannot perform this action in current state | State machine violation |
| `{MODULE1}_FIELD1_INVALID` | 400 | {FIELD_1} is invalid | Validation failure |
| `INTERNAL_SERVER_ERROR` | 500 | An unexpected error occurred | Unhandled exception |
| `{CUSTOM_ERROR_CODE}` | {STATUS} | {MESSAGE} | {TRIGGER} |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| Tenant | An isolated organizational unit within the EKSAD platform |
| `tenant_id` | Unique string identifier for a tenant — present in all JWT tokens and database rows |
| Soft Delete | Records are never permanently deleted. `deleted_at` is set instead of removing the row. |
| Module Type | Dot-separated string identifying the source of an audit event: `<PROJECT>.<MODULE>.<ACTION>` |
| `BaseEntity` | Superclass from `eksad-core-common` with `created_at`, `updated_at`, `deleted_at`, `created_by`, `updated_by`, `deleted_by` |
| `CrudFlows` | Generic reactive CRUD interface in `eksad-core-common` with built-in audit trail |
| `BaseRepository` | Abstract implementation of `CrudFlows` — extend this in every service repository |
| JWT | JSON Web Token — RS256-signed bearer token for authentication |
| Flyway | Database migration tool — all DDL in versioned `.sql` files |
| `file_id` | A `BIGINT` stored in a domain entity referencing a file record in `eksad-core-storage`. The domain service never stores raw S3 keys or CDN URLs — only this ID. URLs are resolved at render-time via `GET /api/v1/storage/{fileId}/url`. |
| File Visibility | Classification of every uploaded file: `PUBLIC` (served via permanent CDN URL) or `PRIVATE` (served via short-lived signed URL, TTL default 300 s). |
| `PUBLIC` file | A file accessible to anyone with the CDN URL. Suitable for logos, brochures, public images. |
| `PRIVATE` file | A file requiring authentication. A signed URL is generated per request. Suitable for contracts, reports, confidential documents. |
| Signed URL | A time-limited, tamper-proof URL for accessing a PRIVATE file. Generated by `eksad-core-storage` at request-time. Frontend must not cache these long-term. |
| Thumbnail | A smaller preview image generated asynchronously after upload. Supported for PNG, JPG, GIF, WEBP, and PDF (page 1). Inherits parent file visibility. Falls back to original file URL if generation fails. |
| `eksad-core-storage` | Dedicated EKSAD core service (`:8090`) for all file uploads, metadata management, CDN URL resolution, and thumbnail generation. |
| {DOMAIN_TERM_1} | {DEFINITION_1} |
| {DOMAIN_TERM_2} | {DEFINITION_2} |

---

## Appendix — Change Log

| Version | Date | Author | Summary of Changes |
|---------|------|--------|--------------------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `file_id` field guidance, `eksad-core-storage` API endpoints (Section 9.3), BR-PLATFORM-006–009, and file storage glossary entries |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |
