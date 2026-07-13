# Technical Specification Document (TSD)
# {PROJECT_NAME} — Version {VERSION}

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — Technical Specification Document |
| **Document Type** | Technical Specification Document (TSD) — Backend |
| **Project Name** | {PROJECT_NAME} |
| **Module / Domain** | {MODULE_OR_DOMAIN} |
| **Version** | {VERSION} |
| **Status** | 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)* |
| **System** | `{ARTIFACT_ID}` (`{SERVICE_NAME}`) |
| **Organization** | PT EKSAD / {BUSINESS_UNIT} |
| **Classification** | Internal — Confidential |
| **Related BRD** | `BRD_{PROJECT_CODE}_v{VERSION}.md` |
| **Related FSD** | `FSD_{PROJECT_CODE}_v{VERSION}.md` |
| **Supersedes** | `TSD_{PROJECT_CODE}_v{PREV_VERSION}.md` *(if applicable)* |
| **Prepared By** | {PREPARED_BY} |
| **Reviewed By** | {REVIEWED_BY} |
| **Approved By** | {APPROVED_BY} |
| **Last Updated** | {DATE} |

> **Audience:** System Analysts, Tech Leads, Backend Developers.
> This document describes **HOW** the system is built — architecture, data models, class design, API skeletons, event contracts, and deployment.
> For **WHAT** the system does (user flows, business rules, acceptance criteria), see `FSD_{PROJECT_CODE}_v{VERSION}.md`.

> **Related Documents:**
> - `BRD_{PROJECT_CODE}_v{VERSION}.md` — Business requirements
> - `FSD_{PROJECT_CODE}_v{VERSION}.md` — Functional specification (source of all FR IDs referenced here)
> - `TSD_FE_{PROJECT_CODE}_v{VERSION}.md` — Frontend technical specification

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |

---

## Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Business Owner | | | |
| Project Manager | | | |
| Lead SA / System Analyst | | | |
| Tech Lead | | | |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Traceability Matrix](#2-traceability-matrix)
3. [Architecture Overview](#3-architecture-overview)
4. [Parent POM & Dependencies](#4-parent-pom--dependencies)
5. [Project Structure](#5-project-structure)
6. [Docker Compose — Local Development](#6-docker-compose--local-development)
7. [JWT Configuration — RS256](#7-jwt-configuration--rs256)
8. [application.properties — Per Service Template](#8-applicationproperties--per-service-template)
9. [Flyway DDL Conventions](#9-flyway-ddl-conventions)
10. [RabbitMQ Event Schemas](#10-rabbitmq-event-schemas)
11. [MongoDB Audit Schema](#11-mongodb-audit-schema)
12. [API Code Skeleton](#12-api-code-skeleton)
13. [BaseRepository Implementation Guide](#13-baserepository-implementation-guide)
14. [Testing Strategy](#14-testing-strategy)
15. [Nexus & Deployment Configuration](#15-nexus--deployment-configuration)
16. [File Storage Integration](#16-file-storage-integration)
17. [Global Technical Rules](#17-global-technical-rules)
18. [Gap Analysis](#18-gap-analysis)
19. [Open Issues & Decisions Log](#19-open-issues--decisions-log)
20. [Glossary](#20-glossary)
21. [Appendix — Change Log](#appendix--change-log)

---

## 1. Introduction

### 1.1 Purpose

> *Describe the purpose of this document. Explain that the TSD translates the functional requirements defined in the FSD into concrete technical implementation decisions: class design, data schema, event contracts, deployment config. State which FSD version this document is derived from.*

### 1.2 Scope

> *Define the technical boundary of this document — which services, modules, and infrastructure components are covered and which are explicitly out of scope.*

### 1.3 Intended Audience

| Audience | Purpose |
|---|---|
| System Analyst / SA | Authoring and maintaining technical design decisions |
| Tech Lead | Reviewing architecture, patterns, and code standards |
| Backend Developer | Implementing classes, repositories, APIs described here |
| DevOps / Infra | Provisioning infrastructure, deployment configuration |

---

## 2. Traceability Matrix

> *Every tech component in this document must trace back to a named FR from the FSD. If a component cannot be traced to an FR, it must be escalated — either added to the FSD first, or flagged in Gap Analysis (§18).*
>
> **Columns:** `FR ID` — from FSD; `Feature ID` — parent feature; `Class` — Java class name; `Method / Function` — primary method implementing the behaviour.
>
> **Maintenance note:** Method signatures are indicative — mark outdated rows with `[STALE]` and update at each sprint review. Do not delete stale rows until resolved.

| FR ID | Feature ID | Description | Class | Method / Function |
|---|---|---|---|---|
| FR-{MODULE}-001 | F-001 | {FR description} | `{Entity}Service` | `create({Entity}DTO dto)` |
| FR-{MODULE}-002 | F-001 | {FR description} | `{Entity}Repository` | `updateEntity({Entity}DTO dto)` |
| FR-{MODULE}-003 | F-001 | {FR description} | `{Entity}Repository` | `deleteEntity({Entity}DTO dto)` |
| FR-{MODULE}-004 | F-001 | {FR description} | `{Entity}Resource` | `findById(@PathParam Long id)` |
| FR-AUTH-001 | F-003 | JWT validation per request | `{Entity}Resource` | All endpoints via `@RolesAllowed` |
| FR-AUDIT-001 | F-004 | Audit log on every CRUD | `{Entity}Repository` | `createFlow` / `updateFlow` / `deleteFlow` (via `BaseRepository`) |
| FR-{MODULE}-{N} | F-{N} | {FR description} | `{Class}` | `{method}({params})` |

---

## 3. Architecture Overview

```
                      ┌─────────────────────────────────┐
                      │      eksad-gateway :8080          │
                      │  JWT filter · rate limit · CORS   │
                      │  Vert.x HTTP reverse proxy        │
                      └──────────────────┬───────────────┘
                                         │ routes to
         ┌───────────────┬───────────────┼───────────────┬──────────────┐
         │               │               │               │              │
  :{PORT} │        :{PORT}│        :{PORT}│        :{PORT}│       :{PORT}│
eksad-auth│  {SERVICE_2}  │  {SERVICE_3}  │  {SERVICE_4}  │  {SERVICE_5} │
         │               │               │               │              │
         └───────────────┴───────────────┴───────────────┴──────────────┘
                                         │
                               RabbitMQ  │  (exchanges + queues)
                  ┌────────────────────┬─┴──────────────────┐
                  │                    │                     │
           :8089  │             :8090  │              :{PORT}│
  eksad-core-audittrail   eksad-core-storage        {OTHER_CONSUMER}
      (MongoDB)           (PostgreSQL + S3/R2)
                              │
                   exc-file-processing
                   (async thumbnail generation)
```

### 3.1 Stack Profile Decision

> **SA Action Required:** Lock the service's technology profile across the three independent axes and explain the
> rationale. Defaults apply when unspecified. See `EKSAD_BASE_PRINCIPLES.md → Stack Profiles`.
> Tier-1 (battle-tested): *Quarkus·Reactive·RabbitMQ* or *Spring Boot·Imperative·RabbitMQ*. Any other combination
> is Tier-2 (allowed) — justify it.

| Axis | Chosen | Options | Tier | Rationale |
|------|--------|---------|------|-----------|
| **Framework** | {Quarkus / Spring Boot} | Quarkus 3.30.6 · Spring Boot 3.x | — | {why} |
| **Paradigm** | {Reactive / Imperative} | Reactive · Imperative | — | {why} |
| **Broker** | {RabbitMQ / Kafka} | RabbitMQ · Kafka | — | {why} |

**Declared profile:** *(fill in)* **{Framework} · {Paradigm} · {Broker}** — Tier **{1/2}**.
*(Default when unspecified: Quarkus · Reactive · RabbitMQ.)*

**Business driver (from FSD/NFR):** *(fill in — e.g. reference `NFR-ASYNC-001` "eventual consistency acceptable",
high event throughput, or team Kafka-familiarity.)*

> **Audit-trail note (broker-independent):** Regardless of the broker chosen above, the audit **producer** in
> `eksad-core-common` always publishes to **RabbitMQ** (`exc-log-activity`). If this service is Kafka-native and
> does not run RabbitMQ, it may instead emit the identical audit envelope to the Kafka topic `log-activity`
> (`eksad-core-audittrail` is dual-ingress, `AUDIT_KAFKA_ENABLED=true`). See `EKSAD_EVENT_CATALOG.md §6`.

> **Skeleton impact:** Apply the profile's mappings to all code skeletons in §12–§13 (return types, transaction &
> auth annotations, repository base) and to the broker config in §10. The event **envelope is identical** across
> brokers — only transport config differs.

### 3.2 Design Principles

1. **No business logic in gateway** — only JWT validation, rate limiting, routing
2. **Each service owns its schema** — no cross-service DB JOINs; use events for data sync
3. **Events over synchronous calls** — async event broker (RabbitMQ or Kafka, per §3.1 profile) for audit, notifications; sync HTTP only for user-facing reads. The event envelope is identical across brokers.
4. **`tenant_id` everywhere** — every DB row, every JWT claim, every RabbitMQ message payload
5. **Flyway only** — zero `ddl-auto=update`; all DDL changes versioned in `V{N}__{description}.sql`
6. **Auto audit trail** — every CRUD operation uses `BaseRepository` flows; no manual RabbitMQ wiring
7. **Long epoch for timestamps** — all DB timestamps as `BIGINT` (epoch milliseconds); Java type is `Long`
8. **Soft delete** — never hard-delete; use `deleted_at BIGINT` + `deleted_by VARCHAR` from `BaseEntity`
9. **File reference by ID only** — domain services store only `file_id BIGINT`; never raw S3 keys or CDN URLs. Resolve URLs at render-time via `GET /api/v1/storage/{fileId}/url`

### 3.3 Service Registry

| Service | Artifact ID | Port | DB | Purpose |
|---------|-------------|------|----|---------|
| eksad-auth | `eksad-svc-auth` | 8081 | PostgreSQL | JWT issuance, user management |
| {SERVICE_2} | `{ARTIFACT_2}` | {PORT} | PostgreSQL | {PURPOSE} |
| {SERVICE_3} | `{ARTIFACT_3}` | {PORT} | PostgreSQL | {PURPOSE} |
| eksad-core-audittrail | `eksad-core-audittrail` | 8089 | MongoDB | Audit log storage |
| eksad-core-storage | `eksad-core-storage` | 8090 | PostgreSQL (`eksad_storage`) + AWS S3 or Cloudflare R2 | File upload, metadata, CDN URL resolution, thumbnail generation |

### 3.4 Gateway Infrastructure Decision

> **SA Action Required:** Select the gateway mode for each environment and fill in the config blocks below.
> See `EKSAD_DB_DEPLOYMENT_STRATEGY.md §12` for gateway deployment patterns and Kong configuration.
> Rule: gateway must validate JWT and route only — **no business logic in gateway** (Principle #1).

#### Gateway Mode per Environment

| Environment | Mode | Gateway URL | Notes |
|-------------|------|-------------|-------|
| Development | ☐ No Gateway (direct service URLs) / ☐ Gateway (`localhost:8080`) | `http://localhost:{PORT}` per service | Recommended: No Gateway in dev for faster iteration |
| Staging | ☐ No Gateway / ☐ Gateway (`{STAGING_GATEWAY_HOST}`) | `https://{STAGING_GATEWAY_HOST}` | |
| Production | ☐ No Gateway / ☐ Gateway (`{PROD_GATEWAY_HOST}`) | `https://{PROD_GATEWAY_HOST}` | |

**SA Decision:** *(fill in)* We will use **{NO GATEWAY / GATEWAY}** from **{environment}** onward because **{reason}**.

> **Threshold signal (from §12 Deployment Strategy):** Introduce gateway when ≥ 3 domain services are live **AND** cross-cutting concerns (rate limiting, CORS, auth header normalisation) require centralised enforcement.

#### Per-Service JWT Configuration (when running WITHOUT gateway)

> Each service validates JWT independently. Copy the block below into each service's `application.properties`.

```properties
# JWT — RS256 public key (same key across all services)
mp.jwt.verify.publickey.location=classpath:public.pem
mp.jwt.verify.issuer=${JWT_ISSUER}
quarkus.http.auth.permission.authenticated.paths=/api/*
quarkus.http.auth.permission.authenticated.policy=authenticated
```

> When **WITH gateway**: gateway validates JWT and forwards `X-Auth-Claims` header to services. Remove the `mp.jwt.*` block from services and configure trust on the internal network only.

#### Gateway Routing Table (fill in when gateway is active)

| Route | Backend Service | Backend Port | Strip Prefix | Rate Limit |
|-------|----------------|-------------|-------------|------------|
| `/api/v1/auth/*` | `eksad-svc-auth` | 8081 | No | 20 req/min |
| `/api/v1/{module-1}/*` | `{SERVICE_2}` | {PORT} | No | {RATE} |
| `/api/v1/{module-2}/*` | `{SERVICE_3}` | {PORT} | No | {RATE} |
| `/api/v1/storage/*` | `eksad-core-storage` | 8090 | No | 50 req/min |

#### Frontend Configuration per Mode

> **Without gateway** — `frontend/.env.{environment}`:
```dotenv
VITE_AUTH_API_URL=http://localhost:8081
VITE_{MODULE_1}_API_URL=http://localhost:{PORT}
VITE_{MODULE_2}_API_URL=http://localhost:{PORT}
VITE_STORAGE_API_URL=http://localhost:8090
```

> **With gateway** — single base URL, all services behind gateway:
```dotenv
VITE_API_BASE_URL=https://{GATEWAY_HOST}
# All service paths become: VITE_API_BASE_URL + /api/v1/{module}/*
```

> Switching from No-Gateway to Gateway is a **build-time env-var change only** — zero backend code change required (per Principle §12.5 Zero-Code-Change).

#### Gateway Infrastructure Checklist

- [ ] SA confirmed gateway mode per environment (table above filled)
- [ ] Per-service JWT config added to `application.properties` for each service (no-gateway mode)
- [ ] Frontend `.env.*` files updated with correct base URLs per mode
- [ ] Gateway routing table completed for all services (gateway mode)
- [ ] Gateway must-not-do verified: no business logic, no DB access, no response transformation beyond header
- [ ] TRULE-014 Gateway Infrastructure Declaration added to §17 Global Technical Rules

---

## 4. Parent POM & Dependencies

### 4.1 `eksad-parent` POM

**File:** `eksad-parent/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.eksad</groupId>
  <artifactId>eksad-parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>
  <name>EKSAD Platform — Parent BOM</name>

  <properties>
    <java.version>21</java.version>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

    <!-- Platform versions — DO NOT change per-service -->
    <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
    <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
    <quarkus.platform.version>3.30.6</quarkus.platform.version>

    <lombok.version>1.18.32</lombok.version>
    <mapstruct.version>1.5.5.Final</mapstruct.version>
    <lombok-mapstruct-binding.version>0.2.0</lombok-mapstruct-binding.version>
    <micrometer.version>1.12.5</micrometer.version>

    <!-- Plugin versions -->
    <compiler-plugin.version>3.14.1</compiler-plugin.version>
    <surefire-plugin.version>3.5.4</surefire-plugin.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>${quarkus.platform.group-id}</groupId>
        <artifactId>${quarkus.platform.artifact-id}</artifactId>
        <version>${quarkus.platform.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <distributionManagement>
    <snapshotRepository>
      <id>eksad-nexus-snapshots</id>
      <url>${NEXUS_URL}/repository/maven-snapshots/</url>
    </snapshotRepository>
    <repository>
      <id>eksad-nexus-releases</id>
      <url>${NEXUS_URL}/repository/maven-releases/</url>
    </repository>
  </distributionManagement>
</project>
```

### 4.2 Per-Service `pom.xml` Template

**File:** `{service-name}/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.eksad</groupId>
    <artifactId>eksad-parent</artifactId>
    <version>1.0.0</version>
  </parent>

  <groupId>com.eksad.svc</groupId>
  <artifactId>{SERVICE_ARTIFACT_ID}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <dependencies>
    <!-- EKSAD Common Library — provides BaseRepository, CrudFlows, LogHandler, auto audit -->
    <dependency>
      <groupId>com.eksad.core</groupId>
      <artifactId>eksad-core-common</artifactId>
      <version>1.0.0-SNAPSHOT</version>
    </dependency>

    <!-- Quarkus Reactive Stack -->
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-hibernate-reactive-panache</artifactId>
    </dependency>
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-reactive-pg-client</artifactId>
    </dependency>
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-rest-jsonb</artifactId>
    </dependency>

    <!-- JWT -->
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-smallrye-jwt</artifactId>
    </dependency>

    <!-- OpenAPI + Swagger -->
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-smallrye-openapi</artifactId>
    </dependency>
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-swagger-ui</artifactId>
    </dependency>

    <!-- Lombok + MapStruct -->
    <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>${lombok.version}</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.mapstruct</groupId>
      <artifactId>mapstruct</artifactId>
      <version>${mapstruct.version}</version>
    </dependency>
    <dependency>
      <groupId>org.mapstruct</groupId>
      <artifactId>mapstruct-processor</artifactId>
      <version>${mapstruct.version}</version>
      <scope>provided</scope>
    </dependency>

    <!-- Testing -->
    <dependency>
      <groupId>io.quarkus</groupId>
      <artifactId>quarkus-junit5</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>rest-assured</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>${quarkus.platform.group-id}</groupId>
        <artifactId>quarkus-maven-plugin</artifactId>
        <version>${quarkus.platform.version}</version>
        <extensions>true</extensions>
        <executions>
          <execution>
            <goals>
              <goal>build</goal>
              <goal>generate-code</goal>
              <goal>generate-code-tests</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>${compiler-plugin.version}</version>
        <configuration>
          <parameters>true</parameters>
          <annotationProcessorPaths>
            <path>
              <groupId>org.mapstruct</groupId>
              <artifactId>mapstruct-processor</artifactId>
              <version>${mapstruct.version}</version>
            </path>
            <path>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok</artifactId>
              <version>${lombok.version}</version>
            </path>
            <path>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok-mapstruct-binding</artifactId>
              <version>${lombok-mapstruct-binding.version}</version>
            </path>
          </annotationProcessorPaths>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

---

## 5. Project Structure

```
{service-name}/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/eksad/svc/{domain}/
│   │   │   ├── common/
│   │   │   │   └── constants/
│   │   │   │       └── {Domain}ModuleType.java    ← module type string constants
│   │   │   ├── core/
│   │   │   │   ├── dto/
│   │   │   │   │   ├── {Entity}CreateDTO.java
│   │   │   │   │   ├── {Entity}UpdateDTO.java
│   │   │   │   │   └── {Entity}ResponseDTO.java
│   │   │   │   ├── mapper/
│   │   │   │   │   └── {Entity}Mapper.java        ← MapStruct
│   │   │   │   └── service/
│   │   │   │       └── {Entity}Service.java
│   │   │   ├── data/
│   │   │   │   ├── entities/
│   │   │   │   │   └── {Entity}Entity.java         ← extends BaseEntity
│   │   │   │   └── repositories/
│   │   │   │       └── {Entity}Repository.java     ← extends BaseRepository
│   │   │   └── transport/
│   │   │       └── resource/
│   │   │           └── {Entity}Resource.java       ← JAX-RS REST endpoint
│   │   └── resources/
│   │       ├── application.properties
│   │       └── db/migration/
│   │           └── V1__{description}.sql           ← Flyway DDL
│   └── test/
│       └── java/com/eksad/svc/{domain}/
│           ├── {Entity}ServiceTest.java
│           └── {Entity}ResourceTest.java
```

---

## 6. Docker Compose — Local Development

**File:** `docker-compose.yml` (at project root or in `devops/`)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    container_name: eksad-postgres
    environment:
      POSTGRES_USER: eksad
      POSTGRES_PASSWORD: eksad_dev_password
      POSTGRES_DB: eksad_{domain}
    ports:
      - "5432:5432"
    volumes:
      - eksad_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U eksad"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:6.0
    container_name: eksad-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: eksad
      MONGO_INITDB_ROOT_PASSWORD: eksad_dev_password
      MONGO_INITDB_DATABASE: eksad_audit
    ports:
      - "27017:27017"
    volumes:
      - eksad_mongodata:/data/db

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: eksad-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: eksad
      RABBITMQ_DEFAULT_PASS: eksad_dev_password
      RABBITMQ_DEFAULT_VHOST: eksad_vhost
    ports:
      - "5672:5672"
      - "15672:15672"    # Management UI
    volumes:
      - eksad_rabbitmqdata:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  eksad_pgdata:
  eksad_mongodata:
  eksad_rabbitmqdata:
```

---

## 7. JWT Configuration — RS256

### 7.1 Key Generation (Run Once)

```bash
# Generate 4096-bit RSA key pair — store private key in secure vault (never commit to Git)
openssl genrsa -out eksad-private-key.pem 4096
openssl rsa -in eksad-private-key.pem -pubout -out eksad-public-key.pem

# Convert to PKCS8 — required by SmallRye JWT
openssl pkcs8 -topk8 -nocrypt -inform pem -in eksad-private-key.pem \
  -outform pem -out eksad-private-key-pkcs8.pem
```

### 7.2 JWT Payload Structure

```json
{
  "iss": "eksad-auth-service",
  "sub": "{user_email_or_username}",
  "jti": "{uuid-v4}",
  "iat": 1745280000000,
  "exp": 1745366400000,
  "groups": ["ROLE_{ROLE_CODE}"],
  "eksad_tenant_id": "{tenant_id}",
  "eksad_user_id": "{user_id}",
  "eksad_role": "{role_code}",
  "eksad_permissions": [
    "{MODULE}_READ",
    "{MODULE}_WRITE",
    "{MODULE}_APPROVE"
  ]
}
```

### 7.3 Auth Service Config

```properties
# application.properties — eksad-auth-service ONLY
mp.jwt.verify.issuer=eksad-auth-service
smallrye.jwt.sign.key.location=META-INF/resources/eksad-private-key-pkcs8.pem
smallrye.jwt.new-token.issuer=eksad-auth-service
smallrye.jwt.new-token.lifespan=86400
smallrye.jwt.new-token.audience=eksad-services
```

### 7.4 All Other Services — JWT Validator Config

```properties
# application.properties — every service EXCEPT eksad-auth-service
mp.jwt.verify.issuer=eksad-auth-service
mp.jwt.verify.publickey.location=META-INF/resources/eksad-public-key.pem
quarkus.smallrye-jwt.enabled=true
```

---

## 8. application.properties — Per Service Template

```properties
# ─── Server ────────────────────────────────────────────────────────────────
quarkus.http.port=${PORT:8080}
quarkus.http.cors=true
quarkus.http.cors.origins=*
quarkus.http.cors.headers=*
quarkus.http.cors.methods=POST, GET, PUT, PATCH, DELETE, OPTIONS

# ─── PostgreSQL (Reactive) ──────────────────────────────────────────────────
quarkus.datasource.db-kind=postgresql
quarkus.datasource.username=${DB_USERNAME}
quarkus.datasource.password=${DB_PASSWORD}
quarkus.datasource.reactive.url=${DB_REACTIVE_URL}

# ─── Hibernate Reactive ─────────────────────────────────────────────────────
# NEVER use 'update' in production — Flyway manages schema
quarkus.hibernate-orm.database.generation=none
quarkus.hibernate-orm.log.sql=${LOG_SQL:false}

# ─── Flyway ──────────────────────────────────────────────────────────────────
quarkus.flyway.migrate-at-start=true
quarkus.flyway.locations=db/migration
quarkus.flyway.baseline-on-migrate=true

# ─── JWT Validation ──────────────────────────────────────────────────────────
mp.jwt.verify.issuer=eksad-auth-service
mp.jwt.verify.publickey.location=META-INF/resources/eksad-public-key.pem
quarkus.smallrye-jwt.enabled=true

# ─── OpenAPI / Swagger UI ───────────────────────────────────────────────────
mp.openapi.scan.disable=false
quarkus.smallrye-openapi.info-title={SERVICE_NAME} API
quarkus.smallrye-openapi.info-version={VERSION}
quarkus.smallrye-openapi.info-description={SERVICE_DESCRIPTION}

# ─── Logging ──────────────────────────────────────────────────────────────────
quarkus.log.console.format=%d{yyyy-MM-dd HH:mm:ss} %-5p [%c{1.}] (%t) %s%e%n
quarkus.log.category."com.eksad".level=DEBUG

# ─── RabbitMQ ─────────────────────────────────────────────────────────────────
# Connection (required — set via environment variables)
rabbitmq-host=${RABBITMQ_HOST}
rabbitmq-port=${RABBITMQ_PORT:5672}
rabbitmq-username=${RABBITMQ_USERNAME}
rabbitmq-password=${RABBITMQ_PASSWORD}
mp.messaging.connector.smallrye-rabbitmq.virtual-host=${RABBITMQ_VHOST:eksad_vhost}

# Connection tuning
mp.messaging.connector.smallrye-rabbitmq.publisher-confirm=true
mp.messaging.connector.smallrye-rabbitmq.publisher-returns=true

# ─── Audit Trail Outgoing Channel (auto-configured by eksad-core-common) ─────
# These defaults come from META-INF/microprofile-config.properties in eksad-core-common.
# Override here ONLY if you need a non-default exchange/routing-key.
# mp.messaging.outgoing.out-log-activity.exchange.name=exc-log-activity
# mp.messaging.outgoing.out-log-activity.default-routing-key=r.q-log-activity-eksad

# ─── File Storage (eksad-core-storage) ────────────────────────────────────────
# ⚠️  Include this block ONLY if this service integrates with file uploads.
# ⚠️  Do NOT add to services that have no file upload functionality.
# Domain services do NOT talk to S3/R2 directly — they only call eksad-core-storage REST API.
# The storage URL below is the internal service address (not gateway-routed).
#
eksad.storage.base-url=${STORAGE_SERVICE_URL:http://eksad-core-storage:8090}
#
# The following STORAGE_* env vars are required on the eksad-core-storage service itself,
# NOT on domain services. They are listed here for reference / infrastructure provisioning:
#
# STORAGE_PROVIDER                  = aws | cloudflare          (default: aws)
# STORAGE_S3_BUCKET_PUBLIC          = <bucket name>
# STORAGE_S3_BUCKET_PRIVATE         = <bucket name>
# STORAGE_S3_REGION                 = ap-southeast-1            (AWS only)
# STORAGE_S3_ENDPOINT               = https://{account}.r2.cloudflarestorage.com  (Cloudflare R2 only)
# STORAGE_S3_ACCESS_KEY             = <access key>
# STORAGE_S3_SECRET_KEY             = <secret key>
# STORAGE_CDN_BASE_URL_PUBLIC       = https://cdn.eksad.com     (base URL for PUBLIC files)
# STORAGE_CDN_PRIVATE_KEY_ID        = <CloudFront key pair ID>  (AWS signed URL only)
# STORAGE_CDN_PRIVATE_KEY_PATH      = /path/to/cloudfront-private-key.pem  (AWS signed URL only)
# STORAGE_SIGNED_URL_TTL_SECONDS    = 300                       (PRIVATE file URL lifetime)
# STORAGE_MAX_FILE_SIZE_MB          = 20
# STORAGE_ALLOWED_MIME_TYPES        = image/png,image/jpeg,image/gif,image/webp,application/pdf
```

---

## 9. Flyway DDL Conventions

### 9.1 Naming Convention

```
V{version}__{description}.sql

Examples:
  V1__init_schema.sql
  V2__add_status_column_to_transactions.sql
  V3__create_index_tenant_id.sql
```

Rules:
- Version is an integer, incrementing from 1
- Double underscore `__` separates version from description
- Description in `snake_case`, lowercase
- Never edit a committed migration file — always create a new version

### 9.2 Standard Table Template

```sql
-- V1__init_{domain}.sql
-- Service: {SERVICE_NAME}
-- Author:  {AUTHOR}
-- Date:    {DATE}
-- FR Refs: FR-{MODULE}-001, FR-{MODULE}-002   ← list all FRs this table supports

CREATE TABLE IF NOT EXISTS {table_name} (
    -- Primary Key
    id            BIGSERIAL       PRIMARY KEY,

    -- Tenant isolation (REQUIRED on every table — TRULE-009)
    tenant_id     VARCHAR(100)    NOT NULL,

    -- Domain columns
    {COLUMN_1}    {TYPE_1}        {CONSTRAINTS_1},
    {COLUMN_2}    {TYPE_2}        {CONSTRAINTS_2},

    -- Reserved fields (transactional entities only — TRULE-012)
    -- Include ONLY when entity extends BaseTransactionalEntity (opt-in)
    -- See EKSAD_RESERVED_FIELD_PATTERNS.md. Master data, _cache, audit tables are EXEMPT.
    reserved_str_1    TEXT          NULL,
    reserved_str_2    TEXT          NULL,
    reserved_str_3    TEXT          NULL,
    reserved_str_4    TEXT          NULL,
    reserved_str_5    TEXT          NULL,
    reserved_num_1    NUMERIC(20,4) NULL,
    reserved_num_2    NUMERIC(20,4) NULL,
    reserved_num_3    NUMERIC(20,4) NULL,
    reserved_date_1   BIGINT        NULL,
    reserved_date_2   BIGINT        NULL,
    reserved_bool_1   BOOLEAN       NULL,
    reserved_bool_2   BOOLEAN       NULL,
    reserved_ext      JSONB         NULL DEFAULT '{}',

    -- Soft delete (from BaseEntity — REQUIRED — TRULE-010)
    deleted_at    BIGINT          NULL,
    deleted_by    VARCHAR(100)    NULL,

    -- Audit columns (from BaseEntity — REQUIRED)
    created_at    BIGINT          NOT NULL,
    created_by    VARCHAR(100)    NOT NULL,
    updated_at    BIGINT          NULL,
    updated_by    VARCHAR(100)    NULL
);

-- Recommended indexes
CREATE INDEX idx_{table_name}_tenant_id       ON {table_name} (tenant_id);
CREATE INDEX idx_{table_name}_deleted_at      ON {table_name} (deleted_at);
CREATE INDEX idx_{table_name}_created_at      ON {table_name} (created_at);
CREATE INDEX idx_{table_name}_{key_field}     ON {table_name} ({key_field});
```

### 9.3 Financial Values

```sql
-- ALWAYS use NUMERIC for financial data — NEVER VARCHAR (TRULE-004)
{amount_column}    NUMERIC(20,4)   NOT NULL DEFAULT 0.0000,
```

---

## 10. RabbitMQ Event Schemas

> **Broker note:** RabbitMQ is the **default** transport. If this service's Stack Profile (§3.1) selects **Kafka**,
> the **event envelopes in §10.1–§10.3 are identical** — only the transport binding/config changes. Fill in
> §10.4 for Kafka and write *"§10.4 N/A — broker is RabbitMQ"* otherwise. See `EKSAD_EVENT_CATALOG.md §11` for
> the full naming convention (topics, consumer groups, DLT, retry).

### 10.1 Standard Event Envelope

All RabbitMQ messages published by EKSAD services follow this JSON envelope:

```json
{
  "eventType"   : "<PROJECT>.<MODULE>.<ACTION>",
  "eventId"     : "{uuid-v4}",
  "tenantId"    : "{tenant_id}",
  "actorId"     : "{user_id}",
  "actorName"   : "{username}",
  "occurredAt"  : 1745280000000,
  "serviceId"   : "{service_name}",
  "payload"     : { }
}
```

### 10.2 Audit Log Event (`out-log-activity`)

> Automatically published by `eksad-core-common` `LogHandler`. Never produce this manually.

```json
{
  "transaction_id"       : "{entity_id}",
  "action"               : "CREATE",
  "username"             : "{username}",
  "role"                 : "ROLE_ADMIN",
  "status"               : "SUCCESS",
  "fail_reason"          : null,
  "request_uri"          : "/api/v1/transactions",
  "request_services"     : "{serialized request DTO}",
  "request_time"         : 1745280000000,
  "response_time"        : 1745280000150,
  "data_before"          : "{}",
  "data_after"           : "{serialized entity}",
  "log_activity_type"    : "EKSAD_SVC_LEADS.TRANSACTION.CREATE",
  "tenant_id"            : "{tenant_id}"
}
```

**RabbitMQ binding:**

| Property | Value |
|----------|-------|
| Exchange | `exc-log-activity` |
| Exchange Type | `direct` |
| Queue | `q-log-activity-eksad` |
| Routing Key | `r.q-log-activity-eksad` |

### 10.3 Custom Domain Events

```json
{
  "eventType"   : "{PROJECT_CODE}.{MODULE}.{ACTION}",
  "eventId"     : "{uuid-v4}",
  "tenantId"    : "{tenant_id}",
  "actorId"     : "{user_id}",
  "occurredAt"  : 1745280000000,
  "serviceId"   : "{SERVICE_NAME}",
  "payload"     : {
    "{FIELD_1}" : "{VALUE_1}",
    "{FIELD_2}" : "{VALUE_2}"
  }
}
```

### 10.4 Kafka Transport (opt-in — only when Stack Profile §3.1 broker = Kafka)

> Fill in this subsection **only** if the service is Kafka-native. RabbitMQ-broker services write *"N/A — broker
> is RabbitMQ"*. The envelope (§10.1) and `eventType` are unchanged — Kafka carries the same JSON as the message
> `value`, keyed by `tenantId`. Naming follows `EKSAD_EVENT_CATALOG.md §11.2`.

**Topic bindings:**

| Stream | Topic | Partition Key | Consumer Group | DLT | Retry |
|--------|-------|---------------|----------------|-----|-------|
| Domain events | `{domain}.domain-events` | `tenantId` | `cg-{SERVICE_NAME}` | `{domain}.domain-events.dlt` | `{domain}.domain-events.retry` |
| Master-data sync (consume) | `{domain}.master-data` | `tenantId` | `cg-{SERVICE_NAME}-master-sync` | `{domain}.master-data.dlt` | — |
| Audit (optional alt-ingress) | `log-activity` | `tenantId` | `cg-audittrail` | `log-activity.dlt` | `log-activity.retry` |

**`application.properties` — SmallRye Kafka (copy + fill `${ENV_VAR}`):**

```properties
# ── Kafka connection (shared) ─────────────────────────────────────────────
kafka.bootstrap.servers=${KAFKA_BOOTSTRAP_SERVERS}
mp.messaging.connector.smallrye-kafka.security.protocol=${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
# (SASL example — uncomment for managed Kafka)
# mp.messaging.connector.smallrye-kafka.sasl.mechanism=${KAFKA_SASL_MECHANISM}
# mp.messaging.connector.smallrye-kafka.sasl.jaas.config=${KAFKA_SASL_JAAS_CONFIG}

# ── Outgoing: domain events ───────────────────────────────────────────────
mp.messaging.outgoing.out-domain-events.connector=smallrye-kafka
mp.messaging.outgoing.out-domain-events.topic={domain}.domain-events
mp.messaging.outgoing.out-domain-events.key.serializer=org.apache.kafka.common.serialization.StringSerializer
mp.messaging.outgoing.out-domain-events.value.serializer=org.apache.kafka.common.serialization.StringSerializer
# Reliability: wait for all in-sync replicas + idempotent producer (exactly-once-ish)
mp.messaging.outgoing.out-domain-events.acks=all
mp.messaging.outgoing.out-domain-events.enable.idempotence=true

# ── Incoming: master-data sync (cache) ────────────────────────────────────
mp.messaging.incoming.in-master-data.connector=smallrye-kafka
mp.messaging.incoming.in-master-data.topic={domain}.master-data
mp.messaging.incoming.in-master-data.group.id=cg-${quarkus.application.name}-master-sync
mp.messaging.incoming.in-master-data.key.deserializer=org.apache.kafka.common.serialization.StringDeserializer
mp.messaging.incoming.in-master-data.value.deserializer=org.apache.kafka.common.serialization.StringDeserializer
mp.messaging.incoming.in-master-data.auto.offset.reset=earliest
mp.messaging.incoming.in-master-data.enable.auto.commit=false
# Dead-letter + retry (SmallRye failure strategy)
mp.messaging.incoming.in-master-data.failure-strategy=dead-letter-queue
mp.messaging.incoming.in-master-data.dead-letter-queue.topic={domain}.master-data.dlt
```

> **Rules carried over from the platform:** never hard-code broker host/credentials — always `${ENV_VAR}`;
> consumers must be idempotent (dedup by `eventId`) and tolerate unknown fields (`FAIL_ON_UNKNOWN_PROPERTIES=false`)
> per `EKSAD_EVENT_CATALOG.md §14.3`; stamp `last_synced_at` from envelope `occurredAt` for cache ordering.

---

## 11. MongoDB Audit Schema

**Database:** `eksad_audit`
**Collection:** `log_activity`

### 11.1 Document Structure

```json
{
  "_id"                : ObjectId,
  "transaction_id"     : "String",
  "action"             : "String",
  "username"           : "String",
  "role"               : "String",
  "status"             : "String",
  "fail_reason"        : "String | null",
  "request_uri"        : "String",
  "request_payload"    : "String (JSON)",
  "request_time"       : NumberLong,
  "response_time"      : NumberLong,
  "data_before"        : "String (JSON)",
  "data_after"         : "String (JSON)",
  "data_changes"       : "String (JSON diff)",
  "log_activity_type"  : "String",
  "tenant_id"          : "String",
  "created_at"         : NumberLong
}
```

### 11.2 Recommended Indexes

```javascript
db.log_activity.createIndex({ "log_activity_type": 1 });
db.log_activity.createIndex({ "tenant_id": 1 });
db.log_activity.createIndex({ "username": 1 });
db.log_activity.createIndex({ "request_time": -1 });
db.log_activity.createIndex({ "tenant_id": 1, "log_activity_type": 1, "request_time": -1 });
db.log_activity.createIndex({ "transaction_id": 1 });
```

---

## 12. API Code Skeleton

### 12.1 Entity

> *Add `// FR-{MODULE}-{N}` comment next to each domain field to record which FR requires that field.*

```java
package com.eksad.svc.{domain}.data.entities;

import com.eksad.core.common.data.base.BaseEntity;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

@Data
@SuperBuilder
@NoArgsConstructor
@Entity
@Table(name = "{table_name}")
public class {Entity}Entity extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "tenant_id", nullable = false)
    private String tenantId;                         // FR-AUTH-001

    // ─── Domain columns ────────────────────────────────────
    @Column(name = "{column_1}", nullable = false)
    private String {field1};                         // FR-{MODULE}-001

    // Financial values: ALWAYS BigDecimal, NEVER String/Double (TRULE-004)
    @Column(name = "amount", nullable = false, precision = 20, scale = 4)
    private java.math.BigDecimal amount;             // FR-{MODULE}-001

    // ─── Reserved fields (transactional entities only) ─────────────────────────
    // Opt-in: if this entity requires tenant-configurable extension fields,
    // extend BaseTransactionalEntity instead of BaseEntity (see TRULE-012).
    //
    //   public class {Entity}Entity extends BaseTransactionalEntity {  ← change this line
    //
    // BaseTransactionalEntity adds all 13 reserved columns automatically:
    //   reserved_str_1..5   VARCHAR(500)  — flexible text slots
    //   reserved_num_1..3   NUMERIC(20,4) — numeric / financial slots
    //   reserved_date_1..2  BIGINT        — epoch-ms date slots (TRULE-007)
    //   reserved_bool_1..2  BOOLEAN       — flag slots
    //   reserved_ext        JSONB         — overflow JSONB (Sprint 2+, TRULE-013)
    //
    // If this entity does NOT need reserved fields, keep extending BaseEntity and
    // remove this comment block before merging.
    // ────────────────────────────────────────────────────────────────────────────

    // ─── File reference (optional — include only if this entity has attachments) ──
    // Store ONLY the file_id returned by eksad-core-storage after upload (TRULE-005).
    // NEVER store s3_key, cdn_url, or any raw storage path.
    // Resolve URL at render-time: GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/url
    @Column(name = "{field_name}_file_id")
    private Long {fieldName}FileId;                  // FR-{MODULE}-002
}
```

### 12.2 Module Type Constants

```java
package com.eksad.svc.{domain}.common.constants;

/**
 * Audit log module type constants.
 * Format: <PROJECT>.<MODULE>.<ACTION>
 * Convention: {PROJECT_CODE} = EKSAD_SVC_{DOMAIN_UPPER}
 */
public interface {Domain}ModuleType {
    String PREFIX     = "EKSAD_SVC_{DOMAIN_UPPER}";

    interface {Module} {
        String CREATE  = PREFIX + ".{MODULE_UPPER}.CREATE";   // FR-{MODULE}-001
        String UPDATE  = PREFIX + ".{MODULE_UPPER}.UPDATE";   // FR-{MODULE}-002
        String DELETE  = PREFIX + ".{MODULE_UPPER}.DELETE";   // FR-{MODULE}-003
        String SUBMIT  = PREFIX + ".{MODULE_UPPER}.SUBMIT";   // FR-{MODULE}-{N}
        String APPROVE = PREFIX + ".{MODULE_UPPER}.APPROVE";  // FR-{MODULE}-{N}
        String REJECT  = PREFIX + ".{MODULE_UPPER}.REJECT";   // FR-{MODULE}-{N}
    }
}
```

### 12.3 Repository

```java
package com.eksad.svc.{domain}.data.repositories;

import com.eksad.core.common.core.repository.BaseRepository;
import com.eksad.svc.{domain}.common.constants.{Domain}ModuleType;
import com.eksad.svc.{domain}.core.dto.{Entity}DTO;
import com.eksad.svc.{domain}.data.entities.{Entity}Entity;
import jakarta.enterprise.context.ApplicationScoped;
import io.smallrye.mutiny.Uni;
import java.time.Instant;

@ApplicationScoped
public class {Entity}Repository extends BaseRepository<{Entity}Entity, {Entity}DTO, Long> {

    @Override
    public String moduleType() {
        return {Domain}ModuleType.{Module}.CREATE;
    }

    @Override
    public Long toId({Entity}DTO dto) {
        return dto.getId();
    }

    @Override
    public String extractDtoId({Entity}DTO dto) {
        return dto.getId() != null ? dto.getId().toString() : null;
    }

    @Override
    public String extractTransactionId({Entity}Entity entity) {
        return entity.getId() != null ? entity.getId().toString() : null;
    }

    @Override
    public {Entity}Entity toNewEntity({Entity}DTO dto, Object... extras) {
        long now = Instant.now().toEpochMilli();
        return {Entity}Entity.builder()
                .tenantId(getUserContext().getTenantId())
                .{field1}(dto.get{Field1}())
                .createdAt(now)
                .createdBy(currentUser())
                .build();
    }

    // ─── Business methods ──────────────────────────────────────────────────

    // FR-{MODULE}-001 · Traceability Matrix row 1
    @Override
    public Uni<{Entity}Entity> createEntity({Entity}DTO dto) {
        return createFlow(dto, {Domain}ModuleType.{Module}.CREATE);
    }

    // FR-{MODULE}-002 · Traceability Matrix row 2
    @Override
    public Uni<{Entity}Entity> updateEntity({Entity}DTO dto) {
        return updateFlow(dto,
                {Domain}ModuleType.{Module}.UPDATE,
                entity -> entity.getDeletedAt() == null,
                entity -> "{Entity} is already deleted",
                auditMutator(entity -> {
                    entity.set{Field1}(dto.get{Field1}());
                }));
    }

    // FR-{MODULE}-003 · Traceability Matrix row 3
    @Override
    public Uni<{Entity}Entity> deleteEntity({Entity}DTO dto) {
        return deleteFlow(dto, {Domain}ModuleType.{Module}.DELETE, softDeleteMutator());
    }
}
```

### 12.4 Service

```java
package com.eksad.svc.{domain}.core.service;

import com.eksad.svc.{domain}.core.dto.{Entity}DTO;
import com.eksad.svc.{domain}.data.entities.{Entity}Entity;
import com.eksad.svc.{domain}.data.repositories.{Entity}Repository;
import io.quarkus.hibernate.reactive.panache.common.WithSession;
import io.quarkus.hibernate.reactive.panache.common.runtime.ReactiveTransactional;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
@WithSession
public class {Entity}Service {

    @Inject
    {Entity}Repository repository;

    // FR-{MODULE}-001 · Traceability Matrix row 1
    @ReactiveTransactional
    public Uni<{Entity}Entity> create({Entity}DTO dto) {
        return repository.createEntity(dto);
    }

    // FR-{MODULE}-002 · Traceability Matrix row 2
    @ReactiveTransactional
    public Uni<{Entity}Entity> update({Entity}DTO dto) {
        return repository.updateEntity(dto);
    }

    // FR-{MODULE}-003 · Traceability Matrix row 3
    @ReactiveTransactional
    public Uni<{Entity}Entity> delete({Entity}DTO dto) {
        return repository.deleteEntity(dto);
    }

    // FR-{MODULE}-004 · Traceability Matrix row 4
    public Uni<{Entity}Entity> findById(Long id) {
        return repository.findById(id);
    }
}
```

### 12.5 REST Resource

```java
package com.eksad.svc.{domain}.transport.resource;

import com.eksad.svc.{domain}.core.dto.{Entity}DTO;
import com.eksad.svc.{domain}.core.service.{Entity}Service;
import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import io.smallrye.mutiny.Uni;
import org.eclipse.microprofile.openapi.annotations.tags.Tag;

@Path("/api/v1/{module_path}")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "{Module} API", description = "{Module description}")
public class {Entity}Resource {

    @Inject
    {Entity}Service service;

    // FR-{MODULE}-001 · Traceability Matrix row 1
    @POST
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}"})
    public Uni<Response> create({Entity}DTO dto) {
        return service.create(dto)
                .map(entity -> Response.status(Response.Status.CREATED).entity(entity).build());
    }

    // FR-{MODULE}-004 · Traceability Matrix row 4
    @GET
    @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}", "ROLE_VIEWER"})
    public Uni<Response> findById(@PathParam("id") Long id) {
        return service.findById(id)
                .map(entity -> Response.ok(entity).build());
    }

    // FR-{MODULE}-002 · Traceability Matrix row 2
    @PUT
    @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}"})
    public Uni<Response> update({Entity}DTO dto) {
        return service.update(dto)
                .map(entity -> Response.ok(entity).build());
    }

    // FR-{MODULE}-003 · Traceability Matrix row 3
    @DELETE
    @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN"})
    public Uni<Response> delete({Entity}DTO dto) {
        return service.delete(dto)
                .map(entity -> Response.ok(entity).build());
    }
}
```

---

## 13. BaseRepository Implementation Guide

> For detailed patterns, diagrams, and edge cases see `EKSAD_SYSTEM_DESIGN_PATTERNS.md`.

### 13.1 Steps to Implement a New Repository

1. Create your entity extending `BaseEntity` — add `tenant_id` field
2. Create your DTO class with Lombok `@Data @Builder @NoArgsConstructor @AllArgsConstructor`
3. Create `{Domain}ModuleType` interface with string constants — add FR ref comments per constant
4. Extend `BaseRepository<Entity, DTO, ID>`
5. Implement 5 abstract methods: `toId`, `extractDtoId`, `extractTransactionId`, `toNewEntity`, `moduleType`
6. Implement 3 CRUD methods: `createEntity`, `updateEntity`, `deleteEntity` — using `createFlow`, `updateFlow`, `deleteFlow`
7. Inject repository in service, annotate service with `@WithSession`
8. Add `// FR-{MODULE}-{N} · Traceability Matrix row {N}` comment to each business method
9. Audit trail fires automatically to RabbitMQ — no additional config needed

### 13.2 Module Type Naming Quick Reference

```
Format: <PROJECT>.<MODULE>.<ACTION>

PROJECT  = EKSAD_SVC_{SERVICE_DOMAIN_UPPER}
MODULE   = domain entity or bounded context (TRANSACTION, ORDER, USER, etc.)
ACTION   = CREATE | UPDATE | DELETE | SUBMIT | APPROVE | REJECT | EXPORT | IMPORT
```

---

## 14. Testing Strategy

### 14.1 Unit Tests (Service Layer)

> *Each test method maps to a specific FR. Add `// FR-{MODULE}-{N}` comment above each test.*

```java
@ExtendWith(MockitoExtension.class)
class {Entity}ServiceTest {

    @Mock
    {Entity}Repository repository;

    @InjectMocks
    {Entity}Service service;

    // FR-{MODULE}-001
    @Test
    void create_shouldReturnEntity() {
        {Entity}DTO dto = {Entity}DTO.builder().{field1}("test").build();
        {Entity}Entity expected = {Entity}Entity.builder().id(1L).{field1}("test").build();

        when(repository.createEntity(dto)).thenReturn(Uni.createFrom().item(expected));

        {Entity}Entity result = service.create(dto).await().indefinitely();
        assertThat(result.getId()).isEqualTo(1L);
    }
}
```

### 14.2 Integration Tests

```java
@QuarkusTest
@TestHTTPEndpoint({Entity}Resource.class)
class {Entity}ResourceTest {

    // FR-{MODULE}-001
    @Test
    void create_shouldReturn201() {
        given()
            .header("Authorization", "Bearer " + getTestJwt())
            .contentType(ContentType.JSON)
            .body("""
                { "{field1}": "test_value" }
            """)
            .when().post()
            .then()
            .statusCode(201);
    }
}
```

### 14.3 Mock UserContext for Tests

```java
@ApplicationScoped
@Priority(1)
@Alternative
public class MockUserContext extends UserContext {
    @Override public String getUser() { return "test-user"; }
    @Override public String getRole() { return "ROLE_ADMIN"; }
}
```

---

## 15. Nexus & Deployment Configuration

### 15.1 `~/.m2/settings.xml` — Nexus Credentials

```xml
<settings>
  <servers>
    <server>
      <id>eksad-nexus-snapshots</id>
      <username>${NEXUS_USERNAME}</username>
      <password>${NEXUS_PASSWORD}</password>
    </server>
    <server>
      <id>eksad-nexus-releases</id>
      <username>${NEXUS_USERNAME}</username>
      <password>${NEXUS_PASSWORD}</password>
    </server>
  </servers>
</settings>
```

### 15.2 Publish to Nexus

```bash
# Publish SNAPSHOT
mvn clean deploy -DskipTests

# Promote to RELEASE (update version first — remove -SNAPSHOT)
mvn versions:set -DnewVersion=1.0.0
mvn clean deploy -DskipTests -P release
```

### 15.3 Build Native Image (Optional)

```bash
mvn package -Pnative -DskipTests
```

---

## 16. File Storage Integration

> ⚠️ **This section is OPTIONAL.** Include it only if this service requires file upload or attachment functionality. If this service has no file handling requirements, skip this section entirely.

---

### 16.1 Overview

The EKSAD platform centralizes all file operations in a dedicated core service: **`eksad-core-storage`** (`:8090`). No domain service may interact with S3 or Cloudflare R2 directly (TRULE-005).

The responsibilities are split clearly:
- **`eksad-core-storage`** — owns the file lifecycle: upload validation, object storage, CDN URL management, and thumbnail generation.
- **Domain service** — stores only a `file_id` (BIGINT) as a lightweight reference. It never holds any object storage key, bucket path, or CDN URL.

This separation means that if the storage provider changes (e.g., from AWS to Cloudflare), domain services require zero changes.

---

### 16.2 Upload Flow

1. The **client** sends the file directly to `eksad-core-storage` via `POST /api/v1/storage/upload` as a multipart request, including: `file`, `visibility` (`PUBLIC`/`PRIVATE`), `refEntityType`, `refEntityId`.
2. `eksad-core-storage` validates, stores to object storage, persists metadata, and returns `{ fileId, cdnUrl? }`. `cdnUrl` returned for `PUBLIC` files only.
3. The **client** passes the returned `fileId` as part of the domain service's create/update request body.
4. The **domain service** stores only the `fileId` (e.g., `{field}_file_id BIGINT`).
5. Thumbnail generation runs asynchronously via RabbitMQ `exc-file-processing` — does not block the response.

---

### 16.3 URL Resolution at Render-Time

Domain services must **never** cache or store resolved URLs. Fetch on demand:

- **File URL:** `GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/url`
  → Permanent CDN URL for `PUBLIC`; short-lived signed URL for `PRIVATE` (TTL: 300 s).

- **Thumbnail URL:** `GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/thumbnail-url`
  → Falls back to original URL if thumbnail is pending or failed.

Signed URLs must not be stored or forwarded in RabbitMQ events.

---

### 16.4 File Visibility Rules

- **`PUBLIC`** — public-read bucket; permanent CDN URL; for logos, brochures, non-sensitive images.
- **`PRIVATE`** — private bucket; signed URL per request (TTL default 300 s); for contracts, reports, confidential documents.
- **Thumbnail visibility** always inherits from parent file.

---

### 16.5 Flyway DDL — Storing `file_id` in Domain Tables

```sql
-- Logical FK by convention only — no DB-level FOREIGN KEY constraint (TRULE-006)
{field_name}_file_id   BIGINT   NULL,   -- ref: eksad-core-storage.file_metadata.id

-- Index if queried:
CREATE INDEX idx_{table_name}_{field_name}_file_id ON {table_name} ({field_name}_file_id);
```

---

### 16.6 Module Types for File Audit Trail

| Action | Module Type String |
|--------|--------------------|
| Upload | `EKSAD_CORE_STORAGE.FILE.UPLOAD` |
| Delete | `EKSAD_CORE_STORAGE.FILE.DELETE` |
| Access audit *(reserved)* | `EKSAD_CORE_STORAGE.FILE.ACCESS` |

Domain services do not produce these events — `eksad-core-storage` handles them automatically.

---

### 16.7 Further Reference

> **`EKSAD_SYSTEM_DESIGN_PATTERNS.md` — Section 10: File Storage Pattern**

---

## 17. Global Technical Rules

> *Enforcement rules for all technical components in this TSD — derived from the platform design principles in §3.1.*

| Rule ID | Rule | Applies To |
|---|---|---|
| TRULE-001 | Every class implementing business logic must trace to at least one FR ID in the Traceability Matrix (§2). Classes with no FR link must be flagged in Gap Analysis (§18). | All service and repository classes |
| TRULE-002 | All CRUD operations must go through `BaseRepository` flows (`createFlow`, `updateFlow`, `deleteFlow`). No direct entity manager or Panache CRUD calls. | All repositories |
| TRULE-003 | All DB timestamps must be `BIGINT` (epoch milliseconds). Java type must be `Long`. Never use `LocalDateTime`, `Date`, or `Timestamp`. | All entities, DDL |
| TRULE-004 | All financial values must use `NUMERIC(20,4)` in DDL and `BigDecimal` in Java. Never use `VARCHAR`, `DOUBLE`, or `FLOAT`. | All financial entities |
| TRULE-005 | No domain service may call S3, R2, or any object storage directly. All file operations via `eksad-core-storage` REST API. Domain entities store only `file_id BIGINT`. | All file-handling features |
| TRULE-006 | No domain service may add a `FOREIGN KEY` constraint referencing another service's database. Cross-service references are by ID convention only. | All DDL migrations |
| TRULE-007 | All API endpoints must declare `@RolesAllowed`. Any PUBLIC endpoint must be explicitly documented with justification in the FSD. | All REST resources |
| TRULE-008 | All Flyway migration files are immutable after commit. Schema changes require a new versioned file. `ddl-auto=update` is forbidden. | All DDL migrations |
| TRULE-009 | Every DB table must include `tenant_id VARCHAR(100) NOT NULL` with an index on `tenant_id`. | All entities, DDL |
| TRULE-010 | Soft delete is mandatory. Never issue a hard `DELETE`. Use `deleteFlow` from `BaseRepository` which sets `deleted_at` + `deleted_by`. | All repositories |
| TRULE-011 | `[STALE]` tag must be applied to any Traceability Matrix row where the method signature has changed. Remove only after updating the row. | Traceability Matrix (§2) |
| TRULE-012 | Every transactional entity that opts-in to reserved fields must include 13 reserved field columns per `EKSAD_RESERVED_FIELD_PATTERNS.md` (5 string + 3 numeric + 2 date + 2 boolean + 1 JSONB overflow) and extend `BaseTransactionalEntity` (NOT `BaseEntity`). Master data, cache, and audit tables are EXEMPT. | All transactional DDL & entities |
| TRULE-013 | The `reserved_field_config` table must be created in every domain service database that has at least one transactional entity opted-in to reserved fields. Config rows are managed via admin UI — never seeded in V1 migration. | All domain service DDL |
| TRULE-014 | Every service must validate JWT independently via JWKS from `eksad-core-auth`. API Gateway is OPTIONAL — services MUST NOT depend on gateway for auth (D13). | All services |
| TRULE-015 | Domain service names must follow `svc-{function}` convention (lowercase, hyphen, domain-agnostic). Business jargon (`svc-spk`, `svc-leads`, `svc-prospek`) is FORBIDDEN. FIXED platform services (`eksad-core-*`, `svc-user-management`, `svc-tenant-management`, `svc-master-data`) MUST NOT be renamed. Final names + ports documented in §3.2 Service Registry. | All services |

---

## 18. Gap Analysis

> *Record all gaps identified during TSD authoring. Critical gaps block TSD approval.*

> **Rule:** No TSD may be submitted for approval while a Critical gap remains unresolved.

| Gap ID | Description | Severity | Affected Section / Component | Owner | Resolution / Status |
|---|---|---|---|---|---|
| GAP-001 | {DESCRIPTION} | Critical / Non-Critical | {SECTION / CLASS} | {OWNER} | Open / Resolved / Deferred |

**Severity Definitions:**
- **Critical** — missing implementation decision for a core FR, undefined DB schema for a required entity, or unresolved integration contract. Blocks TSD approval.
- **Non-Critical** — missing edge case handling, non-blocking tech detail. Document may proceed with gap documented and owner assigned.

---

## 19. Open Issues & Decisions Log

> *Track all unresolved technical questions and decisions tagged `[CLARIFY]` or `[UNCONFIRMED]`. This log must be empty before the document status changes to Approved.*

| Issue ID | Description | Raised By | Owner | Target Date | Status |
|---|---|---|---|---|---|
| ISS-001 | {DESCRIPTION} | {RAISED_BY} | {OWNER} | {DATE} | Open / Resolved / Deferred |

---

## 20. Glossary

| Term | Definition |
|------|------------|
| `BaseEntity` | Superclass from `eksad-core-common` providing `created_at`, `updated_at`, `deleted_at`, `created_by`, `updated_by`, `deleted_by` as `BIGINT`/`VARCHAR` fields. |
| `CrudFlows` | Generic reactive CRUD interface in `eksad-core-common` with built-in audit trail integration. |
| `BaseRepository` | Abstract implementation of `CrudFlows` — extend this in every service repository. Handles `createFlow`, `updateFlow`, `deleteFlow`, and automatic RabbitMQ audit publishing. |
| `createFlow` | `BaseRepository` method that persists a new entity and publishes an audit event. Accepts module type string. |
| `updateFlow` | `BaseRepository` method that updates an entity with a guard predicate and audit mutator, then publishes an audit event. |
| `deleteFlow` | `BaseRepository` method that soft-deletes an entity and publishes an audit event. |
| `softDeleteMutator()` | Helper in `BaseRepository` that sets `deleted_at` and `deleted_by` from the JWT context. |
| `auditMutator(consumer)` | Helper in `BaseRepository` that captures `data_before` before applying a field mutation, then captures `data_after`. |
| Module Type | Dot-separated string identifying the audit event source: `<PROJECT>.<MODULE>.<ACTION>`. |
| `LogHandler` | Component in `eksad-core-common` that serializes and publishes audit log events to RabbitMQ. Invoked automatically by `BaseRepository` flows. |
| `UserContext` | CDI bean providing the current JWT-authenticated user's `sub`, `role`, and `tenant_id`. Injected into `BaseRepository`. |
| Flyway | Database migration tool — all DDL in versioned `.sql` files. `ddl-auto=update` is forbidden. |
| Epoch Milliseconds | All timestamps stored as `BIGINT` — ms since 1970-01-01T00:00:00Z. Java: `Instant.now().toEpochMilli()`. |
| `file_id` | A `BIGINT` stored in a domain entity referencing a file record in `eksad-core-storage`. Never store raw S3 keys or CDN URLs. |
| Signed URL | A time-limited URL for accessing a `PRIVATE` file. Generated by `eksad-core-storage` per request. TTL default: 300 s. |
| `[STALE]` | Tag applied to a Traceability Matrix row when the referenced method signature has changed. Remove only after updating the row. |
| FR ID | Functional Requirement identifier from the FSD. Format: `FR-{MODULE}-{N}`. |
| Feature ID | Feature identifier from the FSD. Format: `F-{N}`. |
| `tenant_id` | Unique string identifier for a tenant — present in all JWT tokens, DB rows, and RabbitMQ messages. |
| `BaseTransactionalEntity` | Subclass of `BaseEntity` in `eksad-core-common` that adds 13 reserved field columns (5 string + 3 numeric + 2 date + 2 boolean + 1 JSONB). Transactional entities that opt-in to tenant-configurable custom fields extend this instead of `BaseEntity` directly. Master data, cache (`_cache`), and audit tables are EXEMPT — they continue to extend `BaseEntity`. See `EKSAD_RESERVED_FIELD_PATTERNS.md`. |
| Reserved Field | A pre-allocated column in a transactional entity table (`reserved_str_1..5`, `reserved_num_1..3`, `reserved_date_1..2`, `reserved_bool_1..2`) that can be mapped to a tenant-specific custom field via `reserved_field_config`. Enables tenant customization without DDL changes. |
| `reserved_field_config` | Per-domain-service config table that maps reserved columns to display labels, validation rules, visibility, and conditional logic per tenant. Supports 3-tier cascade resolution: global < domain < tenant (later wins). Resolved values are cached with TTL via `@CacheResult`. |
| `reserved_ext` | JSONB overflow column on every `BaseTransactionalEntity` for unlimited ad-hoc custom fields beyond the 12 typed slots. Indexable via PostgreSQL functional index or GIN (`USING GIN (reserved_ext jsonb_path_ops)`) on opt-in basis. |

---

## Appendix — Change Log

| Version | Date | Author | Summary of Changes |
|---------|------|--------|--------------------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `eksad-core-storage :8090` to architecture diagram and service registry; added Design Principle #8 (soft delete) and #9 (file reference by ID only); added optional `STORAGE_*` env block to `application.properties`; added `file_id` comment to entity skeleton; added Section 16 — File Storage Integration |
| 3.0 | 2026-05-02 | EKSAD Platform Team | Major upgrade to v3: Document Control table, Revision History & Approval blocks, Introduction (§1), Traceability Matrix (§2) with FR ID → Feature ID → Class → Method columns, `[STALE]` tagging convention, FR ref comments throughout all code skeleton methods and entity fields, DDL template updated with FR Refs comment header and TRULE references, Global Technical Rules (§17) TRULE-001–011, Gap Analysis (§18), Open Issues & Decisions Log (§19), Glossary (§20), all sections renumbered |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |
