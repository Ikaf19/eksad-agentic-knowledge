# EKSAD Event Catalog

| Meta | Value |
|------|-------|
| **Version** | 1.1 |
| **Date** | 2026-05-31 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Developers, Architects, SA |
| **Priority** | 🟡 P1 |
| **Related** | `EKSAD_MASTER_DATA_PATTERNS.md`, `EKSAD_CACHE_SYNC_PATTERNS.md`, `EKSAD_BASE_PRINCIPLES.md` |

---

## Table of Contents

1. [Exchange Registry](#1-exchange-registry)
2. [Queue Registry](#2-queue-registry)
3. [Event Envelope (Universal)](#3-event-envelope-universal)
4. [Master Data Events — Automotive](#4-master-data-events--automotive)
5. [Master Data Events — HRIS](#5-master-data-events--hris)
6. [Audit Trail Events](#6-audit-trail-events)
7. [File Processing Events](#7-file-processing-events)
8. [Notification Events](#8-notification-events)
9. [Auth Events](#9-auth-events)
10. [Domain Events (per Project — Examples)](#10-domain-events-per-project--examples)
11. [Naming Conventions](#11-naming-conventions)
12. [Adding a New Event](#12-adding-a-new-event)
13. [Registering Events for a New Domain](#13-registering-events-for-a-new-domain)
14. [Event Versioning Strategy](#14-event-versioning-strategy)

---

## 1. Exchange Registry

> **Transport note:** EKSAD services run a per-service **Stack Profile** broker — RabbitMQ (default) or Kafka
> (opt-in). See `EKSAD_BASE_PRINCIPLES.md → Stack Profiles`. The event **envelope (§3) is identical across brokers**;
> only the transport differs. The `Transport` column below states which transport(s) carry each stream today.
> RabbitMQ exchanges and their Kafka topic equivalents are listed in §1.1.

| Exchange | Type | Transport | Purpose | Publisher Service(s) | Domain | Status |
|----------|------|-----------|---------|----------------------|--------|--------|
| `exc-log-activity` | direct | AMQP (+ Kafka ingress) | Audit trail logging | ALL services (via `BaseRepository` flows) | ALL DOMAINS | ✅ Active |
| `exc-master-data` | topic | AMQP | Master data CDC | `svc-master-data` (Automotive) | Automotive | ✅ Active |
| `exc-hris-master-data` | topic | AMQP | Master data CDC | `svc-hris-master-data` | HRIS | 🟡 PLANNED |
| `exc-finance-master-data` | topic | AMQP | Master data CDC | `svc-finance-master-data` | Finance | 🟢 FUTURE |
| `exc-file-processing` | direct | AMQP | Thumbnail / file post-processing | `eksad-core-storage` | ALL DOMAINS | ✅ Active |
| `exc-notification` | topic | AMQP | Email / push / SMS dispatch | Various (orchestrator) | ALL DOMAINS | 🟡 PLANNED |
| `exc-domain-events` | topic | AMQP **or** Kafka | Cross-service domain event stream (CQRS) | All domain services | ALL DOMAINS | 🟢 FUTURE (Sprint 4+) |

> Naming convention: `exc-{domain}-{purpose}` for domain-scoped exchanges; `exc-{purpose}` for platform-wide exchanges. See §11 Naming Conventions.

### 1.1 Kafka Topic Registry (opt-in)

Kafka-native services (Stack Profile broker = Kafka) use topics instead of exchanges. A topic carries the **same
envelope** as its AMQP counterpart. Only services whose TSD selects the Kafka broker provision these.

| Topic | AMQP Equivalent | Partition Key | Consumer Group | Purpose | Status |
|-------|-----------------|---------------|----------------|---------|--------|
| `log-activity` | `exc-log-activity` | `tenantId` | `cg-audittrail` | Audit ingress for Kafka-native producers → `eksad-core-audittrail` | 🟡 PLANNED (opt-in) |
| `{domain}.master-data` | `exc-{domain}-master-data` | `tenantId` | `cg-{service}-master-sync` | Master data CDC for Kafka-native domain services | 🟢 FUTURE |
| `domain-events` | `exc-domain-events` | `tenantId` | `cg-{service}` | Cross-service domain stream (CQRS) | 🟢 FUTURE (Sprint 4+) |

> **Topic naming:** `{domain}.{purpose}` (dot-separated, lowercase) — e.g. `automotive.master-data`, `log-activity`.
> **Envelope rule:** Kafka message `value` = the universal envelope (§3) as JSON; Kafka `key` = `tenantId` (or
> `eventId` for strict ordering). Envelope headers (§3) are mirrored as Kafka record headers.

---

## 2. Queue Registry

| Queue | Bound to Exchange | Routing Key Binding | Consumer Service | Domain | Purpose |
|-------|-------------------|---------------------|------------------|--------|---------|
| `q-log-activity-eksad` | `exc-log-activity` | `r.q-log-activity-eksad` | `eksad-core-audittrail` | ALL | Persist audit logs to MongoDB |
| `q-master-sync-pipeline` | `exc-master-data` | `r.brand.*, r.model.*, r.type.*, r.color.*, r.branch.*` | `svc-pipeline` | Automotive | Cache sync for pipeline service |
| `q-master-sync-orders` | `exc-master-data` | `r.brand.*, r.model.*, r.type.*` | `svc-orders` | Automotive | Cache sync for orders service |
| `q-master-sync-payment` | `exc-master-data` | `r.branch.*` | `svc-payment` | Automotive | Cache sync for payment service |
| `q-hris-master-sync-attendance` | `exc-hris-master-data` | `r.department.*, r.position.*, r.grade.*, r.shift_type.*` | `svc-attendance` | HRIS [PLANNED] | Cache sync for attendance service |
| `q-hris-master-sync-leave` | `exc-hris-master-data` | `r.department.*, r.position.*, r.leave_type.*` | `svc-leave` | HRIS [PLANNED] | Cache sync for leave service |
| `q-generate-thumbnail-core-storage` | `exc-file-processing` | `r.q-generate-thumbnail-core-storage` | `eksad-core-storage` | ALL | Async thumbnail generation |
| `q-notification-email` | `exc-notification` | `r.notification.email.*` | `svc-notification` | ALL [PLANNED] | Email delivery worker |
| `q-notification-push` | `exc-notification` | `r.notification.push.*` | `svc-notification` | ALL [PLANNED] | Push worker |

### Dead Letter Queues (DLQ)

Every domain-critical queue has a paired DLQ at `q-{queue-name}-dlq` (or via `x-dead-letter-exchange=exc-{queue}-dlx` for topic exchanges). DLQ depth is monitored as a `WARNING` Prometheus alert (`rabbitmq_queue_messages_ready > 100`).

> Queue naming convention: `q-{action}-{service}` (single-word action) or `q-{domain}-{action}-{service}` (multi-domain disambiguation). See §11.

---

## 3. Event Envelope (Universal)

ALL EKSAD events conform to this envelope format:

```json
{
  "eventType":  "<PROJECT>.<MODULE>.<ACTION>",
  "eventId":    "{uuid-v4}",
  "tenantId":   "{tenant_id}",
  "occurredAt": 1745280000000,
  "actorId":    "{user_id}",         // optional — null for system events
  "actorName":  "{username}",        // optional
  "serviceId":  "{service_name}",
  "correlationId": "{uuid-v4}",      // for tracing
  "payload":    { /* event-specific */ }
}
```

### AMQP Headers (mirrored)
| Header | Value |
|--------|-------|
| `eventType` | Same as envelope |
| `tenantId` | Same as envelope |
| `correlationId` | Same as envelope |
| `routingKey` | Set by publisher |

---

## 4. Master Data Events — Automotive

**Exchange:** `exc-master-data` (topic)
**Routing key pattern:** `r.{entity}.{action}`

| Event Type | Routing Key | Payload | Triggered by |
|------------|-------------|---------|--------------|
| `BRAND.CREATED` | `r.brand.created` | `{ id, name, code, active, ... }` | `POST /api/v1/brands` |
| `BRAND.UPDATED` | `r.brand.updated` | full entity | `PUT /api/v1/brands/{id}` |
| `BRAND.DELETED` | `r.brand.deleted` | `{ id }` | `DELETE /api/v1/brands/{id}` |
| `MODEL.CREATED` | `r.model.created` | `{ id, brand_id, name, code, ... }` | `POST /api/v1/models` |
| `MODEL.UPDATED` | `r.model.updated` | full entity | `PUT /api/v1/models/{id}` |
| `MODEL.DELETED` | `r.model.deleted` | `{ id }` | `DELETE /api/v1/models/{id}` |
| `TYPE.CREATED` | `r.type.created` | `{ id, model_id, name, code, ... }` | `POST /api/v1/types` |
| `TYPE.UPDATED` | `r.type.updated` | full entity | `PUT /api/v1/types/{id}` |
| `TYPE.DELETED` | `r.type.deleted` | `{ id }` | `DELETE /api/v1/types/{id}` |
| `COLOR.CREATED` | `r.color.created` | full entity | `POST /api/v1/colors` |
| `COLOR.UPDATED` | `r.color.updated` | full entity | `PUT /api/v1/colors/{id}` |
| `COLOR.DELETED` | `r.color.deleted` | `{ id }` | `DELETE /api/v1/colors/{id}` |
| `BRANCH.CREATED` | `r.branch.created` | full entity | `POST /api/v1/branches` |
| `BRANCH.UPDATED` | `r.branch.updated` | full entity | `PUT /api/v1/branches/{id}` |
| `BRANCH.DELETED` | `r.branch.deleted` | `{ id }` | `DELETE /api/v1/branches/{id}` |

---

## 5. Master Data Events — HRIS

**Exchange:** `exc-hris-master-data` (topic)

| Event Type | Routing Key | Payload | Triggered by |
|------------|-------------|---------|--------------|
| `DEPARTMENT.CREATED` | `r.department.created` | `{ id, name, code, parent_id?, ... }` | `POST /api/v1/departments` |
| `DEPARTMENT.UPDATED` | `r.department.updated` | full entity | `PUT /api/v1/departments/{id}` |
| `DEPARTMENT.DELETED` | `r.department.deleted` | `{ id }` | `DELETE /api/v1/departments/{id}` |
| `POSITION.CREATED` | `r.position.created` | `{ id, department_id, name, ... }` | `POST /api/v1/positions` |
| `POSITION.UPDATED` | `r.position.updated` | full entity | `PUT /api/v1/positions/{id}` |
| `POSITION.DELETED` | `r.position.deleted` | `{ id }` | `DELETE /api/v1/positions/{id}` |
| `GRADE.CREATED` | `r.grade.created` | `{ id, position_id, name, level, ... }` | `POST /api/v1/grades` |
| `GRADE.UPDATED` | `r.grade.updated` | full entity | `PUT /api/v1/grades/{id}` |
| `GRADE.DELETED` | `r.grade.deleted` | `{ id }` | `DELETE /api/v1/grades/{id}` |
| `LEAVE_TYPE.CREATED` | `r.leave_type.created` | full entity | `POST /api/v1/leave-types` |
| `LEAVE_TYPE.UPDATED` | `r.leave_type.updated` | full entity | `PUT /api/v1/leave-types/{id}` |
| `LEAVE_TYPE.DELETED` | `r.leave_type.deleted` | `{ id }` | `DELETE /api/v1/leave-types/{id}` |
| `SHIFT_TYPE.CREATED` | `r.shift_type.created` | full entity | `POST /api/v1/shift-types` |
| `SHIFT_TYPE.UPDATED` | `r.shift_type.updated` | full entity | `PUT /api/v1/shift-types/{id}` |
| `SHIFT_TYPE.DELETED` | `r.shift_type.deleted` | `{ id }` | `DELETE /api/v1/shift-types/{id}` |

---

## 6. Audit Trail Events

**Producer (always RabbitMQ):**
**Exchange:** `exc-log-activity` (direct) · **Routing key:** `r.q-log-activity-eksad` · **Queue:** `q-log-activity-eksad`

**Consumer (`eksad-core-audittrail`) — DUAL-INGRESS → MongoDB `log_activity`:**

| Ingress channel | Transport | Source | Enabled by | Default |
|-----------------|-----------|--------|------------|---------|
| `in-log-activity-amqp` | RabbitMQ | queue `q-log-activity-eksad` | always-on | ✅ on |
| `in-log-activity-kafka` | Kafka | topic `log-activity` (consumer group `cg-audittrail`) | env `AUDIT_KAFKA_ENABLED=true` | ☐ off |

> **Why dual-ingress:** Every service using `eksad-core-common` emits audit to **RabbitMQ** (producer never
> changes → zero risk for existing services). A future **Kafka-native** service whose team does not run RabbitMQ
> may publish the **identical `LogActivityDTO` envelope** to the Kafka topic `log-activity` instead.
> `eksad-core-audittrail` consumes **both** channels, converges them into `ILogActivityService.post(dto)`, and
> **de-duplicates by `eventId`** (idempotent upsert) so a message delivered on both transports is stored once.

### Audit Consumer Configuration (`eksad-core-audittrail`)

```properties
# RabbitMQ ingress — always enabled
mp.messaging.incoming.in-log-activity-amqp.connector=smallrye-rabbitmq
mp.messaging.incoming.in-log-activity-amqp.queue.name=q-log-activity-eksad

# Kafka ingress — opt-in (only when a Kafka-native producer exists)
audit.kafka.enabled=${AUDIT_KAFKA_ENABLED:false}
mp.messaging.incoming.in-log-activity-kafka.connector=smallrye-kafka
mp.messaging.incoming.in-log-activity-kafka.topic=log-activity
mp.messaging.incoming.in-log-activity-kafka.group.id=cg-audittrail
```

> Producers never hard-code secrets — broker host/credentials always via `${ENV_VAR}`.

### `LogActivityDTO` Shape (producer → broker)

Published as **snake_case JSON** (fields carry `@JsonProperty("snake_case")`; single-word fields like `action`,
`status`, `username`, `role`, `activity` need none). Built exclusively by `eksad-core-common` `LogHandler` —
never constructed manually.

```json
{
  "transaction_id":   "42",
  "action":           "Create Lead",
  "activity":         "user-001 created lead #42",
  "module_type":      "EKSAD_SVC_PIPELINE.LEAD.CREATE",
  "entity_type":      "Lead",
  "entity_id":        "42",
  "username":         "user-001",
  "role":             "ROLE_SALES",
  "tenant_id":        "tenant-ahm",      // top-level tenant — isolation key (EKSAD Principle 4)
  "company_id":       "company-ahm-jkt", // company within the tenant — optional finer scope (nullable)
  "status":           "SUCCESS",         // SUCCESS | FAIL
  "fail_reason":      null,              // populated on FAIL
  "request_uri":      "/api/v1/leads",
  "request_services": "{...}",           // serialized request DTO as JSON string
  "data_before":      null,             // JSON string of entity BEFORE change (null for CREATE)
  "data_after":       "{...}",          // JSON string of entity AFTER change (null for DELETE)
  "log_activity_type": 1,                // numeric activity-type discriminator
  "request_time":     1745280000000,     // epoch ms — operation start
  "response_time":    1745280000150      // epoch ms — operation end
}
```

> **`tenant_id` vs `company_id`:** `tenant_id` is the **isolation key** — always present, always the audit query
> filter (prevents cross-tenant leakage, Principle #4). `company_id` is an **optional finer scope** for the
> scenario where one tenant contains multiple companies (group of companies): same `tenant_id`, different
> `company_id`. Both are sourced from JWT claims. Keep them as **separate fields** — do not alias one to the other.

### Consumer-Computed Field — `data_changes` (JSON diff)

The consumer (`eksad-core-audittrail` `LogActivityService.post()`) computes a field-level diff and stores it in
the document field `data_changes` (a JSON array string). **Producers do NOT send `data_changes`** — they only send
`data_before` / `data_after`.

| Operation | `data_before` | `data_after` | `data_changes` |
|-----------|---------------|--------------|----------------|
| CREATE | `null` / `{}` | entity JSON | `[]` |
| DELETE | entity JSON | `null` | `[]` |
| UPDATE | entity JSON | entity JSON | `[{ "attribute","before","after" }, …]` |

```json
// data_changes — array of LogActivityDifferentDataDTO
[
  { "attribute": "status", "before": "DRAFT",  "after": "SUBMITTED" },
  { "attribute": "amount", "before": "1000",   "after": "1500" }
]
```

> ⚠️ **Producer requirement:** `data_before` / `data_after` MUST be **valid JSON** (serialize the entity with
> Jackson — never `toString()`). The consumer compares them via JSONAssert; invalid JSON is caught non-fatally and
> yields an empty diff (`[]`) — the audit record is still stored, but the compare feature is lost. For entities
> containing arrays/nested objects, prefer a lenient compare mode so element reordering is not reported as a change.

Published automatically by `BaseRepository` flow methods (always to RabbitMQ). Kafka-native producers may publish
the same shape (wrapped in the §3 envelope) to topic `log-activity`.

---

## 7. File Processing Events

**Exchange:** `exc-file-processing` (direct)
**Publisher:** `eksad-core-storage` (self-publishes after upload to trigger async post-processing)
**Consumer:** `eksad-core-storage` (worker pool for thumbnail generation)

| Event Type | Routing Key | Queue | Payload | Purpose |
|------------|-------------|-------|---------|---------|
| `FILE.UPLOADED` | `r.q-generate-thumbnail-core-storage` | `q-generate-thumbnail-core-storage` | `{ fileId, ownerTenantId, mimeType, sourceKey, visibility, refEntityType, refEntityId }` | Trigger async thumbnail generation for image/PDF files |
| `THUMBNAIL.READY` | `r.thumbnail.ready` | (no default consumer — domain services may opt-in) | `{ fileId, thumbnailKey, thumbnailUrl?, generatedAt }` | Notify owning entity / refresh CDN cache |
| `THUMBNAIL.FAILED` | `r.thumbnail.failed` | (no default consumer) | `{ fileId, errorCode, errorMessage, attemptCount }` | Surface for retry / alerting |

### `FILE.UPLOADED` Payload Detail

```json
{
  "eventType":     "FILE.UPLOADED",
  "eventId":       "{uuid-v4}",
  "tenantId":      "{tenant_id}",
  "occurredAt":    1745280000000,
  "serviceId":     "eksad-core-storage",
  "correlationId": "{uuid-v4}",
  "payload": {
    "fileId":         12345,
    "ownerTenantId":  "tenant-ahm",
    "mimeType":       "image/png",
    "sourceKey":      "tenant-ahm/2026/05/uploads/abc123.png",
    "visibility":     "PRIVATE",
    "refEntityType":  "contract",
    "refEntityId":    "987"
  }
}
```

### Supported Source Types for Thumbnail

| MIME prefix | Library | Output |
|-------------|---------|--------|
| `image/png`, `image/jpeg`, `image/gif`, `image/webp` | Thumbnailator | JPEG thumbnail |
| `application/pdf` | Apache PDFBox | JPEG (page 1) |
| Other | — | `thumbnail_status = SKIPPED` |

> See `EKSAD_SYSTEM_DESIGN_PATTERNS.md` §10 (File Storage) and `EKSAD_DOMAIN_GLOSSARY.md` A.8 for the full storage contract.

---

## 8. Notification Events

**Exchange:** `exc-notification` (topic)
**Routing key patterns:** `r.notification.email.*`, `r.notification.push.*`, `r.notification.sms.*`

| Event Type | Routing Key | Payload | Purpose |
|------------|-------------|---------|---------|
| `NOTIFICATION.EMAIL.SEND` | `r.notification.email.send` | `{ to, subject, template, variables }` | Email delivery |
| `NOTIFICATION.PUSH.SEND` | `r.notification.push.send` | `{ user_ref, title, body, data }` | Push notification |
| `NOTIFICATION.SMS.SEND` | `r.notification.sms.send` | `{ to, message }` | SMS (future) |

---

## 9. Auth Events

> **Note:** Auth events are logged **internally** to `eksad-core-auth.auth_events` table — NOT to `exc-log-activity`. They are separate from the business audit trail.

| Event Type | Stored In | Trigger |
|------------|-----------|---------|
| `LOGIN_SUCCESS` | `auth_events` | Successful credential validation |
| `LOGIN_FAILED` | `auth_events` | Wrong password / unknown user |
| `TOKEN_REFRESH` | `auth_events` | Refresh token rotation |
| `TOKEN_REVOKE` | `auth_events` | Logout, kick-oldest, etc. |
| `PASSWORD_CHANGE` | `auth_events` | Password reset/change |
| `LOCKOUT_TRIGGERED` | `auth_events` | Failed attempt threshold reached |
| `KEY_ROTATION` | `auth_events` | Signing key rotated |
| `MFA_ENABLED` / `MFA_VERIFIED` | `auth_events` | MFA setup / verification |

Retention: **90 days** (configurable via `EKSAD_AUTH_EVENT_RETENTION_DAYS`).

---

## 10. Domain Events (per Project — Examples)

Domain events are project-specific. They represent **business state changes** for cross-service consumption. Naming convention:

```
<PROJECT>.<MODULE>.<ACTION>
```

### [Example: Automotive] `svc-pipeline`
- `EKSAD_SVC_PIPELINE.LEAD.CREATED`
- `EKSAD_SVC_PIPELINE.LEAD.QUALIFIED`
- `EKSAD_SVC_PIPELINE.LEAD.CONVERTED`

### [Example: Automotive] `svc-orders`
- `EKSAD_SVC_ORDERS.ORDER.CREATED`
- `EKSAD_SVC_ORDERS.ORDER.SUBMITTED`
- `EKSAD_SVC_ORDERS.ORDER.APPROVED`
- `EKSAD_SVC_ORDERS.ORDER.REJECTED`

### [Example: HRIS] `svc-attendance`
- `EKSAD_SVC_ATTENDANCE.CLOCKIN.RECORDED`
- `EKSAD_SVC_ATTENDANCE.CLOCKOUT.RECORDED`

### [Example: HRIS] `svc-leave`
- `EKSAD_SVC_LEAVE.REQUEST.SUBMITTED`
- `EKSAD_SVC_LEAVE.REQUEST.APPROVED`
- `EKSAD_SVC_LEAVE.REQUEST.REJECTED`

> Domain events are published to `exc-domain-events` (topic). See `EKSAD_CQRS_PATTERNS.md` for the read-model consumption pattern (Sprint 4+).

---

## 11. Naming Conventions

### 11.1 RabbitMQ (default transport)

| Artifact | Pattern | Example |
|----------|---------|---------|
| Exchange | `exc-{purpose}` or `exc-{domain}-{purpose}` | `exc-master-data`, `exc-hris-master-data`, `exc-log-activity` |
| Queue | `q-{action}-{service}` | `q-master-sync-pipeline`, `q-log-activity-eksad` |
| Routing key | `r.{entity}.{action}` or `r.{purpose}` | `r.brand.created`, `r.q-log-activity-eksad` |
| Event type | `<PROJECT>.<MODULE>.<ACTION>` (uppercase) | `BRAND.CREATED`, `EKSAD_SVC_PIPELINE.LEAD.CREATED` |
| DLQ | `q-{queue-name}-dlq` | `q-master-sync-pipeline-dlq` |

### 11.2 Kafka (opt-in transport — Stack Profile broker = Kafka)

> **Style rule:** topics and consumer groups are **lowercase**, **dot-separated** between logical segments, and
> **hyphen-separated** within a multi-word segment (kebab-case). Never use camelCase or underscores in Kafka
> topic/group names. The `eventType` **inside** the envelope is unchanged (`<PROJECT>.<MODULE>.<ACTION>`,
> uppercase) — it is transport-independent, so the same event keeps the same `eventType` on either broker.

| Artifact | Pattern | Example | AMQP Equivalent |
|----------|---------|---------|-----------------|
| Topic (platform-wide) | `{purpose}` | `log-activity` | `exc-log-activity` |
| Topic (domain-scoped) | `{domain}.{purpose}` | `automotive.master-data`, `hris.master-data` | `exc-{domain}-master-data` |
| Topic (domain event stream) | `{domain}.domain-events` (or platform `domain-events`) | `automotive.domain-events` | `exc-domain-events` |
| Consumer group | `cg-{service}` or `cg-{service}-{purpose}` | `cg-audittrail`, `cg-pipeline-master-sync` | (consumer) queue binding |
| Partition key (record key) | `tenantId` (default — per-tenant ordering) | `tenant-ahm` | — (AMQP has no partitions) |
| Strict-order key (opt-in) | `{entity}Id` or `eventId` when per-entity ordering is required | `lead-42` | — |
| Retry topic | `{topic}.retry` (or `.retry-{n}` for tiered backoff) | `log-activity.retry`, `automotive.master-data.retry-1` | `x-message-ttl` requeue |
| Dead Letter Topic (DLT) | `{topic}.dlt` | `log-activity.dlt`, `automotive.master-data.dlt` | `q-{queue}-dlq` |
| Schema subject (Sprint 3+) | `{topic}-value` / `{topic}-key` (Confluent convention) | `log-activity-value` | — |

**Rationale (good-practice notes):**
- **Partition key = `tenantId` by default** → guarantees per-tenant ordering and co-locates a tenant's events on
  one partition (matches Principle #4 `tenant_id` everywhere). Use a finer key (`{entity}Id`) only when strict
  per-entity ordering is required and tenant-level ordering is insufficient.
- **`.dlt` / `.retry` suffixes** follow the SmallRye Reactive Messaging / Spring Kafka community standard, so
  framework auto-config (e.g. `dead-letter-queue.topic`) maps cleanly with zero custom wiring.
- **`cg-` prefix on consumer groups** makes them instantly distinguishable from topics in monitoring dashboards
  and `kafka-consumer-groups.sh` output.
- **Topic = noun/stream, not verb** → name the *stream of data* (`master-data`, `log-activity`), not the action;
  the action lives in the envelope `eventType`. One topic carries many related event types.

### 11.3 Transport-Independent (both brokers)

| Artifact | Pattern | Note |
|----------|---------|------|
| Event type (envelope) | `<PROJECT>.<MODULE>.<ACTION>` (uppercase) | Identical on RabbitMQ and Kafka — see §3 envelope |
| Version suffix | `.v{N}` on breaking change | Applies to `eventType`, routing key, **and** topic — see §14 |
| Tenant scoping | `tenantId` in envelope + (Kafka) as partition key | Principle #4 |

---

## 12. Adding a New Event

1. **Decide transport** per the publishing service's Stack Profile (RabbitMQ default, or Kafka if the service's TSD §3.1 selects it).
2. **Decide destination:**
   - RabbitMQ → master-data event uses existing topic exchange; new domain event → `exc-domain-events`.
   - Kafka → master-data → `{domain}.master-data`; domain event → `{domain}.domain-events`.
3. **Choose key:** RabbitMQ routing key `r.{entity}.{action}`; Kafka partition key `tenantId` (or `{entity}Id` for strict per-entity ordering).
4. **Keep `eventType` transport-independent:** `<PROJECT>.<MODULE>.<ACTION>` — same string on either broker.
5. **Document here:** add a row to the appropriate section above (and §1.1 Kafka Topic Registry if a new topic).
6. **Update producer:** RabbitMQ → `MutinyEmitter.send(Message.of(envelope))`; Kafka → `Emitter`/`KafkaTemplate.send(topic, tenantId, envelope)`.
7. **Update consumer(s):** add `@Incoming` handler (`in-...-amqp` and/or `in-...-kafka`); ensure idempotency (dedup by `eventId`) when both transports may carry the same event.
8. **Add tests:** publish → consume → verify side effect.
9. **Update `EKSAD_DOMAIN_REGISTRY.md`** if adding a new domain.

---

## 13. Registering Events for a New Domain

> Use this 4-step workflow when introducing an **entirely new business domain** (e.g., adding `Healthcare` alongside the existing Automotive / HRIS / Finance). For adding a single new event within an existing domain, use §12 instead.

| # | Step | Owner | Output |
|---|------|-------|--------|
| 1 | **Create the domain master-data exchange** — declare `exc-{domain}-master-data` (topic, durable) in RabbitMQ. Example: `exc-healthcare-master-data`. Add to §1 Exchange Registry as 🟡 PLANNED. | Platform Architect | Exchange declared + registry row |
| 2 | **Define entity events** following `{ENTITY}.{ACTION}` pattern — list every master-data entity in the new domain (e.g., `PATIENT.CREATED`, `CLINIC.UPDATED`, `INSURANCE_PROVIDER.DELETED`). Use past-tense UPPER_SNAKE_CASE. Routing keys follow `r.{entity}.{action}` (lowercase). | SA / Backend Lead | Event list per entity |
| 3 | **Add catalog section to this file** — append `## N. Master Data Events — {Domain}` table after §5 (HRIS). Document every event with routing key + payload schema + trigger endpoint. Add corresponding queue rows to §2 Queue Registry. | Backend Dev / Tech Writer | New section + queue rows |
| 4 | **Update `EKSAD_DOMAIN_REGISTRY.md`** — register the new domain in the registry (services, master-data entities, cache tables, exchange, queues). This unlocks AI-assisted detection for downstream consumers. | SA | Registry updated |

> The 4 steps above MUST run in order. Skipping step 4 leaves the domain undiscoverable by AI/Copilot and breaks the cross-reference invariant in T-12 consistency audit.

### When a Domain Also Needs a Domain Events Exchange (Sprint 4+)

If the new domain also publishes CQRS-style domain events (e.g., `HEALTHCARE_SVC_VISIT.VISIT.COMPLETED`), repeat steps 1–4 for `exc-{domain}-events` as well — but this is **deferred to Sprint 4+** per Decision D6 (CQRS Reserved for Future).

---

## 14. Event Versioning Strategy

EKSAD events follow a **forward-compatible, additive-only** schema-evolution policy. The goal: producers can add fields without breaking existing consumers, and consumers gracefully tolerate unknown fields.

### 14.1 Compatibility Rules

| Change | Compatibility | Action |
|--------|---------------|--------|
| ✅ Add new optional field to `payload` | Forward-compatible (non-breaking) | Bump only producer; no consumer change needed |
| ✅ Add new optional field to envelope (e.g., new metadata) | Forward-compatible | Bump only producer |
| ✅ Add new event type | Non-breaking | New row in catalog; consumers ignore unknown `eventType` |
| ✅ Change field default value | Forward-compatible if business semantics preserved | Producer update only |
| ⚠️ Make optional field required | **Breaking** — bump event version | Use `.v2` suffix |
| ⚠️ Remove a field | **Breaking** — bump event version | Use `.v2` suffix |
| ⚠️ Rename a field | **Breaking** — bump event version | Use `.v2` suffix |
| ⚠️ Change a field's type (e.g., `String` → `Long`) | **Breaking** — bump event version | Use `.v2` suffix |
| ❌ Reuse a deleted field name with different semantics | **NEVER** allowed | Pick a new name entirely |

### 14.2 Version Suffix Convention

Breaking changes get a `.v{N}` suffix on `eventType` and a new routing key:

| Era | Event Type | Routing Key |
|-----|------------|-------------|
| v1 (default — no suffix) | `BRAND.UPDATED` | `r.brand.updated` |
| v2 (after breaking change) | `BRAND.UPDATED.v2` | `r.brand.updated.v2` |

Producers publish v2 alongside v1 for a **transition window** (default: 30 days, configurable per event). Consumers migrate independently. After all consumers are on v2, the producer drops v1 emission.

### 14.3 Consumer Forward-Compatibility Rules

Every consumer MUST:

1. **Ignore unknown fields** in payload silently — never throw on unexpected JSON properties (`@JsonbAnnotation`: do NOT use `FAIL_ON_UNKNOWN_PROPERTIES`; in Jackson, set `DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES = false`).
2. **Skip unknown `eventType`** — log at WARN level, do NOT throw (matches §4 consumer pattern in `EKSAD_CACHE_SYNC_PATTERNS.md`).
3. **Treat missing optional fields as null** — never assume presence.
4. **Stamp `last_synced_at`** from envelope `occurredAt` — version-agnostic.

### 14.4 Schema Registry (Future — Sprint 3+)

Sprint 1–2 use convention-only schema discipline. Sprint 3+ may introduce a JSON Schema registry (e.g., Confluent Schema Registry, Apicurio) to enforce compatibility at publish-time. Documentation here remains the source of truth until then.

### 14.5 Versioning Applies Universally

All exchanges (`exc-master-data`, `exc-hris-master-data`, `exc-file-processing`, `exc-domain-events`, future per-domain exchanges) follow the **same** versioning rules. No exchange-specific exceptions — keeps the developer mental model uniform across the platform.

---

*End of file.*
