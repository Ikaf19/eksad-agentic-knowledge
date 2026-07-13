---
name: eksad-adr-workflow
description: Use when an EKSAD technical decision has material architectural impact, durable trade-offs, multiple viable options, cross-service or platform consequences, a security or operational boundary, or needs an explicit approver and supersession history. Produces evidence-linked Architecture Decision Records without replacing TSD approval or specialist authority.
version: 1.0.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, adr, architecture, governance, decision, trade-off, supersession]
    related_skills: [eksad-tsd-design, eksad-appsec-review]
---

# EKSAD ADR Workflow

## Purpose

Create and govern durable EKSAD architecture decisions. An ADR records context, constraints, options, evidence, trade-offs, decision authority, consequences, and lifecycle. It complements the TSD: the ADR explains **why a material choice was made**; the TSD specifies **how the approved design is implemented**.

Use `<EKSAD_PACK_ROOT>` for the canonical EKSAD repository, resolved from `EKSAD_PACK_SRC` when valid, otherwise the active shared deployment, otherwise `~/.hermes/knowledge/eksad`.

## Required References

- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/EKSAD_GENERIC_ADR_TEMPLATE.md`
- Relevant approved BRD/FSD/TSD, NFRs, domain registry, security review/threat model, operational evidence, and existing ADRs.

## ADR Decision Triggers

Create an ADR when one or more apply:

- More than one viable option has materially different cost, risk, operability, security, performance, or maintainability consequences.
- A choice changes service boundaries, data ownership, integration style, stack profile, broker, gateway mode, tenancy model, identity/trust boundary, or a shared platform contract.
- The choice introduces or changes an external dependency, infrastructure component, data store, migration strategy, compatibility promise, or irreversible/high-cost commitment.
- The design requests an exception to an EKSAD default or needs an explicit risk owner/approver.
- A prior accepted ADR is no longer valid and must be superseded or deprecated.

Do not create an ADR for routine implementation details already determined by an accepted standard, formatting preferences, or a reversible local choice with no durable consequence. Link such choices in the TSD decision log instead.

## Non-Negotiable Boundary

An ADR cannot waive EKSAD principles merely by being accepted. Preserve all EKSAD non-negotiables, including tenant isolation, Flyway-only DDL, soft delete and audit columns, epoch-millisecond timestamps, `BigDecimal`/`NUMERIC(20,4)` for money, `BaseRepository` audit flows, per-endpoint authorization, fixed service names, and signatures-only TSD skeletons. Any exception requires the named EKSAD authority and an explicit, scoped, expiring exception record; absent authority, status is `Blocked`, not `Accepted`.

## Canonical Lifecycle

Allowed transitions are deterministic:

| From | Allowed next state | Rule |
|---|---|---|
| `Proposed` | `In Review` | Required context/options are ready for affected-owner review. |
| `In Review` | `Accepted` or `Rejected` | Only the named decision authority records either outcome. |
| `Accepted` | `Superseded` or `Deprecated` | `Superseded` requires an accepted successor ADR; `Deprecated` retires the decision for new work without implying a replacement. |
| `Rejected` | None | Rejection is terminal. A materially revised proposal receives a new ADR ID. |
| `Superseded` | None | Terminal historical state; retained scope is recorded in the successor links. |
| `Deprecated` | None | Terminal historical state; replacement or retirement plan is recorded. |

- **Proposed:** author has supplied context, options, initial recommendation, and evidence gaps.
- **In Review:** affected owners and specialists are reviewing; unresolved items retain owner and due date.
- **Accepted:** the named decision authority records decision, date, rationale, conditions, and evidence. Recommendation is not approval.
- **Rejected:** authority declines the proposal; retain rationale and record subsequent path.
- **Superseded:** a newer accepted ADR replaces all or part of this ADR. Link both directions and state retained scope.
- **Deprecated:** an accepted decision remains historical but must not govern new work; record replacement or retirement plan.

Never rewrite an accepted ADR to make a new outcome appear original. Preserve history, create a new ADR, and use supersession links. Editorial corrections that do not alter the decision may increment the document version and must be recorded in revision history.

## Workflow

### 1. Establish Scope and Trigger

Assign immutable `ADR-{PROJECT_CODE}-{NNN}`, name the file exactly `ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md`, and record title, owner, affected services/domains, trigger, related requirement/TSD IDs, and target decision date. Search for duplicate or conflicting ADRs first.

### 2. Record Context and Constraints

Separate facts, approved constraints, assumptions, and unknowns. Cite evidence locations and freshness. Capture EKSAD principles and NFRs that constrain the decision. Unknown mandatory input becomes `TBD — Owner — Due Date`; do not silently convert it to fact.

### 3. Define Options Fairly

Include the status quo where viable and at least one genuine alternative. For each option assess:

- EKSAD alignment and requirement traceability;
- security/trust boundaries and tenant/data exposure;
- reliability, failure modes, observability, and supportability;
- migration, compatibility, rollback/reversibility, and lock-in;
- performance, capacity, delivery effort, and total operating cost;
- dependency/supply-chain and ownership implications.

Do not manufacture precision. Label estimates and assumptions.

### 4. Obtain Specialist Checkpoints

Any role may raise a security trigger or supply evidence. The System Analyst or Technical Leader coordinates and invokes the shared `eksad-appsec-review` workflow and uses `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md`; AppSec is not a profile. Obtain data, DevOps, QA, privacy/compliance, or business input when their authority is affected. Specialists supply evidence and recommendations; only the named decision authority accepts/rejects the ADR, and only the named risk authority accepts residual risk or grants a waiver.

### 5. Recommend and Decide

State the recommended option and why its benefits outweigh known drawbacks under the recorded constraints. The decision record must name approver role/person, decision, date, conditions, evidence, and any time-bound review trigger. Missing authority remains `In Review` or `Blocked`.

### 6. Propagate the Decision

After acceptance, update or link the TSD, architecture document, backlog, threat model, migration/rollback plan, operational runbook, and affected contracts. Record owners and evidence. Acceptance without propagation is incomplete.

### 7. Review and Supersede

Review when an explicit date arrives or when assumptions, NFRs, security posture, dependency support, service boundaries, or operating evidence materially change. Create a successor ADR for a changed decision and mark the predecessor `Superseded` only after successor acceptance.

## Completion Gate

- [ ] Trigger and scope are explicit; no duplicate/conflicting ADR is unaddressed.
- [ ] Context distinguishes fact, assumption, constraint, and unknown.
- [ ] Viable options and status quo are compared with balanced trade-offs.
- [ ] Security, observability, migration, compatibility, rollback, and supply-chain impact are addressed.
- [ ] EKSAD non-negotiables remain intact.
- [ ] Decision authority, outcome, date, rationale, conditions, and evidence are present.
- [ ] TSD/requirements/threat-model links and propagation owners are present.
- [ ] Supersession and review triggers are explicit.

## Output

Use `EKSAD_GENERIC_ADR_TEMPLATE.md`. Return ADR ID/status, trigger, recommendation, decision authority/state, key evidence, unresolved items with owners/dates, and propagation actions. Never report `Accepted` from author recommendation alone.
