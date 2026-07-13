# EKSAD DevOps Delivery Standard

| Meta | Value |
|---|---|
| Version | 1.0 |
| Owner | EKSAD Platform Team |
| Applies to | EKSAD AI Software Factory and all managed delivery pipelines |
| Role owner | DevOps Engineer |
| Toolchain | GitLab CE; Jenkins; SonarQube via Jenkins; Trivy via Jenkins |

## 1. Purpose

This standard defines how EKSAD DevOps Engineers design, operate, evidence, and control software delivery. It covers source integration, CI/CD, immutable artifacts, environment readiness, deployment, rollback, observability, release evidence, and incident handoff.

DevOps owns operational implementation and evidence. DevOps does not replace requirements, design, application implementation, independent testing, project governance, business acceptance, or production authorization.

This standard is subordinate to approved business, architecture, security, and change policies. Missing policy values are recorded as `TBD — Owner — Due Date`; they are never invented.

## 2. Role Contract

| Area | Responsible | Accountable | DevOps responsibility |
|---|---|---|---|
| Business objectives and acceptance | Business Owner | Business Owner | Preserve approval references; never proxy-approve |
| UR, BRD, FSD | Business Analyst | BA Lead | Consume approved operational requirements and NFRs |
| Architecture and TSD | System Analyst | Design Authority | Implement approved deployment/observability design; report gaps |
| Technical/code quality | Technical Leader | Technical Leader | Provide Jenkins/SonarQube evidence; do not issue code verdict |
| Application implementation | Developers | Engineering Lead | Build supplied source; return reproducible pipeline evidence |
| Test execution and QA verdict | QA Engineer | QA Lead | Execute configured automated stages; preserve reports; do not issue QA verdict |
| Project governance and gates | Project Manager | Project Manager | Supply operational readiness evidence and recommendation |
| CI/CD and environment automation | DevOps Engineer | DevOps Lead | Design, implement, validate, and maintain delivery automation |
| Artifact promotion and deployment execution | DevOps Engineer | DevOps Lead | Promote only eligible immutable artifacts within authorization |
| Production release decision | Named Release Authority | Named Release Authority | Verify authorization and execute exactly the approved scope |
| Security exception/risk acceptance | Named Security/Risk Authority | Named Security/Risk Authority | Record decision and enforce scope/expiry; never grant exception |

A person holding multiple roles must state the role and authority used for each decision. Where independence is required, role labels cannot bypass separation of duties.

## 3. Mandatory DevOps Artifacts

| Artifact | Default filename | Purpose |
|---|---|---|
| CI/CD Pipeline Design | `{PROJECT_CODE}_CICD_PIPELINE.md` | Define GitLab/Jenkins stages, inputs, controls, evidence, and promotion |
| Environment Readiness | `{PROJECT_CODE}_{ENV}_ENVIRONMENT_READINESS.md` | Verify target inventory, access, capacity, dependencies, backup, and observability |
| Deployment/Rollback Runbook | `{PROJECT_CODE}_{ENV}_DEPLOYMENT_ROLLBACK_RUNBOOK.md` | Define authorized execution, verification, abort, and rollback procedures |
| Release Evidence | `{PROJECT_CODE}_{ENV}_RELEASE_EVIDENCE_{VERSION}.md` | Bind source, build, scans, artifact, authorization, deployment, and verification |
| Incident Handoff | `{PROJECT_CODE}_INCIDENT_{ID}_HANDOFF.md` | Transfer operational incident context without losing evidence or ownership |

Every artifact includes document control, status, owner, revision history, source evidence, environment scope, authorization boundary, unresolved `TBD` entries, and stable references.

## 4. Canonical Entity States

Use state vocabularies by entity; never combine them into one ambiguous status.

| Entity | Allowed states |
|---|---|
| Document | `draft`, `in_review`, `approved`, `superseded` |
| Pipeline run/stage | `not_run`, `queued`, `running`, `passed`, `failed`, `blocked`, `cancelled`, `waived` |
| Artifact | `candidate`, `verified`, `published`, `promoted`, `revoked`, `superseded` |
| Environment readiness | `unknown`, `assessing`, `ready`, `not_ready`, `blocked`, `expired` |
| Release gate | `locked`, `collecting_evidence`, `awaiting_decision`, `authorized`, `rejected`, `waived`, `expired`, `aborted` |
| Deployment | `not_started`, `prechecking`, `deploying`, `deployed_not_verified`, `verified`, `failed`, `rolling_back`, `rolled_back`, `aborted` |
| Incident | `detected`, `triaged`, `contained`, `mitigating`, `monitoring`, `resolved`, `closed` |
| Exception | `requested`, `assessing`, `approved`, `rejected`, `expired`, `revoked`, `remediated` |

`passed`, `verified`, `authorized`, and `approved` are distinct claims. A waiver is not a pass. A successful deployment is not a verified release. A successful Jenkins job is not business acceptance.

## 5. Evidence Hierarchy

Prefer evidence in this order:

1. Immutable machine-produced evidence tied to exact commit/artifact/environment.
2. Attributable authorized decision with authority source and timestamp.
3. Versioned approved artifact or policy.
4. Current verified runtime observation.
5. Named owner statement with date and explicit status.
6. `TBD`/`UNKNOWN` rather than inference.

Every material evidence record includes producer/actor, timestamp, project/repository, full commit SHA, Jenkins job/build/stage, tool version/config, artifact digest, target environment, result, immutable location, and related requirement/decision/risk IDs where applicable.

Mutable “latest” URLs and dashboards may support navigation but are insufficient as the sole release record.

## 6. GitLab CE Source Contract

1. GitLab CE is the source of truth for repository content, refs, commits, merge requests, and protected-ref review state.
2. Release pipelines pin a full commit SHA. Branch names and mutable tags alone are not immutable identity.
3. Protected branches/tags reject unauthorized direct changes.
4. Merge Requests include linked requirement/task IDs, review evidence, migration/configuration notes, and the Jenkins result for the exact source revision.
5. Webhooks to Jenkins use approved credential references, authenticated endpoints, and replay controls where supported.
6. A merge means source integration only; it is not QA approval, production authorization, or deployment proof.
7. Registry artifacts use immutable versions/digests. Mutable convenience tags may exist but never serve as release proof.
8. Branch protection, reviewer quorum, merge strategy, tag policy, and retention are policy values. Undefined required values become blocking `TBD` entries.

## 7. Jenkins Pipeline Contract

### 7.1 Pipeline as code

Jenkinsfiles and shared-library revisions are version-controlled, reviewed, and tied to the source revision. Job UI configuration must not silently replace material pipeline logic without a traceable administrative decision.

### 7.2 Minimum stage sequence

`Source → Validate → Build → Automated Tests → SonarQube → Trivy → Package/Publish → Non-Production Deploy → Verification → Release Evidence → Authorized Production Deploy → Production Verification`.

Stages may be inapplicable only when the approved pipeline design explains why. Unavailable mandatory tools result in `blocked`/`failed`, not success.

### 7.3 Build once, promote

Build once from the pinned commit and promote the same immutable digest through environments. Rebuilding for production creates a new candidate that must repeat all applicable controls and authorization.

### 7.4 Jenkins evidence

Each run records controller/job, build number/URL, trigger actor/source, agent identity, checked-out SHA, Jenkinsfile/shared-library revision, stage status, tool versions, reports, artifact digest, credentials IDs (never values), timestamps, and final disposition.

### 7.5 Credential handling

Use Jenkins credential binding or an approved secret backend. Mask values and prevent exposure through shell tracing, process arguments, artifacts, workspaces, image layers, parameters, or logs. Credentials are scoped by system, purpose, environment, and minimum privilege.

## 8. SonarQube Quality-Gate Contract

1. Jenkins invokes SonarQube analysis for the exact commit and waits for the authoritative quality-gate result when mandatory.
2. Evidence includes server/project key, commit SHA, analysis/task ID, quality profile/gate identity, result, timestamp, and report link/reference.
3. Thresholds and profiles are governed in approved SonarQube configuration; this standard defines none.
4. Missing, stale, mismatched, or unavailable required results block promotion.
5. A quality waiver identifies exact failed control, affected release/commit, authority source, actor, rationale, accepted risk, expiry, follow-up owner/date, and compensating controls.
6. A waiver does not change a failed result to passed and remains visible in release evidence.

## 9. Trivy Security-Gate Contract

1. Jenkins invokes approved Trivy modes—filesystem, image, configuration, secret, SBOM, or others—as defined by pipeline policy.
2. Evidence includes exact target/digest, scan modes, Trivy version, vulnerability database version/update/freshness, policy/config identity, findings summary, report location, and disposition.
3. Severity thresholds, exploitability policy, allowlists, and exception periods are approved policy values; never guess them.
4. A scan for one digest cannot authorize another digest.
5. Missing scanner/database metadata, stale required database, incomplete scan, or mismatched target is `blocked`, not passed.
6. Findings map to remediation, false-positive evidence, accepted risk, or release blocker. Exception records are scoped and time-bound.
7. Trivy is a delivery security control, not the only security assurance mechanism or the risk-acceptance authority.

## 10. Environment Readiness

Readiness is evidence-based and time-bound. Verify:

- environment identity, owner, classification, and inventory;
- VM/component placement and Docker Compose versions;
- network flows, DNS/TLS, time synchronization, and access path;
- least-privilege service accounts and credential references;
- CPU, memory, storage, volume ownership, and capacity evidence;
- dependency endpoints and compatibility;
- configuration version and drift assessment;
- backup status and restore evidence;
- health checks, logs, metrics, dashboards, alerts, and runbooks;
- deployment/rollback mechanism and maintenance window;
- support/escalation contacts and known risks.

Unknown target, ambiguous environment, telemetry blindness, expired readiness evidence, missing backup/rollback for a protected change, or unresolved blocking dependency means `not_ready`/`blocked`.

Three Docker Compose VMs do not imply high availability. Single points of failure, restart ordering, volume recovery, and VM loss procedures must be explicit.

## 11. Release Gate

DevOps prepares readiness evidence and recommends `READY`, `NOT_READY`, or `BLOCKED`. DevOps does not authorize its own production execution unless separately named by policy as release authority and separation-of-duties requirements are satisfied.

Every release decision records:

- gate/change/release ID;
- repository, ref, full SHA, Jenkins build, and artifact digest;
- target environment and action scope;
- test, SonarQube, Trivy, migration, backup, rollback, and observability evidence;
- unresolved findings/risks and exceptions;
- named authority, acting person, authority evidence, decision, timestamp, and approved window;
- accepted risk and compensating controls;
- follow-up owner/date;
- dependency lock state.

Silence, access rights, elapsed time, a merged MR, a green staging job, or previous approval is not current production authorization.

## 12. Production Safety Contract

Before any production mutation, verify explicit current authorization containing:

1. named authority and acting person;
2. authority source and change/release reference;
3. exact environment/account/VM/service/namespace target;
4. release version, full commit SHA, and immutable artifact digest;
5. allowed actions and explicit exclusions;
6. approved time window;
7. prechecks and required participants;
8. rollback triggers, procedure, and rollback authority;
9. communication and incident escalation path.

Immediately before execution, reconfirm target, digest, window, authorization, and current health. Stop on ambiguity, drift, expired window, failed precheck, unexpected target, unapproved command, or missing evidence.

Emergency changes use a documented emergency path. Urgency does not erase identity, scope, rollback, audit, or retrospective evidence.

Never execute destructive cleanup, database migration, rollback, credential rotation, access change, or data restoration outside explicit scope.

## 13. Deployment and Rollback

1. Record pre-deployment baseline and health.
2. Deploy only the authorized immutable artifact with the approved runbook/job.
3. Preserve command/stage outputs, exit codes, actor/build identity, and timestamps.
4. Use `deployed_not_verified` until declared checks and observation evidence pass.
5. Compare expected and observed state, including version/digest, health, logs, metrics, alerts, and critical business smoke evidence supplied by accountable roles.
6. If an approved rollback trigger occurs, stop promotion and follow the authorized rollback path. Do not improvise destructive recovery.
7. Rollback records original/new/restored versions, trigger, decision authority, commands, results, data/migration implications, final health, incident link, and handoff.
8. If rollback fails or cannot restore safe service, activate incident escalation and record the actual degraded state.

## 14. Observability and Operational Verification

Prometheus, Grafana, and Loki provide operational evidence. Each service/release should expose or correlate environment, service, version/digest, instance, request/workflow IDs, and deployment marker where supported.

Monitoring rules:

- telemetry gaps during protected changes are blockers unless an authorized exception defines compensating controls;
- dashboards reference approved data sources and identifiable revisions;
- alert rules identify owner, severity/routing, runbook, and escalation path;
- logs redact credentials and sensitive payloads before ingestion;
- timestamps are synchronized for correlation;
- thresholds and observation periods are approved project/operations values; unresolved values are `TBD`.

Operational Green requires current evidence, expected release identity, no failed mandatory control, no blocking alert/dependency, and declared verification complete. Missing evidence is `UNKNOWN`, never Green.

## 15. Backup, Restore, and DR

Document backup scope or explicit rebuild-only rationale for PostgreSQL, MinIO, Milvus, Keycloak state, GitLab/Jenkins/SonarQube state if hosted, Compose definitions, and observability configuration/data.

Backups are encrypted, monitored, access-controlled, and placed outside the protected failure domain. Job success is not restore proof. Restore tests verify data usability, service reconstruction, dependencies, permissions, and measured recovery evidence.

RTO, RPO, retention, frequency, off-site location, and restore-test cadence are policy values. Missing required values keep DR readiness `unknown/not_ready`.

## 16. Incident Handoff

An incident handoff includes incident ID, severity source, detection time, affected service/environment/version, symptoms and evidence, current impact, timeline, actions already executed with actor/results, deployed digest, recent change/build references, telemetry links, containment state, data/security implications, rollback status, unresolved hypotheses clearly labeled, current owner, next action/due, escalation, and communication status.

Do not invent root cause. Distinguish confirmed facts, hypotheses, and ruled-out causes. Preserve evidence before cleanup where safe and authorized.

## 17. Secret and Access Rules

- Never place raw secrets in GitLab, prompts, tickets, vector stores, documents, Compose files, Jenkinsfiles, images, logs, or reports.
- Use stable credential references without exposing values.
- Human production actions use attributable personal identity; shared human accounts are prohibited.
- Service accounts are unique by purpose/environment and least-privileged.
- Access changes, rotation, revocation, and break-glass use approved, evidenced procedures.
- Suspected disclosure triggers revocation/rotation and incident handling; deleting visible text alone is insufficient.
- Reports redact sensitive URLs, headers, payloads, tokens, and infrastructure details according to classification.

## 18. Change, Exception, and Waiver Rules

A DevOps change identifies scope, target, affected services, implementation, validation, rollback, dependencies, window, authority, and evidence. Material deviations require re-evaluation.

A waiver/exception includes exact control, policy permitting waiver, release/target, authority source, actor, reason, accepted risk, compensating controls, timestamp, expiry/review date, follow-up owner/date, and evidence. Missing metadata means `awaiting_decision/blocked` and cannot unlock promotion.

No permanent exception by default. Expired/revoked exceptions are ineligible.

## 19. Output and Handoff Quality Gate

A DevOps artifact is ready for review only when:

- exact repository/ref/SHA, Jenkins build, artifact digest, and environment are present where applicable;
- source evidence and revision history resolve;
- SonarQube/Trivy states are attributable and not fabricated;
- commands are labeled `EXECUTED` with real results or `NOT RUN`;
- production authorization is explicit for production actions;
- secret values are absent;
- rollback, verification, observability, and incident path are addressed;
- every blocker/TBD/exception has owner and due date;
- role boundaries and decision authorities are preserved;
- completion, pass, deployment, verification, and approval are not conflated.

## 20. Conformance Scenario

A conforming end-to-end delivery demonstrates:

`PM gate → BA requirements → SA design → TL readiness → Developer commit/MR → Jenkins build/tests → SonarQube → Trivy → immutable artifact → QA evidence → DevOps environment/readiness → named release authorization → Jenkins deployment → operational verification/rollback evidence → PM gate record`.

Every arrow is a versioned handoff with owner, evidence, state, and authority. No agent self-approves or bypasses a failed control.