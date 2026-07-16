---
name: eksad-be-impl
description: Use when an EKSAD Backend Developer must implement or change a Java service from an approved FSD/TSD, including entities, DTOs, mappers, repositories, CrudFlows v2 operations, services, REST endpoints, Flyway migrations, messaging, configuration, and developer-owned tests. Resolves the SA-selected Framework, Paradigm, and Broker stack profile before writing code and enforces lightweight-VPS no-build constraints.
version: 1.0.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, backend, java21, quarkus, spring-boot, reactive, imperative, crudflows, flyway]
    related_skills: [eksad-tsd-design, eksad-code-review]
---

# EKSAD Backend Implementation

## Overview

Implement complete backend changes from approved requirements and design while preserving traceability and EKSAD platform patterns. The Backend Developer implements; the role does not redefine business requirements, architecture, release policy, or QA acceptance.

This VPS is an authoring and inspection environment, not a build machine. Produce source, configuration, migrations, and developer-owned tests here; execution and build evidence come from external CI or another approved build environment.

## When to Use

- Implement a backend feature described by an FSD and TSD.
- Add or change a Java entity, DTO, mapper, repository, service, or REST endpoint.
- Implement CrudFlows v2 CRUD or state transitions.
- Add a versioned Flyway migration.
- Implement a RabbitMQ or Kafka producer/consumer selected by the TSD.
- Add developer-owned unit or internal integration tests.
- Correct an implementation defect without changing approved behavior or architecture.

Do not use this skill to author or approve UR/BRD/FSD, choose a new stack profile, make architecture decisions, perform independent code-review approval, write QA-owned black-box suites, change CI/CD/infrastructure, authorize a release, or deploy.

## Required Knowledge and Inputs

Resolve `<EKSAD_PACK_ROOT>` in this order:

1. `EKSAD_PACK_SRC` when set and valid.
2. The active shared EKSAD knowledge deployment.
3. `~/.hermes/knowledge/eksad`.

Read before implementation:

1. `<EKSAD_PACK_ROOT>/role-system-instructions/developer-backend.md`
2. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md`
3. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md`
4. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_PATTERN.md`
5. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_TESTING_GUIDE.md`
6. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_SPRING_BOOT_MAPPINGS.md` when the selected framework is Spring Boot or a mapping is needed.
7. Applicable reserved-field, multi-tenancy, auth, event, resilience, observability, cache-sync, DB-deployment, and repository-strategy standards.
8. The exact approved FSD, TSD, API/event contracts, current repository code, parent/BOM constraints, and task scope.

Precedence is: **approved project TSD**, then the current applicable `EKSAD/gpt/_base/**` standards, then this skill/extracted role instruction, then examples or stale skeletons. The approved FSD remains authoritative for business behavior. If equal/higher-precedence sources conflict, identify the exact conflict and return it to the accountable owner rather than silently choosing behavior.

Minimum implementation inputs:

- repository/service and allowed paths;
- FSD version with relevant `FR-*`, acceptance criteria, business rules, errors, and state transitions;
- TSD version with classes/components, API/schema/event contracts, Stack Profile, and Flyway design;
- current source baseline/ref;
- requested change and exclusions.

Missing business behavior is a BA gap. Missing or contradictory technical design is an SA gap. Do not invent either to complete code.

## Role Boundary

| Area | Accountable owner | Backend Developer action |
|---|---|---|
| Business behavior and acceptance criteria | BA / Business Owner | Implement approved FSD; report ambiguity |
| Architecture, Stack Profile, schema/event design | SA / Design Authority | Follow approved TSD; return design gaps |
| Backend implementation and developer tests | Engineering Lead / Backend Developer | Write complete scoped code and tests |
| Technical/code verdict | Technical Leader | Supply implementation and self-check evidence; do not self-approve |
| QA plan, acceptance automation, QA verdict | QA / QA Lead | Preserve TC/RTM references and support defect resolution |
| CI/CD, environment, deployment evidence | DevOps | Provide source/config; do not operate deployment |
| Release authorization | Named Release Authority | Never infer or issue authorization |

A defect fix may change implementation only within approved behavior. A required contract, schema, state, security, or stack decision change must be handed back to the owning role before implementation proceeds.

## Stack Profile Resolution

The TSD selects three independent axes: **Framework**, **Paradigm**, and **Broker**. Record the declared profile before editing.

| Axis | Values | Default only when TSD is silent |
|---|---|---|
| Framework | Quarkus 3.30.6 / Spring Boot 3.x | Quarkus 3.30.6 |
| Paradigm | Reactive / Imperative | Reactive |
| Broker | RabbitMQ / Kafka | RabbitMQ |

When the TSD is silent, use the EKSAD default **Quarkus · Reactive · RabbitMQ** and mark that the default rule was applied. Do not select a non-default profile or rationale on behalf of the SA.

Apply the concrete profile consistently:

| Profile concern | Quarkus Reactive | Quarkus Imperative | Spring Boot Imperative | Spring Boot Reactive |
|---|---|---|---|---|
| Return model | `Uni<T>` / `Multi<T>` | blocking `T` | blocking `T` | `Mono<T>` / `Flux<T>` |
| Transaction | `@ReactiveTransactional` | `@Transactional` | `@Transactional` | reactive transaction manager per approved design |
| Authorization | `@RolesAllowed` | `@RolesAllowed` | `@PreAuthorize` | `@PreAuthorize` |
| Persistence base | reactive Panache mapping | blocking Panache mapping | Spring Data JPA mapping | reactive repository mapping |
| HTTP | Quarkus REST | Quarkus REST | Spring MVC | Spring WebFlux |

Use `EKSAD_BASE_PRINCIPLES.md` and `EKSAD_SPRING_BOOT_MAPPINGS.md` for exact mappings; do not extrapolate APIs absent from those sources or the project.

Broker changes transport, not the approved event envelope:

- RabbitMQ: approved exchange, queue, routing key, retry, and DLQ design.
- Kafka: approved topic, key/partition, consumer group, retry/DLT design.
- Preserve `tenantId` and all approved envelope fields.
- The audit-trail path follows the current EKSAD audit constraint; never manually bypass CrudFlows audit behavior.

## Implementation Workflow

### Step 1 — Establish Scope and Baseline

Inspect repository status, layout, current implementation, dependency/config files, and applicable project instructions. Capture:

- source ref and changed-path boundary;
- FSD/TSD versions and IDs in scope;
- declared/defaulted Stack Profile;
- endpoint, table, event, and state-machine surfaces affected;
- files expected to be created or modified;
- explicit exclusions and upstream gaps.

Do not overwrite unrelated work. Do not commit, push, switch branches, or broaden scope unless explicitly requested and authorized.

Completion criterion: every planned file maps to an approved requirement/design element and no unresolved blocking design gap remains.

### Step 2 — Build an Implementation Trace

Create a working trace before code:

| FR / rule | TSD reference | Component / method | Migration / config | Developer test | State |
|---|---|---|---|---|---|
| `{FR-ID}` | `{SECTION}` | `{CLASS#METHOD}` | `{FILE_OR_NA}` | `{TEST}` | planned / implemented / blocked |

Preserve existing IDs. Never create an FR, business rule, error code, role, state transition, queue/topic, table, or field merely to fill a blank.

Completion criterion: all requested behavior has an implementation target and test intent, or an explicit owner-tagged blocker.

### Step 3 — Implement Persistence and Contract Types

Implement in dependency order, as applicable:

1. Flyway migration under `src/main/resources/db/migration/` using the next repository-approved `V{N}__{description}.sql` sequence.
2. Entity extending the approved EKSAD base type.
3. Request/command and response DTOs.
4. MapStruct mapper; entities/documents never reach the presentation layer.
5. Reserved-field columns/config integration only when the approved TSD says the transactional entity opts in.

Mandatory invariant checks:

- Java 21 and project-pinned dependency versions;
- PostgreSQL for transactional data; MongoDB only for the EKSAD-approved service categories;
- `tenant_id` is `String` / `VARCHAR(100)` and every data path is tenant-scoped;
- timestamps persisted as epoch-millisecond `Long` / `BIGINT`;
- money is `BigDecimal` / `NUMERIC(20,4)`;
- soft delete, never hard delete, **except event-sourced `{entity}_cache` rows defined by `EKSAD_CACHE_SYNC_PATTERNS.md`**: cache entities do not extend `BaseEntity`, cache repositories do not use `BaseRepository`, cache tables have no soft-delete columns, and source DELETE events hard-delete the matching tenant-scoped cache row;
- Flyway only and DDL auto/generation disabled;
- required base audit fields and indexes from the approved schema/base standards;
- file references store approved file IDs, not storage keys or URLs;
- no raw secrets; use environment-variable references.

Completion criterion: data and contract code match the TSD and preserve all applicable platform invariants.

### Step 4 — Implement CrudFlows v2 Repository Behavior

For transactional repositories using `BaseRepository<E,D,I>` / approved equivalent:

- implement the five required hooks: `moduleType`, `toId`, `extractDtoId`, `extractTransactionId`, and `toNewEntity(D,Object... extras)`;
- pair `XxxModuleType` machine-code constants with mirrored `XxxActionLabels` human-readable constants; use interfaces, not enums;
- use `createFlow`, `updateFlow`, `updateFlowAsync`, `deleteFlow`, `commandFlow`, or `commandFlowMutator` according to the approved operation;
- pass the human-readable `ActionLabels` value to each flow and keep `moduleType()` as the machine-code fallback;
- wrap state-transition mutations with `auditMutator(...)`;
- derive tenant/user/time through the approved BaseRepository/context helpers;
- tenant-filter and soft-delete-filter every applicable query.

Never call direct persistence or hard-delete operations in a transactional repository in a way that bypasses CrudFlows and automatic audit behavior. The sole platform exception is a TSD-approved event-sourced cache table: use the cache standard's simple `PanacheRepositoryBase`/mapped equivalent, tenant-scope all operations, reject stale events, and hard-delete only the sourced cache row on its source DELETE event. Do not use `BaseRepository`, soft-delete columns, or standard CRUD audit flows for cache rows.

Completion criterion: every transactional write follows an approved audited flow and every transactional read is tenant/soft-delete safe; any cache-row exception follows the approved cache-sync design and tenant/stale-event controls.

### Step 5 — Implement Service and API Layers

Service:

- keep business orchestration in the service layer;
- use the transaction/session annotations selected by the Stack Profile;
- map entities to response DTOs;
- preserve approved validation, guards, error codes, state transitions, and external interaction order;
- avoid blocking calls in reactive paths.

REST resource/controller:

- apply authorization on every endpoint using the profile mapping;
- preserve `/api/v{N}/{resource}` and approved HTTP status behavior;
- return `GenericResponseDTO.success(...)` / approved failure mapping, never raw entities;
- implement only roles and payload fields documented by the FSD/TSD;
- validate JWT RS256 independently as specified by the approved architecture.

Completion criterion: endpoint behavior traces to the FSD, technical wiring traces to the TSD, and no presentation response exposes persistence objects.

### Step 6 — Implement Messaging and Cross-Cutting Concerns

When in scope:

- implement the selected RabbitMQ/Kafka transport from the TSD;
- preserve the universal envelope, event IDs, `tenantId`, actor, occurrence time, service ID, and approved payload;
- implement idempotency, stale-event handling, retries/DLQ/DLT, cache sync, resilience, health, correlation, logging, and metrics only as required by applicable approved standards/design;
- keep credentials and environment-specific values out of source;
- preserve the automatic Mongo-backed audit-trail integration rather than coupling the domain service to MongoDB.

Completion criterion: transport code matches the declared Broker axis and approved contract without altering business semantics.

### Step 7 — Add Developer-Owned Tests

Developer owns white-box unit tests and internal integration tests:

- service tests with Mockito;
- repository mapping/guard tests;
- resource/internal integration tests appropriate to the selected profile;
- reactive assertions for reactive code;
- Testcontainers wiring when already approved by the project;
- tenant fixture and cross-tenant isolation coverage for data-touching tests;
- guard pass/fail, field mapping, response wrapper, authorization, error, soft-delete, and state-transition coverage as applicable.

QA owns black-box API/acceptance, cross-service E2E, FE E2E, and non-functional suites. Do not place developer tests in QA-owned paths or claim a QA verdict.

Completion criterion: each implementation trace row identifies developer evidence and any QA handoff IDs.

### Step 8 — Static Verification on the VPS

Permitted verification is non-build inspection only:

- inspect changed files and `git diff`;
- check path/scope and repository status;
- parse Markdown/YAML/JSON/XML where a lightweight parser is available;
- search for placeholders, unauthorized direct persistence/hard delete, missing tenant filters, forbidden timestamp/money types, raw secrets, `ddl-auto=update`, entity exposure, and profile-mixing; verify every cache hard-delete is limited to a sourced `_cache` row and follows the cache-sync TSD/standard;
- verify migrations, imports, signatures, annotations, and test names by review.

**Do not run Maven, Gradle, npm, pnpm, yarn, Quarkus, Spring Boot, containers, tests, package resolution, application startup, or load tests on this VPS. Do not install a build toolchain.** A command not run is reported as `NOT RUN`, never as passed.

Completion criterion: static checks are reported honestly and build/test execution is explicitly delegated to external CI.

### Step 9 — Handoff

Return:

1. declared Stack Profile and its source/default status;
2. FSD/TSD versions and traceability IDs implemented;
3. exact files changed;
4. implementation trace status;
5. static verification performed and findings;
6. commands intentionally not run because of VPS constraints;
7. external CI checks required;
8. blockers, assumptions, and owner handoffs;
9. no-commit/no-push status unless explicitly requested otherwise.

Do not call the work production-ready, QA-passed, approved, or released based on source authoring alone.

## Hard Stops

Stop and hand off when:

- required FSD behavior, acceptance result, role, state, or error is absent/contradictory;
- the TSD Stack Profile, schema, event contract, or integration design conflicts with current code and no approved resolution exists;
- implementation would require changing production behavior outside scope;
- migration sequencing is ambiguous or risks collision;
- required common-library API/version cannot be verified;
- a secret or credential is discovered;
- requested work crosses into another role or forbidden path;
- verification would require executing a build on this VPS.

Use `TBD — Owner: <role/person> — Due: <date or explicit TBD>` for unresolved facts; classify each as blocking or non-blocking.

## Verification Checklist

- [ ] Developer role and path scope are explicit
- [ ] Approved FSD/TSD and current source inspected
- [ ] Framework · Paradigm · Broker profile recorded
- [ ] Every change traces to an approved ID/design element
- [ ] No business or architecture decision invented
- [ ] Java 21 / pinned framework conventions preserved
- [ ] `tenant_id`, soft delete, epoch timestamps, and money types correct; any hard-delete is only the sourced cache-row exception
- [ ] Cache entities/repositories avoid `BaseEntity`/`BaseRepository` and soft-delete columns as required
- [ ] CrudFlows v2 and paired ModuleType/ActionLabels used correctly
- [ ] Response DTO + mapper + `GenericResponseDTO` boundary preserved
- [ ] JWT RS256 authorization is applied per endpoint/design
- [ ] Flyway migration is versioned; no DDL auto-update
- [ ] Broker implementation matches the TSD and envelope
- [ ] Reserved fields applied only to approved opt-in entities
- [ ] Developer-owned tests supplied; QA ownership not claimed
- [ ] No hard-coded secret or raw storage location
- [ ] Only static VPS verification performed
- [ ] Maven/Gradle/npm and runtime execution reported `NOT RUN`
- [ ] External CI handoff and blockers are explicit
- [ ] No commit or push unless explicitly authorized

## Phase F Enrichment — Backend Patterns and TDD Workflow

Adapted benchmark patterns: backend-patterns, API design, tdd-workflow.

- Start from approved FSD/TSD only; if design is missing, hand off to BA/SA instead of inventing contracts.
- Preserve EKSAD backend invariants: tenant isolation, soft delete, audit trail, reserved fields, DTO/mapping boundaries, and CrudFlows/BaseRepository conventions.
- Prefer test-first implementation notes for every behavioral change; when tests cannot run in this workspace, document the exact CI/local command and expected evidence.
- Use API design guardrails for resource names, status codes, errors, pagination, and versioning.
