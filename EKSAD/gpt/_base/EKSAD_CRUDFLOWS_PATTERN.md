# EKSAD CrudFlows — Repository Flow Pattern

**Status:** v2 (post-ASL-merge, May 2026)
**Applies to:** all EKSAD backend services using `eksad-core-common`

---

## Overview

`CrudFlows<E, D, I>` is the provider-agnostic interface that powers all EKSAD audit-aware CRUD
+ state-transition flows. It lives in `eksad-core-common` and ships in two flavours:

| Base class               | Persistence              | Entity bound                 |
|--------------------------|--------------------------|------------------------------|
| `BaseRepository`         | Hibernate Reactive Panache (PostgreSQL) | `extends BaseEntity`        |
| `BaseMongoRepository`    | Reactive Panache MongoDB | `extends BaseMongoDocument` |

Both implement `CrudFlows`, so the **flow API is identical** across providers.

---

## Why per-call `action` matters

Every flow method takes a humanish, report-friendly `action` string that lands in
`LogActivityDTO.action` verbatim. The machine-readable `moduleType` (dot-notation) is
stored alongside it for filtering.

```text
moduleType: EKSAD_SVC_LEADS.SPK.SUBMIT_APPROVAL    ← machine, dashboards
action:     Submit Approval SPK                    ← humanish, reports & emails
```

This means **one entity can have many distinct audit actions beyond CREATE/UPDATE/DELETE**
("Submit Approval", "Approve", "Reject", "Wanpres", "Update Invoice", …) — each producing
a clean line in the audit report.

---

## Paired ModuleType + ActionLabels interfaces

Define **two paired interfaces** per module:

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

Rules:
- ALWAYS `interface` — never `enum` (EKSAD §Module Type Constants).
- Canonical EN strings for `ActionLabels` v1 — i18n keys can be added later.
- Pair names by mirror: `XxxModuleType` ↔ `XxxActionLabels`.

---

## Flow surface — full reference

| Method | Use when | Audit action published |
|---|---|---|
| `createFlow(dto, action, extras…)` | new entity insertion | SUCCESS or FAIL |
| `updateFlow(dto, action, guard, errorFn, mutator)` | sync field update with state-machine guard | SUCCESS or FAIL |
| `updateFlowAsync(dto, action, guard, errorFn, handler)` | update that needs REST or another DB call mid-mutation | SUCCESS or FAIL |
| `deleteFlow(dto, action)` | soft delete (uses default `softDeleteMutator()`) | SUCCESS or FAIL |
| `deleteFlow(dto, action, deleter)` | soft delete with custom deleter | SUCCESS or FAIL |
| `commandFlow(dto, action, handler)` | command using primary DTO (`D`), no guard | SUCCESS or FAIL |
| `commandFlow(X, idFn, dtoIdFn, action, handler)` | command using auxiliary DTO type | SUCCESS or FAIL |
| `commandFlow(X, idFn, dtoIdFn, action, guard, errorFn, handler)` | guarded command, auxiliary DTO | SUCCESS or FAIL |
| `commandFlowMutator(X, idFn, dtoIdFn, action, guard, errorFn, mutator)` | sync mutator wrapped in update | SUCCESS or FAIL |

Wrap every state-transition mutator with `auditMutator(...)` so `updatedAt` / `updatedBy`
are always stamped — even if the caller forgets.

---

## Worked example — PostgreSQL (`BaseRepository`)

```java
@ApplicationScoped
public class SpkRepository extends BaseRepository<Spk, SpkDTO, Long> {

    @Override public String moduleType()                           { return SpkModuleType.SPK.UPDATE; }
    @Override public Long   toId(SpkDTO d)                         { return d.getId(); }
    @Override public String extractDtoId(SpkDTO d)                 { return d.getId() == null ? null : d.getId().toString(); }
    @Override public String extractTransactionId(Spk e)            { return e.getId().toString(); }

    @Override
    public Spk toNewEntity(SpkDTO d, Object... extras) {
        return Spk.builder()
            .tenantId(currentTenantId())                // EKSAD Principle 4
            .createdAt(now())                           // EKSAD Principle 7 (epoch ms)
            .createdBy(currentUser())
            .status(SpkStatus.DRAFT)
            .customerId(d.getCustomerId())
            .amount(d.getAmount())                      // BigDecimal — never Double/Float
            .build();
    }

    public Uni<Spk> create(SpkDTO d) {
        return createFlow(d, SpkActionLabels.SPK.CREATE);
    }

    public Uni<Spk> submitApproval(SpkDTO d) {
        return updateFlow(
            d, SpkActionLabels.SPK.SUBMIT_APPROVAL,
            e -> e.getStatus() == SpkStatus.DRAFT,
            e -> new ValidationException("SPK is not DRAFT (current: " + e.getStatus() + ")", 409),
            auditMutator(e -> e.setStatus(SpkStatus.WAITING_APPROVAL))
        );
    }

    public Uni<Spk> approve(SpkDTO d) {
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

    public Uni<Spk> delete(SpkDTO d) {
        return deleteFlow(d, SpkActionLabels.SPK.DELETE);   // uses default softDeleteMutator()
    }
}
```

---

## Worked example — MongoDB (`BaseMongoRepository`)

```java
@MongoEntity(collection = "auction")
public class Auction extends BaseMongoDocument {
    private String companyId;       // tenant — String for Mongo
    private String inventoryId;
    private TransactionStatus status;
    private BigDecimal auctionPrice;
    private Long auctionDate;       // epoch ms
}

@ApplicationScoped
public class AuctionRepository extends BaseMongoRepository<Auction, AuctionDTO, ObjectId> {

    @Override public String   moduleType()                           { return AuctionModuleType.AUCTION.UPDATE; }
    @Override public ObjectId toId(AuctionDTO d)                     { return new ObjectId(d.getId()); }
    @Override public String   extractDtoId(AuctionDTO d)             { return d.getId(); }
    @Override public String   extractTransactionId(Auction e)        { return e.id == null ? null : e.id.toString(); }

    @Override
    public Auction toNewEntity(AuctionDTO d, Object... extras) {
        Auction a = new Auction();
        a.setCompanyId(currentCompanyId());
        a.setCreatedAt(now());
        a.setCreatedBy(currentUser());
        a.setStatus(TransactionStatus.DRAFT);
        a.setInventoryId(d.getInventoryId());
        a.setAuctionPrice(d.getAuctionPrice());
        a.setAuctionDate(d.getAuctionDate());
        return a;
    }

    public Uni<Auction> create(AuctionDTO d) {
        return createFlow(d, AuctionActionLabels.AUCTION.CREATE);
    }

    public Uni<Auction> approve(AuctionDTO d) {
        return updateFlow(
            d, AuctionActionLabels.AUCTION.APPROVE,
            e -> e.getStatus() == TransactionStatus.WAITING_APPROVAL,
            e -> new ValidationException("Auction is not WAITING_APPROVAL", 409),
            auditMutator(e -> e.setStatus(TransactionStatus.APPROVED))
        );
    }
}
```

---

## Transaction boundary

Apply `@ReactiveTransactional` on the **service** method only — never on the flow methods
in the repository. Flows are transaction-agnostic so they compose cleanly with REST calls
and external messaging that the service layer orchestrates.

```java
@ApplicationScoped
@WithSession
public class SpkService {

    @Inject SpkRepository repository;

    @ReactiveTransactional
    public Uni<Spk> submitApproval(SpkDTO d) {
        return repository.submitApproval(d);   // ← repository flow runs inside this tx
    }
}
```

---

## Forbidden patterns

| ❌ | ✅ |
|---|---|
| Calling `persist(e)` or `update(e)` directly in a repository | Always go through `createFlow` / `updateFlow` / `deleteFlow` / `commandFlow` |
| Re-implementing audit fields inline in a mutator | Wrap with `auditMutator(...)` so `updatedAt`/`updatedBy` are auto-stamped |
| Hardcoding action strings inside flow calls | Always reference `XxxActionLabels.XXX.YYY` constants |
| Putting `@ReactiveTransactional` on the repository | Service layer only |
| Using `enum` for `ModuleType` or `ActionLabels` | Always `interface` of `String` constants |
