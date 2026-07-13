# EKSAD Cache Sync Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Developers, Architects |
| **Priority** | 🔴 P0 |
| **Related** | `EKSAD_MASTER_DATA_PATTERNS.md`, `EKSAD_EVENT_CATALOG.md`, `EKSAD_RESILIENCE_PATTERNS.md` |

---

## Table of Contents

1. [Why Denormalized Cache](#1-why-denormalized-cache)
2. [3 Patterns Compared](#2-3-patterns-compared)
3. [Cache Table Design](#3-cache-table-design)
4. [Event Consumer Implementation](#4-event-consumer-implementation)
5. [Stale Event Handling](#5-stale-event-handling)
6. [Startup Sync](#6-startup-sync)
7. [RabbitMQ Configuration](#7-rabbitmq-configuration)
8. [Cache Repository (Simple Panache)](#8-cache-repository-simple-panache)
9. [Resilience](#9-resilience)
10. [Testing](#10-testing)
11. [Query Patterns with Cache](#11-query-patterns-with-cache)
12. [Spring Boot Equivalent](#12-spring-boot-equivalent)

---

## 1. Why Denormalized Cache

**Problem:** Cross-service data is needed for display (e.g., **[Example: Automotive]** model name in a leads list; **[Example: HRIS]** department name in an attendance list).

If every read calls master-data over the network → tight coupling + latency + cascading failure.

**Solution:** maintain a local **read-only** copy of master data inside the domain service, synced via events.

**Benefits:**
- Independent services — no runtime coupling.
- Fast local JOINs.
- Resilient — master-data down ≠ domain service down.

---

## 2. 3 Patterns Compared

| Pattern | Approach | Verdict |
|---------|----------|---------|
| 1. FE merge | Frontend fetches each piece separately | ❌ Many round-trips, complex FE |
| 2. Backend enrichment | Service calls master-data on every request | ❌ Tight runtime coupling, latency |
| 3. **Denormalized cache** | Local `_cache` table synced via events | ✅ **Chosen for EKSAD** |

---

## 3. Cache Table Design

### Standards

- Naming: `{entity}_cache` (e.g., `brand_cache`, `model_cache`, `department_cache`).
- Schema: mirror master data + `last_synced_at BIGINT NOT NULL` + `tenant_id`.
- Primary key: same ID as master data entity.
- Hierarchical caches denormalize parent name for display (e.g., `model_cache.brand_name`).
- ❌ Do NOT extend `BaseEntity` — cache tables have no audit columns.
- ❌ Do NOT use `BaseRepository` — use `PanacheRepositoryBase`.
- ❌ No soft-delete columns — cache rows are upserted or hard-deleted.

### Example (Flat)
```sql
CREATE TABLE brand_cache (
    id              BIGINT       PRIMARY KEY,             -- same ID as master
    tenant_id       VARCHAR(100) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50),
    active          BOOLEAN      NOT NULL DEFAULT TRUE,
    last_synced_at  BIGINT       NOT NULL                  -- event ordering
);
CREATE INDEX idx_brand_cache_tenant ON brand_cache (tenant_id);
```

### Example (Hierarchical — Denormalized)
```sql
CREATE TABLE model_cache (
    id              BIGINT       PRIMARY KEY,
    tenant_id       VARCHAR(100) NOT NULL,
    brand_id        BIGINT       NOT NULL,
    brand_name      VARCHAR(200),                          -- denormalized for display
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50),
    last_synced_at  BIGINT       NOT NULL
);
CREATE INDEX idx_model_cache_brand ON model_cache (brand_id);
CREATE INDEX idx_model_cache_tenant ON model_cache (tenant_id);
```

---

## 4. Event Consumer Implementation

```java
@ApplicationScoped
public class MasterDataEventConsumer {

    @Inject BrandCacheRepository brandCache;
    @Inject ModelCacheRepository modelCache;
    @Inject TypeCacheRepository  typeCache;

    @Incoming("master-data-events")
    public Uni<Void> consume(JsonObject envelope) {
        String     eventType  = envelope.getString("eventType");
        long       occurredAt = envelope.getLong("occurredAt");
        JsonObject payload    = envelope.getJsonObject("payload");

        return switch (eventType) {
            case "BRAND.CREATED", "BRAND.UPDATED" -> brandCache.upsert(payload, occurredAt);
            case "BRAND.DELETED"                  -> brandCache.deleteById(payload.getLong("id"));
            case "MODEL.CREATED", "MODEL.UPDATED" -> modelCache.upsert(payload, occurredAt);
            case "MODEL.DELETED"                  -> modelCache.deleteById(payload.getLong("id"));
            case "TYPE.CREATED",  "TYPE.UPDATED"  -> typeCache.upsert(payload, occurredAt);
            case "TYPE.DELETED"                   -> typeCache.deleteById(payload.getLong("id"));
            default -> {
                Log.warnf("Unknown event type: %s — skipping", eventType);
                yield Uni.createFrom().voidItem();
            }
        };
    }
}
```

---

## 5. Stale Event Handling

Events may arrive **out of order**. The consumer MUST skip events older than the cached row's `last_synced_at`.

```java
public Uni<Void> upsert(JsonObject payload, long occurredAt) {
    Long id = payload.getLong("id");
    return findById(id).onItem().transformToUni(existing -> {
        if (existing != null && existing.getLastSyncedAt() >= occurredAt) {
            return Uni.createFrom().voidItem();   // stale event → skip
        }
        BrandCache b = existing != null ? existing : new BrandCache();
        b.setId(id);
        b.setTenantId(payload.getString("tenantId"));
        b.setName(payload.getString("name"));
        b.setLastSyncedAt(occurredAt);
        return persist(b).replaceWithVoid();
    });
}
```

---

## 6. Startup Sync

If the cache table is empty on startup, perform a full sync from `svc-master-data` REST API **before** accepting traffic.

```java
@ApplicationScoped
public class CacheSyncJob {

    @Inject BrandCacheRepository repo;
    @Inject @RestClient MasterDataClient client;

    void onStart(@Observes StartupEvent ev) {
        repo.count().subscribe().with(count -> {
            if (count == 0) {
                Log.info("Brand cache empty — performing startup sync...");
                client.listAllBrands()
                    .onItem().transformToUni(repo::bulkInsert)
                    .subscribe().with(
                        v -> Log.info("Startup sync done"),
                        e -> Log.error("Startup sync failed", e));
            }
        });
    }
}
```

```java
@RegisterRestClient(configKey = "master-data")
@Path("/api/v1")
public interface MasterDataClient {
    @GET @Path("/brands")
    @Timeout(value = 10000)
    Uni<List<BrandDTO>> listAllBrands();
}
```

---

## 7. RabbitMQ Configuration

```properties
mp.messaging.incoming.master-data-events.connector=smallrye-rabbitmq
mp.messaging.incoming.master-data-events.exchange.name=exc-master-data
mp.messaging.incoming.master-data-events.exchange.type=topic
mp.messaging.incoming.master-data-events.queue.name=q-master-sync-pipeline
mp.messaging.incoming.master-data-events.routing-keys=r.brand.*,r.model.*,r.type.*
mp.messaging.incoming.master-data-events.queue.x-dead-letter-exchange=exc-master-data-dlx
mp.messaging.incoming.master-data-events.queue.x-dead-letter-routing-key=dlq.master-data
```

Replace `pipeline` with your service name. For non-default domains, replace `master-data` with `{domain}-master-data` (e.g., `hris-master-data`).

---

## 8. Cache Repository (Simple Panache)

```java
@ApplicationScoped
public class BrandCacheRepository implements PanacheRepositoryBase<BrandCache, Long> {

    public Uni<Void> upsert(JsonObject payload, long occurredAt) { /* see §5 */ }

    public Uni<Void> deleteById(Long id) {
        return delete("id", id).replaceWithVoid();
    }

    public Uni<Void> bulkInsert(List<BrandDTO> brands) {
        long now = Instant.now().toEpochMilli();
        List<BrandCache> entities = brands.stream()
            .map(dto -> {
                BrandCache b = new BrandCache();
                b.setId(dto.getId());
                b.setTenantId(dto.getTenantId());
                b.setName(dto.getName());
                b.setCode(dto.getCode());
                b.setLastSyncedAt(now);
                return b;
            })
            .toList();
        return persist(entities.stream()).replaceWithVoid();
    }
}
```

---

## 9. Resilience

- **Event consumer:** `nack + requeue` on transient error, DLQ after 3 redeliveries (see `EKSAD_RESILIENCE_PATTERNS.md`).
- **Startup sync:** wrap REST call with `@Timeout` + `@Retry`. If it fails, log error but allow service to start (degraded mode — empty cache → falls back to live REST calls).
- **Master-data down at runtime:** cache continues serving stale-but-available data. No impact on domain service operations.

---

## 10. Testing

| Test | Scenario |
|------|----------|
| Unit | Mock event → call consumer → verify upsert |
| Unit | Stale event (`occurredAt < last_synced_at`) → verify skip |
| Unit | Unknown event type → log warning, no action, no exception |
| Unit | DELETE event → cache row removed |
| Integration | Testcontainers RabbitMQ → publish `BRAND.CREATED` → wait → verify cache row |
| Integration | Empty cache → startup → WireMock master-data → verify bulk insert |
| Idempotency | Publish same event twice → verify same cache state (no duplicates) |

See `EKSAD_TESTING_GUIDE.md` Section "Cache Sync Testing".

---

## 11. Query Patterns with Cache

Once cache tables are populated, consuming services run **local JOINs** instead of cross-service REST calls. The patterns below show how to write Panache queries that combine domain tables with `{entity}_cache` tables — always filtered by `tenant_id`.

### 11.1 Automotive — Leads List

```java
@ApplicationScoped
public class LeadQueryRepository implements PanacheRepositoryBase<Lead, Long> {

    public Uni<List<LeadListItemDTO>> findListWithCache(String tenantId, int page, int size) {
        String sql = """
            SELECT  l.id            AS id,
                    l.status        AS status,
                    l.customer_name AS customer_name,
                    b.name          AS brand_name,
                    m.name          AS model_name,
                    br.name         AS branch_name
            FROM    leads l
            JOIN    model_cache  m  ON m.id  = l.model_id
            JOIN    brand_cache  b  ON b.id  = m.brand_id
            JOIN    branch_cache br ON br.id = l.branch_id
            WHERE   l.tenant_id   = :tenantId
              AND   l.deleted_at  IS NULL
            ORDER BY l.created_at DESC
            LIMIT :size OFFSET :offset
        """;
        return getSession().chain(s -> s.createNativeQuery(sql, LeadListItemDTO.class)
            .setParameter("tenantId", tenantId)
            .setParameter("size",     size)
            .setParameter("offset",   page * size)
            .getResultList());
    }
}
```

### 11.2 HRIS — Attendance List

```java
@ApplicationScoped
public class AttendanceQueryRepository implements PanacheRepositoryBase<Attendance, Long> {

    public Uni<List<AttendanceListItemDTO>> findListWithCache(String tenantId, LocalDate day) {
        String sql = """
            SELECT  a.id              AS id,
                    a.check_in_at     AS check_in_at,
                    a.check_out_at    AS check_out_at,
                    d.name            AS department_name,
                    p.name            AS position_name,
                    g.name            AS grade_name
            FROM    attendance      a
            JOIN    department_cache d ON d.id = a.department_id
            JOIN    position_cache   p ON p.id = a.position_id
            JOIN    grade_cache      g ON g.id = a.grade_id
            WHERE   a.tenant_id    = :tenantId
              AND   a.attendance_date = :day
              AND   a.deleted_at   IS NULL
            ORDER BY a.check_in_at
        """;
        return getSession().chain(s -> s.createNativeQuery(sql, AttendanceListItemDTO.class)
            .setParameter("tenantId", tenantId)
            .setParameter("day",       day.atStartOfDay().toInstant(ZoneOffset.UTC).toEpochMilli())
            .getResultList());
    }
}
```

### 11.3 Response DTO (Mapped from Cache)

The DTO carries the **denormalized** display fields directly — no further lookup needed by the controller:

```java
@Data
public class LeadListItemDTO {
    private Long   id;
    private String status;
    private String customerName;
    private String brandName;        // from brand_cache
    private String modelName;        // from model_cache
    private String branchName;       // from branch_cache
}
```

### 11.4 Rules for Cache-Joined Queries

| Rule | Detail |
|------|--------|
| ✅ Always filter by `tenant_id` | On EVERY table in the JOIN — domain row AND each `_cache` row (defense in depth) |
| ✅ Use native SQL or HQL `JOIN` | Cache tables are FKs by ID — never cross-service REST in a list query |
| ✅ Soft-delete filter on domain row only | `_cache` tables don't have `deleted_at` — DELETE event removes the row entirely |
| ✅ Map straight to DTO | Avoid intermediate entity hydration; use `createNativeQuery(sql, DTO.class)` |
| ❌ Never JOIN across services | If a join target is in another service's DB, refactor to event-synced cache |
| ❌ Never call REST in a list iteration | N+1 latency anti-pattern; pre-aggregate via cache JOIN |
| ❌ Never rely on cache for write-side validation | For create/update, fetch the live record via `svc-master-data` REST API (cache may lag) |

> Cross-reference: `EKSAD_MASTER_DATA_PATTERNS.md` §12.6 (Backend Pattern — Local JOIN) shows the same pattern from the master-data consumer perspective.

---

## 12. Spring Boot Equivalent

When the project uses Spring Boot imperative mode, replace Quarkus reactive primitives with the equivalents below. All 9 EKSAD architecture principles still apply unchanged (tenant_id, soft delete, BigDecimal, Long timestamps, etc.).

### 12.1 Mapping Table

| Concern | Quarkus (default) | Spring Boot equivalent |
|---------|-------------------|------------------------|
| Event consumer | `@Incoming("master-data-events")` on method returning `Uni<Void>` | `@RabbitListener(queues = "q-master-sync-{service}")` on method returning `void` |
| Reactive return type | `Uni<Void>` / `Uni<T>` | `void` / `T` (blocking) |
| Repository base | `PanacheRepositoryBase<E, I>` | `JpaRepository<E, I>` |
| Startup hook | `void onStart(@Observes StartupEvent ev)` | `@EventListener(ApplicationReadyEvent.class) public void onStart(...)` |
| REST client | `@RegisterRestClient` + `@Path` interface | `WebClient.Builder` bean → `WebClient` calls, **or** `RestTemplate` (blocking legacy) |
| Resilience annotations | MicroProfile `@Timeout` / `@Retry` / `@CircuitBreaker` | Resilience4j `@TimeLimiter` / `@Retry` / `@CircuitBreaker` |
| Reactive transaction | `@ReactiveTransactional` | `@Transactional` |
| Message metadata | `OutgoingRabbitMQMetadata` | `RabbitTemplate.convertAndSend(exchange, routingKey, payload, postProcessor)` |
| JSON envelope type | `JsonObject` (Vert.x) | `Map<String, Object>` (Jackson) or POJO `EventEnvelope` |

### 12.2 Event Consumer (Spring Boot)

```java
@Component
@RequiredArgsConstructor
public class MasterDataEventListener {

    private final BrandCacheRepository brandCache;
    private final ModelCacheRepository modelCache;

    @RabbitListener(queues = "q-master-sync-pipeline")
    public void onEvent(Map<String, Object> envelope) {
        String type        = (String) envelope.get("eventType");
        long   occurredAt  = ((Number) envelope.get("occurredAt")).longValue();
        @SuppressWarnings("unchecked")
        Map<String, Object> payload = (Map<String, Object>) envelope.get("payload");

        switch (type) {
            case "BRAND.CREATED", "BRAND.UPDATED" -> brandCache.upsert(payload, occurredAt);
            case "BRAND.DELETED"                  -> brandCache.deleteById(((Number) payload.get("id")).longValue());
            case "MODEL.CREATED", "MODEL.UPDATED" -> modelCache.upsert(payload, occurredAt);
            case "MODEL.DELETED"                  -> modelCache.deleteById(((Number) payload.get("id")).longValue());
            default -> log.warn("Unknown event type: {} — skipping", type);
        }
    }
}
```

### 12.3 Cache Repository (Spring Boot)

```java
public interface BrandCacheRepository extends JpaRepository<BrandCache, Long> {

    @Modifying
    @Transactional
    @Query(value = """
        INSERT INTO brand_cache (id, tenant_id, name, code, last_synced_at)
        VALUES (:id, :tenantId, :name, :code, :occurredAt)
        ON CONFLICT (id) DO UPDATE SET
            name           = EXCLUDED.name,
            code           = EXCLUDED.code,
            last_synced_at = EXCLUDED.last_synced_at
        WHERE brand_cache.last_synced_at < EXCLUDED.last_synced_at
        """, nativeQuery = true)
    void upsertIfNewer(@Param("id") Long id,
                       @Param("tenantId") String tenantId,
                       @Param("name") String name,
                       @Param("code") String code,
                       @Param("occurredAt") long occurredAt);
}
```

> The `WHERE last_synced_at < EXCLUDED.last_synced_at` clause is the imperative-mode equivalent of the Quarkus stale-event guard in §5 — atomic and race-free.

### 12.4 Startup Sync (Spring Boot)

```java
@Component
@RequiredArgsConstructor
public class CacheSyncBootstrap {

    private final BrandCacheRepository repo;
    private final MasterDataClient     client;          // WebClient-backed @HttpExchange interface

    @EventListener(ApplicationReadyEvent.class)
    @Async
    public void onReady() {
        if (repo.count() == 0) {
            log.info("Brand cache empty — performing startup sync...");
            try {
                List<BrandDTO> brands = client.listAllBrands().block(Duration.ofSeconds(10));
                repo.saveAll(brands.stream().map(this::toCacheEntity).toList());
                log.info("Startup sync done — {} brands loaded", brands.size());
            } catch (Exception e) {
                log.error("Startup sync failed — running in degraded mode", e);
            }
        }
    }
}
```

### 12.5 REST Client (Spring Boot 6 @HttpExchange)

```java
@HttpExchange(url = "/api/v1")
public interface MasterDataClient {

    @GetExchange("/brands")
    Mono<List<BrandDTO>> listAllBrands();
}

@Bean
WebClient masterDataWebClient(WebClient.Builder builder,
                              @Value("${master-data.base-url}") String baseUrl) {
    return builder.baseUrl(baseUrl).build();
}

@Bean
MasterDataClient masterDataClient(WebClient masterDataWebClient) {
    return HttpServiceProxyFactory
        .builderFor(WebClientAdapter.create(masterDataWebClient))
        .build()
        .createClient(MasterDataClient.class);
}
```

### 12.6 application.yml (Spring Boot)

```yaml
spring:
  rabbitmq:
    host: ${RABBITMQ_HOST:localhost}
    port: ${RABBITMQ_PORT:5672}
    username: ${RABBITMQ_USER:guest}
    password: ${RABBITMQ_PASS:guest}
    virtual-host: eksad_vhost

master-data:
  base-url: ${MASTER_DATA_URL:http://svc-master-data:8086}

resilience4j:
  retry:
    instances:
      master-data:
        max-attempts: 3
        wait-duration: 500ms
  timelimiter:
    instances:
      master-data:
        timeout-duration: 10s
```

Queue + exchange + binding declaration via `@Configuration`:

```java
@Configuration
public class RabbitTopology {

    @Bean TopicExchange masterDataExchange()      { return new TopicExchange("exc-master-data", true, false); }
    @Bean Queue        masterSyncQueue()           { return QueueBuilder.durable("q-master-sync-pipeline")
        .withArgument("x-dead-letter-exchange",    "exc-master-data-dlx")
        .withArgument("x-dead-letter-routing-key", "dlq.master-data")
        .build(); }

    @Bean Binding bindBrand() { return BindingBuilder.bind(masterSyncQueue()).to(masterDataExchange()).with("r.brand.*"); }
    @Bean Binding bindModel() { return BindingBuilder.bind(masterSyncQueue()).to(masterDataExchange()).with("r.model.*"); }
    @Bean Binding bindType()  { return BindingBuilder.bind(masterSyncQueue()).to(masterDataExchange()).with("r.type.*"); }
}
```

### 12.7 Rules (Spring Boot Mode)

| Rule | Detail |
|------|--------|
| ✅ Same envelope schema | `eventType`, `eventId`, `tenantId`, `occurredAt`, `payload` — language-agnostic JSON |
| ✅ Same routing key convention | `r.{entity}.{action}` — exchanges/queues are framework-agnostic |
| ✅ Same idempotency rule | Upsert only if `event.occurredAt > existing.last_synced_at` — enforce via SQL `ON CONFLICT` |
| ✅ Same cache table DDL | No framework-specific columns — works identically across Quarkus / Spring Boot |
| ❌ Never block the RabbitMQ thread | If processing is long, use `@Async` or push to a worker queue |
| ❌ Never put `@Transactional` on the listener method without `propagation = REQUIRES_NEW` | A failure mid-batch should not roll back successfully consumed messages |

> Full Spring Boot ↔ Quarkus mapping reference: `EKSAD_SPRING_BOOT_MAPPINGS.md`.

---

*End of file.*
