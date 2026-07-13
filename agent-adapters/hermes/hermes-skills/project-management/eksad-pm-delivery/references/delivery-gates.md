# EKSAD Delivery Gate Reference

Use this reference with `eksad-pm-delivery`. It defines minimum evidence for readiness recommendations. Named authorities—not the PM assistant—make approvals.

## Universal Gate Contract

Every gate record includes:

| Field | Requirement |
|---|---|
| Gate ID/name | Stable and unambiguous |
| Artifact | Path/name, version, owner |
| Required checks | Named checks and results |
| Reviewers | Required reviewers and response state |
| Decision authority | Named role/person |
| Gaps | Blocking and non-blocking |
| RAID | New/changed/residual IDs |
| Decision | APPROVE / REVISE / ABORT / SKIP-WAIVE |
| Evidence | Decision source/date/actor |
| Dependencies | What unlocks or remains locked |

Universal rules:

- `completed` is not `approved`.
- `SKIP/WAIVE` is not approval.
- Silence or elapsed time is not approval.
- Failed mandatory checks cannot receive an APPROVE recommendation.
- A bypass requires authority, reason, accepted risk, and follow-up owner/date.
- Auto-approval and no-gates execution are prohibited for PM-governed work.

## Strict PM Gate Tracker

Maintain one row/event per gate decision with all fields below. Missing mandatory decision metadata keeps the gate `awaiting_review` and dependent work locked.

| Field | Requirement |
|---|---|
| Gate ID | Stable identifier |
| Previous state | Canonical gate state |
| Requested decision | APPROVE / REVISE / ABORT / SKIP-WAIVE |
| Named authority | Authorized role/person |
| Acting person | Person making the decision |
| Authority evidence | Charter/RACI/decision reference |
| Artifact evidence | Version/path/check results |
| Reason | Decision rationale |
| Accepted risk | Required for SKIP/WAIVE; otherwise None |
| Follow-up owner/date | Required for SKIP/WAIVE and residual gaps |
| Decision timestamp | Explicit date/time |
| New state | Canonical gate state |
| Dependency lock | Locked/unlocked plus affected work |

Only APPROVE by verified authority may set `approved`. A complete artifact without approval stays `awaiting_review`. SKIP/WAIVE sets `skipped` or `waived`, never `approved`.

## Gate 0 — Project Charter

### Definition of Ready

- Project name/code and problem/opportunity are identified.
- Sponsor, Business Owner, PM, and key specialist roles are named or explicit gaps.
- Objectives and measurable outcomes are drafted.
- Scope boundaries, assumptions, constraints, and initial risks are visible.

### Definition of Done

- Charter uses current EKSAD template.
- Objectives have metrics/targets or explicit validation gaps.
- In/out scope and key deliverables are unambiguous.
- High-level RACI has exactly one accountable authority per decision.
- Initial milestones, dependencies, RAID, governance, and gates exist.
- Sponsor/authority approval is explicit.

Decision authority: Sponsor, with Business Owner per governance.

## Gate 1 — User Requirements

### Definition of Ready

- Approved Charter or authorized initiation basis exists.
- Stakeholder sources and business objective references exist.
- BA owns the artifact.

### Definition of Done

- UR IDs are stable and trace to sources/objectives.
- Priorities and actors are stated.
- Ambiguities and assumptions are visible.
- Business Owner explicitly confirms the UR baseline.

Decision authority: Business Owner. PM coordinates only.

## Gate 2 — BRD

### Definition of Ready

- UR baseline is approved or authorized waiver recorded.
- BA has current BRD template and business inputs.

### Definition of Done

- BRD traceability from UR to BR exists.
- Scope, stakeholders, rules, risks, and outcomes are complete.
- Forbidden technical detail check passes.
- Review gaps are resolved or accepted explicitly.
- Business Owner approval is recorded.

Decision authority: Business Owner.

## Gate 3 — FSD

### Definition of Ready

- BRD is approved or authorized waiver recorded.
- Feature list and source BR IDs are available.

### Definition of Done

- Every feature traces to BR/UR.
- Main, alternative, exception flows and validation rules exist.
- Acceptance criteria are testable.
- NFR and async behavior signals are captured in business language.
- QA/System Analyst reviews are complete as required.
- Business Owner approval is recorded.

Decision authority: Business Owner.

## Gate 4 — Architecture / TSD

### Definition of Ready

- FSD is approved or waiver recorded.
- Architecture constraints, domain/service context, and integration inputs exist.
- System Analyst/Solution Architect owns the artifact.

### Definition of Done

- Architecture/service boundaries and stack profile are explicit.
- API, data, event, security, tenancy, resilience, observability, deployment, and testing design are covered as applicable.
- Requirements trace to technical decisions.
- Architecture risks and exceptions are visible.
- Required design/TL review is complete and approval recorded.

Decision authority: designated design authority, not PM.

## Gate 5 — Implementation Readiness / Completion

### Definition of Ready

- Approved TSD or authorized design waiver exists.
- Tasks have owner, dependencies, acceptance criteria, and estimates from technical owners.
- Development/test environments and required access are ready or explicit blockers.

### Definition of Done

- Build/CI evidence passes.
- Code review and technical findings are closed or accepted.
- Required unit/integration tests pass.
- Implementation traces to planned scope/tasks.
- Known defects and technical debt are recorded.

Decision authority: Technical Leader for technical readiness.

## Gate 6 — QA / UAT

### Definition of Ready

- Testable build and environment are available.
- Approved FSD/acceptance criteria and test plan exist.
- Test data, roles, integrations, and dependencies are ready.

### Definition of Done

- Required test suites executed with evidence.
- Defect status and severity are current.
- Regression and non-functional checks are complete as scoped.
- Residual defects/risks have acceptance authority and decision.
- UAT/business acceptance is explicit where required.

Decision authority: QA for test evidence; Business Owner for business acceptance/residual business risk.

## Gate 7 — Release

### Definition of Ready

- QA/UAT gate approved or authorized waiver recorded.
- Release scope/version, deployment plan, rollback, monitoring, support, and communications exist.
- Open RAID and residual risk are visible.

### Definition of Done

- Release authorization is explicit.
- Deployment/rollback evidence is captured.
- Smoke/health verification passes.
- Incident/escalation ownership is active.
- Stakeholders receive release outcome.

Decision authority: Sponsor/Business Owner/technical authority according to governance.

## Gate 8 — Closure

### Definition of Ready

- Planned release/outcome is delivered or project is formally stopped.
- Deliverable and RAID status are current.

### Definition of Done

- Deliverables accepted, waived, deferred, or cancelled explicitly.
- Residual RAID transferred to named operational owners.
- Follow-up backlog and unresolved scope are recorded.
- Final outcome/success metrics are reported with evidence.
- Lessons learned and closure approval are recorded.

Decision authority: Sponsor, with Business Owner acceptance.

## Readiness Output Format

```text
Gate:
Recommendation: APPROVE | REVISE | ABORT | SKIP/WAIVE
Decision authority:
Evidence reviewed:
Checks passed:
Blocking gaps:
Non-blocking gaps:
Residual RAID:
Dependencies unlocked/locked:
Decision needed by:
```

A readiness recommendation is not itself an approval.
