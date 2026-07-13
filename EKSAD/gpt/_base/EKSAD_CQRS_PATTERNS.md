# EKSAD CQRS Patterns (Future — Sprint 4+)

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Architects, Senior Developers |
| **Priority** | 🟢 P2 — Reserved for Sprint 4+ |
| **Status** | 📌 **NOT for Sprint 1** — placeholder for future implementation |
| **Related** | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` §16, `EKSAD_EVENT_CATALOG.md` |

> ⚠️ Do NOT implement any CQRS code in Sprint 1. This file documents the planned architecture so the platform stays migration-ready.

---

## 1. When Does EKSAD Need CQRS?

**Trigger:** cross-service dashboard / reporting needs that span 3+ services.

**Examples:**
- Customer journey: lead → order → payment → delivery (across 4 services).
- Conversion funnel analytics.
- Real-time cross-service dashboards.

**NOT needed when:**
- Each service queries its own data only (Sprint 1 default).
- Reports are scheduled batch (not real-time).

---

## 2. EKSAD's Choice: CQRS + Domain Events (NOT Event Sourcing)

### Why NOT Full Event Sourcing
- `CrudFlows` is state-based and works well for current scale.
- Event sourcing adds complexity: event replay, snapshots, schema versioning.
- Audit trail already provides compliance logging.

### EKSAD CQRS Architecture
```
Domain services publish DOMAIN EVENTS → exc-domain-events (topic)
                                              │
                                              ▼
                                       svc-query consumes
                                              │
                                              ▼
                              Read-model tables in eksad_query DB
                                              │
                                              ▼
                          Dashboard / reporting APIs (svc-query)
```

---

## 3. Domain Events vs Audit Events

| Aspect | Audit Events (existing) | Domain Events (future) |
|--------|-------------------------|------------------------|
| Purpose | Compliance logging | Business state propagation |
| Payload | Generic `dataBefore` / `dataAfter` JSON | Typed semantic business payload |
| Exchange | `exc-log-activity` (direct) | `exc-domain-events` (topic) |
| Consumer | `eksad-core-audittrail` (MongoDB) | `svc-query` + future consumers |
| Retention | Forever (compliance) | Configurable per event type |
| Schema | Fixed `LogActivityDTO` | Per-event typed schema |

---

## 4. Domain Event Design Standards

> Producer-facing rules for every domain event published to `exc-domain-events`.

### 4.1 Naming Convention

```
<AGGREGATE>.<PAST_TENSE_VERB>            // bare form (within a project namespace)
<PROJECT>.<AGGREGATE>.<PAST_TENSE_VERB>  // fully-qualified — RECOMMENDED for cross-service catalog
```

| ✅ Good | ❌ Bad | Reason |
|---------|--------|--------|
| `LEAD.QUALIFIED` | `LeadQualified` | Must be UPPER_SNAKE_CASE |
| `ORDER.APPROVED` | `ORDER.APPROVE` | Must be **past tense** (event = something that happened) |
| `EKSAD_SVC_PIPELINE.LEAD.QUALIFIED` | `LEAD.UPDATED` | Use specific business verb (`QUALIFIED`, `CONVERTED`, `REJECTED`), not generic CRUD verbs |
| `PAYMENT.RECEIVED` | `PAYMENT.PAID` | Use receiver-perspective semantic verb |

Rule of thumb: if you can replace the verb with `CREATED`/`UPDATED`/`DELETED` and the event still makes business sense, it's an **audit event**, not a domain event — keep it in `exc-log-activity` instead.

### 4.2 Payload Structure

Payload MUST be **typed, semantic, and self-contained** — consumers should not need to call back to the producer to interpret the event.

```json
{
  "eventType":      "EKSAD_SVC_PIPELINE.LEAD.QUALIFIED",
  "eventId":        "550e8400-e29b-41d4-a716-446655440000",
  "tenantId":       "tenant-ahm",
  "occurredAt":     1716530400123,
  "actorId":        "user-001",
  "serviceId":      "svc-pipeline",
  "correlationId":  "c-9a8b7c6d",       // trace ID — propagated from inbound request
  "causationId":    "e-prev-uuid",      // optional — the eventId that triggered THIS event
  "payload": {
    "leadId":           42,
    "customerRef":      "cust-1138",
    "previousStatus":   "NEW",
    "newStatus":        "QUALIFIED",
    "qualifiedScore":   85,
    "brandId":          7,
    "modelId":          21,
    "qualifiedAt":      1716530400000,
    "qualifiedBy":      "user-001"
  }
}
```

| Payload Rule | Detail |
|--------------|--------|
| ✅ Include relevant IDs | Aggregate ID + foreign keys (brand_id, model_id, etc.) — projections need them for JOINs |
| ✅ Include both `previousStatus` and `newStatus` | Lets consumers detect state transitions without lookup |
| ✅ Include `actorId` + `actorName` | For attribution in dashboards |
| ✅ Self-contained | Consumer can fully project from payload alone — no callbacks |
| ❌ Never include full entity dump | Domain events are **semantic**, not row snapshots (that's master-data events) |
| ❌ Never include sensitive data | Passwords, tokens, PII — projection databases have different ACLs |

### 4.3 Metadata Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `eventId` | ✅ | UUID v4 — dedup key for idempotent consumers (see §10) |
| `correlationId` | ✅ | Distributed-trace ID — propagated from inbound HTTP `X-Correlation-ID` or RabbitMQ message header, enables end-to-end tracing across the read-model build chain |
| `causationId` | ⚪ optional | `eventId` of the event that triggered THIS event — builds causal lineage (e.g., `ORDER.CREATED` → `LEAD.CONVERTED.causationId = ORDER.CREATED.eventId`) |
| `actorId` / `actorName` | ✅ | Who triggered the event (or `system` for automated actions) |
| `serviceId` | ✅ | Producing service name — used by projection switch-case |
| `occurredAt` | ✅ | Epoch ms at event creation — ordering guarantee (see §10) |
| `tenantId` | ✅ | Multi-tenant isolation — projections MUST partition by this |

> Difference vs. master-data events: domain events carry `causationId` to support event-lineage debugging in cross-service workflows. Master-data events do not (single-producer chain).

---

## 5. Migration Path

Extend `CrudFlows` to publish **domain events alongside** audit events. Producer-side change only — additive, non-breaking.

```java
// Inside BaseRepository — future extension
protected Uni<E> createFlow(D dto, String moduleType) {
    return /* existing flow */
        .invoke(saved -> {
            // existing: audit event already fired
            // NEW: also fire typed domain event
            domainEventEmitter.sendAndForget(toDomainEvent(saved, "CREATED"));
        });
}

protected DomainEventEnvelope toDomainEvent(E entity, String action) {
    return DomainEventEnvelope.builder()
        .eventType(entityType() + "." + action)   // e.g., "LEAD.CREATED"
        .eventId(UUID.randomUUID().toString())
        .tenantId(entity.getTenantId())
        .occurredAt(Instant.now().toEpochMilli())
        .payload(entity)
        .build();
}
```

---

## 6. `svc-query` Service Design

**Purpose:** Consume domain events from all services → build denormalized read-model tables → expose query APIs.

| Attribute | Value |
|-----------|-------|
| Service name | `svc-query` |
| Database | PostgreSQL (`eksad_query`) — separate DB |
| Tables | One per read model (`customer_journey`, `sales_funnel`, …) |
| Consumes | All `exc-domain-events` topics |
| Produces | Read-model query APIs (GraphQL or REST) |

### Example Read Model — Customer Journey
```sql
CREATE TABLE customer_journey (
    customer_ref         VARCHAR(100) PRIMARY KEY,
    tenant_id            VARCHAR(100) NOT NULL,
    lead_created_at      BIGINT,
    lead_qualified_at    BIGINT,
    order_created_at     BIGINT,
    order_approved_at    BIGINT,
    payment_received_at  BIGINT,
    delivery_at          BIGINT,
    current_stage        VARCHAR(50),
    last_event_at        BIGINT       NOT NULL
);
CREATE INDEX idx_journey_tenant ON customer_journey (tenant_id, current_stage);
```

### Projection Logic
```java
@Incoming("domain-events")
public Uni<Void> project(JsonObject envelope) {
    String eventType = envelope.getString("eventType");
    return switch (eventType) {
        case "EKSAD_SVC_PIPELINE.LEAD.CREATED" -> journeyRepo.updateLeadCreated(envelope);
        case "EKSAD_SVC_ORDERS.ORDER.CREATED"  -> journeyRepo.updateOrderCreated(envelope);
        case "EKSAD_SVC_PAYMENT.PAYMENT.RECEIVED" -> journeyRepo.updatePayment(envelope);
        // ...
        default -> Uni.createFrom().voidItem();
    };
}
```

---

## 7. Eventual Consistency Tradeoffs

| Operation | Allowed in CQRS read model? |
|-----------|----------------------------|
| Dashboards, reports, analytics | ✅ Yes (eventual consistency acceptable) |
| Transactional UI (create/update) | ❌ NO — query the source service directly |
| Financial calculations | ❌ NO — query source service for accuracy |
| Audit/compliance lookups | ❌ NO — use audit trail |

Lag window goal: **< 5 seconds** under normal load.

---

## 8. Trigger Conditions to Plan CQRS

Plan CQRS when ONE of these is true:
- Dashboard requirement joins data from **3+ services**.
- Aggregated reporting with **sub-second** response targets.
- Read load >> write load (cache insufficient).
- Cross-service analytics needed.

---

## 9. NOT Doing (Avoid Premature Optimization)

| Anti-pattern | Reason |
|--------------|--------|
| ❌ Event sourcing (event-only state) | Too complex, no current business need |
| ❌ Snapshot / replay | Not needed without event sourcing |
| ❌ CQRS for single-service queries | Use direct DB query — CQRS adds latency |
| ❌ CQRS in Sprint 1 | Wait for actual cross-service reporting needs |

---

## 10. Idempotency & Ordering

Domain events are delivered **at-least-once** by RabbitMQ. Read-model projections MUST be idempotent (same event applied twice → same end state) and tolerant of out-of-order delivery.

### 10.1 `processed_events` Dedup Table

Every read-model service maintains a dedup table to record successfully-processed `eventId`s. The projection checks this table BEFORE applying a mutation.

```sql
-- V{N}__create_processed_events_table.sql (in eksad_query DB)
CREATE TABLE processed_events (
    event_id        VARCHAR(64)  PRIMARY KEY,           -- UUID v4 from envelope
    event_type      VARCHAR(200) NOT NULL,
    tenant_id       VARCHAR(100) NOT NULL,
    occurred_at     BIGINT       NOT NULL,              -- event source timestamp
    processed_at    BIGINT       NOT NULL,              -- when projection applied it
    consumer_name   VARCHAR(100) NOT NULL,              -- e.g., "customer_journey"
    UNIQUE (event_id, consumer_name)                    -- same event can be processed by multiple read models
);
CREATE INDEX idx_processed_events_tenant_time
    ON processed_events (tenant_id, occurred_at);
```

> Retention: 90 days (matches audit retention). Older rows are pruned by a nightly batch (Sprint 5+).

### 10.2 Idempotent Projection Pattern

```java
@ApplicationScoped
public class CustomerJourneyProjection {

    @Inject ProcessedEventRepository processedRepo;
    @Inject CustomerJourneyRepository journeyRepo;

    @Incoming("domain-events")
    public Uni<Void> project(JsonObject envelope) {
        String eventId   = envelope.getString("eventId");
        String eventType = envelope.getString("eventType");
        long   occurredAt = envelope.getLong("occurredAt");
        String consumer  = "customer_journey";

        return processedRepo.exists(eventId, consumer)
            .flatMap(seen -> {
                if (seen) {
                    Log.debugf("Event %s already processed by %s — skipping", eventId, consumer);
                    return Uni.createFrom().voidItem();              // idempotent: skip
                }
                return applyProjection(eventType, envelope, occurredAt)
                    .flatMap(v -> processedRepo.markProcessed(eventId, eventType,
                                  envelope.getString("tenantId"), occurredAt, consumer));
            });
    }
}
```

### 10.3 Ordering Guard (Out-of-Order Tolerance)

Like master-data cache (`last_synced_at`), the projection MUST skip events whose `occurredAt` is older than the read-model row's `last_event_at`:

```java
public Uni<Void> updateLeadCreated(JsonObject env) {
    long occurredAt = env.getLong("occurredAt");
    String customerRef = env.getJsonObject("payload").getString("customerRef");

    return findByCustomerRef(customerRef).flatMap(row -> {
        if (row != null && row.getLastEventAt() >= occurredAt) {
            return Uni.createFrom().voidItem();                       // stale — skip
        }
        // apply mutation + bump last_event_at
        return upsertJourney(env, occurredAt);
    });
}
```

### 10.4 Rules

| Rule | Detail |
|------|--------|
| ✅ Always check `processed_events` first | Single SELECT before mutation — sub-millisecond |
| ✅ Always stamp `last_event_at` after mutation | Atomic ordering guard, version-agnostic |
| ✅ Use `UNIQUE (event_id, consumer_name)` | Same event can have multiple projection consumers (e.g., `customer_journey` + `sales_funnel`) |
| ✅ Idempotent for both dedup AND ordering | Together they make projection convergent under retries + out-of-order delivery |
| ❌ Never trust RabbitMQ ordering | Topic exchanges + fanout do NOT guarantee order — assume scrambled |
| ❌ Never rely on `eventId` ordering | UUIDs are not monotonic — use `occurredAt` |
| ❌ Never delete from `processed_events` mid-window | Within retention period, dedup must remain authoritative |

---

## 11. Implementation Phases (4-Phase Roadmap)

CQRS rollout is **incremental** — each phase delivers business value independently. Do NOT skip phases.

### Phase 1 — Publish Domain Events (Sprint 4)

> **Effort:** Low. **Risk:** Low (additive; consumers don't exist yet).

- Extend `BaseRepository.createFlow/updateFlow/deleteFlow` to emit domain events alongside audit events (see §5).
- Declare `exc-domain-events` topic exchange in RabbitMQ.
- Producers publish; no consumers required yet — events are durably queued (or dropped if no binding).
- Define naming convention per project: `EKSAD_SVC_PIPELINE.LEAD.QUALIFIED`, etc. — register in `EKSAD_EVENT_CATALOG.md` §10.

**Exit criteria:** First 3 services emit domain events; envelope schema validated; producer-side latency unchanged (fire-and-forget).

### Phase 2 — `svc-query` + First Read Model (Sprint 5)

> **Effort:** Medium. **Risk:** Medium (introduces new service + new DB).

- Stand up `svc-query` (Quarkus, PostgreSQL `eksad_query` database — separate per `EKSAD_DB_DEPLOYMENT_STRATEGY.md`).
- Create `processed_events` dedup table + first read model table (`customer_journey`).
- Implement projection consumer with idempotency + ordering guards (§10).
- Expose first query API (REST or GraphQL) → dashboard team consumes.
- Set up lag monitoring: Prometheus metric `cqrs_projection_lag_seconds`, alert if > 30s for >5 min.

**Exit criteria:** Customer-journey dashboard live; projection lag < 5s p95 under normal load; cross-tenant isolation verified.

### Phase 3 — Elasticsearch / OpenSearch (Sprint 6+, conditional)

> **Effort:** High. **Risk:** Medium-High. **Trigger:** PostgreSQL read model fails to meet query latency or full-text-search needs.

- Add Elasticsearch (or OpenSearch) as a secondary read-model sink.
- Extend `svc-query` projection consumer to dual-write: PostgreSQL (for transactional aggregates) + ES (for full-text + faceted search).
- Use the same `processed_events` table (one row per `(eventId, consumer_name)` with `consumer_name = "es_customer_journey"`).
- Reconciliation job: nightly diff between PostgreSQL projection and ES — alert on drift > 0.1%.

**Exit criteria:** Full-text search latency < 100ms p95 across all read models; ES cluster healthy + monitored.

**SKIP Phase 3 if** PostgreSQL JSONB + GIN indexes meet query SLAs.

### Phase 4 — Event Replay Capability (Sprint 7+, conditional)

> **Effort:** High. **Risk:** High. **Trigger:** Need to rebuild a read model from scratch (schema migration, new consumer, projection bug fix).

- Persist all domain events in an immutable event store (durable RabbitMQ stream OR dedicated `domain_events` archive table).
- Build `EventReplayService` exposing `POST /api/v1/replay/{consumer_name}?from={epoch_ms}&to={epoch_ms}` — internal API.
- Replay must:
  - Suspend live consumer for target read model
  - Truncate read-model table + clear matching `processed_events` rows
  - Stream archived events in `occurredAt` order
  - Apply projection logic identically to live consumer
  - Resume live consumer once replay completes
- Replay throttled to avoid event-store DoS (default 1000 events/sec).

**Exit criteria:** Replay tested end-to-end for `customer_journey` read model; rebuild from 30-day archive completes in < 15 min.

**SKIP Phase 4 if** read models can be rebuilt acceptably from source services via REST + initial sync (similar to cache startup sync).

### Phase Summary

| Phase | Sprint | Effort | Business Value | Key Deliverable |
|-------|--------|--------|----------------|-----------------|
| 1 | 4 | Low | Future-proofs platform | Domain events flowing |
| 2 | 5 | Medium | First cross-service dashboard | `svc-query` + `customer_journey` |
| 3 | 6+ | High | Full-text + faceted search | Elasticsearch projection |
| 4 | 7+ | High | Rebuildable read models | Replay tooling |

---

*End of file. Reserved for future implementation. Cross-reference: `EKSAD_EVENT_CATALOG.md` §7.*
