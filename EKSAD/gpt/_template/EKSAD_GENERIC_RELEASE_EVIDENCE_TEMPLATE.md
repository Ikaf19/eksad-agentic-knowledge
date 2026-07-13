# EKSAD Generic Release Evidence Template

> Filename: `{PROJECT_CODE}_{ENV}_RELEASE_EVIDENCE_{VERSION}.md`
> Owner: DevOps Engineer
> This is an evidence pack, not release authorization or business acceptance.

# {PROJECT_NAME} — {ENVIRONMENT} Release Evidence {RELEASE_VERSION}

## Document Control

| Field | Value |
|---|---|
| Evidence pack ID | {REL-EVIDENCE-ID} |
| Version/status | {VERSION} / Draft / In Review / Approved / Superseded |
| Owner/accountable | {DEVOPS_OWNER} / {DEVOPS_LEAD} |
| Environment | {ENVIRONMENT} |
| Evidence cut-off | {TIMESTAMP} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Review evidence |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial evidence pack | {REFERENCE} |

## 1. Release Identity

| Field | Immutable/exact value | Evidence |
|---|---|---|
| Project/service | {VALUE} | {REFERENCE} |
| Release/change ID | {VALUE} | {REFERENCE} |
| GitLab project | {VALUE} | {REFERENCE} |
| Ref/full commit SHA | {REF} / {FULL_SHA} | {REFERENCE} |
| MR/review | {MR_ID} | {REFERENCE} |
| Jenkins job/build | {JOB} / {BUILD_ID_URL} | {REFERENCE} |
| Artifact name/version | {VALUE} | {REFERENCE} |
| Artifact digest/checksum | {IMMUTABLE_VALUE} | {REFERENCE} |
| Target environment | {EXACT_TARGET} | {REFERENCE} |

Any identity mismatch blocks readiness.

## 2. Upstream Baselines and Handoffs

| Artifact/decision | Version/state | Owner/accountable | Evidence |
|---|---|---|---|
| Charter/Plan/gate | {REFERENCE} | PM | {EVIDENCE} |
| UR/BRD/FSD | {REFERENCE} | BA/BA Lead | {EVIDENCE} |
| Architecture/TSD | {REFERENCE} | SA/Design Authority | {EVIDENCE} |
| Technical readiness | {REFERENCE} | TL | {EVIDENCE} |
| QA evidence/verdict | {REFERENCE} | QA/QA Lead | {EVIDENCE} |

DevOps records these decisions but does not issue them.

## 3. Jenkins Pipeline Evidence

| Stage | State | Tool/version | Start/end | Evidence location | Notes/exception |
|---|---|---|---|---|---|
| Source | Not Run / Passed / Failed / Blocked / Waived | Git/Jenkins | {TIME} | {REFERENCE} | {DETAIL} |
| Validate | {STATE} | {TOOLS} | {TIME} | {REFERENCE} | {DETAIL} |
| Build | {STATE} | {TOOLS} | {TIME} | {REFERENCE} | {DETAIL} |
| Automated tests | {STATE} | {TOOLS} | {TIME} | {REFERENCE} | Not a QA verdict |
| SonarQube | {STATE} | {VERSION} | {TIME} | {REFERENCE} | {DETAIL} |
| Trivy | {STATE} | {VERSION} | {TIME} | {REFERENCE} | {DETAIL} |
| Publish | {STATE} | {REGISTRY} | {TIME} | {REFERENCE} | {DIGEST} |
| Non-prod deploy/verify | {STATE} | {JOB} | {TIME} | {REFERENCE} | {DETAIL} |

## 4. SonarQube Evidence

| Field | Value |
|---|---|
| Server/project key | {REFERENCE} |
| Commit SHA | {FULL_SHA} |
| Analysis/task ID | {ID} |
| Quality profile/gate | {IDENTITY} |
| Result | Passed / Failed / Error / Blocked / Waived |
| Timestamp/report | {VALUE} |
| Failed conditions | {NONE_OR_LIST} |
| Exception | {NONE_OR_EXCEPTION_ID} |

## 5. Trivy Evidence

| Field | Value |
|---|---|
| Exact target/digest | {VALUE} |
| Scan modes | {MODES} |
| Trivy version | {VERSION} |
| DB version/update/freshness | {VALUE} |
| Policy/config | {REFERENCE} |
| Findings summary | {COUNTS_BY_SEVERITY/TYPE} |
| Result | Passed / Failed / Error / Blocked / Waived |
| Report | {IMMUTABLE_OR_VERSIONED_REFERENCE} |
| Exception | {NONE_OR_EXCEPTION_ID} |

## 6. Artifact Provenance

| Field | Value/evidence |
|---|---|
| Build source SHA | {VALUE} |
| Builder/Jenkins agent | {IDENTITY} |
| Build number/time | {VALUE} |
| Dependency/SBOM evidence | {REFERENCE} |
| Signature/provenance | {REFERENCE_OR_NOT_CONFIGURED_WITH_TBD} |
| Registry path/digest | {VALUE} |
| Promotion history | {REFERENCE} |

## 7. Environment and Deployment Readiness

| Control | State | Evidence | Owner/gap |
|---|---|---|---|
| Environment readiness current | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Deployment runbook approved | {STATE} | {REFERENCE} | {DETAIL} |
| Rollback path/artifact | {STATE} | {REFERENCE} | {DETAIL} |
| Backup/migration controls | {STATE} | {REFERENCE} | {DETAIL} |
| Observability/support | {STATE} | {REFERENCE} | {DETAIL} |
| Window/participants | {STATE} | {REFERENCE} | {DETAIL} |

## 8. Findings, Risks, and Exceptions

| ID | Control/finding | State | Authority | Accepted risk | Expiry | Follow-up owner/due | Evidence |
|---|---|---|---|---|---|---|---|
| {ID} | {DETAIL} | Open / Remediated / Waived | {AUTHORITY} | {RISK} | {DATE} | {OWNER/DATE} | {REFERENCE} |

## 9. DevOps Readiness Recommendation

Recommendation: READY / NOT_READY / BLOCKED.

Rationale references evidence only. Missing/stale/contradictory evidence means BLOCKED, not READY.

## 10. Production Decision

| Decision | Named authority | Acting person | Authority evidence | Timestamp/window | Exact target/digest/scope | Risk/follow-up |
|---|---|---|---|---|---|---|
| Authorize / Reject / Waive | {AUTHORITY} | {PERSON} | {REFERENCE} | {VALUE} | {VALUE} | {DETAIL} |

## 11. Deployment and Verification Result

| Field | Value/evidence |
|---|---|
| Jenkins deployment build | {REFERENCE} |
| Actor/start/end | {VALUE} |
| Exact deployed digest | {VALUE} |
| Deployment state | Not Started / Deploying / Deployed Not Verified / Verified / Failed / Rolled Back / Aborted |
| Health/smoke evidence | {REFERENCE} |
| Prometheus/Grafana/Loki evidence | {REFERENCE} |
| Deviations/incident | {NONE_OR_REFERENCE} |
| Rollback decision/result | {NONE_OR_REFERENCE} |
| Final handoff owner | {OWNER} |

## 12. Integrity and Storage

| Artifact | Checksum/digest | MinIO/versioned location | PostgreSQL metadata ID | Retention/classification |
|---|---|---|---|---|
| Release evidence pack | {VALUE} | {REFERENCE} | {ID} | {POLICY} |

## 13. Open Actions

| Action ID | Action | Owner | Due | Blocking? | Evidence/state |
|---|---|---|---|---|---|
| ACT-{PROJECT}-001 | {ACTION} | {OWNER} | {DATE} | Yes/No | Open |

Evidence-pack approval confirms completeness of the record; it does not replace named release authorization.