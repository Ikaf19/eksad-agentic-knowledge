# EKSAD Resilience Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Developers, Architects |
| **Priority** | 🟡 P1 |
| **Related** | `EKSAD_SYSTEM_DESIGN_PATTERNS.md`, `EKSAD_CODING_STANDARDS.md`, `EKSAD_OBSERVABILITY_PATTERNS.md` |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Sprint Phasing](#2-sprint-phasing)
3. [Timeout Pattern (`@Timeout`)](#3-timeout-pattern-timeout)
4. [Retry Pattern (`@Retry`)](#4-retry-pattern-retry)
5. [Circuit Breaker Pattern (`@CircuitBreaker`)](#5-circuit-breaker-pattern-circuitbreaker)
6. [Fallback Pattern (`@Fallback`)](#6-fallback-pattern-fallback)
7. [Bulkhead Pattern (`@Bulkhead`)](#7-bulkhead-pattern-bulkhead)
8. [Health Checks](#8-health-checks)
9. [RabbitMQ Resilience](#9-rabbitmq-resilience)
10. [Database Connection Pool Resilience](#10-database-connection-pool-resilience)
11. [Standard Error Response Envelope](#11-standard-error-response-envelope)
12. [Resilience per Integration Point](#12-resilience-per-integration-point-summary)
13. [Testing](#13-testing)

---

## 1. Overview

**Problem:** one service down → cascading failure across all services.

EKSAD inter-service communication points to harden:
- **REST calls** — `svc-master-data` startup sync, `eksad-core-auth-client` SDK
- **RabbitMQ** — event publishing/consumption
- **Database** — connection pool exhaustion

**Goal:** isolate failures, degrade gracefully, recover automatically.

---

## 2. Sprint Phasing

| Sprint | Patterns |
|--------|----------|
| **Sprint 1 (MUST)** | ✅ `@Timeout` on ALL REST clients · ✅ Health checks · ✅ Standard error envelope |
| **Sprint 2 (ADD)** | 🟡 `@Retry` · 🟡 `@CircuitBreaker` · 🟡 `@Fallback` · 🟡 `@Bulkhead` |
| **Sprint 3+ (TUNE)** | 🟢 Fine-tune thresholds from production metrics · 🟢 Custom health checks (queue depth, cache freshness) |

---

## 3. Timeout Pattern (`@Timeout`)

- Every external REST call MUST have a timeout.
- Default: **5000 ms (5 s)**, configurable per client.

```java
@RegisterRestClient(configKey = "master-data")
@Path("/api/v1/master")
public interface MasterDataRestClient {

    @GET @Path("/brands")
    @Timeout(value = 5000)
    List<BrandDTO> listBrands();
}
```

```properties
quarkus.rest-client."master-data".url=http://svc-master-data:8086
quarkus.rest-client."master-data".connect-timeout=2000
quarkus.rest-client."master-data".read-timeout=5000
```

> Rule: **NEVER** make an external call without timeout.

---

## 4. Retry Pattern (`@Retry`)

For transient failures: network blip, temporary 503.

```java
@Retry(
    maxRetries  = 3,
    delay       = 1000,
    maxDuration = 10000,
    jitter      = 200,
    retryOn     = { ConnectException.class, TimeoutException.class, WebApplicationException.class },
    abortOn     = { BadRequestException.class, NotFoundException.class }
)
public List<BrandDTO> listBrands() { ... }
```

| Retry | DO NOT retry |
|-------|--------------|
| 5xx errors | 4xx errors (client error) |
| `ConnectException` | Business validation errors |
| `TimeoutException` | — |

---

## 5. Circuit Breaker Pattern (`@CircuitBreaker`)

Prevents repeated calls to a failing service. **States:** CLOSED → OPEN → HALF_OPEN.

```java
@CircuitBreaker(
    requestVolumeThreshold = 10,   // min calls before evaluating
    failureRatio           = 0.5,  // 50% failures → open
    delay                  = 10000, // 10 s before half-open
    successThreshold       = 3     // 3 successes in half-open → close
)
public List<BrandDTO> listBrands() { ... }
```

> Monitoring: circuit state exposed via `/q/health` and Micrometer metrics (`eksad_circuit_breaker_state`).

---

## 6. Fallback Pattern (`@Fallback`)

When circuit is OPEN or all retries exhausted → fallback.

| Integration | Fallback Strategy |
|-------------|-------------------|
| `svc-master-data` REST | Return cached data from `_cache` tables (stale but available) |
| `eksad-core-auth` validate | **Reject login** — no fallback (security-critical) |
| `eksad-core-auth` JWKS | Use cached JWKS keys (cache with TTL) |

```java
@Fallback(fallbackMethod = "fallbackBrands")
public List<BrandDTO> listBrands() { ... }

public List<BrandDTO> fallbackBrands() {
    return brandCacheRepository.listAll().stream()
        .map(this::toDTO).toList();
}
```

> **Rule:** NEVER fall back on security-critical operations (auth, permission checks).

---

## 7. Bulkhead Pattern (`@Bulkhead`)

Isolate thread pools so one slow dependency doesn't block everything.

```java
@Bulkhead(value = 5)   // max 5 concurrent calls
public List<BrandDTO> heavyExternalCall() { ... }
```

Use for: external REST clients, file processing, heavy DB queries. Don't overuse.

---

## 8. Health Checks

Quarkus SmallRye Health (built-in):

| Endpoint | Purpose |
|----------|---------|
| `/q/health/live` | Is the process alive? (container restart) |
| `/q/health/ready` | Is the service ready to accept traffic? (load balancer) |
| `/q/health/started` | Has startup finished? |

### Custom Health Checks per Service
- Database connection (PG pool active connections)
- RabbitMQ broker reachable
- Cache freshness (`last_synced_at` within window, e.g. < 1 hour)
- `eksad-core-auth` JWKS reachable

```java
@Readiness
@ApplicationScoped
public class JwksReachableCheck implements HealthCheck {
    @Inject @RestClient JwksClient jwks;
    @Override public HealthCheckResponse call() {
        try { jwks.get(); return HealthCheckResponse.up("jwks"); }
        catch (Exception e) { return HealthCheckResponse.down("jwks"); }
    }
}
```

### docker-compose Integration
```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost:8082/q/health/ready"]
  interval: 30s
  timeout: 5s
  retries: 3
```

---

## 9. RabbitMQ Resilience

- **Event publishing:** fire-and-forget, but with error logging.
- **Event consumption:**
  - `nack + requeue` on transient error
  - **Dead Letter Queue (DLQ)** on permanent error
  - DLQ name: `q-{queue}-dlq`
  - Retry policy: **3 redeliveries** before DLQ
- Consumer reconnect: Quarkus SmallRye auto-reconnect on broker restart.

```properties
mp.messaging.incoming.master-data.connector=smallrye-rabbitmq
mp.messaging.incoming.master-data.queue.name=q-master-sync-pipeline
mp.messaging.incoming.master-data.queue.x-dead-letter-exchange=exc-master-data-dlx
mp.messaging.incoming.master-data.queue.x-dead-letter-routing-key=dlq.master-data
```

---

## 10. Database Connection Pool Resilience

Quarkus Agroal config (PostgreSQL):

```properties
quarkus.datasource.reactive.max-size=20
quarkus.datasource.reactive.idle-timeout=PT5M
quarkus.datasource.reactive.acquisition-timeout=PT5S
quarkus.datasource.reactive.leak-detection-interval=PT10S
```

- Health check: pool exhaustion warning at **80% usage**.
- On connection failure: Agroal handles retry/backoff automatically.

---

## 11. Standard Error Response Envelope

All services return a consistent format:

```json
{
  "status": "error",
  "error_code": "EKSAD_PIPELINE_VALIDATION_ERROR",
  "message": "Field 'amount' must be > 0",
  "correlation_id": "abc-123-def",
  "timestamp": 1745280000000,
  "details": [ { "field": "amount", "rule": "min", "value": 0 } ]
}
```

- Error codes: `EKSAD_{SERVICE}_{CODE}`.
- Map exceptions to HTTP status codes consistently across all services.

```java
@Provider
public class GlobalExceptionMapper implements ExceptionMapper<Throwable> {
    public Response toResponse(Throwable ex) {
        // map ex → status + error envelope
    }
}
```

---

## 12. Resilience per Integration Point (Summary)

| Integration | Timeout | Retry | Circuit Breaker | Fallback | Sprint |
|-------------|---------|-------|-----------------|----------|--------|
| `svc-master-data` REST (startup sync) | 5 s | 3× | yes | Return cache | Sprint 2 |
| `svc-master-data` REST (on-demand) | 3 s | 2× | yes | Return cache | Sprint 2 |
| `eksad-core-auth-client` validate | 3 s | 2× | yes | **Reject** (no fallback) | Sprint 2 |
| `eksad-core-auth` JWKS | 5 s | 3× | yes | Use cached keys | Sprint 1 (timeout only) |
| RabbitMQ publish | fire-and-forget | — | — | Log error | Sprint 1 |
| RabbitMQ consume | — | `nack` 3× → DLQ | — | Log + skip | Sprint 1 |
| PostgreSQL | Pool acquisition timeout 5 s | — | — | Health check | Sprint 1 |

---

## 13. Testing

| Test Type | Scenario |
|-----------|----------|
| Unit | `@Timeout` mock slow response → `TimeoutException` |
| Unit | `@Retry` 2 failures + 1 success → method succeeds on 3rd attempt |
| Unit | `@Retry` 4xx error → NOT retried (`abortOn`) |
| Unit | `@CircuitBreaker` 50% failures → circuit OPEN |
| Unit | `@CircuitBreaker` OPEN → `@Fallback` returns cached data |
| Integration | Testcontainers — stop `svc-master-data` → domain service returns cached brands |
| Integration | RabbitMQ consumer error 3× → DLQ message verified |
| Integration | Mock DB down → `/q/health/ready = DOWN` |

See `EKSAD_TESTING_GUIDE.md` Section "Resilience Testing".

---

*End of file. Cross-references: `EKSAD_OBSERVABILITY_PATTERNS.md`, `EKSAD_CACHE_SYNC_PATTERNS.md`.*
