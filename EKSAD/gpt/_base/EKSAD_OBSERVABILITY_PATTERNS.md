# EKSAD Observability Patterns

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | Developers, DevOps, Architects |
| **Priority** | 🟡 P1 |
| **Related** | `EKSAD_RESILIENCE_PATTERNS.md`, `EKSAD_CODING_STANDARDS.md`, `EKSAD_CICD_CONTAINER_PATTERNS.md` |

---

## Table of Contents

1. [Overview — The 3 Pillars](#1-overview--the-3-pillars-of-observability)
2. [Sprint Phasing](#2-sprint-phasing)
3. [Structured Logging (Sprint 1)](#3-structured-logging-sprint-1--day-1)
4. [Correlation ID Propagation (Sprint 1)](#4-correlation-id-propagation-sprint-1--day-1)
5. [Distributed Tracing — OpenTelemetry + Jaeger (Sprint 2)](#5-distributed-tracing--opentelemetry--jaeger-sprint-2)
6. [Metrics — Micrometer + Prometheus + Grafana (Sprint 2)](#6-metrics--micrometer--prometheus--grafana-sprint-2)
7. [Grafana Dashboard Templates (Sprint 3)](#7-grafana-dashboard-templates-sprint-3)
8. [Alerting Rules (Sprint 3)](#8-alerting-rules-sprint-3)
9. [Log Aggregation (Sprint 3+)](#9-log-aggregation-sprint-3-optional)
10. [Coding Standards Integration](#10-coding-standards-integration)
11. [Testing](#11-testing)

---

## 1. Overview — The 3 Pillars of Observability

| Pillar | What it answers | Tool |
|--------|-----------------|------|
| **Logs** | What happened? | Structured JSON logs |
| **Traces** | How requests flow across services? | OpenTelemetry + Jaeger |
| **Metrics** | How is the system performing? | Micrometer + Prometheus + Grafana |

All three are **connected via `correlation_id`**.

---

## 2. Sprint Phasing

| Sprint | Items |
|--------|-------|
| **Sprint 1 (MUST)** | ✅ Structured logging (JSON + `correlation_id`) · ✅ Health check endpoints · ✅ Correlation ID propagation |
| **Sprint 2 (ADD)** | 🟡 OpenTelemetry → Jaeger · 🟡 Micrometer → Prometheus |
| **Sprint 3+ (ENHANCE)** | 🟢 Grafana dashboards per service · 🟢 Alerting (Slack/PagerDuty) · 🟢 Log aggregation (Loki/ELK) |

---

## 3. Structured Logging (Sprint 1 — Day 1)

- ALL logs in production MUST be **JSON format**.
- Quarkus config:
  ```properties
  %prod.quarkus.log.console.json=true
  %dev.quarkus.log.console.json=false   # keep human-readable in dev
  ```

### Standard Log Fields
- `timestamp`, `level`, `logger`, `message`, `thread`
- `correlation_id` (from MDC)
- `tenant_id` (from JWT / MDC)
- `service_name` (from env var `EKSAD_SERVICE_NAME`)
- `user_ref` (from JWT / MDC, if available)

### Log Levels

| Level | Use for |
|-------|---------|
| `ERROR` | Unexpected failures, requires attention |
| `WARN` | Recoverable issues (circuit open, retry triggered, stale event skipped) |
| `INFO` | Business events (entity created, login success, cache synced) |
| `DEBUG` | Technical detail (SQL queries, request/response payloads) |

### Never Log
- ❌ Passwords, tokens, API keys
- ❌ PII in plain text (full name + ID combos)
- ❌ Full stack traces at INFO level

---

## 4. Correlation ID Propagation (Sprint 1 — Day 1)

### Flow
1. Request arrives → check `X-Correlation-ID` header → use it, or generate UUID.
2. Store in **MDC** (Mapped Diagnostic Context) → all logs include it automatically.
3. Propagate to downstream calls:
   - **REST client:** add `X-Correlation-ID` header
   - **RabbitMQ:** add `correlation_id` to message envelope **and** AMQP headers
   - **`eksad-core-auth-client` SDK:** auto-propagate

### Server-Side Filter

```java
@Provider
@Priority(Priorities.AUTHENTICATION - 10)
public class CorrelationIdFilter implements ContainerRequestFilter, ContainerResponseFilter {
    public static final String HEADER = "X-Correlation-ID";

    @Override
    public void filter(ContainerRequestContext req) {
        String corr = req.getHeaderString(HEADER);
        if (corr == null || corr.isBlank()) corr = UUID.randomUUID().toString();
        MDC.put("correlation_id", corr);
        req.setProperty("correlation_id", corr);
    }

    @Override
    public void filter(ContainerRequestContext req, ContainerResponseContext res) {
        Object corr = req.getProperty("correlation_id");
        if (corr != null) res.getHeaders().add(HEADER, corr);
        MDC.remove("correlation_id");
    }
}
```

### Client-Side Filter
```java
@Provider
public class CorrelationIdClientFilter implements ClientRequestFilter {
    @Override
    public void filter(ClientRequestContext ctx) {
        String corr = MDC.get("correlation_id");
        if (corr != null) ctx.getHeaders().add("X-Correlation-ID", corr);
    }
}
```

### Visual
```
Client → Gateway [gen: abc-123] → svc-pipeline [abc-123] → svc-master-data [abc-123]
                                                       → RabbitMQ (header: abc-123) → audittrail [abc-123]
```

> Debugging tip: search all logs by `correlation_id` → see the full request journey across services.

---

## 5. Distributed Tracing — OpenTelemetry + Jaeger (Sprint 2)

Quarkus OpenTelemetry extension (built-in):

```properties
quarkus.otel.exporter.otlp.endpoint=http://jaeger:4317
quarkus.otel.service.name=${EKSAD_SERVICE_NAME}
quarkus.otel.traces.sampler=parentbased_traceidratio
quarkus.otel.traces.sampler.arg=1.0   # 100% in dev, lower in prod
```

### Auto-Instrumented
- JAX-RS endpoints, REST clients, JDBC, RabbitMQ (Reactive Messaging).

### Custom Spans
```java
@WithSpan("process-login")
public TokenResult login(LoginRequest request) { ... }
```

> **Trace ID == correlation_id** for consistency. Configure W3C `traceparent` propagation alongside `X-Correlation-ID`.

### docker-compose
```yaml
jaeger:
  image: jaegertracing/all-in-one:latest
  ports: ["16686:16686", "4317:4317"]
```
Jaeger UI: `http://localhost:16686`.

---

## 6. Metrics — Micrometer + Prometheus + Grafana (Sprint 2)

Quarkus Micrometer extension (built-in). Metrics endpoint: `/q/metrics` (Prometheus format).

### Auto-Collected Metrics
- `http_server_requests_seconds` (count, sum, max, histogram)
- `db_pool_active_connections`, `db_pool_idle_connections`
- `jvm_memory_used_bytes`, `jvm_gc_pause_seconds`
- `rabbitmq_consumed_total`, `rabbitmq_published_total`

### Custom Business Metrics
- `eksad_login_total{status="success|failed"}` — Counter
- `eksad_token_issued_total` — Counter
- `eksad_cache_sync_duration_seconds` — Timer
- `eksad_circuit_breaker_state{service="master-data"}` — Gauge (0=closed, 1=open, 2=half-open)

```java
@Inject MeterRegistry registry;

void onLoginSuccess() {
    registry.counter("eksad_login_total", "status", "success").increment();
}
```

### docker-compose
```yaml
prometheus:
  image: prom/prometheus:latest
  volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml"]
  ports: ["9090:9090"]

grafana:
  image: grafana/grafana:latest
  ports: ["3001:3000"]   # mapped to 3001 to avoid FE conflicts
```

`prometheus.yml` scrape config: one job per EKSAD service (port `/q/metrics`).

---

## 7. Grafana Dashboard Templates (Sprint 3)

### Per-Service Dashboard
- Request rate (req/s)
- Error rate (% 5xx)
- Latency p50 / p95 / p99
- DB connection pool usage
- JVM heap usage
- RabbitMQ queue depth

### Platform Overview Dashboard
- All services health status
- Total request rate across platform
- Cross-service latency heatmap

### Auth Dashboard (`eksad-core-auth`)
- Login success / failure rate
- Token issuance rate
- Active sessions count
- Lockout events

Provisioned as **JSON files** (Infrastructure as Code).

---

## 8. Alerting Rules (Sprint 3)

Prometheus alerting rules:

| Severity | Rule |
|----------|------|
| 🔴 CRITICAL | Error rate > 10% for 5 min |
| 🔴 CRITICAL | Service down (health check failing) for 2 min |
| 🟡 WARNING | Error rate > 5% for 5 min |
| 🟡 WARNING | p95 latency > 500 ms for 10 min |
| 🟡 WARNING | DB pool usage > 80% for 5 min |
| 🟡 WARNING | RabbitMQ queue depth > 1000 for 5 min |
| 🟡 WARNING | Login failure rate > 50% for 5 min (possible brute force) |

**Channels:** Slack webhook (Sprint 3), PagerDuty (production).

---

## 9. Log Aggregation (Sprint 3+, Optional)

| Option | Notes |
|--------|-------|
| **Grafana Loki** | ✅ Lightweight, integrates with Grafana. Recommended. |
| **ELK Stack** | Heavyweight, powerful — choose when full-text search needed. |

### docker-compose (Loki + Promtail)
```yaml
loki:
  image: grafana/loki:latest
  ports: ["3100:3100"]
promtail:
  image: grafana/promtail:latest
  volumes: ["/var/log:/var/log", "./promtail-config.yml:/etc/promtail/config.yml"]
```

Query by: `correlation_id`, `tenant_id`, `service_name`, `level`, time range.

---

## 10. Coding Standards Integration

Add to `EKSAD_CODING_STANDARDS.md` code review checklist:

- [ ] All external REST calls have `@Timeout`
- [ ] Structured logging — no `System.out.println` or string concatenation in logs
- [ ] Correlation ID propagated to downstream calls
- [ ] Sensitive data NOT logged (passwords, tokens, PII)
- [ ] Custom business metrics registered for key operations
- [ ] Health check covers all external dependencies (DB, RabbitMQ, core-auth JWKS)

New sections in `EKSAD_CODING_STANDARDS.md`:
- **Section 23: Logging Standards**
- **Section 24: Observability Standards**

---

## 11. Testing

| Test Type | Scenario |
|-----------|----------|
| Unit | `CorrelationIdFilter` extracts existing header / generates new UUID |
| Unit | MDC populated with `correlation_id`, `tenant_id` |
| Integration | Request across 2 services → same `correlation_id` in both service logs |
| Integration | RabbitMQ event with `correlation_id` header → consumer logs match |
| Metrics | Custom counter `eksad_login_total` increments on success |
| Metrics | `/q/metrics` returns Prometheus format |
| Health | All deps up → `/q/health/ready = UP`; mock DB down → `DOWN` |

See `EKSAD_TESTING_GUIDE.md` Section "Observability Testing".

---

*End of file. Cross-references: `EKSAD_RESILIENCE_PATTERNS.md`, `EKSAD_CICD_CONTAINER_PATTERNS.md`.*
