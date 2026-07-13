# EKSAD Test Plan and Requirements Traceability Matrix
# {PROJECT_NAME} — {MODULE_NAME} — Version {VERSION}

> Filename: `TESTPLAN_{MODULE_CODE}_v{VERSION}.md`

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — {MODULE_NAME} Test Plan and RTM |
| **Document Type** | QA Test Plan and Requirements Traceability Matrix |
| **Project / Service** | {PROJECT_NAME} / {SERVICE_NAME_OR_TBD} |
| **Project Code** | `{PROJECT_CODE}` |
| **Module** | `{MODULE_CODE}` — {MODULE_NAME} |
| **Version** | {VERSION} |
| **Status** | Draft / In Review / Baselined / Superseded *(pick one)* |
| **QA Mode** | Mode A — Design / Docs |
| **FSD Baseline** | `{FSD_PATH}` — v{FSD_VERSION}, {FSD_STATUS} |
| **TSD Baseline** | `{TSD_PATH_OR_NOT_APPLICABLE}` — v{TSD_VERSION_OR_NA} *(required for Mode B handoff)* |
| **Baseline Reference** | {IMMUTABLE_TAG_COMMIT_DOCUMENT_REFERENCE_OR_TBD} |
| **Prepared By** | {QA_AUTHOR} |
| **Reviewed By** | {QA_REVIEWER} |
| **Formal Approval Policy** | {POLICY_TITLE_VERSION_PATH_OR_URL_OR_NOT_REQUIRED} |
| **Approved By** | {PLAN_APPROVER_OR_NOT_REQUIRED_BY_NAMED_POLICY} |
| **Classification** | {CLASSIFICATION} |
| **Last Updated** | {DATE} |

> **Purpose and boundary:** This is an immutable/baselined Mode A black-box design artifact plus a read-only Mode B handoff manifest for the `vibe-coding/qa` in-IDE agent. It contains no execution runs, reruns, defects, mutable results, QA verdict, DevOps readiness determination, or final release decision.
>
> **Baseline rule:** Before baseline, revise this document through normal review. At baseline, assign a version and immutable reference. After baseline, do not update it with execution or defect data; a design/scope correction creates a new version. Every planned test remains `NOT_RUN` here permanently because execution status belongs to separate project evidence artifacts.
>
> **Approval rule:** Formal plan approval is required only when the named project policy in Document Control requires it. If no such policy applies, use `Not required — no named project policy` and record review/baseline evidence without inventing an approval gate.

---

## Revision History

| Version | Date | Author | Change Summary | FSD / Decision Reference |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial Mode A draft | {REFERENCE} |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGE} | {REFERENCE} |

---

## Review, Baseline, and Conditional Plan Approval

| Role | Name | Decision | Scope / Evidence Reference | Date |
|---|---|---|---|---|
| QA Lead / Reviewer | {NAME} | Reviewed / Revise | {REFERENCE} | {DATE} |
| Business Analyst / FSD Owner | {NAME} | Confirm behavior baseline / Revise | {REFERENCE} | {DATE} |
| System Analyst / TSD Owner *(Mode B readiness only)* | {NAME_OR_NA} | Confirm technical baseline / Revise / N/A | {REFERENCE_OR_NA} | {DATE_OR_NA} |
| Policy-named Plan Approver *(only if required)* | {NAME_OR_NA} | Approve / Revise / Not Required | {POLICY_AND_EVIDENCE_OR_NA} | {DATE_OR_NA} |

> Reviewer silence is not evidence. Unresolved blocking design gaps prevent baselining. Formal approval blocks baseline/handoff only when the identified project policy says so.

---

## Table of Contents

1. [Purpose and Objectives](#1-purpose-and-objectives)
2. [Source Baseline and Change Scope](#2-source-baseline-and-change-scope)
3. [Scope](#3-scope)
4. [Requirements Traceability Matrix](#4-requirements-traceability-matrix)
5. [Test Strategy and Ownership](#5-test-strategy-and-ownership)
6. [Risk-Based Coverage](#6-risk-based-coverage)
7. [Test Environment and Dependencies](#7-test-environment-and-dependencies)
8. [Test Data and Isolation](#8-test-data-and-isolation)
9. [Entry, Exit, Suspension, and Resumption Criteria](#9-entry-exit-suspension-and-resumption-criteria)
10. [Test Case Matrix](#10-test-case-matrix)
11. [State Machine Coverage](#11-state-machine-coverage)
12. [Endpoint, Auth, and Tenant Coverage](#12-endpoint-auth-and-tenant-coverage)
13. [Cross-Cutting and Non-Functional Coverage](#13-cross-cutting-and-non-functional-coverage)
14. [Mode B Automation Handoff](#14-mode-b-automation-handoff)
15. [Gaps, Assumptions, and Design Decisions](#15-gaps-assumptions-and-design-decisions)
16. [Separate Evidence and QA Assessment References](#16-separate-evidence-and-qa-assessment-references)
17. [Baseline Completion Checklist](#17-baseline-completion-checklist)

---

## 1. Purpose and Objectives

### 1.1 Purpose

{PURPOSE}

### 1.2 Quality Objectives

| Objective ID | Source Requirement / Risk | Observable Objective | Planned Test IDs | Success Basis |
|---|---|---|---|---|
| QO-001 | {FSD_OR_RISK_REFERENCE} | {OBSERVABLE_OBJECTIVE} | TC-001 | {SOURCE_BACKED_EXPECTATION} |

### 1.3 Intended Audience

| Audience | Use of This Artifact |
|---|---|
| QA / QA Lead | Review and baseline design; prepare handoff; ingest and assess evidence in separate artifacts |
| BA / FSD Owner | Resolve missing or contradictory expected behavior |
| SA / Design Authority | Supply Mode B endpoint, event, stack-profile, and environment design |
| Developers / Technical Leader | Consume defect and regression scope; production code remains outside QA write scope |
| `vibe-coding/qa` in-IDE agent | Consume the read-only Mode B manifest and implement automation outside Hermes |
| DevOps / PM / Release Authority | Consume separate attributable QA evidence/assessment; DevOps readiness and release authorization stay separate |

---

## 2. Source Baseline and Change Scope

### 2.1 Source Register

| Source ID | Artifact | Exact Path / Location | Version / Ref | Status | Owner | Purpose |
|---|---|---|---|---|---|---|
| SRC-001 | FSD | `{FSD_PATH}` | v{FSD_VERSION} | {STATUS} | {OWNER} | Mode A behavioral source |
| SRC-002 | BRD / UR *(context only)* | `{PATH_OR_NA}` | {VERSION_OR_NA} | {STATUS_OR_NA} | {OWNER_OR_NA} | Upstream traceability |
| SRC-003 | TSD *(Mode B only)* | `{TSD_PATH_OR_NA}` | v{TSD_VERSION_OR_NA} | {STATUS_OR_NA} | {OWNER_OR_NA} | Technical wiring, not new expected behavior |
| SRC-004 | Prior plan / defect / change | `{REFERENCE_OR_NA}` | {VERSION_OR_NA} | {STATUS_OR_NA} | {OWNER_OR_NA} | Regression/change context |

### 2.2 Baseline Alignment

| Check | Result | Evidence / Action |
|---|---|---|
| FSD is approved/current for the requested scope | Yes / No / Blocked | {REFERENCE_OR_OWNER_ACTION} |
| FSD IDs and section references are stable | Yes / No / Blocked | {REFERENCE_OR_OWNER_ACTION} |
| TSD matches the FSD baseline *(Mode B only)* | Yes / No / N/A / Blocked | {REFERENCE_OR_OWNER_ACTION} |
| Repository/ref is known *(Mode B handoff only)* | Yes / No / N/A / Blocked | {REFERENCE_OR_OWNER_ACTION} |
| Prior tests/defects affected by this change are identified | Yes / No / N/A / Blocked | {REFERENCE_OR_OWNER_ACTION} |

### 2.3 Change Baseline

| Change ID / Ref | Changed FSD Section / Requirement | Prior Baseline | Current Baseline | Test Impact | Regression IDs |
|---|---|---|---|---|---|
| {CHANGE_ID} | {REFERENCE} | {OLD_VERSION_OR_VALUE} | {NEW_VERSION_OR_VALUE} | Add / Update / Retire / Review | {TC_IDS_OR_TBD} |

---

## 3. Scope

### 3.1 In Scope

| Scope ID | Capability / Requirement Range | Test Level | Planned Suite / Artifact | Source |
|---|---|---|---|---|
| TSCP-001 | {CAPABILITY_OR_ID_RANGE} | API / Acceptance / Cross-service E2E / FE E2E / Non-functional | {SUITE_OR_PLAN} | {FSD_REFERENCE} |

### 3.2 Out of Scope

| Exclusion ID | Excluded Item | Reason / Approved Boundary | Owner / Approval Evidence | Future Reference |
|---|---|---|---|---|
| TEX-001 | {EXCLUSION} | {SOURCE_BACKED_REASON} | {OWNER_AND_REFERENCE} | {REFERENCE_OR_NONE} |

> Do not move an in-scope uncovered requirement to this table to hide a gap. It remains `GAP` or `BLOCKED` in the RTM unless the named scope authority approves the exclusion.

### 3.3 QA Deliverables

- [ ] RTM with one row per in-scope testable source requirement
- [ ] Canonical eight-column Test Case Matrix
- [ ] State Machine Matrix for every in-scope workflow
- [ ] Endpoint/auth/tenant matrix where APIs are in scope
- [ ] Risk, environment, test-data, entry/exit, and evidence plans
- [ ] Mode B automation handoff where automation is requested
- [ ] References/destinations for separate execution evidence and QA assessment artifacts

---

## 4. Requirements Traceability Matrix

> Build the RTM before or with the test cases. Preserve each original source ID and exact section reference. Include testable FRs, acceptance criteria, business rules, validations, state transitions, endpoint/auth behavior, error codes, and NFRs. One test may cover multiple requirements when its assertions genuinely verify each; do not duplicate equivalent tests merely to create one test per row.

### 4.1 RTM

| Requirement ID | Source Reference | Requirement Summary | Type / Risk | Test Case ID(s) | Coverage | Gap / Blocker |
|---|---|---|---|---|---|---|
| {FR_ID} | FSD §{SECTION} | {SUMMARY} | Functional | TC-001 | COVERED | — |
| {AC_OR_RULE_ID} | FSD §{SECTION} | {SUMMARY} | Acceptance / Business Rule | TC-002, TC-003 | COVERED | — |
| {NFR_ID} | FSD §{SECTION} | {SUMMARY_AND_SOURCE_TARGET} | Non-functional | PERF-001 | PARTIAL | {MISSING_COVERAGE_OWNER_DUE} |
| {SOURCE_ID} | FSD §{SECTION} | {SUMMARY} | {TYPE} | — | GAP / BLOCKED | {OWNER_AND_DUE} |

**Coverage states:**

- `COVERED` — one or more designed tests cover the requirement.
- `PARTIAL` — designed tests cover only part of the requirement; state the residual gap.
- `GAP` — no adequate test is designed.
- `BLOCKED` — coverage cannot be designed or completed because a named dependency or decision is unresolved.

Coverage is design status, not execution status.

### 4.2 Bidirectional Trace Check

| Test ID | Source Requirement ID(s) | FSD Reference | RTM Row Present? | Orphan / Action |
|---|---|---|---|---|
| TC-001 | {FR_ID}, {AC_ID} | FSD §{SECTION} | Yes / No | {NONE_OR_ACTION} |

### 4.3 RTM Summary

| Metric | Count | Reproducible Basis |
|---|---:|---|
| In-scope requirement rows | {COUNT} | RTM §4.1 |
| COVERED | {COUNT} | RTM §4.1 |
| PARTIAL | {COUNT} | RTM §4.1 |
| GAP | {COUNT} | RTM §4.1 |
| BLOCKED | {COUNT} | RTM §4.1 |
| Orphan test cases | {COUNT} | Bidirectional check §4.2 |

> If a percentage is reported, state its numerator, denominator, formula, and source rows. Do not treat excluded requirements as covered.

---

## 5. Test Strategy and Ownership

### 5.1 Planned Test Levels

| Test Level | QA Intent | Source | Owner | Planned Tool / Surface | Included IDs |
|---|---|---|---|---|---|
| API / Acceptance | Black-box requirement and abuse matrix | FSD | QA | REST Assured / approved API tooling | {TC_IDS} |
| Cross-service E2E | End-to-end business flow | FSD | QA | `e2e/**` / approved suite | {TC_IDS} |
| FE E2E | User journey and observable UI behavior | FSD | QA | Playwright when project-confirmed | {TC_IDS} |
| Load / Performance | Approved NFR behavior | FSD NFRs | QA | k6 / approved tool | {PERF_IDS} |
| Security | Approved auth/abuse/security scope | FSD and applicable standards | QA | `security/**` / approved tool | {TC_IDS} |
| Unit / Internal Integration | White-box implementation confidence | TSD/code | Developer | Developer-owned paths and reports | Not authored or owned by QA |

### 5.2 Derivation Method

For the approved scope, inspect and map:

- user stories, main/alternative/exception flows, and every acceptance criterion;
- business and global rules;
- field validations and source-defined boundaries;
- all valid and invalid state transitions, including terminal-state attempts;
- endpoint success, authentication, authorization, tenant-scope, validation, and documented errors;
- soft-delete behavior and write/audit acceptance behavior where applicable;
- reserved fields only for source-confirmed opted-in transactional entities;
- integrations, event behavior, resilience, observability, cache sync, and measurable NFRs only when applicable and sourced.

Expected results must identify observable status, response/error field, state/data effect, event/evidence, or UI outcome as applicable. If the FSD does not define the expected result, create a gap instead of copying behavior from code or inventing a value.

---

## 6. Risk-Based Coverage

> Risk prioritization orders work; it does not remove mandatory in-scope coverage. Do not invent likelihood, impact, performance thresholds, recovery objectives, or regulatory duties.

| Risk ID / Source | Failure Mode | Impact / Likelihood Source | Covered Requirement(s) | Test ID(s) | Layer | Residual Gap / Owner |
|---|---|---|---|---|---|---|
| {RISK_ID_OR_REFERENCE} | {FAILURE_MODE} | {SOURCE_VALUE_OR_TBD} | {REQ_IDS} | {TC_OR_PERF_IDS} | {LAYER} | {NONE_OR_OWNER_DUE} |

### 6.1 Priority Assignment

| Priority | EKSAD Meaning | Application in This Plan |
|---|---|---|
| P1 | Must pass before release | Assign only to source/risk-backed critical coverage |
| P2 | Should pass; failure requires an approved mitigation plan | Record mitigation authority and evidence; QA does not self-waive |
| P3 | Lower-priority coverage | Apply only when supported by project prioritization; retain result and limitation |

---

## 7. Test Environment and Dependencies

### 7.1 Environment

| Item | Required Value / Configuration | Owner | Prerequisite Evidence | Project-Defined Availability |
|---|---|---|---|---|
| Environment name | {ENVIRONMENT} | {OWNER} | {REFERENCE} | {PROJECT_DEFINED_AVAILABILITY_VALUE_OR_TBD} |
| API/UI endpoint | `{BASE_URL_VARIABLE_OR_APPROVED_ENDPOINT}` | {OWNER} | {REFERENCE} | {STATUS} |
| Candidate identity | {FULL_SHA_BUILD_ARTIFACT_DIGEST} | {OWNER} | {REFERENCE} | {STATUS_OR_NA} |
| Deployment identity | {DEPLOYMENT_JOB_AND_BUILD} | {OWNER} | {REFERENCE} | {STATUS_OR_NA} |
| Database / broker / dependencies | {APPROVED_TEST_DEPENDENCIES} | {OWNER} | {REFERENCE} | {STATUS} |
| Auth / test identities | {VARIABLE_NAMES_OR_IDENTITY_CLASSES} | {OWNER} | {REFERENCE} | {STATUS} |
| Observability / evidence access | {LOG_METRIC_TRACE_REPORT_ACCESS} | {OWNER} | {REFERENCE} | {STATUS} |

Do not hard-code credentials, tokens, tenant secrets, production URLs, or environment-specific endpoints in this artifact or automation. Never use uncontrolled production data.

### 7.2 Dependency Register

| Dependency ID | Dependency | Provider / Owner | Needed By | Acceptance / Evidence | Status / Blocker |
|---|---|---|---|---|---|
| TDEP-001 | {DEPENDENCY} | {OWNER} | {DATE_OR_MILESTONE} | {EVIDENCE} | {PROJECT_DEFINED_DEPENDENCY_VALUE_OR_TBD} |

---

## 8. Test Data and Isolation

### 8.1 Data Set Catalogue

| Data ID | Purpose / Related Tests | Tenant / Actor / Role | Initial State / Records | Boundary / Invalid Value | Sensitivity | Provisioning / Cleanup |
|---|---|---|---|---|---|---|
| TD-001 | {PURPOSE_AND_TC_IDS} | Tenant A / {ACTOR_ROLE} | {PRECONDITION} | {VALUE_OR_NA} | {CLASSIFICATION} | {METHOD} |
| TD-002 | Cross-tenant isolation | Tenant B / {ACTOR_ROLE} | {ISOLATED_RECORDS} | N/A | {CLASSIFICATION} | {METHOD} |

### 8.2 Isolation and Reset Rules

- Each independent test provisions or identifies its own data and leaves no dependency on test order.
- Tenant A and Tenant B identities and records are distinct and attributable.
- Cleanup/reset preserves evidence and does not operate on uncontrolled production data.
- Files, events, reserved-field configurations, and external dependency fixtures are versioned or reproducible when in scope.
- Sensitive values are masked or redacted in reports, screenshots, logs, and traces.

---

## 9. Entry, Exit, Suspension, and Resumption Criteria

### 9.1 Entry Criteria

| Criterion | Required Evidence | Owner | State |
|---|---|---|---|
| FSD baseline is approved/current and traceable | {REFERENCE} | {OWNER} | Met / Not Met / Blocked |
| TSD and technical contracts align *(Mode B/execution)* | {REFERENCE_OR_NA} | {OWNER_OR_NA} | Met / N/A / Blocked |
| Exact candidate and environment are identifiable *(execution)* | {REFERENCE_OR_NA} | {OWNER_OR_NA} | Met / N/A / Blocked |
| Approved suite, data, access, and dependencies are ready | {REFERENCE} | {OWNER} | Met / Not Met / Blocked |
| Blocking requirement/test-design gaps are resolved | {REFERENCE} | {OWNER} | Met / Not Met / Blocked |

### 9.2 Exit Criteria

| Criterion | Source / Policy | Evidence Required | State |
|---|---|---|---|
| All applicable planned tests have attributable disposition | {POLICY_REFERENCE} | {EXECUTION_REPORT} | Met / Not Met / Blocked |
| P1 tests pass | EKSAD Testing Guide / {PROJECT_POLICY} | {EVIDENCE} | Met / Not Met / Blocked |
| P2 failures have an approved mitigation plan | EKSAD Testing Guide / {PROJECT_POLICY} | {NAMED_DECISION_REFERENCE} | Met / Not Met / Blocked |
| Defect and residual-risk conditions satisfy approved policy | {POLICY_OR_TBD_OWNER} | {EVIDENCE} | Met / Not Met / Blocked |
| RTM gaps/blockers are resolved or have named disposition | {POLICY_REFERENCE} | {EVIDENCE} | Met / Not Met / Blocked |

Do not add defect-count limits, coverage percentages, performance thresholds, or waiver authority unless an approved source supplies them.

### 9.3 Suspension and Resumption

| Condition | Suspend When | Resume When / Required Evidence | Decision Owner |
|---|---|---|---|
| Environment instability | {OBJECTIVE_CONDITION} | {READINESS_EVIDENCE} | {OWNER} |
| Candidate mismatch | SHA/build/artifact/environment differs from the approved target | Identity is reconciled and evidenced | {OWNER} |
| Dependency or test-data failure | {OBJECTIVE_CONDITION} | {RECOVERY_EVIDENCE} | {OWNER} |
| Security or sensitive-data exposure | {OBJECTIVE_CONDITION} | Exposure is contained and authorized to resume | {OWNER} |
| Invalid/stale evidence | {OBJECTIVE_CONDITION} | New attributable evidence is available | {OWNER} |

---

## 10. Test Case Matrix

> Use stable IDs: `TC-NNN`; use `PERF-NNN` for a separate performance series when useful. Every row must contain all eight canonical columns and trace to at least one RTM requirement. Status is permanently `NOT_RUN` in this immutable design artifact; actual results live in separate evidence artifacts.

| TC ID | Description | Precondition | Steps | Input | Expected Result | Priority | Status |
|---|---|---|---|---|---|---|---|
| TC-001 | {DESCRIPTION} | {PRECONDITION} | 1. {STEP_ONE}<br>2. {STEP_TWO} | {INPUT_OR_DATA_ID} | {EXACT_OBSERVABLE_RESULT_FROM_FSD} | P1 / P2 / P3 | NOT_RUN |
| TC-002 | {NEGATIVE_OR_BOUNDARY_DESCRIPTION} | {PRECONDITION} | 1. {STEP_ONE}<br>2. {STEP_TWO} | {INPUT_OR_DATA_ID} | {STATUS_ERROR_STATE_OR_EFFECT} | {PRIORITY} | NOT_RUN |

**Design marker:** `NOT_RUN` means this baseline makes no execution claim. Never replace it with an execution result in this document.

### 10.1 Test-to-Source Detail

| TC ID | Requirement ID(s) | FSD Reference | Test Layer | Automation Intent | Evidence Target |
|---|---|---|---|---|---|
| TC-001 | {REQ_IDS} | FSD §{SECTION} | API / E2E / FE E2E / Security | Manual / Automate / TBD | {REPORT_LOG_TRACE_SCREENSHOT} |

---

## 11. State Machine Coverage

> Repeat for each in-scope workflow. Enumerate every FSD-required `(from state, action)` pair, including valid, invalid, and terminal-state attempts. Expected states/errors must come from the FSD.

### 11.1 Workflow: {WORKFLOW_NAME}

| From State | Action | Actor / Role | Valid? | Expected State / Error | Source Rule | Test ID | Coverage |
|---|---|---|---|---|---|---|---|
| {FROM_STATE} | {ACTION} | {ACTOR_ROLE} | Yes | {TO_STATE} | {FSD_REFERENCE} | TC-{NNN} | COVERED |
| {FROM_STATE} | {ACTION} | {ACTOR_ROLE} | No | {SOURCE_DEFINED_ERROR} | {FSD_REFERENCE} | TC-{NNN} | COVERED |

### 11.2 State Coverage Check

| State / Transition Group | Valid Cases Complete? | Invalid Cases Complete? | Terminal Attempts Complete? | Gap / Owner |
|---|---|---|---|---|
| {STATE_OR_GROUP} | Yes / No / N/A | Yes / No / N/A | Yes / No / N/A | {NONE_OR_OWNER_DUE} |

---

## 12. Endpoint, Auth, and Tenant Coverage

> Repeat per endpoint. Apply only source/applicable-standard-backed results. For example, cross-tenant item access and cross-tenant list filtering may have different expected responses; do not assume one response for every operation.

| Endpoint / Operation | Success | No Token | Expired Token | Invalid Signature | Wrong Role | Wrong Tenant / Scope | Validation / Errors | Soft Delete | Write / Audit | Test IDs |
|---|---|---|---|---|---|---|---|---|---|---|
| `{METHOD} {PATH}` | {EXPECTED} | {EXPECTED} | {EXPECTED} | {EXPECTED} | {EXPECTED} | {SOURCE_DEFINED_EXPECTED} | {ERROR_IDS} | {EXPECTED_OR_NA} | {EXPECTED_OR_NA} | {TC_IDS} |

### 12.1 Tenant and Hierarchy Scenarios

| Scenario | Source Scope Rule | Expected Observable Result | Test ID | Data IDs |
|---|---|---|---|---|
| Tenant A attempts Tenant B item access | {FSD_OR_STANDARD_REFERENCE} | {SOURCE_DEFINED_RESULT} | TC-{NNN} | TD-001, TD-002 |
| Tenant B lists records after Tenant A creates data | {FSD_OR_STANDARD_REFERENCE} | {SOURCE_DEFINED_FILTER_RESULT} | TC-{NNN} | TD-001, TD-002 |
| {APPROVED_HIERARCHY_ROLE_SCENARIO} | {REFERENCE} | {EXPECTED_RESULT} | TC-{NNN} | {DATA_IDS} |

---

## 13. Cross-Cutting and Non-Functional Coverage

Use only rows applicable to the approved scope; mark others `N/A` with a reason rather than fabricating tests or targets.

| Concern | Source Requirement / Standard | Scenario / Assertion | Test ID(s) | Target / Expected Result | Status / Gap |
|---|---|---|---|---|---|
| Soft delete | {REFERENCE} | Deleted item list/read behavior | {TC_IDS} | {EXPECTED} | {STATUS} |
| Audit acceptance | {REFERENCE} | Write produces attributable audit evidence | {TC_IDS} | {EXPECTED_FIELDS_OR_EVENT} | {STATUS} |
| Reserved fields | {OPT_IN_REFERENCE_OR_NA} | Tenant schema/validation/persistence behavior | {TC_IDS} | {EXPECTED_OR_NA} | {STATUS} |
| Integration / event | {REFERENCE_OR_NA} | Contract, idempotency, ordering, retry/dead-letter behavior | {TC_IDS} | {EXPECTED_OR_NA} | {STATUS} |
| Cache sync | {REFERENCE_OR_NA} | Fresh/stale/delete/startup behavior | {TC_IDS} | {EXPECTED_OR_NA} | {STATUS} |
| Resilience | {REFERENCE_OR_NA} | Timeout/retry/circuit/fallback/health | {TC_IDS} | {SOURCE_TARGET_OR_TBD} | {STATUS} |
| Observability | {REFERENCE_OR_NA} | Correlation/log/metric/trace behavior | {TC_IDS} | {EXPECTED_OR_NA} | {STATUS} |
| Performance / load | {NFR_REFERENCE_OR_NA} | {WORKLOAD_MODEL} | {PERF_IDS} | {SOURCE_THRESHOLD_OR_TBD} | {STATUS} |
| Security | {REFERENCE_OR_NA} | {APPROVED_SECURITY_SCENARIO} | {TC_IDS} | {EXPECTED_OR_NA} | {STATUS} |

---

## 14. Mode B Automation Handoff

> This section is a read-only manifest for the `vibe-coding/qa` in-IDE agent. Hermes prepares the handoff but writes no test code. The handoff requires aligned TSD/FSD/Mode A baselines, stable test IDs, and repository/ref plus intended test-only paths. Formal plan approval is a gate only when a named project policy requires it.

### 14.1 Automation Gate

| Gate | Required Value | Evidence | State |
|---|---|---|---|
| Mode A plan / RTM baselined | {VERSION_AND_IMMUTABLE_REFERENCE} | {EVIDENCE} | Met / Not Met / Blocked |
| Formal plan approval *(conditional)* | {POLICY_TITLE_VERSION_PATH_OR_NOT_REQUIRED} | {APPROVAL_EVIDENCE_OR_NA} | Met / Not Required / Blocked |
| FSD / TSD versions aligned | {VERSIONS} | {EVIDENCE} | Met / Not Met / Blocked |
| Stack Profile and contracts declared | {FRAMEWORK_PARADIGM_BROKER_AND_REFERENCE} | {EVIDENCE} | Met / Not Met / Blocked |
| Repository and approved ref/branch identified | {REPOSITORY_AND_REF} | {EVIDENCE} | Met / Not Met / Blocked |
| Writable test paths approved | {PATHS} | {EVIDENCE} | Met / Not Met / Blocked |

Default test-only write paths from the EKSAD Testing Guide are:

- `src/test/**`
- `e2e/**`
- `perf/**`
- `security/**`

These are intended writable paths for the receiving in-IDE agent, not for Hermes. `src/main/**`, production configuration, and migrations are read-only for QA. Any project-specific test path outside the defaults requires explicit approval.

### 14.2 Automation Plan

| File / Path | Action | Layer / Tool | Requirement IDs | Test IDs | Helpers / Fixtures | Production Reads | Status |
|---|---|---|---|---|---|---|---|
| `{APPROVED_TEST_PATH}` | Create / Modify | {REST_ASSURED_PLAYWRIGHT_K6_OR_APPROVED_TOOL} | {REQ_IDS} | {TC_IDS} | {HELPERS} | {READ_ONLY_PATHS_OR_NONE} | Handoff Planned / Blocked |

### 14.3 External Execution Request

| Field | Value |
|---|---|
| Repository / exact ref | {REPOSITORY} / {FULL_SHA_OR_REF} |
| Candidate / environment | {BUILD_ARTIFACT_DIGEST} / {ENVIRONMENT} |
| Suite / test IDs | {SUITE_AND_TC_IDS} |
| Variables by name | {VARIABLE_NAMES_ONLY} |
| Pipeline job / stage | {JOB_OR_STAGE} |
| Required reports | {REPORT_TYPES_AND_DESTINATIONS} |
| Evidence owner | {OWNER} |

On a lightweight authoring VPS, perform manifest inspection only. Hermes must not write test code. The `vibe-coding/qa` in-IDE agent owns implementation; build tools and suites run in external CI or another approved environment. `NOT_RUN` remains unchanged in this baseline.

---

## 15. Gaps, Assumptions, and Design Decisions

### 15.1 Gap and Blocker Register

| Gap ID | Description | Affected Requirement / Test | Blocking? | Owner | Due Date | Required Resolution / Evidence | Status |
|---|---|---|---|---|---|---|---|
| QGAP-001 | {DESCRIPTION} | {REFERENCE} | Yes / No | {OWNER} | {DATE_OR_TBD} | {ACTION_OR_DECISION} | Open / Resolved / Deferred |

Use `TBD — Owner: <role/person> — Due: <date or explicit TBD>` for unresolved design facts. Missing expected behavior is an FSD/BA gap; missing or conflicting technical wiring is a TSD/SA gap. Execution/environment issues belong in separate evidence artifacts, not this register.

### 15.2 Assumptions

| Assumption ID | Assumption | Basis | Validator / Owner | Due Date | Impact if False | Status |
|---|---|---|---|---|---|---|
| QASM-001 | {ASSUMPTION} | {SOURCE_OR_REASON} | {OWNER} | {DATE_OR_TBD} | {IMPACT} | Open / Validated / Invalidated |

### 15.3 Design Decisions and Scope Exceptions

| Decision / Exception ID | Description | Named Authority | Scope / Reason | Evidence | Expiry / Follow-up | Status |
|---|---|---|---|---|---|---|
| {ID} | {DECISION_OR_EXCEPTION} | {AUTHORITY} | {SCOPE_REASON} | {REFERENCE} | {DATE_OWNER} | Proposed / Approved / Rejected / Expired |

Record only decisions needed to baseline design/scope. Runtime waivers, defect dispositions, residual-risk decisions, and release decisions belong in separate governed artifacts.

---

## 16. Separate Evidence and QA Assessment References

> This section defines destinations/references only. Do not embed or update runs, reruns, results, defect records, or a final QA/release verdict in this immutable plan. Use existing project-governed artifacts; this template does not create an additional evidence or verdict template.

| Separate artifact | Project-defined location / naming convention | Accountable owner | Required linkage / fields |
|---|---|---|---|
| Execution evidence | {PROJECT_EVIDENCE_ARTIFACT_LOCATION_OR_TBD} | {OWNER} | This plan version/reference; candidate SHA/build/artifact/environment; suite/test IDs; timestamps; executor/job; tool/version; result/exit; immutable reports |
| Defect tracker | {PROJECT_DEFECT_SYSTEM_OR_TBD} | {OWNER} | Project defect ID; requirement/test IDs; expected/actual; evidence; disposition/retest links |
| QA evidence assessment | {PROJECT_QA_ASSESSMENT_ARTIFACT_OR_TBD} | {OWNER} | Named QA policy; exact policy-defined QA verdict fields/values; evidence cut-off and references |
| DevOps release readiness | {DEVOPS_READINESS_ARTIFACT_OR_TBD} | DevOps | Separate DevOps-owned readiness determination; never inferred or populated by this plan |

The QA assessment must use verdict fields and allowed values from `{NAMED_PROJECT_QA_POLICY_TITLE_VERSION_PATH_OR_URL}`. If that policy does not define them, record `TBD` with the policy owner; do not invent fallback QA readiness states and do not borrow DevOps `READY`, `NOT_READY`, or `BLOCKED`.

---

## 17. Baseline Completion Checklist

### 17.1 Sources, Scope, and Traceability

- [ ] QA Mode A and immutable baseline reference are explicit; Mode B is a read-only handoff manifest.
- [ ] Formal approval is required only by an identified named project policy, or is recorded as not required.
- [ ] Exact FSD and applicable TSD paths, versions, and statuses are recorded.
- [ ] In-scope and approved out-of-scope boundaries are explicit.
- [ ] Every in-scope testable requirement has an RTM row.
- [ ] Every test maps back to at least one source requirement.
- [ ] PARTIAL, GAP, and BLOCKED rows have named owners and due dates.
- [ ] Coverage design is not represented as execution success.

### 17.2 Coverage Quality

- [ ] Every test case has all eight canonical columns and a stable ID.
- [ ] Expected results are observable and source-backed.
- [ ] Main, alternative, exception, validation, and documented error behavior is covered.
- [ ] All applicable valid/invalid state transitions and terminal attempts are covered.
- [ ] Endpoint success/auth/role/tenant scenarios are covered where applicable.
- [ ] Soft-delete and write/audit acceptance behavior is covered where applicable.
- [ ] Reserved-field, integration, event, resilience, observability, cache-sync, and NFR tests are included only when sourced.
- [ ] Risk values and thresholds are sourced or explicitly TBD; none are invented.

### 17.3 Ownership, Portability, and Evidence Boundaries

- [ ] QA black-box scope is separate from developer-owned unit/internal integration tests.
- [ ] Mode B intended writes are confined to approved test-only paths for `vibe-coding/qa`; Hermes writes no test code.
- [ ] Environment endpoints and credentials are variables/references, not hard-coded local assumptions or secrets.
- [ ] Test data is isolated, tenant-aware, reproducible, and safe.
- [ ] Entry/exit/suspension criteria cite approved sources and owners.
- [ ] Separate evidence/defect/QA-assessment destinations are identified without embedding mutable records.
- [ ] Every test remains `NOT_RUN` in this design baseline.
- [ ] Named QA policy reference and its exact verdict fields/values are delegated to the separate assessment.
- [ ] QA verdict is explicitly distinct from DevOps release readiness, release authorization, and business acceptance.
- [ ] No build, runtime, container, browser, load, or test execution was performed on the lightweight authoring VPS.

---

> **Template use:** Copy this file to the project's approved QA-document path, rename it `TESTPLAN_{MODULE_CODE}_v{VERSION}.md`, and replace placeholders. Before baseline it may be reviewed/revised. At baseline assign an immutable reference; never append run, rerun, defect, QA verdict, DevOps readiness, or release data. A later design change produces a new version. Keep this generic template free of project-specific completed content.
