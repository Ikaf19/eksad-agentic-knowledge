````markdown
# EKSAD CrudFlows — JPA / Blocking Flow Pattern

**Status:** v1 (June 2026 — `eksad-core-jpa` split)
**Applies to:** all EKSAD backend services using the `eksad-core-jpa` artifact
**Counterpart:** `EKSAD_CRUDFLOWS_PATTERN.md` (reactive — `eksad-core-reactive`)
**ADR:** `_base/ADR_EKSAD_CORE_COMMON_SPLIT.md`

---

## Overview

`CrudFlows<E, D, I>` is the provider-agnostic interface that powers all EKSAD audit-aware
CRUD + state-transition flows. The **blocking / JPA** implementation lives in
`eksad-core-jpa` and supports two runtimes:

| Runtime | Framework binding | Entity bound |
|---------|-------------------|--------------|
| **Spring Boot · Imperative** | Spring Data JPA + `@Transactional` | `extends BaseEntity` |
| **Quarkus · Imperative** | Quarkus blocking + `@Transactional` (Panache JPA) | `extends BaseEntity` |

Both consume the **same `BaseJpaRepository<E, D, I>`** base class, so the
**flow API and audit envelope are identical** across both runtimes — and identical to the
reactive `BaseRepository` counterpart. Only the method return type (`T` vs `Uni<T>`) and
transaction annotation differ.

### Dependency graph

```
eksad-core-api          ← contracts only (DTO, CrudFlows interface, GenericResponseDTO)
      ▲
eksad-core-jpa          ← blocking impl (BaseJpaRepository, BaseEntity, auditMutator)
      ▲                 ← depends on: eksad-core-api + jakarta.persistence + jakarta.transaction
eksad-core-spring-boot-starter   ← Spring DI wiring on top of eksad-core-jpa
eksad-core-quarkus-starter       ← Quarkus CDI wiring on top of eksad-core-jpa (imperative)
```

> **Rule:** never import `eksad-core-reactive` in an imperative service — the reactive
> runtime (Mutiny, Panache-reactive) must not be on the classpath of a blocking service.

---

## Why the flow API stays identical

Every flow publishes the same `LogActivityDTO` envelope regardless of runtime:

```text
moduleType: EKSAD_SVC_LEADS.SPK.SUBMIT_APPROVAL    ← machine code, dashboards
action:     Submit Approval SPK                    ← humanish label, audit reports
```

The `eksad-core-audittrail` consumer (MongoDB) receives the same JSON regardless of
whether the producer is reactive, Spring Boot, or Quarkus-imperative. This is why the
blocking base is a **separate artifact**, not a reuse of the reactive jar.

---

## Paired ModuleType + ActionLabels interfaces

Identical convention to the reactive pattern — no change:

```java
// Machine codes — used for filtering, dashboards, RBAC mapping
public interface SpkModuleType {
    String PREFIX = "EKSAD_SVC_LEADS";
    interface SPK {
        String CREATE           = PREFIX + ".SPK.CREATE";
        String UPDATE           = PREFIX + ".SPK.UPDATE";
        String DELETE           = PREFIX + ".SPK.DELETE";
        String SUBMIT_APPROVAL  = PREFIX + ".SPK.SUBMIT_APPROVAL";
        String APPROVE          = PREFIX + ".SPK.APPROVE";
        String REJECT           = PREFIX + ".SPK.REJECT";
    }
}

// Humanish labels — used in audit reports, email notifications, history UI
public interface SpkActionLabels {
    interface SPK {
        String CREATE           = "Create SPK";
        String UPDATE           = "Update SPK";
        String DELETE           = "Delete SPK";
        String SUBMIT_APPROVAL  = "Submit Approval SPK";
        String APPROVE          = "Approve SPK";
        String REJECT           = "Reject SPK";
    }
}
```

Rules: ALWAYS `interface`, never `enum`. Mirror keys 1-to-1 between `XxxModuleType` and
`XxxActionLabels`.

---

## Flow surface — full reference (blocking)

All method names are **identical** to the reactive surface. The return type is `T`
(blocking) instead of `Uni<T>`.

| Method | Use when | Audit action published |
|---|---|---|
| `createFlow(dto, action, extras…)` | new entity insertion | SUCCESS or FAIL |
| `updateFlow(dto, action, guard, errorFn, mutator)` | sync field update with state-machine guard | SUCCESS or FAIL |
| `deleteFlow(dto, action)` | soft delete (uses default `softDeleteMutator()`) | SUCCESS or FAIL |
| `deleteFlow(dto, action, deleter)` | soft delete with custom deleter | SUCCESS or FAIL |
| `commandFlow(dto, action, handler)` | command using primary DTO (`D`), no guard | SUCCESS or FAIL |
| `commandFlow(X, idFn, dtoIdFn, action, handler)` | command using auxiliary DTO type | SUCCESS or FAIL |
| `commandFlow(X, idFn, dtoIdFn, action, guard, errorFn, handler)` | guarded command, auxiliary DTO | SUCCESS or FAIL |
| `commandFlowMutator(X, idFn, dtoIdFn, action, guard, errorFn, mutator)` | sync mutator wrapped in update | SUCCESS or FAIL |

> `updateFlowAsync` is **not available** in the blocking flavour — there is no async
> mid-mutation in a blocking transaction. Use `updateFlow` + a synchronous REST/DB call
> inside the mutator if needed.

Wrap every state-transition mutator with `auditMutator(...)` so `updatedAt` / `updatedBy`
are always stamped — even if the caller forgets.

---

## Worked example — Spring Boot (`BaseJpaRepository`)

```java
// ─── Repository ───────────────────────────────────────────────────────────────
@Repository
public class SpkRepository extends BaseJpaRepository<Spk, SpkDTO, Long> {

    @Override public String moduleType()                       { return SpkModuleType.SPK.UPDATE; }
    @Override public Long   toId(SpkDTO d)                     { return d.getId(); }
    @Override public String extractDtoId(SpkDTO d)             { return d.getId() == null ? null : d.getId().toString(); }
    @Override public String extractTransactionId(Spk e)        { return e.getId().toString(); }

    @Override
    public Spk toNewEntity(SpkDTO d, Object... extras) {
        return Spk.builder()
            .tenantId(currentTenantId())        // BaseJpaRepository helper — NEVER getUserContext()
            .createdAt(now())                   // epoch ms — EKSAD Principle 7
            .createdBy(currentUser())
            .status(SpkStatus.DRAFT)
            .customerId(d.getCustomerId())
            .amount(d.getAmount())              // BigDecimal — never Double/Float
            .build();
    }

    public Spk create(SpkDTO d) {
        return createFlow(d, SpkActionLabels.SPK.CREATE);
    }

    public Spk submitApproval(SpkDTO d) {
        return updateFlow(
            d, SpkActionLabels.SPK.SUBMIT_APPROVAL,
            e -> e.getStatus() == SpkStatus.DRAFT,
            e -> new ValidationException("SPK is not DRAFT (current: " + e.getStatus() + ")", 409),
            auditMutator(e -> e.setStatus(SpkStatus.WAITING_APPROVAL))
        );
    }

    public Spk approve(SpkDTO d) {
        return updateFlow(
            d, SpkActionLabels.SPK.APPROVE,
            e -> e.getStatus() == SpkStatus.WAITING_APPROVAL,
            e -> new ValidationException("SPK is not WAITING_APPROVAL", 409),
            auditMutator(e -> {
                e.setStatus(SpkStatus.APPROVED);
                e.setApprovedAt(now());
                e.setApprovedBy(currentUser());
            })
        );
    }

    public Spk delete(SpkDTO d) {
        return deleteFlow(d, SpkActionLabels.SPK.DELETE);
    }
}

// ─── Service (Spring Boot) ────────────────────────────────────────────────────
@Service
public class SpkService {

    private final SpkRepository repository;
    private final SpkMapper     mapper;

    public SpkService(SpkRepository repository, SpkMapper mapper) {
        this.repository = repository;
        this.mapper     = mapper;
    }

    @Transactional                              // ← @Transactional on write methods only
    public SpkResponseDTO submitApproval(SpkDTO d) {
        return mapper.toResponseDto(repository.submitApproval(d));
    }

    public SpkResponseDTO findById(Long id) {  // ← read: no @Transactional
        return mapper.toResponseDto(repository.findByIdAndTenant(id, currentTenantId()));
    }
}

// ─── REST Controller (Spring Boot) ───────────────────────────────────────────
@RestController
@RequestMapping("/api/v1/spk")
public class SpkController {

    private final SpkService service;

    @PutMapping("/{id}/submit")
    @PreAuthorize("hasRole('ROLE_SUBMITTER')")  // ← REQUIRED on every method — no exceptions
    public ResponseEntity<GenericResponseDTO<SpkResponseDTO>> submitApproval(
            @PathVariable Long id, @RequestBody SpkDTO dto) {
        dto.setId(id);
        return ResponseEntity.ok(GenericResponseDTO.success(service.submitApproval(dto)));
    }
}
```

---

## Worked example — Quarkus · Imperative (`BaseJpaRepository`)

The repository is **identical** to the Spring Boot example above — only the service and
resource annotations change.

```java
// ─── Service (Quarkus-imperative) ────────────────────────────────────────────
@ApplicationScoped
public class SpkService {

    @Inject SpkRepository repository;
    @Inject SpkMapper     mapper;

    @Transactional                              // ← jakarta.transaction.Transactional (blocking)
    public SpkResponseDTO submitApproval(SpkDTO d) {
        return mapper.toResponseDto(repository.submitApproval(d));
    }

    public SpkResponseDTO findById(Long id) {
        return mapper.toResponseDto(repository.findByIdAndTenant(id, currentTenantId()));
    }
}

// ─── REST Resource (Quarkus-imperative) ──────────────────────────────────────
@Path("/api/v1/spk")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class SpkResource {

    @Inject SpkService service;

    @PUT
    @Path("/{id}/submit")
    @RolesAllowed("ROLE_SUBMITTER")             // ← REQUIRED on every method — no exceptions
    public Response submitApproval(@PathParam("id") Long id, SpkDTO dto) {
        dto.setId(id);
        return Response.ok(GenericResponseDTO.success(service.submitApproval(dto))).build();
    }
}
```

---

## Reactive vs Blocking — quick reference

| Aspect | Reactive (`eksad-core-reactive`) | Blocking JPA (`eksad-core-jpa`) |
|--------|----------------------------------|---------------------------------|
| Base class | `BaseRepository<E,D,I>` | `BaseJpaRepository<E,D,I>` |
| Return type | `Uni<T>` | `T` |
| Transaction | `@ReactiveTransactional` (service) | `@Transactional` (service) |
| Session | `@WithSession` on service class | Not needed |
| REST return | `Uni<Response>` | `Response` / `ResponseEntity<T>` |
| `updateFlowAsync` | ✅ available | ❌ not available (use sync updateFlow) |
| Audit envelope | Identical `LogActivityDTO` | Identical `LogActivityDTO` |
| `auditMutator` | Required | Required |
| Paired interfaces | Required | Required |
| `currentTenantId()` | BaseRepository helper | BaseJpaRepository helper |

---

## Transaction boundary

Apply `@Transactional` on the **service** method only — never on the repository flows.
Flows are transaction-agnostic so they compose cleanly within the service transaction.

```java
// ✅ Correct — transaction on service
@Transactional
public SpkResponseDTO approve(SpkDTO d) {
    return mapper.toResponseDto(repository.approve(d));   // flow runs inside this tx
}

// ❌ Wrong — transaction on the repository method
@Transactional                      // ← NEVER annotate repository methods
public Spk approve(SpkDTO d) { ... }
```

---

## Forbidden patterns

| ❌ Forbidden | ✅ Correct | Why |
|---|---|---|
| `repository.save(entity)` / `entityManager.persist(e)` directly | Always go through `createFlow` / `updateFlow` / `deleteFlow` / `commandFlow` | Bypasses audit trail — audit silently does not fire |
| Re-implementing audit fields inline in a mutator | Wrap with `auditMutator(...)` | Raw mutator does not stamp `updatedAt`/`updatedBy` |
| Hardcoding action strings inside flow calls | Always reference `XxxActionLabels.XXX.YYY` constants | Hard-coded strings diverge from audit reports |
| `@Transactional` on the repository method | Service layer only | Creates nested transaction nesting issues |
| `enum` for `ModuleType` or `ActionLabels` | Always `interface` of `String` constants | EKSAD standard — enums cannot be extended |
| Importing `eksad-core-reactive` jar in an imperative service | Import `eksad-core-jpa` | Reactive runtime (Mutiny) blocks classpath; wrong contract |
| `getUserContext().getTenantId()` in repository | `currentTenantId()` BaseJpaRepository helper | Helpers are mockable in unit tests |
| `private Long tenantId` on entity | `private String tenantId` (`VARCHAR(100)`) | tenant_id is always String — EKSAD Principle 4 (D1) |
| `updateFlowAsync(...)` | `updateFlow(...)` + synchronous call inside mutator | Async variant not available in blocking flavour |
````
