# EKSAD Generic Project Charter Template

> Filename: `{PROJECT_CODE}_PROJECT_CHARTER.md`
> Owner: Project Manager
> Replace placeholders before approval. Unknowns use `TBD — Owner: {ROLE} — Due: {DATE}`.

# {PROJECT_NAME} — Project Charter

## Document Control

| Field | Value |
|---|---|
| Project code | {PROJECT_CODE} |
| Version | {VERSION} |
| Status | Draft / In Review / Approved / Superseded |
| Project Manager | {NAME_OR_TBD} |
| Sponsor | {NAME_OR_TBD} |
| Business Owner | {NAME_OR_TBD} |
| Created | {YYYY-MM-DD} |
| Last updated | {YYYY-MM-DD} |

## Revision History

| Version | Date | Author | Change | Status |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial draft | Draft |

## Approval

| Role | Name | Decision | Date | Evidence / Note |
|---|---|---|---|---|
| Sponsor | {NAME} | Pending | | |
| Business Owner | {NAME} | Pending | | |
| Project Manager | {NAME} | Pending | | |

## 1. Executive Summary

{Why the project exists, expected outcome, and why now.}

## 2. Problem / Opportunity

| Item | Description | Evidence / Source |
|---|---|---|
| Current condition | {DESCRIPTION} | {SOURCE} |
| Business impact | {DESCRIPTION} | {SOURCE} |
| Opportunity | {DESCRIPTION} | {SOURCE} |

## 3. Objectives and Success Measures

| Objective ID | Objective | Metric | Baseline | Target | Measurement owner |
|---|---|---|---|---|---|
| OBJ-{PROJECT_CODE}-001 | {OBJECTIVE} | {METRIC} | {BASELINE_OR_TBD} | {TARGET_OR_TBD} | {OWNER} |

## 4. Scope

### 4.1 In Scope

| Scope ID | Item | Outcome / Deliverable | Owner |
|---|---|---|---|
| SCP-{PROJECT_CODE}-001 | {ITEM} | {OUTCOME} | {OWNER} |

### 4.2 Out of Scope

| Scope ID | Item | Rationale | Potential future phase |
|---|---|---|---|
| OOS-{PROJECT_CODE}-001 | {ITEM} | {RATIONALE} | {PHASE_OR_NONE} |

## 5. Key Deliverables

| Deliverable ID | Deliverable | Accountable owner | Acceptance authority | Target milestone |
|---|---|---|---|---|
| DLV-{PROJECT_CODE}-001 | {DELIVERABLE} | {OWNER} | {APPROVER} | {MILESTONE} |

## 6. Initial Milestone Baseline

| Milestone ID | Milestone | Target date | Owner | Exit evidence | Confidence |
|---|---|---|---|---|---|
| MS-{PROJECT_CODE}-001 | Charter approved | {DATE_OR_TBD} | PM | Explicit approval record | High / Medium / Low |

## 7. Stakeholders and Governance

| Stakeholder / Role | Interest | Decision authority | Engagement cadence |
|---|---|---|---|
| Sponsor | {INTEREST} | {AUTHORITY} | {CADENCE} |
| Business Owner | {INTEREST} | {AUTHORITY} | {CADENCE} |
| Project Manager | Delivery governance | Project process/reporting | {CADENCE} |
| Business Analyst | Requirements | UR/BRD/FSD quality | {CADENCE} |
| System Analyst | Technical specification | TSD quality | {CADENCE} |
| Technical Leader | Technical quality | Architecture/code review | {CADENCE} |
| QA Engineer | Quality verification | Test evidence | {CADENCE} |

## 8. High-Level RACI

| Deliverable / Decision | Sponsor | Business Owner | PM | BA | System Analyst | TL | Dev | QA |
|---|---|---|---|---|---|---|---|---|
| Charter approval | A | C | R | C | I | I | I | I |
| BRD approval | I | A | C | R | C | I | I | C |
| TSD approval | I | C | C | I | R/A | C | I | C |
| Release readiness | A | C | R | C | C | C | C | C |

## 9. Assumptions and Constraints

| ID | Type | Statement | Validation / Source | Owner | Due date | Status |
|---|---|---|---|---|---|---|
| ASM-{PROJECT_CODE}-001 | Assumption | {STATEMENT} | {METHOD} | {OWNER} | {DATE} | Open |
| CON-{PROJECT_CODE}-001 | Constraint | {STATEMENT} | {SOURCE} | {OWNER} | {DATE} | Confirmed / TBD |

## 10. Initial Risks and Dependencies

| ID | Type | Description | Impact | Owner | Response / Next action | Due date |
|---|---|---|---|---|---|---|
| RSK-{PROJECT_CODE}-001 | Risk | {DESCRIPTION} | {IMPACT} | {OWNER} | {ACTION} | {DATE} |
| DEP-{PROJECT_CODE}-001 | Dependency | {DESCRIPTION} | {IMPACT} | {OWNER} | {ACTION} | {DATE} |

## 11. Delivery Approach and Gates

| Gate | Required artifact/evidence | Responsible owner | Accountable owner | Approval authority |
|---|---|---|---|---|
| Initiation | Approved Project Charter | PM | PM | Sponsor |
| Requirements | Approved UR/BRD/FSD | BA | BA Lead | Business Owner |
| Technical design | Approved Architecture/TSD | System Analyst | Design Authority | Design Authority |
| Implementation | Build and review evidence | Developers | Engineering Lead | Technical Leader |
| QA | Test evidence | QA | QA Lead | QA Lead |
| UAT | Business acceptance evidence | Business Owner | Business Owner | Business Owner |
| Release | Readiness checklist and residual risks | PM | PM | Sponsor / Business Owner |

## 12. Communication and Reporting

| Forum / Report | Purpose | Participants | Cadence | Owner |
|---|---|---|---|---|
| Project status | Health and decisions | {LIST} | Weekly | PM |
| RAID review | Top RAID and actions | {LIST} | Weekly | PM |
| Steering decision | Escalated decisions | {LIST} | As required | Sponsor |

## 13. Authorization Statement

Approval authorizes planning and execution within approved scope and governance. It does not authorize unrecorded scope, schedule, budget, architecture, or acceptance changes.

## 14. Open Gaps Before Approval

| Gap ID | Missing decision/information | Owner | Due date | Blocking? |
|---|---|---|---|---|
| GAP-{PROJECT_CODE}-001 | {DESCRIPTION} | {OWNER} | {DATE} | Yes / No |