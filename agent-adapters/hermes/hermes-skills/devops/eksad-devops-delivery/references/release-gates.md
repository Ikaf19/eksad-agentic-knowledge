# EKSAD DevOps Release Gates

## Purpose

This reference defines the strict release tracker used by `eksad-devops-delivery`. It cannot approve on behalf of a human authority and has no no-gates mode.

## Gate Sequence

`Source Eligible → Build Verified → Quality/Security Eligible → Artifact Published → Environment Ready → Release Decision → Production Execution → Operational Verification`.

A dependent gate remains locked until predecessor evidence is eligible or a policy-permitted waiver explicitly unlocks that dependency.

## Mandatory Gate Record

| Field | Requirement |
|---|---|
| Gate ID/state | Stable ID and canonical state |
| Project/repository | GitLab CE identity |
| Source | Ref and full commit SHA |
| Pipeline | Jenkins controller/job/build and Jenkinsfile/shared-library revision |
| Artifact | Name/version and immutable digest/checksum |
| Environment | Exact target and classification |
| Evidence | Run-specific test, SonarQube, Trivy, artifact, readiness, runbook, rollback, backup/migration, observability, support references |
| Findings | Open defects, vulnerabilities, quality failures, risks, drift, and blockers |
| Exceptions | Exact bypassed control and full waiver metadata |
| Decision | READY/NOT_READY/BLOCKED recommendation; AUTHORIZE/REJECT/WAIVE authority decision |
| Authority | Named authority, acting person, authority evidence, timestamp, window |
| Risk | Accepted risk and compensating controls |
| Follow-up | Owner and due/expiry date |
| Dependency lock | Locked/unlocked with reason/evidence |

## Gate Rules

### Source Eligible

Requires protected-ref eligibility, full SHA, MR/review evidence where policy requires it, and exact Jenkinsfile revision. Merge alone is not release approval.

### Build Verified

Requires a successful Jenkins build of the pinned SHA, reproducible inputs, and immutable candidate digest. Re-running creates a new evidence record.

### Quality/Security Eligible

Requires configured test reports plus authoritative SonarQube and Trivy results from the same Jenkins context. A missing/stale/mismatched mandatory result blocks. Test reports do not constitute QA verdict.

### Artifact Published

Requires source/build correlation, immutable registry digest/checksum, provenance/signature where configured, access controls, and retention metadata. Mutable tags are insufficient.

### Environment Ready

Requires current environment readiness, approved runbook, rollback path/artifact, backup/migration controls, telemetry, support, window, and no blocking drift/dependency.

### Release Decision

DevOps recommends READY/NOT_READY/BLOCKED. Only the named authority records AUTHORIZE/REJECT/WAIVE. Silence, elapsed time, prior access, staging success, or job success is not authorization.

### Production Execution

Requires the production-safety authorization envelope and immediate scope reconfirmation. Exact digest and target must match. Stop on drift, expired window, failed precheck, ambiguity, or widened scope.

### Operational Verification

Requires deployed digest identity, declared health/smoke checks, telemetry observation, release marker, incidents/deviations, and final handoff. Until complete, state is `deployed_not_verified`.

## Waiver Metadata

A valid waiver records:

- policy that permits waiver;
- exact failed/bypassed control;
- affected release, SHA, digest, environment, and scope;
- named authority and acting person;
- authority/artifact evidence;
- decision timestamp;
- reason and accepted risk;
- compensating controls;
- expiry/review date;
- follow-up owner/date;
- dependency unlocked and downstream constraints.

Missing metadata means `awaiting_decision/blocked`. A waiver never changes failed to passed and cannot silently apply to another release or environment.

## Hard Stops

- Unknown or mismatched SHA/digest/target.
- Missing/expired production authorization.
- Failed mandatory control without valid waiver.
- Missing/stale/mismatched SonarQube or Trivy evidence.
- Unresolved policy-blocking security/quality finding or undefined required severity policy.
- Missing rollback for protected change.
- Telemetry blindness without authorized compensating control.
- Unapproved migration/data/destructive operation.
- Generic auto/no-gates path.

## Audit Check

A reviewer must reconstruct objective/requirements/design/task → commit/MR → Jenkins build → tests/scans → digest → target → authorization → deployment → verification/rollback from durable evidence. If the chain breaks, the release is not ready.