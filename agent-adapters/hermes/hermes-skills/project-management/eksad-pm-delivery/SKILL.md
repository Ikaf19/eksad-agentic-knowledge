---
name: eksad-pm-delivery
description: "Use when an EKSAD Project Manager must initiate, plan, monitor, control, or close a software-delivery project; produce Charter, Plan, WBS baseline, RAID, status, or Change Request artifacts; coordinate cross-role dependencies; or assess stage-gate readiness without taking ownership from BA, architecture, engineering, or QA specialists."
version: 1.2.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, project-management, delivery, raid, governance, stage-gates]

---

# EKSAD Project Manager Delivery Workflow

## Overview

Run evidence-based EKSAD project governance from initiation through closure. This skill creates and maintains PM-owned artifacts while preserving specialist ownership:

- PM owns Charter, Plan, the WBS artifact and approved WBS baseline, RAID, status, changes, decisions, escalations, and gate coordination.
- BA owns UR, BRD, and FSD.
- System Analyst/Solution Architect owns architecture and TSD.
- Technical Leader owns technical/code review.
- Developers are responsible for implementation and technical estimates; Engineering Lead is accountable for implementation delivery.
- QA owns test design/execution; Business Owner owns business acceptance.

Use the strict gate contract in this skill when dependent stages require visible persisted state and human decisions. PM supervises the gates; PM does not become the author or approver of specialist artifacts.

## When to Use

- Start a new EKSAD project or formalize an existing one.
- Create/review Project Charter, Project Plan, RAID, status, RACI, or Change Request.
- Create, review, baseline, or control a cross-role WBS for delivery/sprint/milestone planning when approved source scope is sufficiently stable.
- Coordinate milestones, dependencies, decisions, and escalations across roles.
- Assess readiness for BRD, FSD, TSD, QA/UAT, release, or closure gates.
- Challenge unsupported RAG, hidden variance, ownerless actions, or fake approvals.
- Prepare an evidence-backed steering update.

Do not use WBS governance for detailed TDD implementation planning, solution design, test design, or specialist execution. Do not load `eksad-task-breakdown` or another role's skill in the PM profile: this PM skill governs the WBS and requests specialist inputs/validation through handoffs without reproducing the full technical task-breakdown workflow. Do not use this skill to write specialist artifacts; route that work to the appropriate specialist profile.

## Required Knowledge

Resolve `<EKSAD_PACK_ROOT>` in this order: `EKSAD_PACK_SRC`, the active deployment's shared EKSAD knowledge clone, then `~/.hermes/knowledge/eksad`. Never assume a named profile keeps a private copy of the Git knowledge pack.

Read before substantive work:

1. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md`
2. The exact template for the requested artifact under `EKSAD/gpt/_template/`
3. `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/EKSAD_GENERIC_WBS_TEMPLATE.md` for every WBS assignment
4. `references/delivery-gates.md` when evaluating a gate
5. Existing Charter/Plan/WBS/RAID/current status and relevant specialist artifacts

Completion criterion: all inputs used are named by path/version/date; missing inputs are explicit gaps.

## Operating Contract

### Evidence hierarchy

Prefer, in order:

1. Explicit authorized decision with date/actor.
2. Verified artifact/check result.
3. Named owner commitment with date.
4. Current documented forecast.
5. Assumption with validator and due date.
6. Unknown (`TBD`) rather than invention.

### Stable states

Use entity-specific vocabularies:

- Document: `draft`, `in_review`, `approved`, `superseded`.
- Work item/milestone: `planned`, `in_progress`, `blocked`, `completed`, `cancelled`, `deferred`.
- RAID: `open`, `monitoring`, `mitigating`, `closed`, `invalidated`, `transferred`, `superseded`.
- Gate: `locked`, `in_progress`, `awaiting_review`, `approved`, `revision_required`, `aborted`, `skipped`, `waived`.
- Change Request: `draft`, `assessing`, `awaiting_decision`, `approved`, `rejected`, `withdrawn`, `implemented`.

Never translate `completed` into `approved`, or `waived` into `approved`.

### Gap format

Every missing fact is:

```text
TBD — Owner: <role/person> — Due: <date or explicit TBD>
```

Classify each gap as blocking or non-blocking.

## Workflow

### Step 1 — Establish the mission

Capture:

- project name/code and workspace;
- requested PM artifact or decision;
- current lifecycle stage;
- available artifact paths/versions;
- decision authorities;
- reporting/gate deadline;
- whether a baseline already exists.

Do not ask for information that can be read from provided artifacts. Do not assume missing commitments.

Completion criterion: requested output, source evidence, and authority boundary are explicit.

### Step 2 — Route ownership

Build a compact ownership table for affected work:

| Work | Responsible role | Accountable role | PM action |
|---|---|---|---|
| Business scope/acceptance | Business Owner | Business Owner | Record decision and deadline |
| UR/BRD/FSD | BA | BA Lead | Coordinate review and track gaps |
| Architecture/TSD | System Analyst | Design Authority | Coordinate review and decisions |
| Implementation | Developers | Engineering Lead | Track commitments and build evidence |
| Technical quality | Technical Leader | Technical Leader | Track review and finding closure |
| Test execution | QA | QA Lead | Track evidence and defects |
| UAT | Business Owner | Business Owner | Track acceptance and residual risks |
| Governance | PM | PM | Author and maintain PM artifact |

If ownership is ambiguous, mark it blocked and request a governance decision.

Completion criterion: one accountable role exists for every deliverable/decision.

### Step 3 — Select the exact artifact

| Need | Template |
|---|---|
| Initiation and authorization | `EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md` |
| Milestones/workstreams/dependencies | `EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md` |
| Traceable cross-role work packages, tasks, estimates, and dependency baseline | `EKSAD_GENERIC_WBS_TEMPLATE.md`; filename exactly `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md` |
| Risks/assumptions/issues/dependencies | `EKSAD_GENERIC_RAID_LOG_TEMPLATE.md` |
| Periodic health/steering report | `EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md` |
| Approved-baseline change | `EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md` |
| Formal closure and lessons learned | `EKSAD_GENERIC_PROJECT_CLOSURE_TEMPLATE.md`; filename `{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md` |

Never merge all artifacts into one document. Reference shared information rather than duplicating it.

Completion criterion: one output path and template are declared.

### Step 4 — Draft from evidence

- Preserve source IDs and versions.
- Add stable PM IDs.
- Separate fact, forecast, assumption, and decision.
- For dates, estimates, cost, capacity, and status, cite source or use TBD.
- Keep baseline and forecast separate.
- Ensure every action has owner, due, state, and acceptance/closure evidence.

Completion criterion: no invented value and no ownerless material item.

### Step 5 — Apply artifact-specific controls

#### Charter

Verify measurable objectives, scope boundaries, governance, RACI, assumptions, constraints, initial RAID, milestones, gates, approvers, and authorization statement.

#### Plan

Verify Charter basis, workstreams, owner-confirmed dates, dependency graph, milestone exit evidence, gate schedule, communication cadence, quality/acceptance ownership, and change control.

#### WBS baseline governance

Use a WBS when approved source scope must be decomposed into traceable cross-role work packages for estimation, sequencing, sprint/milestone planning, or assignment readiness. Keep the Project Plan as the milestone/workstream view, RAID as the material risk/dependency view, and Change Request as the mechanism for changing an approved baseline; reference rather than duplicate those artifacts.

Start only from named, versioned source artifacts and decisions. A provisional draft may expose gaps, but the WBS must not be approved or used for sprint commitment while a mandatory source is unapproved, unavailable, or materially ambiguous. Build outcome-verifiable vertical slices where feasible. Every task must have a stable task ID, parent WBS ID, source requirement/design/decision IDs, role owner, concrete output, acceptance criteria/evidence, predecessor IDs, and downstream consumer. Report orphan source IDs, ownerless tasks, and unverifiable outputs as blocking gaps.

PM orchestrates and maintains the artifact and is accountable for its approved baseline and change control. BA, SA, TL, Backend, Frontend, QA, DevOps, and other applicable specialists own their lane's task content, technical estimates, assumptions, and acceptance evidence. Obtain attributable specialist validation for each affected slice before baseline approval. PM may normalize supplied inputs but must not invent or approve specialist content, convert estimation scales, infer velocity, assign capacity, or create dates/sprint assignments without approved owner evidence; leave unsupported values as explicit TBD gaps.

For every dependency, record type, provider, consumer, required outcome, required-by task/date, acceptance evidence, fallback, and state; obtain provider/consumer confirmation of that dependency contract before baseline. Provider completion alone does not close it: the consumer must confirm that the delivered outcome is usable. Check the complete predecessor graph for self-dependencies and direct or transitive cycles before baseline or sprint assignment. Any unresolved cycle, unconfirmed dependency contract, mandatory external dependency without an authorized disposition, or missing specialist validation keeps the WBS `draft`/`in_review` and the affected commitment locked.

Approve a baseline only when the named PM baseline owner (or the governance authority required by the Charter) records actor, date, decision, artifact version, specialist validations, validation result, and evidence. Preserve the approved version; do not overwrite it. Any proposed change to approved scope, tasks, acceptance, estimate, dependency, or commitment is assessed through change control, linked to the affected IDs, and—only after explicit approval—issued as a new WBS version with revision history while the prior version becomes `superseded`. WBS or baseline approval never implies Git commit or push authorization.

WBS closure requires the delivered-output reference and acceptance evidence, specialist/consumer confirmation where applicable, dependency closure evidence, and source-coverage reconciliation. Cancelled/deferred work and residual gaps/RAID require an authority decision, owner, disposition, and follow-up date. Missing acceptance, unresolved dependency, uncovered source ID, ownerless residual work, or absent closure evidence prevents closure and must flow into status/project-closure records.

#### RAID

Use immutable IDs. Risk exposure = Probability × Impact. High/Critical has trigger, mitigation, contingency, owner, date, cadence. Assumptions have validation. Issues have observed evidence/containment. Dependencies have provider, consumer, required-by date, acceptance criteria, fallback, and consumer confirmation.

#### Status

Assess Scope, Schedule, Quality, Risk, and Overall. Use Grey for insufficient evidence. Overall is the worst material dimension unless exception is explicit. Show baseline vs forecast, decisions needed, top RAID, gate state, and evidence cut-off.

#### Change Request

Map affected objective/scope/requirement/artifact/milestone IDs. Collect specialist impacts. Include no-change option. PM recommends; authority decides. Update baselines only after approval.

#### Outcome and benefit metrics

For Charter, Plan, status, and closure, trace each intended outcome/benefit to its objective and record: metric definition, baseline, target, measurement source/method, accountable benefit owner, measurement date/frequency, actual/forecast value, and evidence cut-off. Values and thresholds must come from an approved business case, Charter, policy, or named owner; otherwise use the standard TBD gap format. Distinguish delivered outputs from realized outcomes, and do not claim causation or benefit realization from delivery completion alone.

#### Closure and lessons learned

Use the Project Closure template to reconcile scope/deliverables, acceptance and gate decisions, outcome/benefit measurement status, financial/schedule summary where approved evidence exists, residual RAID and operational ownership, records/knowledge transfer, and follow-up actions. Capture lessons as evidence-linked observation, impact, recommendation, owner, and destination; do not assign blame or rewrite historical baselines. PM recommends closure, but the named authority approves it. Unaccepted deliverables, ownerless residual risk, missing mandatory handoff, or absent authority evidence keeps closure `blocked` or `awaiting_review`.

Completion criterion: artifact-specific mandatory fields pass.

### Step 6 — Evaluate gates

Read `references/delivery-gates.md`, verify required evidence, and record observable semantic events in the PM gate tracker.

Allowed decisions:

- `APPROVE`: explicit authorized acceptance.
- `REVISE`: same owner corrects listed gaps.
- `ABORT`: stop dependent work and preserve evidence.
- `SKIP/WAIVE`: authorized bypass with reason and accepted risk.

PM may issue a readiness recommendation, but only named authority makes the decision.

PM-governed pipelines are always strict HITL. Auto-approval and no-gates execution are prohibited. A `SKIP/WAIVE` request must include named authority, actor, evidence, reason, accepted risk, and follow-up owner/date. If any field is missing, remain `awaiting_review`; do not unlock work or mark it `approved`.

Completion criterion: actor, date, decision, evidence, gaps, residual risk, and dependency lock state are recorded.

### Step 7 — Validate before delivery

Check:

- exact template and mandatory sections;
- exact WBS filename `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md` when applicable;
- stable IDs and traceability;
- no accidental placeholder;
- all material owner/date fields filled or explicit TBD;
- RAG supported by current evidence;
- baseline not silently rewritten;
- approvals attributable;
- specialist boundaries preserved;
- open gaps and decisions summarized.

Completion criterion: validation result is reported with deviations; failed artifact remains draft/revision_required.

### Step 8 — Report and stop at the gate

Return:

1. artifact path and version;
2. evidence sources;
3. RAG/gate status;
4. blocking and non-blocking gaps;
5. top RAID and overdue actions;
6. decisions required with authority/due date;
7. exact next gate command or specialist handoff.

Do not continue into dependent work without approval or authorized waiver.

Completion criterion: user can make the next decision from the report alone.

## Status Challenge Procedure

When asked to review a status report:

1. Verify data cut-off and baseline version.
2. Test every RAG statement against evidence.
3. Compare baseline and forecast dates.
4. Identify unsupported completion/approval language.
5. Find ownerless/overdue actions and dependencies.
6. Confirm top High/Critical RAID appears in the executive view.
7. Recalculate Overall RAG using worst material dimension.
8. Produce corrected status plus an evidence-gap list.

Never make the report more positive without facts.

## Escalation Format

```text
Decision needed:
Impact of delay:
Evidence:
Options:
Recommendation:
Decision owner:
Due date:
```

Escalation is a decision aid, not blame assignment.

## Common Pitfalls

1. PM writes BRD/TSD to unblock schedule. Route it to the specialist; track the blocker.
2. Artifact exists, so status is Complete. Verify quality checks and owner evidence.
3. Reviewer silence treated as approval. Keep `awaiting_review`.
4. Forecast overwrites baseline. Preserve both and calculate variance.
5. Risk written as an issue or assumption. Use cause-event-impact and current reality.
6. Dependency closed by provider only. Require consumer confirmation.
7. PM approves its own change recommendation. Record the authority decision separately.
8. All-Green reporting without evidence. Use Grey/Amber/Red deterministically.
9. Stage tracker logs invented percentages or hidden reasoning. Record observable events only.
10. Closed RAID deleted. Preserve history and closure evidence.

## Verification Checklist

- [ ] Correct PM artifact and template selected
- [ ] WBS uses `EKSAD_GENERIC_WBS_TEMPLATE.md` and exact `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md` filename when applicable
- [ ] WBS source/parent/output/acceptance traceability and source coverage validated
- [ ] Specialists supplied estimates and validated their affected slices; unsupported estimates/dates/capacity/sprints remain TBD
- [ ] Dependencies have provider/consumer acceptance and the graph has no unresolved cycle
- [ ] WBS approval/version/change/closure evidence is attributable; approval did not infer commit/push authority
- [ ] Evidence sources and versions recorded
- [ ] Role ownership matrix respected
- [ ] No invented names/dates/cost/capacity/progress/approval
- [ ] Stable IDs and traceability present
- [ ] Owner/date/evidence on every material action
- [ ] RAG follows standard; Grey used for missing evidence
- [ ] Baseline and forecast remain distinct
- [ ] Outcome/benefit values trace to approved evidence or explicit TBD
- [ ] Closure recommendation is separate from named-authority decision
- [ ] Residual RAID and lessons-learned actions have owners/evidence
- [ ] Gate authority and decision are explicit
- [ ] SKIP/WAIVE distinguished from APPROVE
- [ ] Dependent work remains locked when required
- [ ] Blocking/non-blocking gaps listed
- [ ] Artifact path, version, deviations, and next decision reported

## Phase F Enrichment — Product Capability and Planning Patterns

Adapted benchmark patterns: planning-with-files, product-capability, prioritization.

- Convert requests into owner-specific work packages with dependencies, assumptions, acceptance evidence, and approval gates.
- PM may coordinate WBS/RAID/status but specialists validate technical estimates, design decisions, test verdicts, and release evidence.
- Track change impact across BA/SA/TL/Dev/QA/DevOps/Data/UI/Content roles.
- Escalate when scope, timeline, risk acceptance, or publication/deployment authority is unclear.
