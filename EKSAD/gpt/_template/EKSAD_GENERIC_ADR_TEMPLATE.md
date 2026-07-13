# EKSAD Generic Architecture Decision Record (ADR) Template

> Filename: `ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md`
> Owner: System Analyst / Architecture owner
> An author recommendation is not an accepted decision. Acceptance requires the named decision authority.

# ADR-{PROJECT_CODE}-{NNN} — {DECISION_TITLE}

## Document Control

| Field | Value |
|---|---|
| ADR ID | ADR-{PROJECT_CODE}-{NNN} |
| Version | {VERSION} |
| Status | Proposed / In Review / Accepted / Rejected / Superseded / Deprecated |
| Scope / Services | {SCOPE} |
| Decision owner | {NAME_ROLE} |
| Decision authority | {NAME_ROLE} |
| Created / Updated | {DATE} / {DATE} |
| Decision required by | {DATE_OR_NA} |
| Review trigger/date | {TRIGGER_OR_DATE} |
| Supersedes | {ADR_IDS_OR_NONE} |
| Superseded by | {ADR_ID_OR_NONE} |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial proposal |

## 1. Decision Summary

| Item | Detail |
|---|---|
| Trigger | {WHY_A_DURABLE_DECISION_IS_REQUIRED} |
| Decision question | {ONE_CLEAR_QUESTION} |
| Recommended option | {OPTION_OR_PENDING} |
| Current decision | Pending / Accept {OPTION} / Reject / Defer |
| One-sentence rationale | {RATIONALE_OR_PENDING} |

## 2. Context, Scope, and Traceability

### 2.1 In Scope / Out of Scope

- In scope: {COMPONENTS_DOMAINS_ENVIRONMENTS}
- Out of scope: {EXCLUSIONS}

### 2.2 Related Sources

| Source type | ID / version / location | Relevance |
|---|---|---|
| BRD/FSD/NFR | {REFERENCE} | {DRIVER} |
| TSD/Architecture | {REFERENCE} | {AFFECTED_DESIGN} |
| Existing ADR | {REFERENCE_OR_NONE} | {RELATION} |
| Threat model/AppSec | {REFERENCE_OR_PENDING} | {SECURITY_IMPACT} |
| Operational/data evidence | {REFERENCE} | {EVIDENCE} |

### 2.3 Facts, Constraints, Assumptions, Unknowns

| Type | Statement | Evidence / Owner | Freshness / Due date |
|---|---|---|---|
| Fact | {STATEMENT} | {REFERENCE} | {DATE} |
| Approved constraint | {STATEMENT} | {REFERENCE} | {DATE} |
| Assumption | {STATEMENT} | {VALIDATION_OWNER} | {DATE} |
| Unknown | {QUESTION} | {OWNER} | {DATE} |

## 3. Decision Drivers

| Driver / EKSAD principle / NFR | Priority | Measure or acceptance condition |
|---|---|---|
| {DRIVER} | Must / Should / Could | {CONDITION} |

## 4. Options Considered

> Include the status quo where viable. Describe genuine options fairly; do not manufacture precision.

### Option A — {NAME}

{DESCRIPTION}

### Option B — {NAME}

{DESCRIPTION}

### Option C — {NAME_OR_REMOVE}

{DESCRIPTION}

## 5. Trade-off Assessment

| Dimension | Option A | Option B | Option C | Evidence / assumption |
|---|---|---|---|---|
| EKSAD alignment | {ASSESSMENT} | {ASSESSMENT} | {ASSESSMENT} | {REFERENCE} |
| Security / trust boundaries | | | | |
| Reliability / failure modes | | | | |
| Observability / support | | | | |
| Data / tenant isolation | | | | |
| Performance / capacity | | | | |
| Migration / compatibility | | | | |
| Rollback / reversibility | | | | |
| Dependency / supply chain | | | | |
| Delivery effort / operating cost | | | | |
| Lock-in / long-term maintenance | | | | |

## 6. Security and Operational Checkpoints

- Assets/data affected: {DETAIL}
- Trust boundaries added/changed: {DETAIL}
- Threat-model/AppSec disposition: Required / Updated / Not required because {EVIDENCE}
- Telemetry and alert ownership: {SIGNALS_OWNER}
- Failure and degraded modes: {DETAIL}
- Migration/preconditions: {DETAIL}
- Rollback trigger, procedure, and data compatibility: {DETAIL}

## 7. Recommendation

{RECOMMENDED_OPTION_AND_WHY_BENEFITS_OUTWEIGH_DRAWBACKS}

Known drawbacks accepted by the recommendation: {DRAWBACKS}. This recommendation does not constitute approval.

## 8. Decision Record

| Field | Value |
|---|---|
| Authority | {NAME_ROLE} |
| Decision | Pending / Accept Option {X} / Reject / Defer |
| Date | {DATE} |
| Rationale | {RATIONALE} |
| Conditions / expiry | {CONDITIONS_OR_NONE} |
| Evidence | {REFERENCE} |
| Dissent / unresolved concern | {DETAIL_OR_NONE} |

## 9. Consequences and Risks

### Positive Consequences

- {CONSEQUENCE}

### Negative Consequences / Debt

- {CONSEQUENCE_AND_OWNER}

### Residual Risks

| Risk | Treatment | Authority / owner | Due / expiry | Evidence |
|---|---|---|---|---|
| {RISK} | Mitigate / Avoid / Transfer / Awaiting acceptance | {ROLE} | {DATE} | {REFERENCE} |

## 10. Implementation and Propagation

Complete after acceptance.

| Artifact/action | Required update | Owner | Due | Status | Evidence |
|---|---|---|---|---|---|
| TSD / Architecture | {UPDATE} | {OWNER} | {DATE} | Pending | {REFERENCE} |
| Threat model / AppSec | {UPDATE} | {OWNER} | {DATE} | Pending | {REFERENCE} |
| Contract / backlog / runbook | {UPDATE} | {OWNER} | {DATE} | Pending | {REFERENCE} |
| Migration / rollback / observability | {UPDATE} | {OWNER} | {DATE} | Pending | {REFERENCE} |

## 11. Validation and Review

| Validation / review trigger | Expected evidence | Owner | Date / condition | Result |
|---|---|---|---|---|
| {VALIDATION} | {EVIDENCE} | {OWNER} | {DATE_OR_TRIGGER} | Pending |

## 12. Supersession Record

When replaced, create and accept the successor ADR before marking this ADR `Superseded`.

| Field | Value |
|---|---|
| Successor ADR | {ADR_ID} |
| Effective date | {DATE} |
| Scope replaced / retained | {DETAIL} |
| Updated by | {NAME_ROLE} |

> **Template use:** Copy this file to the approved architecture-decision path, rename it `ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md`, replace placeholders, and keep this generic template free of project-specific completed content.
