# ADR — Split `eksad-core-common` (Reactive vs Imperative/Spring)

**Status:** Accepted
**Date:** 2026-06-02
**Owner:** EKSAD Platform Team
**Supersedes:** monolithic `eksad-core-common` (single JAR pulling Hibernate Reactive)
**Source:** Notion brainstorming — decisions **D1–D5** + implementation guidance **G1–G5**

---

## Context

`eksad-core-common` currently ships as a **single JAR** that pulls
`quarkus-hibernate-reactive-panache`. This is a problem for:

- **MongoDB-only services** (e.g. `eksad-core-audittrail`) — the Hibernate Reactive
  transitive dependency conflicts with the MongoDB-only stack, forcing them to **fork a
  local `GenericResponseDTO`** instead of importing from common.
- **Imperative / Spring Boot services** — they cannot reuse the reactive `BaseRepository`
  (it returns `Uni<T>` and binds Mutiny/Panache-reactive). The earlier claim
  *"BaseRepository is used in Spring Boot too"* was **incorrect** (corrected per **G2**).
- **Quarkus-imperative services** — a valid Tier-2 profile (blocking `T` + `@Transactional`)
  that also needs the audit-aware flows without the reactive runtime.

The CrudFlows **flow API and audit envelope must stay identical** across all paradigms so
audit reports, dashboards, and `LogActivityDTO` ingestion remain uniform.

---

## Decision

### 1. Split into layered modules (D4 — Option B, refined naming)

| Module | Contains | Framework binding |
|--------|----------|-------------------|
| `eksad-core-api` | DTO contracts, `GenericResponseDTO`, `PageMetadata`, `CrudFlows<E,D,I>` interface, `ModuleType`/`ActionLabels` conventions, `UserContext` abstraction | **None** (pure Java + `jakarta.*` annotations only) |
| `eksad-core-reactive` | Quarkus reactive impl — `BaseRepository` (Hibernate Reactive Panache) + `BaseMongoRepository` (Panache Mongo), Mutiny `Uni<T>` flows | Quarkus reactive |
| `eksad-core-jpa` | **Blocking JPA** CrudFlows impl — framework-neutral, depends only on `jakarta.persistence` + `jakarta.transaction`; returns `T`, uses `@Transactional` | **None** beyond `jakarta.*` — reused by both imperative runtimes |
| `eksad-core-spring-boot-starter` | Spring auto-configuration / DI wiring on top of `eksad-core-jpa` | Spring Boot |
| `eksad-core-quarkus-starter` *(optional)* | Quarkus CDI producers / config wiring (serves reactive **and** Quarkus-imperative) | Quarkus |

**Dependency direction:** `*-reactive`, `*-jpa`, and the starters all depend on
`eksad-core-api`. The two starters depend on the matching impl module. No impl module
depends on another impl module.

### 2. Paradigm scope (D3) — three supported profiles

Imperative is **not** Spring-only. Supported profiles:

| Profile | Modules pulled |
|---------|----------------|
| Quarkus · Reactive (default) | `eksad-core-api` + `eksad-core-reactive` (+ `eksad-core-quarkus-starter`) |
| Quarkus · Imperative | `eksad-core-api` + `eksad-core-jpa` + `eksad-core-quarkus-starter` |
| Spring Boot · Imperative | `eksad-core-api` + `eksad-core-jpa` + `eksad-core-spring-boot-starter` |

The blocking core (`eksad-core-jpa`) is **shared** by Quarkus-imperative and Spring Boot —
only the thin starter (DI + transaction wiring) differs.

### 3. Imperative artifact name (D2)

The imperative blocking core is named **`eksad-core-jpa`** (not `eksad-core-spring`) —
it is framework-neutral and intentionally **does not reuse the reactive jar** (per G2).

### 4. `tenant_id` type (D1)

Locked to **`String` / `VARCHAR(100)`** everywhere — DB columns, JWT claim, RabbitMQ
messages, and all KB worked-examples. The `version` optimistic-lock column is dropped from
the standard template; `deleted_by` is `VARCHAR(100)`.

### 5. Parent (`eksad-parent`)

**Not split.** `eksad-parent` remains a single **published BOM** managing the versions of
all `eksad-core-*` modules and shared dependencies (EKSAD Principle 14 — BOM, never a
monorepo reactor). Each service repo imports the BOM and selects only the modules it needs.

---

## Consequences

**Positive**
- MongoDB-only services import `eksad-core-api` for `GenericResponseDTO` — **local fork
  removed**.
- Imperative services (Spring **and** Quarkus) get audit-aware flows with identical
  envelope, no reactive runtime.
- Clear dependency boundaries; no accidental Hibernate-Reactive leakage.

**Negative / cost**
- Migration: existing `eksad-core-common` consumers must repoint to the right module(s).
- More artifacts to release — mitigated by the single `eksad-parent` BOM.
- `eksad-core-jpa` must keep its public flow API in lockstep with `eksad-core-reactive`.

**Follow-ups**
- Author `EKSAD_CRUDFLOWS_JPA.md` — the blocking counterpart to `EKSAD_CRUDFLOWS_PATTERN.md`
  (D4 note).
- Provide a migration guide for current `eksad-core-common` dependents.
- Decide deprecation timeline for the legacy `eksad-core-common` JAR.

---

## Related KB changes (this batch)

- `vibe-coding/PLAN_FIRST_WORKFLOW.md`, `vibe-coding/developer/CURSOR_DEV_RULES.md` — D1/G1/G3.
- `vibe-coding/developer/COPILOT_DEV_INSTRUCTIONS.md`, `CLAUDE_CODE_DEV_INSTRUCTIONS.md` — G2.
- All active instruction/setup primers — Quarkus `3.30.6` (G5).
- `system-analyst/SA_SYSTEM_INSTRUCTIONS.md` (+ `_SHORT`) — D5 SA policy.
- `_base/EKSAD_CRUDFLOWS_PATTERN.md` registered in `README.md`.
