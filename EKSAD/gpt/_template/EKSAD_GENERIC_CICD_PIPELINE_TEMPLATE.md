# EKSAD Generic CI/CD Pipeline Design Template

> Filename: `{PROJECT_CODE}_CICD_PIPELINE.md`
> Owner: DevOps Engineer
> Toolchain: GitLab CE → Jenkins → SonarQube/Trivy via Jenkins
> Never place raw secrets in this document.

# {PROJECT_NAME} — CI/CD Pipeline Design

## Document Control

| Field | Value |
|---|---|
| Project/service | {PROJECT_AND_SERVICE} |
| Version | {VERSION} |
| Status | Draft / In Review / Approved / Superseded |
| Owner | {DEVOPS_OWNER} |
| Accountable | {DEVOPS_LEAD} |
| Source architecture/TSD | {REFERENCE} |
| Source repository | {GITLAB_PROJECT} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Review/approval evidence |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial design | {REFERENCE_OR_PENDING} |

## 1. Purpose and Scope

{Describe the services, repositories, environments, and delivery outcomes.}

Out of scope: business requirements, application architecture, application implementation, QA verdict, and release authorization.

## 2. Ownership and Authorities

| Responsibility | Responsible | Accountable | Evidence |
|---|---|---|---|
| Source implementation | Developers | Engineering Lead | MR/commit |
| Technical/code review | Technical Leader | Technical Leader | Review decision |
| Test verdict | QA | QA Lead | Test evidence |
| Pipeline implementation | DevOps | DevOps Lead | Reviewed Jenkinsfile |
| Production release decision | {ROLE/PERSON} | {AUTHORITY} | {POLICY/DECISION} |
| Security exception | {ROLE/PERSON} | {AUTHORITY} | {POLICY/DECISION} |

## 3. Source and Trigger Contract

| Item | Definition | Evidence/Control |
|---|---|---|
| GitLab project | {URL_OR_PATH} | {PROJECT_ID} |
| Protected refs | {BRANCHES/TAGS} | {POLICY_REFERENCE} |
| Trigger | MR / merge / tag / manual authorized | {WEBHOOK/JOB_REFERENCE} |
| Jenkinsfile | {PATH} | Commit SHA |
| Shared library | {NAME_AND_REVISION} | Immutable revision |
| Credentials | {CREDENTIAL_IDS_ONLY} | Jenkins binding |

## 4. Pipeline Stage Contract

| # | Stage | Inputs | Commands/Tools | Required evidence | Failure behavior |
|---:|---|---|---|---|---|
| 1 | Source | GitLab ref/full SHA | Jenkins SCM checkout | Project/ref/SHA/actor/build | Stop on mismatch |
| 2 | Validate | Jenkinsfile/config | Lint/parse/dry-run | Tool versions/exits | Block |
| 3 | Build | Pinned SHA | {BUILD_TOOL} | Build log/dependencies | Fail |
| 4 | Automated Tests | Built source | {TEST_COMMANDS} | JUnit/coverage reports | Policy-driven block |
| 5 | SonarQube | Exact SHA | Jenkins SonarQube integration | Task ID/gate/profile/result | Block if mandatory result not pass |
| 6 | Trivy | Source/image/config | Jenkins Trivy stage | Version/DB time/mode/findings/policy | Block per approved policy |
| 7 | Package/Publish | Verified candidate | {REGISTRY_TOOL} | Immutable digest/checksum/provenance | Stop on publish mismatch |
| 8 | Non-Prod Deploy | Same digest | {JENKINS_JOB/RUNBOOK} | Target/rollout/health | Roll back/stop per runbook |
| 9 | Release Evidence | All prior evidence | Evidence pack generation | Immutable evidence reference | Remain locked if incomplete |
| 10 | Production | Authorized digest/target | Approved Jenkins stage | Authorization/build/deploy result | Stop/rollback |
| 11 | Verify | Deployed digest | Health/smoke/telemetry | Observation evidence | Incident/rollback |

## 5. Artifact and Promotion Model

| Artifact | Naming/version | Registry | Immutable identity | Retention owner |
|---|---|---|---|---|
| {ARTIFACT} | {PATTERN} | {REGISTRY_TBD} | Digest/checksum | {OWNER} |

Build once and promote the same digest. Mutable tags are navigation only.

## 6. SonarQube Gate

| Field | Value |
|---|---|
| Server/project key | {REFERENCE} |
| Analysis mode | {MODE} |
| Quality profile/gate | {APPROVED_IDENTITY} |
| Mandatory result | {POLICY_REFERENCE_OR_TBD_OWNER_DUE} |
| Jenkins evidence | Project, SHA, task ID, result, timestamp |
| Exception authority | {ROLE/POLICY} |

Do not invent thresholds. Missing mandatory results block promotion.

## 7. Trivy Gate

| Field | Value |
|---|---|
| Scan modes | Filesystem / image / config / secret / SBOM / {OTHER} |
| Scan targets | {EXACT_TARGETS_OR_DIGESTS} |
| Policy/config | {REFERENCE} |
| DB freshness rule | {POLICY_OR_TBD_OWNER_DUE} |
| Blocking severity/rule | {POLICY_OR_TBD_OWNER_DUE} |
| Evidence | Target/digest, mode, version, DB timestamp, findings, report |
| Exception authority | {ROLE/POLICY} |

## 8. Environment Promotion

| From | To | Entry criteria | Authority | Same-digest check | Verification |
|---|---|---|---|---|---|
| Build | {ENV} | {CRITERIA} | {AUTHORITY} | Required | {CHECKS} |

## 9. Credentials and Access

List credential IDs, purpose, environment, scope, owner, rotation reference, and masking control. Never list values.

| Credential ID | Purpose | Environment | Minimum permission | Owner | Rotation evidence |
|---|---|---|---|---|---|
| {JENKINS_CREDENTIAL_ID} | {PURPOSE} | {ENV} | {SCOPE} | {OWNER} | {REFERENCE} |

## 10. Evidence Publication

| Evidence | Producer | Immutable/versioned location | Metadata/index | Retention policy |
|---|---|---|---|---|
| Jenkins run | Jenkins | {URL/EXPORT} | Build/SHA | {POLICY} |
| SonarQube | Jenkins/SonarQube | {TASK/REPORT} | SHA/gate | {POLICY} |
| Trivy | Jenkins/Trivy | {REPORT} | Digest/DB time | {POLICY} |
| Artifact | Registry | {DIGEST} | Build/SHA | {POLICY} |
| Release pack | DevOps | MinIO/{PATH} | PostgreSQL/{ID} | {POLICY} |

## 11. Notification, Observability, and Support

| Event | Audience | Channel | Owner | Runbook |
|---|---|---|---|---|
| Pipeline failure | {AUDIENCE} | {CHANNEL} | {OWNER} | {REFERENCE} |
| Production deploy | {AUDIENCE} | {CHANNEL} | {OWNER} | {REFERENCE} |

## 12. Failure, Retry, and Recovery

Define retry-safe stages, idempotency, workspace cleanup, artifact preservation, scanner outage behavior, deployment abort, rollback handoff, and incident escalation. Mandatory unavailable controls never become pass.

## 13. TBD and Risk Register

| ID | Gap/risk | Blocking scope | Owner | Due | Evidence/state |
|---|---|---|---|---|---|
| TBD-CICD-001 | {DECISION} | {GATE} | {OWNER} | {DATE} | Open |

## 14. Approval

| Role | Name | Decision | Date | Evidence |
|---|---|---|---|---|
| DevOps Lead | {NAME} | Approve / Revise / Reject | {DATE} | {REFERENCE} |
| Technical Leader | {NAME} | Review only | {DATE} | {REFERENCE} |
| Security authority | {NAME} | Approve policy/exception authority | {DATE} | {REFERENCE} |

Approval of this design does not authorize a production deployment.