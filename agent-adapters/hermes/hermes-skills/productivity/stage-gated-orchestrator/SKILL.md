---
name: stage-gated-orchestrator
description: "Use when an EKSAD assignment must run as a visible multi-role pipeline with human review gates, especially UR → BRD → FSD → TSD. Creates a local conductor tracker, records real semantic progress events, delegates each stage to the correct EKSAD role, verifies artifacts, and pauses for APPROVE, REVISE, ABORT, or SKIP before dependent work starts. Gates are mandatory by default; use no-gates mode only when the user explicitly requests automatic continuation."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native)
license: MIT
metadata:
  hermes:
    tags: [eksad, orchestration, hitl, conductor, pipeline, brd, fsd, tsd]
    related_skills: [eksad-ba-workflow, eksad-tsd-design, eksad-task-breakdown]
---

# EKSAD Stage-Gated Orchestrator

## Overview

Coordinate EKSAD work across specialist roles while keeping progress visible and every handoff reviewable. The default document pipeline is:

```text
UR (Business Analyst) → BRD (Business Analyst) → FSD (Business Analyst) → TSD (System Analyst)
```

The conductor records real, semantic activity events and artifact state. It does not expose hidden chain-of-thought or raw internal tool telemetry. A progress event must describe an observable action such as reading a template, drafting a section, running validation, producing an artifact, or waiting for a gate decision.

Default behavior is strict HITL: after a stage artifact passes verification, mark it `awaiting_review` and stop. Never dispatch a dependent stage until the user chooses `APPROVE` or `SKIP`. `--no-gates` is allowed only when the user explicitly asks for automatic continuation **and** the configured pipeline contains neither Project Manager nor DevOps work. A pipeline containing either role must fail closed with gates enabled; user authorization cannot waive this restriction.

## When to Use

- User asks multiple EKSAD roles to collaborate on one assignment.
- User requests live tracking, a conductor view, stage progress, or agent visibility.
- Work has dependent stages such as BRD → FSD → TSD.
- User wants to review or approve each phase before the next role starts.
- The output must preserve an auditable history of artifact creation and gate decisions.

## When NOT to Use

- A single specialist can complete the task in one stage.
- Independent subtasks can safely run in parallel with no shared artifacts.
- User only wants a static status report after completion.
- The task is not EKSAD-related; use a generic orchestration skill instead.

## Required Components

This skill ships with:

```text
stage-gated-orchestrator/
├── SKILL.md
├── references/
│   └── hitl-gate-protocol.md
├── scripts/
│   └── conductor.py
└── templates/
    ├── eksad-pipeline.json
    └── conductor.html
```

Runtime data is created inside the project workspace:

```text
<project>/.conductor/
├── config.json
├── state.json
└── events.jsonl
```

Do not put runtime state in the skill directory or knowledge pack.

## Roles and Default Artifacts

| Stage | Role profile | Required skill | Default artifact |
|---|---|---|---|
| UR | `business-analyst` | `eksad-ba-workflow` | `docs/ur/UR_{PROJECT_CODE}_v{VERSION}.md` |
| BRD | `business-analyst` | `eksad-ba-workflow` | `docs/brd/BRD_<PROJECT>_v1.md` |
| FSD | `business-analyst` | `eksad-ba-workflow` | `docs/fsd/FSD_<PROJECT>_v1.md` |
| TSD | `system-analyst` | `eksad-tsd-design` | `docs/tsd/TSD_<PROJECT>_v1.md` |

Adjust artifact names in the generated project config when an existing project uses another convention. Never silently rename existing artifacts.

### Thirteen-profile routing plus shared AppSec workflow

Route work across the thirteen canonical profiles (General Coordinator plus twelve specialists) by accountable output. The General Coordinator role coordinates and never absorbs specialist ownership. AppSec is a shared workflow, not a tenth profile.

| Role/profile | Route when the required output is | Handoff evidence |
|---|---|---|
| General Coordinator / `eksad-general` | Cross-role intake, coordination, routing, dependency tracking, or synthesis of specialist-owned outputs | Mission, routing decision, source references, and unresolved ownership/authority gaps |
| Project Manager / `project-manager` | Charter, Plan, WBS coordination, RAID, status, change, or closure governance | PM artifact and authority references |
| Business Analyst / `business-analyst` | UR, BRD, FSD, business rules, or business traceability | Baselined requirement IDs and open gaps |
| System Analyst / `system-analyst` | Architecture, TSD, contracts, data/event design, or technical decisions | Approved design references and constraints |
| Technical Leader / `technical-leader` | Design/code quality review or technical readiness verdict | Attributable findings and review verdict |
| Backend Developer / `developer-backend` | Backend implementation and developer-owned tests | Source/build/test evidence available to the worker |
| Frontend Developer / `developer-frontend` | Frontend implementation and developer-owned tests | UI/API contract references and test evidence |
| QA Engineer / `qa-engineer` | Test design, RTM, execution evidence, or QA verdict | Requirement/build identity and test evidence |
| DevOps Engineer / `devops-engineer` | CI/CD, environment, release, deployment, rollback, or operational evidence | Immutable source/artifact identity and authorization references |
| Data Analyst / `data-analyst` | KPI definitions, read-only analysis, data quality findings, or dashboard specifications | Approved question, source inventory, data cut-off, metric definitions, and caveats |
| Data Scientist / `data-scientist` | ML/statistical problem framing, experiment design, model evaluation, or model-risk notes | Data readiness, target/baseline, experiment setup, metrics, and sandbox evidence |
| UI/UX Designer / `ui-ux-designer` | UX research, journey maps, wireframes, usability findings, or frontend handoff | Approved requirements, user context, design states, accessibility notes, and open gaps |
| Content Creator / `content-creator` | Content briefs, sourced drafts, release notes, training/help material, or content calendar | Source artifacts, claim inventory, audience/channel, approval owner, and draft status |

#### Shared AppSec workflow routing

| Responsibility | Canonical routing rule | Required evidence |
|---|---|---|
| Raise trigger / supply evidence | Any role may identify an AppSec trigger and provide scoped design, code, test, scan, dependency, or operational evidence | Trigger, affected scope, target identity/version, and evidence location |
| Coordinate and invoke review | System Analyst or Technical Leader owns review coordination and invokes `eksad-appsec-review`; this is a function assignment, not a profile | Assigned review function, scope, evidence cut-off, and requested decision date |
| Accept residual risk | Only the named risk authority may accept residual risk or authorize a waiver | Attributable decision, scope, rationale, conditions, expiry, and evidence |

When one request spans roles, split it into owned stages and preserve dependency locks. If ownership or authority is unresolved, record a blocking gap instead of routing by convenience.

### Artifact handoff manifest

Every role transition carries one compact manifest; reference artifacts rather than copying their content:

```text
Handoff ID:
From role / to role:
Mission and permitted scope:
Input artifact(s): path, version/state, immutable ID or checksum when available
Source requirement/decision IDs:
Output artifact and exact path:
Acceptance/exit checks:
Known gaps, assumptions, risks, and waivers:
Dependency/gate state and named authority:
Evidence locations and evidence cut-off:
Next action, owner, and due date:
```

The receiver verifies manifest references before starting. A missing, stale, contradictory, inaccessible, or unapproved mandatory input blocks dependent work; it is not silently reconstructed.

### Evidence before status

Derive tracker status only after checking observable evidence. Artifact existence alone does not prove completeness, review, approval, build success, test success, release readiness, or deployment health. Record the evidence reference and cut-off before changing status; otherwise use `blocked`, `unknown`, or the applicable non-terminal state. Never promote worker narrative, elapsed time, or an invented percentage into evidence.

## Workflow

### Step 1 — Confirm Mission and Gates

Capture:

- project name and workspace path;
- requested start/end stage;
- output paths;
- whether gates are strict or explicitly disabled;
- tracker bind host and port;
- whether any artifact already exists and should be reused.

Resolve every configured stage to its role before initialization. If `--no-gates` is requested and any stage includes `project-manager` or `devops-engineer` ownership, reject no-gates initialization, record the conflict, and require gates. Do not silently omit, rename, or re-route those stages to bypass the restriction.

Consequential defaults:

- workspace: user-provided path;
- gates: enabled;
- host: `127.0.0.1`;
- port: `8765`;
- remote git writes: disabled.

Completion criterion: the user has confirmed scope, workspace, and any eligible non-default `--no-gates` or public-network exposure; PM/DevOps pipelines are confirmed as gated.

### Step 2 — Initialize the Conductor

From this skill directory:

```bash
python3 scripts/conductor.py init \
  --workspace /absolute/project/path \
  --project "Project Name"
```

To expose on a trusted network, serving is separate and explicit:

```bash
python3 scripts/conductor.py serve \
  --workspace /absolute/project/path \
  --host 0.0.0.0 \
  --port 8765
```

For explicit automatic continuation in a pipeline that contains neither PM nor DevOps work:

```bash
python3 scripts/conductor.py init \
  --workspace /absolute/project/path \
  --project "Project Name" \
  --no-gates
```

Completion criterion: `.conductor/config.json`, `state.json`, and `events.jsonl` exist; `status` returns valid JSON.

### Step 3 — Record Dispatch Before Delegation

Before spawning a worker, mark the stage in progress:

```bash
python3 scripts/conductor.py event \
  --workspace /absolute/project/path \
  --stage BRD \
  --role orchestrator \
  --status in_progress \
  --message "Dispatching Business Analyst for BRD"
```

The worker prompt must include:

1. exact role/profile and skill;
2. source artifacts and knowledge files;
3. one exact output path;
4. machine-checkable exit criteria;
5. instruction to record meaningful progress events;
6. prohibition on dependent-stage work.

Completion criterion: tracker shows the stage as `in_progress` before worker execution begins.

### Step 4 — Track Real Semantic Progress

Record events at meaningful boundaries, not invented percentages:

```bash
python3 scripts/conductor.py event --workspace /path --stage BRD --role ba \
  --message "Reading EKSAD BRD template v3.2"

python3 scripts/conductor.py event --workspace /path --stage BRD --role ba \
  --message "Drafting scope, stakeholders, and business rules"

python3 scripts/conductor.py event --workspace /path --stage BRD --role ba \
  --message "Running traceability and forbidden-technology checks"
```

Never claim visibility into hidden reasoning. If a delegated worker cannot write events itself, the orchestrator may record only externally observed milestones: dispatched, artifact appeared, validation started, validation result, and gate opened.

Completion criterion: each completed stage has at least dispatch, validation, and artifact events.

### Step 5 — Verify the Artifact

Every stage needs stage-specific checks plus these minimum checks:

- expected file exists;
- file is non-trivial;
- required template headings are present;
- source-to-output traceability is present;
- forbidden content check passes;
- no downstream artifact was generated early.

Example:

```bash
test -f docs/brd/BRD_PROJECT_v1.md
test "$(wc -c < docs/brd/BRD_PROJECT_v1.md)" -ge 3000
grep -q '^## Document Control' docs/brd/BRD_PROJECT_v1.md
```

If verification fails, set `blocked` or `revision_required`; do not open an approval gate.

Completion criterion: all declared checks pass and their result is recorded as a conductor event.

### Step 6 — Open the HITL Gate

After successful verification:

```bash
python3 scripts/conductor.py complete \
  --workspace /absolute/project/path \
  --stage BRD \
  --artifact docs/brd/BRD_PROJECT_v1.md \
  --summary "BRD verified; ready for business review"
```

With gates enabled, this sets the stage to `awaiting_review`. Ask the user to choose:

- `APPROVE` — accept and unlock next stage;
- `REVISE <notes>` — return to the same role with review feedback;
- `ABORT <reason>` — stop this pipeline;
- `SKIP <reason>` — unlock next stage without approval, explicitly audited.

Use the exact decision command after the user responds:

```bash
python3 scripts/conductor.py gate \
  --workspace /absolute/project/path \
  --stage BRD \
  --decision APPROVE \
  --note "Approved by user in chat"
```

Completion criterion: the gate decision appears in `events.jsonl` and stage state is `approved`, `revision_required`, `aborted`, or `skipped`.

### Step 7 — Chain or Revise

- `APPROVE` / `SKIP`: dispatch only the immediate next stage.
- `REVISE`: send the exact review notes to the same role, overwrite only the agreed artifact, re-run all checks, and reopen the gate.
- `ABORT`: cancel dependent todo items and leave artifacts untouched.
- No response: remain paused. Do not interpret silence as approval.

When an eligible `--no-gates` pipeline is active, `complete` marks the stage `approved` automatically, but verification is still mandatory. Discovery of PM or DevOps work after initialization immediately blocks automatic continuation until gates are enabled and the conflict is recorded.

Completion criterion: only an unlocked stage can become `in_progress`.

### Step 8 — Finalize

After TSD (or the configured final stage) is approved:

- report all artifacts and sizes;
- report each gate decision and revision count;
- report unresolved assumptions;
- leave the tracker available until the user asks to stop it;
- do not commit or push unless separately authorized.

Completion criterion: every configured stage is approved/skipped or the pipeline is explicitly aborted.

## Worker Prompt Contract

Append this to each delegated task:

```text
Conductor tracking is enabled.
Before each meaningful activity boundary, record a semantic event for this stage.
Do not report hidden reasoning or invented progress percentages.
Write exactly the declared artifact.
Run all exit criteria before completion.
Do not begin any dependent stage.
After writing the artifact, return a compact summary with path, size, checks, and deviations.
```

## Network Exposure

The tracker contains project names, file paths, event messages, and document metadata. Treat it as internal project information.

- Default: `127.0.0.1`.
- `0.0.0.0` requires explicit user approval.
- This server has no authentication or TLS.
- Do not expose secrets, prompt contents, credentials, or document bodies in event messages.
- Prefer VPN, SSH tunnel, or a trusted internal network.

## Git Safety

Conductor state is local runtime data. Add `.conductor/` to the project `.gitignore` unless the user explicitly wants the audit trail versioned.

This skill itself may live in the EKSAD knowledge repository, but:

- create a feature branch;
- never commit without review;
- never push to `feature/eksad-knowledge-v2`;
- never push any branch without explicit user approval.

## Common Pitfalls

1. Calling a simulated animation “live tracking.” Only file state and recorded events are real.
2. Starting FSD while BRD is merely complete but not approved.
3. Letting a worker produce BRD, FSD, and TSD in one task, bypassing gates.
4. Recording hidden reasoning or confidential document content in logs.
5. Exposing `0.0.0.0` without explaining the lack of auth/TLS.
6. Treating `SKIP` as `APPROVE`; preserve the difference in the audit log.
7. Auto-committing artifacts after a gate. Approval of content is not approval to commit or push.
8. Deleting artifacts on `ABORT`; abort stops work but preserves evidence.

## Verification Checklist

- [ ] Skill loaded for an EKSAD multi-stage assignment
- [ ] Project workspace and stage range confirmed
- [ ] Gate mode confirmed; default is enabled
- [ ] `--no-gates` rejected if any configured or discovered stage contains PM or DevOps work
- [ ] Conductor initialized and status endpoint works
- [ ] Public binding explicitly approved if used
- [ ] One specialist role owns each stage
- [ ] Nine-profile routing plus shared AppSec workflow used without absorbing specialist ownership
- [ ] Handoff manifest references verified before receiver starts
- [ ] Real semantic events recorded; no simulated claims
- [ ] Evidence reference/cut-off recorded before status changes
- [ ] Artifact checks pass before gate opens
- [ ] User decision is recorded exactly
- [ ] Dependent stage remains locked until APPROVE/SKIP
- [ ] REVISE loops back with exact feedback
- [ ] ABORT preserves existing artifacts
- [ ] Commit and push handled as separate approvals
