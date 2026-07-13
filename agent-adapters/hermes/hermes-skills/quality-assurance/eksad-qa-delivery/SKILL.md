---
name: eksad-qa-delivery
description: Use when EKSAD QA work requires Mode A black-box test design, preparation of a read-only Mode B handoff manifest for the in-IDE QA agent, ingestion of externally produced execution evidence, or an evidence-based QA assessment. Produces no test code and keeps QA verdicts distinct from DevOps release readiness.
version: 1.1.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, qa, testing, rtm, test-plan, acceptance, evidence]
    related_skills: [eksad-code-review, eksad-devops-delivery]
---

# EKSAD QA Delivery

## Overview

This Hermes skill has four permitted activities:

1. **Mode A — Design / Docs (canonical Hermes profile):** derive and baseline an immutable Test Plan/RTM, Test Case Matrix, State Machine Matrix, risk coverage, test data, and execution/evidence plan from the approved/current FSD.
2. **Mode B — Handoff preparation only:** prepare a read-only automation manifest for the `vibe-coding/qa` in-IDE agent. Hermes does not write or modify REST Assured, Playwright, k6, security, fixture, helper, or other test code.
3. **Evidence ingestion:** verify and catalogue externally produced execution evidence in a separate project evidence artifact; never rewrite the baselined plan with run data.
4. **QA evidence assessment:** apply the project's named QA policy and record its defined QA verdict fields and allowed values in a separate assessment artifact.

QA owns black-box quality design and evidence assessment. The in-IDE QA agent owns Mode B test-code authoring; execution systems produce execution evidence. QA does not own developer white-box tests, production implementation, architecture, deployment, business acceptance, risk acceptance, DevOps release readiness, or release authorization.

## When to Use

- Create, review, or baseline an EKSAD Test Plan and RTM.
- Derive complete black-box tests from an FSD.
- Prepare a Mode B handoff manifest from a baselined plan and approved/current TSD.
- Ingest externally produced evidence without modifying the baseline design.
- Assess evidence using QA verdict fields and values defined by a named project policy.

Do not use this skill to write or edit test code, test helpers, fixtures, or test configuration; edit application code; decide requirements or architecture; conduct technical code approval; deploy; approve UAT; accept residual risk; determine DevOps release readiness; or authorize release.

## Required Knowledge and Inputs

Resolve `<EKSAD_PACK_ROOT>` in this order:

1. `EKSAD_PACK_SRC` when set and valid.
2. The active shared EKSAD knowledge deployment.
3. `~/.hermes/knowledge/eksad`.

Read as applicable:

- `<EKSAD_PACK_ROOT>/role-system-instructions/qa-engineer.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_TESTING_GUIDE.md`
- applicable frontend, load, auth, multi-tenancy, reserved-field, resilience, observability, event, and cache-sync standards
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md`
- exact FSD and, for Mode B handoff, exact TSD plus the baselined `TESTPLAN_{MODULE_CODE}_v{VERSION}.md`
- named project QA policy, when formal plan approval or a QA verdict is requested
- actual environment, candidate identity, reports, defect records, and authority decisions when ingesting or assessing evidence

Mode A's behavioral source is the FSD. Mode B handoff uses the TSD and may name production paths for read-only inspection by the in-IDE agent only to wire approved behavior to technical contracts. Never derive a new business expectation from implementation behavior.

## Role Boundary

| Area | Accountable owner | QA action |
|---|---|---|
| UR/BRD/FSD behavior | BA / Business Owner | Derive tests; report requirement gaps |
| TSD, Stack Profile, technical contracts | SA / Design Authority | Consume for Mode B handoff; report mismatch |
| Production implementation | Developers / Engineering Lead | Read only; report defects, never fix |
| Unit/internal integration tests | Developers | Use reports as supporting evidence; do not own or rewrite |
| Black-box acceptance/E2E/non-functional design | QA / QA Lead | Design and baseline |
| Black-box automation implementation | `vibe-coding/qa` in-IDE agent under QA ownership | Supply read-only handoff manifest; write no code in Hermes |
| Pipeline/environment/deployment and release readiness | DevOps | Request/consume attributable evidence; do not reuse DevOps readiness vocabulary as QA verdicts |
| UAT/business acceptance | Business Owner | Provide QA evidence; never impersonate acceptance |
| Residual-risk acceptance | Named Risk/Business Authority | Record decision; never self-waive |
| Release authorization | Named Release Authority | Supply policy-defined QA evidence input only |

## Stable IDs and Design States

Preserve source IDs (`UR-*`, `BR-*`, `F-*`, `FR-*`, `NFR-*`, `US-*`, acceptance criteria, validation/error/state references). Use stable QA IDs:

- test cases: `TC-NNN`;
- performance cases: `PERF-NNN` when a separate series is useful;
- defects: the project's defect ID, never a fabricated tracker identity;
- evidence: the external/project ID, or `EVD-{MODULE}-{NNN}` only inside the separate evidence artifact when no external ID exists.

The baselined design records each planned test as `NOT_RUN`; this means no execution claim was made at design time. Do not mutate that marker after execution. Actual execution status (`PASSED`, `FAILED`, `BLOCKED`, `SKIPPED`, or `NOT_RUN`) belongs to separate evidence artifacts.

RTM coverage is `COVERED`, `PARTIAL`, `GAP`, or `BLOCKED`. Coverage means a test is designed; it never implies execution success or a QA verdict.

## Mode and Activity Selection

| Activity | Required input | Allowed output |
|---|---|---|
| Mode A — Design / Docs | Approved/current FSD and project scope | Versioned immutable Test Plan/RTM baseline and design matrices/plans |
| Mode B — Handoff preparation | TSD + baselined Mode A plan/RTM; repository/ref and approved path scope | Read-only manifest naming test IDs, intended files, tool/layer, contracts, fixtures, and CI evidence request; no code writes |
| Evidence ingestion | External evidence + exact candidate identity | Separate project evidence record/reference; no Test Plan/RTM mutation |
| QA evidence assessment | Named project QA policy + verified evidence | Separate assessment using exactly the policy-defined QA verdict fields and allowed values |

Finish and baseline Mode A before preparing Mode B handoff. **Formal plan approval is required only when a named project policy requires it.** Record that policy's exact title, version, path/URL, and approval evidence. If no such policy is identified, record review/baseline evidence and do not invent an approval gate.

## Mode A Workflow — Design / Docs

### A1 — Establish Scope and Sources

Record project/module, FSD path/version/status, requirements, exclusions, change baseline, stakeholders, environment assumptions, planned levels, and evidence destination. Inspect traceability, FRs/acceptance criteria, flows, validations, state machines, roles, API catalog, business rules, NFRs, errors, reserved fields, gaps, and decisions.

Completion: every source is named/versioned; missing or contradictory behavior is a gap, not an invented expected result.

### A2 — Build the RTM First

Create one row for every in-scope testable source requirement and preserve exact IDs/sections.

| Requirement ID | Source reference | Requirement summary | Type / risk | Test case IDs | Coverage | Gap / blocker |
|---|---|---|---|---|---|---|
| `{FR-ID}` | `{FSD §}` | `{SUMMARY}` | functional | `TC-NNN` | `COVERED` | — |

Include separately testable acceptance criteria, rules, validations, transitions, endpoint/auth behavior, errors, and NFRs. Any row without an adequate test is `GAP` or `BLOCKED`, with owner and due date. No test may be orphaned from source requirements.

### A3 — Derive the Full Test Matrix

Use the canonical eight columns:

| TC ID | Description | Precondition | Steps | Input | Expected Result | Priority | Status |
|---|---|---|---|---|---|---|---|

Cover main, alternative, and exception paths; every acceptance criterion and validation boundary; all valid/invalid/terminal transitions; endpoint success and auth/role/tenant abuse cases; documented errors; applicable soft-delete, audit, reserved-field, integration, event, resilience, observability, cache-sync, security, and NFR behavior.

Expected results must be observable and source-backed. At baseline every design row is `NOT_RUN`; later execution does not alter this matrix.

### A4 — Build Supporting Matrices and Test Data

For each workflow, enumerate every required `(from state, action)` pair and map it to test ID, expected state/error, actor, and source. For APIs, map success, authentication, authorization, tenant isolation, validation, errors, soft delete, and writes/audit.

Define tenant A/B identities, actors/roles, pre-existing states, boundary/invalid data, dependencies/events/files/configurations, cleanup/reset, and masking/classification. Never use production credentials or uncontrolled production data.

### A5 — Apply Risk-Based Coverage

Risk prioritization orders work; it does not erase mandatory coverage. Map source-backed failure modes and material risks to requirements/tests/layers. Do not invent likelihood, impact, load thresholds, recovery objectives, regulatory duties, defect thresholds, coverage percentages, or waiver authority. Use `TBD` with owner and due date.

### A6 — Define Entry, Exit, Suspension, and Evidence Requirements

Entry criteria cite real baselines, candidate/environment/data/access/dependencies, and suite prerequisites. Exit and pass/fail criteria must cite approved EKSAD sources or named project policy. Preserve documented P1/P2 rules without inventing extra thresholds.

The evidence plan requires exact SHA/build/artifact/environment, suite/test version, timestamps, executor/job, command/stage/tool version, result/exit status, immutable report location, defect/rerun linkage, and redaction. These are required fields for a **separate execution evidence artifact**, not mutable sections of the plan.

### A7 — Review, Baseline, and Handoff

Validate traceability, matrices, risk mapping, feasibility, gaps, and output path. Record Mode B priorities and intended test-only files in the read-only handoff manifest. If a named project policy requires formal approval, record its required evidence; otherwise do not claim approval is mandatory.

Baseline with a version and immutable reference. After baseline, corrections or scope changes create a new plan version; execution, rerun, defect, and QA verdict data go to separate project artifacts. Mode A completion does not mean tests executed or QA passed.

## Mode B Workflow — Handoff Preparation Only

### B1 — Verify Baseline and Scope

Verify aligned FSD/TSD/plan versions, declared Stack Profile/contracts, repository/ref, stable test IDs, and intended test-only paths. Default paths from the EKSAD Testing Guide are `src/test/**`, `e2e/**`, `perf/**`, and `security/**`; these are proposed writable paths for the in-IDE agent, not Hermes. Production code and migrations remain read-only.

### B2 — Inspect Contracts Read-Only

Read the TSD, plan, repository conventions, schemas, and endpoint/DTO/config code needed to describe wiring. A conflict becomes a design/QA gap; implementation behavior never replaces the FSD expectation.

### B3 — Publish the Read-Only Manifest

For each intended file list action, layer/tool, requirement IDs, TC IDs, helpers/fixtures, read-only production references, variables by name, CI outputs, evidence destination, and exclusions. Name `vibe-coding/qa` as implementation owner. Record a formal gate only when a named project policy requires it.

### B4 — Validate and Transfer

Statically inspect only manifest IDs, intended paths, source mappings, variables, evidence destinations, and exclusions. Do not create, modify, or review implementation-level test code as part of this skill. Do not run or install Maven, Gradle, npm, pnpm, yarn, application runtimes, browsers, k6, containers, or test suites on this VPS.

Transfer the manifest and immutable plan reference to `vibe-coding/qa`. All tests remain `NOT_RUN` in the design baseline; execution statuses live only in external evidence artifacts.

## Evidence Ingestion

Verify source SHA/build/artifact, environment, suite/version, TC IDs, timestamps, executor/job, tool/version, result/exit status, immutable report location, and integrity/provenance. Catalogue accepted and rejected evidence in a **separate project evidence artifact selected by project convention** and link the immutable Test Plan/RTM baseline. Do not create an extra generic template.

Preserve every run and rerun as separate evidence. Link project defect IDs without fabricating tracker identities. Classify non-passes as product defect, test defect, environment issue, data issue, or requirement/design gap, with owner and source/evidence links. Never weaken an expected result or mutate the plan's design marker.

## QA Evidence Assessment and Verdict Boundary

First locate a **named project QA policy**. Record its title, version, path/URL, effective scope, QA verdict field names, allowed values, decision rules, and authority. Copy those names and values exactly. If any are undefined, use `TBD — Owner: <named policy owner> — Due: <date or explicit TBD>` and state that no QA verdict can be issued. **Do not create fallback readiness states.**

Keep distinct:

- design coverage;
- execution evidence/result;
- defect disposition;
- policy-defined QA verdict;
- DevOps release readiness;
- business/UAT acceptance, risk acceptance, and release authorization.

QA must not borrow DevOps `READY`, `NOT_READY`, or `BLOCKED` labels. Such a string may appear as a QA verdict only if the named QA policy explicitly defines that exact QA field/value; even then, label it as QA policy output and explicitly state that it is not the DevOps readiness determination.

A separate QA assessment artifact must contain at least:

| Field | Required value |
|---|---|
| Candidate | full SHA/build/artifact digest/version/environment |
| Scope | FSD/TSD/Test Plan versions and included/excluded suites |
| Evidence | immutable evidence artifact references and cut-off |
| RTM design | covered/partial/gap/blocked counts from immutable baseline |
| Execution | result counts and evidence references |
| P1/P2, defects, risks/exceptions | evidence and named decision references |
| QA policy | exact title/version/path or URL |
| QA verdict fields | exact policy-defined field name(s) |
| QA verdict values | exact policy-defined value(s), or `TBD` when undefined |
| Rationale | evidence references and policy rule only |
| QA owner/date | attributable issuer and cut-off |
| DevOps boundary | explicit statement that this is not DevOps release readiness |
| Next authority | policy-defined recipient |

A waiver remains a waiver; it does not convert a failed test to passed. Do not use percentages unless the denominator, formula, and source are reproducible.

## Hard Stops

Stop and report a blocker when:

- FSD lacks an expected behavior required for a test;
- FSD/TSD/code versions conflict;
- Mode B lacks a baselined plan, stable IDs, repository/ref, or path scope;
- formal approval is requested but no named project policy establishes it;
- requested writes include test code, helpers/config, production code, or developer-owned tests;
- candidate identity or evidence provenance cannot be proven;
- evidence is stale, incomplete, contradictory, mutable without provenance, or mismatched;
- no named project policy defines the requested QA verdict fields/values;
- a secret or sensitive production datum is exposed;
- the user asks QA to accept risk, approve UAT, determine DevOps release readiness, authorize release, or deploy;
- verification would require build/test/runtime execution on this VPS.

## Verification Checklist

- [ ] Activity is Mode A, Mode B handoff, evidence ingestion, or QA assessment
- [ ] Exact sources and versions are recorded
- [ ] Mode A design is versioned/baselined and immutable
- [ ] Formal approval gate cites a named project policy, or is not imposed
- [ ] Every in-scope requirement maps to test ID(s), and every test maps to source
- [ ] Eight-column tests and supporting matrices are complete and source-backed
- [ ] Baseline test rows remain `NOT_RUN`; execution status is separate
- [ ] Mode B output is a read-only manifest for `vibe-coding/qa`
- [ ] Hermes wrote no test code, helper, fixture, or test configuration
- [ ] Production code remained read-only
- [ ] External evidence matches the exact candidate and preserves run/rerun history
- [ ] Defects use project IDs and live outside the immutable plan
- [ ] QA verdict names/values come from a named project QA policy
- [ ] QA verdict is explicitly distinct from DevOps release readiness
- [ ] No build/runtime/test execution occurred on this VPS
- [ ] No commit or push unless explicitly authorized
