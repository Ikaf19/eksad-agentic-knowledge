# EKSAD Load Testing Guide

| Meta | Value |
|------|-------|
| **Version** | 1.1 |
| **Date** | 2026-05-24 |
| **Owner** | EKSAD Platform Team |
| **Audience** | QA, DevOps, Tech Leads |
| **Priority** | 🟢 P2 |
| **Related** | `EKSAD_TESTING_GUIDE.md`, `EKSAD_OBSERVABILITY_PATTERNS.md` |

---

## Table of Contents

1. [When to Run Load Tests](#1-when-to-run-load-tests)
2. [Tool Selection](#2-tool-selection-k6-recommended)
3. [Test Types](#3-test-types)
4. [Performance Targets (Per Endpoint)](#4-performance-targets-per-endpoint)
5. [k6 Patterns](#5-k6-patterns)
6. [Test Environment Setup](#6-test-environment-setup)
7. [Authentication in Load Tests](#7-authentication-in-load-tests)
8. [Multi-Tenant Load Tests](#8-multi-tenant-load-tests)
9. [Observability During Load](#9-observability-during-load)
10. [Pass/Fail Criteria](#10-passfail-criteria)
11. [CI Integration](#11-ci-integration)
12. [Sprint Phasing](#12-sprint-phasing)
13. [Reporting Template](#13-reporting-template)

---

## 1. When to Run Load Tests

| Trigger | Type | Frequency |
|---------|------|-----------|
| Pre-production cutover | Full battery | Once per major release |
| New endpoint with anticipated heavy use | Targeted | Before sprint review |
| Suspected regression | Smoke | Per PR (lightweight) |
| Capacity planning | Stress + Soak | Quarterly |
| After infra changes (DB upgrade, K8s tier) | Smoke + Spike | Same day |

> Sprint 1 — load testing is **optional**. Sprint 3+ — required for production-grade endpoints.

---

## 2. Tool Selection: k6 (Recommended)

| Tool | Pros | Cons | Use For |
|------|------|------|---------|
| **k6** ✅ | JS scripting, lightweight, Grafana integration, CI-friendly | Limited UI | EKSAD default |
| Gatling | Scala DSL, detailed HTML reports | Heavier, Scala learning curve | Complex scenarios |
| JMeter | GUI, mature | Heavy resource use, XML config | Legacy / GUI users |
| Locust | Python | Less performant | Quick scripting |

EKSAD standard: **k6** (https://k6.io/).

---

## 3. Test Types

| Type | Goal | Duration | Load Pattern |
|------|------|----------|--------------|
| **Smoke** | Sanity check post-deploy | 1–2 min | 1–5 VUs |
| **Load** | Verify under expected production load | 10–30 min | ramp to target VUs |
| **Stress** | Find breaking point | 20–60 min | ramp beyond expected |
| **Spike** | Sudden traffic burst (Black Friday) | 5–15 min | 0 → max → 0 quickly |
| **Soak** | Memory leaks, connection leaks over time | 4–24 hours | Sustained moderate load |

---

## 4. Performance Targets (Per Endpoint)

Adjust per project — these are EKSAD defaults:

| Endpoint Category | p50 | p95 | p99 | Throughput |
|-------------------|-----|-----|-----|------------|
| Auth (login) | < 100 ms | < 300 ms | < 500 ms | 100 req/s |
| Master data — list (cached) | < 50 ms | < 150 ms | < 300 ms | 500 req/s |
| Master data — CRUD | < 100 ms | < 300 ms | < 500 ms | 50 req/s |
| Domain service — GET | < 100 ms | < 300 ms | < 500 ms | 200 req/s |
| Domain service — POST/PUT | < 200 ms | < 500 ms | < 1000 ms | 100 req/s |
| RabbitMQ consume → cache write | < 100 ms | < 300 ms | < 500 ms | 1000 msg/s |

**Error rate target:** < 0.1% across all endpoints.

---

## 5. k6 Patterns

### 5.1 Basic Smoke Test

```javascript
// smoke.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '1m',
  thresholds: {
    http_req_failed: ['rate<0.01'],          // < 1% error
    http_req_duration: ['p(95)<500'],         // p95 < 500ms
  },
};

const BASE = __ENV.BASE_URL || 'http://localhost:8086';
const TOKEN = __ENV.JWT_TOKEN;

export default function () {
  const res = http.get(`${BASE}/api/v1/brands`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
  });
  check(res, {
    'status is 200': r => r.status === 200,
    'has body':       r => r.body && r.body.length > 0,
  });
  sleep(1);
}
```

Run: `k6 run smoke.js --env BASE_URL=https://staging.eksad.com --env JWT_TOKEN=$JWT`

### 5.2 Ramp-Up Load Test

```javascript
// load.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m',  target: 50  },   // ramp to 50 VUs
    { duration: '5m',  target: 50  },   // hold at 50
    { duration: '2m',  target: 200 },   // ramp to 200
    { duration: '10m', target: 200 },   // hold at 200
    { duration: '3m',  target: 0   },   // ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.005'],
    http_req_duration: ['p(50)<200', 'p(95)<500', 'p(99)<1000'],
  },
};

export default function () {
  // payload + auth
  http.post(`${__ENV.BASE_URL}/api/v1/orders`, JSON.stringify({/* ... */}), {
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${__ENV.JWT_TOKEN}` },
  });
}
```

### 5.3 Spike Test

```javascript
export const options = {
  stages: [
    { duration: '30s', target: 10  },
    { duration: '30s', target: 500 },   // SPIKE
    { duration: '1m',  target: 500 },
    { duration: '30s', target: 10  },   // recover
  ],
};
```

### 5.4 Soak Test (24h)

```javascript
export const options = {
  vus: 50,
  duration: '24h',
  thresholds: {
    http_req_failed: ['rate<0.001'],
    http_req_duration: ['p(95)<500'],
  },
};
```

Watch for: rising memory, connection pool exhaustion, increasing latency over time.

### 5.5 Auth Endpoint Load Test (Login Under Load)

```javascript
// auth-load.js — measures eksad-core-auth login throughput
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 50 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_failed:   ['rate<0.01'],
    http_req_duration: ['p(95)<300'],   // login must be fast
  },
};

const BASE = __ENV.AUTH_URL || 'http://localhost:8090';

export default function () {
  const res = http.post(`${BASE}/api/v1/auth/login`, JSON.stringify({
    username: `loadtest-user-${__VU}@eksad.test`,
    password: 'LoadTest@1234',
  }), { headers: { 'Content-Type': 'application/json' } });

  check(res, {
    'login 200': r => r.status === 200,
    'has access_token': r => JSON.parse(r.body).access_token !== undefined,
  });
  sleep(2);
}
```

### 5.6 RabbitMQ Consumer Throughput Test

Publish a burst of master data events and measure consumer processing latency:

```javascript
// rabbitmq-throughput.js — uses k6 AMQP extension (xk6-amqp)
import amqp from 'k6/x/amqp';
import { check } from 'k6';

export const options = {
  vus: 10,
  iterations: 1000,   // publish 1000 events total
  thresholds: {
    'rabbitmq_publish_duration': ['p(95)<50'],  // publish < 50ms
  },
};

export default function () {
  const conn = amqp.connect(__ENV.AMQP_URL || 'amqp://guest:guest@localhost:5672/');
  amqp.publish(conn, {
    exchange: 'exc-master-data',
    routingKey: 'r.brand.created',
    body: JSON.stringify({
      eventType: 'BRAND.CREATED',
      eventId: `evt-${__ITER}`,
      tenantId: 'load-tenant',
      occurredAt: Date.now(),
      payload: { id: __ITER, name: `Brand-${__ITER}` },
    }),
  });
  amqp.close(conn);
}
```

> Monitor `q-master-sync-pipeline` queue depth in RabbitMQ Management UI — should drain within 30s after burst.

### 5.7 Cache Sync Load Scenario

Verify cache hit rate doesn't degrade under concurrent requests:

```javascript
// cache-sync-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 200,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<150'],   // cache hits should be fast
    http_req_failed:   ['rate<0.001'],
  },
};

const BASE = __ENV.BASE_URL;
const TOKEN = __ENV.JWT_TOKEN;
// Pre-seeded brand IDs in cache
const BRAND_IDS = Array.from({ length: 100 }, (_, i) => i + 1);

export default function () {
  const id = BRAND_IDS[Math.floor(Math.random() * BRAND_IDS.length)];
  const res = http.get(`${BASE}/api/v1/brands/${id}`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
  });
  check(res, {
    'cache hit 200': r => r.status === 200,
    'fast response': r => r.timings.duration < 150,
  });
  sleep(0.1);
}
```

## 6. Test Environment Setup

### 6.1 Dedicated Load Test Environment

- **Never load-test production directly** unless explicitly approved.
- Dedicated `staging-load` environment matching production sizing.
- Separate database (load-test data only).
- Tagged metrics in observability (Grafana `env=load-test`).

### 6.2 Test Data Seeding

```bash
# Pre-load 10,000 tenants + 1M orders before running load test
./scripts/seed-load-data.sh --tenants 10000 --orders-per-tenant 100
```

Keep seeding scripts versioned in `tests/load/seed/`.

---

## 7. Authentication in Load Tests

Pre-generate a pool of JWT tokens (test users):

```javascript
import { SharedArray } from 'k6/data';

const tokens = new SharedArray('tokens', () =>
  JSON.parse(open('./tokens.json'))   // pre-generated, ~1000 tokens
);

export default function () {
  const token = tokens[__VU % tokens.length];
  http.get(url, { headers: { Authorization: `Bearer ${token}` } });
}
```

Generate `tokens.json` via a helper script that calls `eksad-core-auth` issue endpoint for each test user.

---

## 8. Multi-Tenant Load Tests

Mix tenants randomly to simulate real production:

```javascript
const tenants = ['tenant-ahm', 'tenant-tam', 'tenant-acc', /* ... */];

export default function () {
  const tenant = tenants[Math.floor(Math.random() * tenants.length)];
  const token = tokensByTenant[tenant];
  // ... request
}
```

Test isolation under load: tenant A's heavy load should NOT degrade tenant B's response times.

### 8.1 Noisy Neighbor Test

Run two VU groups simultaneously — one "noisy" (high load) and one "quiet":

```javascript
export const options = {
  scenarios: {
    noisy_tenant: {
      executor: 'constant-vus',
      vus: 150,
      duration: '5m',
      env: { TENANT: 'tenant-noisy', TOKEN: __ENV.TOKEN_NOISY },
    },
    quiet_tenant: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m',
      env: { TENANT: 'tenant-quiet', TOKEN: __ENV.TOKEN_QUIET },
    },
  },
  thresholds: {
    // Quiet tenant must NOT be affected by noisy tenant
    'http_req_duration{scenario:quiet_tenant}': ['p(95)<300'],
    'http_req_failed{scenario:quiet_tenant}':   ['rate<0.001'],
  },
};
```

**Pass criterion:** quiet tenant p95 stays within normal threshold despite noisy neighbor.

### 8.2 Shared DB Contention Test

Phase 1 uses a single PostgreSQL instance. Verify no lock contention under concurrent multi-tenant writes:

```javascript
// Concurrent WRITE from 5 different tenants simultaneously
export const options = { vus: 50, duration: '3m' };

const TENANTS = ['tenant-ahm', 'tenant-tam', 'tenant-acc', 'tenant-fif', 'tenant-trac'];

export default function () {
  const tenant = TENANTS[__VU % TENANTS.length];
  const token  = tokensByTenant[tenant];
  http.post(`${BASE}/api/v1/orders`, payload, { headers: { Authorization: `Bearer ${token}` } });
}
```

Watch during test: `pg_locks`, `pg_stat_activity` waiting rows, connection pool exhaustion.

### 8.3 Tenant Provisioning Under Load

Test that creating a new tenant while production load is running does NOT degrade existing tenants:

```javascript
// Phase 1: steady production load on 10 tenants
// Phase 2: trigger tenant provisioning (POST /api/v1/tenants) mid-test
// Watch: API latency for existing tenants during provisioning window
```

## 9. Observability During Load

Watch in Grafana while load test runs:

| Metric | Target |
|--------|--------|
| API p95 latency | Within threshold |
| Error rate | < 0.1% |
| DB connection pool | < 80% utilization |
| RabbitMQ queue depth | < 1000 |
| JVM heap | < 80%, no continuous growth |
| CPU per pod | < 70% |

Correlation: when latency spikes → check DB metrics → check downstream services.

---

## 10. Pass/Fail Criteria

A load test **fails** if ANY of:
- p95 latency exceeds threshold
- Error rate > 0.1%
- Any service health check fails during test
- DB connection pool exhausted (`acquisition-timeout` errors)
- Memory leak detected (heap continuously growing in soak test)

Report findings in `tests/load/reports/{date}/REPORT.md`.

---

## 11. CI Integration

Smoke test on every PR (lightweight):
```yaml
# .gitlab-ci.yml
load-smoke:
  stage: test
  image: grafana/k6:latest
  script:
    - k6 run --env BASE_URL=$STAGING_URL --env JWT_TOKEN=$TEST_JWT tests/load/smoke.js
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Full load test on demand (manual trigger) or nightly.

---

## 12. Sprint Phasing

| Sprint | Load Testing Scope | Tool | Notes |
|--------|--------------------|------|-------|
| **Sprint 1** | Optional — smoke test only on core-auth login + 1 domain endpoint | k6 CLI | Manual trigger, no CI gate |
| **Sprint 2** | Required — smoke + load for all endpoints added in Sprint 1–2 | k6 + GitHub Actions | CI gate on staging |
| **Sprint 3** | Required — full battery (smoke / load / stress / spike) per service | k6 + Grafana dashboard | Nightly scheduled + merge gate |
| **Sprint 4+** | Required — soak test added; regression baselines locked per version | k6 + Grafana k6 Cloud (optional) | Historical comparison enabled |

**Rationale:** Load tests before Sprint 2 are usually premature — services are still changing rapidly. Sprint 3 is the first production-grade cutover window.

---

## 13. Reporting Template

Create `tests/load/reports/{YYYY-MM-DD}/REPORT.md` after each load test run:

```markdown
# Load Test Report — {SERVICE_NAME} @ {VERSION}

| Field | Value |
|-------|-------|
| Date | {YYYY-MM-DD} |
| Tester | {Name} |
| Environment | staging-load |
| k6 Version | {version} |
| Script | `tests/load/{script}.js` |
| Duration | {N} min |
| Peak VUs | {N} |

## Results Summary

| Endpoint | p50 | p95 | p99 | Error Rate | Pass/Fail |
|----------|-----|-----|-----|------------|-----------|
| `POST /api/v1/orders` | {ms} | {ms} | {ms} | {%} | ✅/❌ |
| `GET /api/v1/orders/{id}` | {ms} | {ms} | {ms} | {%} | ✅/❌ |
| `POST /api/v1/auth/login` | {ms} | {ms} | {ms} | {%} | ✅/❌ |

## Infrastructure Metrics (During Test)

| Metric | Min | Max | Avg | Threshold | Pass/Fail |
|--------|-----|-----|-----|-----------|-----------|
| DB connections used | {n} | {n} | {n} | < 80% pool | ✅/❌ |
| JVM heap | {MB} | {MB} | {MB} | < 80% max | ✅/❌ |
| CPU (peak pod) | {%} | {%} | {%} | < 70% | ✅/❌ |
| RabbitMQ queue depth peak | {n} | — | — | < 1000 | ✅/❌ |

## Findings & Recommendations

1. {finding}
2. {finding}

## Attachments

- `k6-summary.json` — raw k6 output
- `grafana-screenshot-{endpoint}.png` — dashboard during test
- `pg_stat_statements-snapshot.sql` — slow queries captured

## Overall Verdict

☐ **PASS** — All thresholds met. Ready for production.  
☐ **FAIL** — See findings above. Retest after fixes.
```

> File naming: `tests/load/reports/2026-05-24/REPORT-svc-pipeline-v1.2.md`

