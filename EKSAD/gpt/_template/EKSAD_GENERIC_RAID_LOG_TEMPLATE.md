# EKSAD Generic RAID Log Template

> Filename: `{PROJECT_CODE}_RAID_LOG.md`
> Owner: Project Manager
> IDs are immutable. Never delete closed records; retain closure evidence.

# {PROJECT_NAME} — RAID Log

## Document Control

| Field | Value |
|---|---|
| Project code | {PROJECT_CODE} |
| Version | {VERSION} |
| Status | Draft / In Review / Approved / Superseded |
| Owner | {PM_NAME} |
| Review cadence | {CADENCE} |
| Source evidence | {PROJECT_PLAN_AND_ARTIFACT_REFERENCES} |
| Last reviewed | {DATE} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Evidence / Approval |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial RAID baseline | {REFERENCE_OR_PENDING} |

## Scoring

Probability and Impact use `1..5`; Exposure = Probability × Impact.

| Exposure | Severity |
|---|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–15 | High |
| 16–25 | Critical |

## Risks

| ID | Opened | Risk (cause → event → impact) | P | I | Exposure | Trigger | Mitigation | Contingency | Owner | Due | Status | Closure evidence |
|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| RSK-{PROJECT_CODE}-001 | {DATE} | {STATEMENT} | {1-5} | {1-5} | {P_X_I} | {TRIGGER} | {ACTION} | {CONTINGENCY} | {OWNER} | {DATE} | Open | |

## Assumptions

| ID | Opened | Assumption | Impact if false | Validation method | Owner | Due | Status | Result / conversion reference |
|---|---|---|---|---|---|---|---|---|
| ASM-{PROJECT_CODE}-001 | {DATE} | {ASSUMPTION} | {IMPACT} | {METHOD} | {OWNER} | {DATE} | Open | |

## Issues

| ID | Opened | Issue and evidence | Impact | Containment | Resolution | Owner | Due | Escalation | Status | Closure evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| ISS-{PROJECT_CODE}-001 | {DATE} | {ISSUE} | {IMPACT} | {ACTION} | {ACTION} | {OWNER} | {DATE} | {LEVEL} | Open | |

## Dependencies

| ID | Opened | Provider | Consumer | Required outcome | Required by | Acceptance criteria | Fallback | Owner | Status | Consumer confirmation |
|---|---|---|---|---|---|---|---|---|---|---|
| DEP-{PROJECT_CODE}-001 | {DATE} | {PROVIDER} | {CONSUMER} | {OUTCOME} | {DATE} | {CRITERIA} | {FALLBACK} | {OWNER} | Open | |

## Review History

| Review date | Participants | Top changes | Escalations | Next review |
|---|---|---|---|---|
| {DATE} | {LIST} | {SUMMARY} | {IDS_OR_NONE} | {DATE} |

## Record Retention

Do not remove records. Set status to `Closed`, `Invalidated`, `Transferred`, or `Superseded`, then provide dated evidence and successor ID if applicable.