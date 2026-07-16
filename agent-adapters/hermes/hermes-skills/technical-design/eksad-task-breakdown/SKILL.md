---
name: eksad-task-breakdown
description: "Use as a Project Manager-orchestrated helper when the project team must decompose FSD features into Work Breakdown Structure (WBS) tasks for sprint planning, estimation, or task assignment. Produces a structured WBS with task IDs, role owners, specialist-supplied estimates, dependencies, and acceptance criteria. The PM is accountable for the WBS baseline; specialists own their task content and estimates. Distinct from built-in `writing-plans`, which is bite-sized TDD implementation planning."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native)
license: MIT
metadata:
  hermes:
    tags: [eksad, wbs, task-breakdown, sprint-planning, estimation]
    related_skills: [eksad-ba-workflow, eksad-tsd-design, writing-plans]
---

# EKSAD Task Breakdown / WBS Skill

Project-level Work Breakdown Structure helper for EKSAD projects. The Project Manager orchestrates decomposition and is accountable for the WBS baseline; each specialist owns the content and estimate of tasks in that specialist's lane.

## When to Use

- User asks "break this feature into tasks" / "create WBS"
- User wants sprint planning input
- User wants to estimate effort for a feature
- Project kickoff — assign tasks to BA / SA / TL / Dev-BE / Dev-FE / QA / DevOps

## When NOT to Use

- **Bite-sized TDD implementation tasks** (2-5 min each with code) → use built-in `writing-plans` skill
- **Architecture decisions** → `system-analyst` + `eksad-tsd-design`
- **Business requirements** → `business-analyst` + `eksad-ba-workflow`
- **Code review** → `technical-leader` + `eksad-code-review`
- **Test case design** → `qa-engineer`

**Why this is separate from `writing-plans`:** `writing-plans` is for one feature implementation (bite-sized TDD steps with code). This skill is for project-level WBS — multiple features, multiple roles, multiple sprints.

## Knowledge References

- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_FSD_TEMPLATE.md` — FSD structure (input for WBS)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_TSD_TEMPLATE.md` — TSD structure (downstream of WBS)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` — service boundaries
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_REGISTRY.md` — domain map for multi-service projects
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_RESERVED_FIELD_PATTERNS.md` — when reserved fields add work
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_WBS_TEMPLATE.md` — canonical WBS output structure

## Operating Context

You operate on a **lightweight VPS Hermes Agent**. Constraints:
- **WBS coordination/drafting** — performed under Project Manager orchestration ✅
- **Specialist task content and estimates** — supplied or confirmed by the applicable specialist ✅
- **WBS baseline approval** — Project Manager accountability; this helper cannot self-baseline ✅
- **Git commit/push** — not automatic and not implied by WBS approval; requires separate explicit authorization
- **Execution** — NOT your job (task execution happens on developer machine)

## WBS Methodology

### Input

- FSD (baselined) — source of features (`F-NNN`)
- TSD (if exists) — clarifies technical breakdown
- Stack Profile (Quarkus/SB/Reactive/Imperative/RabbitMQ/Kafka) — affects task complexity

### Output

A WBS file named exactly `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md` and based on `EKSAD_GENERIC_WBS_TEMPLATE.md`, with:
- Task IDs (linked to F-NNN + role prefix)
- Task names
- Task type (BA / SA / TL / Dev-BE / Dev-FE / QA / DevOps)
- Owner role
- Estimate (T-shirt S/M/L/XL or hours)
- Dependencies (Task IDs that must complete first)
- Acceptance criteria
- Sprint assignment (optional)

### Traceable slices and dependencies

Decompose into outcome-verifiable vertical slices where feasible. Every task must identify its source `UR/BR/F/FR` or approved TSD/decision IDs, parent WBS element, role owner, concrete output, acceptance evidence, predecessor IDs, and downstream consumer. Use `None` only after checking dependencies; use `TBD — Owner — Due Date` for an unresolved dependency.

Classify dependencies as mandatory predecessor, external/provider, approval/gate, environment/tooling, or sequencing preference. Record provider, consumer, needed outcome, required-by point, acceptance evidence, and fallback. A provider's completion does not close the dependency until the consumer confirms the required outcome. Detect cycles, ownerless tasks, orphan source IDs, and tasks with no verifiable output before sprint assignment.

Do not invent estimates, velocity, capacity, sprint dates, implementation choices, acceptance thresholds, or team availability. Copy them from approved sources or named-owner evidence; otherwise leave explicit TBDs. Keep specialist design/test decisions with the accountable role.

### Ownership and baseline governance

- The Project Manager orchestrates this helper, resolves planning dependencies, and is accountable for the WBS baseline and change control.
- BA, SA, TL, Backend, Frontend, QA, and DevOps specialists own and confirm their respective task content, estimates, technical assumptions, and acceptance evidence.
- The helper may assemble, normalize, and validate supplied content but cannot approve specialist estimates, assign people, baseline the WBS, or authorize repository writes.

### Task Type per EKSAD Role

| Role | Typical tasks |
|------|---------------|
| **BA** | Stakeholder interview, UR refinement, BRD review, FSD review, gap analysis |
| **SA** | TSD design (per module), Flyway DDL design, API contract design, ERD, event schema design, ADR |
| **TL** | Architecture decision review, code review, mentoring, PR checklist enforcement |
| **Dev-BE** | Entity, BaseRepository, service, REST resource, DTO, mapper, Flyway DDL, unit test, integration test, BaseRepository implementation |
| **Dev-FE** | Feature package scaffold, hook, service, component, schema, test (monorepo structure per `eksad-fe-impl`) |
| **DevOps** | Dockerfile, docker-compose, CI/CD pipeline, K8s manifest, monitoring setup |
| **QA** | Mode A test plan, RTM, test case matrix, and state machine matrix; Mode B automation is an in-IDE handoff and not produced by Hermes |

### Estimation Conventions

**T-shirt sizes (recommended for fast sprint planning):**

| Size | Hours | When to use |
|------|-------|-------------|
| **S** | 1-4 hours | Single file, well-understood, copy-paste from existing pattern |
| **M** | 4-8 hours (1 day) | New entity + repo + service + resource, multiple files but standard pattern |
| **L** | 1-3 days | New module with complex logic, multiple states, integration points |
| **XL** | 3-5 days | Architectural change, new bounded context, multi-service coordination |
| **XXL** | > 1 week | Should be broken down further — escalate |

**Story points (alternative):** Fibonacci (1, 2, 3, 5, 8, 13, 21) — for teams with stable velocity.

## Template usage

Start from `EKSAD_GENERIC_WBS_TEMPLATE.md`; do not reproduce a second embedded template. Populate its source basis, hierarchy, task inventory, dependency register, traceability coverage, estimate/sprint evidence, and validation sections. Preserve TBDs until the accountable owner supplies evidence.

## Optional Git Handoff

Only after separate explicit commit and push authorization:

```bash
cd /workspace/projects/<project>/
git add TIA_WBS_AUTH_v1.0.md
git commit -m "docs(WBS): initial task breakdown for [feature]"
git push
```

WBS content approval or PM baseline approval alone does not authorize either command.

## Anti-Patterns

❌ Decompose before FSD is baselined (leads to rework)
❌ Use story points without team velocity history (just use T-shirt sizes)
❌ Skip dependency graph (leads to scheduling conflicts)
❌ Single mega-task > XXL (always break down further)
❌ Skip acceptance criteria per task (QA can't verify)
❌ Assign concrete people (use roles, not names — names change)
❌ Include time buffers in tasks (use sprint capacity for that)
❌ Use this skill for one-feature TDD planning (use `writing-plans` instead)

## Related Skills

- `eksad-ba-workflow` — FSD output is the WBS input
- `eksad-tsd-design` — TSD clarifies technical breakdown
- `eksad-code-review` — Task T-TL-002/003 use this
- `writing-plans` (built-in) — For bite-sized TDD implementation, NOT this
- `subagent-driven-development` (built-in) — For executing plans task-by-task

## Output Standards

1. Always include **dependency graph** (text or Mermaid)
2. Always include **sprint plan** section (or note "no sprint assignment yet")
3. Always include **risks & assumptions** section
4. Always link tasks to **UR/BR/F/FR or approved TSD/decision IDs**
5. Always include **acceptance criteria and evidence** per task
6. Include parent WBS, predecessor IDs, and downstream consumer per task
7. Validate dependency cycles and require consumer confirmation for closure
8. Use **roles not names** for owners
9. **Never** assign concrete people to tasks (that happens in sprint planning, not WBS)
10. Never invent estimates, velocity, capacity, dates, thresholds, or implementation choices

## Phase F Enrichment — File-Based Planning Pattern

Adapted benchmark patterns: planning-with-files and product-capability.

- Decompose work by artifact and accountable role, not only by implementation component.
- Each task should identify source requirement, owner, dependency, expected evidence, and approval gate.
- Keep PM WBS ownership separate from specialist estimate/technical validation ownership.
