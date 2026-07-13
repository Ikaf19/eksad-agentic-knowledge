# EKSAD Generic Incident Handoff Template

> Filename: `{PROJECT_CODE}_INCIDENT_{ID}_HANDOFF.md`
> Owner: Current Incident/Operations Owner
> Distinguish confirmed facts, hypotheses, and ruled-out causes. Never invent root cause.

# {PROJECT_NAME} — Incident {INCIDENT_ID} Handoff

## Document Control

| Field | Value |
|---|---|
| Incident ID | {INCIDENT_ID} |
| Version/status | {VERSION} / Draft / In Review / Approved / Superseded |
| Current owner | {OWNER} |
| Receiving owner | {OWNER} |
| Environment | {ENVIRONMENT} |
| Evidence cut-off | {TIMESTAMP} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Handoff acknowledgement |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial handoff | Pending |

## 1. Incident Summary

| Field | Value/evidence |
|---|---|
| Detection time/source | {TIMESTAMP/ALERT/REPORT} |
| Severity | {POLICY_CLASSIFICATION_OR_TBD} |
| Current state | Detected / Triaged / Contained / Mitigating / Monitoring / Resolved / Closed |
| Affected service/environment | {EXACT_SCOPE} |
| Current impact | {CONFIRMED_IMPACT} |
| Start/latest known good | {TIMESTAMPS} |
| Incident commander | {NAME/ROLE} |
| Communication channel/reference | {REFERENCE} |

## 2. Release and Change Context

| Field | Value/evidence |
|---|---|
| Current deployed version/digest | {VALUE} |
| Previous known-good digest | {VALUE} |
| GitLab commit/MR | {FULL_SHA/MR/REFERENCE} |
| Jenkins build/deployment | {JOB/BUILD/REFERENCE} |
| Recent change/release ID | {VALUE} |
| SonarQube/Trivy evidence | {REFERENCE} |
| Deployment/rollback runbook | {REFERENCE} |

## 3. Confirmed Facts

| Fact ID | Confirmed observation | Timestamp | Source/evidence | Confidence limitation |
|---|---|---|---|---|
| FACT-001 | {OBSERVATION} | {TIME} | {LOG/METRIC/COMMAND} | {LIMITATION_OR_NONE} |

## 4. Hypotheses

| Hypothesis ID | Statement | Supporting evidence | Contradicting evidence | Validation action | Owner/due | State |
|---|---|---|---|---|---|---|
| HYP-001 | {HYPOTHESIS} | {REFERENCE} | {REFERENCE} | {ACTION} | {OWNER/DATE} | Open |

Hypotheses are not root cause and must not be reported as fact.

## 5. Ruled-Out Causes

| ID | Cause | Test/evidence | Result | Scope/limitations |
|---|---|---|---|---|
| RULED-001 | {CAUSE} | {REFERENCE} | Ruled Out | {LIMITATION} |

## 6. Timeline

| Timestamp | Actor/system | Event/action | Observed result | Evidence |
|---|---|---|---|---|
| {TIME} | {ACTOR} | {EVENT} | {RESULT} | {REFERENCE} |

## 7. Operational Evidence

| Evidence | Query/reference | Time range | Result/interpretation |
|---|---|---|---|
| Prometheus metrics/alerts | {REFERENCE} | {RANGE} | {OBSERVATION} |
| Grafana dashboard/snapshot | {REFERENCE} | {RANGE} | {OBSERVATION} |
| Loki logs/query | {REFERENCE} | {RANGE} | {OBSERVATION} |
| Health/smoke checks | {REFERENCE} | {RANGE} | {OBSERVATION} |
| VM/container state | {REFERENCE} | {RANGE} | {OBSERVATION} |

Redact secrets and sensitive payloads. Preserve immutable/query-specific evidence where possible.

## 8. Actions Executed

| Timestamp | Acting person/build | Authorized scope/reference | Command/job/action | Exit/state | Result/evidence | Reversible? |
|---|---|---|---|---|---|---|
| {TIME} | {ACTOR} | {REFERENCE} | {ACTION} | {RESULT} | {REFERENCE} | Yes/No |

Do not list fabricated or proposed actions as executed. Label proposals `NOT RUN`.

## 9. Containment and Mitigation

| Action | State | Owner | Due | Expected effect | Evidence/result | Residual risk |
|---|---|---|---|---|---|---|
| {ACTION} | Planned / In Progress / Completed / Failed / Blocked | {OWNER} | {DATE} | {EFFECT} | {REFERENCE} | {RISK} |

## 10. Rollback and Recovery

| Field | Value/evidence |
|---|---|
| Rollback trigger reached? | Yes / No / Unknown |
| Decision authority/actor | {VALUE} |
| Decision evidence/time | {REFERENCE} |
| Rollback target/digest | {VALUE} |
| Procedure/job | {REFERENCE} |
| State/result | Not Started / Rolling Back / Rolled Back / Failed / Aborted |
| Data/migration implications | {DETAIL} |
| Post-rollback health | {REFERENCE} |

If rollback is not authorized or safe, state the blocker; do not improvise destructive recovery.

## 11. Security and Data Impact

| Question | Answer/evidence | Owner/action |
|---|---|---|
| Suspected credential exposure? | Yes / No / Unknown | {ACTION} |
| Suspected data confidentiality/integrity impact? | Yes / No / Unknown | {ACTION} |
| Audit/evidence preservation required? | Yes / No / Unknown | {ACTION} |
| Security authority notified? | {REFERENCE} | {ACTION} |

## 12. Current Handoff State

| Item | Detail |
|---|---|
| Current service state | {STATE} |
| What is contained | {DETAIL} |
| What remains affected | {DETAIL} |
| Blocking risks | {DETAIL} |
| Next exact action | {ACTION} |
| Action owner/due | {OWNER/DATE} |
| Escalation needed | {DECISION/OWNER/DUE} |
| Required participants | {LIST} |
| Communication status | {REFERENCE} |

## 13. Open Decisions and Actions

| ID | Decision/action | Options | Recommendation | Authority/owner | Due | Impact of delay |
|---|---|---|---|---|---|---|
| INC-ACT-001 | {ITEM} | {OPTIONS} | {RECOMMENDATION} | {OWNER} | {DATE} | {IMPACT} |

## 14. Handoff Acknowledgement

| From | To | Timestamp | Decision | Evidence/notes |
|---|---|---|---|---|
| {CURRENT_OWNER} | {RECEIVING_OWNER} | {TIME} | Accepted / Returned for Clarification / Rejected Out of Scope | {REFERENCE} |

Acceptance means the receiving owner has workable context; it does not approve root cause, risk acceptance, or closure.

## 15. Closure Requirements

Close only when service state and impact are evidenced; root cause is confirmed or explicitly deferred with owner/date; remediation and prevention actions are tracked; security/data obligations are addressed; communication is complete; evidence is retained; and the authorized incident owner records closure.