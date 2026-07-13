# Technical Specification Document (TSD)
# {PROJECT_NAME} — Version {VERSION}

**Document Version:** {VERSION}
**Date:** {DATE}
**Status:** 🔴 Draft / 🟡 In Progress / 🟢 Final *(pick one)*
**Prepared by:** {PREPARED_BY}
**Organization:** PT EKSAD / {BUSINESS_UNIT}
**Related Documents:**
- `BRD_{PROJECT_CODE}_v{VERSION}.md` — Business requirements
- `FSD_{PROJECT_CODE}_v{VERSION}.md` — Functional specification

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Parent POM & Dependencies](#2-parent-pom--dependencies)
3. [Project Structure](#3-project-structure)
4. [Docker Compose — Local Development](#4-docker-compose--local-development)
5. [JWT Configuration — RS256](#5-jwt-configuration--rs256)
6. [application.properties — Per Service Template](#6-applicationproperties--per-service-template)
7. [Flyway DDL Conventions](#7-flyway-ddl-conventions)
8. [RabbitMQ Event Schemas](#8-rabbitmq-event-schemas)
9. [MongoDB Audit Schema](#9-mongodb-audit-schema)
10. [API Code Skeleton](#10-api-code-skeleton)
11. [BaseRepository Implementation Guide](#11-baserepository-implementation-guide)
12. [Testing Strategy](#12-testing-strategy)
13. [Nexus & Deployment Configuration](#13-nexus--deployment-configuration)
14. [File Storage Integration](#14-file-storage-integration)

---

## 1. Architecture Overview

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

### 1.1 Design Principles

1. **No business logic in gateway** — only JWT validation, rate limiting, routing
2. **Each service owns its schema** — no cross-service DB JOINs; use events for data sync
3. **Events over synchronous calls** — async RabbitMQ for audit, notifications; sync HTTP only for user-facing reads
4. **`tenant_id` everywhere** — every DB row, every JWT claim, every RabbitMQ message payload
5. **Flyway only** — zero `ddl-auto=update`; all DDL changes versioned in `V{N}__{description}.sql`
6. **Auto audit trail** — every CRUD operation uses `BaseRepository` flows; no manual RabbitMQ wiring
7. **Long epoch for timestamps** — all DB timestamps as `BIGINT` (epoch milliseconds); Java type is `Long`
8. **Soft delete** — never hard-delete; use `deleted_at BIGINT` + `deleted_by VARCHAR` from `BaseEntity`
9. **File reference by ID only** — domain services store only `file_id BIGINT`; never raw S3 keys or CDN URLs. Resolve URLs at render-time via `GET /api/v1/storage/{fileId}/url`

### 1.2 Service Registry

| Service | Artifact ID | Port | DB | Purpose |
|---------|-------------|------|----|---------|
| eksad-auth | `eksad-svc-auth` | 8081 | PostgreSQL | JWT issuance, user management |
| {SERVICE_2} | `{ARTIFACT_2}` | {PORT} | PostgreSQL | {PURPOSE} |
| {SERVICE_3} | `{ARTIFACT_3}` | {PORT} | PostgreSQL | {PURPOSE} |
| eksad-core-audittrail | `eksad-core-audittrail` | 8089 | MongoDB | Audit log storage |
| eksad-core-storage | `eksad-core-storage` | 8090 | PostgreSQL (`eksad_storage`) + AWS S3 or Cloudflare R2 | File upload, metadata, CDN URL resolution, thumbnail generation |

---

## 2. Parent POM & Dependencies

### 2.1 `eksad-parent` POM

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

### 2.2 Per-Service `pom.xml` Template

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

## 3. Project Structure

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

## 4. Docker Compose — Local Development

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

## 5. JWT Configuration — RS256

### 5.1 Key Generation (Run Once)

```bash
# Generate 4096-bit RSA key pair — store private key in secure vault (never commit to Git)
openssl genrsa -out eksad-private-key.pem 4096
openssl rsa -in eksad-private-key.pem -pubout -out eksad-public-key.pem

# Convert to PKCS8 — required by SmallRye JWT
openssl pkcs8 -topk8 -nocrypt -inform pem -in eksad-private-key.pem \
  -outform pem -out eksad-private-key-pkcs8.pem
```

### 5.2 JWT Payload Structure

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

### 5.3 Auth Service Config

```properties
# application.properties — eksad-auth-service ONLY
mp.jwt.verify.issuer=eksad-auth-service
smallrye.jwt.sign.key.location=META-INF/resources/eksad-private-key-pkcs8.pem
smallrye.jwt.new-token.issuer=eksad-auth-service
smallrye.jwt.new-token.lifespan=86400
smallrye.jwt.new-token.audience=eksad-services
```

### 5.4 All Other Services — JWT Validator Config

```properties
# application.properties — every service EXCEPT eksad-auth-service
mp.jwt.verify.issuer=eksad-auth-service
mp.jwt.verify.publickey.location=META-INF/resources/eksad-public-key.pem
quarkus.smallrye-jwt.enabled=true
```

---

## 6. application.properties — Per Service Template

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

## 7. Flyway DDL Conventions

### 7.1 Naming Convention

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

### 7.2 Standard Table Template

```sql
-- V1__init_{domain}.sql
-- Service: {SERVICE_NAME}
-- Author:  {AUTHOR}
-- Date:    {DATE}

CREATE TABLE IF NOT EXISTS {table_name} (
    -- Primary Key
    id            BIGSERIAL       PRIMARY KEY,

    -- Tenant isolation (REQUIRED on every table)
    tenant_id     VARCHAR(100)    NOT NULL,

    -- Domain columns
    {COLUMN_1}    {TYPE_1}        {CONSTRAINTS_1},
    {COLUMN_2}    {TYPE_2}        {CONSTRAINTS_2},

    -- Soft delete (from BaseEntity — REQUIRED)
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

### 7.3 Financial Values

```sql
-- ALWAYS use NUMERIC for financial data — NEVER VARCHAR
{amount_column}    NUMERIC(20,4)   NOT NULL DEFAULT 0.0000,
```

---

## 8. RabbitMQ Event Schemas

### 8.1 Standard Event Envelope

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

### 8.2 Audit Log Event (`out-log-activity`)

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

### 8.3 Custom Domain Events

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

---

## 9. MongoDB Audit Schema

**Database:** `eksad_audit`
**Collection:** `log_activity`

### 9.1 Document Structure

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

### 9.2 Recommended Indexes

```javascript
// Run in MongoDB shell or Atlas index manager
db.log_activity.createIndex({ "log_activity_type": 1 });
db.log_activity.createIndex({ "tenant_id": 1 });
db.log_activity.createIndex({ "username": 1 });
db.log_activity.createIndex({ "request_time": -1 });
db.log_activity.createIndex({ "tenant_id": 1, "log_activity_type": 1, "request_time": -1 });
db.log_activity.createIndex({ "transaction_id": 1 });
```

---

## 10. API Code Skeleton

### 10.1 Entity

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
    private String tenantId;

    // ─── Domain columns ────────────────────────────────────
    @Column(name = "{column_1}", nullable = false)
    private String {field1};

    // Financial values: ALWAYS BigDecimal, NEVER String/Double
    @Column(name = "amount", nullable = false, precision = 20, scale = 4)
    private java.math.BigDecimal amount;

    // ─── File reference (optional — include only if this entity has attachments) ──
    // Store ONLY the file_id returned by eksad-core-storage after upload.
    // NEVER store s3_key, cdn_url, or any raw storage path in domain entities.
    // Resolve to URL at render-time: GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/url
    @Column(name = "{field_name}_file_id")
    private Long {fieldName}FileId;
}
```

### 10.2 Module Type Constants

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
        String CREATE  = PREFIX + ".{MODULE_UPPER}.CREATE";
        String UPDATE  = PREFIX + ".{MODULE_UPPER}.UPDATE";
        String DELETE  = PREFIX + ".{MODULE_UPPER}.DELETE";
        String SUBMIT  = PREFIX + ".{MODULE_UPPER}.SUBMIT";
        String APPROVE = PREFIX + ".{MODULE_UPPER}.APPROVE";
        String REJECT  = PREFIX + ".{MODULE_UPPER}.REJECT";
    }
}
```

### 10.3 Repository

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
        return {Domain}ModuleType.{Module}.CREATE; // default; overridden per flow call
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

    @Override
    public Uni<{Entity}Entity> createEntity({Entity}DTO dto) {
        return createFlow(dto, {Domain}ModuleType.{Module}.CREATE);
    }

    @Override
    public Uni<{Entity}Entity> updateEntity({Entity}DTO dto) {
        return updateFlow(dto,
                {Domain}ModuleType.{Module}.UPDATE,
                entity -> entity.getDeletedAt() == null,       // guard: not deleted
                entity -> "{Entity} is already deleted",
                auditMutator(entity -> {
                    entity.set{Field1}(dto.get{Field1}());
                }));
    }

    @Override
    public Uni<{Entity}Entity> deleteEntity({Entity}DTO dto) {
        return deleteFlow(dto, {Domain}ModuleType.{Module}.DELETE, softDeleteMutator());
    }
}
```

### 10.4 Service

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

    @ReactiveTransactional
    public Uni<{Entity}Entity> create({Entity}DTO dto) {
        return repository.createEntity(dto);
    }

    @ReactiveTransactional
    public Uni<{Entity}Entity> update({Entity}DTO dto) {
        return repository.updateEntity(dto);
    }

    @ReactiveTransactional
    public Uni<{Entity}Entity> delete({Entity}DTO dto) {
        return repository.deleteEntity(dto);
    }

    public Uni<{Entity}Entity> findById(Long id) {
        return repository.findById(id);
    }
}
```

### 10.5 REST Resource

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

    @POST
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}"})
    public Uni<Response> create({Entity}DTO dto) {
        return service.create(dto)
                .map(entity -> Response.status(Response.Status.CREATED).entity(entity).build());
    }

    @GET
    @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}", "ROLE_VIEWER"})
    public Uni<Response> findById(@PathParam("id") Long id) {
        return service.findById(id)
                .map(entity -> Response.ok(entity).build());
    }

    @PUT
    @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN_UPPER}"})
    public Uni<Response> update({Entity}DTO dto) {
        return service.update(dto)
                .map(entity -> Response.ok(entity).build());
    }

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

## 11. BaseRepository Implementation Guide

> For detailed patterns, diagrams, and edge cases see `EKSAD_SYSTEM_DESIGN_PATTERNS.md`.

### 11.1 Steps to Implement a New Repository

1. Create your entity extending `BaseEntity` — add `tenant_id` field
2. Create your DTO class with Lombok `@Data @Builder @NoArgsConstructor @AllArgsConstructor`
3. Create `{Domain}ModuleType` interface with string constants
4. Extend `BaseRepository<Entity, DTO, ID>`
5. Implement 5 abstract methods: `toId`, `extractDtoId`, `extractTransactionId`, `toNewEntity`, `moduleType`
6. Implement 3 CRUD methods: `createEntity`, `updateEntity`, `deleteEntity` — using `createFlow`, `updateFlow`, `deleteFlow`
7. Inject repository in service, annotate service with `@WithSession`
8. Audit trail fires automatically to RabbitMQ — no additional config needed

### 11.2 Module Type Naming Quick Reference

```
Format: <PROJECT>.<MODULE>.<ACTION>

PROJECT  = EKSAD_SVC_{SERVICE_DOMAIN_UPPER}
MODULE   = domain entity or bounded context (TRANSACTION, ORDER, USER, etc.)
ACTION   = CREATE | UPDATE | DELETE | SUBMIT | APPROVE | REJECT | EXPORT | IMPORT
```

---

## 12. Testing Strategy

### 12.1 Unit Tests (Service Layer)

```java
@ExtendWith(MockitoExtension.class)
class {Entity}ServiceTest {

    @Mock
    {Entity}Repository repository;

    @InjectMocks
    {Entity}Service service;

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

### 12.2 Integration Tests

```java
@QuarkusTest
@TestHTTPEndpoint({Entity}Resource.class)
class {Entity}ResourceTest {

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

### 12.3 Mock UserContext for Tests

```java
// In test resources — override UserContext for tests
@ApplicationScoped
@Priority(1)
@Alternative
public class MockUserContext extends UserContext {
    @Override public String getUser() { return "test-user"; }
    @Override public String getRole() { return "ROLE_ADMIN"; }
}
```

---

## 13. Nexus & Deployment Configuration

### 13.1 `~/.m2/settings.xml` — Nexus Credentials

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

### 13.2 Publish to Nexus

```bash
# Publish SNAPSHOT
mvn clean deploy -DskipTests

# Promote to RELEASE (update version first — remove -SNAPSHOT)
mvn versions:set -DnewVersion=1.0.0
mvn clean deploy -DskipTests -P release
```

### 13.3 Build Native Image (Optional)

```bash
mvn package -Pnative -DskipTests
```

---

## 14. File Storage Integration

> ⚠️ **This section is OPTIONAL.** Include it only if this service requires file upload or attachment functionality. If this service has no file handling requirements, skip this section entirely.

---

### 14.1 Overview

The EKSAD platform centralizes all file operations in a dedicated core service: **`eksad-core-storage`** (`:8090`). No domain service may interact with S3 or Cloudflare R2 directly.

The responsibilities are split clearly:
- **`eksad-core-storage`** — owns the file lifecycle: upload validation, object storage, CDN URL management, and thumbnail generation.
- **Domain service** — stores only a `file_id` (BIGINT) as a lightweight reference to a file record. It never holds any object storage key, bucket path, or CDN URL.

This separation means that if the storage provider changes (e.g., from AWS to Cloudflare), domain services require zero changes.

---

### 14.2 Upload Flow

When a user attaches a file to a domain entity (e.g., a contract document, a profile photo, a report attachment), the upload flow follows these steps:

1. The **client** sends the file directly to `eksad-core-storage` via `POST /api/v1/storage/upload` as a multipart request, including:
   - `file` — the binary file content
   - `visibility` — `PUBLIC` or `PRIVATE` (controls access and URL type)
   - `refEntityType` — the owning domain entity name (e.g., `contract`, `lead`, `submission`)
   - `refEntityId` — the ID of the owning entity in the calling service (can be sent after entity creation as a second step)
2. `eksad-core-storage` validates the MIME type and file size, streams the file to the configured object storage (AWS S3 or Cloudflare R2), persists metadata in its own `file_metadata` PostgreSQL table, and returns a `{ fileId, cdnUrl? }` response. `cdnUrl` is included only for `PUBLIC` files.
3. The **client** passes the returned `fileId` as part of the domain service's create or update request body.
4. The **domain service** stores only the `fileId` value (e.g., in a `{field}_file_id BIGINT` column on its entity).
5. Thumbnail generation runs asynchronously via RabbitMQ (`exc-file-processing` exchange) — it does not block the upload response.

---

### 14.3 URL Resolution at Render-Time

Domain services must **never** cache or store resolved URLs. URLs are always fetched on demand from `eksad-core-storage`:

- **File URL:** `GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/url`
  Returns a permanent CDN URL for `PUBLIC` files, or a short-lived signed URL for `PRIVATE` files (TTL default: 300 seconds).

- **Thumbnail URL:** `GET http://eksad-core-storage:8090/api/v1/storage/{fileId}/thumbnail-url`
  Returns the thumbnail URL (same visibility rules). If thumbnail generation failed or is still pending, falls back gracefully to the original file URL — the frontend always receives a usable URL.

The domain service's response DTO should call these endpoints in the service layer and include the resolved URL as a computed field before returning to the client. Signed URLs must not be stored anywhere and must not be passed along in RabbitMQ events.

---

### 14.4 File Visibility Rules

Every file is classified at upload time and this classification is immutable:

- **`PUBLIC`** — The file is stored in a public-read bucket. A permanent CDN URL is stored in `file_metadata.cdn_url` and returned directly on each URL resolution request. Use for logos, brochures, and non-sensitive images.
- **`PRIVATE`** — The file is stored in a private bucket with no public access. No CDN URL is stored. A signed URL is generated per resolution request and expires after `STORAGE_SIGNED_URL_TTL_SECONDS` (default: 300 seconds). Use for contracts, financial reports, confidential documents.
- **Thumbnail visibility** always inherits from its parent file — a `PRIVATE` file always has a `PRIVATE` thumbnail.

---

### 14.5 Flyway DDL — Storing `file_id` in Domain Tables

When a domain table references a file, add a `file_id` column. This is a logical foreign key by convention only — no database-level `FOREIGN KEY` constraint is created (since `eksad-core-storage` is a separate service with its own database).

```sql
-- Example: adding an attachment column to a domain table
{field_name}_file_id   BIGINT   NULL,   -- FK by convention to eksad-core-storage.file_metadata.id
```

Add an index if the column will be queried:

```sql
CREATE INDEX idx_{table_name}_{field_name}_file_id ON {table_name} ({field_name}_file_id);
```

---

### 14.6 Module Types for File Audit Trail

File operations in `eksad-core-storage` are automatically audited. The module type strings are:

| Action | Module Type String |
|--------|--------------------|
| Upload | `EKSAD_CORE_STORAGE.FILE.UPLOAD` |
| Delete | `EKSAD_CORE_STORAGE.FILE.DELETE` |
| Access audit *(reserved)* | `EKSAD_CORE_STORAGE.FILE.ACCESS` |

Domain services do not need to produce these audit events — `eksad-core-storage` handles them via `BaseRepository` flows automatically.

---

### 14.7 Further Reference

For complete technical detail including the `file_metadata` DDL, `StorageProvider` interface, environment variables, S3 key naming convention, and thumbnail fallback behaviour, see:

> **`EKSAD_SYSTEM_DESIGN_PATTERNS.md` — Section 10: File Storage Pattern**

---

## Appendix — Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `eksad-core-storage :8090` to architecture diagram and service registry; added Design Principle #8 (soft delete) and #9 (file reference by ID only); added optional `STORAGE_*` env block to `application.properties`; added `file_id` comment to entity skeleton; added Section 14 — File Storage Integration |
