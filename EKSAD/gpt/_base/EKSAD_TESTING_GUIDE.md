# EKSAD Testing Guide
# Quarkus Reactive — Unit, Integration & QA Testing Patterns

**Version:** 1.3
**Date:** 2026-05-31
**Owner:** EKSAD Platform Team
**Audience:** Developers, QA Engineers, Technical Leaders (via GPT Knowledge)

> This file is uploaded as a **GPT knowledge file** for Developer GPT, QA GPT, and TL GPT.

---

## Table of Contents

1. [Testing Philosophy](#1-testing-philosophy)
2. [Test Layer Overview](#2-test-layer-overview)
   - [2.1 Test Ownership Matrix (Developer vs QA)](#21-test-ownership-matrix-developer-vs-qa)
   - [2.2 QA Operating Modes — A (Design) & B (Automation)](#22-qa-operating-modes--a-design--b-automation)
3. [Unit Tests — Service Layer](#3-unit-tests--service-layer)
4. [Unit Tests — Repository Logic](#4-unit-tests--repository-logic)
5. [Integration Tests — REST Resource Layer](#5-integration-tests--rest-resource-layer)
6. [Reactive Test Patterns (Mutiny)](#6-reactive-test-patterns-mutiny)
7. [Mocking UserContext & AuthContextStore](#7-mocking-usercontext--authcontextstore)
8. [Testcontainers Setup](#8-testcontainers-setup)
9. [Test Naming Convention](#9-test-naming-convention)
10. [Coverage Targets](#10-coverage-targets)
11. [QA: Deriving Test Cases from FSD](#11-qa-deriving-test-cases-from-fsd)
12. [QA: Test Plan Template](#12-qa-test-plan-template)
13. [QA: API Testing with REST Assured](#13-qa-api-testing-with-rest-assured)
14. [Master Data Service Testing](#14-master-data-service-testing)
15. [Cache Sync Testing](#15-cache-sync-testing)
16. [Multi-Tenancy Testing](#16-multi-tenancy-testing)
17. [Core Auth Testing](#17-core-auth-testing)
18. [Security Testing](#18-security-testing)
19. [Resilience Testing](#19-resilience-testing)
20. [Observability Testing](#20-observability-testing)
21. [Reserved Field Testing](#21-reserved-field-testing)
22. [Testcontainers — Extended Infrastructure](#22-testcontainers--extended-infrastructure)
24. [Test Code Review Checklist](#24-test-code-review-checklist)

---

## 1. Testing Philosophy

| Principle | Description |
|-----------|-------------|
| **Test behavior, not implementation** | Test what the code *does*, not *how* it does it internally |
| **Each layer has its own test style** | Service layer → unit test with mocks; Resource layer → integration test with running app |
| **Failure scenarios matter as much as happy paths** | Every guard, validation, and state check must have a failure test |
| **Reactive operations need special handling** | Never call `.await()` in production code; it's acceptable in tests only |
| **Tests must be independent** | No test should depend on another test's state. Each test sets up its own data. |
| **Audit trail is fire-and-forget** | Do NOT assert on audit log content in unit/integration tests — mock the emitter |

---

## 2. Test Layer Overview

```
┌─────────────────────────────────────────────────────────────┐
│  REST Resource Layer  (@QuarkusTest + REST Assured)          │
│  → Tests HTTP behavior, status codes, auth, request/response │
├─────────────────────────────────────────────────────────────┤
│  Service Layer  (@ExtendWith(MockitoExtension.class))        │
│  → Tests business logic, calls to repository, error handling │
├─────────────────────────────────────────────────────────────┤
│  Repository Layer  (tested via integration or skipped)       │
│  → BaseRepository flows tested via @QuarkusTest with real DB │
└─────────────────────────────────────────────────────────────┘
```

**Coverage priority:** Service layer → Resource layer → Repository layer

---

## 2.1 Test Ownership Matrix (Developer vs QA)

> **Single source of truth for who owns which test layer.** Resolves the developer/QA overlap on
> integration/API tests. Split is by **owner + viewpoint**, not by tool.

| Layer | Owner | Viewpoint | Intent | Lives in |
|-------|-------|-----------|--------|----------|
| **Unit** (service w/ mocks, repository logic) | 🧑‍💻 Developer | White-box (knows internal guards) | "my code works" | `src/test/java/.../service`, `.../repository` |
| **Integration — internal** (own service + Testcontainers, happy + guard) | 🧑‍💻 Developer | White-box | Fast TDD regression | `src/test/java/.../resource` (dev-owned) |
| **API / Acceptance** (REST Assured vs running app, full matrix) | 🧪 QA | **Black-box, derived from FSD** | "requirement satisfied + breaks under abuse" | `src/test/java/.../qa` (QA-owned) |
| **E2E — cross-service** (business flow across services) | 🧪 QA | Black-box | "end-to-end flow correct" | `*-e2e` repo / `e2e/` module |
| **FE E2E** (UI flows) | 🧪 QA | Black-box | "user journey works" | **Playwright** project (default tooling) |
| **Non-functional** (load `k6`, security smoke) | 🧪 QA | Black-box | "survives load / abuse" | `perf/`, `security/` |

**Overlap rule (API/integration):** Developer writes integration tests for **their own happy + guard paths**
during TDD. QA writes **acceptance API tests derived from the FSD** covering the **full matrix** — all error
codes, every state-machine transition, multi-tenant isolation, 401/403, and audit-trail verification.
Different intent: developer proves the code is correct; QA proves the requirement is satisfied **and** the
system fails safely when abused. **QA does not touch unit tests** — those are developer-owned.

---

## 2.2 QA Operating Modes — A (Design) & B (Automation)

QA work runs in two distinct modes with different inputs and outputs:

| Mode | Input | Output | Surface |
|------|-------|--------|---------|
| **A — Design / Docs** | **FSD** | Test Plan, Test Case Matrix (8-col), **RTM** (Requirement Traceability Matrix), state-machine matrix | QA GPT-knowledge assistant (`qa/`) |
| **B — Automation** | **TSD** + `PLAN_<MODULE>.md` | REST Assured API scripts, E2E suites, regression packs | QA vibe-coding in-IDE agent (`vibe-coding/qa/`) |

**Scope boundaries for Mode B (in-IDE agent):**
- ✅ Writes **test code only** (REST Assured / Playwright / k6) — never production code.
- ✅ May **read production code read-only** to understand endpoints/contracts.
- ✅ Operates from **staging branches** (test code may land on staging without touching prod logic).
- ❌ Never edits `src/main/**` (entities, services, resources, migrations).
- 📁 Writes confined to `src/test/**`, `e2e/**`, `perf/**`, `security/**`.

**Default automation tooling:** REST Assured (API), **Playwright** (FE E2E), k6 (load). FE E2E tool choice is
provisional — team to confirm after research.

---

## 3. Unit Tests — Service Layer

### 3.1 Standard Setup

```java
@ExtendWith(MockitoExtension.class)
class TransactionServiceTest {

    @Mock
    TransactionRepository repository;

    @InjectMocks
    TransactionService service;

    // ─── Happy Path ────────────────────────────────────────────

    @Test
    @DisplayName("create: valid DTO → returns saved entity")
    void create_validDto_returnsSavedEntity() {
        // Arrange
        TransactionDTO dto = TransactionDTO.builder()
                .userId("user-01")
                .type("CREDIT")
                .amount(new BigDecimal("1000.0000"))
                .build();

        TransactionEntity expected = TransactionEntity.builder()
                .id(1L)
                .userId("user-01")
                .type("CREDIT")
                .amount(new BigDecimal("1000.0000"))
                .status("PENDING")
                .build();

        when(repository.createEntity(dto))
                .thenReturn(Uni.createFrom().item(expected));

        // Act
        TransactionEntity result = service.create(dto)
                .await().indefinitely();

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getType()).isEqualTo("CREDIT");
        verify(repository).createEntity(dto);
    }

    // ─── Failure Path ──────────────────────────────────────────

    @Test
    @DisplayName("update: entity not found → throws ValidationException")
    void update_entityNotFound_throwsValidationException() {
        TransactionDTO dto = TransactionDTO.builder().id(999L).build();

        when(repository.updateEntity(dto))
                .thenReturn(Uni.createFrom()
                        .failure(new ValidationException("Data not found")));

        assertThatThrownBy(() ->
                service.update(dto).await().indefinitely()
        ).isInstanceOf(ValidationException.class)
         .hasMessageContaining("Data not found");
    }
}
```

### 3.2 What to Test in Service Layer

| Scenario | Test |
|----------|------|
| Happy path — create | Verify repository called, result returned |
| Happy path — update | Verify mutator applied, repository called |
| Happy path — delete | Verify soft delete applied |
| Entity not found | Expect `ValidationException` |
| Guard fails (e.g., wrong state) | Expect `ValidationException` with correct message |
| Repository throws unexpected error | Verify error propagates |
| `findById` returns null | Verify failure handled |

---

## 4. Unit Tests — Repository Logic

Repository logic (guards, `toNewEntity` mapping, module type strings) can be tested in isolation:

```java
@ExtendWith(MockitoExtension.class)
class TransactionRepositoryTest {

    @Mock
    UserContext userContext;

    @Mock
    LogHandler logHandler;

    @Mock
    UriResolver uriResolver;

    // Partial mock — test only toNewEntity logic
    @Test
    @DisplayName("toNewEntity: maps DTO fields correctly")
    void toNewEntity_mapsAllFields() {
        when(userContext.getUser()).thenReturn("test-user");
        when(userContext.getTenantId()).thenReturn("test-tenant");

        TransactionRepository repo = new TransactionRepository();
        // inject mocks manually if not using @InjectMocks
        // ...

        TransactionDTO dto = TransactionDTO.builder()
                .type("DEBIT")
                .amount(new BigDecimal("500.0000"))
                .build();

        TransactionEntity entity = repo.toNewEntity(dto);

        assertThat(entity.getType()).isEqualTo("DEBIT");
        assertThat(entity.getTenantId()).isEqualTo("test-tenant");
        assertThat(entity.getCreatedBy()).isEqualTo("test-user");
        assertThat(entity.getCreatedAt()).isNotNull().isPositive();
        assertThat(entity.getDeletedAt()).isNull();
    }
}
```

---

## 5. Integration Tests — REST Resource Layer

### 5.1 Standard Setup

```java
@QuarkusTest
@TestHTTPEndpoint(TransactionResource.class)
class TransactionResourceTest {

    // ─── Helper: generate test JWT ────────────────────────────
    private static String adminToken() {
        return Jwt.preferredUserName("test-admin")
                  .claim("eksad_role", "ROLE_ADMIN")
                  .claim("eksad_tenant_id", "test-tenant")
                  .claim("eksad_user_id", "user-001")
                  .groups("ROLE_ADMIN")
                  .issuer("eksad-auth-service")
                  .sign(); // requires test private key in META-INF/resources
    }

    // ─── Happy Path ────────────────────────────────────────────

    @Test
    @DisplayName("POST /: valid payload → 201 Created")
    void create_validPayload_returns201() {
        given()
            .header("Authorization", "Bearer " + adminToken())
            .contentType(ContentType.JSON)
            .body("""
                {
                  "userId": "user-01",
                  "type": "CREDIT",
                  "amount": 1000.0000
                }
            """)
        .when()
            .post()
        .then()
            .statusCode(201)
            .body("type", equalTo("CREDIT"))
            .body("status", equalTo("PENDING"));
    }

    // ─── Auth Failure ──────────────────────────────────────────

    @Test
    @DisplayName("POST /: no token → 401")
    void create_noToken_returns401() {
        given()
            .contentType(ContentType.JSON)
            .body("{}")
        .when()
            .post()
        .then()
            .statusCode(401);
    }

    @Test
    @DisplayName("POST /: wrong role → 403")
    void create_viewerRole_returns403() {
        String viewerToken = Jwt.preferredUserName("viewer")
                .claim("eksad_role", "ROLE_VIEWER")
                .groups("ROLE_VIEWER")
                .issuer("eksad-auth-service")
                .sign();

        given()
            .header("Authorization", "Bearer " + viewerToken)
            .contentType(ContentType.JSON)
            .body("{}")
        .when()
            .post()
        .then()
            .statusCode(403);
    }

    // ─── Validation Failure ────────────────────────────────────

    @Test
    @DisplayName("GET /{id}: not found → 422")
    void findById_notFound_returns422() {
        given()
            .header("Authorization", "Bearer " + adminToken())
        .when()
            .get("/99999")
        .then()
            .statusCode(422);
    }
}
```

### 5.2 JWT Test Key Setup

Add test private key to `src/test/resources/META-INF/resources/test-private-key.pem` and configure:

```properties
# src/test/resources/application.properties (test override)
smallrye.jwt.sign.key.location=META-INF/resources/test-private-key.pem
mp.jwt.verify.publickey.location=META-INF/resources/test-public-key.pem
mp.jwt.verify.issuer=eksad-auth-service
```

---

## 6. Reactive Test Patterns (Mutiny)

### 6.1 Awaiting Uni Results in Tests

```java
// ✅ In tests — .await().indefinitely() is acceptable
TransactionEntity result = service.create(dto).await().indefinitely();

// ✅ With timeout — safer for CI environments
TransactionEntity result = service.create(dto)
        .await().atMost(Duration.ofSeconds(5));

// ✅ Assert failure with UniAssertSubscriber
service.update(invalidDto)
        .subscribe().withSubscriber(UniAssertSubscriber.create())
        .awaitFailure()
        .assertFailedWith(ValidationException.class, "Data not found");

// ❌ Never use .await() in production code — only in tests
```

### 6.2 Testing Failure Propagation

```java
@Test
@DisplayName("commandFlow: guard fails → ValidationException with correct message")
void commandFlow_guardFails_throwsWithMessage() {
    // Simulate entity in wrong state
    TransactionEntity entity = TransactionEntity.builder()
            .id(1L).status("APPROVED").build(); // already approved

    when(repository.findById(1L))
            .thenReturn(Uni.createFrom().item(entity));

    ApproveDTO dto = ApproveDTO.builder().transactionId(1L).build();

    service.approve(dto)
            .subscribe().withSubscriber(UniAssertSubscriber.create())
            .awaitFailure()
            .assertFailedWith(ValidationException.class);
}
```

---

## 7. Mocking UserContext & AuthContextStore

### 7.1 CDI `@Alternative` Mock (Integration Tests)

```java
// src/test/java/.../mock/MockUserContext.java
@ApplicationScoped
@Alternative
@Priority(1)                 // ← overrides the real UserContext
public class MockUserContext extends UserContext {

    @Override
    public String getUser() { return "test-user"; }

    @Override
    public String getRole() { return "ROLE_ADMIN"; }

    @Override
    public String getTenantId() { return "test-tenant"; }

    @Override
    public String getAuditActor() { return "test-user"; }
}
```

Activate in `src/test/resources/META-INF/beans.xml`:
```xml
<beans>
  <alternatives>
    <class>com.eksad.svc.{domain}.mock.MockUserContext</class>
  </alternatives>
</beans>
```

### 7.2 Mock `MutinyEmitter` to Silence Audit in Tests

```java
@ApplicationScoped
@Alternative
@Priority(1)
public class MockLogHandler extends LogHandler {

    @Override
    public <E> Uni<Void> logSuccess(LogActivityDTO log, String txId, E after) {
        // No-op in tests — don't send to RabbitMQ
        return Uni.createFrom().voidItem();
    }

    @Override
    public <T> Uni<T> logFailure(LogActivityDTO log, String message) {
        return Uni.createFrom().failure(new ValidationException(message));
    }
}
```

---

## 8. Testcontainers Setup

### 8.1 PostgreSQL Container

```java
// src/test/java/.../infrastructure/PostgresTestResource.java
public class PostgresTestResource implements QuarkusTestResourceLifecycleManager {

    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine")
            .withDatabaseName("eksad_test")
            .withUsername("eksad")
            .withPassword("eksad_test");

    @Override
    public Map<String, String> start() {
        postgres.start();
        return Map.of(
            "quarkus.datasource.reactive.url",
                "postgresql://" + postgres.getHost() + ":" + postgres.getMappedPort(5432) + "/eksad_test",
            "quarkus.datasource.username", "eksad",
            "quarkus.datasource.password", "eksad_test"
        );
    }

    @Override
    public void stop() { postgres.stop(); }
}
```

Activate on test class:
```java
@QuarkusTest
@QuarkusTestResource(PostgresTestResource.class)
class TransactionRepositoryIntegrationTest { ... }
```

### 8.2 RabbitMQ Container (Optional — for audit trail integration tests)

```java
public class RabbitMQTestResource implements QuarkusTestResourceLifecycleManager {

    static RabbitMQContainer rabbit = new RabbitMQContainer("rabbitmq:3.13-alpine")
            .withVhost("eksad_vhost");

    @Override
    public Map<String, String> start() {
        rabbit.start();
        return Map.of(
            "rabbitmq-host", rabbit.getHost(),
            "rabbitmq-port", String.valueOf(rabbit.getMappedPort(5672)),
            "rabbitmq-username", rabbit.getAdminUsername(),
            "rabbitmq-password", rabbit.getAdminPassword()
        );
    }

    @Override
    public void stop() { rabbit.stop(); }
}
```

---

## 9. Test Naming Convention

```
methodName_scenario_expectedResult

Examples:
  create_validDto_returnsSavedEntity
  create_missingUserId_throwsValidationException
  update_entityNotFound_throwsValidationException
  update_deletedEntity_throwsValidationException
  delete_activeEntity_setsDeletedAt
  approve_wrongState_throwsWithMessage
  findById_notFound_returns422
  create_noToken_returns401
  create_viewerRole_returns403
```

**Rules:**
- Always 3 parts separated by `_`
- `methodName` = the method or endpoint being tested
- `scenario` = the input condition or state
- `expectedResult` = what should happen
- Always add `@DisplayName` with a human-readable description

---

## 10. Coverage Targets

| Layer | Target | Tool |
|-------|--------|------|
| Service layer (unit tests) | **≥ 70%** line coverage | JaCoCo |
| Resource layer (integration tests) | All endpoints: happy path + 401 + 403 + main error | REST Assured |
| Repository `toNewEntity` | 100% — always test field mapping | JUnit 5 |
| Guard conditions | 100% — test both pass and fail for each guard | JUnit 5 |
| State machine transitions | All valid + all invalid transitions | JUnit 5 |

### Maven JaCoCo Config

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>check</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>PACKAGE</element>
            <limits>
              <limit>
                <counter>LINE</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.70</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

---

## 11. QA: Deriving Test Cases from FSD

### 11.1 From User Stories

For every user story `US-{MODULE}-{N}`, derive:

| User Story Element | Test Case |
|-------------------|-----------|
| Main success path | Happy path integration test |
| Each validation rule | 1 test per validation — invalid input |
| Each acceptance criterion | 1 test asserting the criterion is met |
| Role restriction | 1 test per forbidden role |

### 11.2 From State Machine

For every state transition table in FSD:

| State Machine Element | Test Case |
|----------------------|-----------|
| Each valid transition | `test_{action}_from{State}_transitions_to{NewState}` |
| Each invalid transition (wrong state) | `test_{action}_from{WrongState}_throws422` |
| Terminal state (APPROVED, etc.) | `test_{action}_onTerminalState_throws422` |

Example for a 3-state machine (DRAFT → SUBMITTED → APPROVED):

```
✅ submit_fromDraft_transitionsToSubmitted
✅ approve_fromSubmitted_transitionsToApproved
✅ reject_fromSubmitted_transitionsToRejected
❌ submit_fromApproved_throws422
❌ approve_fromDraft_throws422
❌ approve_fromRejected_throws422
```

### 11.3 From Validation Rules Table

For every field validation rule in FSD:

```
Field: amount, Rule: must be > 0
→ Test: create_withZeroAmount_returns400
→ Test: create_withNegativeAmount_returns400
→ Test: create_withValidAmount_returns201
```

---

## 12. QA: Test Plan Template

### 12.0 Requirement Traceability Matrix (RTM) — Mode A Deliverable

The RTM is the first artifact QA produces in **Mode A** (§2.2). It links every FSD requirement to the test
case(s) that verify it — guaranteeing no requirement ships untested. Each FSD requirement must map to **≥ 1**
test case; flag any row with no coverage.

```markdown
# RTM — {MODULE} Module
## FSD Source: {FSD filename} | Date: {DATE}

| Req ID | FSD Reference | Requirement (short) | Type | Test Case ID(s) | Owner | Coverage |
|--------|--------------|---------------------|------|-----------------|-------|----------|
| REQ-01 | US-1 / AC-1.1 | Submitter can create a submission | Functional | TC-001, TC-002 | QA | ✅ |
| REQ-02 | BR-3 | Only SUBMITTED can be approved | Business Rule | TC-014, TC-015 | QA | ✅ |
| REQ-03 | §4 State Machine | All invalid transitions → 422 | State Machine | TC-020..TC-027 | QA | ✅ |
| REQ-04 | NFR-2 | p95 < 300ms @ 200 rps | Non-functional | PERF-01 | QA | ⚠️ pending tool |
| REQ-05 | §5 Field Rules | amount > 0 | Validation | TC-030, TC-031 | QA | ✅ |

> Coverage legend: ✅ covered · ⚠️ partial/blocked · ❌ no test yet (gap — must flag)
```

---

### 12.1 Test Plan Skeleton

```markdown
# Test Plan — {MODULE} Module
## Service: {SERVICE_NAME} | Version: {VERSION} | Date: {DATE}

### 1. Scope
Modules covered: {list}
Out of scope: {list}

### 2. Test Environment
| Item | Value |
|------|-------|
| Base URL | `http://localhost:{PORT}/api/v1` |
| Test DB | PostgreSQL (Testcontainers) |
| Auth | Test JWT from `SmallRye JWT test key` |

### 3. Test Cases

#### 3.1 {Module} — Happy Path
| ID | Description | Input | Expected Result | Status |
|----|-------------|-------|-----------------|--------|
| TC-{N} | Create {entity} successfully | Valid DTO | 201, entity returned | 🔲 |
| TC-{N} | Get {entity} by ID | Valid ID | 200, entity returned | 🔲 |

#### 3.2 {Module} — Authentication
| ID | Description | Input | Expected | Status |
|----|-------------|-------|----------|--------|
| TC-{N} | No token | Any request | 401 | 🔲 |
| TC-{N} | Expired token | Expired JWT | 401 | 🔲 |
| TC-{N} | Wrong role | Insufficient role JWT | 403 | 🔲 |
| TC-{N} | Wrong tenant | Cross-tenant JWT | 403 | 🔲 |

#### 3.3 {Module} — Validation
| ID | Description | Input | Expected | Status |
|----|-------------|-------|----------|--------|
| TC-{N} | {Field} empty | {field}: null | 400/422 | 🔲 |
| TC-{N} | {Field} over max length | {field}: 256 chars | 400/422 | 🔲 |

#### 3.4 {Module} — State Machine
| ID | Description | From State | Action | Expected To State | Status |
|----|-------------|-----------|--------|-------------------|--------|
| TC-{N} | Valid submit | DRAFT | submit | SUBMITTED | 🔲 |
| TC-{N} | Invalid approve from DRAFT | DRAFT | approve | 422 | 🔲 |

### 4. Pass/Fail Criteria
- All TC marked 🔲 must be executed
- 0 P1 failures allowed for release
- P2 failures must have approved mitigation plan
```

---

## 13. QA: API Testing with REST Assured

### 13.1 Collection Structure

Organize tests as a REST Assured test class per module:

```java
@QuarkusTest
@QuarkusTestResource(PostgresTestResource.class)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class TransactionApiTest {

    private static Long createdId;

    // ─── Create ──────────────────────────────────────────────

    @Test
    @Order(1)
    @DisplayName("TC-001: Create transaction — 201")
    void tc001_createTransaction_returns201() {
        Integer id = given()
            .header("Authorization", "Bearer " + adminToken())
            .contentType(ContentType.JSON)
            .body("""
                { "userId": "u01", "type": "CREDIT", "amount": 1000.0000 }
            """)
        .when().post("/api/v1/transactions")
        .then()
            .statusCode(201)
            .body("status", equalTo("PENDING"))
            .extract().path("id");

        createdId = id.longValue();
    }

    // ─── Read ─────────────────────────────────────────────────

    @Test
    @Order(2)
    @DisplayName("TC-002: Get by ID — 200")
    void tc002_getById_returns200() {
        given()
            .header("Authorization", "Bearer " + adminToken())
        .when().get("/api/v1/transactions/" + createdId)
        .then()
            .statusCode(200)
            .body("id", equalTo(createdId.intValue()));
    }

    // ─── Auth Failures ────────────────────────────────────────

    @Test
    @Order(10)
    @DisplayName("TC-010: No token — 401")
    void tc010_noToken_returns401() {
        given().contentType(ContentType.JSON).body("{}")
        .when().post("/api/v1/transactions")
        .then().statusCode(401);
    }

    @Test
    @Order(11)
    @DisplayName("TC-011: Viewer role — 403")
    void tc011_viewerRole_returns403() {
        given()
            .header("Authorization", "Bearer " + viewerToken())
            .contentType(ContentType.JSON).body("{}")
        .when().post("/api/v1/transactions")
        .then().statusCode(403);
    }
}
```

### 13.2 Common JWT Helper

```java
// src/test/java/.../helper/TestJwtHelper.java
public class TestJwtHelper {

    public static String adminToken() {
        return Jwt.preferredUserName("test-admin")
                .claim("eksad_role", "ROLE_ADMIN")
                .claim("eksad_tenant_id", "test-tenant")
                .claim("eksad_user_id", "user-001")
                .groups("ROLE_ADMIN")
                .issuer("eksad-auth-service")
                .sign();
    }

    public static String viewerToken() {
        return Jwt.preferredUserName("test-viewer")
                .claim("eksad_role", "ROLE_VIEWER")
                .groups("ROLE_VIEWER")
                .issuer("eksad-auth-service")
                .sign();
    }

    public static String tokenWithTenant(String tenantId) {
        return Jwt.preferredUserName("test-user")
                .claim("eksad_tenant_id", tenantId)
                .groups("ROLE_ADMIN")
                .issuer("eksad-auth-service")
                .sign();
    }
}
```

---

## 14. Master Data Service Testing

### Unit
- Repository CRUD on master entity (create, update, soft-delete).
- Hierarchical validation (parent exists before child create).
- Event payload structure (`eventType`, `tenantId`, `occurredAt`, `payload`).

### Integration (Testcontainers)
- Start PostgreSQL + RabbitMQ.
- `POST /api/v1/brands` → verify DB row inserted.
- Verify event published to `exc-master-data` with routing key `r.brand.created`.
- Batch endpoint `POST /api/v1/brands/batch` returns multiple by IDs.

```java
@QuarkusTest
@TestMethodOrder(OrderAnnotation.class)
class BrandResourceIT {
    @Test @Order(1)
    void create_shouldReturn201_andPublishEvent() {
        // RestAssured POST, capture body
        // verify on test queue that event arrived
    }
}
```

---

## 15. Cache Sync Testing

> Implementation pattern under test: `EKSAD_CACHE_SYNC_PATTERNS.md` Section 4 (Event Consumer) and Section 6 (Startup Sync).

### Unit
- Consumer receives valid event → upserts cache row.
- Stale event (`occurredAt < last_synced_at`) → skipped (no DB change).
- Unknown event type → logged + skipped, no exception.
- DELETE event → cache row removed.

### Integration
- Publish `BRAND.CREATED` to `exc-master-data` → assert `brand_cache` row exists.
- Empty cache on startup → mock master-data REST → verify bulk insert.
- Idempotency: publish same event twice → no duplicates.

```java
@QuarkusTest
class MasterDataEventConsumerIT {
    @Inject @Connector("smallrye-in-memory") InMemoryConnector connector;

    @Test
    void brandCreatedEvent_upsertsCache() {
        JsonObject evt = buildBrandCreatedEvent(42, "Toyota");
        connector.source("master-data-events").send(evt);
        await().untilAsserted(() ->
            assertThat(brandCacheRepository.findById(42L).await().indefinitely()).isNotNull());
    }
}
```

---

## 16. Multi-Tenancy Testing

### Unit
- Config inheritance: child overrides parent, parent overrides grandparent.
- Materialized path computation on create/move (`parent.path + "/" + id`).
- `TenantAwareRepository.findById(id)` throws `TenantContextMissingException`.

### Integration
- Tenant A creates data → Tenant B queries → empty result.
- Group admin query → sees all descendant data.
- Platform admin query → sees all data.
- Suspend group → all children JWT issuance blocked.
- Config override on child → effective config correct.

```java
@QuarkusTest
class TenantIsolationIT {
    @Test
    void tenantB_cannotSeeTenantA_data() {
        // create order with TenantContext=tenant-a
        // switch to TenantContext=tenant-b
        // GET /api/v1/orders → empty list
    }
}
```

---

## 17. Core Auth Testing

### Unit
- BCrypt password hash + compare.
- Lockout logic: 5 failed attempts → lock 15 min → auto-unlock.
- JWT signing with RS256, key rotation maintains old key for verification.
- Session limit: 4th login kicks oldest refresh token.
- **Device tracking:** 4th device login → `device_id` persisted in `refresh_tokens`; 5th login kicks the device with oldest `last_used_at`; device name stored as metadata.

### Integration (Testcontainers: PG + Mongo + Auth)
- Register credential → validate → issue token pair → refresh → revoke.
- JWT validation: valid → 200; expired → 401; wrong key → 401; tampered → 401.
- JWKS endpoint returns all non-expired keys.

### SDK
- WireMock `eksad-core-auth` endpoints.
- Verify SDK methods correctly map errors to `CoreAuthException` subclasses.

---

## 18. Security Testing

### Mandatory Auth Scenarios (Every Endpoint)
| Scenario | Expected |
|----------|----------|
| No `Authorization` header | 401 |
| Expired JWT | 401 |
| Invalid signature | 401 |
| Valid JWT, wrong role | 403 |
| Valid JWT, wrong tenant | 403 |
| Valid JWT, correct role + tenant | 2xx |

### Rate Limiting
- Login endpoint: 5/min per user_ref → 6th request → 429.

### JWT Manipulation Tests
| Scenario | Expected |
|----------|----------|
| Tamper JWT **header** (change `alg` to `none`) | 401 |
| Tamper JWT **payload** (change `eksad_tenant_id` to another tenant) | 401 |
| Tamper JWT **signature** (flip last byte) | 401 |
| Algorithm confusion attack (`alg=HS256` signed with public key) | 401 |
| Reuse revoked `access_token` after logout | 401 |
| Reuse revoked `refresh_token` after single-use | 401 |

```java
@Test
@DisplayName("JWT: tampered tenant claim → 401")
void jwt_tamperedTenantClaim_returns401() {
    // Build valid token, then Base64-decode payload, modify tenant_id, re-encode
    String tamperedToken = buildTamperedJwt("eksad_tenant_id", "malicious-tenant");

    given()
        .header("Authorization", "Bearer " + tamperedToken)
    .when()
        .get("/api/v1/orders")
    .then()
        .statusCode(401);
}
```

### Brute Force / Lockout Tests
| Scenario | Expected |
|----------|----------|
| 5 failed login attempts | last attempt → 401 |
| 6th attempt within lockout window | 429 or 401 with "Account locked" |
| Wait 15 min (simulate auto-unlock) | Login succeeds again |
| Lockout event logged in `auth_events` | Event type `ACCOUNT_LOCKED` present |

### Tenant Isolation (Deep)
| Scenario | Expected |
|----------|----------|
| Tenant A JWT used against Tenant B resource endpoint | 403 |
| Tenant A creates entity → query with Tenant B token → empty | 200 empty list |
| Platform admin JWT → sees data from both tenants | 200 with both |
| Group admin JWT → sees direct children only, not sibling group | 200 partial |

### Impersonation
| Scenario | Expected |
|----------|----------|
| Replay old Tenant A token after logout | 401 |
| Use Tenant A `refresh_token` to get Tenant B `access_token` | 401 |
| `eksad_user_id` in token doesn't exist in user registry | 401 |
| Forge `eksad_role=ROLE_PLATFORM_ADMIN` in payload | 401 (sig invalid) |

### OWASP Top 10 (Integration Checklist)
| # | OWASP Risk | Test Scenario | Status |
|---|-----------|---------------|--------|
| A01 | Broken Access Control | Cross-tenant read/write blocked (§16 Isolation tests) | per tenant isolation above |
| A02 | Cryptographic Failures | JWT signed RS256, password BCrypt ≥13 rounds | § 17 unit tests |
| A03 | Injection | SQL via path param (`/orders/1 OR 1=1`) | 400/404, no data leak |
| A05 | Security Misconfiguration | No `ddl-auto=update`, no hardcoded secrets | config review |
| A07 | Auth & Session Mgmt | Lockout, token revocation, session limit | §17 + §18 above |
| A09 | Logging & Monitoring Failures | Auth failures produce `auth_events` log entries | §17 integration |

---

## 19. Resilience Testing

| Test | Scenario |
|------|----------|
| `@Timeout` | Mock slow response (10s) → `TimeoutException` after 5s |
| `@Retry` | 2 failures + 1 success → method succeeds on 3rd attempt |
| `@Retry` `abortOn` | 4xx error → NOT retried |
| `@CircuitBreaker` | 50% failures across 10 calls → circuit OPEN |
| `@Fallback` | Circuit OPEN → fallback returns cached data |
| RabbitMQ DLQ | Consumer error 3× → message in DLQ |
| Health check | Stop dependency → `/q/health/ready=DOWN` |

```java
@QuarkusTest
class MasterDataClientResilienceIT {
    @InjectMock @RestClient MasterDataRestClient client;

    @Test
    void timeoutAfter5s() {
        when(client.listBrands()).thenAnswer(inv -> {
            Thread.sleep(10_000); return List.of();
        });
        assertThrows(TimeoutException.class, () -> client.listBrands());
    }
}
```

---

## 20. Observability Testing

| Test | Scenario |
|------|----------|
| Correlation ID extract | Existing `X-Correlation-ID` header → reused |
| Correlation ID generate | No header → UUID generated |
| MDC populated | `correlation_id`, `tenant_id` in log JSON |
| Propagation REST | Service A → Service B → same `correlation_id` in both logs |
| Propagation RMQ | Publish event with `correlation_id` → consumer logs match |
| Custom counter | Call login → `eksad_login_total{status="success"}` increments |
| Metrics endpoint | `GET /q/metrics` → Prometheus format |

---

## 21. Reserved Field Testing

| Test | Scenario |
|------|----------|
| Config cascade | Tenant override wins over domain default |
| Validation: required | Required field missing → `ValidationException` |
| Validation: regex | Pattern mismatch → `ValidationException` |
| Validation: hidden | Field hidden in config → skip validation |
| Validation: **conditional** | Trigger condition met (`reserved_str_2 == "EXPORT"`) → `reserved_str_3` becomes required → missing → `ValidationException` |
| Validation: **aggregate errors** | 3 fields invalid simultaneously → error list contains all 3 messages, not just first |
| Schema endpoint | `GET /api/v1/orders/_schema` returns correct per-tenant labels (13 slots) |
| Schema: **two-tenant** | Tenant A and Tenant B request `_schema` → receive different label configs, both valid |
| Persistence | Create order with reserved fields → all 13 columns populated correctly |
| **JSONB overflow** | `reserved_ext` stores `{"internal_code": "X42"}` → retrieve → value intact; 2nd key added → both keys present |
| **FE hook** | Schema endpoint returns `ReservedFieldConfig[]` with correct `slot/label/dataType/required` per tenant config |
| Two-tenant test | Same entity, two tenants → different schemas, both work |

---

## 22. Testcontainers — Extended Infrastructure

This section complements **Section 8** with multi-database, multi-broker setups required for the full EKSAD platform (core-auth, master-data, domain services, audit, observability).

### 22.1 PostgreSQL — Multiple Databases in One Container

Single PostgreSQL Testcontainer hosting per-service databases (mirrors Phase 1 deployment strategy — see `EKSAD_DB_DEPLOYMENT_STRATEGY.md`).

```java
public class PostgresTestResource implements QuarkusTestResourceLifecycleManager {

    private static final PostgreSQLContainer<?> POSTGRES =
        new PostgreSQLContainer<>("postgres:15-alpine")
            .withDatabaseName("eksad_init")
            .withUsername("eksad")
            .withPassword("eksad")
            .withInitScript("init-test-databases.sql");

    @Override
    public Map<String, String> start() {
        POSTGRES.start();
        String host = POSTGRES.getHost();
        Integer port = POSTGRES.getFirstMappedPort();
        return Map.ofEntries(
            Map.entry("quarkus.datasource.reactive.url",
                "postgresql://" + host + ":" + port + "/eksad_core_auth"),
            Map.entry("quarkus.datasource.username", "core_auth_user"),
            Map.entry("quarkus.datasource.password", "core_auth_pwd"),
            // override per @QuarkusTest profile for other services
            Map.entry("DB_HOST", host),
            Map.entry("DB_PORT", String.valueOf(port))
        );
    }

    @Override public void stop() { POSTGRES.stop(); }
}
```

`src/test/resources/init-test-databases.sql`:

```sql
-- One per service — keep in sync with prod init-databases.sql
CREATE DATABASE eksad_core_auth;
CREATE DATABASE eksad_master;
CREATE DATABASE eksad_pipeline;   -- example domain service

CREATE USER core_auth_user WITH PASSWORD 'core_auth_pwd';
CREATE USER master_user    WITH PASSWORD 'master_pwd';
CREATE USER pipeline_user  WITH PASSWORD 'pipeline_pwd';

GRANT ALL PRIVILEGES ON DATABASE eksad_core_auth TO core_auth_user;
GRANT ALL PRIVILEGES ON DATABASE eksad_master    TO master_user;
GRANT ALL PRIVILEGES ON DATABASE eksad_pipeline  TO pipeline_user;
```

### 22.2 MongoDB — Audit, User-Mgmt, Tenant-Mgmt

```java
public class MongoTestResource implements QuarkusTestResourceLifecycleManager {

    private static final MongoDBContainer MONGO =
        new MongoDBContainer("mongo:7.0");

    @Override
    public Map<String, String> start() {
        MONGO.start();
        return Map.of(
            "quarkus.mongodb.connection-string", MONGO.getReplicaSetUrl(),
            "quarkus.mongodb.database", "eksad_audit"
        );
    }

    @Override public void stop() { MONGO.stop(); }
}
```

Multiple logical DBs (`eksad_users`, `eksad_tenants`, `eksad_audit`) share the same container — selected per service via `quarkus.mongodb.database` override.

### 22.3 RabbitMQ — Auto-Declare Exchanges & Queues

```java
public class RabbitMQTestResource implements QuarkusTestResourceLifecycleManager {

    private static final RabbitMQContainer RABBIT =
        new RabbitMQContainer("rabbitmq:3.13-management")
            .withExchange("exc-log-activity", "direct")
            .withExchange("exc-master-data", "topic")
            .withExchange("exc-file-processing", "direct")
            .withQueue("q-audit-log")
            .withQueue("q-master-sync-pipeline")
            .withBinding("exc-master-data", "q-master-sync-pipeline",
                Map.of(), "r.brand.*", "queue");

    @Override
    public Map<String, String> start() {
        RABBIT.start();
        return Map.ofEntries(
            Map.entry("rabbitmq-host", RABBIT.getHost()),
            Map.entry("rabbitmq-port", String.valueOf(RABBIT.getAmqpPort())),
            Map.entry("rabbitmq-username", RABBIT.getAdminUsername()),
            Map.entry("rabbitmq-password", RABBIT.getAdminPassword())
        );
    }

    @Override public void stop() { RABBIT.stop(); }
}
```

### 22.4 Test Profile Composition

```java
@QuarkusTest
@QuarkusTestResource(PostgresTestResource.class)
@QuarkusTestResource(MongoTestResource.class)
@QuarkusTestResource(RabbitMQTestResource.class)
class FullStackIT { /* tests spanning DB + Mongo + RMQ */ }
```

### 22.5 Multi-Service Integration (`docker-compose-test.yml`)

For end-to-end test suites that need real running services (not just `@QuarkusTest`):

```yaml
version: "3.9"
services:
  postgres:
    image: postgres:15-alpine
    environment: { POSTGRES_USER: eksad, POSTGRES_PASSWORD: eksad }
    volumes: [ "./init-test-databases.sql:/docker-entrypoint-initdb.d/init.sql" ]
  mongo:
    image: mongo:7.0
  rabbit:
    image: rabbitmq:3.13-management
  core-auth:
    image: eksad/core-auth:test
    depends_on: [ postgres, mongo ]
  master-data:
    image: eksad/svc-master-data:test
    depends_on: [ postgres, rabbit ]
```

### 22.6 Spring Boot Equivalent

```java
@SpringBootTest
@Testcontainers
class FullStackIT {
    @Container static PostgreSQLContainer<?> POSTGRES = new PostgreSQLContainer<>("postgres:15-alpine");
    @Container static RabbitMQContainer RABBIT = new RabbitMQContainer("rabbitmq:3.13-management");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", POSTGRES::getJdbcUrl);
        r.add("spring.rabbitmq.host", RABBIT::getHost);
        r.add("spring.rabbitmq.port", RABBIT::getAmqpPort);
    }
}
```

---

## 23. Test Fixture Standards — Multi-Tenant

Every test that touches data MUST set tenant context first. This section defines the **mandatory** tenant fixture pattern.

### 23.1 Standard Constants

```java
public final class TestTenantConstants {
    public static final String TEST_TENANT_A = "tenant-test-001";
    public static final String TEST_TENANT_B = "tenant-test-002";
    public static final String TEST_GROUP    = "tenant-test-group";
    public static final String TEST_PLATFORM = "platform";
    public static final String TEST_USER     = "user-test-001";
    private TestTenantConstants() {}
}
```

### 23.2 `TestTenantContext` — CDI Alternative

```java
@Alternative
@Priority(1)
@RequestScoped
public class TestTenantContext extends TenantContext {

    private String tenantId = TestTenantConstants.TEST_TENANT_A;
    private String userId   = TestTenantConstants.TEST_USER;
    private String scope    = "tenant";

    public void switchTo(String tenantId)  { this.tenantId = tenantId; }
    public void switchToGroup()            { this.scope = "group"; }
    public void switchToPlatform()         { this.scope = "platform"; }

    @Override public String getTenantId()  { return tenantId; }
    @Override public String getUserId()    { return userId; }
    @Override public String getScope()     { return scope; }
}
```

Register in `src/test/resources/META-INF/beans.xml`:

```xml
<alternatives>
    <class>com.eksad.test.TestTenantContext</class>
</alternatives>
```

### 23.3 Mandatory Isolation Check (Every Repository Integration Test)

```java
@Test
@DisplayName("Tenant isolation: Tenant B cannot see Tenant A data")
void tenantIsolation_crossTenantQuery_returnsEmpty() {
    // 1. Set context to Tenant A
    testCtx.switchTo(TEST_TENANT_A);
    PipelineEntry created = repo.create(buildDto()).await().indefinitely();

    // 2. Switch context to Tenant B
    testCtx.switchTo(TEST_TENANT_B);
    List<PipelineEntry> resultB = repo.listAll().await().indefinitely();
    assertThat(resultB).isEmpty();

    // 3. Switch back to Tenant A → data still found
    testCtx.switchTo(TEST_TENANT_A);
    PipelineEntry resultA = repo.findById(created.getId()).await().indefinitely();
    assertThat(resultA).isNotNull();
}
```

### 23.4 Test Data Builder

```java
public class TestDataBuilder {
    private String tenantId = TEST_TENANT_A;
    private String userId   = TEST_USER;

    public static TestDataBuilder withTenant(String tenantId) {
        TestDataBuilder b = new TestDataBuilder();
        b.tenantId = tenantId;
        return b;
    }
    public TestDataBuilder withUser(String userId) { this.userId = userId; return this; }

    public PipelineEntryDTO createPipelineEntryDto(String name) {
        return PipelineEntryDTO.builder()
            .tenantId(tenantId)
            .createdBy(userId)
            .name(name)
            .createdAt(Instant.now().toEpochMilli())
            .build();
    }
    // ... factory methods per entity
}
```

Usage:

```java
PipelineEntryDTO dto = TestDataBuilder
    .withTenant(TEST_TENANT_A)
    .withUser(TEST_USER)
    .createPipelineEntryDto("Lead-001");
```

### 23.5 Hierarchy Access Fixtures

For tests that exercise group/platform scopes (see `EKSAD_MULTI_TENANCY_PATTERNS.md`):

```java
// Tenant under Astra group
testCtx.switchTo("tenant-ahm-001");
repo.create(...);

// Group admin of Astra → can see AHM
testCtx.switchTo("tenant-astra-group");
testCtx.switchToGroup();
assertThat(repo.listAll()).contains(ahmRow);

// Group admin of Sinar Mas → cannot see AHM
testCtx.switchTo("tenant-sinarmas-group");
testCtx.switchToGroup();
assertThat(repo.listAll()).doesNotContain(ahmRow);
```

### 23.6 Spring Boot Equivalent

```java
@TestConfiguration
public class TestTenantConfig {
    @Bean @Primary
    public TenantContext tenantContext() { return new TestTenantContext(); }
}

@SpringBootTest
@Import(TestTenantConfig.class)
class PipelineRepositoryTest { /* ... */ }
```

### 23.7 Mandatory Checklist (Add to Section 18 Code Review)

- [ ] Test class uses `TestTenantContext` (not the production CDI default)
- [ ] Every test method sets `tenantId` explicitly before data ops
- [ ] Repository integration tests include tenant isolation assertion
- [ ] Test data factories accept `tenantId` parameter
- [ ] No hardcoded tenant strings outside `TestTenantConstants`

---

## 24. Test Code Review Checklist

> Apply this checklist on **every PR** that adds or modifies test files. Groups are cumulative — check all that apply.

### 24.1 Multi-Tenancy Group
_(Required for every test touching DB data or repository layer)_

- [ ] Test class injects/activates `TestTenantContext` (CDI `@Alternative @Priority(1)`) — not the real context
- [ ] Every `@Test` method sets `tenantId` explicitly via `testCtx.switchTo(TEST_TENANT_A)` before any data operation
- [ ] At least one test asserts **cross-tenant isolation**: data created by Tenant A is NOT visible to Tenant B
- [ ] Test data builders accept `tenantId` parameter — no hardcoded `"tenant-001"` literals outside `TestTenantConstants`
- [ ] Group admin / platform admin scope tests use `testCtx.switchToGroup()` / `testCtx.switchToPlatform()` explicitly

### 24.2 Security Group
_(Required for every test touching REST Resource layer)_

- [ ] Every endpoint has at minimum: `no token → 401`, `wrong role → 403`, `correct role + tenant → 2xx`
- [ ] At least one test attempts **cross-tenant JWT reuse** (Tenant A JWT against Tenant B resource → 403)
- [ ] JWT manipulation test present for sensitive endpoints: tampered payload → 401
- [ ] Auth failure tests assert the correct HTTP status code (401 vs 403 distinction is intentional — do NOT collapse to generic 4xx)
- [ ] No hardcoded raw JWT strings in test code — use `TestJwtHelper.adminToken()` / `viewerToken()` etc.

### 24.3 Resilience Group
_(Required for every test touching external service calls or messaging)_

- [ ] `@Timeout` annotated methods have a test with mocked slow response → `TimeoutException` asserted
- [ ] `@Retry` annotated methods have a test with N-1 failures + 1 success → method succeeds on final attempt
- [ ] `@CircuitBreaker` annotated methods have a test forcing OPEN state → fallback or exception verified
- [ ] RabbitMQ consumer tests use `@Connector("smallrye-in-memory")` — never connect to real broker in unit tests
- [ ] `MockLogHandler` (no-op audit emitter) activated in integration tests — never assert on audit trail content in unit/integration tests

### 24.4 Reserved Field Group
_(Required for PRs touching transactional entities with reserved fields)_

- [ ] `ReservedFieldValidator` is invoked in service test — aggregate error semantics verified (all errors collected, not first-fail)
- [ ] Conditional validation test: trigger condition set → dependent field becomes required → missing → `ValidationException`
- [ ] PATCH null-handling verified: `null` reserved field in PATCH request does NOT overwrite existing value
- [ ] Config cascade test: tenant override > domain default > global default (3-tier verified in isolation)
- [ ] Schema endpoint test: `GET /api/v1/{entity}/_schema` returns 13-slot config with correct labels for test tenant
