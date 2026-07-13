# EKSAD Generic Project Plan Template

> Filename: `{PROJECT_CODE}_PROJECT_PLAN.md`
> Owner: Project Manager
> Dates and commitments must come from accountable owners or an approved baseline.

# {PROJECT_NAME} — Project Plan

## Document Control

| Field | Value |
|---|---|
| Project code | {PROJECT_CODE} |
| Version | {VERSION} |
| Status | Draft / In Review / Approved / Superseded |
| Project Manager | {NAME} |
| Baseline date | {DATE_OR_TBD} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Approval reference |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial draft | Pending |

## 1. Planning Basis

| Input | Version / Date | Status | Owner |
|---|---|---|---|
| Project Charter | {REFERENCE} | Draft / In Review / Approved / Superseded | PM |
| UR | {REFERENCE} | {STATUS} | BA |
| BRD | {REFERENCE} | {STATUS} | BA |
| FSD | {REFERENCE} | {STATUS} | BA |
| Architecture/TSD | {REFERENCE} | {STATUS} | System Analyst |

## 2. Delivery Strategy

{Describe phases, release strategy, governance cadence, and constraints. Do not invent specialist estimates.}

## 3. Workstreams

| Workstream ID | Workstream | Responsible | Accountable | Objective | Inputs | Outputs |
|---|---|---|---|---|---|---|
| WS-{PROJECT_CODE}-001 | Requirements | BA | BA Lead | Baselined functional scope | Charter | UR, BRD, FSD |
| WS-{PROJECT_CODE}-002 | Technical design | System Analyst | Design Authority | Implementation-ready design | FSD | TSD |
| WS-{PROJECT_CODE}-003 | Implementation | Developers | Engineering Lead | Working software | TSD | Build evidence |
| WS-{PROJECT_CODE}-004 | Technical quality | Technical Leader | Technical Leader | Architecture/code quality | TSD, build | Review evidence |
| WS-{PROJECT_CODE}-005 | Quality | QA | QA Lead | Verified acceptance | FSD, build | Test/UAT evidence |

## 4. Milestone Baseline

| Milestone ID | Milestone | Planned date | Forecast date | Owner | Dependency | Exit evidence | Status |
|---|---|---|---|---|---|---|---|
| MS-{PROJECT_CODE}-001 | Charter approved | {DATE} | {DATE} | PM | None | Approval evidence | Planned |

## 5. Deliverable Schedule

| Deliverable ID | Deliverable | Owner | Start | Target | Reviewer | Acceptance authority | Status |
|---|---|---|---|---|---|---|---|
| DLV-{PROJECT_CODE}-001 | {DELIVERABLE} | {OWNER} | {DATE} | {DATE} | {REVIEWER} | {APPROVER} | Planned |

## 6. Dependency Plan

| Dependency ID | Provider | Consumer | Required outcome | Required by | Acceptance criteria | Fallback | Status |
|---|---|---|---|---|---|---|---|
| DEP-{PROJECT_CODE}-001 | {PROVIDER} | {CONSUMER} | {OUTCOME} | {DATE} | {CRITERIA} | {FALLBACK} | Open |

## 7. Stage-Gate Plan

| Gate | Planned review | Required evidence | Reviewers | Decision authority | State |
|---|---|---|---|---|---|
| Charter | {DATE} | Charter checklist | Sponsor, Business Owner | Sponsor | Locked |
| BRD | {DATE} | Traceability/gap review | PM, SA, QA | Business Owner | Locked |
| FSD | {DATE} | Functional completeness | PM, SA, QA | Business Owner | Locked |
| TSD | {DATE} | Design review | TL, QA | Design authority | Locked |
| Release | {DATE} | QA/UAT, residual risk, rollback | Stakeholders | Sponsor / Business Owner | Locked |

## 8. Resource and Responsibility Plan

| Role | Named person / TBD | Responsibility | Availability assumption | Confirmation evidence |
|---|---|---|---|---|
| Project Manager | {NAME_OR_TBD} | Delivery governance | {ASSUMPTION} | {SOURCE} |

## 9. Communication Plan

| Communication | Audience | Purpose | Cadence | Channel | Owner |
|---|---|---|---|---|---|
| Weekly status | {AUDIENCE} | Health, variance, decisions | Weekly | {CHANNEL} | PM |
| RAID review | Workstream leads | Review RAID and actions | Weekly | {CHANNEL} | PM |

## 10. Quality and Acceptance Plan

| Deliverable | Quality owner | Required review | Acceptance evidence |
|---|---|---|---|
| BRD/FSD | BA | Traceability/completeness | Business Owner decision |
| TSD | System Analyst | Architecture/design review | Design approval |
| Software | TL / Dev | Build, tests, code review | CI/PR evidence |
| Release | QA / Business Owner | QA/UAT | Test report and acceptance |

## 11. RAID Summary

Reference `{PROJECT_CODE}_RAID_LOG.md`; do not duplicate it.

| Category | Open | High/Critical | Top item | Owner |
|---|---:|---:|---|---|
| Risks | {N} | {N} | {ID} | {OWNER} |
| Issues | {N} | {N} | {ID} | {OWNER} |
| Dependencies | {N} | {N} | {ID} | {OWNER} |

## 12. Change Control

Changes to approved scope, milestone baseline, acceptance criteria, or release commitment require `{PROJECT_CODE}_CR_{NNN}.md`. Approved changes update this plan version and history.

## 13. Open Planning Gaps

| Gap ID | Missing input/decision | Owner | Due | Impact if late |
|---|---|---|---|---|
| GAP-{PROJECT_CODE}-001 | {DESCRIPTION} | {OWNER} | {DATE} | {IMPACT} |