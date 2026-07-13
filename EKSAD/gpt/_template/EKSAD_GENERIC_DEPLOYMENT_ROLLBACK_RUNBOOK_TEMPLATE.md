# EKSAD Generic Deployment and Rollback Runbook Template

> Filename: `{PROJECT_CODE}_{ENV}_DEPLOYMENT_ROLLBACK_RUNBOOK.md`
> Owner: DevOps Engineer
> Commands are drafts until validated. Production execution requires explicit current authorization.

# {PROJECT_NAME} — {ENVIRONMENT} Deployment and Rollback Runbook

## Document Control

| Field | Value |
|---|---|
| Version/status | {VERSION} / Draft / In Review / Approved / Superseded |
| Service/environment | {SERVICE} / {ENVIRONMENT} |
| Owner/accountable | {DEVOPS_OWNER} / {DEVOPS_LEAD} |
| Source design | {TSD/ARCHITECTURE_REFERENCE} |
| Pipeline | {JENKINS_JOB_REFERENCE} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Approval evidence |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial runbook | {PENDING_OR_REFERENCE} |

## 1. Scope and Safety Classification

| Field | Value |
|---|---|
| Change/release ID | {ID} |
| Production? | Yes / No |
| Exact target | {VM/SERVICE/COMPOSE_PROJECT} |
| Source commit | {FULL_SHA} |
| Artifact | {NAME_VERSION_DIGEST} |
| Allowed actions | {EXACT_SCOPE} |
| Explicit exclusions | {OUT_OF_SCOPE} |
| Authorized window | {START_END_TZ} |

## 2. Authorities and Participants

| Responsibility | Named person/role | Authority evidence | Availability |
|---|---|---|---|
| Release authority | {NAME} | {REFERENCE} | {WINDOW} |
| Acting DevOps engineer | {NAME} | {IDENTITY} | {WINDOW} |
| Rollback authority | {NAME} | {REFERENCE} | {WINDOW} |
| QA contact | {NAME} | Test evidence owner | {WINDOW} |
| Business contact | {NAME} | Acceptance authority | {WINDOW} |
| Incident escalation | {NAME/TEAM} | {POLICY} | {CONTACT_REF} |

## 3. Evidence Inputs

| Input | Exact identity | State | Evidence |
|---|---|---|---|
| GitLab commit/MR | {SHA/MR} | Eligible / Blocked | {REFERENCE} |
| Jenkins build | {JOB/BUILD} | Passed / Waived / Blocked | {REFERENCE} |
| Artifact | {DIGEST} | Verified / Revoked | {REFERENCE} |
| SonarQube | {TASK/GATE} | Passed / Failed / Waived | {REFERENCE} |
| Trivy | {REPORT/DIGEST/DB_TIME} | Passed / Failed / Waived | {REFERENCE} |
| QA evidence | {TEST_RUN} | {VERDICT} | {REFERENCE} |
| Environment readiness | {DOC_VERSION} | Ready / Not Ready / Expired | {REFERENCE} |
| Backup/migration | {REFERENCE} | Ready / Blocked | {REFERENCE} |

## 4. Stop Conditions

Stop before mutation for unknown/mismatched target or digest; missing/expired authorization/window; failed mandatory control without valid waiver; unavailable telemetry; failed backup/precheck; unexpected drift; unapproved command; or missing rollback path.

## 5. Pre-Deployment Checklist

| Check | Expected | Evidence/command | Result |
|---|---|---|---|
| Current target identity | {EXPECTED} | {NON_MUTATING_COMMAND} | Not Run |
| Current deployed digest | {EXPECTED/PREVIOUS} | {COMMAND} | Not Run |
| Service/VM health | {EXPECTED} | {COMMAND/LINK} | Not Run |
| Capacity/storage | {EXPECTED} | {COMMAND/LINK} | Not Run |
| Backup/restore point | {EXPECTED} | {REFERENCE} | Not Run |
| Dependencies | {EXPECTED} | {CHECKS} | Not Run |
| Monitoring/alerts | Available | {LINK/CHECK} | Not Run |
| Rollback artifact | {PREVIOUS_DIGEST} | {REFERENCE} | Not Run |
| Communication | Sent | {REFERENCE} | Not Run |

## 6. Deployment Procedure

For each step, replace placeholders only after validation.

| # | Purpose | Jenkins stage/command | Expected effect | Reversible? | Evidence/result |
|---:|---|---|---|---|---|
| 1 | Reconfirm authorization | {CHECK} | Scope remains valid | N/A | Not Run |
| 2 | Deploy immutable artifact | {APPROVED_JOB_OR_COMMAND} | Target uses {DIGEST} | Yes/No | Not Run |
| 3 | Check rollout | {COMMAND} | Desired replicas/services healthy | N/A | Not Run |
| 4 | Record release marker | {ACTION} | Telemetry identifies release | Yes | Not Run |

Never paste credentials. Use Jenkins credential IDs/approved secret references.

## 7. Post-Deployment Verification

| Verification | Owner | Observation period | Expected | Evidence/result |
|---|---|---|---|---|
| Artifact identity | DevOps | Immediate | Exact digest | Not Run |
| Health/readiness | DevOps | {PERIOD} | Healthy | Not Run |
| Logs/errors | DevOps | {PERIOD} | Within approved baseline | Not Run |
| Metrics/alerts | DevOps | {PERIOD} | No blocking signal | Not Run |
| Smoke checks | {QA/OWNER} | {PERIOD} | Pass | Not Run |
| Business validation | Business Owner | {PERIOD} | Separate decision | Pending |

State remains `deployed_not_verified` until all declared operational checks pass.

## 8. Rollback Triggers

| Trigger | Source/evidence | Decision authority | Immediate action |
|---|---|---|---|
| {HEALTH/ERROR/DATA/SECURITY_TRIGGER} | {QUERY/ALERT} | {AUTHORITY} | Stop/rollback/escalate |

Thresholds must reference approved policy; do not invent them.

## 9. Rollback Procedure

| # | Purpose | Jenkins stage/command | Expected restored state | Evidence/result |
|---:|---|---|---|---|
| 1 | Record rollback decision | {REFERENCE} | Authority/time captured | Not Run |
| 2 | Restore prior artifact/config | {APPROVED_JOB_OR_COMMAND} | {PREVIOUS_DIGEST} active | Not Run |
| 3 | Handle migration/data | {APPROVED_PROCEDURE} | Data compatibility preserved | Not Run |
| 4 | Verify restored state | {CHECKS} | Health and telemetry recovered | Not Run |
| 5 | Open/update incident | {ACTION} | Ownership/escalation recorded | Not Run |

If rollback fails, do not improvise destructive recovery. Activate incident escalation.

## 10. Communication and Closure

Record start/end, actor, target, digest, Jenkins build, deviations, final state, health evidence, rollback/incident status, open risks, follow-up owner/date, and handoff.

## 11. Execution Log

| Timestamp | Actor/build | Step | Exit/status | Evidence | Deviation |
|---|---|---|---|---|---|
| {TIME} | {ACTOR} | {STEP} | NOT RUN | {REFERENCE} | None |

## 12. Approval

| Decision | Authority | Acting person | Timestamp | Scope/digest/window | Evidence |
|---|---|---|---|---|---|
| Authorize / Reject / Waive | {AUTHORITY} | {PERSON} | {TIME} | {EXACT_SCOPE} | {REFERENCE} |

Runbook approval is not deployment authorization; each production execution needs current authorization.