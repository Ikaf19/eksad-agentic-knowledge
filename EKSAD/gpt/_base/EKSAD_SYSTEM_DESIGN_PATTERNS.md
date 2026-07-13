# EKSAD System Design Patterns
# Knowledge Reference for GPT & Development Teams

**Version:** 1.1
**Date:** 2026-05-23
**Owner:** EKSAD Platform Team
**Audience:** Developers, Architects, BA (via GPT Knowledge)

> This document is a **GPT knowledge file**. It teaches the GPT the architectural patterns
> used across all EKSAD services so it can give accurate, consistent answers.

---

## Table of Contents

1. [Overall Architecture](#1-overall-architecture)
2. [Auto Audit Trail Flow](#2-auto-audit-trail-flow)
3. [CrudFlows & BaseRepository Pattern](#3-crudflows--baserepository-pattern)
4. [Module Type Naming Convention](#4-module-type-naming-convention)
5. [Multi-Tenant Pattern](#5-multi-tenant-pattern)
6. [Approval Engine Pattern](#6-approval-engine-pattern)
7. [Event-Driven Design Rules](#7-event-driven-design-rules)
8. [Reactive Programming with Mutiny](#8-reactive-programming-with-mutiny)
9. [Authentication Flow](#9-authentication-flow)
10. [File Storage Pattern](#10-file-storage-pattern)
11. [Known Pitfalls & How to Avoid Them](#11-known-pitfalls--how-to-avoid-them)
12. [Master Data Service Pattern](#12-master-data-service-pattern)
13. [Denormalized Cache Sync Pattern](#13-denormalized-cache-sync-pattern)
14. [Database Deployment Strategy](#14-database-deployment-strategy)
15. [API Gateway — Optional Infrastructure](#15-api-gateway--optional-infrastructure)
16. [CQRS — Future Architecture (Reserved)](#16-cqrs--future-architecture-reserved)

---

## 1. Overall Architecture

EKSAD services follow an **event-driven microservices architecture** on Quarkus 3.x + Java 21.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Web / Mobile / API)                       │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │ HTTPS
┌────────────────────────────────▼─────────────────────────────────────────┐
│                eksad-gateway  :8080  (OPTIONAL — see §15)                 │
│       JWT RS256 validation  ·  routing  ·  rate limiting  ·  CORS         │
└───┬────────┬────────────┬────────────┬────────────┬────────────────────┘
    │        │            │            │            │
    ▼        ▼            ▼            ▼            ▼
┌────────┐┌──────────┐┌────────────┐┌────────────┐┌────────────────┐
│ eksad- ││ svc-user-││ svc-tenant-││ svc-master-││ svc-{domain}    │
│ core-  ││ mgmt     ││ mgmt       ││ data       ││ (svc-pipeline,  │
│ auth   ││ :8087    ││ :8091      ││ :8086      ││  svc-orders,    │
│ :8090  ││ MongoDB: ││ MongoDB:   ││ PostgreSQL:││  svc-attendance,│
│ PG:    ││ eksad_   ││ eksad_     ││ eksad_     ││  etc.) :8082+   │
│ eksad_ ││ users    ││ tenants    ││ master     ││ PostgreSQL:     │
│ core_  │└──────────┘└────────────┘└─────┬──────┘│ eksad_{function}│
│ auth   │                                │       └─────────┬──────┘
└────────┘                                │                 │
                                          │ events          │ events
                                          ▼                 ▼
                              ┌──────────────────────────────────────┐
                              │           RabbitMQ Cluster            │
                              │  Exchange: exc-log-activity           │
                              │  Exchange: exc-notification           │
                              │  Exchange: exc-file-processing        │
                              │  Exchange: exc-master-data (topic)    │ ◄── cache sync
                              │  Exchange: exc-{domain-events}        │
                              └──────┬───────────────────────┬───────┘
                                     │                       │
                ┌────────────────────┼─────┐                 │
                │                    │     │                 │
   ┌────────────▼──────────┐  ┌──────▼─────▼──────────┐  ┌──▼────────────────────┐
   │ eksad-core-audittrail │  │ Domain services       │  │ eksad-core-storage    │
   │ (consumer only)        │  │ (cache consumers)     │  │ :8090                 │
   │ MongoDB: eksad_audit   │  │ Each maintains local  │  │ PostgreSQL:           │
   │ Collection:            │  │ {entity}_cache table  │  │ eksad_storage         │
   │ log_activity           │  │ synced from           │  │ Table: file_metadata  │
   └───────────────────────┘  │ exc-master-data       │  │                       │
                              └───────────────────────┘  │ Provider (switchable):│
                                                          │ ┌──────────────────┐ │
                                                          │ │ AWS S3 + CF      │ │
                                                          │ │ ── OR ──         │ │
                                                          │ │ Cloudflare R2    │ │
                                                          │ └──────────────────┘ │
                                                          └──────────────────────┘

Database deployment (Phase 1): 1 PostgreSQL instance, separate database per service
(eksad_core_auth, eksad_master, eksad_{function}, ...). See §14.
```

**Key rules:**
- Gateway has ZERO business logic
- Services NEVER query each other's database
- Cross-service data: publish an event, the other service subscribes and maintains its own copy
- Every service is horizontally scalable and stateless
- Domain services store only `file_id` — never raw S3 keys or CDN URLs (Principle #9)

---

## 2. Auto Audit Trail Flow

This is the **most important pattern** to understand. Audit trail is ZERO developer effort.

### 2.1 Flow Diagram

```
Developer code in Service:
  service.create(dto)
        │
        ▼
  repository.createEntity(dto)          ← calls createFlow() inside
        │
        ▼
  CrudFlows.createFlow(dto, moduleType)
  ┌──────────────────────────────────────────────────┐
  │ 1. buildBaseLog(dto) → LogActivityDTO (status=FAIL by default)
  │ 2. toNewEntity(dto) → new Entity object
  │ 3. persist(entity)  → save to PostgreSQL
  │ 4. logSuccess(log, transactionId, savedEntity)
  │    → sets status=SUCCESS, dataAfter=JSON, responseTime
  │    → MutinyEmitter.sendAndForget(jsonb.toJson(log))
  └──────────────────────────────────────────────────┘
        │
        │ fire-and-forget (non-blocking)
        ▼
  RabbitMQ Exchange: exc-log-activity
  Routing Key: r.q-log-activity-eksad
  Queue: q-log-activity-eksad
        │
        ▼
  eksad-core-audittrail
  IncomingMessage @Incoming("in-log-activity")
        │
        ▼
  ILogActivityService.post(dto)
        │
        ▼
  MongoDB: eksad_audit.log_activity
  { document saved }
```

### 2.2 On Failure

```
If any step throws an exception:
  CrudFlows.updateFlow() → guard fails → logFailure(log, errorMessage)
    → MutinyEmitter sends log with status="FAIL", failReason=message
    → Returns Uni.failure(ValidationException)
    → HTTP 422 returned to client
    → Audit record saved in MongoDB with status=FAIL
```

### 2.3 What Developers Need to Do

| Step | Developer Action | Framework Does Automatically |
|------|-----------------|------------------------------|
| 1 | Extend `BaseRepository` | Injects `LogHandler`, `UserContext`, `UriResolver` |
| 2 | Implement 5 abstract methods | — |
| 3 | Call `createFlow` / `updateFlow` / `deleteFlow` | Builds log, persists, fires audit event |
| 4 | Add 4 env vars (RabbitMQ connection) | Channel binding, exchange declaration, serialization |

**Developer does NOT need to:**
- Write any RabbitMQ producer code
- Configure `mp.messaging.outgoing.*` properties (defaults in library)
- Build `LogActivityDTO` manually
- Handle audit failures (fire-and-forget — main operation succeeds regardless)

---

## 3. CrudFlows & BaseRepository Pattern

### 3.1 Interface Hierarchy

```
PanacheRepositoryBase<E, I>        ← Quarkus Hibernate Reactive
        │
        ▼
CrudFlows<E, D, I>                 ← EKSAD interface (eksad-core-common)
  Default methods:
  - createFlow(dto, action, extras)
  - updateFlow(dto, action, guard, errorFn, mutator)
  - deleteFlow(dto, action, deleter)
  - commandFlow(dto, idFn, dtoIdFn, action, handler)
  - commandFlow(..., guard, onGuardFailure, handler)
        │
        ▼
BaseRepository<E, D, I>            ← EKSAD abstract class (eksad-core-common)
  Injects: LogHandler, UserContext, UriResolver
  Provides: auditMutator(), softDeleteMutator(), now(), currentUser()
        │
        ▼
{Entity}Repository                 ← YOUR SERVICE (extend this)
  Implements: toId, extractDtoId, extractTransactionId, toNewEntity, moduleType
  Implements: createEntity, updateEntity, deleteEntity
```

### 3.2 The 5 Abstract Methods Explained

| Method | Signature | Purpose | Example |
|--------|-----------|---------|---------|
| `moduleType()` | `() → String` | Returns default module type string | `return TransactionModuleType.TRANSACTION.CREATE` |
| `toId(dto)` | `D → I` | Extract entity ID from DTO | `return dto.getId()` |
| `extractDtoId(dto)` | `D → String` | Extract ID as String for log | `return String.valueOf(dto.getId())` |
| `extractTransactionId(entity)` | `E → String` | Extract entity ID after save | `return String.valueOf(entity.getId())` |
| `toNewEntity(dto, extras)` | `(D, Object...) → E` | Map DTO to new entity | Builder pattern with `createdAt`, `tenantId` set |

### 3.3 The 3 Flow Methods Explained

**`createFlow`** — for INSERT operations:
```
1. Build log
2. Call toNewEntity(dto) 
3. persist(entity)         ← @ReactiveTransactional wraps this
4. logSuccess → fire audit
5. return saved entity
```

**`updateFlow`** — for UPDATE operations with guard:
```
1. Build log
2. findById(toId(dto))
3. If null → logFailure("Data not found") → throw ValidationException
4. Check guard.test(entity)
5. If guard fails → logFailure(errorFn.apply(entity))
6. Capture dataBefore = JSON(entity)
7. Apply mutator(entity)
8. persist(entity)
9. logSuccess → fire audit
10. return updated entity
```

**`deleteFlow`** — soft delete (uses updateFlow internally):
```
Same as updateFlow with:
- guard = always true (v -> true)
- mutator = softDeleteMutator() which sets deletedAt + deletedBy
```

### 3.4 `commandFlow` — for Custom State Changes

Use when the DTO type differs from the main CRUD DTO (e.g., approval, rejection):

```java
// In repository:
public Uni<OrderEntity> approve(ApprovalDTO dto) {
    return commandFlow(
        dto,
        d -> d.getOrderId(),               // idFn: how to get entity ID
        d -> d.getOrderId().toString(),     // dtoIdFn: ID as string for log
        OrderModuleType.ORDER.APPROVE,
        entity -> entity.getStatus().equals("SUBMITTED"),   // guard
        entity -> "Order must be SUBMITTED to approve",     // guard failure msg
        entity -> {
            entity.setStatus("APPROVED");
            entity.setApprovedAt(Instant.now().toEpochMilli());
            entity.setApprovedBy(currentUser());
            return persist(entity);
        }
    );
}
```

---

## 4. Module Type Naming Convention

### 4.1 Format

```
<PROJECT>.<MODULE>.<ACTION>

PROJECT  = EKSAD_SVC_{SERVICE_DOMAIN}    (e.g., EKSAD_SVC_LEADS, EKSAD_TIA, EKSAD_HR)
MODULE   = Bounded context or entity     (e.g., TRANSACTION, SUBMISSION, APPROVAL, USER)
ACTION   = Verb in UPPER_SNAKE_CASE      (e.g., CREATE, UPDATE, DELETE, SUBMIT, APPROVE, REJECT)
```

### 4.2 Examples by Service

| Service | Module | Action | Full String |
|---------|--------|--------|-------------|
| eksad-svc-leads | TRANSACTION | CREATE | `EKSAD_SVC_LEADS.TRANSACTION.CREATE` |
| eksad-svc-leads | TRANSACTION | UPDATE | `EKSAD_SVC_LEADS.TRANSACTION.UPDATE` |
| eksad-tia | SUBMISSION | SUBMIT | `EKSAD_TIA.SUBMISSION.SUBMIT` |
| eksad-tia | APPROVAL | APPROVE | `EKSAD_TIA.APPROVAL.APPROVE` |
| eksad-tia | APPROVAL | REJECT | `EKSAD_TIA.APPROVAL.REJECT` |
| eksad-hr | EMPLOYEE | CREATE | `EKSAD_HR.EMPLOYEE.CREATE` |
| eksad-hr | LEAVE | SUBMIT | `EKSAD_HR.LEAVE.SUBMIT` |

### 4.3 Implementation Pattern

```java
// Use a Java interface with String constants — NOT an enum
// Reason: enums cannot be extended across services; interfaces can
public interface TransactionModuleType {
    String PREFIX = "EKSAD_SVC_LEADS";

    interface TRANSACTION {
        String CREATE = PREFIX + ".TRANSACTION.CREATE";
        String UPDATE = PREFIX + ".TRANSACTION.UPDATE";
        String DELETE = PREFIX + ".TRANSACTION.DELETE";
    }

    interface ORDER {
        String CREATE  = PREFIX + ".ORDER.CREATE";
        String APPROVE = PREFIX + ".ORDER.APPROVE";
        String REJECT  = PREFIX + ".ORDER.REJECT";
    }
}
```

---

## 5. Multi-Tenant Pattern

### 5.1 Tenant Identity Source

The `tenant_id` comes exclusively from the **JWT token**:
```json
{
  "eksad_tenant_id": "triputra-group"
}
```

### 5.2 Where `tenant_id` Must Appear

| Location | How |
|----------|-----|
| Every PostgreSQL entity | `@Column(name = "tenant_id", nullable = false)` |
| Every MongoDB document | `"tenant_id": "{value}"` field in every document |
| Every RabbitMQ event | `"tenantId": "{value}"` in event envelope |
| JWT claims | `eksad_tenant_id` claim |
| `toNewEntity()` | `entity.setTenantId(getUserContext().getTenantId())` |

### 5.3 Query Isolation

Using Hibernate `@Filter`:
```java
// On entity class
@FilterDef(name = "tenantFilter",
    parameters = @ParamDef(name = "tenantId", type = String.class))
@Filter(name = "tenantFilter", condition = "tenant_id = :tenantId")
public class {Entity}Entity extends BaseEntity { ... }

// Activated in BaseRepository or a RequestFilter CDI interceptor
session.enableFilter("tenantFilter")
       .setParameter("tenantId", userContext.getTenantId());
```

### 5.4 Cross-Tenant Access

- Only `ROLE_SUPER_ADMIN` may bypass `tenant_id` filter
- All other roles: `tenant_id` filter is always applied automatically
- Any endpoint returning cross-tenant data must be explicitly documented in FSD with `[SUPER_ADMIN ONLY]` label

---

## 6. Approval Engine Pattern

### 6.1 Generic State Machine

```
                 ┌─────────────────────────────────────────────┐
                 │                                             │
DRAFT ──submit──► SUBMITTED ──review──► IN_REVIEW ──approve──► APPROVED
                      │                     │
                      │                     └──reject──► REJECTED
                      │                                      │
                      └──reject────────────────────────────► │
                                                              │
                                                         revise/reopen
                                                              │
                                                              ▼
                                                           DRAFT
```

### 6.2 Approval Level Configuration

Stored in `approval_config` table per module per tenant:

| Column | Type | Example |
|--------|------|---------|
| `tenant_id` | VARCHAR | `"triputra-group"` |
| `module_type` | VARCHAR | `"EKSAD_TIA.SUBMISSION"` |
| `levels` | INT | `2` |
| `level_1_role` | VARCHAR | `"ROLE_REVIEWER"` |
| `level_2_role` | VARCHAR | `"ROLE_DIRECTOR"` |
| `auto_approve_condition` | VARCHAR | `null` or `"amount < 1000000"` |

### 6.3 Implementing an Approval Action in Repository

```java
public Uni<SubmissionEntity> approve(ApproveDTO dto) {
    return commandFlow(
        dto,
        ApproveDTO::getSubmissionId,
        d -> d.getSubmissionId().toString(),
        SubmissionModuleType.SUBMISSION.APPROVE,
        entity -> "SUBMITTED".equals(entity.getStatus())
               || "IN_REVIEW".equals(entity.getStatus()),
        entity -> "Cannot approve from state: " + entity.getStatus(),
        entity -> {
            entity.setStatus("APPROVED");
            entity.setApprovedAt(Instant.now().toEpochMilli());
            entity.setApprovedBy(currentUser());
            entity.setApprovalComment(dto.getComment());
            return persist(entity);
        }
    );
}
```

---

## 7. Event-Driven Design Rules

### 7.1 When to Use Async (RabbitMQ)

| Use Case | Reason |
|----------|--------|
| Audit trail | Fire-and-forget; must not block main flow |
| Email / push notifications | Slow; user doesn't wait for email to send |
| Cross-service data sync | Each service maintains its own read model |
| Scheduled batch jobs | Trigger via message |
| Events with no immediate user response | Status changes, background processing |

### 7.2 When to Use Sync (HTTP)

| Use Case | Reason |
|----------|--------|
| User login / JWT validation | Immediate response required |
| Direct user queries (GET) | User is waiting for data |
| Gateway → Service calls | User-initiated request-response cycle |

### 7.3 Event Naming Convention

```
Exchange naming:  exc-{domain}           (e.g., exc-log-activity, exc-notification)
Queue naming:     q-{action}-{service}   (e.g., q-log-activity-eksad)
Routing key:      r.q-{action}-{service} (e.g., r.q-log-activity-eksad)
```

### 7.4 Guaranteed Delivery

- All exchanges declared as `durable=true`
- All queues declared as `durable=true`
- Publisher confirm enabled: `publisher-confirm=true`
- Dead-letter queue: `q-dlq-{queue-name}` for failed processing
- Audit events: fire-and-forget is acceptable (audit should never block business flow)

---

## 8. Reactive Programming with Mutiny

### 8.1 `Uni<T>` vs `Multi<T>`

| Type | Use When | Example |
|------|----------|---------|
| `Uni<T>` | Single item or nothing (most CRUD ops) | `findById()`, `persist()`, `delete()` |
| `Multi<T>` | Stream of items | Real-time updates, SSE, list with streaming |

### 8.2 Common Patterns

**Chain operations:**
```java
return repository.findById(id)
    .onItem().ifNull().failWith(() -> new ValidationException("Not found"))
    .flatMap(entity -> {
        entity.setStatus("UPDATED");
        return repository.persist(entity);
    });
```

**Fire-and-forget (audit trail pattern):**
```java
emitter.sendAndForget(jsonPayload);
// Does not block. Does not wait for RabbitMQ ACK.
// Failures are logged but don't affect the main Uni chain.
```

**Recover from failure:**
```java
return service.doSomething()
    .onFailure(ValidationException.class)
    .recoverWithItem(fallbackValue);
```

### 8.3 Transactional Boundary

```java
// Service method must be annotated — NOT the repository
@ApplicationScoped
@WithSession
public class MyService {

    @ReactiveTransactional
    public Uni<MyEntity> create(MyDTO dto) {
        return repository.createEntity(dto);
    }
}
```

---

## 9. Authentication Flow

### 9.1 Login → JWT → Service

```
1. Client: POST /api/v1/auth/login { username, password }
2. eksad-auth: validates credentials → issues JWT (RS256, signed with private key)
3. Client: stores access_token, refresh_token
4. Client: GET /api/v1/transactions (Authorization: Bearer {access_token})
5. eksad-gateway: validates JWT signature using public key → routes to service
6. Service: SmallRye JWT automatically validates token locally (no round-trip to auth)
7. Service: injects @Context SecurityContext or @Inject JsonWebToken
8. UserContext: reads eksad_tenant_id, eksad_user_id, eksad_role from claims
```

### 9.2 How Services Read JWT Claims

`UserContext` (from `eksad-core-common`) wraps this automatically:

```java
@Inject
UserContext userContext;

String user     = userContext.getUser();          // from JWT "sub"
String role     = userContext.getRole();          // from JWT "eksad_role"
String tenantId = userContext.getTenantId();      // from JWT "eksad_tenant_id"
String actor    = userContext.getAuditActor();    // "user (impersonating original)"
```

---

## 10. File Storage Pattern

---

### 10.1 Overview

`eksad-core-storage` is a dedicated core Quarkus microservice (`:8090`) responsible for all file operations across the EKSAD platform. No domain service may interact with S3/R2 directly.

```
Client
  │  POST /api/v1/storage/upload (multipart + visibility + refEntityType + refEntityId)
  ▼
eksad-core-storage (:8090)
  │  1. Validate JWT + tenant_id
  │  2. Enforce MIME allowlist + file size cap
  │  3. Stream file to StorageProvider
  │  4. Persist file_metadata → PostgreSQL
  │  5. Publish thumbnail event to exc-file-processing (fire-and-forget)
  │  6. Return { fileId, cdnUrl (PUBLIC only) }
  ▼
StorageProvider (pluggable)
  ├── AwsS3StorageProvider     → AWS S3 bucket + CloudFront CDN
  └── CloudflareR2StorageProvider → Cloudflare R2 bucket + Cloudflare CDN

RabbitMQ: exc-file-processing → q-generate-thumbnail-core-storage
  ▼
Thumbnail Consumer (inside eksad-core-storage)
  ├── Image (PNG/JPG/GIF/WEBP) → Thumbnailator
  └── PDF                      → Apache PDFBox (page 1 → JPEG)
  ▼
Upload thumbnail → StorageProvider (same visibility as parent)
Update file_metadata: thumbnail_s3_key, thumbnail_cdn_url (PUBLIC), thumbnail_status=READY
```

---

### 10.2 File Visibility Rules

| Visibility | Storage Bucket Policy | `cdn_url` in DB | URL Resolution |
|------------|----------------------|-----------------|----------------|
| `PUBLIC`   | Public-read bucket policy | Stored permanently | Returned directly from DB |
| `PRIVATE`  | Private bucket, no public access | `NULL` | Signed CDN URL generated at request-time (TTL = `STORAGE_SIGNED_URL_TTL_SECONDS`, default `300`s) |

> **Rule:** Thumbnail inherits the `visibility` of its parent file — always.

---

### 10.3 Pluggable `StorageProvider` Interface

```java
public interface StorageProvider {
    Uni<String> upload(String s3Key, InputStream content, String mimeType, long size);
    Uni<Void>   delete(String s3Key);
    String      buildCdnUrl(String s3Key);          // PUBLIC only
    Uni<String> generateSignedUrl(String s3Key);    // PRIVATE only — TTL from env
}
```

Active provider selected via `STORAGE_PROVIDER=aws|cloudflare` env var. Cloudflare R2 is S3-compatible — same AWS SDK, different endpoint injected via `STORAGE_S3_ENDPOINT` env var.

---

### 10.4 S3 Key Naming Convention

```
{tenant_id}/{visibility_lower}/{ref_entity_type}/{uuid}.{ext}
{tenant_id}/{visibility_lower}/thumbnails/{uuid}_thumb.jpg

Examples:
  triputra-group/private/contract/a1b2c3d4.pdf
  triputra-group/private/thumbnails/a1b2c3d4_thumb.jpg
  triputra-group/public/logo/e5f6g7h8.png
  triputra-group/public/thumbnails/e5f6g7h8_thumb.jpg
```

---

### 10.5 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STORAGE_PROVIDER` | Active provider: `aws` or `cloudflare` | `aws` |
| `STORAGE_S3_BUCKET_PUBLIC` | Bucket name for PUBLIC files | — |
| `STORAGE_S3_BUCKET_PRIVATE` | Bucket name for PRIVATE files | — |
| `STORAGE_S3_REGION` | AWS region (AWS only) | `ap-southeast-1` |
| `STORAGE_S3_ENDPOINT` | Custom endpoint URL (Cloudflare R2: `https://{account}.r2.cloudflarestorage.com`) | — |
| `STORAGE_S3_ACCESS_KEY` | S3 / R2 access key | — |
| `STORAGE_S3_SECRET_KEY` | S3 / R2 secret key | — |
| `STORAGE_CDN_BASE_URL_PUBLIC` | CDN base URL for PUBLIC files (e.g. `https://cdn.eksad.com`) | — |
| `STORAGE_CDN_PRIVATE_KEY_ID` | CloudFront key pair ID for signed URLs (AWS only) | — |
| `STORAGE_CDN_PRIVATE_KEY_PATH` | Path to CloudFront private key PEM (AWS only) | — |
| `STORAGE_SIGNED_URL_TTL_SECONDS` | Signed URL lifetime for PRIVATE files | `300` |
| `STORAGE_MAX_FILE_SIZE_MB` | Max upload size in MB | `20` |
| `STORAGE_ALLOWED_MIME_TYPES` | Comma-separated MIME allowlist | `image/png,image/jpeg,image/gif,image/webp,application/pdf` |

---

### 10.6 `file_metadata` Table (PostgreSQL)

```sql
CREATE TABLE file_metadata (
    id                  BIGSERIAL PRIMARY KEY,
    tenant_id           VARCHAR(100)  NOT NULL,
    s3_key              VARCHAR(500)  NOT NULL,
    original_filename   VARCHAR(255)  NOT NULL,
    mime_type           VARCHAR(100)  NOT NULL,
    file_size_bytes     BIGINT        NOT NULL,
    visibility          VARCHAR(10)   NOT NULL CHECK (visibility IN ('PUBLIC','PRIVATE')),
    cdn_url             VARCHAR(1000) NULL,           -- populated for PUBLIC only
    thumbnail_s3_key    VARCHAR(500)  NULL,
    thumbnail_cdn_url   VARCHAR(1000) NULL,           -- populated for PUBLIC thumbnail only
    thumbnail_status    VARCHAR(10)   NOT NULL DEFAULT 'PENDING'
                            CHECK (thumbnail_status IN ('PENDING','READY','FAILED','SKIPPED')),
    ref_entity_type     VARCHAR(100)  NULL,           -- e.g. 'contract', 'lead'
    ref_entity_id       VARCHAR(100)  NULL,           -- ID of the owning entity in caller service
    provider            VARCHAR(20)   NOT NULL,       -- 'aws' or 'cloudflare'
    confidential        BOOLEAN       NOT NULL DEFAULT FALSE, -- reserved for future access audit
    deleted_at          BIGINT        NULL,
    deleted_by          VARCHAR(100)  NULL,
    created_at          BIGINT        NOT NULL,
    created_by          VARCHAR(100)  NOT NULL,
    updated_at          BIGINT        NULL,
    updated_by          VARCHAR(100)  NULL
);

CREATE INDEX idx_file_metadata_tenant       ON file_metadata (tenant_id);
CREATE INDEX idx_file_metadata_ref          ON file_metadata (tenant_id, ref_entity_type, ref_entity_id);
CREATE INDEX idx_file_metadata_deleted      ON file_metadata (deleted_at);
CREATE INDEX idx_file_metadata_thumb_status ON file_metadata (thumbnail_status) WHERE thumbnail_status = 'PENDING';
```

---

### 10.7 Module Types for `eksad-core-storage`

```java
public interface StorageModuleType {
    String PREFIX = "EKSAD_CORE_STORAGE";

    interface FILE {
        String UPLOAD = PREFIX + ".FILE.UPLOAD";
        String DELETE = PREFIX + ".FILE.DELETE";
        // Reserved for future confidential file access audit:
        String ACCESS = PREFIX + ".FILE.ACCESS";
    }
}
```

---

### 10.8 How Domain Services Reference Files

```java
// In domain service entity (e.g., ContractEntity):
@Column(name = "attachment_file_id")
private Long attachmentFileId;   // FK by convention — not a DB foreign key constraint

// In domain service REST layer — resolve URL at render-time:
// GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/url
// GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/thumbnail-url

// NEVER store in domain service:
// ❌ private String s3Key;
// ❌ private String cdnUrl;
```

---

### 10.9 Thumbnail Fallback Behaviour

If `thumbnail_status = 'FAILED'`, the `/thumbnail-url` endpoint falls back gracefully to returning the **original file's URL** (signed or permanent, per visibility) — the frontend always receives a usable URL and never an error from a missing thumbnail.

---

## 11. Known Pitfalls & How to Avoid Them

### 10.1 ⚠️ ThreadLocal in Reactive Context

**Problem:** `AuthContextStore` uses `ThreadLocal<JsonWebToken>`. In Quarkus reactive (Vert.x event loop), a single request can switch threads mid-execution, causing `ThreadLocal` to return null or stale data.

**Current mitigation:** `UserContext` gracefully falls back to CDI-injected `JsonWebToken` if `ThreadLocal` returns null.

**Best practice:**
- Do NOT store request state in `ThreadLocal` in new code
- Prefer `@RequestScoped` CDI beans or pass context explicitly through method parameters
- For long reactive chains, use Vert.x `context.putLocal()` / `context.getLocal()`

### 10.2 ⚠️ `ddl-auto=update` in Production

**Problem:** Using `quarkus.hibernate-orm.database.generation=update` in production silently alters schema without version tracking — data loss risk.

**Rule:** Always `none` in production. Always `Flyway` for migrations. Use `update` only in local dev if needed, and never commit it.

### 10.3 ⚠️ Missing `tenant_id` on New Entities

**Problem:** Developer forgets to set `tenant_id` in `toNewEntity()` — data becomes inaccessible or visible to wrong tenant.

**Prevention:**
- Code review checklist: `tenant_id` must be set in every `toNewEntity()`
- Add NOT NULL constraint on `tenant_id` column in Flyway DDL
- `BaseRepository.toNewEntity()` docstring reminds about this

### 10.4 ⚠️ Storing Financial Values as `String` or `Double`

**Problem:** `String` → runtime cast failures; `Double` → floating-point precision errors on financial sums.

**Rule:** Always `NUMERIC(20,4)` in PostgreSQL, always `BigDecimal` in Java. Never `Double`, never `Float`, never `String`.

### 10.5 ⚠️ Hard-coding `company_id` or Tenant Params in Queries

**Problem:** Hardcoded parameters in queries (as seen in legacy systems like `getytdoutlookpa` bug in TIA v1) mean all tenants or companies get wrong data.

**Prevention:**
- Always source `tenant_id` from `UserContext` (JWT)
- Never pass company/tenant IDs as literal values in query methods
- Code review must verify all query parameters come from JWT or validated input

### 10.6 ⚠️ `@Singleton` vs `@ApplicationScoped` for Stateful Beans

**Problem:** Using `@Singleton` for beans that maintain mutable state (like `AuthContextStore`) in a concurrent environment can lead to race conditions.

**Rule:** `@ApplicationScoped` is the standard scope. Use `@Singleton` only for truly stateless utility beans. Never store mutable request state in `@ApplicationScoped` or `@Singleton` beans without `ThreadLocal` or request-scoped guards.

---

## 12. Master Data Service Pattern

### 12.1 What Qualifies as Master Data

| Decision Criteria | Classification |
|-------------------|----------------|
| Catalog/reference data referenced by 2+ services within a domain? | ✅ **Master data** (`svc-master-data`) |
| Countable stock with quantity/availability? | ❌ Inventory data (separate `svc-inventory`, future) |
| Domain-specific transactional data? | ❌ Domain service |

**Examples by domain** (see `EKSAD_DOMAIN_REGISTRY.md` for the full list):
- **[Example: Automotive]** brands, models, types/variants, colors, branches
- **[Example: HRIS]** departments, positions, grades, leave_types, shift_types

### 12.2 `svc-master-data` Responsibility

- CRUD catalog/reference entities + validation
- Publish events to `exc-{domain}-master-data` (topic exchange)
- Per business domain: separate instance/namespace + database
- Module type convention: `EKSAD_{DOMAIN}_MASTER.{ENTITY}.{ACTION}` (e.g., `EKSAD_MASTER.BRAND.CREATE`)

### 12.3 Write-Path Architecture

```
Admin UI → svc-master-data REST API
            │
            ├─→ PostgreSQL (eksad_{domain}_master)
            │
            └─→ exc-{domain}-master-data (topic)
                    │
                    ├─→ q-{domain}-master-sync-{service-A} → svc-A.{entity}_cache
                    ├─→ q-{domain}-master-sync-{service-B} → svc-B.{entity}_cache
                    └─→ q-{domain}-master-sync-{service-N} → svc-N.{entity}_cache
```

### 12.4 REST API Catalog (Template)

Per entity:
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/v1/{entity}` | `@RolesAllowed("MASTER_VIEWER")` | List (paginated) |
| `GET` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_VIEWER")` | Detail |
| `POST` | `/api/v1/{entity}` | `@RolesAllowed("MASTER_ADMIN")` | Create |
| `PUT` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_ADMIN")` | Update |
| `DELETE` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_ADMIN")` | Soft delete |
| `POST` | `/api/v1/{entity}/batch` | `@RolesAllowed("MASTER_VIEWER")` | Batch fetch by IDs (for cache sync) |

**Hierarchical endpoints (where applicable):**
- `GET /api/v1/brands/{id}/models` — children
- `GET /api/v1/models/{id}/types` — grandchildren

### 12.5 Domain Service Consumption

- Store **reference IDs only** (`brand_id`, `model_id`, `department_id`).
- Maintain `{entity}_cache` table (see Section 13).
- Frontend dropdowns: call `svc-master-data` REST directly.
- Backend list/detail views: **local JOIN** with cache table.

> Full guide: `EKSAD_MASTER_DATA_PATTERNS.md`.

---

## 13. Denormalized Cache Sync Pattern

### 13.1 Why Denormalized Cache?

**Problem:** cross-service data needed for display (e.g., model name in leads list, dept name in attendance).

**3 patterns compared:**
| Pattern | Approach | Verdict |
|---------|----------|---------|
| 1. FE merge | Frontend fetches each piece separately | ❌ Many round-trips, complex FE |
| 2. Backend enrichment | Service calls master-data on every request | ❌ Tight runtime coupling |
| 3. **Denormalized cache** | Local `_cache` table synced via events | ✅ **Chosen for EKSAD** |

**Benefits:** independent services, zero runtime coupling, fast local JOINs.

### 13.2 Cache Table Design Standards

- Naming: `{entity}_cache` (e.g., `brand_cache`, `model_cache`).
- Schema: mirror master data + `last_synced_at BIGINT NOT NULL` + `tenant_id`.
- Primary key: same ID as master data entity.
- Hierarchical caches denormalize parent name for display (e.g., `model_cache.brand_name`).
- ❌ DO NOT extend `BaseEntity` — cache tables have no audit columns.
- ❌ DO NOT use `BaseRepository` — use simple `PanacheRepositoryBase`.
- ❌ NO soft-delete columns — cache rows are upserted or hard-deleted.

### 13.3 Event Consumer Implementation

```java
@ApplicationScoped
public class MasterDataEventConsumer {

    @Inject BrandCacheRepository brandCache;
    @Inject ModelCacheRepository modelCache;

    @Incoming("master-data-events")
    public Uni<Void> consume(JsonObject envelope) {
        String eventType = envelope.getString("eventType");
        long   occurredAt = envelope.getLong("occurredAt");
        JsonObject payload = envelope.getJsonObject("payload");

        return switch (eventType) {
            case "BRAND.CREATED", "BRAND.UPDATED" -> brandCache.upsert(payload, occurredAt);
            case "BRAND.DELETED"                  -> brandCache.deleteById(payload.getLong("id"));
            case "MODEL.CREATED", "MODEL.UPDATED" -> modelCache.upsert(payload, occurredAt);
            case "MODEL.DELETED"                  -> modelCache.deleteById(payload.getLong("id"));
            default -> {
                Log.warnf("Unknown event type: %s — skipping", eventType);
                yield Uni.createFrom().voidItem();
            }
        };
    }
}
```

### 13.4 Cache Repository (simple Panache, NOT BaseRepository)

```java
@ApplicationScoped
public class BrandCacheRepository implements PanacheRepositoryBase<BrandCache, Long> {

    public Uni<Void> upsert(JsonObject payload, long occurredAt) {
        Long id = payload.getLong("id");
        return findById(id).onItem().transformToUni(existing -> {
            if (existing != null && existing.getLastSyncedAt() >= occurredAt) {
                return Uni.createFrom().voidItem();  // stale event, skip
            }
            BrandCache b = existing != null ? existing : new BrandCache();
            b.setId(id);
            b.setTenantId(payload.getString("tenantId"));
            b.setName(payload.getString("name"));
            b.setLastSyncedAt(occurredAt);
            return persist(b).replaceWithVoid();
        });
    }
}
```

### 13.5 Startup Sync

```java
@ApplicationScoped
public class CacheSyncJob {

    @Inject BrandCacheRepository repo;
    @Inject @RestClient MasterDataClient client;

    void onStart(@Observes StartupEvent ev) {
        repo.count().subscribe().with(count -> {
            if (count == 0) {
                client.listAllBrands().subscribe().with(repo::bulkInsert);
            }
        });
    }
}
```

### 13.6 RabbitMQ Config

```properties
mp.messaging.incoming.master-data-events.connector=smallrye-rabbitmq
mp.messaging.incoming.master-data-events.exchange.name=exc-master-data
mp.messaging.incoming.master-data-events.exchange.type=topic
mp.messaging.incoming.master-data-events.queue.name=q-master-sync-pipeline
mp.messaging.incoming.master-data-events.routing-keys=r.brand.*,r.model.*,r.type.*
```

> Full guide: `EKSAD_CACHE_SYNC_PATTERNS.md`.

---

## 14. Database Deployment Strategy

### 14.1 Phased Approach

| Phase | Strategy | When |
|-------|----------|------|
| **Phase 1** | 1 PostgreSQL instance, **separate databases per service** | Sprint 1–4 |
| **Phase 2** | Split hot services to **dedicated instances** | Sprint 5+ |
| **Phase 3** | Full dedicated per service, read replicas | Large scale (multi-region, compliance) |

### 14.2 Phase 1 — Shared Instance

- 1 PostgreSQL instance (`postgres:16-alpine`).
- Separate database per service (`eksad_core_auth`, `eksad_master`, `eksad_pipeline`, …).
- Per-service DB credentials (least privilege).
- Cross-DB joins **impossible by design** — isolation enforced at DB level.

```sql
-- init-databases.sql
CREATE DATABASE eksad_core_auth;
CREATE USER eksad_core_auth WITH PASSWORD '<from env>';
GRANT ALL PRIVILEGES ON DATABASE eksad_core_auth TO eksad_core_auth;

CREATE DATABASE eksad_master;
CREATE USER eksad_master WITH PASSWORD '<from env>';
GRANT ALL PRIVILEGES ON DATABASE eksad_master TO eksad_master;
-- ... per service
```

### 14.3 Zero Code Change on Migration

Services reference DB only via env vars:
```properties
quarkus.datasource.reactive.url=postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}
quarkus.datasource.username=${DB_USER}
quarkus.datasource.password=${DB_PASSWORD}
```

Migrating to dedicated instance = update env vars in K8s manifest. No code change.

> Full guide: `EKSAD_DB_DEPLOYMENT_STRATEGY.md`.

---

## 15. API Gateway — Optional Infrastructure

### 15.1 Gateway is Optional

Per **Decision 13**, `eksad-gateway` is **optional**. Every domain service MUST validate JWT independently via JWKS from `eksad-core-auth` — gateway is an add-on, not a dependency.

### 15.2 Phased Approach

| Phase | Gateway? | Access Pattern | JWT Validation |
|-------|----------|----------------|----------------|
| **Dev / Sprint 1** | ❌ No | Direct service access (multiple ports) | Per-service via JWKS |
| **Staging / Sprint 3+** | ✅ Yes | Single entry point (:8080) | Gateway + per-service (defense in depth) |
| **Production** | ✅ Yes + LB | Gateway + load balancer | Gateway primary, per-service fallback |

### 15.3 Per-Service JWT Config (Mandatory)

```properties
# Quarkus — every service
mp.jwt.verify.publickey.location=http://eksad-core-auth:8090/.well-known/jwks.json
mp.jwt.verify.issuer=eksad-core-auth
quarkus.smallrye-jwt.enabled=true
```

### 15.4 Architecture — Both Modes

**Without gateway (dev):**
```
Client → svc-pipeline :8082 (validates JWT via JWKS)
       → svc-orders   :8083 (validates JWT via JWKS)
       → svc-master   :8086 (validates JWT via JWKS)
```

**With gateway (staging+):**
```
Client → eksad-gateway :8080 (validates JWT) → svc-pipeline :8082 (re-validates or trusts)
                                              → svc-orders   :8083
```

When gateway is present, services can optionally trust the internal network (configurable, less safe).

### 15.5 When to Add Gateway?

| Trigger | Add Gateway? |
|---------|--------------|
| Frontend complexity (many service URLs) | ✅ |
| Centralized rate limiting needed | ✅ |
| External clients / partners | ✅ |
| TLS termination point needed | ✅ |
| Sprint 1 dev iteration | ❌ Skip |

---

## 16. CQRS — Future Architecture (Reserved)

> 🟡 **Status:** NOT implemented in Sprint 1. Reserved for Sprint 4+ when cross-service reporting is needed.

### 16.1 When Does EKSAD Need CQRS?

**Trigger:** cross-service dashboard / reporting needs.
**Examples:**
- Customer journey: lead → order → payment → delivery
- Conversion funnels
- Cross-service analytics dashboards

**NOT needed when:** each service queries its own data only (Sprint 1 default).

### 16.2 EKSAD CQRS Approach: CQRS + Domain Events (NOT Event Sourcing)

**Why not full Event Sourcing?**
- `CrudFlows` is state-based and works well.
- Team complexity (event replay, snapshots).
- Audit trail already exists for compliance.

**EKSAD architecture (future):**
```
Domain services publish events → exc-domain-events (topic)
                                       │
                                       ▼
                              svc-query consumes
                                       │
                                       ▼
                       Read model tables in eksad_query DB
                                       │
                                       ▼
                          Dashboard / reporting APIs
```

### 16.3 Domain Events vs Audit Events

| Aspect | Audit Events (existing) | Domain Events (future) |
|--------|-------------------------|------------------------|
| Purpose | Compliance logging | Business state propagation |
| Payload | Generic `dataBefore` / `dataAfter` JSON | Typed semantic business payload |
| Exchange | `exc-log-activity` | `exc-domain-events` |
| Consumer | `eksad-core-audittrail` | `svc-query` (+ future consumers) |
| Retention | Forever | Configurable per event |

### 16.4 Migration Path

Extend `CrudFlows` to publish domain events **alongside** audit events:
```java
createFlow(dto, moduleType)
    .invoke(saved -> domainEventEmitter.sendAndForget(toDomainEvent(saved)))
```

### 16.5 Trigger Conditions

When the team should plan CQRS:
- Dashboard requirement that joins data from 3+ services
- Aggregated reporting with sub-second response targets
- Read load >> write load (read-heavy with caching insufficient)

> Full guide: `EKSAD_CQRS_PATTERNS.md`.
