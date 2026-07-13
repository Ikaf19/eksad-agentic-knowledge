# EKSAD Generic Change Request Template

> Filename: `{PROJECT_CODE}_CR_{NNN}.md`
> Owner: Project Manager
> A proposed change does not alter the approved baseline until an authorized decision is recorded.

# {PROJECT_NAME} — Change Request {CR_ID}

## Document Control

| Field | Value |
|---|---|
| Change ID | CR-{PROJECT_CODE}-{NNN} |
| Version | {VERSION} |
| Status | Draft / Assessing / Awaiting Decision / Approved / Rejected / Withdrawn / Implemented |
| Requester | {NAME_ROLE} |
| Project Manager | {NAME} |
| Submitted | {DATE} |
| Decision required by | {DATE} |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial request |

## 1. Requested Change

| Field | Description |
|---|---|
| Current approved baseline | {REFERENCE_AND_VERSION} |
| Requested change | {CLEAR_DESCRIPTION} |
| Reason / business value | {RATIONALE} |
| Urgency | Normal / Expedited / Emergency |
| Trigger / source | {SOURCE} |

## 2. Affected Scope and Traceability

| Affected type | ID / Artifact | Current state | Required update |
|---|---|---|---|
| Objective / Scope | {ID} | {STATE} | {UPDATE} |
| Requirement | {UR_BR_F_FR_ID} | {STATE} | {UPDATE} |
| Technical artifact | {TSD_ADR_ID} | {STATE} | {UPDATE} |
| Milestone / Release | {MS_ID} | {STATE} | {UPDATE} |

## 3. Impact Assessment

| Dimension | Impact | Specialist owner | Evidence / Assumption |
|---|---|---|---|
| Scope | None / Low / Medium / High | BA / Business Owner | {DETAIL} |
| Schedule | {DAYS_OR_TBD} | PM / Workstream owner | {DETAIL} |
| Cost / Resources | {IMPACT_OR_TBD} | Sponsor / Resource owner | {DETAIL} |
| Quality / Testing | {IMPACT} | QA | {DETAIL} |
| Architecture / Technical | {IMPACT} | System Analyst / TL | {DETAIL} |
| Security / Compliance | {IMPACT} | Relevant authority | {DETAIL} |
| Operations / Release | {IMPACT} | Operations owner | {DETAIL} |
| RAID | {NEW_OR_CHANGED_IDS} | PM | {DETAIL} |

## 4. Options

| Option | Description | Benefits | Drawbacks | Schedule impact | Risk |
|---|---|---|---|---|---|
| A | Do not change | {BENEFIT} | {DRAWBACK} | None | {RISK} |
| B | Implement requested change | {BENEFIT} | {DRAWBACK} | {IMPACT} | {RISK} |
| C | Defer / phase change | {BENEFIT} | {DRAWBACK} | {IMPACT} | {RISK} |

## 5. Recommendation

{PM recommendation based on specialist assessments. PM may recommend but cannot impersonate approval authority.}

## 6. Decision

| Decision authority | Name | Decision | Date | Conditions / Rationale | Evidence |
|---|---|---|---|---|---|
| {ROLE} | {NAME} | Pending / Approve / Reject / Defer | {DATE} | {DETAIL} | {REFERENCE} |

## 7. Approved Baseline Updates

Complete only after approval.

| Artifact / Baseline | Old version | New version | Owner | Due | Completed evidence |
|---|---|---|---|---|---|
| {ARTIFACT} | {VERSION} | {VERSION} | {OWNER} | {DATE} | {REFERENCE} |

## 8. Verification and Closure

| Verification | Owner | Expected evidence | Status | Date |
|---|---|---|---|---|
| Change implemented as approved | {OWNER} | {EVIDENCE} | Pending | |
| Regression / acceptance complete | QA / Business Owner | {EVIDENCE} | Pending | |
| Project plan and RAID updated | PM | Updated versions | Pending | |

Closure statement: {CONFIRM APPROVED CHANGE AND BASELINE UPDATES, OR LIST RESIDUAL ITEMS.}