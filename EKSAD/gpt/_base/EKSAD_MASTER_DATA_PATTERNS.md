# EKSAD Master Data Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | ALL (Developers, Architects, SA, AI/Claude) |
| **Priority** | 🔴 P0 |
| **Related** | `EKSAD_DOMAIN_REGISTRY.md`, `EKSAD_CACHE_SYNC_PATTERNS.md` (T-07), `EKSAD_EVENT_CATALOG.md` (T-08) |

---

## Table of Contents

1. [Overview](#1-overview)
2. [What Qualifies as Master Data](#2-what-qualifies-as-master-data)
3. [Service Responsibility](#3-service-responsibility)
4. [Per-Domain Catalog Examples](#4-per-domain-catalog-examples)
5. [Database Schema (Generic Template)](#5-database-schema-generic-template)
6. [REST API Catalog](#6-rest-api-catalog)
7. [Event Publishing](#7-event-publishing)
8. [Hierarchical Entities Handling](#8-hierarchical-entities-handling)
9. [Audit Trail](#9-audit-trail)
10. [Performance Considerations](#10-performance-considerations)
11. [Testing](#11-testing)
12. [How Domain Services Consume Master Data](#12-how-domain-services-consume-master-data)
13. [Adding a New Master Data Entity](#13-adding-a-new-master-data-entity)
14. [Known Pitfalls](#14-known-pitfalls)

---

## 1. Overview

`svc-master-data` is the **single source of truth** for shared catalog/reference entities within a business domain.

- Domain services NEVER create/modify master data — they only consume events.
- One instance/namespace per business domain (Automotive, HRIS, Finance).
- Database name: `eksad_{domain}_master` (e.g., `eksad_master` for Automotive).

---

## 2. What Qualifies as Master Data

| Decision Criterion | Classification |
|--------------------|----------------|
| Catalog/reference data referenced by 2+ services within a domain | ✅ **Master data** |
| Countable stock with quantity/availability | ❌ Inventory data (separate `svc-inventory`, future) |
| Domain-specific transactional data | ❌ Domain service |
| Per-tenant configuration | ❌ Tenant config (`svc-tenant-management`) |

---

## 3. Service Responsibility

- CRUD catalog/reference entities + validation.
- Publish events to `exc-{domain}-master-data` (topic exchange).
- Per business domain: separate instance/namespace + database.
- Module type convention: `EKSAD_{DOMAIN}_MASTER.{ENTITY}.{ACTION}` (e.g., `EKSAD_MASTER.BRAND.CREATE`, `EKSAD_HRIS_MASTER.DEPARTMENT.CREATE`).

---

## 4. Per-Domain Catalog Examples

| Domain | Entities | Hierarchy |
|--------|----------|-----------|
| **[Example: Automotive]** | brands, models, types/variants, colors, branches | `brand → model → type` |
| **[Example: HRIS]** | departments, positions, grades, leave_types, shift_types | `department → sub-department`, `position → grade` |
| **[Example: Finance]** | chart_of_accounts, cost_centers, vendors, tax_codes | `coa → sub_account` |

> See `EKSAD_DOMAIN_REGISTRY.md` for the authoritative list.

---

## 5. Database Schema (Generic Template)

```sql
-- Example: V1__create_brands_table.sql
CREATE TABLE brands (
    id              BIGSERIAL    PRIMARY KEY,
    tenant_id       VARCHAR(100) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50)  NOT NULL,
    description     TEXT,
    active          BOOLEAN      NOT NULL DEFAULT TRUE,
    -- BaseEntity columns
    created_at      BIGINT       NOT NULL,
    created_by      VARCHAR(100) NOT NULL,
    updated_at      BIGINT,
    updated_by      VARCHAR(100),
    deleted_at      BIGINT,
    deleted_by      VARCHAR(100),
    version         BIGINT       NOT NULL DEFAULT 0,
    UNIQUE (tenant_id, code) WHERE deleted_at IS NULL
);
CREATE INDEX idx_brands_tenant ON brands (tenant_id);
CREATE INDEX idx_brands_deleted ON brands (deleted_at);
```

### Hierarchical Entity Template
```sql
CREATE TABLE models (
    id              BIGSERIAL    PRIMARY KEY,
    tenant_id       VARCHAR(100) NOT NULL,
    brand_id        BIGINT       NOT NULL REFERENCES brands(id),  -- parent
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50)  NOT NULL,
    -- ... BaseEntity columns
);
CREATE INDEX idx_models_brand ON models (brand_id);
```

---

## 6. REST API Catalog

Per entity:

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/v1/{entity}` | `@RolesAllowed("MASTER_VIEWER")` | List (paginated) |
| `GET` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_VIEWER")` | Detail |
| `POST` | `/api/v1/{entity}` | `@RolesAllowed("MASTER_ADMIN")` | Create |
| `PUT` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_ADMIN")` | Update |
| `DELETE` | `/api/v1/{entity}/{id}` | `@RolesAllowed("MASTER_ADMIN")` | Soft delete |
| `POST` | `/api/v1/{entity}/batch` | `@RolesAllowed("MASTER_VIEWER")` | Batch fetch by IDs (used by cache startup sync) |

### Hierarchical Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/v1/brands/{id}/models` | Direct children |
| `GET` | `/api/v1/models/{id}/types` | Grandchildren |
| `GET` | `/api/v1/{entity}/{id}/descendants` | All descendants (for tree views) |

---

## 7. Event Publishing

Every successful create/update/delete publishes an event to `exc-{domain}-master-data` (topic exchange).

### Event Envelope
```json
{
  "eventType":  "BRAND.CREATED",
  "eventId":    "{uuid-v4}",
  "tenantId":   "tenant-ahm",
  "occurredAt": 1745280000000,
  "payload":    { "id": 42, "name": "Toyota", "code": "TOY", "active": true }
}
```

### Routing Keys
| Pattern | Examples |
|---------|----------|
| `r.{entity}.{action}` | `r.brand.created`, `r.model.updated`, `r.department.deleted` |

### Repository Integration

The repository's `createFlow`/`updateFlow`/`deleteFlow` should fire-and-forget the master-data event **in addition to** the audit log:

```java
@Inject @Channel("master-data-events") MutinyEmitter<JsonObject> emitter;

protected void publishMasterEvent(String eventType, Object payload, String tenantId) {
    JsonObject envelope = new JsonObject()
        .put("eventType",  eventType)
        .put("eventId",    UUID.randomUUID().toString())
        .put("tenantId",   tenantId)
        .put("occurredAt", Instant.now().toEpochMilli())
        .put("payload",    JsonObject.mapFrom(payload));

    OutgoingRabbitMQMetadata meta = OutgoingRabbitMQMetadata.builder()
        .withRoutingKey("r." + entityName.toLowerCase() + "." + actionFromEventType(eventType))
        .build();

    emitter.sendAndForget(Message.of(envelope).addMetadata(meta));
}
```

```properties
mp.messaging.outgoing.master-data-events.connector=smallrye-rabbitmq
mp.messaging.outgoing.master-data-events.exchange.name=exc-master-data
mp.messaging.outgoing.master-data-events.exchange.type=topic
```

> Full event catalog: `EKSAD_EVENT_CATALOG.md`.

---

## 8. Hierarchical Entities Handling

For entities with parent-child relationships (e.g., `brand → model → type`):

- Validate parent exists before creating child.
- Soft-delete cascade: deleting a parent does **NOT** auto-delete children (manual cleanup or block with FK).
- When publishing events for child entities, include `parent_id` in payload so consumers can denormalize.

```java
public Uni<Model> create(ModelCreateDTO dto) {
    return brandRepository.findByIdAndTenant(dto.getBrandId(), tenantContext.getTenantId())
        .onItem().ifNull().failWith(() -> new NotFoundException("Brand not found"))
        .flatMap(brand -> createFlow(dto, ModelModuleType.MODEL.CREATE));
}
```

---

## 9. Audit Trail

All CRUD operations on master data are audited via the standard `BaseRepository.createFlow/updateFlow/deleteFlow` flow (publishes to `exc-log-activity` → `eksad-core-audittrail`).

Module types follow the standard convention:
```
EKSAD_MASTER.BRAND.CREATE
EKSAD_MASTER.MODEL.UPDATE
EKSAD_HRIS_MASTER.DEPARTMENT.DELETE
```

---

## 10. Performance Considerations

| Concern | Approach |
|---------|----------|
| High read load (catalog browsing) | Read replicas (future) — Sprint 1 uses single instance |
| Bulk import (initial seed) | `POST /api/v1/{entity}/bulk-import` — admin only |
| Event publish failure | Fire-and-forget — log error, do NOT roll back DB write (eventual consistency) |
| Event delivery ordering | `last_synced_at` on consumer side handles out-of-order events |

---

## 11. Testing

| Test | Scenarios |
|------|-----------|
| Unit | CRUD operations, hierarchical validation (parent must exist) |
| Integration | Testcontainers PostgreSQL + RabbitMQ → CRUD → verify event published |
| Event | Consumer receives event → verify payload structure |
| Hierarchy | Create brand → create model under brand → query brand's models |
| Soft delete | Delete brand → verify `deleted_at` set, not visible in default queries |

---

## 12. How Domain Services Consume Master Data

> Universal consumer pattern. Full implementation reference: `EKSAD_CACHE_SYNC_PATTERNS.md` (T-07).

### 12.1 Reference by ID Only

Domain entities NEVER store raw master data fields (name, code, description). They store only the foreign-key ID:

```java
@Entity
@Table(name = "leads")
public class Lead extends BaseEntity {
    @Column(name = "brand_id", nullable = false)
    private Long brandId;                   // ✅ reference only

    @Column(name = "model_id", nullable = false)
    private Long modelId;                   // ✅ reference only

    // ❌ NEVER: private String brandName;   <- raw master field forbidden
}
```

Rationale: master data updates (e.g., brand renamed) must NOT require backfilling every domain transaction. Display name resolves via `model_cache.name` JOIN at read time.

### 12.2 Cache Tables (Denormalized Read Replica)

Each consuming domain service maintains local cache tables (`{entity}_cache`) populated by `MasterDataEventConsumer`. Full schema + consumer code in `EKSAD_CACHE_SYNC_PATTERNS.md`.

| Aspect | Rule |
|--------|------|
| Naming | `{entity}_cache` (e.g., `brand_cache`, `model_cache`, `department_cache`) |
| Persistence | `PanacheRepositoryBase` (NOT `BaseRepository`) — no audit columns |
| Mandatory column | `last_synced_at BIGINT NOT NULL` |
| Update path | Event consumer upsert (idempotent) |
| Fallback | Startup sync if cache empty |

### 12.3 Event Consumer (consumer-side outline)

```java
@ApplicationScoped
public class MasterDataEventConsumer {

    @Inject BrandCacheRepository brandCache;
    @Inject ModelCacheRepository modelCache;

    @Incoming("master-data-in")
    public Uni<Void> onEvent(JsonObject envelope) {
        long occurredAt = envelope.getLong("occurredAt");
        String type     = envelope.getString("eventType");
        JsonObject p    = envelope.getJsonObject("payload");

        return switch (type) {
            case "BRAND.CREATED", "BRAND.UPDATED" -> brandCache.upsertIfNewer(p, occurredAt);
            case "BRAND.DELETED"                  -> brandCache.deleteIfNewer(p.getLong("id"), occurredAt);
            case "MODEL.CREATED", "MODEL.UPDATED" -> modelCache.upsertIfNewer(p, occurredAt);
            default -> { log.warn("Unknown event type: {}", type); yield Uni.createFrom().voidItem(); }
        };
    }
}
```

```properties
mp.messaging.incoming.master-data-in.connector=smallrye-rabbitmq
mp.messaging.incoming.master-data-in.exchange.name=exc-master-data
mp.messaging.incoming.master-data-in.exchange.type=topic
mp.messaging.incoming.master-data-in.queue.name=q-master-sync-leads
mp.messaging.incoming.master-data-in.routing-keys=r.brand.*,r.model.*
```

### 12.4 Startup Sync (Safety Net)

If a consumer was down during an event burst, the cache may be incomplete. On startup, every consuming service MUST check whether its cache tables are empty and, if so, fetch a full snapshot via REST:

```java
void onStartup(@Observes StartupEvent ev) {
    brandCache.count()
        .flatMap(c -> c == 0 ? fullSyncFromApi() : Uni.createFrom().voidItem())
        .subscribe().with(unused -> log.info("Brand cache ready"));
}
```

Full reference: `EKSAD_CACHE_SYNC_PATTERNS.md` §6.

### 12.5 Frontend Pattern (Dropdowns)

For create/edit forms, the frontend calls `svc-master-data` REST API **directly** (not the consuming domain service):

```
GET /api/v1/brands?active=true                            ← used by FE dropdown
GET /api/v1/brands/{brandId}/models?active=true           ← cascading dropdown
```

Rationale: ensures dropdowns always reflect the live source of truth. Caching is the FE's concern (e.g., React Query 5-min TTL).

### 12.6 Backend Pattern (Local JOIN)

For list/detail views, the backend uses local JOINs against the denormalized cache tables — NO cross-service REST call:

```sql
-- [Example: Automotive] svc-leads listing
SELECT l.id, l.status, b.name AS brand_name, m.name AS model_name
FROM leads l
JOIN brand_cache b ON b.id = l.brand_id
JOIN model_cache m ON m.id = l.model_id
WHERE l.tenant_id = :tenantId AND l.deleted_at IS NULL;
```

```sql
-- [Example: HRIS] svc-attendance listing
SELECT a.id, a.check_in_at, d.name AS department_name, p.name AS position_name
FROM attendance a
JOIN department_cache d ON d.id = a.department_id
JOIN position_cache  p ON p.id = a.position_id
WHERE a.tenant_id = :tenantId;
```

### 12.7 Decision Matrix — Cache vs. REST

| Use Case | Source | Why |
|----------|--------|-----|
| Create/edit form dropdown | `svc-master-data` REST API | Live source of truth, low frequency |
| List/detail view JOIN | Local `{entity}_cache` table | High read frequency, no network hop |
| Backfill / report generation | Local cache | Avoid hammering master-data service |
| Initial cache population (cold start) | `svc-master-data` REST API `/batch` | One-time startup sync |

---

## 13. Adding a New Master Data Entity

> Universal 9-step workflow for introducing a new master-data entity (any domain).

| # | Step | Owner | Output |
|---|------|-------|--------|
| 1 | **Classify the entity** — open `EKSAD_DOMAIN_REGISTRY.md`; confirm which business domain (Automotive / HRIS / Finance) owns it | SA / Architect | Domain decision |
| 2 | **Confirm it's master data** — apply the §2 decision criteria (catalog/reference + 2+ consumers + low write frequency). If countable inventory or per-tenant config, route to a different service | SA / BA | Yes/No |
| 3 | **Create table + entity in domain's svc-master-data** — Flyway `V{N}__create_{entity}_table.sql` + `@Entity` extending `BaseEntity` + `tenant_id` + `version` + soft-delete columns | Backend Dev | DDL + entity class |
| 4 | **Add `CrudFlows` + event publishing** — repository extends `BaseRepository`, override `toNewEntity()` with `tenant_id` from `UserContext`, hook `publishMasterEvent()` after create/update/delete (see §7) | Backend Dev | Repository + service + resource |
| 5 | **Add routing key to domain's exchange** — extend `r.{entity}.{action}` set (e.g., `r.color.created`, `r.color.updated`, `r.color.deleted`); ensure topic exchange `exc-{domain}-master-data` already exists | Backend Dev | Routing key declared |
| 6 | **Create cache-table Flyway migration in EACH consuming domain service** — `V{N}__create_{entity}_cache_table.sql` with `id`, `tenant_id`, denormalized display fields, `last_synced_at`; `PanacheRepositoryBase` (NOT `BaseRepository`) | Backend Dev (per consumer) | Cache table per consumer |
| 7 | **Add case to `MasterDataEventConsumer` in each consumer** — handle `{ENTITY}.CREATED` / `UPDATED` / `DELETED`, upsert into cache, skip if `occurredAt ≤ last_synced_at` | Backend Dev (per consumer) | Consumer branch + tests |
| 8 | **Add startup sync for the new entity** — extend `StartupCacheSync` to call `GET /api/v1/{entity}` if cache table is empty | Backend Dev (per consumer) | Bootstrap path |
| 9 | **Update knowledge base** — `EKSAD_DOMAIN_REGISTRY.md` (entity list + cache tables) + `EKSAD_EVENT_CATALOG.md` (new routing keys + payload schema) | SA / Tech Writer | Registry + catalog updated |

> Skipping step 8 is the most common bug — cache starts empty, dropdowns fail, list JOINs return null until first event is published.

---

## 14. Known Pitfalls

| # | Pitfall | Symptom | Mitigation |
|---|---------|---------|------------|
| 1 | **Stale cache after event loss** — RabbitMQ outage, consumer crash, or DLQ pile-up causes cache to drift from source of truth | List views show outdated brand/model names; new entries missing from dropdowns | Always implement startup sync (§12.4); add nightly reconciliation job (Sprint 2+); monitor DLQ depth as `WARNING` alert |
| 2 | **Circular dependency** — domain service publishes events BACK to `exc-{domain}-master-data` (e.g., svc-leads emits "brand updated") | Master data corrupted by downstream services; infinite loops; ownership inversion | `exc-{domain}-master-data` is publish-only from `svc-master-data`. Domain services are consumer-only. Enforce via code review + distinct exchange naming (`exc-{domain}-master-data` vs `exc-{domain}-events` for domain-emitted events) |
| 3 | **Cache schema drift** — consumer copies ALL fields from master payload; later master adds 10 new columns; cache table inflates | Migration churn; storage waste; consumers receive fields they don't display | Keep cache schema minimal — only fields needed for display + join keys + `last_synced_at`. Ignore unknown payload fields in consumer (no `@JsonbProperty` enforced on extras) |
| 4 | **Cross-domain master data sharing** — HRIS service consumes Automotive's `exc-master-data`; Finance service consumes HRIS's `exc-hris-master-data` | Domains coupled; one domain's exchange outage breaks others; security boundary violated | Each business domain owns its own master data exchange. Cross-domain integration goes via REST + explicit contract (Option A in `EKSAD_DOMAIN_REGISTRY.md` §6), not by sharing exchanges |
| 5 | **Reference-by-name (anti-pattern)** — domain entity stores `brand_name VARCHAR` instead of `brand_id BIGINT` | Renames in master require backfilling every transaction; tenant data corruption on rename; FK integrity lost | ALWAYS store `{entity}_id BIGINT`. Resolve display name via `{entity}_cache` JOIN at read time |
| 6 | **Missing `last_synced_at` check** — consumer upserts every received event blindly | Late-arriving stale events overwrite fresh state; data regression | Every consumer must guard with `IF event.occurredAt > existing.last_synced_at THEN upsert ELSE skip` |
| 7 | **Treating master-data events as transactional** — caller awaits emit confirmation; rolls back DB on event publish failure | Coupled write path; throughput degraded; consistency goal mismatched | Fire-and-forget (§7). Cache divergence is acceptable short-term and self-heals via startup sync + reconciliation. NOT acceptable for inventory/financial — those need explicit transactional outbox (Sprint 3+) |

---

*End of file. See also: `EKSAD_CACHE_SYNC_PATTERNS.md`, `EKSAD_EVENT_CATALOG.md`.*
