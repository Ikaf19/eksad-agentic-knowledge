# EKSAD Generic WBS Template

> Filename: `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md`
> Owner: Project Manager, accountable for orchestration, baseline approval, and WBS change control; specialist roles own and confirm their task content and estimates.
> Use approved source evidence. Do not invent estimates, thresholds, dates, capacity, dependencies, or implementation choices.

# {PROJECT_NAME} — Work Breakdown Structure: {SCOPE}

## Document Control

| Field | Value |
|---|---|
| Project / scope | {PROJECT_CODE} / {SCOPE} |
| Version / status | {VERSION} / Draft / In Review / Approved / Superseded |
| Accountable WBS baseline owner | Project Manager / {NAMED_PM_OR_TBD} |
| Baseline reference | {REFERENCE_OR_TBD} |
| Evidence cut-off | {DATE_OR_TBD} |
| Last updated | {DATE} |

## 1. Source and Planning Basis

| Source artifact/decision | Version/state | Applicable IDs | Owner | Evidence |
|---|---|---|---|---|
| UR / BRD / FSD | {VALUE} | {UR/BR/F/FR_IDS} | BA | {REFERENCE} |
| Architecture / TSD / ADR | {VALUE_OR_NA} | {IDS} | SA / Design Authority | {REFERENCE} |
| Release / policy / constraints | {VALUE_OR_NA} | {IDS} | {OWNER} | {REFERENCE} |

Missing mandatory input: `TBD — Owner: {OWNER} — Due: {DATE_OR_TBD}`. Mark whether it blocks decomposition or sprint assignment.

## 2. Scope and Decomposition Rules

**Included outcome:** {OUTCOME}

**Excluded:** {BOUNDARIES}

**Slice rule:** Prefer outcome-verifiable vertical slices. Keep specialist design, implementation, test, security-risk, and release decisions with their accountable roles.

**Ownership rule:** The PM orchestrates and baselines the WBS. Each specialist confirms task content, estimate, assumptions, and acceptance evidence for that specialist lane. Drafting or baseline approval does not authorize a git commit or push.

## 3. WBS Hierarchy

| WBS ID | Parent ID | Slice/deliverable | Source IDs | Role owner | Concrete output | Acceptance evidence |
|---|---|---|---|---|---|---|
| WBS-{PROJECT}-1 | None | {SLICE} | {UR/BR/F/FR/TSD/ADR} | {ROLE} | {OUTPUT} | {EVIDENCE} |
| WBS-{PROJECT}-1.1 | WBS-{PROJECT}-1 | {WORK_PACKAGE} | {IDS} | {ROLE} | {OUTPUT} | {EVIDENCE} |

## 4. Task Inventory

| Task ID | Parent WBS | Source IDs | Task / outcome | Role owner | Output | Acceptance criteria/evidence | Estimate/source | Predecessors | Downstream consumer | State |
|---|---|---|---|---|---|---|---|---|---|---|
| T-{ROLE}-001 | {WBS_ID} | {IDS} | {TASK} | {ROLE} | {OUTPUT} | {CRITERIA_AND_EVIDENCE} | {VALUE_OR_TBD_AND_SOURCE} | {TASK_IDS/NONE/TBD} | {ROLE/TASK} | Planned |

Use roles, not person names. `None` means dependencies were checked and none exist; unresolved values use `TBD — Owner — Due Date`.

## 5. Dependency Register

| Dependency ID | Type | Provider | Consumer | Required outcome | Required by | Acceptance evidence | Fallback | State / consumer confirmation |
|---|---|---|---|---|---|---|---|---|
| DEP-{PROJECT}-001 | Mandatory predecessor / External / Gate / Environment / Sequencing | {PROVIDER} | {CONSUMER} | {OUTCOME} | {TASK_OR_DATE} | {EVIDENCE} | {APPROVED_FALLBACK_OR_TBD} | Open / Confirmed / Blocked / Closed |

A dependency closes only after the consumer confirms the required outcome. Identify cycles and unresolved external dependencies explicitly.

## 6. Traceability Coverage

| Source ID | Covered by task(s) | Acceptance evidence | Gap / owner / due |
|---|---|---|---|
| {F/FR/TSD/ADR_ID} | {TASK_IDS} | {REFERENCE} | {NONE_OR_TBD} |

## 7. Estimate and Sprint Assignment

| Task ID | Estimate | Estimator/source | Confidence/assumptions | Sprint/milestone | Capacity confirmation |
|---|---|---|---|---|---|
| {TASK_ID} | {VALUE_OR_TBD} | {ROLE_AND_REFERENCE} | {VALUE} | {VALUE_OR_UNASSIGNED} | {REFERENCE_OR_TBD} |

Do not infer velocity, convert estimation scales, or assign a sprint without approved team evidence.

## 8. Risks, Assumptions, and Gaps

| ID | Type | Statement | Impact | Owner | Due / validation | Blocking? | Evidence/state |
|---|---|---|---|---|---|---|---|
| {ID} | Risk / Assumption / Gap | {STATEMENT} | {IMPACT} | {OWNER} | {DATE_OR_TBD} | Yes / No | {REFERENCE/STATE} |

## 9. Validation

- [ ] Every task has a parent, source ID, role owner, output, and acceptance evidence
- [ ] Source coverage has no unexplained orphan IDs
- [ ] Dependencies name provider, consumer, required outcome, and acceptance evidence
- [ ] Dependency graph has no unresolved cycle
- [ ] Estimates/dates/capacity cite approved or owner-provided evidence, otherwise TBD
- [ ] No specialist decision or external assumption was invented
- [ ] Sprint assignment is absent or supported by capacity/dependency evidence
- [ ] Review decision, actor, date, and evidence are recorded
- [ ] PM baseline accountability and specialist confirmations are recorded
- [ ] Any commit/push has separate explicit authorization; no repository write authority is inferred from approval

> **Template use:** Copy this file to the approved project-planning path, rename it `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md`, replace placeholders, and keep this generic template free of project-specific completed content.
