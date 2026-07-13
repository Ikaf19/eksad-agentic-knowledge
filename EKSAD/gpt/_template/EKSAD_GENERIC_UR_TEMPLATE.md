# User Requirements Document (UR)
# {PROJECT_NAME} — Version {VERSION}

> Filename: `UR_{PROJECT_CODE}_v{VERSION}.md`

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — User Requirements Document |
| **Document Type** | User Requirements Document (UR) |
| **Project Name** | {PROJECT_NAME} |
| **Project Code** | `{PROJECT_CODE}` |
| **Module / Domain** | {MODULE_OR_DOMAIN} |
| **Version** | {VERSION} |
| **Status** | 🔴 Draft / 🟡 In Review / 🟢 Confirmed / ⚫ Superseded *(pick one)* |
| **Organization** | PT EKSAD / {BUSINESS_UNIT} |
| **Classification** | Internal — Confidential |
| **Source / Request Reference** | {INTERVIEW_WORKSHOP_TICKET_OR_SOURCE} |
| **Prepared By** | {PREPARED_BY} |
| **Reviewed By** | {REVIEWED_BY} |
| **Confirmed By** | {CONFIRMED_BY} |
| **Last Updated** | {DATE} |

> **Audience:** Business Owner, Product Owner, Business Analyst, Project Manager, and downstream specification owners.
>
> This document captures **what users need and why**, in user/business language. It precedes the BRD and must not contain solution architecture, framework, database, class, deployment, or infrastructure design.

> **Related Documents:**
> - `{PROJECT_CODE}_PROJECT_CHARTER.md` — Project Charter *(if applicable)*
> - `BRD_{PROJECT_CODE}_v{BRD_VERSION}.md` — downstream Business Requirements Document
> - `FSD_{PROJECT_CODE}_v{FSD_VERSION}.md` — downstream Functional Specification Document

---

## Revision History

| Version | Date | Author | Summary of Changes | Source / Decision Reference |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial draft | {REFERENCE} |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} | {REFERENCE} |

---

## Confirmation

> Confirmation means the captured user needs are a valid input to BRD analysis. It does not approve the BRD, FSD, architecture, implementation, QA verdict, or release.

| Role | Name | Decision | Evidence / Signature | Date |
|---|---|---|---|---|
| Business Owner / Product Owner | {NAME} | Confirm / Revise | {REFERENCE} | {DATE} |
| Lead Business Analyst | {NAME} | Confirm / Revise | {REFERENCE} | {DATE} |
| Key User Representative | {NAME} | Confirm / Revise | {REFERENCE} | {DATE} |

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Background and User Problem](#2-background-and-user-problem)
3. [Source and Elicitation Record](#3-source-and-elicitation-record)
4. [Users and Stakeholders](#4-users-and-stakeholders)
5. [Scope Boundary](#5-scope-boundary)
6. [User Requirement Catalogue](#6-user-requirement-catalogue)
7. [User Journeys and Scenarios](#7-user-journeys-and-scenarios)
8. [User Data and Information Needs](#8-user-data-and-information-needs)
9. [Business-Level Quality Expectations](#9-business-level-quality-expectations)
10. [Constraints, Assumptions, and Dependencies](#10-constraints-assumptions-and-dependencies)
11. [Traceability Summary](#11-traceability-summary)
12. [Prioritization and Release Grouping](#12-prioritization-and-release-grouping)
13. [Gap Analysis](#13-gap-analysis)
14. [Open Issues and Decisions Log](#14-open-issues-and-decisions-log)
15. [Confirmation Checklist](#15-confirmation-checklist)
16. [Glossary](#16-glossary)
17. [Appendix — Change Log](#17-appendix--change-log)

---

## 1. Purpose

### 1.1 Document Purpose

> *State why these user requirements are being captured, which initiative or problem they support, and how the document will be used as input to the BRD.*

{PURPOSE}

### 1.2 Intended Outcome

> *Describe the user-visible or business outcome without prescribing a technical solution.*

{INTENDED_OUTCOME}

### 1.3 Requirement Language

- Use clear, testable user/business language.
- Use **must** for mandatory needs, **should** for important non-mandatory needs, and **may** for optional needs.
- Keep one need per UR ID.
- Mark unknown facts `[CLARIFY]` and unconfirmed statements `[UNCONFIRMED]`.
- Do not invent missing business rules, roles, measures, dates, or approvals.

---

## 2. Background and User Problem

### 2.1 Business Context

> *Describe who performs the current process, what triggers it, its frequency or volume when known, and why it matters. Use source-backed facts; otherwise mark them unconfirmed.*

{BUSINESS_CONTEXT}

### 2.2 User Problem Statements

| Problem ID | Affected User / Group | Current Problem | Evidence / Source | Impact |
|---|---|---|---|---|
| UP-001 | {USER} | {PROBLEM} | {REFERENCE} | {IMPACT} |
| UP-002 | {USER} | {PROBLEM} | {REFERENCE} | {IMPACT} |

### 2.3 Current Process Summary

| Step | Actor | Current Action | Input / Information | Pain Point | Problem ID |
|---|---|---|---|---|---|
| 1 | {ACTOR} | {ACTION} | {INPUT} | {PAIN_POINT} | UP-001 |
| 2 | {ACTOR} | {ACTION} | {INPUT} | {PAIN_POINT} | UP-002 |

### 2.4 Desired User Outcome

| Outcome ID | Desired Outcome | Beneficiary | Observable Success | Source |
|---|---|---|---|---|
| UO-001 | {OUTCOME} | {USER_GROUP} | {OBSERVABLE_RESULT} | {REFERENCE} |
| UO-002 | {OUTCOME} | {USER_GROUP} | {OBSERVABLE_RESULT} | {REFERENCE} |

---

## 3. Source and Elicitation Record

### 3.1 Source Register

| Source ID | Source Type | Title / Description | Owner / Participant | Date / Version | Location / Evidence | Reliability / Notes |
|---|---|---|---|---|---|---|
| SRC-001 | Interview / Workshop / Ticket / Existing Document / Observation | {DESCRIPTION} | {OWNER} | {DATE_VERSION} | {REFERENCE} | {NOTES} |
| SRC-002 | {TYPE} | {DESCRIPTION} | {OWNER} | {DATE_VERSION} | {REFERENCE} | {NOTES} |

### 3.2 Elicitation Sessions

| Session ID | Date | Method | Participants / Roles | Topics | Decisions / Findings | Follow-up |
|---|---|---|---|---|---|---|
| ELC-001 | {DATE} | {METHOD} | {PARTICIPANTS} | {TOPICS} | {FINDINGS} | {ACTION_OR_NONE} |

### 3.3 Source User Stories / Requests

> *Preserve an existing source ID. If the source has no stable ID, assign a local `SRC-*` reference rather than fabricating a ticket number.*

| Source ID | User Story / Request | Actor | Business Value | Related Problem / Outcome |
|---|---|---|---|---|
| {US_OR_SRC_ID} | As a {ACTOR}, I want {NEED}, so that {VALUE}. | {ACTOR} | {VALUE} | UP-001 / UO-001 |

---

## 4. Users and Stakeholders

### 4.1 User Groups

| User ID | User / Role Name | Description | Goals | Current Pain Points | Scope / Organization Boundary |
|---|---|---|---|---|---|
| USER-001 | {ROLE_NAME} | {DESCRIPTION} | {GOALS} | {PAIN_POINTS} | {BOUNDARY} |
| USER-002 | {ROLE_NAME} | {DESCRIPTION} | {GOALS} | {PAIN_POINTS} | {BOUNDARY} |

### 4.2 Stakeholders

| Stakeholder / Role | Interest | Responsibility for This UR | Decision / Confirmation Authority |
|---|---|---|---|
| Business Owner | {INTEREST} | Owns desired business outcome | {AUTHORITY} |
| Product Owner / Key User | {INTEREST} | Confirms user need and priority | {AUTHORITY} |
| Business Analyst | {INTEREST} | Elicits, analyzes, and maintains UR | Document owner |
| {STAKEHOLDER} | {INTEREST} | {RESPONSIBILITY} | {AUTHORITY_OR_NONE} |

### 4.3 Access and Responsibility Needs

> *Describe user-visible responsibilities and boundaries. Do not assign technical authorization annotations, token claims, or implementation details here.*

| User ID | Information / Capability Needed | Allowed Business Action | Prohibited / Restricted Action | Source |
|---|---|---|---|---|
| USER-001 | {CAPABILITY} | {ALLOWED} | {RESTRICTED} | SRC-001 |

---

## 5. Scope Boundary

### 5.1 In Scope

| Scope ID | User Capability / Process | Description | Beneficiary | Source |
|---|---|---|---|---|
| USCP-001 | {CAPABILITY} | {DESCRIPTION} | {USER} | SRC-001 |
| USCP-002 | {CAPABILITY} | {DESCRIPTION} | {USER} | SRC-002 |

### 5.2 Out of Scope

| Exclusion ID | Excluded Capability / Process | Reason | Future Reference / Owner |
|---|---|---|---|
| UEX-001 | {EXCLUSION} | {REASON} | {REFERENCE_OR_OWNER} |

### 5.3 Scope Notes

> Scope is expressed as user and business capability. Technology, data schema, class design, integration transport, ports, build tools, and deployment topology belong to downstream technical design.

---

## 6. User Requirement Catalogue

> **ID Format:** `UR-{DOMAIN}-{NNN}`. Use a stable, uppercase domain/module code and a three-digit zero-padded sequence.
>
> **Priority:** Must / Should / Nice to Have. Priority must come from the named business/product source.
>
> Every UR must trace to at least one source and one user problem or desired outcome. Downstream BR/Feature/FR IDs remain `TBD` until those artifacts exist.

### 6.1 Requirement Summary

| UR ID | Title | User / Actor | Requirement Statement | Priority | Source ID(s) | Problem / Outcome | Status |
|---|---|---|---|---|---|---|---|
| UR-{DOMAIN}-001 | {TITLE} | USER-001 | The user must be able to {USER_NEED}. | Must | SRC-001 | UP-001 / UO-001 | Draft / Confirmed / Revised / Withdrawn |
| UR-{DOMAIN}-002 | {TITLE} | USER-002 | The user should be able to {USER_NEED}. | Should | SRC-002 | UP-002 / UO-002 | {STATUS} |

### 6.2 Detailed User Requirements

> *Repeat this subsection for every UR.*

#### UR-{DOMAIN}-001 — {TITLE}

| Field | Detail |
|---|---|
| **User / Actor** | USER-001 — {ROLE} |
| **Statement** | The user must be able to {ONE_CLEAR_USER_NEED}. |
| **Business Rationale** | {WHY_THIS_IS_NEEDED} |
| **Source** | SRC-001 / {EXACT_REFERENCE} |
| **Addresses** | UP-001 / UO-001 |
| **Priority** | Must / Should / Nice to Have |
| **Precondition (business/user level)** | {PRECONDITION_OR_NONE} |
| **Expected User Outcome** | {OBSERVABLE_OUTCOME} |
| **Frequency / Volume** | {SOURCE_BACKED_VALUE_OR_TBD} |
| **Dependencies** | {DEPENDENCY_ID_OR_NONE} |
| **Exclusions** | {WHAT_THIS_UR_DOES_NOT_INCLUDE} |
| **Notes** | {NOTES_OR_NONE} |

**User-level confirmation examples:**

```text
Given {user/business context},
When {user action or business event},
Then {observable user/business outcome}.
```

> These examples clarify the user need. Detailed acceptance criteria and system behavior are defined in the FSD.

---

## 7. User Journeys and Scenarios

### 7.1 Journey Catalogue

| Journey ID | Journey Name | Primary User | Trigger | Related URs | Outcome |
|---|---|---|---|---|---|
| UJ-001 | {JOURNEY_NAME} | USER-001 | {TRIGGER} | UR-{DOMAIN}-001 | {OUTCOME} |

### 7.2 Journey Detail

#### UJ-001 — {JOURNEY_NAME}

| Step | User / Actor | User Action | Information Needed | Expected User-Visible Outcome | Related UR |
|---|---|---|---|---|---|
| 1 | USER-001 | {ACTION} | {INFORMATION} | {OUTCOME} | UR-{DOMAIN}-001 |
| 2 | {ACTOR} | {ACTION} | {INFORMATION} | {OUTCOME} | UR-{DOMAIN}-002 |

### 7.3 Alternative and Exception Scenarios

| Scenario ID | Related Journey / UR | Condition | User Need / Expected Outcome | Source / Gap |
|---|---|---|---|---|
| UALT-001 | UJ-001 / UR-{DOMAIN}-001 | {CONDITION} | {EXPECTED_OUTCOME} | SRC-001 |
| UEXC-001 | UJ-001 / UR-{DOMAIN}-001 | {FAILURE_CONDITION} | {EXPECTED_OUTCOME_OR_CLARIFY} | GAP-001 / SRC-002 |

---

## 8. User Data and Information Needs

> *Capture the information users need to provide, view, search, export, or retain. Do not define database tables, column types, JSON schemas, or storage technology.*

| Information ID | Information / Data Need | User / Actor | Purpose | Required / Optional | Sensitivity / Handling Need | Related UR | Source |
|---|---|---|---|---|---|---|---|
| UDATA-001 | {INFORMATION} | USER-001 | {PURPOSE} | Required | {CLASSIFICATION_OR_TBD} | UR-{DOMAIN}-001 | SRC-001 |

### 8.1 Tenant-Specific Custom Information Discovery

> *Use this section only to capture business/user needs for organization-specific fields. Whether reserved fields apply and how they are designed is resolved in downstream EKSAD analysis/design.*

| User / Organization | Entity / Record | Custom Information Needed | Type in User Language | Required? | Visibility / Rule | Related UR | Status |
|---|---|---|---|---|---|---|---|
| {USER_OR_ORG} | {BUSINESS_ENTITY} | {CUSTOM_FIELD_LABEL} | Text / Number / Date / Yes-No / Other | Yes / No / TBD | {USER_RULE} | UR-{DOMAIN}-001 | Confirmed / Clarify |

---

## 9. Business-Level Quality Expectations

> *Capture measurable user/business expectations only when supplied by an authorized source. Do not select frameworks, brokers, databases, protocols, architecture patterns, or implementation thresholds.*

| Expectation ID | Category | User / Business Expectation | Measure / Target | Source | Related UR | Status |
|---|---|---|---|---|---|---|
| UQE-001 | Availability / Performance / Accessibility / Security / Auditability / Reporting / Other | {EXPECTATION} | {MEASURABLE_TARGET_OR_TBD} | SRC-001 | UR-{DOMAIN}-001 | Confirmed / Clarify |

> If users need delayed/background processing, describe the business expectation (for example, “the user may continue while processing completes”) without selecting messaging technology.

---

## 10. Constraints, Assumptions, and Dependencies

### 10.1 User / Business Constraints

| Constraint ID | Constraint | Type | Source | Impacted URs | Impact |
|---|---|---|---|---|---|
| UCON-001 | {CONSTRAINT} | Business / Regulatory / Policy / Timeline / Budget / Operational | SRC-001 | UR-{DOMAIN}-001 | {IMPACT} |

### 10.2 Assumptions

| Assumption ID | Assumption | Basis | Validator / Owner | Due Date | Impact if False | Status |
|---|---|---|---|---|---|---|
| UASM-001 | {ASSUMPTION} | {SOURCE_OR_REASON} | {OWNER} | {DATE_OR_TBD} | {IMPACT} | Open / Validated / Invalidated |

### 10.3 Dependencies

| Dependency ID | Dependency | Provider / Owner | Consumer / Related UR | Needed By | Acceptance / Evidence | Status |
|---|---|---|---|---|---|---|
| UDEP-001 | {DEPENDENCY} | {OWNER} | UR-{DOMAIN}-001 | {DATE_OR_TBD} | {EVIDENCE} | Open / Confirmed / Blocked |

---

## 11. Traceability Summary

### 11.1 Source-to-UR Traceability

| Source ID / User Story | Problem / Outcome | UR ID(s) | Coverage | Gap / Note |
|---|---|---|---|---|
| SRC-001 | UP-001 / UO-001 | UR-{DOMAIN}-001 | Covered / Partial / Gap | {NOTE} |

### 11.2 UR-to-Downstream Traceability

> *Populate downstream columns only after the corresponding artifact exists. Use `TBD` rather than inventing IDs.*

| UR ID | BR ID | Feature ID | FR ID(s) | BRD / FSD Version | Trace Status |
|---|---|---|---|---|---|
| UR-{DOMAIN}-001 | TBD | TBD | TBD | TBD | Pending BRD |
| UR-{DOMAIN}-002 | {BR_ID_OR_TBD} | {FEATURE_ID_OR_TBD} | {FR_IDS_OR_TBD} | {BRD_FSD_VERSIONS_OR_TBD} | Pending / Traced |

### 11.3 Traceability Checks

- [ ] Every UR has at least one source reference.
- [ ] Every UR addresses a named problem or desired outcome.
- [ ] Every in-scope source need maps to at least one UR or a documented gap.
- [ ] No downstream BR/Feature/FR exists without a confirmed UR, or the exception is escalated.
- [ ] Withdrawn/superseded URs retain history and downstream impact.

---

## 12. Prioritization and Release Grouping

> *Priority and grouping are business/product decisions. Record source and authority; do not infer urgency from wording.*

| UR ID | Priority | Target Group / Release | Rationale | Decision Owner | Decision Evidence | Dependencies |
|---|---|---|---|---|---|---|
| UR-{DOMAIN}-001 | Must | {GROUP_OR_TBD} | {RATIONALE} | {OWNER} | {REFERENCE} | UDEP-001 |

---

## 13. Gap Analysis

> Critical gaps include missing core user need, undefined primary user/process/outcome, contradictory mandatory requirements, or missing confirmation needed to proceed. Critical gaps block UR confirmation.

| Gap ID | Description | Severity | Affected UR / Section | Blocking? | Owner | Due Date | Resolution / Status |
|---|---|---|---|---|---|---|---|
| GAP-001 | {DESCRIPTION} | Critical / Non-Critical | {REFERENCE} | Yes / No | {OWNER} | {DATE_OR_TBD} | Open / Resolved / Deferred |

**Severity definitions:**

- **Critical** — prevents reliable understanding or confirmation of a core user requirement.
- **Non-Critical** — a limited detail is missing; it remains visible with an owner and does not invalidate the core need.

---

## 14. Open Issues and Decisions Log

| Issue / Decision ID | Type | Description | Options / Decision | Owner / Authority | Due / Decision Date | Evidence | Status |
|---|---|---|---|---|---|---|---|
| UID-001 | Question / Decision | {DESCRIPTION} | {OPTIONS_OR_DECISION} | {OWNER} | {DATE_OR_TBD} | {REFERENCE} | Open / Decided / Deferred / Superseded |

> Reviewer silence is not confirmation. Deferred items require an owner, rationale, and downstream impact.

---

## 15. Confirmation Checklist

### 15.1 Content

- [ ] Purpose, context, problems, and desired outcomes are clear.
- [ ] Users, stakeholders, and business responsibility boundaries are identified.
- [ ] In-scope and out-of-scope capabilities are explicit.
- [ ] Each UR contains one clear user need.
- [ ] Priority has an authorized source.
- [ ] User journeys include relevant alternative/exception needs.
- [ ] Information and custom-field needs are captured in user language.
- [ ] Quality expectations are measurable or explicitly TBD.

### 15.2 Traceability and Governance

- [ ] Stable `UR-{DOMAIN}-{NNN}` IDs are used.
- [ ] Sources, problems/outcomes, and downstream placeholders are traceable.
- [ ] Assumptions, dependencies, gaps, and decisions have owners.
- [ ] No Critical gap remains open for Confirmed status.
- [ ] Confirmation is attributable to named roles and evidence.
- [ ] Revision history is current.

### 15.3 Role and Language Boundary

- [ ] No architecture, framework, database schema, Java class, messaging transport, port, CI/CD, or deployment design appears.
- [ ] No business rule, role, metric, deadline, or approval was invented.
- [ ] `[CLARIFY]`, `[UNCONFIRMED]`, and `TBD` are used for unresolved facts.
- [ ] Document language follows the project/user language decision; IDs and system identifiers remain stable.

---

## 16. Glossary

| Term | Definition | Source / Owner |
|---|---|---|
| UR | A stable statement of a user need that precedes downstream business and functional specification. | EKSAD BA workflow |
| User Problem | A current user/business difficulty supported by a source. | {SOURCE} |
| Desired Outcome | An observable result the user or business seeks. | {SOURCE} |
| `[CLARIFY]` | Missing information requiring a named answer. | Document convention |
| `[UNCONFIRMED]` | A captured statement that has not yet been confirmed by its owner. | Document convention |
| {TERM} | {DEFINITION} | {SOURCE} |

---

## 17. Appendix — Change Log

| Change ID | Date | Changed UR / Section | Previous Value | New Value | Reason / Source | Downstream Impact | Author |
|---|---|---|---|---|---|---|---|
| UCH-001 | {DATE} | {UR_OR_SECTION} | {OLD} | {NEW} | {REFERENCE} | {BRD_FSD_IMPACT_OR_NONE} | {AUTHOR} |

---

> **Template use:** Copy this file to the project UR folder, rename it `UR_{PROJECT_CODE}_v{VERSION}.md`, replace placeholders, preserve source and traceability IDs, and keep this generic template free of project-specific completed content.
