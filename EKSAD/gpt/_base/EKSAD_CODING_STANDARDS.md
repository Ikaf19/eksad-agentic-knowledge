# EKSAD Coding Standards & Conventions

**Version:** 1.1
**Date:** 2026-05-23
**Owner:** EKSAD Platform Team
**Status:** 🟢 Active — Mandatory for all EKSAD services
**Audience:** All Backend Developers, Tech Leads, Code Reviewers

> These standards are enforced during code review. All PRs must comply before merge.
> When in doubt, ask the GPT: *"Review this code against EKSAD standards."*

---

## Table of Contents

1. [Technology Stack & Versions](#1-technology-stack--versions)
2. [Package Naming Convention](#2-package-naming-convention)
3. [Project Structure](#3-project-structure)
4. [Entity Design Rules](#4-entity-design-rules)
5. [Repository Pattern (BaseRepository)](#5-repository-pattern-baserepository)
6. [Module Type Naming](#6-module-type-naming)
7. [Timestamp Convention](#7-timestamp-convention)
8. [Financial Value Convention](#8-financial-value-convention)
9. [Soft Delete Convention](#9-soft-delete-convention)
10. [Multi-Tenant Convention](#10-multi-tenant-convention)
11. [API Design Rules](#11-api-design-rules)
12. [Exception Handling](#12-exception-handling)
13. [Audit Trail Rules](#13-audit-trail-rules)
14. [Configuration & Secrets](#14-configuration--secrets)
15. [Testing Standards](#15-testing-standards)
16. [Database (Flyway) Standards](#16-database-flyway-standards)
17. [Reactive Programming Rules](#17-reactive-programming-rules)
18. [Code Review Checklist](#18-code-review-checklist)
19. [Master Data & Cache Sync Standards](#19-master-data--cache-sync-standards)
20. [Tenant-Aware Repository Pattern](#20-tenant-aware-repository-pattern)
21. [Resilience Annotations (MicroProfile Fault Tolerance)](#21-resilience-annotations-microprofile-fault-tolerance)
22. [Health Check Standards](#22-health-check-standards)
23. [Logging Standards](#23-logging-standards)
24. [Observability Standards](#24-observability-standards)
25. [Reserved Field Standards](#25-reserved-field-standards)
26. [Repo & Build Strategy](#26-repo--build-strategy)
27. [Standard Response Wrapper (`GenericResponseDTO`)](#27-standard-response-wrapper-genericresponsedto)
28. [Mapper Rule — Entity/Document Must Never Reach Presentation Layer](#28-mapper-rule--entitydocument-must-never-reach-presentation-layer)
29. [MongoDB Document BSON Naming Rule + Reactive Pagination Pattern](#29-mongodb-document-bson-naming-rule)

---

## 1. Technology Stack & Versions

These versions are **pinned in `eksad-parent`**. Never override per-service without Platform Team approval.

| Technology | Version | Notes |
|------------|---------|-------|
| Java | 21 (LTS) | Use records, sealed classes, text blocks where appropriate |
| Quarkus | 3.30.6 | Platform BOM version — never mix versions across services |
| Hibernate Reactive Panache | Managed by Quarkus BOM | Reactive only — no blocking ORM |
| PostgreSQL Driver | Managed by Quarkus BOM | Reactive PG client |
| Flyway | Managed by Quarkus BOM | All DDL migrations |
| MongoDB Panache | Managed by Quarkus BOM | Audit service only |
| SmallRye JWT | Managed by Quarkus BOM | RS256 validation |
| SmallRye Reactive Messaging | Managed by Quarkus BOM | RabbitMQ integration |
| Lombok | 1.18.32 | Boilerplate reduction |
| MapStruct | 1.5.5.Final | DTO ↔ Entity mapping |
| Micrometer + Prometheus | 1.12.5 | Metrics (where applicable) |
| JUnit 5 | Managed by Quarkus BOM | Test framework |
| Mockito | Managed by Quarkus BOM | Mocking |
| Testcontainers | Managed by Quarkus BOM | Integration test infra |

---

## 2. Package Naming Convention

### 2.1 Standard Package Structure

```
com.eksad.<layer>.<domain>
```

| Project Type | Group ID | Example |
|---|---|---|
| Platform core library | `com.eksad.core` | `com.eksad.core.common`, `com.eksad.core.audittrail` |
| Domain service | `com.eksad.svc.<domain>` | `com.eksad.svc.leads`, `com.eksad.svc.hr` |
| Gateway | `com.eksad.gateway` | `com.eksad.gateway` |
| Auth service | `com.eksad.svc.auth` | `com.eksad.svc.auth` |

### 2.2 Internal Package Layers (per service)

```
com.eksad.svc.{domain}.
  ├── common/
  │   └── constants/       ← Module type string constants
  ├── core/
  │   ├── dto/             ← Request/Response DTOs
  │   ├── mapper/          ← MapStruct mappers
  │   └── service/         ← Business logic layer
  ├── data/
  │   ├── entities/        ← JPA entities (extend BaseEntity)
  │   │   └── base/        ← (do not put custom entities here)
  │   └── repositories/    ← Extend BaseRepository
  └── transport/
      └── resource/        ← JAX-RS REST endpoints
```

### 2.3 Naming Rules

| Element | Convention | Example |
|---------|------------|---------|
| Class | `PascalCase` | `TransactionEntity`, `TransactionService` |
| Interface | `PascalCase`, prefix `I` for explicit interfaces | `CrudFlows`, `ILogActivityService` |
| Method | `camelCase` | `createEntity()`, `findByTenantId()` |
| Field | `camelCase` | `tenantId`, `createdAt` |

---

### 2.4 Service / Artifact Naming Convention

> **Rule:** Use the correct suffix based on the role of the service. Never use `-service` for a shared cross-project core.

| Suffix | Role | Examples |
|--------|------|---------|
| `-core` | Shared cross-project infrastructure service. Consumed by multiple projects (UCMS, HRMS, etc.). | `eksad-core-common`, `eksad-core-audittrail`, `ucms-auth-core` |
| `-service` | Domain service owned by a single project. Contains business logic for a specific domain. | `ucms-usermgmt-service`, `ucms-leads-service`, `ucms-sales-service` |
| `-gateway` | API gateway — JWT validation, routing, CORS, rate limiting only. No business logic. | `ucms-gateway`, `eksad-gateway` |
| `-parent` | Maven BOM — version management only. No Java code. | `eksad-parent`, `ucms-parent` |

**Examples — correct vs wrong:**

| ✅ Correct | ❌ Wrong | Reason |
|---|---|---|
| `ucms-auth-core` | `ucms-auth-service` | Auth is a shared cross-project credential store — it's a core, not a domain service |
| `eksad-core-audittrail` | `eksad-audit-service` | Audit is cross-project platform infrastructure |
| `ucms-leads-service` | `ucms-leads-core` | Leads is a UCMS-specific domain — not shared across projects |
| Constant | `UPPER_SNAKE_CASE` | `EKSAD_SVC_LEADS.TRANSACTION.CREATE` |
| DB Column | `snake_case` | `tenant_id`, `created_at` |
| DB Table | `snake_case`, plural | `transactions`, `audit_logs` |
| Flyway file | `V{N}__{snake_case_description}.sql` | `V1__init_transactions.sql` |
| Env variable | `UPPER_SNAKE_CASE` | `RABBITMQ_HOST`, `DB_PASSWORD` |
| Maven artifact | `kebab-case` | `eksad-svc-leads`, `eksad-core-common` |

---

## 3. Project Structure

Every EKSAD service MUST follow this exact structure:

```
{service-name}/
├── pom.xml                              ← parent = eksad-parent
├── README.md                            ← setup + run instructions
├── docker-compose.yml                   ← local dev infra
└── src/
    ├── main/
    │   ├── java/com/eksad/svc/{domain}/
    │   │   ├── common/constants/        ← module type strings
    │   │   ├── core/dto/                ← DTOs
    │   │   ├── core/mapper/             ← MapStruct mappers
    │   │   ├── core/service/            ← @ApplicationScoped services
    │   │   ├── data/entities/           ← JPA entities
    │   │   ├── data/entities/base/      ← (inherited from eksad-core-common)
    │   │   ├── data/repositories/       ← extends BaseRepository
    │   │   └── transport/resource/      ← JAX-RS resources
    │   └── resources/
    │       ├── application.properties
    │       └── db/migration/
    │           └── V1__init_{domain}.sql
    └── test/
        └── java/com/eksad/svc/{domain}/
            ├── {Entity}ServiceTest.java
            └── {Entity}ResourceTest.java
```

---

## 4. Entity Design Rules

### ✅ Required

```java
@Data
@SuperBuilder                // ← MUST use SuperBuilder (not @Builder) for inheritance
@NoArgsConstructor
@Entity
@Table(name = "{table_name}")
public class {Entity}Entity extends BaseEntity {  // ← MUST extend BaseEntity

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "tenant_id", nullable = false)  // ← MUST have tenant_id
    private String tenantId;

    // Domain fields ...
}
```

### ❌ Forbidden

| Rule | Reason |
|------|--------|
| `extends BaseEntity` without `@SuperBuilder` | `@Builder` breaks inheritance; `@SuperBuilder` is required |
| Missing `tenant_id` column | Data isolation failure — all tenants see each other's data |
| `String` for financial amounts | Use `BigDecimal` |
| `Date` or `LocalDateTime` for timestamps | Use `Long` (epoch ms). See Section 7 |
| No `@Column(nullable = false)` on required fields | Silent null insertions |

---

## 5. Repository Pattern (BaseRepository)

### ✅ Required Pattern

```java
@ApplicationScoped
public class {Entity}Repository extends BaseRepository<{Entity}Entity, {Entity}DTO, Long> {

    // Implement ALL 5 abstract methods
    @Override public String moduleType() { ... }
    @Override public Long toId({Entity}DTO dto) { ... }
    @Override public String extractDtoId({Entity}DTO dto) { ... }
    @Override public String extractTransactionId({Entity}Entity entity) { ... }
    @Override public {Entity}Entity toNewEntity({Entity}DTO dto, Object... extras) { ... }

    // Implement 3 CRUD methods using flow methods
    @Override public Uni<{Entity}Entity> createEntity({Entity}DTO dto) {
        return createFlow(dto, {Domain}ModuleType.ENTITY.CREATE);
    }
    @Override public Uni<{Entity}Entity> updateEntity({Entity}DTO dto) {
        return updateFlow(dto, {Domain}ModuleType.ENTITY.UPDATE, guard, errorFn, mutator);
    }
    @Override public Uni<{Entity}Entity> deleteEntity({Entity}DTO dto) {
        return deleteFlow(dto, {Domain}ModuleType.ENTITY.DELETE, softDeleteMutator());
    }
}
```

### `UserContextProvider` — Mandatory Injection Pattern

> **Rule:** Never parse JWT statically inside a repository or service. Always inject `UserContextProvider` as a CDI bean so it is mockable in unit tests.

```java
// ✅ Correct — inject UserContextProvider from eksad-core-common
@ApplicationScoped
public class OrderRepository extends BaseRepository<OrderEntity, OrderDTO, Long> {

    @Inject
    UserContextProvider userContext;   // ← injected, not static

    @Override
    public OrderEntity toNewEntity(OrderDTO dto, Object... extras) {
        return OrderEntity.builder()
            .tenantId(userContext.get().getTenantId())   // ← from CDI bean
            .createdBy(userContext.get().getUsername())
            .createdAt(Instant.now().toEpochMilli())
            .build();
    }
}

// ✅ UserContext record (from eksad-core-common)
public record UserContext(
    String tenantId,
    String userId,
    String username,
    String role,
    String companyId
) {}

// ✅ UserContextProvider — populated from @Context SecurityContext / JWT
@RequestScoped
public class UserContextProvider {
    @Inject JsonWebToken jwt;

    public UserContext get() {
        return new UserContext(
            jwt.getClaim("tenant_id"),
            jwt.getClaim("user_id"),
            jwt.getName(),             // sub claim
            jwt.getClaim("role"),
            jwt.getClaim("company_id")
        );
    }
}

// ❌ Forbidden — static JWT parsing inside repository
SecurityContext.getCurrentUser().getTenantId()   // ❌ not mockable
jwt.getClaim(...)                                // ❌ direct in repository
```

### ❌ Forbidden

| Rule | Reason |
|------|--------|
| Calling `persist()` directly without a flow method | Bypasses audit trail |
| Business logic inside repository | Business logic belongs in Service layer |
| `@Transactional` on repository | Use `@ReactiveTransactional` on Service instead |
| Manual `LogActivityDTO` construction | Always use `LogHandler` via flow methods |
| Static JWT parse in repository/service | Not mockable in unit tests — use `UserContextProvider` |

---

## 6. Module Type Naming

### Format
```
<PROJECT>.<MODULE>.<ACTION>

PROJECT  = EKSAD_SVC_{DOMAIN_UPPER}  (e.g., EKSAD_SVC_LEADS)
MODULE   = UPPER_SNAKE_CASE           (e.g., TRANSACTION, ORDER)
ACTION   = UPPER_SNAKE_CASE verb      (e.g., CREATE, UPDATE, DELETE, SUBMIT, APPROVE, REJECT)
```

### Implementation

```java
// ✅ Correct — String constants interface (extensible, no enum limitation)
public interface TransactionModuleType {
    String PREFIX = "EKSAD_SVC_LEADS";
    interface TRANSACTION {
        String CREATE  = PREFIX + ".TRANSACTION.CREATE";
        String UPDATE  = PREFIX + ".TRANSACTION.UPDATE";
        String DELETE  = PREFIX + ".TRANSACTION.DELETE";
    }
}

// ❌ Wrong — enum (can't be extended by other modules)
public enum TransactionModuleType { CREATE, UPDATE, DELETE }
```

---

## 7. Timestamp Convention

### Decision: `Long` (epoch milliseconds) ✅

**Why `Long` over `Instant` or `LocalDateTime` in entities:**

| Criterion | `Long` (epoch ms) | `Instant` | `LocalDateTime` |
|-----------|------------------|-----------|-----------------|
| DB indexing | ✅ `BIGINT` B-tree — fastest | ⚠️ `TIMESTAMPTZ` — good | ⚠️ `TIMESTAMP` — no timezone |
| Timezone issues | ✅ None (UTC by definition) | ✅ None | ❌ Ambiguous |
| JSON serialization | ✅ Plain number | ⚠️ ISO string | ❌ Varies by config |
| Cross-language | ✅ Universal | ⚠️ Needs parsing | ❌ Java-specific format |
| Range query in DB | ✅ Simple `WHERE > 1745280000000` | ✅ Works | ✅ Works |
| Human readability | ⚠️ Not human-readable | ✅ ISO string | ✅ ISO string |

**Verdict:** `Long` epoch ms for all DB entity timestamps. Use `Instant` for Java business logic calculations, convert to `Long` before storing.

### Implementation Rules

```java
// ✅ In entity (DB layer) — always Long
@Column(name = "created_at", nullable = false)
private Long createdAt;    // BIGINT in DB

// ✅ In toNewEntity() — convert from Instant to Long
.createdAt(Instant.now().toEpochMilli())

// ✅ In business logic (Java only, not persisted) — use Instant
Instant now = Instant.now();
if (Instant.ofEpochMilli(entity.getCreatedAt()).isBefore(now.minus(30, DAYS))) { ... }

// ❌ Never store Date or LocalDateTime in entities
private Date createdAt;           // ❌
private LocalDateTime createdAt;  // ❌
private Instant createdAt;        // ❌ (for DB columns)
```

---

## 8. Financial Value Convention

**Rule: PostgreSQL `NUMERIC(20,4)` → Java `BigDecimal`. ALWAYS. No exceptions.**

```java
// ✅ Correct
@Column(name = "amount", precision = 20, scale = 4, nullable = false)
private BigDecimal amount;

// ❌ All of these are forbidden for financial values
private Double amount;    // ❌ floating-point precision errors
private Float amount;     // ❌ worse precision
private String amount;    // ❌ runtime cast failures, no DB constraints
private Long amount;      // ❌ loses decimal precision
```

**SQL:**
```sql
-- ✅ Correct
amount NUMERIC(20,4) NOT NULL DEFAULT 0.0000

-- ❌ Forbidden
amount FLOAT
amount VARCHAR(50)
```

---

## 9. Soft Delete Convention

**Rule: NEVER hard-delete. Always soft-delete using `BaseEntity` fields.**

```java
// ✅ Correct — use softDeleteMutator() from BaseRepository
@Override
public Uni<OrderEntity> deleteEntity(OrderDTO dto) {
    return deleteFlow(dto, OrderModuleType.ORDER.DELETE, softDeleteMutator());
}
// softDeleteMutator() sets deletedAt = Instant.now().toEpochMilli() and deletedBy = currentUser()

// ✅ Active records query — always filter deleted
// Panache: add @Filter in entity or use explicit WHERE in custom queries
.where("deletedAt IS NULL AND tenantId = ?1", tenantId)

// ❌ Forbidden
entity.delete();                // hard delete
repository.deleteById(id);      // hard delete
```

---

## 10. Multi-Tenant Convention

**Rule: Every entity MUST have `tenant_id`. Every query MUST filter by `tenant_id`.**

```java
// ✅ In toNewEntity() — always set tenantId from JWT
.tenantId(getUserContext().getTenantId())

// ✅ In custom queries — always include tenant_id filter
return find("tenantId = ?1 AND deletedAt IS NULL", getUserContext().getTenantId())
         .list();

// ❌ Forbidden
return findAll().list();   // ❌ returns all tenants' data
return findById(id);       // ❌ no tenant check — use findById + tenant validation
```

---

## 11. API Design Rules

```java
// ✅ Correct REST resource
@Path("/api/v1/{resource}")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class {Entity}Resource {

    // ✅ Always annotate with @RolesAllowed — never omit auth
    @POST
    @RolesAllowed({"ROLE_ADMIN", "ROLE_{DOMAIN}"})
    public Uni<Response> create({Entity}DTO dto) { ... }

    // ✅ Return Uni<Response> — not entity directly
    // ✅ Use Response.Status constants — not magic numbers
    .map(entity -> Response.status(Response.Status.CREATED).entity(entity).build())
}
```

| Rule | Correct | Wrong |
|------|---------|-------|
| Return type | `Uni<Response>` | `{Entity}Entity` directly |
| Auth | `@RolesAllowed` always | No annotation (open endpoint) |
| HTTP status for create | `201 Created` | `200 OK` |
| HTTP status for not found | `404` via `ValidationException` | Return `null` |
| Credentials in URL | Never | `?password=xxx` |
| API version in path | `/api/v1/...` | `/api/...` |

---

## 12. Exception Handling

```java
// ✅ Business rule violations — use ValidationException (from eksad-core-common)
// This produces HTTP 422 Unprocessable Entity
throw new ValidationException("Order must be in SUBMITTED state to approve");

// ✅ Inside CrudFlows — guard failures auto-produce ValidationException
.onItem().ifNull().switchTo(() -> logHandler.logFailure(log, "Data not found"))

// ❌ Never throw raw RuntimeException for business errors
throw new RuntimeException("not found");   // ❌

// ❌ Never swallow exceptions silently
} catch (Exception e) { }   // ❌
```

---

## 13. Audit Trail Rules

| Rule | Description |
|------|-------------|
| All CRUD via flow methods | `createFlow`, `updateFlow`, `deleteFlow`, `commandFlow` |
| Never call `persist()` directly | Always go through a flow method to ensure audit is captured |
| Never build `LogActivityDTO` manually | `LogHandler.buildBaseLog()` is called automatically inside flows |
| Module type string required | Every `createFlow` / `updateFlow` call must pass a module type string |
| Fire-and-forget is intentional | Audit failures must NOT block main business operation |
| `dataBefore` is captured automatically | `updateFlow` captures entity state before mutation |

---

## 14. Configuration & Secrets

```properties
# ✅ Correct — always use environment variables for secrets
quarkus.datasource.password=${DB_PASSWORD}
rabbitmq-password=${RABBITMQ_PASSWORD}

# ❌ Never hard-code secrets in committed files
quarkus.datasource.password=mypassword123   # ❌
```

| Rule | Description |
|------|-------------|
| No secrets in `application.properties` | Use `${ENV_VAR}` — actual values come from environment or secrets manager |
| Default values allowed for non-sensitive config | `quarkus.http.port=${PORT:8080}` — port has a safe default |
| Never commit `.env` files with real secrets | Add to `.gitignore` |
| JWT private key | Never in source code — mount from secrets vault at deploy time |
| `ddl-auto` in production | Always `none` — never `update` or `create` |

---

## 15. Testing Standards

### Required Tests

| Type | Coverage Target | Tools |
|------|----------------|-------|
| Unit tests (service layer) | ≥ 70% | JUnit 5 + Mockito |
| Integration tests (resource layer) | Key endpoints | `@QuarkusTest` + Rest Assured |

### Conventions

```java
// ✅ Unit test — mock repository, test service logic
@ExtendWith(MockitoExtension.class)
class TransactionServiceTest {
    @Mock TransactionRepository repository;
    @InjectMocks TransactionService service;

    @Test
    @DisplayName("create should return saved entity")
    void create_shouldReturnEntity() { ... }
}

// ✅ Integration test naming — methodName_scenario_expectedResult
void create_withValidDto_shouldReturn201() { ... }
void create_withMissingTenantId_shouldReturn401() { ... }
void update_withDeletedEntity_shouldReturn422() { ... }
```

---

## 16. Database (Flyway) Standards

```sql
-- ✅ File naming: V{N}__{snake_case}.sql
-- V1__init_transactions.sql

-- ✅ Always use IF NOT EXISTS
CREATE TABLE IF NOT EXISTS transactions ( ... );

-- ✅ Always include BaseEntity columns on EVERY table
created_at    BIGINT          NOT NULL,
created_by    VARCHAR(100)    NOT NULL,
updated_at    BIGINT,
updated_by    VARCHAR(100),
deleted_at    BIGINT,
deleted_by    VARCHAR(100),

-- ✅ Always include tenant_id on EVERY table
tenant_id     VARCHAR(100)    NOT NULL,

-- ✅ Create index on tenant_id (and deleted_at, created_at) on EVERY table
CREATE INDEX idx_{table}_tenant_id   ON {table} (tenant_id);
CREATE INDEX idx_{table}_deleted_at  ON {table} (deleted_at);
CREATE INDEX idx_{table}_created_at  ON {table} (created_at);
```

| Rule | Description |
|------|-------------|
| Never edit committed migration files | Create a new version instead |
| `V` prefix required | Flyway won't pick up files without `V` prefix |
| Double underscore separator | `V1__description.sql` — not `V1_description.sql` |
| No raw DDL in application startup | Only Flyway manages schema in production |

---

## 17. Reactive Programming Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| Transaction scope | `@ReactiveTransactional` on service method | On repository method |
| Session scope | `@WithSession` on service class | On repository class |
| Blocking in event loop | Use `Uni.createFrom().item(...)` for sync work | `Thread.sleep()`, blocking I/O |
| ThreadLocal in reactive chain | Avoid — use `@RequestScoped` CDI or Vert.x context | `ThreadLocal` across `flatMap` chains |
| Error propagation | `onFailure().invoke(...)` or `switchTo(logFailure(...))` | Silent catch blocks |
| Return from REST resource | `Uni<Response>` | Blocking `Response` |

---

## 18. Code Review Checklist

Use this checklist for every PR:

### Entity & Repository
- [ ] Entity extends `BaseEntity`
- [ ] Entity has `tenant_id` field with `nullable = false`
- [ ] Entity uses `@SuperBuilder` (not `@Builder`)
- [ ] Financial fields use `BigDecimal` (`NUMERIC(20,4)` in DB)
- [ ] Timestamps use `Long` (epoch ms)
- [ ] Repository extends `BaseRepository`
- [ ] All 5 abstract methods implemented
- [ ] CRUD uses `createFlow` / `updateFlow` / `deleteFlow` (not raw `persist`)
- [ ] Module type string follows `<PROJECT>.<MODULE>.<ACTION>` format

### API & Auth
- [ ] All endpoints have `@RolesAllowed`
- [ ] No endpoint missing authentication
- [ ] Response uses `Uni<Response>` with correct HTTP status
- [ ] No entity exposed directly (use DTO)
- [ ] API versioned: `/api/v{N}/...`

### Configuration
- [ ] No hardcoded secrets in `application.properties`
- [ ] `ddl-auto` is `none` (not `update`)
- [ ] Flyway migration file follows `V{N}__{description}.sql` naming
- [ ] Flyway migration includes `tenant_id`, `created_at`, `deleted_at` columns

### Multi-Tenant
- [ ] `tenantId` set from `getUserContext().getTenantId()` in `toNewEntity()`
- [ ] Custom queries filter by `tenantId`
- [ ] No cross-tenant data leakage possible

### Tests
- [ ] Unit tests for service layer
- [ ] Key integration test for main happy path
- [ ] Failure scenarios tested (not found, wrong state, unauthorized)

### Master Data & Cache Sync
- [ ] Master data entities are owned only by `svc-master-data`
- [ ] Domain entities store only reference IDs (e.g., `brand_id`, `department_id`)
- [ ] Cache tables use `PanacheRepositoryBase` (NOT `BaseRepository`)
- [ ] Cache tables include `last_synced_at BIGINT NOT NULL`
- [ ] Stale events (`occurredAt ≤ last_synced_at`) are skipped
- [ ] Domain service has a startup sync job for empty cache
- [ ] RabbitMQ consumer uses topic exchange `exc-{domain}-master-data`
- [ ] Routing keys follow `r.{entity}.{action}` pattern

### Multi-Tenancy
- [ ] Every repository method filters by `tenant_id` from `TenantContext`
- [ ] `TenantAwareRepository.findById(id)` is FORBIDDEN — use `findByIdAndTenant(id, tenantId)`
- [ ] Every entity test sets `TenantContext` before data operations
- [ ] Tenant isolation check included in every repository integration test
- [ ] Materialized path computed automatically (never set manually)

### Security
- [ ] New endpoints have `@RolesAllowed` annotation
- [ ] JWT claims extracted via injected `JsonWebToken` (not manual parsing)
- [ ] Sensitive data NOT in JWT claims (passwords, PII details)
- [ ] Rate limiting configured for public-facing endpoints

### Resilience
- [ ] All external REST calls have `@Timeout` (max 5s default)
- [ ] `@Retry` configured with `abortOn` for 4xx errors
- [ ] `@CircuitBreaker` on external service clients (Sprint 2+)
- [ ] `@Fallback` returns cached/safe default (NOT for security-critical ops)
- [ ] RabbitMQ consumer has DLQ configured

### Observability
- [ ] Structured JSON logging — NO `System.out.println` or string concatenation in logs
- [ ] Correlation ID propagated to downstream calls (REST + RabbitMQ)
- [ ] Sensitive data NOT logged (passwords, tokens, PII in plain text)
- [ ] Custom business metrics registered for key operations
- [ ] Health check covers all external dependencies (DB, RabbitMQ, core-auth JWKS)

### Reserved Fields
- [ ] Transactional entities that opt-in extend `BaseTransactionalEntity`
- [ ] 13 reserved field columns present (5 string + 3 numeric + 2 date + 2 boolean + 1 JSONB)
- [ ] `ReservedFieldValidator` invoked at create/update boundary
- [ ] Reserved field config resolution uses tenant → domain → global cascade
- [ ] DTO ↔ Entity mapping uses MapStruct — no hand-rolled mappers
- [ ] Null-handling matches HTTP verb (POST/PUT overwrite with `NULL`; PATCH ignores `null` via `NullValuePropertyMappingStrategy.IGNORE`)
- [ ] Flyway migration follows `V{N}__add_reserved_fields_to_{table}.sql` template (`EKSAD_RESERVED_FIELD_PATTERNS.md` §13)
- [ ] Per-tenant indexes follow naming `idx_<table>_<tenant-slug>_<purpose>`

---

## 19. Master Data & Cache Sync Standards

> Implements **Principle #10 (Right DB for right job)**, **Principle #11 (Master data via dedicated service)**, and **Principle #12 (Denormalized cache via events)** from `EKSAD_BASE_PRINCIPLES.md`. Full pattern reference: `EKSAD_MASTER_DATA_PATTERNS.md` and `EKSAD_CACHE_SYNC_PATTERNS.md`.

### 19.1 Master Data Service Ownership

- All shared catalog/reference entities live in `svc-master-data` per business domain.
- See `EKSAD_DOMAIN_REGISTRY.md` for which entities are master data per domain.
- Domain services NEVER create or modify master data — only consume events.

### 19.2 Cache Table Standards (Domain Services)

```sql
CREATE TABLE brand_cache (
    id              BIGINT       PRIMARY KEY,             -- same ID as master
    tenant_id       VARCHAR(100) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50),
    last_synced_at  BIGINT       NOT NULL,                -- event ordering
    PRIMARY KEY (id)
);
CREATE INDEX idx_brand_cache_tenant ON brand_cache (tenant_id);
```

| Rule | Detail |
|------|--------|
| ❌ Do NOT extend `BaseEntity` | Cache tables have no audit columns |
| ❌ Do NOT use `BaseRepository` | Use `PanacheRepositoryBase` |
| ❌ Do NOT use soft delete | Cache rows are upserted or hard-deleted |
| ✅ Include `last_synced_at` | For stale event detection |
| ✅ Include `tenant_id` | Always |

### 19.3 Event Consumer Pattern

```properties
mp.messaging.incoming.master-data-events.connector=smallrye-rabbitmq
mp.messaging.incoming.master-data-events.exchange.name=exc-master-data
mp.messaging.incoming.master-data-events.exchange.type=topic
mp.messaging.incoming.master-data-events.queue.name=q-master-sync-{service}
mp.messaging.incoming.master-data-events.routing-keys=r.brand.*,r.model.*,r.type.*
```

Consumer must:
- Skip events where `occurredAt ≤ last_synced_at`
- Log + skip unknown event types (do NOT throw)
- Use upsert pattern (insert or update)

### 19.4 Startup Sync

Every domain service consuming master data MUST implement a startup sync that calls `svc-master-data` REST API if cache is empty.

> Full guide: `EKSAD_CACHE_SYNC_PATTERNS.md`.

### 19.5 Master Data Event Publishing (svc-master-data only)

> **Scope:** This subsection applies **only to `svc-master-data`** (the source of truth).
> Domain services NEVER publish to `exc-master-data` — they only consume.

After every `createFlow` / `updateFlow` / `deleteFlow` on a master data entity, `svc-master-data` MUST publish a domain event to the topic exchange `exc-{domain}-master-data` (e.g., `exc-master-data` for Automotive, `exc-hris-master-data` for HRIS).

#### Event Envelope (canonical schema)

```json
{
  "eventType":  "BRAND_CREATED",          // <ENTITY>_<ACTION_PAST_TENSE>
  "eventId":    "550e8400-e29b-41d4-a716-446655440000",   // UUID v4, unique per emission
  "tenantId":   "tenant-astra",           // from UserContext.getTenantId()
  "occurredAt": 1716530400123,            // epoch ms — used by consumers to skip stale events
  "payload":    { /* full entity state (post-change) */ }
}
```

| Field | Rule |
|-------|------|
| `eventType` | `<ENTITY>_<ACTION>` — `BRAND_CREATED`, `MODEL_UPDATED`, `BRAND_DELETED`. Past tense. UPPER_SNAKE_CASE. |
| `eventId` | UUID v4 — required for consumer idempotency (dedup key). |
| `tenantId` | ALWAYS present. Sourced from `UserContext.getTenantId()`. |
| `occurredAt` | Epoch ms at publish time — `Instant.now().toEpochMilli()`. Used by consumers for stale-event detection. |
| `payload` | **Full** post-change entity snapshot (not a diff). Consumers must be able to rebuild cache row from payload alone. |

#### Routing Key Convention

| Pattern | Example |
|---------|---------|
| `r.{entity}.{action}` | `r.brand.created`, `r.brand.updated`, `r.brand.deleted`, `r.model.created`, `r.type.updated` |

- Entity = singular lowercase (`brand`, not `brands`).
- Action = past tense lowercase (`created` / `updated` / `deleted`).
- Consumers subscribe via wildcard: `r.brand.*` or `r.*.*`.

#### MutinyEmitter Pattern (Repository helper)

```java
@ApplicationScoped
public class BrandRepository extends BaseRepository<Brand, BrandDTO, Long> {

    @Inject
    @Channel("master-data-out")                          // declared in application.properties
    MutinyEmitter<Map<String, Object>> emitter;

    @Inject UserContext userContext;

    @Override public Long toId(Brand e) { return e.getId(); }
    @Override public Long extractDtoId(BrandDTO dto) { return dto.getId(); }
    @Override public Long extractTransactionId(BrandDTO dto) { return dto.getTransactionId(); }
    @Override public String moduleType() { return MasterDataModuleType.BRAND.CREATE; }

    @Override
    public Brand toNewEntity(BrandDTO dto) {
        return Brand.builder()
            .tenantId(userContext.getTenantId())
            .createdAt(Instant.now().toEpochMilli())
            .name(dto.getName())
            .build();
    }

    public Uni<Brand> create(BrandDTO dto) {
        return createFlow(dto, MasterDataModuleType.BRAND.CREATE)
            .invoke(entity -> publishEvent("BRAND_CREATED", "r.brand.created", entity));
    }

    public Uni<Brand> update(BrandDTO dto) {
        return updateFlow(dto, MasterDataModuleType.BRAND.UPDATE,
                e -> e.getId().equals(dto.getId()),
                () -> new WebApplicationException("Brand not found", 404),
                (existing, d) -> existing.setName(d.getName()))
            .invoke(entity -> publishEvent("BRAND_UPDATED", "r.brand.updated", entity));
    }

    public Uni<Void> delete(BrandDTO dto) {
        return deleteFlow(dto, MasterDataModuleType.BRAND.DELETE, softDeleteMutator())
            .invoke(v -> publishEvent("BRAND_DELETED", "r.brand.deleted",
                Brand.builder().id(dto.getId()).tenantId(userContext.getTenantId()).build()));
    }

    /**
     * Fire-and-forget publish to exc-master-data.
     * MUST NOT block the reactive chain — same pattern as audit trail (LogHandler).
     * Failure to publish is logged but does NOT roll back the DB transaction
     * (consumers reconcile via startup sync — see §19.4).
     */
    private void publishEvent(String eventType, String routingKey, Brand entity) {
        Map<String, Object> envelope = Map.of(
            "eventType",  eventType,
            "eventId",    UUID.randomUUID().toString(),
            "tenantId",   entity.getTenantId(),
            "occurredAt", Instant.now().toEpochMilli(),
            "payload",    entity                                 // serialized via JSON-B
        );
        Message<Map<String, Object>> msg = Message.of(envelope)
            .addMetadata(OutgoingRabbitMQMetadata.builder()
                .withRoutingKey(routingKey)
                .withDeliveryMode(2)                             // persistent
                .build());
        emitter.sendMessageAndForget(msg);                       // fire-and-forget
    }
}
```

#### application.properties (publisher side)

```properties
mp.messaging.outgoing.master-data-out.connector=smallrye-rabbitmq
mp.messaging.outgoing.master-data-out.exchange.name=exc-master-data
mp.messaging.outgoing.master-data-out.exchange.type=topic
mp.messaging.outgoing.master-data-out.exchange.durable=true
mp.messaging.outgoing.master-data-out.default-routing-key=r.unknown.unknown
```

#### Rules

| Rule | Detail |
|------|--------|
| ✅ Fire-and-forget | Same as audit trail — never `await()` on emitter. Use `.invoke(...)` after `createFlow`. |
| ✅ Full payload | Payload contains the **entire** post-change entity, not a delta. |
| ✅ Envelope mandatory fields | `eventType`, `eventId`, `tenantId`, `occurredAt`, `payload` — all 5 always present. |
| ✅ Publish AFTER persist | Event emission happens inside `.invoke(...)` chained after `createFlow`/`updateFlow`/`deleteFlow` (entity already persisted with ID). |
| ❌ Never publish on validation failure | If `CrudFlows` guard rejects, no event is fired (the `.invoke` never runs). |
| ❌ Never block | No `Uni.await()` / `Thread.sleep()` / synchronous emit. |
| ❌ Never publish from domain services | Only `svc-master-data` writes to `exc-master-data`. |

> Full pattern reference (consumer side cache repository, multi-domain exchange naming, batch backfill): `EKSAD_MASTER_DATA_PATTERNS.md` and `EKSAD_CACHE_SYNC_PATTERNS.md`.

---

## 20. Tenant-Aware Repository Pattern

### 20.1 `TenantAwareRepository<E, I>` Base Class

```java
public abstract class TenantAwareRepository<E extends BaseEntity, I> {

    @Inject TenantContext tenantContext;

    public Uni<E> findByIdAndTenant(I id, String tenantId) { /* impl */ }

    public final Uni<E> findById(I id) {
        throw new TenantContextMissingException(
            "Use findByIdAndTenant(id, tenantId) — direct findById is forbidden");
    }

    public Uni<List<E>> findAllByTenant(String tenantId, Filter f) { /* impl */ }

    public Uni<E> save(E entity) {
        if (entity.getTenantId() == null) {
            entity.setTenantId(tenantContext.getTenantId());
        }
        return persist(entity);
    }
}
```

### 20.2 Mandatory Rules

- Every entity MUST be queried via `TenantAwareRepository`.
- Direct `findById(id)` is **forbidden** — throws `TenantContextMissingException`.
- `save()` auto-sets `tenant_id` from `TenantContext` if not present.
- Every PostgreSQL table has index on `(tenant_id, ...)`.
- Every MongoDB collection has compound index `{ tenant_id: 1, ... }`.

### 20.3 Scope-Based Queries

| JWT scope | Filter applied |
|-----------|----------------|
| `tenant` | `tenant_id = :tenantId` |
| `group` | `path LIKE :parentPath || '%'` |
| `platform` | No filter (all data) |

> Full guide: `EKSAD_MULTI_TENANCY_PATTERNS.md`.

---

## 21. Resilience Annotations (MicroProfile Fault Tolerance)

### 21.1 Mandatory `@Timeout`

```java
@RegisterRestClient(configKey = "master-data")
public interface MasterDataRestClient {

    @GET @Path("/brands")
    @Timeout(value = 5000)             // MANDATORY — every external call
    List<BrandDTO> listBrands();
}
```

### 21.2 `@Retry` (Sprint 2+)

```java
@Retry(
    maxRetries = 3,
    delay      = 1000,
    jitter     = 200,
    retryOn    = { ConnectException.class, TimeoutException.class },
    abortOn    = { BadRequestException.class, NotFoundException.class }
)
public List<BrandDTO> listBrands() { ... }
```

### 21.3 `@CircuitBreaker` + `@Fallback` (Sprint 2+)

```java
@CircuitBreaker(requestVolumeThreshold = 10, failureRatio = 0.5, delay = 10000)
@Fallback(fallbackMethod = "fallbackBrands")
public List<BrandDTO> listBrands() { ... }

public List<BrandDTO> fallbackBrands() {
    return brandCacheRepository.listAll().stream().map(this::toDTO).toList();
}
```

> ⚠️ NEVER use `@Fallback` for security-critical ops (auth, permission checks).

> Full guide: `EKSAD_RESILIENCE_PATTERNS.md`.

---

## 22. Health Check Standards

### 22.1 Built-in Endpoints
- `/q/health/live` — process alive
- `/q/health/ready` — accepts traffic (must verify all deps)
- `/q/health/started` — startup complete

### 22.2 Custom Health Check Template

```java
@Readiness
@ApplicationScoped
public class JwksReachableCheck implements HealthCheck {
    @Inject @RestClient JwksClient jwks;

    @Override
    public HealthCheckResponse call() {
        try {
            jwks.get();
            return HealthCheckResponse.up("jwks");
        } catch (Exception e) {
            return HealthCheckResponse.down("jwks");
        }
    }
}
```

Required custom checks per service:
- Database connection
- RabbitMQ broker reachable
- Cache freshness (`last_synced_at` within window)
- `eksad-core-auth` JWKS reachable

> Full guide: `EKSAD_OBSERVABILITY_PATTERNS.md` Section 11.

---

## 23. Logging Standards

### 23.1 Structured JSON Logging (Production)

```properties
%prod.quarkus.log.console.json=true
%dev.quarkus.log.console.json=false
```

### 23.2 Mandatory MDC Fields

| Field | Source |
|-------|--------|
| `correlation_id` | From `X-Correlation-ID` header or generated |
| `tenant_id` | From JWT claim |
| `service_name` | From env var `EKSAD_SERVICE_NAME` |
| `user_ref` | From JWT subject (if authenticated) |

### 23.3 Log Levels

| Level | Use for |
|-------|---------|
| `ERROR` | Unexpected failures requiring attention |
| `WARN` | Recoverable issues (circuit open, retry, stale event) |
| `INFO` | Business events (entity created, login success) |
| `DEBUG` | Technical detail (SQL, payloads) |

### 23.4 Never Log

- ❌ Passwords, tokens, API keys
- ❌ PII in plain text (full name + ID combinations)
- ❌ Full stack traces at INFO

### 23.5 Correlation ID Propagation

Implement `CorrelationIdFilter` (server) + `CorrelationIdClientFilter` (REST client) + RabbitMQ envelope header.

---

### 23.6 Logger Declaration — Lombok Annotations (Mandatory)

EKSAD uses Lombok logging annotations to eliminate manual logger boilerplate.
Choose the annotation based on framework — both generate a `log` field (lowercase).

| Framework | Lombok Annotation | Generated Logger | Extra dependency |
|---|---|---|---|
| **Quarkus** | `@JBossLog` | `org.jboss.logging.Logger` | None — built into `quarkus-core` |
| **Spring Boot** | `@Slf4j` | `org.slf4j.Logger` | None — built into `spring-boot-starter` |

Lombok version pinned in `eksad-parent`: **1.18.34** — `@JBossLog` supported since Lombok 1.14.

```java
// ✅ Quarkus service — @JBossLog (Lombok generates JBoss Logger natively)
@JBossLog
@ApplicationScoped
public class MyService {
    public void doSomething() {
        log.infof("Entity created: id=%s, tenant=%s", id, tenantId);  // printf-style (JBoss)
        log.warnf("Recoverable issue: %s", reason);
        log.errorf("Unexpected failure: %s", ex.getMessage());
    }
}

// ✅ Spring Boot service — @Slf4j (Lombok generates SLF4J Logger)
@Slf4j
@Service
public class MyService {
    public void doSomething() {
        log.info("Entity created: id={}, tenant={}", id, tenantId);   // {} placeholder (SLF4J)
    }
}

// ❌ Forbidden — manual declaration (replaced by Lombok annotation)
private static final Logger LOG = Logger.getLogger(MyService.class);

// ❌ Forbidden — @Slf4j in Quarkus (unnecessary SLF4J abstraction over JBoss)
@Slf4j
@ApplicationScoped
public class MyService { ... }
```

> **Why `@JBossLog` for Quarkus?** `org.jboss.logging.Logger` is Quarkus' native logger — built into `quarkus-core`, zero extra dependency, full GraalVM native image support, and integrates directly with `quarkus.log.*` properties. SLF4J works in Quarkus via an automatic bridge (`slf4j-jboss-logmanager`) but adds an unnecessary abstraction layer.
>
> **Format difference:** JBoss Logger uses `%s` printf-style (`log.infof("id=%s", id)`). SLF4J uses `{}` placeholders (`log.info("id={}", id)`). Do not mix.

---

## 24. Observability Standards

### 24.1 Mandatory Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/q/health/live` `/q/health/ready` | Health |
| `/q/metrics` | Prometheus metrics (Sprint 2+) |

### 24.2 Custom Business Metrics

```java
@Inject MeterRegistry registry;

void onLoginSuccess() {
    registry.counter("eksad_login_total", "status", "success").increment();
}
```

Standard custom metrics per service:
- `eksad_{service}_{operation}_total` — Counter
- `eksad_{service}_{operation}_duration_seconds` — Timer
- `eksad_circuit_breaker_state{service="..."}` — Gauge

### 24.3 OpenTelemetry (Sprint 2+)

```properties
quarkus.otel.exporter.otlp.endpoint=http://jaeger:4317
quarkus.otel.service.name=${EKSAD_SERVICE_NAME}
```

Custom spans for business-critical operations:
```java
@WithSpan("process-login")
public TokenResult login(LoginRequest request) { ... }
```

> Full guide: `EKSAD_OBSERVABILITY_PATTERNS.md`.

---

## 25. Reserved Field Standards

> Implements **Principle #13 (Tenant-configurable reserved fields)** and **BR-PLATFORM-013 / BR-PLATFORM-014** from `EKSAD_BASE_PRINCIPLES.md`. Approach C Hybrid (12 typed slots + 1 JSONB overflow). Full pattern reference: `EKSAD_RESERVED_FIELD_PATTERNS.md`.
>
> Reserved fields are **opt-in per entity** — only transactional entities that tenants need to customize. Never apply to master data, cache tables, audit logs, or auth tables.

### 25.1 `BaseTransactionalEntity` Pattern

Transactional entities opt-in to reserved fields by extending `BaseTransactionalEntity` (in `eksad-core-common`) instead of `BaseEntity`.

```java
@MappedSuperclass
@Data
@EqualsAndHashCode(callSuper = true)
@SuperBuilder                         // ← NEVER @Builder — breaks BaseEntity inheritance
@NoArgsConstructor
@AllArgsConstructor
public abstract class BaseTransactionalEntity extends BaseEntity {

    // ── 5 string slots ────────────────────────────────────────────────────
    @Column(name = "reserved_str_1", length = 500) private String reservedStr1;
    @Column(name = "reserved_str_2", length = 500) private String reservedStr2;
    @Column(name = "reserved_str_3", length = 500) private String reservedStr3;
    @Column(name = "reserved_str_4", length = 500) private String reservedStr4;
    @Column(name = "reserved_str_5", length = 500) private String reservedStr5;

    // ── 3 numeric slots ───────────────────────────────────────────────────
    @Column(name = "reserved_num_1", precision = 20, scale = 4) private BigDecimal reservedNum1;
    @Column(name = "reserved_num_2", precision = 20, scale = 4) private BigDecimal reservedNum2;
    @Column(name = "reserved_num_3", precision = 20, scale = 4) private BigDecimal reservedNum3;

    // ── 2 date slots (epoch ms) ───────────────────────────────────────────
    @Column(name = "reserved_date_1") private Long reservedDate1;
    @Column(name = "reserved_date_2") private Long reservedDate2;

    // ── 2 boolean slots ───────────────────────────────────────────────────
    @Column(name = "reserved_bool_1") private Boolean reservedBool1;
    @Column(name = "reserved_bool_2") private Boolean reservedBool2;

    // ── JSONB overflow ────────────────────────────────────────────────────
    @Column(name = "reserved_ext", columnDefinition = "jsonb")
    @JdbcTypeCode(SqlTypes.JSON)
    private Map<String, Object> reservedExt;
}
```

**Opt-in usage:**
```java
@Entity
@Table(name = "orders")
@Data
@SuperBuilder
@NoArgsConstructor
@AllArgsConstructor
public class OrderEntity extends BaseTransactionalEntity {
    // ... regular columns
}
```

**Rules:**
- ✅ Use `@SuperBuilder` (not `@Builder`) — `BaseTransactionalEntity` extends `BaseEntity`.
- ✅ Never rename / reorder / re-type the 13 reserved columns — the shape is contractual across all EKSAD services.
- ❌ Never extend `BaseTransactionalEntity` on master data, cache tables, audit logs, or auth tables.

---

### 25.2 `ReservedFieldValidator` Service Pattern

Validate reserved-field values against tenant config at the create/update boundary in the service layer. **Always aggregate errors** — never throw on first fail.

```java
@ApplicationScoped
public class ReservedFieldValidator {

    @Inject ReservedFieldConfigResolver resolver;
    @Inject UserContext userContext;

    public void validate(String entity, BaseTransactionalEntity e) {
        Map<String, Object> values = extractReservedValues(e);
        List<String> errors = new ArrayList<>();

        for (var entry : values.entrySet()) {
            String slot  = entry.getKey();
            Object value = entry.getValue();
            ReservedFieldConfig cfg = resolver.resolve(userContext.getTenantId(), entity, slot);
            if (cfg == null || !cfg.visible()) continue;

            if (cfg.required() && value == null) {
                errors.add(cfg.label() + " is required");
                continue;
            }
            if (cfg.validation() != null) {
                applyRules(cfg, value, errors);   // ← appends to errors, never throws
            }
        }
        if (!errors.isEmpty()) {
            throw new ValidationException(String.join("; ", errors));
        }
    }
}
```

**Invocation from service layer:**
```java
@ApplicationScoped
@WithSession
public class OrderService {

    @Inject OrderRepository repository;
    @Inject OrderMapper      mapper;
    @Inject ReservedFieldValidator validator;

    @ReactiveTransactional
    public Uni<OrderEntity> create(OrderDTO dto) {
        return Uni.createFrom().item(() -> {
                OrderEntity e = mapper.toEntity(dto);
                validator.validate("orders", e);
                return e;
            })
            .flatMap(repository::create);          // ← createFlow inside repository
    }
}
```

**Rules:**
- ✅ Always aggregate errors — frontend needs all failures at once.
- ✅ Invoke before `createFlow()` / `updateFlow()` — validation must run inside the same reactive chain.
- ❌ Never call `validator.validate(...)` inside the repository — service layer owns business validation.

> Conditional rules (`when`/`then` predicates) and multi-rule composition (AND/OR) are documented in `EKSAD_RESERVED_FIELD_PATTERNS.md` §8.2–§8.3.

---

### 25.3 Reserved Field in DTO Pattern

DTOs are **Java records** with one explicit field per reserved slot — never a `Map<String, Object>` for typed slots (defeats type safety). Use `Map<String, Object>` only for `reserved_ext`.

```java
public record OrderDTO(
    Long       id,
    Long       customerId,
    BigDecimal amount,

    // ── Reserved typed slots (snake_case JSON → camelCase Java) ──────────
    @JsonProperty("reserved_str_1")  String     reservedStr1,
    @JsonProperty("reserved_str_2")  String     reservedStr2,
    @JsonProperty("reserved_str_3")  String     reservedStr3,
    @JsonProperty("reserved_str_4")  String     reservedStr4,
    @JsonProperty("reserved_str_5")  String     reservedStr5,
    @JsonProperty("reserved_num_1")  BigDecimal reservedNum1,
    @JsonProperty("reserved_num_2")  BigDecimal reservedNum2,
    @JsonProperty("reserved_num_3")  BigDecimal reservedNum3,
    @JsonProperty("reserved_date_1") Long       reservedDate1,
    @JsonProperty("reserved_date_2") Long       reservedDate2,
    @JsonProperty("reserved_bool_1") Boolean    reservedBool1,
    @JsonProperty("reserved_bool_2") Boolean    reservedBool2,

    // ── JSONB overflow ────────────────────────────────────────────────────
    @JsonProperty("reserved_ext")    Map<String, Object> reservedExt
) {}
```

**Mapper (MapStruct):**
```java
@Mapper(componentModel = "cdi",
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface OrderMapper {

    OrderEntity toEntity(OrderDTO dto);
    OrderDTO    toDto   (OrderEntity entity);

    // PATCH: null fields ignored — caller can omit untouched reserved slots
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void patch(OrderDTO dto, @MappingTarget OrderEntity entity);
}
```

**Null-handling per HTTP verb:**

| Verb | Behavior on `null` reserved field |
|------|-----------------------------------|
| `POST` (create) | `null` persisted as SQL `NULL` (slot empty) |
| `PUT` (replace) | `null` overwrites existing with SQL `NULL` |
| `PATCH` (partial) | `null` **ignored** — existing value retained |

**Rules:**
- ✅ Always use MapStruct — hand-rolled mappers drift when slots are added.
- ✅ Use `@JsonProperty("reserved_str_1")` to preserve snake_case in JSON wire format.
- ❌ Never collapse the 13 typed slots into a generic `Map<String, Object>` — breaks validation + indexing.

> Full DTO + Mapper reference: `EKSAD_RESERVED_FIELD_PATTERNS.md` §10.

---

### 25.4 Config Resolution Service Pattern

`ReservedFieldConfigResolver` performs the **tenant → domain → global** cascade lookup and **must cache** results — config is read on every reserved-field operation.

```java
@ApplicationScoped
public class ReservedFieldConfigResolver {

    @Inject ReservedFieldConfigRepository repo;
    @Inject TenantDomainLookup           tenantDomainLookup;

    /**
     * Cascade: tenant → domain → global. Cached 5 minutes; invalidated on
     * config update via {@link #invalidate(String, String)}.
     */
    @CacheResult(cacheName = "reserved-field-config")
    public ReservedFieldConfig resolve(
            @CacheKey String tenantId,
            @CacheKey String entity,
            @CacheKey String slot) {

        var tenantCfg = repo.findByScope("tenant", tenantId, entity, slot);
        if (tenantCfg != null) return tenantCfg;

        String domain = tenantDomainLookup.domainOf(tenantId);
        var domainCfg = repo.findByScope("domain", domain, entity, slot);
        if (domainCfg != null) return domainCfg;

        var globalCfg = repo.findByScope("global", "global", entity, slot);
        if (globalCfg != null) return globalCfg;

        return ReservedFieldConfig.hidden();   // ← default: not visible
    }

    @CacheInvalidate(cacheName = "reserved-field-config")
    public void invalidate(@CacheKey String tenantId,
                           @CacheKey String entity,
                           @CacheKey String slot) {
        // Called by config-mutation listener (RabbitMQ event) — keeps cache fresh
    }
}
```

**Configuration:**
```properties
# application.properties — Caffeine cache for reserved field config
quarkus.cache.caffeine."reserved-field-config".expire-after-write=5M
quarkus.cache.caffeine."reserved-field-config".maximum-size=10000
```

**Schema endpoint (JAX-RS Resource):**

```java
@Path("/api/v1/{entity}")
@Produces(MediaType.APPLICATION_JSON)
public class ReservedFieldSchemaResource {

    @Inject ReservedFieldConfigResolver resolver;
    @Inject UserContext                 userContext;

    @GET
    @Path("/_schema")
    @RolesAllowed({"USER", "ADMIN"})
    public Uni<Response> schema(@PathParam("entity") String entity) {
        String tenantId = userContext.getTenantId();
        List<ReservedFieldConfig> fields = Stream.of(
                "reserved_str_1","reserved_str_2","reserved_str_3","reserved_str_4","reserved_str_5",
                "reserved_num_1","reserved_num_2","reserved_num_3",
                "reserved_date_1","reserved_date_2",
                "reserved_bool_1","reserved_bool_2",
                "reserved_ext"
            )
            .map(slot -> resolver.resolve(tenantId, entity, slot))
            .filter(ReservedFieldConfig::visible)
            .toList();
        return Uni.createFrom().item(
            Response.ok(new ReservedFieldSchema(fields)).build()
        );
    }
}
```

**Rules:**
- ✅ Always `@CacheResult` the resolver — uncached cascade does 3 DB lookups per slot per request.
- ✅ Invalidate via `@CacheInvalidate` from the config-mutation event handler — keeps cache fresh.
- ✅ Schema endpoint requires `@RolesAllowed` like any other endpoint (no bare access).
- ❌ Never bypass the cascade — global-only or tenant-only lookups break the inheritance contract.

> Full cascade algorithm: `EKSAD_RESERVED_FIELD_PATTERNS.md` §6. Schema endpoint contract: §9.1.

---

### 25.5 Code Review Checklist (Reserved Field — Canonical Set)

The 8 checklist items below restate the `### Reserved Fields` subsection of §18 as the canonical reserved-field review set. Apply to **every PR** that touches a transactional entity, DTO, mapper, or `reserved_field_config`.

- [ ] Transactional entities that opt-in extend `BaseTransactionalEntity` (never bolt onto master/cache/audit/auth)
- [ ] 13 reserved field columns present in DDL (5 string + 3 numeric + 2 date + 2 boolean + 1 JSONB) — column names match the contract exactly
- [ ] `ReservedFieldValidator` invoked at create/update boundary in the service layer (before repository flow methods)
- [ ] Validator aggregates errors via `List<String>` and throws once — never first-fail
- [ ] Reserved field config resolution uses tenant → domain → global cascade with `@CacheResult` caching
- [ ] DTO ↔ Entity mapping uses MapStruct — no hand-rolled mappers; PATCH variant uses `NullValuePropertyMappingStrategy.IGNORE`
- [ ] Null-handling matches HTTP verb (POST/PUT → NULL; PATCH → ignore)
- [ ] Flyway migration follows `V{N}__add_reserved_fields_to_{table}.sql` template (`EKSAD_RESERVED_FIELD_PATTERNS.md` §13); per-tenant indexes named `idx_<table>_<tenant-slug>_<purpose>`

> Full standards: `EKSAD_RESERVED_FIELD_PATTERNS.md`. Frontend rendering rules: `EKSAD_FRONTEND_CODING_STANDARDS.md` §Reserved Field.

---

## 26. Repo & Build Strategy

> Implements **Principle #14 (Independent repo per service)** and **BR-PLATFORM-015** from `EKSAD_BASE_PRINCIPLES.md`. Rule: **One service = one repo = one CI/CD pipeline = one Docker image.** `eksad-parent` is a **published BOM** only — never a monorepo reactor. See `EKSAD_REPO_STRATEGY.md` for full detail.

---

### 26.1 Dependency Rules

| Maven `<dependency>` | Allowed? | Rule |
|----------------------|----------|------|
| Service → `eksad-core-common` | ✅ Required | All services must depend on `eksad-core-common` for `BaseEntity`, `BaseRepository`, `UserContext`, etc. |
| Service → `eksad-core-auth-client` | ✅ If needed | Add only if the service calls core-auth for credential validation or token issuance. |
| Service → `eksad-parent` (as `<parent>`) | ✅ Required | Every service and library must declare `eksad-parent` as `<parent>` — provides BOM version pins. |
| Service A → Service B (any domain service) | ❌ Forbidden | Services communicate via REST or RabbitMQ **only**. Declaring another service as a Maven dep creates hard compile-time coupling and breaks independent deploy. |
| Business logic in `eksad-core-common` | ❌ Forbidden | `eksad-core-common` must contain only infrastructure/utility code (`BaseEntity`, helpers, `LogHandler`). Business logic belongs in its domain service. |
| `<version>` on BOM-managed deps | ❌ Avoid | BOM-managed dependencies (`quarkus-bom`, `eksad-core-common`, `eksad-core-auth-client`) must NOT have explicit `<version>` tags — use BOM inheritance. |
| `<relativePath>` in `<parent>` block | ❌ Forbidden | Services live in separate repos — `<relativePath>` only works locally. Remove the tag entirely (Maven will fetch from the registry). |
| `-SNAPSHOT` version in production | ❌ Forbidden | Always pin exact released version in `pom.xml` for production branches. SNAPSHOT = non-deterministic build. |

---

### 26.2 `pom.xml` BOM Parent Template

Every EKSAD service and library starts with this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <!-- ── BOM Parent (published artifact, NOT local module) ──────────────── -->
  <parent>
    <groupId>com.eksad.platform</groupId>
    <artifactId>eksad-parent</artifactId>
    <version>1.0.0</version>           <!-- pin exact version; bump within 1–2 sprints of release -->
    <!-- <relativePath/> intentionally omitted — fetched from artifact registry -->
  </parent>

  <groupId>com.eksad</groupId>
  <artifactId>svc-pipeline</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>           <!-- libraries use jar; BOM itself uses pom -->

  <dependencies>

    <!-- Required: infrastructure base (version managed by BOM) -->
    <dependency>
      <groupId>com.eksad.platform</groupId>
      <artifactId>eksad-core-common</artifactId>
      <!-- NO <version> tag — BOM provides it -->
    </dependency>

    <!-- Optional: add only if this service handles auth / token calls -->
    <dependency>
      <groupId>com.eksad.platform</groupId>
      <artifactId>eksad-core-auth-client</artifactId>
      <!-- NO <version> tag — BOM provides it -->
    </dependency>

    <!-- ✅ Tech deps (Quarkus, Lombok, etc.) — all versions managed by BOM -->
    <!-- ❌ NEVER add another svc-* or eksad-core-* service as <dependency> -->

  </dependencies>

</project>
```

> **Publishing (library repos only):** Add `mvn deploy` to CI pipeline on tag push. Service repos (`svc-*`) produce **Docker images only** — never published to Maven registry.

---

### 26.3 Code Review Checklist (Repo & Build)

Apply to every PR that adds a new service, modifies `pom.xml`, or introduces a new Maven dependency.

- [ ] `<parent>` points to `eksad-parent` at latest released version (check for version drift > 2 sprints)
- [ ] No service is declared as Maven `<dependency>` of another service — inter-service communication uses REST or RabbitMQ
- [ ] No business logic in `eksad-core-common` (only infrastructure/utility: `Base*`, helpers, log handler)
- [ ] Version bump follows semver: PATCH for bug fix, MINOR for backward-compatible addition, MAJOR for breaking change
- [ ] New DTO fields or methods in shared libraries are nullable/Optional (backward compatibility within MAJOR)
- [ ] New service repo registered in `EKSAD_DOMAIN_REGISTRY.md` (port, module type prefix, service name)
- [ ] `<relativePath>` is absent from `<parent>` block (removed or never added)
- [ ] No `-SNAPSHOT` version on production-bound branches (`main`, `release/*`)

> Full repo governance rules → `EKSAD_REPO_STRATEGY.md`. Dependency flow diagram → `EKSAD_REPO_STRATEGY.md` §3.

---

## 27. Standard Response Wrapper (`GenericResponseDTO`)

**Version:** 1.0 — **Date:** 2026-05-25
**Rule:** Every REST API response (success AND error) MUST be wrapped in `GenericResponseDTO<T>`. No endpoint may return a raw entity, document, or unstructured JSON body.

### Shape

```json
{
  "status":   "SUCCESS",
  "message":  "Process succeeded",
  "data":     { ... },
  "metadata": { "totalCount": 100, "totalPages": 5, "page": 0, "size": 20, "hasNext": true, "hasPrevious": false }
}
```

- `status`   — always `"SUCCESS"` or `"FAIL"` (String, never Integer code) — consistent with `ErrorResponse.status`
- `message`  — human-readable description; use `"Process succeeded"` for success, error message for failures
- `data`     — payload `T`; `null` for void operations (delete)
- `metadata` — `PageMetadata`; `null` for single-item responses

### Java Classes (add to `eksad-core-common`, package `com.eksad.core.common.response`)

```java
// GenericResponseDTO.java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class GenericResponseDTO<T> {

    private String       status;    // "SUCCESS" or "FAIL"
    private String       message;
    private T            data;
    private PageMetadata metadata;  // null for single-item responses

    // ── Convenience factories ──────────────────────────────────────────────

    public static <T> GenericResponseDTO<T> success(T data) {
        return GenericResponseDTO.<T>builder()
            .status("SUCCESS")
            .message("Process succeeded")
            .data(data)
            .build();
    }

    public static <T> GenericResponseDTO<T> success(T data, PageMetadata metadata) {
        return GenericResponseDTO.<T>builder()
            .status("SUCCESS")
            .message("Process succeeded")
            .data(data)
            .metadata(metadata)
            .build();
    }

    public static <T> GenericResponseDTO<T> fail(String message) {
        return GenericResponseDTO.<T>builder()
            .status("FAIL")
            .message(message)
            .build();
    }
}

// PageMetadata.java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PageMetadata {
    private long    totalCount;
    private int     totalPages;
    private int     page;
    private int     size;
    private boolean hasNext;
    private boolean hasPrevious;

    public static PageMetadata of(long totalCount, int totalPages, int page, int size) {
        return PageMetadata.builder()
            .totalCount(totalCount)
            .totalPages(totalPages)
            .page(page)
            .size(size)
            .hasNext(page < totalPages - 1)
            .hasPrevious(page > 0)
            .build();
    }
}
```

### Usage in REST Resource

```java
// ✅ Single item
@GET @Path("/{id}")
public Uni<Response> findById(@PathParam("id") Long id) {
    return service.findById(id)
        .map(dto -> Response.ok(GenericResponseDTO.success(dto)).build());
}

// ✅ Paginated list
@GET
public Uni<Response> findAll(...) {
    return service.findAll(...)
        .map(paged -> {
            PageMetadata meta = PageMetadata.of(paged.getTotal(), paged.getTotalPages(), paged.getPage(), paged.getSize());
            return Response.ok(GenericResponseDTO.success(paged.getData(), meta)).build();
        });
}

// ✅ Create (201)
@POST
public Uni<Response> create(MyEntityDTO dto) {
    return service.create(dto)
        .map(saved -> Response.status(Response.Status.CREATED).entity(GenericResponseDTO.success(saved)).build());
}

// ❌ Never return raw entity/DTO without wrapper
return Response.ok(entity).build();        // ❌
return Response.ok(pagedResult).build();   // ❌
```

### eksad-core-audittrail Exception

`eksad-core-audittrail` **cannot** import `eksad-core-common` (Hibernate Reactive conflict with MongoDB-only service). Define `GenericResponseDTO` and `PageMetadata` locally in package `com.eksad.core.audittrail.core.dto.response`. Apply identical shape.

| Rule | Notes |
|------|-------|
| Always wrap in `GenericResponseDTO` | No raw entity/document/DTO body in response |
| Use `"SUCCESS"` / `"FAIL"` String status | Never Integer code |
| `metadata` is `null` for single-item | Only set for paginated list responses |
| `@JsonInclude(NON_NULL)` on class | Keeps `null` metadata out of JSON on single-item response |

---

## 28. Mapper Rule — Entity/Document Must Never Reach Presentation Layer

**Version:** 1.0 — **Date:** 2026-05-25
**Rule:** Persistence-layer objects (`*Entity`, MongoDB documents) MUST be converted to a `*ResponseDTO` via a MapStruct mapper **inside the service layer** before being returned. The resource (presentation layer) MUST only ever see `*ResponseDTO` — it must never import or reference any `*Entity` or MongoDB document class.

### Why

| Reason | Detail |
|--------|--------|
| **Security** | Entities often carry internal fields (soft-delete flags, versions, raw IDs) that must not be exposed in API |
| **Stability** | Schema changes (renaming a DB column) break the API contract if entities are returned directly |
| **Testability** | Service unit tests can verify DTO mapping independently of persistence |
| **Type safety** | MongoDB `ObjectId` must be serialized as `String` in JSON — mapper handles this explicitly |

### Pattern

```java
// ─── 1. ResponseDTO — presentation layer shape (never an entity) ───
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MyEntityResponseDTO {
    private Long   id;          // safe serializable type — NOT the raw JPA/MongoDB ID type
    private String name;
    // include only fields that the API consumer should see
}

// ─── 2. MapStruct mapper — inside core layer ──────────────────────
@Mapper(componentModel = "cdi")
public interface MyEntityMapper {
    @Mapping(target = "id", source = "id")   // explicit if type conversion needed
    MyEntityResponseDTO toResponseDTO(MyEntity entity);
    List<MyEntityResponseDTO> toResponseDTOList(List<MyEntity> entities);
}

// ─── 3. Service — returns ResponseDTO, never entity ───────────────
@ApplicationScoped
@WithSession
public class MyEntityService {
    @Inject MyEntityRepository repository;
    @Inject MyEntityMapper mapper;   // ← inject mapper in service layer

    public Uni<MyEntityResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(mapper::toResponseDTO);  // convert before returning
    }

    public Uni<PagedResult<MyEntityResponseDTO>> findAll(...) {
        return repository.findPaged(...)
            .map(list -> new PagedResult<>(mapper.toResponseDTOList(list), total, page, size));
    }
}

// ─── 4. Resource — references only ResponseDTO, never entity ──────
@Path("/api/v1/my-entities")
public class MyEntityResource {
    @Inject MyEntityService service;   // only MyEntityResponseDTO comes out

    @GET @Path("/{id}")
    @RolesAllowed({"ROLE_ADMIN"})
    public Uni<Response> findById(@PathParam("id") Long id) {
        return service.findById(id)
            .map(dto -> Response.ok(GenericResponseDTO.success(dto)).build());
    }
}
```

### MongoDB Document — Special Handling (ObjectId → String)

```java
// ✅ In mapper — convert ObjectId to String manually (no auto-conversion)
@Mapper(componentModel = "cdi")
public interface LogActivityMapper {
    @Mapping(target = "id", expression = "java(doc.getId() != null ? doc.getId().toHexString() : null)")
    LogActivityResponseDTO toResponseDTO(LogActivity doc);
    List<LogActivityResponseDTO> toResponseDTOList(List<LogActivity> docs);
}

// ❌ Never return LogActivity document from service
public Uni<LogActivity> findById(...) { ... }    // ❌ — returns MongoDB document
```

### Forbidden / Correct Table

| ❌ Forbidden | ✅ Correct | Why |
|---|---|---|
| Service returns `Uni<MyEntity>` | `Uni<MyEntityResponseDTO>` | Entity leaks to presentation layer |
| Service returns `Uni<PagedResult<MyEntity>>` | `Uni<PagedResult<MyEntityResponseDTO>>` | Same — entities must stay in data layer |
| Resource imports any `*Entity` class | Resource imports only `*ResponseDTO` | Strict layer boundary |
| Resource imports MongoDB document class | Import only `*ResponseDTO` | Same |
| `@Mapping` omitted for `ObjectId` field | Explicit `expression` mapping | Jackson can't serialize `ObjectId` |
| Mapper defined in resource layer | Mapper in `core/mapper` package | Mapper belongs to core/service layer |

### Code Review Checklist

- [ ] No `*Entity` or MongoDB document class imported in any `*Resource.java`
- [ ] Every service read method returns `Uni<*ResponseDTO>` or `Uni<PagedResult<*ResponseDTO>>`
- [ ] MapStruct mapper exists for every entity that has a REST endpoint
- [ ] `ObjectId` fields explicitly mapped to `String` in MongoDB mappers
- [ ] `GenericResponseDTO.success(dto)` / `GenericResponseDTO.success(list, metadata)` used in every resource response

---

## 29. MongoDB Document BSON Naming Rule

### 29.1 Rule

All **multi-word** fields on a MongoDB document MUST carry `@BsonProperty("snake_case")` so that MongoDB stores them using snake_case field names — consistent with EKSAD PostgreSQL column naming convention.

Single-word fields (`action`, `role`, `status`, `username`, `activity`) do **not** need the annotation.

> **Why:** Without `@BsonProperty`, MongoDB stores Java camelCase field names verbatim (e.g. `transactionId`). This breaks operational queries in MongoDB Compass/Atlas and is inconsistent with EKSAD's snake_case column convention.

### 29.2 Mandatory Template

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@MongoEntity(collection = "log_activity")
public class LogActivity {

    @BsonId
    private ObjectId id;                      // _id — always @BsonId, no @BsonProperty needed

    @BsonProperty("transaction_id")
    private String transactionId;

    private String action;                    // single word — no annotation needed
    private String activity;                  // single word — no annotation needed

    @BsonProperty("module_type")
    private String moduleType;

    @BsonProperty("entity_type")
    private String entityType;

    @BsonProperty("entity_id")
    private String entityId;

    private String username;                  // single word — no annotation needed
    private String role;                      // single word — no annotation needed

    @BsonProperty("company_id")
    private String companyId;               // tenant identifier — ALWAYS present (EKSAD Principle 4)

    private String status;                    // single word — no annotation needed

    @BsonProperty("fail_reason")
    private String failReason;

    @BsonProperty("request_uri")
    private String requestUri;

    @BsonProperty("request_services")
    private String requestServices;

    @BsonProperty("data_before")
    private String dataBefore;

    @BsonProperty("data_after")
    private String dataAfter;

    @BsonProperty("data_changes")
    private String dataChanges;

    @BsonProperty("log_activity_type")
    private Integer logActivityType;

    @BsonProperty("request_time")
    private Long requestTime;               // epoch ms (EKSAD Principle 7)

    @BsonProperty("response_time")
    private Long responseTime;              // epoch ms (EKSAD Principle 7)

    @BsonProperty("created_at")
    private Long createdAt;                 // epoch ms — set by service on persist (EKSAD Principle 7)

    @BsonProperty("created_by")
    private String createdBy;              // actor username — denormalized for log readability
}
```

### 29.3 Panache Query String Rule After `@BsonProperty`

After adding `@BsonProperty`, **all Panache query strings and `Sort.by()` calls must use the BSON (snake_case) field name**, not the Java field name.

```java
// ✅ Correct — use BSON field names in queries
find("company_id = ?1 and module_type = ?2", tenantId, moduleType);
find("_id = ?1 and company_id = ?2", objectId, tenantId);
Sort.by("request_time", Sort.Direction.Descending);

// ❌ Wrong — Java field names no longer resolve after @BsonProperty is applied
find("companyId = ?1 and moduleType = ?2", tenantId, moduleType);
Sort.by("requestTime", Sort.Direction.Descending);
```

### 29.4 `@BsonProperty` is Transparent to MapStruct

MapStruct operates on Java objects — it never touches BSON serialization. No changes to mapper code are needed when `@BsonProperty` is added to a document.

### 29.5 `@JsonProperty` on DTO (RabbitMQ Consumer)

When the RabbitMQ producer sends snake_case JSON keys, add `@JsonProperty("snake_case")` to the corresponding DTO fields so Jackson deserializes them into camelCase Java fields correctly.

```java
// LogActivityDTO — Jackson reads snake_case from RabbitMQ, maps to camelCase Java fields
@JsonProperty("transaction_id")  private String transactionId;
@JsonProperty("module_type")     private String moduleType;
@JsonProperty("company_id")      private String companyId;
@JsonProperty("request_time")    private Long   requestTime;
// Single-word fields: no @JsonProperty needed
private String action;
private String status;
private String username;
private String activity;
```

### 29.6 Forbidden / Correct Table

| ❌ Forbidden | ✅ Correct | Why |
|---|---|---|
| `private String transactionId` without `@BsonProperty` | `@BsonProperty("transaction_id") private String transactionId` | MongoDB stores `transactionId` (camelCase) — breaks snake_case convention |
| `find("companyId = ?1", ...)` after `@BsonProperty` | `find("company_id = ?1", ...)` | Panache resolves against BSON field names after `@BsonProperty` |
| `Sort.by("requestTime", ...)` after `@BsonProperty` | `Sort.by("request_time", ...)` | Same — Sort uses BSON field name |
| Adding `@BsonProperty` to MapStruct mapper | No change to mapper | MapStruct is BSON-unaware — `@BsonProperty` only affects MongoDB codec |

---

## 29.7 MongoDB Reactive Pagination Pattern (`ReactivePanacheQuery`)

### Rule

For **paginated MongoDB reads**, the repository method MUST return `ReactivePanacheQuery<T>` — NOT `Uni<List<T>>`.
The service calls `.list()`, `.count()`, `.pageCount()`, and `.hasNextPage()` on the **same query object** so the filter is built ONCE and reused across all pagination operations.

> **Why:** Separate `findByTenantPaged()` + `countByTenant()` methods duplicate the entire filter string — two strings to keep in sync, two methods to update when filters change, and two separate query builder calls.

### Repository (returns `ReactivePanacheQuery` — no `.list()`)

```java
// ✅ buildQuery() returns the query object — does NOT execute it
public ReactivePanacheQuery<LogActivity> buildQuery(
        String tenantId, String moduleType, String status,
        String username, Long from, Long to, int page, int size) {

    StringBuilder query = new StringBuilder("company_id = ?1");  // filter built ONCE
    List<Object> params = new ArrayList<>();
    params.add(tenantId);

    if (moduleType != null && !moduleType.isBlank()) {
        query.append(" and module_type = ?2");
        params.add(moduleType);
    }
    // ... additional filters ...

    return find(query.toString(),
                Sort.by("request_time", Sort.Direction.Descending),
                params.toArray())
           .page(Page.of(page, Math.min(size, 100)));  // ← NO .list() here
}

// ❌ Old pattern — filter string duplicated across two methods
public Uni<List<LogActivity>> findByTenantPaged(...) { ... }  // ❌ builds query + executes
public Uni<Long>              countByTenant(...)      { ... }  // ❌ rebuilds same query
```

### Service (`flatMap` + `Uni.combine` on one query object)

```java
public Uni<PagedResult<LogActivityResponseDTO>> findAll(...) {
    ReactivePanacheQuery<LogActivity> query = repository.buildQuery(
            tenantId, moduleType, status, username, from, to, page, size);

    boolean hasPrevious = query.hasPreviousPage();  // synchronous — safe outside reactive chain

    return query.list()
            .flatMap(list -> {
                List<LogActivityResponseDTO> dtos = mapper.toResponseDTOList(list);

                return Uni.combine().all()
                        .unis(query.count(),        // Uni<Long>    — total matching docs
                              query.pageCount(),    // Uni<Integer> — total pages
                              query.hasNextPage())  // Uni<Boolean> — has more pages
                        .asTuple()
                        .map(tuple -> new PagedResult<>(
                                dtos,
                                tuple.getItem1(),   // total
                                page,
                                size,
                                tuple.getItem2(),   // totalPages
                                tuple.getItem3(),   // hasNext — from Panache
                                hasPrevious));      // hasPrevious — from Panache
            });
}
```

### Resource (pass Panache hasNext/hasPrevious through — do NOT recompute)

```java
// ✅ Use PagedResult.isHasNext() / isHasPrevious() — sourced from Panache
PageMetadata meta = PageMetadata.of(
        paged.getTotal(), paged.getTotalPages(), paged.getPage(), paged.getSize(),
        paged.isHasNext(), paged.isHasPrevious());   // ← 6-arg overload

// ❌ Do NOT recompute: hasNext(page < totalPages - 1) — Panache already computed it
```

### `hasPreviousPage()` is Synchronous

| Method | Type | Notes |
|--------|------|-------|
| `query.hasNextPage()` | `Uni<Boolean>` | Async — include in `Uni.combine()` |
| `query.hasPreviousPage()` | `boolean` | Synchronous — call before the reactive chain |
| `query.count()` | `Uni<Long>` | Async |
| `query.pageCount()` | `Uni<Integer>` | Async |
| `query.list()` | `Uni<List<T>>` | Async — starts the chain |

### Forbidden / Correct Table

| ❌ Forbidden | ✅ Correct | Why |
|---|---|---|
| `findByTenantPaged()` + `countByTenant()` as separate repository methods | Single `buildQuery()` returning `ReactivePanacheQuery` | Filter string duplication — two strings to keep in sync |
| `repository.buildQuery(...).list()` in repository | `repository.buildQuery(...)` ← `.list()` called in service | Repository must not execute — service drives pagination ops |
| `Uni.combine(dataUni, countUni)` with two separate Uni sources | `query.list().flatMap(...)` + combine on same query | Same query object — no duplication |
| `hasNext(page < totalPages - 1)` in Resource/Service | `paged.isHasNext()` from Panache | Panache calculation is authoritative |
