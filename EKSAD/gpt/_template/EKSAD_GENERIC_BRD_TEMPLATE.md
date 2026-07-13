# Business Requirements Document (BRD)
# {PROJECT_NAME} — Version {VERSION}

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — Business Requirements Document |
| **Document Type** | Business Requirements Document (BRD) |
| **Project Name** | {PROJECT_NAME} |
| **Module / Domain** | {MODULE_OR_DOMAIN} |
| **Version** | {VERSION} |
| **Status** | 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)* |
| **System** | `{ARTIFACT_ID}` (`{SERVICE_NAME}`) |
| **Organization** | PT EKSAD / {BUSINESS_UNIT} |
| **Classification** | Internal — Confidential |
| **Prepared By** | {PREPARED_BY} |
| **Reviewed By** | {REVIEWED_BY} |
| **Approved By** | {APPROVED_BY} |
| **Last Updated** | {DATE} |

> **Related Documents:**
> - `{PROJECT_CODE}_PROJECT_CHARTER.md` — Project Charter *(authorizes this project)*
> - `FSD_{PROJECT_CODE}_v{VERSION}.md` — Functional specification
> - `TSD_{PROJECT_CODE}_v{VERSION}.md` — Technical specification
> - `{PROJECT_CODE}_REGULATORY.md` — Regulatory & Compliance Reference *(external doc — maintained separately)*

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |

---

## Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Business Owner | | | |
| Project Manager | | | |
| Lead BA | | | |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Background & Problem Statement](#2-business-background--problem-statement)
3. [Objectives & KPIs](#3-objectives--kpis)
4. [Scope](#4-scope)
5. [Stakeholders](#5-stakeholders)
6. [Actors](#6-actors)
7. [Traceability Summary](#7-traceability-summary)
8. [Functional Requirements](#8-functional-requirements)
9. [Features](#9-features)
10. [Business Rules](#10-business-rules)
11. [Data Model Summary](#11-data-model-summary)
12. [Multi-Tenant & SaaS Considerations](#12-multi-tenant--saas-considerations)
13. [Constraints](#13-constraints)
14. [Risks & Mitigations](#14-risks--mitigations)
15. [Gap Analysis](#15-gap-analysis)
16. [Open Issues & Decisions Log](#16-open-issues--decisions-log)
17. [Appendix A — Glossary](#appendix-a--glossary)
18. [Appendix B — Change Log](#appendix-b--change-log)

---

## 1. Executive Summary

> *Write 2–4 paragraphs summarizing: what the system is, why it exists, who uses it, and what the key improvements are over the previous version or current manual process.*

**{PROJECT_NAME}** is a **{SHORT_DESCRIPTION}** built on the EKSAD multi-tenant SaaS platform.

**Key capabilities:**
- {CAPABILITY_1}
- {CAPABILITY_2}
- {CAPABILITY_3}

**Key improvements over {PREVIOUS_SYSTEM / manual process}:**

| Area | Before | After |
|------|--------|-------|
| {AREA_1} | {BEFORE_1} | {AFTER_1} |
| {AREA_2} | {BEFORE_2} | {AFTER_2} |
| Audit Trail | Manual / none | Automatic — all data-modifying actions are logged with full actor, timestamp, and before/after context |
| Multi-Tenant | Single tenant | Full data isolation — users can only access data belonging to their own organisation |

---

## 2. Business Background & Problem Statement

### 2.1 Business Background

> *Describe the business context: what organization/team uses this system, what process it supports, and why it matters.*

{ORGANIZATION_NAME} is responsible for {BUSINESS_FUNCTION}. Currently, {N} {BUSINESS_PROCESS_TYPE}s are managed:

| Type | Frequency | Description |
|------|-----------|-------------|
| {TYPE_1} | {FREQUENCY_1} | {DESCRIPTION_1} |
| {TYPE_2} | {FREQUENCY_2} | {DESCRIPTION_2} |

### 2.2 Problem Statement

> *Articulate the specific business problems this project will solve. Each problem must be given a unique ID so that Business Requirements can trace back to it.*

| ID | Problem Description | Impact if Unsolved |
|---|---|---|
| P-001 | {PROBLEM_1} | {IMPACT_1} |
| P-002 | {PROBLEM_2} | {IMPACT_2} |
| P-003 | {PROBLEM_3} | {IMPACT_3} |

> **Rule:** Each problem must link to at least one Functional Requirement in Section 8.
> Use the pattern: *"P-{NNN} is addressed by FR-{MODULE}-{NNN}"*

### 2.3 As-Is Process

> *Describe how the business currently operates without the proposed system or change. Establish the baseline and make the gap to the To-Be state explicit. Include the actor performing each step and any known pain points.*

| Step | Actor | Action | Pain Point / Issue |
|---|---|---|---|
| 1 | {ACTOR} | {ACTION} | {PAIN_POINT} |
| 2 | {ACTOR} | {ACTION} | {PAIN_POINT} |

### 2.4 To-Be Process

> *Describe how the business will operate after the solution is in place. Each step should represent an improvement or resolution of an As-Is pain point.*

| Step | Actor | Action | Improvement Over As-Is |
|---|---|---|---|
| 1 | {ACTOR} | {ACTION} | {IMPROVEMENT} |
| 2 | {ACTOR} | {ACTION} | {IMPROVEMENT} |

---

## 3. Objectives & KPIs

### 3.1 Objectives

> *Use SMART format: Specific, Measurable, Achievable, Relevant, Time-bound.*

| ID | Objective | Success Indicator | Target Date |
|---|---|---|---|
| OBJ-001 | {OBJECTIVE_1} | {SUCCESS_INDICATOR_1} | {DATE_1} |
| OBJ-002 | {OBJECTIVE_2} | {SUCCESS_INDICATOR_2} | {DATE_2} |
| OBJ-003 | {OBJECTIVE_3} | {SUCCESS_INDICATOR_3} | {DATE_3} |

### 3.2 KPIs & Success Metrics

> *Define how the success of this project will be measured after go-live. Each KPI must be linked to a Business Objective, have a measurable baseline (current state), a target value, and a defined measurement method. KPIs without baselines or targets are not acceptable.*

| KPI ID | Metric Name | Linked Objective | Baseline | Target | Measurement Method |
|---|---|---|---|---|---|
| KPI-001 | {METRIC_1} | OBJ-001 | {BASELINE_1} | {TARGET_1} | {METHOD_1} |
| KPI-002 | {METRIC_2} | OBJ-002 | {BASELINE_2} | {TARGET_2} | {METHOD_2} |

---

## 4. Scope

### 4.1 In Scope

> *List the business capabilities and processes this project will address. Describe each item in terms of business function — not technical tools, frameworks, or implementation choices.*

| # | Capability / Feature | Description |
|---|---|---|
| 1 | {FEATURE_1} | {DESCRIPTION_1} |
| 2 | {FEATURE_2} | {DESCRIPTION_2} |
| 3 | {FEATURE_3} | {DESCRIPTION_3} |
| 4 | Audit Trail | All data-modifying operations are automatically recorded with full actor, timestamp, and data context |
| 5 | Multi-Tenant Isolation | Each client's data is fully isolated — users can only access data belonging to their own organisation |

### 4.2 Out of Scope

> *Explicitly state what will not be addressed by this project. Being clear about exclusions prevents scope creep and sets correct stakeholder expectations.*

| # | Exclusion | Reason / Deferral Note |
|---|---|---|
| 1 | {ITEM_1} | {REASON_1} |
| 2 | {ITEM_2} | {REASON_2} |
| 3 | Mobile application | Web-only in this version |

> **Scope Rule:** Scope must describe business capabilities only. Do NOT include technical tools, frameworks, or implementation details.

### 4.3 Future Scope (Backlog)

- {FUTURE_ITEM_1}
- {FUTURE_ITEM_2}

---

## 5. Stakeholders

> *Identify all individuals and groups with a stake in the outcome of this project. For each stakeholder, define their role clearly and state their specific responsibility within the scope of this initiative.*

| Role | Name / Team | Responsibility | Type |
|------|-------------|----------------|------|
| Business Owner | {NAME} | Accountable for business outcomes; final approver | Internal |
| Project Manager | {NAME} | Manages delivery timeline and scope | Internal |
| Business Analyst | {NAME} | Requirements elicitation, document ownership | Internal |
| Tech Lead | {NAME} | Architecture decisions, code review | Internal |
| Backend Developer | {TEAM} | Service implementation | Internal |
| QA Engineer | {NAME} | Test case design, UAT coordination | Internal |
| {EXTERNAL_ROLE} | {NAME} | {RESPONSIBILITY} | External |
| End User | {USER_GROUP} | {USER_RESPONSIBILITY} | {TYPE} |

---

## 6. Actors

> *Define every human and system actor that will interact with the solution. Distinguish between human actors (roles who perform actions) and system actors (external systems that exchange data or trigger processes). Each actor listed here must appear in at least one process flow or business requirement.*

| Actor | Type | Description of Interaction |
|---|---|---|
| {ROLE_NAME} | Human | {DESCRIPTION} |
| API Gateway | System | Entry point for all requests — enforces authentication before routing to any service |
| Audit Service | System | Receives and stores a complete audit log for every data-modifying action |
| File Storage Service | System | *(Conditional)* Manages file uploads, access control, and URL resolution |
| {EXTERNAL_SYSTEM} | System | {DESCRIPTION} |

---

## 7. Traceability Summary

> *This section provides a high-level mapping of the full requirement traceability chain: from User Requirements down to Business Requirements and Features. This must be kept up to date as requirements evolve. No orphan entries are permitted — every BR must trace to a UR, and every Feature must trace to a BR.*

| UR ID | UR Title | BR ID | BR Title | Feature ID | Feature Title |
|---|---|---|---|---|---|
| UR-{DOMAIN}-001 | {UR_TITLE} | BR-001 | {BR_TITLE} | F-001 | {FEATURE_TITLE} |
| UR-{DOMAIN}-002 | {UR_TITLE} | BR-002 | {BR_TITLE} | F-002 | {FEATURE_TITLE} |

---

## 8. Functional Requirements

> **ID Format:** `FR-{MODULE}-{NNN}` (three-digit zero-padded number)
> **Priority:** P1 = Must Have, P2 = Should Have, P3 = Nice to Have

### 8.1 {MODULE_1_NAME} Module

| ID | Requirement | Priority | Related BR | Addresses Problem |
|----|-------------|----------|------------|-------------------|
| FR-{MODULE1}-001 | {REQUIREMENT_1} | P1 | BR-{N} | P-{NNN} |
| FR-{MODULE1}-002 | {REQUIREMENT_2} | P1 | BR-{N} | P-{NNN} |
| FR-{MODULE1}-003 | {REQUIREMENT_3} | P2 | — | — |

### 8.2 {MODULE_2_NAME} Module

| ID | Requirement | Priority | Related BR | Addresses Problem |
|----|-------------|----------|------------|-------------------|
| FR-{MODULE2}-001 | {REQUIREMENT_1} | P1 | BR-{N} | P-{NNN} |
| FR-{MODULE2}-002 | {REQUIREMENT_2} | P2 | — | — |

### 8.3 Authentication & Authorization

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-AUTH-001 | All features must require valid authentication — unauthenticated requests must be rejected | P1 | Via bearer token — all requests must carry a valid authentication credential |
| FR-AUTH-002 | The authentication token must identify the user's organisation, identity, and assigned role | P1 | Enforced by the authentication service |
| FR-AUTH-003 | Role-based access control (RBAC) must be enforced per operation — each action is restricted to only the roles authorised for it | P1 | Enforced by the platform — no unauthenticated or unauthorised action may proceed |

### 8.4 Audit Trail

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-AUDIT-001 | All data-modifying operations (create, update, delete) must be automatically recorded in the audit trail | P1 | Fired automatically by the platform — no manual wiring required per feature |
| FR-AUDIT-002 | Each audit record must capture: who performed the action, when, what changed (before and after state), and which module it came from | P1 | Captured automatically per operation |
| FR-AUDIT-003 | Audit records must be queryable by action type, actor, and date range | P2 | Available via the Audit Trail service |

---

## 9. Features

> *Features translate Business Requirements into named, scoped capabilities that the system must deliver. Each Feature groups related functional behaviour under a single unit and forms the bridge between BRD and FSD. Every Feature must map to at least one BR. Features defined here will become the primary input for Feature Specifications in the FSD.*

| Feature ID | Feature Name | Description | Source BR(s) | Priority |
|---|---|---|---|---|
| F-001 | {FEATURE_NAME_1} | {DESCRIPTION_1} | BR-001 | P1 |
| F-002 | {FEATURE_NAME_2} | {DESCRIPTION_2} | BR-002 | P1 |
| F-003 | Authentication & Authorization | Secure access — only authenticated users with the correct role may access each feature | FR-AUTH-001 | P1 |
| F-004 | Audit Trail | Automatic logging of every data-modifying action — who did what, when, on what record | FR-AUDIT-001 | P1 |

---

## 10. Business Rules

> **ID Format:** `BR-{NNN}` or `BR-{DOMAIN}-{NNN}` for platform-wide rules.
> Business rules describe constraints the system must respect — not how the system implements them.

| Rule ID | Business Rule | Source / Authority | Module | Priority |
|---|---|---|---|---|
| BR-001 | {RULE_1} | {SOURCE} | {MODULE} | P1 |
| BR-002 | {RULE_2} | {SOURCE} | {MODULE} | P1 |
| BR-003 | A record must never be permanently deleted. Records are archived and marked as deleted — the data is retained but hidden from normal use (soft delete). | EKSAD Platform Standard | All | P1 |
| BR-004 | Every data-modifying operation must produce an audit log entry associated with the performing user and their organisation. | EKSAD Platform Standard | All | P1 |
| BR-005 | {RULE_5} | {SOURCE} | {MODULE} | P2 |
| BR-PLATFORM-006 | Files must be uploaded through the File Storage Service only. Domain services store a file reference ID — never raw storage keys or delivery URLs. | EKSAD Platform Standard | All | P1 |
| BR-PLATFORM-007 | Publicly accessible files are served via a permanent link. Restricted files are served via a time-limited access link generated at request time. | EKSAD Platform Standard | All | P1 |
| BR-PLATFORM-008 | Thumbnail visibility inherits from its parent file. A restricted file always has a restricted thumbnail. | EKSAD Platform Standard | All | P1 |
| BR-PLATFORM-009 | File size and format are enforced at upload by the File Storage Service. Domain services must not re-validate these. | EKSAD Platform Standard | All | P1 |
| BR-PLATFORM-010 | Master/catalog data (brands, models, departments, positions, etc.) is owned exclusively by the Master Data service. Domain services consume this data — they must never duplicate its ownership. | EKSAD Platform Standard | All | P1 |
| BR-PLATFORM-013 | Transactional entities that opt-in to tenant-specific custom fields use a pre-allocated set of configurable field slots — no structural change to the system is required. Custom field requirements are captured during BA elicitation. | EKSAD Platform Standard | All (transactional) | P1 |
| BR-PLATFORM-014 | Custom field labels, visibility, and validation rules are configured per organisation. Configuration changes take effect immediately without any system deployment. | EKSAD Platform Standard | All (transactional) | P1 |

---

## 11. Data Model Summary

> *High-level business entity overview — detailed data schema goes in TSD.*

| Entity | Business Name | Key Attributes | Relationships |
|--------|--------------|----------------|---------------|
| {ENTITY_1} | {BUSINESS_NAME_1} | Unique identifier, organisation scope, {KEY_ATTRIBUTE_1}, {KEY_ATTRIBUTE_2} | {RELATIONSHIP} |
| {ENTITY_2} | {BUSINESS_NAME_2} | Unique identifier, organisation scope, {KEY_ATTRIBUTE_1} | belongs to {ENTITY_1} |
| Audit Log Record | Audit Entry | Unique identifier, action performed, actor, timestamp, data before and after | Standalone — written automatically on every data-modifying operation |

### 11.1 Reserved Fields (Transactional Entities)

> *Transactional entities that opt-in support tenant-specific custom fields via a set of pre-allocated configurable field slots — no structural system change is required.
> Master data and audit entries are EXEMPT.
> Custom field requirements are captured during BA elicitation.*

| Entity | Reserved Fields Needed? | Custom Fields Identified | Config Documented? |
|--------|------------------------|--------------------------|--------------------|
| {ENTITY_1} | Yes / No / TBD | {list — e.g., "Salesperson Code (text), Discount % (number)"} | Yes / Pending |
| {ENTITY_2} | No | None | — |

---

## 12. Multi-Tenant & SaaS Considerations

| Aspect | Description |
|--------|-------------|
| Tenant identification | Every request carries the user's organisation identity — validated on every operation |
| Data isolation | The platform automatically enforces that each user only sees their own organisation's data |
| Tenant provisioning | Managed by the platform administration process |
| Cross-tenant access | Forbidden by default — requires explicit super-admin role |
| Configuration per tenant | Organisation-specific settings are managed by the platform configuration service |
| {CUSTOM_TENANT_RULE} | {DESCRIPTION} |

---

## 13. Constraints

> *Document every known limitation that bounds the solution space. Constraints are conditions that cannot be changed within the scope of this project — they are given, not negotiable. Each constraint must be clearly stated so that solution designers understand the boundaries they must work within.*

| Constraint ID | Constraint Description | Type | Impact |
|---|---|---|---|
| CON-001 | {CONSTRAINT_1} | Business / Regulatory / Technical / Budget / Timeline | {IMPACT} |
| CON-002 | {CONSTRAINT_2} | Business / Regulatory / Technical / Budget / Timeline | {IMPACT} |

---

## 14. Risks & Mitigations

> *Identify risks that could prevent the project from achieving its objectives. Each risk must include a likelihood rating, impact rating, and a defined mitigation.*

| Risk ID | Risk Description | Likelihood | Impact | Mitigation / Contingency |
|---|---|---|---|---|
| RSK-001 | Audit service unavailable — audit records not captured | Low | Medium | Audit events are queued for reliable delivery; failed events are automatically retried and flagged for reconciliation |
| RSK-002 | Data isolation breach — user accesses another organisation's data | Medium | High | Platform enforces organisation boundary automatically; code review checklist includes isolation verification |
| RSK-003 | Scope creep from undocumented business rules | High | Medium | All rules must be captured in BR-{N} before development starts |
| RSK-004 | {CUSTOM_RISK_1} | {PROBABILITY} | {IMPACT} | {MITIGATION} |
| RSK-005 | {CUSTOM_RISK_2} | {PROBABILITY} | {IMPACT} | {MITIGATION} |

---

## 15. Gap Analysis

> *Record all identified gaps discovered during requirements elicitation and document review. Every gap must be classified by severity. Critical gaps must be resolved before this document can be approved.*

> **Rule:** No BRD may be submitted for approval while a Critical gap remains unresolved.

| Gap ID | Description | Severity | Affected Section | Owner | Resolution / Status |
|---|---|---|---|---|---|
| GAP-001 | {DESCRIPTION} | Critical / Non-Critical | {SECTION} | {OWNER} | Open / Resolved / Deferred |

**Severity Definitions:**
- **Critical** — missing core business logic, undefined main process, or missing key requirement. Blocks document approval.
- **Non-Critical** — minor detail missing, low-impact edge case. Document may proceed with gap documented and owner assigned.

---

## 16. Open Issues & Decisions Log

> *Track all unresolved questions, pending decisions, and items tagged `[CLARIFY]` or `[UNCONFIRMED]` during document production. This log must be empty (all items resolved or formally deferred with an owner) before the document status changes to Approved.*

| Issue ID | Description | Raised By | Owner | Target Date | Status |
|---|---|---|---|---|---|
| ISS-001 | {DESCRIPTION} | {RAISED_BY} | {OWNER} | {DATE} | Open / Resolved / Deferred |

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| Tenant | An isolated organisational unit within the EKSAD multi-tenant platform — each tenant's data is fully private and inaccessible to other tenants |
| Tenant Identifier | A unique identifier for each organisation, carried in every authentication token and associated with every data record |
| Soft Delete | Records are never permanently deleted. Instead they are archived — marked as deleted and hidden from normal use, but retained and recoverable by administrators |
| Module Type | A structured label that categorises audit log entries by the business module and action that produced them |
| JWT | JSON Web Token — a signed bearer token used for authentication and authorisation. Carries the user's identity, role, and organisation |
| File Reference ID | A unique identifier stored in a domain record to reference an uploaded file. The domain service stores only this ID — actual file access and URL generation are handled by the File Storage Service |
| File Visibility | Every uploaded file is classified as either publicly accessible (permanent link) or restricted (time-limited access link generated per request) |
| Signed URL | A time-limited, tamper-proof access link for a restricted file. Generated at request time — must not be cached long-term |
| File Storage Service | The dedicated EKSAD platform service responsible for all file uploads, access control, and URL generation |
| User Requirement (UR) | A high-level business need expressed by a stakeholder — input to Business Requirements |
| Business Requirement (BR) | A statement of what the system must achieve to fulfil a UR — describes business intent without implementation detail |
| Feature | A named, scoped capability bridging BRD Business Requirements to FSD Functional Requirements |
| {DOMAIN_TERM_1} | {DEFINITION_1} |
| {DOMAIN_TERM_2} | {DEFINITION_2} |

---

## Appendix B — Change Log

| Version | Date | Author | Summary of Changes |
|---------|------|--------|-------------------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `eksad-core-storage` to architecture, NFR-S-006/007, BR-PLATFORM-006–009, dependency, assumption, and glossary entries |
| 3.0 | 2026-05-02 | EKSAD Platform Team | Major upgrade to v3: Document Control table, Revision History & Approval blocks at top; new sections — Actors, Traceability Summary, As-Is/To-Be Process, Features bridge, KPIs & Success Metrics, Constraints, Gap Analysis, Open Issues Log; NFR Source BR column + Compliance category added; Mermaid architecture diagram replaces ASCII; all EKSAD platform specifics retained |
| 3.1 | 2026-06-03 | EKSAD Platform Team | BRD technical content cleanup: removed §12.1 Standard Base Fields and §13 System Architecture Overview; abstracted §12 Data Model to business entity concepts; split Dependencies to business module scope only; cleaned all DB types, Java class names, framework names, infra ports, and implementation details from NFRs, Business Rules, Assumptions, Multi-Tenant section, Actors, Auth/Audit FRs, and Glossary; renumbered §14–20 → §13–19 |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |
