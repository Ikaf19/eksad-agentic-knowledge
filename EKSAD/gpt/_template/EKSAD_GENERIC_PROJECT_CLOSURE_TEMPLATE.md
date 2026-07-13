# EKSAD Generic Project Closure Template

> Filename: `{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md`
> Owner: Project Manager
> Closure is evidence reconciliation and an authority decision. It does not replace business acceptance, QA, technical, security-risk, operational, or release authority.

# {PROJECT_NAME} — Project Closure

## Document Control

| Field | Value |
|---|---|
| Project code | {PROJECT_CODE} |
| Version / status | {VERSION} / Draft / In Review / Approved / Superseded |
| Project Manager | {NAME_OR_TBD} |
| Closure authority | {AUTHORITY_OR_TBD} |
| Evidence cut-off | {DATE_OR_TBD} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Review/approval reference |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial draft | Pending |

## 1. Closure Basis

| Input | Version/state | Owner/authority | Evidence |
|---|---|---|---|
| Charter / approved baseline | {VALUE} | PM / Sponsor | {REFERENCE} |
| Project Plan / approved changes | {VALUE} | PM / Change Authority | {REFERENCE} |
| Business acceptance | {VALUE} | Business Owner | {REFERENCE} |
| Technical / QA / release decisions | {VALUE} | Named specialist authorities | {REFERENCE} |
| Operational handoff | {VALUE} | Operations/Service Owner | {REFERENCE} |

Missing mandatory evidence keeps closure `blocked` or `awaiting_review`; silence is not acceptance.

## 2. Objective, Outcome, and Benefit Reconciliation

| Objective / benefit ID | Metric definition | Baseline | Approved target | Actual/forecast | Source/method | Benefit owner | Measurement date/window | Evidence / disposition |
|---|---|---|---|---|---|---|---|---|
| {ID} | {DEFINITION} | {VALUE_OR_TBD} | {VALUE_OR_TBD} | {VALUE_OR_NOT_YET_MEASURED} | {REFERENCE} | {OWNER} | {DATE/WINDOW} | {REFERENCE/FOLLOW_UP} |

Distinguish outputs delivered from outcomes/benefits realized. Do not infer causation or claim realization without measurement evidence.

## 3. Scope and Deliverable Reconciliation

| Deliverable / scope ID | Baseline | Final state | Acceptance authority | Acceptance evidence | Variance / approved change | Residual action |
|---|---|---|---|---|---|---|
| {ID} | {REFERENCE} | Accepted / Not Accepted / Cancelled / Deferred | {AUTHORITY} | {REFERENCE} | {CR_REFERENCE_OR_NONE} | {ACTION_OR_NONE} |

## 4. Schedule and Financial Reconciliation

| Measure | Approved baseline | Final actual/forecast | Variance | Evidence | Owner/comment |
|---|---|---|---|---|---|
| Start / finish / milestones | {VALUE_OR_TBD} | {VALUE_OR_TBD} | {VALUE_OR_TBD} | {REFERENCE} | {DETAIL} |
| Budget / cost / benefit | {VALUE_OR_NA} | {VALUE_OR_NA} | {VALUE_OR_NA} | {APPROVED_REFERENCE} | {DETAIL} |

Use only approved financial and schedule evidence. Preserve historical baselines; do not reconstruct or overwrite them.

## 5. Gate and Acceptance Decisions

| Gate/decision | State | Named authority / actor | Date | Evidence | Waiver/residual risk |
|---|---|---|---|---|---|
| {GATE} | Approved / Rejected / Skipped / Waived / Awaiting Review | {AUTHORITY/ACTOR} | {DATE} | {REFERENCE} | {DETAIL} |

`Skipped`/`waived` remains distinct from `approved`.

## 6. Residual RAID and Ownership Transfer

| RAID/action ID | Residual item | State | Impact | Receiving owner | Due/review date | Acceptance evidence | Escalation |
|---|---|---|---|---|---|---|---|
| {ID} | {DETAIL} | Open / Monitoring / Transferred / Closed | {IMPACT} | {OWNER_OR_TBD} | {DATE_OR_TBD} | {REFERENCE} | {PATH} |

Ownerless material residual risk blocks closure recommendation.

## 7. Operational and Knowledge Handoff

| Handoff item | Exact artifact/location | Version/state | From / to | Acceptance checks | Receiver evidence | Open gap |
|---|---|---|---|---|---|---|
| Runbook, support, records, access, training, evidence archive, or ownership | {REFERENCE} | {VALUE} | {ROLES} | {CHECKS} | {REFERENCE} | {NONE_OR_TBD} |

Do not include raw secrets; reference approved credential/access processes.

## 8. Lessons Learned

| Lesson ID | Evidence-linked observation | Impact | Recommendation | Owner | Destination / follow-up | Due | State |
|---|---|---|---|---|---|---|---|
| LL-{PROJECT}-001 | {OBSERVATION_AND_REFERENCE} | {IMPACT} | {ACTIONABLE_RECOMMENDATION} | {OWNER} | {STANDARD/BACKLOG/RAID/OTHER} | {DATE_OR_TBD} | Proposed / Accepted / Rejected / Implemented |

Record process/system learning without blame. A lesson is not implemented until its destination contains evidence of the accepted change.

## 9. Open Actions

| Action ID | Action | Owner | Due | Blocking closure? | Acceptance evidence / state |
|---|---|---|---|---|---|
| ACT-{PROJECT}-001 | {ACTION} | {OWNER_OR_TBD} | {DATE_OR_TBD} | Yes / No | {REFERENCE/STATE} |

## 10. PM Closure Recommendation

**Recommendation:** READY_FOR_CLOSURE / NOT_READY / BLOCKED

**Evidence-based rationale:** {RATIONALE}

**Unresolved exceptions:** {LIST_OR_NONE}

PM recommends; the named authority decides.

## 11. Closure Decision

| Decision | Named authority | Acting person | Date/time | Evidence | Conditions / retained actions |
|---|---|---|---|---|---|
| Approve Closure / Reject / Revise | {AUTHORITY} | {PERSON} | {TIMESTAMP} | {REFERENCE} | {DETAIL} |

## 12. Validation

- [ ] Closure basis references current, attributable evidence
- [ ] Outputs, outcomes, and realized benefits are distinguished
- [ ] Baseline and final actual/forecast remain distinct
- [ ] Deliverables and gate decisions retain exact states
- [ ] Residual RAID/actions have accepted owners and dates
- [ ] Mandatory operational/knowledge handoffs are accepted
- [ ] Lessons are evidence-linked, actionable, and non-blaming
- [ ] No metric, threshold, date, cost, approval, or authority is invented
- [ ] Closure recommendation and authority decision are separate

> **Template use:** Copy this file to the approved project-governance path, rename it `{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md`, replace placeholders, and keep this generic template free of project-specific completed content.
