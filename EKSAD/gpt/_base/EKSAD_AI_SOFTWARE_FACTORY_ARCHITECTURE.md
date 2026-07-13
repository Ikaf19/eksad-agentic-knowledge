# EKSAD AI Software Factory Architecture

> **Classification:** Normative shared architecture standard
> **Applicability:** EKSAD AI-assisted software delivery platform and every project using it
> **Normative terms:** **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as requirements.
> **Status:** Baseline; project-specific exceptions require a recorded decision and authorized risk acceptance.

---

## 1. Purpose and Scope

This standard defines the control plane, runtime responsibilities, deployment assumptions, role boundaries, handoffs, and evidence model of the EKSAD AI Software Factory. It governs how humans, AI role agents, source control, CI/CD, security analysis, and runtime services cooperate without transferring decision authority to automation.

The factory assists delivery; it does not replace accountable people. An AI recommendation, generated document, successful pipeline, or elapsed review period is never approval. Production actions are fail-closed.

This document does not redefine business requirements, application-specific architecture, test verdicts, or project governance. Those remain in their authoritative artifacts and role-owned standards.

## 2. Architectural Principles

1. **Human authority over material decisions.** AI agents MAY prepare, analyze, and recommend; only an authorized human may approve a governed baseline, exception, risk acceptance, or production action.
2. **Separation of duties.** Artifact authorship, independent review, QA verdict, release authorization, and production execution MUST remain distinguishable and attributable.
3. **Evidence before state.** A state transition MUST reference immutable or versioned evidence. A statement such as “done” without evidence MUST NOT unlock dependent work.
4. **Least privilege and fail-closed production.** Missing, expired, ambiguous, or unverifiable authorization MUST deny production execution.
5. **One delivery authority.** Jenkins is the CI/CD execution authority. GitLab is source/review/registry coordination; it MUST NOT become a second, independent production deployment authority.
6. **Reproducibility.** Builds and deployments MUST identify source revision, pipeline run, build inputs, artifact digest, configuration version, and target environment.
7. **No invented policy values.** A required but undecided threshold, retention period, RTO/RPO, quorum, or owner MUST be recorded as `TBD` with owner and due date, and treated as blocking when needed for a gate.
8. **Service ownership and isolation.** Components own their data and interfaces. Cross-component access MUST use declared contracts; direct cross-service database access is prohibited.
9. **Observable operations.** Every governed workflow and production change MUST produce correlated logs, metrics, and audit evidence sufficient to reconstruct who did what, to which artifact/environment, when, and with what result.

## 3. Logical Architecture and Component Responsibilities

| Component | Normative responsibility | Must not be treated as |
|---|---|---|
| **Hermes** | Role routing, workflow assistance, artifact generation, evidence collection, and explicit handoff packaging. It MUST preserve the acting role and source references. | Approval authority, test verdict authority, or production identity shared by humans. |
| **General router** | Classify intent and route work to the accountable specialist role. It MUST NOT silently perform specialist approvals or merge incompatible role authorities. | PM, BA, SA, TL, QA, Developer, or DevOps substitute. |
| **LiteLLM** | Controlled model gateway: provider routing, model policy enforcement, request metadata, usage telemetry, and redaction policy integration. | Source of truth for project state or a store for secrets in prompts. |
| **Milvus** | Vector retrieval index for approved/eligible knowledge. Every vector record MUST retain source ID, version, classification, and access scope. | Authoritative document store or approval ledger. |
| **MinIO** | Object storage for controlled artifacts, reports, exports, backups, and evidence where configured. Objects MUST have access controls, integrity metadata, retention classification, and lifecycle ownership. | Secret manager or sole copy of source-controlled definitions. |
| **PostgreSQL** | Transactional metadata such as workflow state, evidence index, authorization records, and configuration metadata according to component schema ownership. | Shared database for bypassing service APIs. |
| **Redis** | Ephemeral cache, coordination, rate limiting, or short-lived job state. Loss of Redis MUST NOT destroy the authoritative approval/evidence history. | System of record, durable authorization ledger, or secret vault. |
| **Keycloak** | Human/service authentication, federation, groups/roles, token issuance, and session policy. Production authorization MUST use attributable identities and least-privilege roles. | Project gate engine or substitute for release approval evidence. |
| **GitLab CE** | Authoritative Git repositories, merge requests, issues, branch/tag controls, and container/package registry where selected. Git history and MR decisions form part of traceability. | Independent production deployment authority. |
| **Jenkins** | Authoritative CI/CD orchestration, controlled credentials binding, quality/security tool invocation, artifact promotion, deployment execution, and evidence publication. | Business owner, QA verdict authority, or automatic production approver. |
| **SonarQube** | Static code analysis and quality-gate result consumed by Jenkins. Rule profiles and gate definitions MUST be versioned or administratively traceable. | CI/CD orchestrator or risk-acceptance authority. |
| **Trivy** | Vulnerability, misconfiguration, secret, image, and/or filesystem scanning as explicitly configured through Jenkins. Scan mode and database freshness MUST be evidenced. | Sole security assurance mechanism or risk-acceptance authority. |
| **Prometheus** | Metrics collection and alert-rule evaluation. Scrape targets and labels MUST distinguish environment, service, version, and instance where technically available. | Durable log/audit store. |
| **Grafana** | Dashboards and operational visualization over approved data sources. Dashboard revisions used for release/incident evidence MUST be identifiable. | Source of raw telemetry truth. |
| **Loki** | Central log aggregation with controlled access and searchable correlation fields. Sensitive values MUST be redacted before ingestion. | Secret store or replacement for security audit records. |

## 4. Three-VM Deployment Topology

### 4.1 Baseline assumptions

The baseline is three independently administered Linux VMs running Docker Compose workloads. Exact hostnames, addresses, CPU, memory, storage, network zones, backup targets, and capacity limits are deployment-specific and MUST be documented in the environment inventory; they are not defined here.

| VM | Baseline responsibility | Typical components | Isolation rule |
|---|---|---|---|
| **VM-1 — Factory / Control Plane** | AI workflow and identity-facing factory services | Hermes, LiteLLM, Keycloak, and approved supporting services | MUST NOT expose administrative endpoints publicly; model/provider credentials remain server-side. |
| **VM-2 — Data / Knowledge Plane** | Durable data and retrieval services | PostgreSQL, Milvus, MinIO, Redis | MUST accept traffic only from approved networks/services; backup and restore ownership is explicit. |
| **VM-3 — Delivery / Observability Plane** | SCM/CI tooling integration endpoints and telemetry services, subject to capacity and organizational hosting decisions | Jenkins, SonarQube, Trivy execution support, Prometheus, Grafana, Loki; GitLab CE if locally hosted | Delivery credentials and production runners/executors MUST be isolated by environment and privilege. |

GitLab CE MAY be externally managed rather than placed on VM-3. The inventory MUST record the actual placement. Component placement MAY change through an approved architecture decision, but logical responsibilities and trust boundaries MUST remain.

### 4.2 Network and exposure rules

- Only required ports and flows documented in a network matrix MAY be opened.
- Administrative UIs MUST be restricted to approved management networks and authenticated through the designated identity control where supported.
- East-west service communication MUST be authenticated where supported and protected in transit according to the approved environment security design.
- Databases, Redis, Milvus, MinIO administrative APIs, Docker sockets, and Jenkins agent/control interfaces MUST NOT be directly exposed to untrusted networks.
- Docker Compose files MUST use explicit networks, persistent volume declarations, health checks where supported, and restart behavior appropriate to the component.
- The actual TLS termination pattern, certificate authority, DNS, firewall owner, and ingress/proxy approval are `TBD` unless recorded in the environment design. DevOps MAY implement an approved proxy design but MUST NOT self-approve it.
- A topology validation record MUST identify single points of failure. Three VMs do not imply high availability.

## 5. Role Boundaries and Cross-Role Handoffs

### 5.1 Accountabilities

| Role | Owns | Required outbound handoff | Explicit non-ownership |
|---|---|---|---|
| **Project Manager (PM)** | Plan, dependencies, RAID, governance coordination, gate tracking | Approved/waived initiation basis, priorities, schedule constraints, named decision authorities | Specialist content approval, test verdict, production execution |
| **Business Analyst (BA)** | User requirements, BRD, FSD business behavior, business traceability | Versioned approved/eligible requirements, acceptance criteria, assumptions and open questions | Technical architecture, pipeline design, production approval |
| **System Analyst / design authority** | TSD, service/data/API/event/security/deployment design and technical requirement mapping | Versioned design, migration implications, NFRs, operational dependencies, design approval evidence | Business baseline approval, implementation completion, QA verdict |
| **Technical Leader (TL)** | Implementation readiness, engineering standards, code review disposition, technical acceptance recommendation | Review evidence, accepted design implementation, technical risks, build readiness | Business acceptance, QA verdict, production authorization unless separately appointed |
| **Developer BE/FE** | Business code, unit/component tests, source changes, implementation evidence | MR/commit, requirement links, tests, migration/config notes, known limitations | Self-approval of protected changes, QA verdict, pipeline/prod administration |
| **QA** | Test strategy, independent execution evidence, defect status, QA verdict | Versioned test result tied to artifact/environment, residual defects and recommendation | Code ownership, deployment execution, business risk acceptance |
| **DevOps** | Pipeline/platform implementation, environment automation, artifact promotion/deployment execution, operational evidence | Pipeline/run IDs, artifact digest, target/config, deployment and rollback evidence, health/telemetry links | BRD/FSD/TSD ownership, business code, test verdict, project governance, proxy approval, production authorization |
| **General router** | Correct role dispatch and context preservation | Routed request with source, scope, constraints, and expected output | Any specialist decision or approval |

A person holding multiple roles MUST declare the role under which each decision is made. Where policy requires independence, one person MUST NOT satisfy both sides merely by changing role labels.

### 5.2 Handoff envelope

Every cross-role handoff MUST include:

- handoff ID and timestamp;
- source and receiving role;
- project/repository/service and environment scope;
- source artifact IDs, versions/commits, and approval state;
- requirement, decision, task, defect, and risk IDs affected;
- requested action and expected output;
- acceptance criteria and applicable gate;
- dependencies, assumptions, constraints, and open `TBD` entries;
- evidence links with access classification;
- responsible owner and due date for every unresolved blocker.

The receiver MUST acknowledge one of: `ACCEPTED`, `RETURNED_FOR_CLARIFICATION`, or `REJECTED_OUT_OF_SCOPE`, with reason. Acceptance means the package is workable, not that its content is approved.

## 6. Traceability and Evidence Model

### 6.1 Trace chain

The minimum bidirectional chain is:

`Objective/Charter → UR → BRD rule/requirement → FSD feature/acceptance criterion/NFR → TSD decision/contract → task → commit/MR → build → test + SonarQube + Trivy → immutable artifact digest → named release authorization → deployment → runtime verification → release closure`.

Every production artifact MUST be traceable backward to an approved or explicitly waived scope, and every in-scope approved requirement MUST trace forward to implementation and verification or an authorized disposition.

### 6.2 Evidence record

Each evidence item MUST contain, directly or by reference:

| Field | Requirement |
|---|---|
| Evidence ID/type | Stable identifier and category |
| Subject | Requirement, decision, source revision, artifact digest, deployment, incident, or gate |
| Producer | Human/service identity and role |
| Time | Generation and, if applicable, expiry time |
| Context | Repository, branch/tag, pipeline/run, tool version/config, environment |
| Result | Machine-readable status plus human-readable summary |
| Integrity | Git object ID, artifact digest, checksum, signed record, or protected immutable reference as applicable |
| Location/classification | Durable URI/path and access/retention classification |
| Relationships | Parent/child evidence, supersedes/superseded-by, requirement/task/defect/risk links |
| Authority | Reviewer/approver and authority source for decisions |

Mutable dashboards and “latest” URLs MAY aid navigation but MUST NOT be the only release evidence. A snapshot, run-specific query, exported result, or immutable record MUST anchor the decision.

### 6.3 Evidence integrity and retention

- Evidence MUST be readable by authorized auditors without relying on an individual workstation.
- Pipeline logs MUST redact credentials and tokens.
- Re-runs MUST create a new evidence record; they MUST NOT overwrite a prior result.
- Manual evidence uploads MUST identify uploader, source, reason, and integrity value.
- Retention periods and legal holds are `TBD` unless defined by policy; record `TBD owner/due`. Until resolved, evidence required for an open release, audit, incident, or risk MUST NOT be deleted.

## 7. Delivery Tool Contracts

### 7.1 GitLab CE contract

- Protected branches/tags MUST reject unauthorized direct changes.
- Merge requests MUST carry requirement/task links, review evidence, and the Jenkins result for the exact source revision.
- Required reviewers and merge strategy are project-governed values; if undefined, record `TBD owner/due` and keep protected release flow blocked.
- GitLab webhooks MAY trigger Jenkins but MUST be authenticated and replay-safe where supported.
- Image/package references promoted beyond development MUST use immutable versions/digests, not only mutable tags.
- A merge is source integration, not QA approval, release authorization, or proof of deployment.

### 7.2 Jenkins contract

- Jenkinsfiles and shared-library revisions MUST be version-controlled and reviewable.
- Jenkins MUST build the checked-out immutable revision, invoke required tests, SonarQube, and Trivy, then publish run-specific evidence.
- Jenkins MUST NOT convert an unavailable mandatory scanner into success. Result is failed or blocked unless an authorized exception explicitly permits continuation.
- Environment promotion MUST reuse the same verified artifact digest; rebuilding for production is prohibited unless the new build repeats all applicable gates and receives new authorization.
- Production stages MUST require validated, scoped, unexpired authorization and an eligible artifact. Inputs MUST identify actor and decision evidence.
- Credentials MUST use Jenkins credential binding or an approved secret backend and be masked; no credential in repository, parameters with unrestricted read access, image layers, or logs.

### 7.3 SonarQube contract

- Jenkins MUST submit analysis for the exact source revision and wait for the authoritative quality-gate result when that gate is mandatory.
- Evidence MUST include project key, source revision, analysis/task ID, quality profile/gate identity, result, and server reference.
- Quality thresholds are owned in the approved SonarQube gate/configuration. This document invents none. Undefined required gates are `TBD owner/due` and block release readiness.
- A waived finding remains visible with rationale, authority, scope, expiry/review date, and follow-up owner.

### 7.4 Trivy contract

- Jenkins MUST run the approved scan modes at the defined stages. Evidence MUST state target/digest, scan modes, Trivy version, vulnerability database update/freshness data, policy/config identity, and result.
- Severity policy and exception windows are policy-owned values. If absent, record `TBD owner/due`; do not silently infer thresholds.
- Findings MUST map to remediation, accepted risk, false-positive disposition, or release blocker.
- A scan of one image digest MUST NOT authorize a different digest.

## 8. Factory Workflow States and RAG

### 8.1 Canonical states

`DRAFT → IN_REVIEW → CHANGES_REQUIRED → READY_FOR_DECISION → APPROVED | REJECTED | WAIVED → IMPLEMENTING → VERIFYING → RELEASE_READY → AUTHORIZED → DEPLOYING → DEPLOYED → VERIFIED → CLOSED`.

`BLOCKED`, `FAILED`, `ROLLED_BACK`, and `ABORTED` are explicit terminal or interrupt states as context dictates. Only verified authorities can set `APPROVED`, `WAIVED`, or `AUTHORIZED`. `COMPLETED` is not synonymous with any approval state.

### 8.2 RAG health

RAG communicates health; it does not override gates.

- **GREEN:** required evidence is current, no known blocking dependency or failed mandatory control, and the next transition is eligible.
- **AMBER:** credible risk, unresolved non-blocking gap, approaching dependency/due date, or conditional evidence requiring attention; owner and due date MUST exist.
- **RED:** failed mandatory control, missing/invalid authority, blocking dependency, material unowned risk, production verification failure, or unauthorized drift.
- **UNKNOWN:** evidence is absent, stale, inaccessible, or contradictory. UNKNOWN MUST be treated as not ready and fail-closed for production.

Numeric RAG thresholds, if desired, are project policy values and MUST be recorded as `TBD owner/due` until approved.

## 9. Security and Secret Handling

- Secrets MUST reside only in an approved secret store or platform credential facility and be delivered just-in-time to the minimum scope.
- Repositories, prompts, vector stores, tickets, chat transcripts, Compose files, images, test fixtures, dashboards, and logs MUST NOT contain plaintext production secrets.
- Service accounts MUST be unique by system/purpose/environment, non-interactive where feasible, and least-privileged.
- Human production actions MUST use personal attributable identities; shared human accounts are prohibited.
- Secret rotation, revocation, access review, and emergency break-glass procedures MUST be documented and evidenced. Their frequencies are `TBD` unless approved, with owner/due.
- Suspected disclosure MUST trigger revocation/rotation and incident handling; merely deleting Git history or logs is insufficient.
- Model prompts and retrieval content MUST be classified and filtered to prevent unauthorized disclosure across projects or tenants.

## 10. Availability, Backup, DR, and Observability

### 10.1 Backup and disaster recovery

- PostgreSQL, MinIO, Milvus, Keycloak state, GitLab/Jenkins/SonarQube state if locally hosted, and observability configuration/data MUST have documented backup scope or an explicit rationale for rebuild-only treatment.
- Backups MUST be encrypted, access-controlled, monitored, and stored outside the failure domain they protect.
- Restore tests MUST verify usability, not only backup job completion, and produce evidence.
- RTO, RPO, backup frequency, retention, off-site location, and restore-test cadence are environment-specific: `TBD owner/due` until approved. Missing values keep DR readiness UNKNOWN/RED as applicable.
- Compose definitions, configuration, schema migrations, dashboard/alert definitions, and runbooks MUST be version-controlled so a VM can be reconstructed.

### 10.2 Observability

- Services MUST emit health, structured logs, metrics, and correlation identifiers suitable for tracing a request/workflow across components. Secrets and sensitive payloads MUST be excluded or redacted.
- Release markers MUST include environment, service, version, artifact digest, pipeline/run, and deployment time.
- Alerts MUST identify owner, severity/routing policy, runbook, and escalation path. Undefined alert thresholds MUST be `TBD owner/due`, not guessed.
- Monitoring failure or telemetry blindness during a production change MUST be treated as a release blocker unless an authorized exception defines compensating controls.
- Clock synchronization and consistent timestamps are required for evidence correlation.

## 11. Architecture Exceptions and TBD Register

An exception MUST identify the violated clause, scope, rationale, alternatives, security/operational impact, compensating controls, approving authority, expiry/review date, and remediation owner/due. Exceptions MUST NOT be hidden in pipeline code or chat.

Use this format for every unresolved value:

| TBD ID | Decision/value needed | Blocking scope | Owner | Due date | Status/evidence |
|---|---|---|---|---|---|
| `TBD-ARCH-<NNN>` | Description | Gate/environment/component | Named role/person | Explicit date | Open / decided + reference |

A blank owner or due date is invalid. If no owner or date can yet be named, use `TBD (appointing authority: <role>, due: <date>)` rather than silently proceeding.

## 12. Conformance Checklist

A factory deployment conforms only when:

- component inventory and actual VM placement are documented;
- trust boundaries and allowed network flows are approved;
- every role handoff uses versioned artifacts and IDs;
- GitLab/Jenkins/SonarQube/Trivy contracts are implemented and evidenced;
- production execution is fail-closed and attributable;
- secrets are absent from prohibited locations;
- backup/restore and observability responsibilities are assigned;
- all unresolved architecture values appear in the TBD register with owner/due; and
- exceptions are explicit, authorized, scoped, and time-bound.
