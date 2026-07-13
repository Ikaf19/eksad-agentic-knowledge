# EKSAD Base Principles — Shared Knowledge File

> **Usage:** Upload this file as a Knowledge file to ALL EKSAD Custom GPTs.
> This is the single source of truth for EKSAD technology stack, architecture principles,
> audit trail flow, module type convention, and document standards.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Java 21 (LTS) |
| Framework | Quarkus 3.30.6 |
| Persistence (SQL) | Hibernate Reactive Panache + PostgreSQL |
| Persistence (Audit) | MongoDB via `eksad-core-audittrail` service |
| Schema Migration | Flyway — `V{N}__{description}.sql` |
| Messaging | Event broker — **RabbitMQ** (default) **or Kafka** (opt-in) via SmallRye Reactive Messaging. See **Stack Profiles** below. Audit-trail producer is always RabbitMQ. |
| Authentication | JWT RS256 (SmallRye JWT) |
| HTTP | Quarkus REST (RESTEasy Reactive) |
| Serialization | JSON-B |
| Code Generation | Lombok + MapStruct |
| API Docs | SmallRye OpenAPI + Swagger UI |
| Metrics | Micrometer (Prometheus registry) |
| Testing | QuarkusTest + Testcontainers + Mockito |
| Build | Maven (parent POM: `com.eksad:eksad-parent`) |
| Common Library | `com.eksad.core:eksad-core-common` |
| Audit Library | `com.eksad.core:eksad-core-audittrail` |
| Object Storage | AWS S3 **or** Cloudflare R2 (S3-compatible) — switched via `STORAGE_PROVIDER` env var |
| CDN | AWS CloudFront (when `aws`) **or** Cloudflare CDN (when `cloudflare`) |
| File Service | `com.eksad.core:eksad-core-storage` — handles upload, metadata, CDN URL resolution, thumbnail generation |
| Thumbnail (Image) | Thumbnailator — PNG / JPG / GIF / WEBP |
| Thumbnail (PDF) | Apache PDFBox — renders PDF page 1 to JPEG thumbnail |
| Master Data Service | `svc-master-data` (Quarkus 3.30.6) — source of truth for shared catalog/reference entities. Each business domain has its own catalog. See `EKSAD_DOMAIN_REGISTRY.md`. |
| Cache Sync | RabbitMQ topic exchange (`exc-{domain}-master-data`) — event-driven cache population in domain services. Universal across domains. |
| Core Auth | `eksad-core-auth` — credentials, JWT signing (RS256), JWKS. PostgreSQL (`eksad_core_auth`). See `EKSAD_CORE_AUTH_PATTERNS.md`. |
| User Management | `svc-user-management` — user CRUD, RBAC, JWT claim packaging. MongoDB (`eksad_users`). |
| Tenant Management | `svc-tenant-management` — N-level hierarchy, config inheritance. MongoDB (`eksad_tenants`). |

> 📌 **Version:** 1.2 · **Date:** 2026-05-31

---

## Stack Profiles (SA-Selected per Service)

EKSAD now supports **three independent technology axes**. Each service picks one value per axis.
The choice is a **System Analyst decision**, recorded in the TSD (§3 "Architecture / Stack Profile Decision").
Business Analysts never choose these — they only capture business-level async expectations (see Language note below).

| Axis | Options | Default |
|------|---------|---------|
| **Framework** | Quarkus 3.30.6 · Spring Boot 3.x | Quarkus |
| **Paradigm** | Reactive · Imperative | Reactive |
| **Broker** | RabbitMQ · Kafka | RabbitMQ |

**The three axes are independent** — any combination is valid because services only ever talk to each other
via REST or via the **universal event envelope** (transport-agnostic). A Quarkus·Imperative·Kafka service and a
Spring Boot·Reactive·RabbitMQ service interoperate transparently.

### Support Tiers

| Tier | Profile | Meaning |
|------|---------|---------|
| **Tier-1 (battle-tested)** | Quarkus · Reactive · RabbitMQ | Reference profile — most existing services. Pick this when unsure. |
| **Tier-1 (battle-tested)** | Spring Boot · Imperative · RabbitMQ | Fully supported imperative path (`eksad-svc-txn-sb`). |
| **Tier-2 (allowed)** | Any other combination (e.g. Quarkus·Imperative, Spring Boot·Reactive, any ·Kafka) | Permitted for scalability/team-familiarity reasons. Document the rationale in the TSD. |

> **Default rule:** When the TSD does not specify a profile, assume **Quarkus · Reactive · RabbitMQ** (status quo —
> existing services keep their behaviour with zero change).

### Broker Selection Guidance

| Choose **RabbitMQ** when… | Choose **Kafka** when… |
|---------------------------|------------------------|
| Default; command/work-queue semantics; per-message routing; DLQ-based retries | High-throughput event streaming, replayable log, many consumer groups, or the owning team is Kafka-native |

> **Audit-trail constraint:** Regardless of a service's broker choice, the **audit producer** in
> `eksad-core-common` always publishes to **RabbitMQ** (`exc-log-activity`). `eksad-core-audittrail` runs a
> **dual-ingress** consumer (RabbitMQ always-on + optional Kafka topic `log-activity`), so a Kafka-native service
> may emit the same audit envelope to Kafka instead. See `EKSAD_EVENT_CATALOG.md §6`.

---

## Non-Negotiable Architecture Principles

| # | Principle | Rule |
|---|-----------|------|
| 1 | No logic in gateway | API gateway = JWT validation + routing only. No business logic. Gateway is **optional** (see Decision 13). |
| 2 | Service owns its schema | No cross-service DB JOINs. Use RabbitMQ events or REST for inter-service data. |
| 3 | Events over sync calls | Async event broker (RabbitMQ or Kafka — per service Stack Profile) for notifications, audit, cross-service data sync. HTTP for user-facing requests only. The event envelope is identical across brokers; only the transport differs. |
| 4 | `tenant_id` everywhere | Every DB row, every JWT claim, every RabbitMQ event message must carry `tenant_id`. |
| 5 | Flyway only | All DDL in versioned `V{N}__{description}.sql` files. Never `ddl-auto=update` in production. |
| 6 | Auto audit trail | All CRUD via `BaseRepository.createFlow()` / `updateFlow()` / `deleteFlow()`. Audit fires automatically. Never wire RabbitMQ manually for auditing. |
| 7 | Long epoch timestamps | All timestamps in PostgreSQL as `BIGINT` (Java `Long`, epoch ms). Never `TIMESTAMP`, `Date`, `LocalDateTime`. |
| 8 | Soft delete | Never hard-delete. Use `deleted_at BIGINT` + `deleted_by VARCHAR` from `BaseEntity`. |
| 9 | File reference by ID only | Domain services must **never** store raw S3 keys or CDN URLs. Store only `file_id BIGINT` referencing `eksad-core-storage`. Resolve URLs at render-time via `GET /api/v1/storage/{fileId}/url`. |
| 10 | Right DB for right job | PostgreSQL for transactional domain services. MongoDB for audit trail, user-mgmt, tenant-mgmt only. Do NOT use MongoDB for transactional/financial data. Redis/Elasticsearch added only when specific scaling needs arise. |
| 11 | Master data via dedicated service | Shared catalog entities live in `svc-master-data` per business domain. Each domain defines its own catalog (Automotive: brands/models/types; HRIS: departments/positions/grades). See `EKSAD_DOMAIN_REGISTRY.md`. Domain services store reference IDs + local cache. Never duplicate master data ownership. |
| 12 | Denormalized cache via events | Domain services maintain local `{entity}_cache` tables synced via RabbitMQ events from `svc-master-data`. Read queries use local JOINs — zero external API calls at read time. |
| 13 | Tenant-configurable reserved fields | Transactional entities **opt-in** to reserved field columns (5 string, 3 numeric, 2 date, 2 boolean, 1 JSONB overflow). Tenants configure display labels, visibility, and validation via `reserved_field_config`. Zero code change for new tenant custom fields. See `EKSAD_RESERVED_FIELD_PATTERNS.md`. |
| 14 | Independent repo per service | Every service lives in its **own Git repository** with its own CI/CD pipeline and Docker image. `eksad-parent` is a **published BOM** (Model B) — not a monorepo reactor. Services communicate via REST or RabbitMQ only — never as Maven `<dependency>` of each other. See `EKSAD_REPO_STRATEGY.md`. |

**Additional rules:**
- Financial values: always `NUMERIC(20,4)` in PostgreSQL, `BigDecimal` in Java. Never `FLOAT`, `DOUBLE`, or `VARCHAR`.
- No hard-coded credentials: always use `${ENV_VAR}` pattern.
- File uploads: always routed through `eksad-core-storage`. Never upload directly to S3/R2 from a domain service.
- File size cap: enforced by `STORAGE_MAX_FILE_SIZE_MB` env var (default `20`).
- MIME allowlist: enforced by `STORAGE_ALLOWED_MIME_TYPES` env var (e.g. `image/png,image/jpeg,application/pdf`).
- Every domain service MUST validate JWT independently via JWKS from `eksad-core-auth` — gateway is optional (Decision 13).

---

## Auto Audit Trail Flow

```
Developer calls repository.createFlow(dto, moduleType)
                         .updateFlow(dto, moduleType, guard, errorFn, mutator)
                         .deleteFlow(dto, moduleType, softDeleteMutator())

  ↓ [inside eksad-core-common — automatic]

LogHandler.logSuccess() / logFailure()
  → LogHandler.publish():
      emitter.send(Message.of(json, Metadata.of(rabbitMQMetadata)))  ← Uni<Void> discarded (fire-and-forget)
      RabbitMQ metadata: routingKey="r.q-log-activity-eksad", deliveryMode=2 (persistent), timestamp=now()
      Publish failures are caught (try/catch) and logged to stderr — NEVER propagate to caller

  ↓ Exchange: exc-log-activity  →  Queue: q-log-activity-eksad   [RabbitMQ — always-on]

  ↓ [inside eksad-core-audittrail service — automatic, DUAL-INGRESS]

@Incoming("in-log-activity-amqp")     ← RabbitMQ ingress (default, always enabled)
@Incoming("in-log-activity-kafka")    ← Kafka ingress (opt-in, AUDIT_KAFKA_ENABLED=true, topic "log-activity")
  → ILogActivityService.post(dto)     ← both channels converge here; dedup by eventId
  → MongoDB collection: log_activity
```

> **Producer side is RabbitMQ-only and never changes** — every service that uses `eksad-core-common` emits audit
> to RabbitMQ. **Consumer side is dual-ingress** — a Kafka-native service that does not run RabbitMQ may instead
> publish the identical audit envelope to the Kafka topic `log-activity`; `eksad-core-audittrail` consumes both
> and de-duplicates by `eventId`. See `EKSAD_EVENT_CATALOG.md §6`.

Developer only needs to:
1. Extend `BaseRepository<E, D, I>` from `eksad-core-common`
2. Implement 5 abstract methods: `moduleType`, `toId`, `extractDtoId`, `extractTransactionId`, `toNewEntity`
3. Call `createFlow` / `updateFlow` / `deleteFlow` — never call `persist()` directly
4. Add 4 env vars: `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USERNAME`, `RABBITMQ_PASSWORD`

---

## Module Type Naming Convention

Every audit-logged operation requires a `logActivityModuleType` string:

```
Format: <PROJECT>.<MODULE>.<ACTION>

PROJECT = service name in UPPER_SNAKE_CASE   e.g. EKSAD_SVC_LEADS, EKSAD_TIA
MODULE  = domain entity/context               e.g. TRANSACTION, SUBMISSION, APPROVAL
ACTION  = verb in UPPER_SNAKE_CASE            e.g. CREATE, UPDATE, DELETE, SUBMIT, APPROVE, REJECT
```

Examples:
- `EKSAD_SVC_LEADS.TRANSACTION.CREATE`
- `EKSAD_TIA.SUBMISSION.SUBMIT`
- `EKSAD_TIA.APPROVAL.APPROVE`
- `EKSAD_CORE_STORAGE.FILE.UPLOAD`
- `EKSAD_CORE_STORAGE.FILE.DELETE`
- `EKSAD_CORE_STORAGE.FILE.ACCESS` _(reserved — for confidential file access audit, future use)_

Always include a **Module Type** column in every API catalog table in FSD and TSD documents.

---

## Database Table Standards

Every table MUST have these columns:

```sql
id           BIGSERIAL PRIMARY KEY,
tenant_id    VARCHAR(100) NOT NULL,
-- ... domain columns ...
deleted_at   BIGINT NULL,
deleted_by   VARCHAR(100) NULL,
created_at   BIGINT NOT NULL,
created_by   VARCHAR(100) NOT NULL,
updated_at   BIGINT NULL,
updated_by   VARCHAR(100) NULL
```

Indexes required on: `tenant_id`, `deleted_at`, `created_at`, and all filter/FK columns.

---

## Document Requirement ID Standards

| Type | Format | Example |
|------|--------|---------|
| Functional Requirement | `FR-{MODULE}-{NNN}` | `FR-AUTH-001` |
| Non-Functional Requirement | `NFR-{NNN}` | `NFR-001` |
| Business Rule | `BR-{NNN}` | `BR-001` |
| User Story | `US-{MODULE}-{NNN}` | `US-AUTH-001` |

---

## Standard Platform Business Rules (Apply to ALL Projects)

| ID | Rule |
|----|------|
| BR-PLATFORM-001 | Records must never be permanently deleted (soft delete). |
| BR-PLATFORM-002 | Every data-modifying action must be recorded in the audit trail automatically. |
| BR-PLATFORM-003 | Users must only access data belonging to their own tenant. |
| BR-PLATFORM-004 | All API access requires authentication (valid JWT). |
| BR-PLATFORM-005 | Access to features is controlled by user roles (RBAC). |
| BR-PLATFORM-006 | Files must be uploaded through `eksad-core-storage` only. Domain services store `file_id`, never raw keys or URLs. |
| BR-PLATFORM-007 | PUBLIC files are served via permanent CDN URL. PRIVATE files are served via short-lived signed CDN URL generated at request-time (TTL = `STORAGE_SIGNED_URL_TTL_SECONDS`, default `300` seconds). |
| BR-PLATFORM-008 | Thumbnail visibility inherits from its parent file. A PRIVATE file always has a PRIVATE thumbnail. |
| BR-PLATFORM-009 | File size and MIME type are enforced at upload by `eksad-core-storage`. Domain services must not re-validate these. |
| BR-PLATFORM-010 | Master/catalog data entities must be created and updated exclusively through `svc-master-data`. Which entities are master data depends on the business domain — see `EKSAD_DOMAIN_REGISTRY.md`. Domain services must never directly insert or modify master/catalog data — only consume events. |
| BR-PLATFORM-011 | Cache tables in domain services must include `last_synced_at BIGINT` for event ordering. Stale events (where event `occurredAt` ≤ `last_synced_at`) must be skipped. |
| BR-PLATFORM-012 | Every domain service must implement startup cache sync — if cache table is empty on startup, perform full sync from `svc-master-data` REST API before accepting traffic. |
| BR-PLATFORM-013 | Every transactional entity that opts-in to reserved fields must include 13 reserved field columns per `EKSAD_RESERVED_FIELD_PATTERNS.md`. Master data, cache tables, and audit logs are exempt. |
| BR-PLATFORM-014 | Reserved field display labels, visibility, and validation rules are configured per tenant in `reserved_field_config`. Configuration changes take effect without code deployment. |
| BR-PLATFORM-015 | Every EKSAD service must live in its own Git repository (one service = one repo = one CI/CD pipeline = one Docker image). Services must never be declared as Maven `<dependency>` of another service. `eksad-parent` is a published BOM POM only — not a monorepo reactor. See `EKSAD_REPO_STRATEGY.md`. |

---

## Standard Auth Test Scenarios (Apply to EVERY API Endpoint)

| Scenario | Expected |
|----------|----------|
| No Authorization header | 401 |
| Expired JWT | 401 |
| Invalid JWT signature | 401 |
| Valid JWT, wrong role | 403 |
| Valid JWT, wrong tenant | 403 |
| Valid JWT, correct role and tenant | 2xx |

---

## API Catalog Table Format

| Method | Path | Auth Role | Request Body | Response | Module Type | Description |
|--------|------|-----------|--------------|----------|-------------|-------------|

HTTP status conventions:
- `POST` → 201 Created
- `GET` → 200 OK
- `PUT` → 200 OK
- `PATCH` (state change) → 200 OK
- `DELETE` (soft) → 200 OK
- Base path: `/api/v{N}/{resource}`

---

## RabbitMQ Event Envelope (Custom Domain Events)

```json
{
  "eventType"  : "<PROJECT>.<MODULE>.<ACTION>",
  "eventId"    : "{uuid-v4}",
  "tenantId"   : "{tenant_id}",
  "actorId"    : "{user_id}",
  "actorName"  : "{username}",
  "occurredAt" : 1745280000000,
  "serviceId"  : "{service_name}",
  "payload"    : {}
}
```

Naming: Exchange `exc-{domain}` · Queue `q-{action}-{service}` · Routing key `r.q-{action}-{service}`

---

## Master Data Event Envelope

Published by `svc-master-data` to `exc-{domain}-master-data` (topic exchange):

```json
{
  "eventType"  : "BRAND.CREATED | MODEL.UPDATED | TYPE.DELETED | ...",
  "eventId"    : "{uuid-v4}",
  "tenantId"   : "{tenant_id}",
  "occurredAt" : 1745280000000,
  "payload"    : { /* full entity fields */ }
}
```

**Routing keys:** `r.{entity}.{action}` — e.g. `r.brand.created`, `r.model.updated`, `r.department.created`, `r.position.updated`

**Consumer queues:** `q-master-sync-{service}` per domain service (or `q-{domain}-master-sync-{service}` for non-default domains).

---

## Language Policy

- User writes **English** → respond in English
- User writes **Bahasa Indonesia** → respond in Bahasa Indonesia
- All code, class/method names, config keys, IDs stay in English regardless of conversation language
- Documents produced in **English** by default unless user specifies otherwise

---

## Stack Profiles — Framework & Paradigm Mappings

A service's Stack Profile (Framework × Paradigm × Broker — see **Stack Profiles** above) determines the concrete
APIs developers use. The pattern mappings below are equivalent; **all 14 architecture principles apply unchanged
regardless of the chosen profile.**

### Framework × Paradigm

| Concern | Quarkus · Reactive (default) | Spring Boot · Imperative | Quarkus · Imperative | Spring Boot · Reactive (WebFlux) |
|---|---|---|---|---|
| Return type | `Uni<T>` / `Multi<T>` | `T` (blocking) | `T` (blocking) | `Mono<T>` / `Flux<T>` |
| Transaction | `@ReactiveTransactional` | `@Transactional` | `@Transactional` | `@Transactional` (reactive tx mgr) |
| Auth | `@RolesAllowed` | `@PreAuthorize("hasRole('...')")` | `@RolesAllowed` | `@PreAuthorize(...)` |
| Repository base | `PanacheRepositoryBase<E,I>` | `JpaRepository<E,I>` | `PanacheRepositoryBase<E,I>` (blocking) | `ReactiveCrudRepository<E,I>` |

### Broker (transport only — envelope is identical)

| Concern | RabbitMQ (default) | Kafka |
|---|---|---|
| Outbound publish | `MutinyEmitter.send(Message.of(...))` (discard `Uni`) / `RabbitTemplate.convertAndSend()` | `Emitter<>`/`KafkaTemplate.send(topic, key, value)` |
| Inbound consume | `@Incoming("in-...-amqp")` | `@Incoming("in-...-kafka")` / `@KafkaListener` |
| Routing | exchange + routing key (`exc-{domain}`, `r.q-...`) | topic + partition key (`{domain}.{entity}`) |
| Retry / DLQ | DLQ via `x-dead-letter-exchange` | consumer-group offset + retry topic / DLT |

> Pick the profile in the TSD. `eksad-core-common`/`BaseRepository`, `CrudFlows`, `auditMutator`, and
> `GenericResponseDTO` are framework-agnostic and used identically across all profiles.
