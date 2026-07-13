# EKSAD Database Deployment Strategy

| Meta | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-05-23 |
| **Owner** | EKSAD Platform Team |
| **Audience** | DevOps, Architects, Senior Developers |
| **Priority** | 🟡 P1 |
| **Related** | Decision 5; `EKSAD_DOMAIN_REGISTRY.md`; `EKSAD_MULTI_TENANCY_PATTERNS.md` |

---

## Table of Contents

1. [Overview — Phased Approach](#1-overview--phased-approach)
2. [Phase 1 — Shared Instance, Separate Databases](#2-phase-1--shared-instance-separate-databases)
3. [Phase 2 — Split Hot Services](#3-phase-2--split-hot-services)
4. [Phase 3 — Full Dedicated Per Service](#4-phase-3--full-dedicated-per-service)
5. [Zero Code Change Principle](#5-zero-code-change-principle)
6. [Database Initialization (Phase 1)](#6-database-initialization-phase-1)
7. [Connection Pooling Guidelines](#7-connection-pooling-guidelines)
8. [Backup & Recovery](#8-backup--recovery)
9. [Migration Triggers](#9-migration-triggers)
10. [Security Standards](#10-security-standards)
11. [Monitoring](#11-monitoring)
12. [API Gateway Deployment (Optional)](#12-api-gateway-deployment-optional)
13. [MongoDB & Other Stores](#13-mongodb--other-stores)

---

## 1. Overview — Phased Approach

EKSAD uses a **phased database deployment** that scales with platform load. **Zero code changes** are required to move between phases — only configuration.

| Phase | Strategy | When |
|-------|----------|------|
| **Phase 1** | 1 PostgreSQL instance, **separate databases** per service | Sprint 1–4 |
| **Phase 2** | Split hot services to **dedicated instances** | Sprint 5+ |
| **Phase 3** | Full dedicated per service, read replicas | Multi-region / compliance |

---

## 2. Phase 1 — Shared Instance, Separate Databases

### Setup
- 1 PostgreSQL instance (`postgres:16-alpine`).
- Separate database per service (e.g., `eksad_core_auth`, `eksad_master`, `eksad_pipeline`, `eksad_orders`).
- Per-service DB credentials (least privilege).
- **Cross-DB JOINs are impossible by design** — isolation enforced at DB level.

### docker-compose Example
```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: ${POSTGRES_ROOT_PASSWORD}
  ports: ["5432:5432"]
  volumes:
    - postgres-data:/var/lib/postgresql/data
    - ./init-databases.sql:/docker-entrypoint-initdb.d/init.sql
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 10s
```

### Resource Sizing (Phase 1)
| Tier | RAM | CPU | Connections |
|------|-----|-----|-------------|
| Dev | 1 GB | 1 | 50 |
| Staging | 4 GB | 2 | 100 |
| Production (Sprint 1) | 16 GB | 4 | 200 |

---

## 3. Phase 2 — Split Hot Services

When a single service's DB activity dominates the shared instance (e.g., `svc-orders` becomes >50% of load):

1. Provision **new** PostgreSQL instance for the hot service.
2. Use `pg_dump` + `pg_restore` to migrate just that service's DB.
3. Update env vars: `DB_HOST`, `DB_PORT` for the hot service.
4. Restart service — picks up new DB. **No code change.**
5. Drop old database on shared instance.

### Typical Hot Services
- `svc-orders` (high write load)
- `svc-master-data` (high read load, fan-out events)
- `eksad-core-auth` (every request validates JWT — but JWKS is cached, so usually OK)

---

## 4. Phase 3 — Full Dedicated Per Service

Each service gets its own PostgreSQL instance. Add:
- Read replicas for hot services
- Multi-AZ for HA
- Possible per-tenant dedicated databases for top-tier tenants (see `EKSAD_MULTI_TENANCY_PATTERNS.md` §10)

---

## 5. Zero Code Change Principle

Services NEVER reference DB host/port directly. Always via env vars:

```properties
quarkus.datasource.reactive.url=postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}
quarkus.datasource.username=${DB_USER}
quarkus.datasource.password=${DB_PASSWORD}
```

**Migrating to dedicated instance = update env vars in K8s manifest. NO code change.**

```yaml
# K8s ConfigMap (Phase 1)
DB_HOST: postgres-shared
DB_PORT: "5432"
DB_NAME: eksad_orders

# K8s ConfigMap (Phase 2)
DB_HOST: postgres-orders-dedicated   # ← only this changes
DB_PORT: "5432"
DB_NAME: eksad_orders
```

---

## 6. Database Initialization (Phase 1)

```sql
-- init-databases.sql (run once on PostgreSQL container init)

-- Core infrastructure
CREATE DATABASE eksad_core_auth;
CREATE USER eksad_core_auth WITH PASSWORD :'EKSAD_CORE_AUTH_DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE eksad_core_auth TO eksad_core_auth;

-- Master data (per domain)
CREATE DATABASE eksad_master;
CREATE USER eksad_master WITH PASSWORD :'EKSAD_MASTER_DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE eksad_master TO eksad_master;

-- Domain services (example: Automotive)
CREATE DATABASE eksad_pipeline;
CREATE USER eksad_pipeline WITH PASSWORD :'EKSAD_PIPELINE_DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE eksad_pipeline TO eksad_pipeline;

CREATE DATABASE eksad_orders;
CREATE USER eksad_orders WITH PASSWORD :'EKSAD_ORDERS_DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE eksad_orders TO eksad_orders;

-- ... per service
```

> Use secrets injection (e.g., Docker secrets, K8s Secrets, Vault) to inject `:'..._PASSWORD'` values — never commit plain text.

---

## 7. Connection Pooling Guidelines

Per service Agroal config (Quarkus):
```properties
quarkus.datasource.reactive.max-size=20
quarkus.datasource.reactive.idle-timeout=PT5M
quarkus.datasource.reactive.acquisition-timeout=PT5S
quarkus.datasource.reactive.leak-detection-interval=PT10S
```

### Per-Service Pool Sizing
| Service | max-size |
|---------|----------|
| Domain services (default) | 20 |
| `svc-master-data` (read-heavy) | 30 |
| `eksad-core-auth` | 10 |

Total connections per instance ≤ **PostgreSQL `max_connections`** (default 100). Adjust if you have many services.

---

## 8. Backup & Recovery

### Phase 1
- Nightly `pg_dump` of all databases.
- WAL archiving for point-in-time recovery (PITR).
- Tested restore procedure documented in `docs/runbooks/db-restore.md`.

### Phase 2+
- Continuous backup to S3 (e.g., `wal-g`, `pgBackRest`).
- Multi-AZ replicas for HA.
- Cross-region replication for DR.

### RPO / RTO Targets

| Environment | RPO | RTO |
|-------------|-----|-----|
| Dev | 24 h | 4 h |
| Staging | 4 h | 1 h |
| Production | 15 min | 30 min |

---

## 9. Migration Triggers

Move from Phase N → Phase N+1 when ONE of these is true:

| Metric | Phase 1→2 Trigger | Phase 2→3 Trigger |
|--------|-------------------|-------------------|
| CPU usage | > 70% sustained (1 hour) | Hot service > 80% sustained |
| Connection saturation | > 80% of max | Per-service pool > 80% |
| p95 query latency | > 100 ms (was < 20 ms) | Per-service > 50 ms |
| Disk IO | > 80% utilization | Hot service IO bottleneck |
| Cross-tenant interference | Detected (noisy neighbor) | — |
| Compliance | — | Per-tenant DB required (regulated tenant) |

---

## 10. Security Standards

Database security is layered: transport (TLS), authentication (per-service roles), authorization (least-privilege GRANTs), credential lifecycle (rotation + storage), and network isolation. **All five layers apply from Phase 1 onward** — security is NOT phased.

### 10.1 TLS in Transit

All client-to-database connections MUST use TLS. PostgreSQL `sslmode=require` minimum; production uses `verify-full`.

```properties
# Quarkus datasource (per-service)
quarkus.datasource.reactive.url=postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=verify-full&sslrootcert=/etc/ssl/certs/eksad-ca.crt
```

| Environment | sslmode | Cert source |
|-------------|---------|-------------|
| Dev | `require` | self-signed (mounted via docker-compose) |
| Staging | `verify-ca` | internal CA |
| Production | `verify-full` | internal CA + hostname match |

PostgreSQL server config:
```conf
# postgresql.conf
ssl = on
ssl_cert_file = '/etc/postgresql/certs/server.crt'
ssl_key_file  = '/etc/postgresql/certs/server.key'
ssl_ca_file   = '/etc/postgresql/certs/eksad-ca.crt'
ssl_min_protocol_version = 'TLSv1.2'
```

### 10.2 Per-Service Role Separation

Each service has its own DB user with `GRANT` scoped to its own database only. **Never use the `postgres` superuser from application code.**

```sql
-- Owner of eksad_orders database (DDL + DML)
CREATE USER eksad_orders WITH PASSWORD :'EKSAD_ORDERS_DB_PASSWORD';
GRANT CONNECT ON DATABASE eksad_orders TO eksad_orders;
GRANT USAGE, CREATE ON SCHEMA public TO eksad_orders;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO eksad_orders;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON TABLES TO eksad_orders;

-- READ-ONLY user for BI / analytics / Grafana datasource
CREATE USER eksad_orders_ro WITH PASSWORD :'EKSAD_ORDERS_RO_PASSWORD';
GRANT CONNECT ON DATABASE eksad_orders TO eksad_orders_ro;
GRANT USAGE ON SCHEMA public TO eksad_orders_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO eksad_orders_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO eksad_orders_ro;
```

| Role pattern | Purpose | Scope |
|--------------|---------|-------|
| `eksad_<service>` | App runtime | DDL + DML on own DB only |
| `eksad_<service>_ro` | BI / analytics / Grafana | SELECT-only on own DB |
| `eksad_migrator` | Flyway migration (CI/CD only) | DDL on all DBs — gated by Vault role |
| `postgres` superuser | Initial bootstrap + emergency | Never used by services |

### 10.3 Password Rotation Policy

| Environment | Rotation cadence | Procedure |
|-------------|------------------|-----------|
| Dev | On-demand | Update `.env`, restart service |
| Staging | Quarterly | Vault auto-rotates, K8s pulls on rollout |
| Production | Monthly OR on incident | Vault auto-rotates + zero-downtime via dual-secret + service rollout |

Zero-downtime rotation pattern (production):
1. Issue NEW password in Vault → `password_v2`.
2. Add `password_v2` to PostgreSQL as additional valid password (PostgreSQL 16+ supports multi-password via SCRAM channel binding).
3. Roll out service with `password_v2` (RollingUpdate).
4. Remove `password_v1` from PostgreSQL.

> Compromise response: rotate immediately, regardless of cadence. Revoke all sessions for the compromised user (`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'eksad_<service>';`).

### 10.4 Network Isolation

| Layer | Rule |
|-------|------|
| ✅ DB reachable from | Service mesh / VPC private subnet only |
| ❌ DB never reachable from | Public internet — period |
| ✅ Allowed CIDR | K8s pod CIDR + bastion host + CI/CD runner CIDR |
| ❌ Forbidden | `0.0.0.0/0` in security group; PostgreSQL `listen_addresses = '*'` without firewall in front |

K8s NetworkPolicy example (deny-by-default + allow service pods):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-allow-services
spec:
  podSelector:
    matchLabels: { app: postgres-shared }
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: { tier: backend }
      ports:
        - protocol: TCP
          port: 5432
```

### 10.5 Credential Storage

| Environment | Storage |
|-------------|---------|
| Dev | `.env` file (gitignored) — local-only, never committed |
| Staging | K8s Secrets (sealed via `sealed-secrets` or `external-secrets-operator`) |
| Production | HashiCorp Vault — dynamic secrets via Vault DB engine (issues short-lived credentials with TTL = 1 hour) |

```yaml
# K8s reference, never inline plaintext
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: orders-db-credentials
        key: password
```

**Forbidden:**
- ❌ Committing plain-text passwords to git (even in `.env.example` with real values)
- ❌ Logging connection strings (mask password in MDC / structured logs — see `EKSAD_OBSERVABILITY_PATTERNS.md` §3 never-log rules)
- ❌ Hardcoding fallback passwords in code or `application.properties`

---

## 11. Monitoring

PostgreSQL observability has 3 layers: **internal stats views** (zero-cost, always-on), **slow-query log** (developer feedback), **Prometheus exporter** (alerting + dashboards). Apply all three from Phase 1.

### 11.1 Internal Stats Views

Enable `pg_stat_statements` extension on every DB (Flyway baseline migration `V0__enable_extensions.sql`):

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

`postgresql.conf` additions:
```conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
pg_stat_statements.max  = 10000
track_activity_query_size = 4096
track_io_timing = on
```

Useful queries (run via `eksad_<service>_ro` user from runbook):
```sql
-- Top 10 slowest queries by total time
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Active long-running sessions
SELECT pid, usename, application_name, state, query_start, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 seconds';
```

### 11.2 Slow-Query Log

```conf
# postgresql.conf
log_min_duration_statement = 500    # log anything > 500ms
log_lock_waits             = on
log_temp_files             = 10240  # log temp files > 10 MB (signals memory pressure)
log_checkpoints            = on
log_connections            = off    # noisy; flip on only during debugging
log_disconnections         = off
log_line_prefix            = '%t [%p] %u@%d app=%a corr=%c '
```

> The `corr=%c` token aligns with `correlationId` MDC — enables grep-correlation between app logs and DB slow logs (T-19).

### 11.3 `postgres_exporter` Deployment

```yaml
# docker-compose snippet
postgres-exporter:
  image: prometheuscommunity/postgres-exporter:v0.15
  environment:
    DATA_SOURCE_NAME: "postgresql://eksad_monitor:${MONITOR_PASSWORD}@postgres:5432/postgres?sslmode=require"
  ports: ["9187:9187"]
  depends_on: [postgres]
```

Create the monitor user (read-only on `pg_stat_*` only):
```sql
CREATE USER eksad_monitor WITH PASSWORD :'MONITOR_PASSWORD';
GRANT pg_monitor TO eksad_monitor;
```

### 11.4 Key Metrics

| Metric | Source | Phase 1 target | Phase 2+ target |
|--------|--------|----------------|------------------|
| `pg_stat_database_numbackends` | exporter | < 80% of `max_connections` | < 70% per-instance |
| `pg_stat_database_xact_commit` rate | exporter | trend baseline | per-service breakdown |
| `pg_locks` waiting count | exporter | < 5 sustained | < 2 sustained |
| `pg_stat_replication_lag_bytes` | exporter | n/a | < 10 MB |
| Cache hit ratio (`blks_hit / (blks_hit + blks_read)`) | derived | > 95% | > 99% |
| Slow-query count (>500ms) | log scrape | < 10/min | < 2/min |
| `pg_stat_statements.mean_exec_time` p95 | exporter | < 50 ms | < 20 ms |

### 11.5 Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Connection saturation | > 70% | > 90% | Investigate pool exhaustion (see `EKSAD_RESILIENCE_PATTERNS.md` §10) |
| p95 query latency | > 50 ms | > 200 ms | Check `pg_stat_statements`; consider Phase 2 split |
| Replication lag | > 10 MB | > 100 MB | Network or write throughput issue |
| Lock waits | > 5 for 5 min | > 20 for 5 min | Deadlock or long transaction |
| Cache hit ratio | < 95% | < 80% | RAM undersized OR scan-heavy queries |
| Disk usage | > 70% | > 85% | Auto-vacuum tuning + archive old data |

### 11.6 Grafana Dashboard

Use the community **PostgreSQL Database Dashboard** (Grafana ID 9628) as baseline; add per-service panels for `pg_stat_statements` top queries. Full dashboard standards in `EKSAD_OBSERVABILITY_PATTERNS.md` §7.

---

## 12. API Gateway Deployment (Optional)

Per Decision 13, the API gateway is **optional and phased**. Sprint 1 services validate JWT themselves (`eksad-core-auth-client` SDK); the gateway is introduced only when its specific benefits (centralized rate-limit, WAF, public-facing aggregation) outweigh the operational cost.

### 12.1 Phased Approach

| Phase | Architecture | Trigger |
|-------|-------------|---------|
| **Phase 1** | No gateway — frontend hits services directly; per-service JWT validation | Sprint 1–N; small surface area |
| **Phase 2** | Gateway-in-front (Kong / Envoy / Spring Cloud Gateway) for public APIs only; internal service-to-service still direct | 3+ public-facing services OR rate-limit / WAF need |
| **Phase 3** | Service mesh (Istio/Linkerd) for east-west + gateway for north-south | Multi-cluster / zero-trust / mTLS mandate |

### 12.2 Decision Matrix — Introduce Gateway When

| Signal | Threshold | Action |
|--------|-----------|--------|
| Public-facing services | ≥ 3 | Add gateway for unified TLS termination + path routing |
| Rate-limit requirement | Per-tenant or per-IP needed | Add gateway (Kong rate-limit plugin) |
| WAF / DDoS protection | Compliance / customer SLA | Add gateway in front of public surface |
| CORS / API key fan-out | Multiple FE apps + partners | Add gateway for centralized auth |
| Aggregation / BFF | FE needs response from 3+ services per page | Add BFF layer (separate concern from gateway) |

If **none** of the above apply: stay Phase 1. Gateway is operational overhead.

### 12.3 Kong docker-compose Snippet (Phase 2)

```yaml
kong:
  image: kong:3.6-alpine
  environment:
    KONG_DATABASE: "off"
    KONG_DECLARATIVE_CONFIG: /etc/kong/kong.yaml
    KONG_PROXY_LISTEN: "0.0.0.0:8000 ssl"
    KONG_ADMIN_LISTEN: "127.0.0.1:8001"
    KONG_SSL_CERT: /etc/kong/certs/server.crt
    KONG_SSL_CERT_KEY: /etc/kong/certs/server.key
  ports: ["8000:8000"]
  volumes:
    - ./kong.yaml:/etc/kong/kong.yaml:ro
    - ./certs:/etc/kong/certs:ro
  depends_on: [eksad-core-auth, svc-orders]
```

```yaml
# kong.yaml — declarative routes
_format_version: "3.0"
services:
  - name: svc-orders
    url: http://svc-orders:8085
    routes:
      - name: orders-public
        paths: [/api/v1/orders]
        strip_path: false
    plugins:
      - name: rate-limiting
        config: { minute: 100, policy: local }
      - name: jwt
        config: { key_claim_name: kid, claims_to_verify: [exp] }
```

### 12.4 K8s Ingress + Gateway Manifest (Phase 2)

```yaml
# Gateway (Kong via Ingress Controller)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: eksad-public
  annotations:
    konghq.com/strip-path: "false"
    konghq.com/plugins: rate-limit-per-tenant,jwt-validate
spec:
  ingressClassName: kong
  tls:
    - hosts: [api.eksad.example.com]
      secretName: eksad-public-tls
  rules:
    - host: api.eksad.example.com
      http:
        paths:
          - path: /api/v1/orders
            pathType: Prefix
            backend: { service: { name: svc-orders, port: { number: 8085 } } }
          - path: /api/v1/master
            pathType: Prefix
            backend: { service: { name: svc-master-data, port: { number: 8086 } } }
```

### 12.5 Frontend Wiring per Phase

| Phase | FE base URL pattern | Env var |
|-------|---------------------|---------|
| Phase 1 (no gateway) | `https://orders.eksad.example.com` per service | `VITE_API_BASE_ORDERS=https://orders...` (multiple) |
| Phase 2 (gateway) | `https://api.eksad.example.com/api/v1/orders` unified | `VITE_API_BASE=https://api.eksad.example.com` (single) |

> Switching phases on the FE is a **build-time env-var change** — no code change in the FE app. Same Zero-Code-Change principle as §5 for backend.

### 12.6 What the Gateway MUST NOT Do

Per Architecture Principle #1 — **no business logic in the gateway**. Allowed: TLS termination, rate-limit, WAF, JWT signature check, path routing, CORS, request/response logging. Forbidden: data transformation, DB lookups, authorization beyond JWT signature, cross-service aggregation (that belongs in a BFF, not gateway).

---

## 13. MongoDB & Other Stores

The phased strategy applies the **same** to MongoDB:

| Phase | MongoDB Strategy |
|-------|------------------|
| Phase 1 | 1 MongoDB instance, separate databases: `eksad_audit`, `eksad_users`, `eksad_tenants` |
| Phase 2 | Dedicated MongoDB for `eksad-core-audittrail` (write-heavy) |
| Phase 3 | Sharded MongoDB, replica sets per service |

### Used By
- `eksad-core-audittrail` — `eksad_audit.log_activity`
- `svc-user-management` — `eksad_users` (users, roles, role_assignments)
- `svc-tenant-management` — `eksad_tenants` (tenants, tenant_config_history)

Connection env vars:
```properties
quarkus.mongodb.connection-string=mongodb://${MONGO_HOST}:${MONGO_PORT}
quarkus.mongodb.database=${MONGO_DB}
```

### Other Stores (Future)
- **Redis** — added when caching needs scaling beyond local memory (Sprint 4+).
- **Elasticsearch** — added when full-text search needed (Sprint 5+).

---

*End of file.*
