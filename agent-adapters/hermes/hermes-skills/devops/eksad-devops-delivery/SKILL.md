---
name: eksad-devops-delivery
description: Use when EKSAD work involves GitLab CE source integration, Jenkins CI/CD, SonarQube or Trivy evidence, immutable artifact promotion, environment readiness, deployment, rollback, observability, release evidence, or incident handoff. Enforces role boundaries, real evidence, secret safety, and fail-closed production authorization.
version: 1.1.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, devops, gitlab, jenkins, sonarqube, trivy, deployment, release, observability]
    related_skills: []
---

# EKSAD DevOps Delivery

## Overview

Operate EKSAD delivery automation using GitLab CE as source/review truth and Jenkins as CI/CD execution authority. SonarQube and Trivy run through Jenkins. Every claim is tied to real evidence; production work is fail-closed.

This skill prepares and executes DevOps-owned work only. It does not grant application code, QA, architecture, PM, business, security-risk, or production-approval authority.

## When to Use

- Design or review Jenkins pipelines and GitLab CE integration.
- Collect SonarQube/Trivy evidence from a Jenkins run.
- Build an immutable release evidence pack.
- Assess environment or operational readiness.
- Draft/validate deployment and rollback runbooks.
- Perform an explicitly authorized deployment or rollback.
- Verify runtime state through Prometheus, Grafana, Loki, health checks, and commands.
- Prepare an incident handoff.

Do not use it to write BRD/FSD/TSD, implement application features, issue code/QA/business verdicts, approve PM gates, accept security risk, or infer production authorization.

## Knowledge Resolution

Resolve `<EKSAD_PACK_ROOT>` in order:

1. `EKSAD_PACK_SRC` when set and valid.
2. Active shared EKSAD knowledge deployment.
3. `~/.hermes/knowledge/eksad`.

Read, as applicable:

- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md`
- observability, resilience, DB deployment, and load-testing standards;
- approved Architecture/TSD, pipeline policy, environment inventory, and runbooks;
- templates under `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/`.

Do not assume profile-local knowledge contains a separate clone. If a required source is absent, report the exact missing path and continue only where safe.

## Role Boundary

| Area | Accountable owner | DevOps action |
|---|---|---|
| Objectives/acceptance | Business Owner | Preserve decision reference |
| UR/BRD/FSD | BA/BA Lead | Consume operational requirements |
| Architecture/TSD | SA/Design Authority | Implement approved deployment design; return gaps |
| Technical/code verdict | Technical Leader | Supply pipeline/quality evidence |
| Application implementation | Developers/Engineering Lead | Build supplied source |
| QA verdict | QA/QA Lead | Preserve reports; never issue verdict |
| PM governance/gates | PM | Supply readiness evidence/recommendation |
| CI/CD/environment/deployment evidence | DevOps/DevOps Lead | Own implementation and verification |
| Production authorization | Named Release Authority | Verify; never impersonate |
| Security waiver | Named Security/Risk Authority | Record/enforce scope and expiry |

For out-of-scope work, identify the accountable role and package a handoff. Never perform specialist work merely to unblock yourself.

## Canonical States

Pipeline: `not_run`, `queued`, `running`, `passed`, `failed`, `blocked`, `cancelled`, `waived`.

Gate: `locked`, `collecting_evidence`, `awaiting_decision`, `authorized`, `rejected`, `waived`, `expired`, `aborted`.

Deployment: `not_started`, `prechecking`, `deploying`, `deployed_not_verified`, `verified`, `failed`, `rolling_back`, `rolled_back`, `aborted`.

Never translate `waived` to `passed`, `deployed` to `verified`, or job success to authorization.

## Workflow

### Step 1 — Establish Scope and Authority

Capture requested outcome, repository/project, full SHA or source ref, target environment, production classification, release/version/digest, allowed actions, exclusions, and expected evidence.

For any mutation, identify acting person/service identity and authorization source. For production, load `references/production-safety.md` and require its full authorization envelope.

Completion criterion: target, identity, mutability, authority, and missing inputs are explicit. Missing safety/authority data is `blocked` before mutation.

### Step 2 — Inspect Authoritative Sources

Read repository configuration, Jenkinsfile/shared-library revision, approved Architecture/TSD, pipeline policy, environment inventory, current deployment identity, runbook, and relevant prior evidence. Inspect before editing or executing.

Never request raw credentials. Record only credential IDs/references and minimum permissions.

Completion criterion: actual source/configuration is distinguished from assumptions and proposals; every gap is `TBD — Owner — Due Date`.

### Step 3 — Validate Source and Pipeline

Pin GitLab CE project/ref/full SHA, MR/review state, trigger actor, Jenkins job/build, Jenkinsfile revision, and shared-library revision. Lint/parse configuration and use dry-run/non-mutating checks where available.

Completion criterion: exact source and pipeline definition are attributable; commands/steps, tool versions, exit codes, and evidence locations are recorded.

### Step 4 — Build Once and Collect Gates

Use Jenkins to build the pinned commit once. Capture build identity and immutable artifact digest. Through Jenkins, collect:

- configured test reports (not a QA verdict);
- SonarQube project/task/profile/gate/result for the exact SHA;
- Trivy target/digest, scan modes, version, database time/freshness, findings, policy, and report.

Unavailable or mismatched mandatory evidence is `blocked/failed`, never pass. Policy thresholds are read from approved configuration; do not invent them.

Completion criterion: SHA → Jenkins build → reports → digest is complete, or the exact blocker is named.

### Step 5 — Publish and Assess Environment

Publish only an eligible immutable candidate. Verify registry identity, digest/checksum, provenance/signature where configured, access controls, and retention metadata.

Generate and retain an SBOM, provenance attestation, and artifact signature only when the approved pipeline/policy configures them. Bind each item to the exact SHA, Jenkins build, artifact digest, tool/version, timestamp, and immutable evidence location; verify configured signatures before promotion. `not_configured` is not `passed`: record the policy/configuration reference and owner. If policy requires a control but configuration or evidence is absent, fail closed.

Assess target inventory, network/TLS/DNS, capacity, access/secrets, dependencies, configuration drift, backup/restore, observability, deployment/rollback, and support readiness.

Completion criterion: environment is `ready`, `not_ready`, `blocked`, `unknown`, or `expired` with evidence, owner, and due date—not an unsupported Green.

### Step 6 — Assemble Release Evidence

Load `references/release-gates.md`. Bind scope, upstream role evidence, full SHA, Jenkins build, SonarQube/Trivy, immutable digest, QA evidence, environment readiness, runbook, rollback, backup/migration, observability, support, findings, and exceptions.

Recommend only `READY`, `NOT_READY`, or `BLOCKED`. Do not authorize.

Completion criterion: every mandatory field resolves or the gate remains locked; waivers retain failed-control identity and full metadata.

### Step 7 — Execute Only Authorized Scope

For non-production, still verify target and permitted mutation. For production, require current explicit authorization and reconfirm immediately before execution.

Use the approved Jenkins job/runbook. Stop on target/digest mismatch, drift, failed precheck, expired window, missing participant, ambiguous instruction, scanner/gate regression, telemetry blindness, or an unapproved command.

Completion criterion: each action records timestamp, actor/build, target, command/stage, exit status, evidence, and deviation; nothing outside scope was changed.

### Step 8 — Verify, Roll Back, and Handoff

Use `deployed_not_verified` until declared health/smoke/telemetry checks pass for the approved observation period. Compare expected and observed digest/state.

Before deployment, copy SLI/SLO/error-budget inputs from approved policy or service ownership evidence; never create values. Use placeholders when absent:

```text
SLI definition/query: TBD — Owner — Due Date
SLO target/window: TBD — Owner — Due Date
Error-budget policy/current state: TBD — Owner — Due Date
Release health window/start/end: TBD — Owner — Due Date
```

Build the release-health and rollback matrix from the approved runbook/policy:

| Signal/check | Approved source/query | Baseline/criterion | Observation window | Triggered? | Action | Decision authority | Evidence |
|---|---|---|---|---|---|---|---|
| {health, SLI, smoke, dependency, migration, or support signal} | {REFERENCE/TBD} | {APPROVED_VALUE/TBD} | {APPROVED_WINDOW/TBD} | Yes / No / Unknown | Continue / Hold / Roll back / Escalate | {AUTHORITY/TBD} | {REFERENCE} |

Unknown mandatory criterion, telemetry blindness, missing authority, or expired health window blocks verification. Keep `deployed_not_verified` throughout the approved health window and record timestamped checks; do not shorten the window or invent rollback triggers.

If a rollback trigger occurs, follow the authorized rollback procedure. Never improvise destructive recovery. If rollback fails, activate incident escalation and record actual degraded state.

Completion criterion: final state is evidenced as `verified`, `failed`, `rolled_back`, or `aborted`, with incident/open-action ownership and release marker.

### Step 9 — Report and Preserve Evidence

Return scope/environment; stage/state/evidence table; SHA/build/digest; SonarQube/Trivy; gate/authority; commands and exits; deployment/verification/rollback; blockers/risks/TBDs; next authorized action and owner.

Store evidence only in approved versioned/immutable locations. Redact sensitive values.

Completion criterion: every claim has evidence or is explicitly `not_run/unknown`; no secret or inferred approval appears.

## Command Discipline

Before a command, record:

```text
Purpose:
Target:
Mutates state: yes/no
Expected effect:
Reversibility:
Authorization reference (if required):
```

After it runs, record:

```text
Timestamp:
Actor/build:
Repository/ref/SHA:
Environment/target:
Command/stage:
Exit status:
Evidence location:
Result: passed | failed | blocked | not_run | waived
```

A proposed command is `NOT RUN`. Never fabricate output or substitute expected results.

## Secret Safety

- Never request, print, persist, or repeat raw secrets or a discovered secret in output.
- Never persist secrets in Git, prompts, knowledge/vector stores, tickets, reports, Compose files, Jenkinsfiles, images, logs, or shell history.
- Use scoped Jenkins credential IDs or approved secret references.
- Redact sensitive headers, URLs, payloads, infrastructure addresses, and tenant data as classified.
- Suspected exposure triggers revocation/rotation and incident handling by authorized owners; deleting visible text is insufficient.

## Fail-Closed Rules

Hard stops include unknown/mismatched digest or target; missing/expired production authorization; failed mandatory check; missing/stale/mismatched scanner evidence; unresolved policy-blocking finding or undefined required severity policy without a valid policy-permitted waiver; missing rollback for a protected change; telemetry blindness; or requested scope exceeding authority.

No `--no-gates`, auto-approval, self-approval, proxy approval, inferred approval, or silent bypass is valid for DevOps-governed production work. Do not install or invoke a generic permissive orchestrator in the isolated `devops-engineer` profile.

## Common Pitfalls

1. Treating a green Jenkins job as production authorization.
2. Rebuilding per environment instead of promoting one digest.
3. Linking a mutable dashboard or “latest” report as sole evidence.
4. Running SonarQube/Trivy outside Jenkins and losing run correlation.
5. Calling configured test execution a QA verdict.
6. Guessing severity thresholds, RTO/RPO, capacity, or observation periods.
7. Logging credential values while trying to prove connectivity.
8. Continuing after a target/digest mismatch.
9. Calling `deployed` success before operational verification.
10. Leaving a legacy permissive skill available in the strict profile.

## Verification Checklist

- [ ] Correct EKSAD role and knowledge sources loaded
- [ ] Role boundary and target scope explicit
- [ ] Full SHA, Jenkins build, and artifact digest linked
- [ ] SonarQube/Trivy results match exact source/artifact
- [ ] Mandatory unavailable controls fail closed
- [ ] Environment readiness evidence is current
- [ ] No raw secret appears
- [ ] Production authorization envelope complete and current
- [ ] Same verified digest is promoted
- [ ] Configured SBOM/provenance/signature evidence matches SHA/build/digest
- [ ] SLI/SLO/error-budget values come from approved policy or remain TBD
- [ ] Release-health window and rollback matrix cite approved criteria/authority
- [ ] Rollback and observability are ready
- [ ] Execution evidence is real and attributable
- [ ] `deployed_not_verified` used until checks pass
- [ ] Waivers remain distinct, scoped, authorized, and time-bound
- [ ] Final report lists blockers, owners, due dates, and next authority
