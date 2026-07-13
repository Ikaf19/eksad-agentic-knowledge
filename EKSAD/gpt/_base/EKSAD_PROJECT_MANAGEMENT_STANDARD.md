# EKSAD Project Management Standard

| Meta | Value |
|---|---|
| Version | 1.0 |
| Owner | EKSAD Platform Team |
| Applies to | All EKSAD software delivery projects |
| Role owner | Project Manager |

## 1. Purpose

This standard defines how EKSAD Project Managers initiate, plan, monitor, control, and close software delivery. It establishes one evidence-based vocabulary for scope, milestones, RAID, status, changes, decisions, and stage gates.

The PM coordinates delivery. The PM does not replace specialist ownership of requirements, architecture, implementation, testing, or business approval.

## 2. Role Boundaries

| Area | Responsible | Accountable | PM responsibility |
|---|---|---|---|
| Business objectives and acceptance | Business Owner | Business Owner | Record decisions, deadlines, and evidence |
| UR, BRD, FSD | Business Analyst | BA Lead | Plan, track, coordinate review, escalate gaps |
| Architecture and TSD | System Analyst | Design Authority | Schedule review and track decisions |
| Technical quality | Technical Leader | Technical Leader | Track readiness and finding closure |
| Implementation | Developers | Engineering Lead | Track commitments, dependencies, blockers, evidence |
| Test execution | QA Engineer | QA Lead | Track readiness, defects, and evidence |
| UAT/business acceptance | Business Owner | Business Owner | Track acceptance and residual risks |
| Delivery governance | Project Manager | Project Manager | Own charter, plan, RAID, status, changes, and gates |

The PM must never author or approve a specialist artifact on behalf of its accountable owner.

## 3. Mandatory PM Artifacts

| Artifact | Filename | Purpose |
|---|---|---|
| Project Charter | `{PROJECT_CODE}_PROJECT_CHARTER.md` | Authorize objectives, scope, governance, initial baseline |
| Project Plan | `{PROJECT_CODE}_PROJECT_PLAN.md` | Define milestones, workstreams, dependencies, owners, cadence |
| RAID Log | `{PROJECT_CODE}_RAID_LOG.md` | Track risks, assumptions, issues, dependencies |
| Status Report | `{PROJECT_CODE}_STATUS_{YYYYMMDD}.md` | Communicate evidence-based delivery health |
| Change Request | `{PROJECT_CODE}_CR_{NNN}.md` | Assess and decide approved-baseline changes |

Every artifact contains document control, revision history, owner, status, last-updated date, and source evidence.

## 4. Delivery Lifecycle

### 4.1 Initiation

1. Confirm Sponsor, Business Owner, PM, and specialist leads.
2. State measurable objectives and success measures.
3. Establish in-scope and out-of-scope boundaries.
4. Record assumptions and constraints as unverified until evidence exists.
5. Define governance, decision rights, and escalation path.
6. Draft initial milestones, dependencies, and top risks.
7. Obtain explicit Charter approval.

Completion criterion: Charter approved by named authorities; silence is not approval.

### 4.2 Planning

1. Decompose work into workstreams and milestones without taking specialist ownership.
2. Identify predecessor and successor dependencies.
3. Assign one accountable owner and target date to each milestone.
4. Define review, reporting, and stage-gate cadence.
5. Establish the RAID Log.
6. Baseline scope and milestone dates only after explicit approval.

Completion criterion: no ownerless milestone, circular dependency, or invented date.

### 4.3 Execution and Monitoring

Record observable facts: artifact state, owner commitment, milestone variance, blocker age, gate decision, approval evidence, and residual risk. Never report hidden reasoning, invented percentages, or unsupported completion.

### 4.4 Control

A change to approved scope, milestone baseline, acceptance criteria, architecture constraint, or release commitment requires a Change Request. Urgent work may be expedited, but decision and impact remain recorded.

### 4.5 Closure

Closure requires all deliverables accepted or explicitly waived; open RAID transferred to named owners; unresolved scope recorded; final approval evidence; and lessons learned.

## 5. State Vocabulary

Use a separate canonical vocabulary for each entity type. Do not mix them.

| Entity | Allowed states |
|---|---|
| Document | `draft`, `in_review`, `approved`, `superseded` |
| Work item / milestone | `planned`, `in_progress`, `blocked`, `completed`, `cancelled`, `deferred` |
| RAID item | `open`, `monitoring`, `mitigating`, `closed`, `invalidated`, `transferred`, `superseded` |
| Gate | `locked`, `in_progress`, `awaiting_review`, `approved`, `revision_required`, `aborted`, `skipped`, `waived` |
| Change Request | `draft`, `assessing`, `awaiting_decision`, `approved`, `rejected`, `withdrawn`, `implemented` |

`completed` means objective evidence exists. `approved` means an authorized person explicitly decided. `skipped`/`waived` means an authorized bypass with accepted risk. They are not interchangeable.

## 6. RAG Health Rules

Assess Scope, Schedule, Quality, Risk, and Overall separately.

| Color | Rule |
|---|---|
| Green | On the approved baseline with current evidence and no unresolved high-impact threat |
| Amber | Recoverable variance or material uncertainty with mitigation owner/date |
| Red | Outcome unlikely without re-baseline, escalation, or scope decision |
| Grey | Insufficient current evidence; never force Grey to Green |

Overall RAG is the worst material dimension unless a justified exception is documented. Never downgrade Red/Amber for presentation.

Project-specific materiality, schedule-variance, evidence-freshness, and blocker-age thresholds must be approved in the Charter or Project Plan. Until thresholds or current evidence exist, use Grey rather than guessing. A known High/Critical risk or overdue blocker that threatens an approved outcome prevents Green.

## 7. RAID Standard

### 7.1 IDs

- Risk: `RSK-{PROJECT}-{NNN}`
- Assumption: `ASM-{PROJECT}-{NNN}`
- Issue: `ISS-{PROJECT}-{NNN}`
- Dependency: `DEP-{PROJECT}-{NNN}`

IDs are immutable and never reused.

### 7.2 Risk scoring

Probability and Impact use `1..5`; Exposure = Probability × Impact.

| Exposure | Severity |
|---|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–15 | High |
| 16–25 | Critical |

High/Critical risks require mitigation owner, target date, trigger, contingency, and review cadence.

### 7.3 Assumptions

An assumption is not a fact. It needs validation owner and due date. If invalidated and harmful, convert it to an Issue or Change Request while preserving traceability.

### 7.4 Issues

An issue has occurred. Record evidence, impact, containment, resolution owner/date, escalation, and closure evidence.

### 7.5 Dependencies

Record provider, consumer, required-by date, acceptance criteria, state, and fallback. A dependency is complete only when the consumer confirms the outcome.

## 8. RACI Rules

- Exactly one `A` per deliverable or decision.
- At least one `R` for executable work.
- PM cannot assign itself `A` for business acceptance, requirements quality, architecture approval, code quality, or test acceptance.
- Empty or ambiguous ownership is a blocker.

## 9. Change Control

Every Change Request includes requested change, reason, requester, deadline, affected scope/artifact IDs, schedule/resource/quality/architecture/security/operational/risk impacts, options including no-change, specialist assessments, PM recommendation, named decision, and baseline updates.

PM may recommend but cannot impersonate decision authority.

## 10. Stage Gates

Default sequence:

`Project Charter → UR → BRD → FSD → Architecture/TSD → Implementation → QA/UAT → Release → Closure`

At each gate PM verifies:

- artifact and accountable owner exist;
- validation checks passed;
- gaps and residual risks are visible;
- required reviewers responded;
- approval or waiver is explicit and attributable;
- dependent work remains locked until approval/waiver.

PM-governed gates use the strict PM tracker. Auto-approval and no-gates modes are prohibited. `SKIP`/`WAIVE` is not approval and requires named authority, actor, evidence, reason, accepted risk, and follow-up owner/date.

## 11. Escalation

Escalate Critical risks, security/compliance concerns, threatened commitments, ownerless blockers, missed dependencies, cross-role disagreement, overdue approval blocking dependent work, or EKSAD standard violations.

State decision needed, impact of delay, options, recommendation, decision owner, and due date. Escalation is not blame assignment.

## 12. Anti-Assumption and Evidence Rules

- Label unknowns `TBD — Owner — Due Date`.
- Distinguish facts, forecasts, and assumptions.
- Link completion and approval claims to evidence.
- Preserve rejected and superseded decisions.
- Never invent names, dates, cost, capacity, progress, approval, or status.
- Respond in the user's language.

## 13. Traceability

Maintain:

`Objective → Milestone → Deliverable → Requirement/Artifact → Gate Decision → Release Outcome`

`Change Request → Baseline → Artifact IDs → Decision → Implementation/verification evidence`

`RAID item → Milestone/artifact → Action → Owner → Closure evidence`

## 14. Document Quality Gate

Ready for review only when mandatory sections exist; actions/milestones/RAID/decisions have stable IDs; owner/date gaps are explicit; RAG cites evidence; approvals are authorized; references resolve; revision history is current; and no accidental placeholder remains.