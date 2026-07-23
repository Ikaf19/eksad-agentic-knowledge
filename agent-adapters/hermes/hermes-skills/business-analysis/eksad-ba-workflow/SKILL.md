---
name: eksad-ba-workflow
description: "Use when the user asks the Business Analyst profile to start a new BRD/FSD/UR workflow, review a BA document, or follow the EKSAD BA pipeline (User Stories → User Requirements → BRD → FSD). Triggers on phrases like 'start a BRD', 'create FSD', 'review this requirement', 'UR dari user story', 'BRD untuk service baru'. Enforces the EKSAD BA pipeline: UR confirmation before BRD, BRD baselined before FSD, gap analysis at every stage, no technology content in business docs."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, ba, brd, fsd, ur, workflow, pipeline]
    related_skills: [multi-role-agent-setup]
---

# EKSAD BA Workflow Skill

Stage-gated workflow for EKSAD Business Analyst work. Produces UR → BRD → FSD with explicit checkpoints, gap analysis, and readiness scoring. **Always pauses for user confirmation between stages** — never skip a stage, never auto-advance.

## When to Use

- User says "start a BRD", "create FSD", "I want to write requirements"
- User provides User Stories and asks to convert to User Requirements
- User asks to review a BRD/FSD for gaps
- User wants a new project kickoff in the BA pipeline

## When NOT to Use

- User asks for TSD / architecture → switch to `system-analyst` profile + `eksad-tsd-design` skill
- User asks for code → switch to `developer-backend` or `developer-frontend` profile
- User asks for test plan → switch to `qa-engineer` profile

## Knowledge References (read before starting)

Primary:
- `~/.hermes/knowledge/eksad/agent-adapters/hermes/role-system-instructions/business-analyst.md` — full operating rules
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BA_DOMAIN_GLOSSARY.md` — BA pipeline terms
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — context for platform BRs

Templates (source of truth):
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_BRD_TEMPLATE.md` — v3.2
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_FSD_TEMPLATE.md` — v3.0
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_REGULATORY_TEMPLATE.md` — companion doc

Supporting:
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_RESERVED_FIELD_PATTERNS.md` — for reserved field discovery
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_GLOSSARY.md` — term check
- `references/greenfield-whole-platform-fsd-decomposition.md` — evidence-based decomposition guidance when common/core/auth/audit/shared foundations do not exist yet

## Pipeline (5 Stages)

### Stage 0 — Intake

Ask the BA Intake questionnaire (15 fields). If user provides partial info, work with what's available and mark assumptions explicitly.

### Stage 1 — User Requirements (UR)

**Input:** User Stories OR rough idea
**Output:** UR document named exactly `UR_{PROJECT_CODE}_v{VERSION}.md`, with requirement entries in this format:
```
UR-[DOMAIN]-[NNN]
Title: ...
Source: [US-XXX, US-YYY]
Statement: ...
Actor(s): ...
Priority: Must / Should / Nice to Have
Notes: ...
```

**Checkpoint:** Present full UR list, ask user to confirm. **DO NOT** proceed to BRD until explicit confirmation.

### Stage 2 — BRD

**Preconditions:**
- [ ] URs confirmed
- [ ] Project name defined
- [ ] BRD template available
- [ ] Stakeholders identified

**Process:**
1. Fill BRD template (15 sections per `EKSAD_GENERIC_BRD_TEMPLATE.md` v3.2)
2. **Auto-include BR-PLATFORM-001..005** + 010/013/014 (if EKSAD context)
3. Service Naming Discovery — suggest `svc-{function}` names
4. Run gap analysis after every section
5. **Critical gap → STOP. Non-critical → annotate and continue**

**Traceability:** `UR-[DOMAIN]-[NNN]` → `BR-[NNN]` → `F-[NNN]` → `FR-[MODULE]-[NNN]`

**Checkpoint:** Present complete BRD, ask user to confirm before FSD.

### Stage 3 — FSD

**Preconditions:**
- [ ] BRD baselined (user says "freeze" or equivalent)
- [ ] FSD template available
- [ ] Per-module feature decomposition done

**Process:**
1. Fill FSD template (15 sections per `EKSAD_GENERIC_FSD_TEMPLATE.md` v3.0)
2. Per-feature 8 components:
   - Precondition
   - Postcondition
   - Main Flow + **Mermaid diagram** (mandatory)
   - Alternative Flow + Mermaid diagram
   - Exception Flow + Mermaid diagram
   - Validation Rules
   - UI Mapping (`UI-[NNN] → FR-[MODULE]-[NNN]`)
   - **Reserved Field Requirements** (mandatory per transactional entity)
3. State Machine per workflow: State Table + Transition Table + **Mermaid `stateDiagram-v2`** + BR per transition
4. Multi-Service FSD: ask per service, one after another

**Forbidden in FSD:**
- DB column types, table/column names
- Java class names (BaseEntity, BaseRepository, etc.)
- Framework/library names (Quarkus, Hibernate, Flyway, etc.)
- Infrastructure ports
- Messaging exchange names
- ASCII / plain-text flow diagrams (Mermaid only)

**Checkpoint:** Present complete FSD, run readiness scoring (target 8.5/10).

### Stage 4 — Final Validation

After FSD, validate against the Definition of Done (13 criteria). If critical gaps remain → do NOT mark as final.

## Output Pattern

Each stage output should include:
1. Narrative paragraph (1–2 sentences)
2. Tables / bullets / numbered lists
3. Mermaid diagrams for flows and state machines
4. Traceability IDs in standard format
5. Gap annotations (Critical vs Non-Critical)
6. Explicit checkpoint request ("Apakah scope ini sudah di-freeze?" / "Lanjut ke FSD?")

## Commit Pattern

After each stage:
```bash
# Save to /workspace/projects/<project>/{UR,BRD,FSD}/<file>.md
cd /workspace/projects/<project>
git add <file>.md
git commit -m "docs(<scope>): <stage> — <short description>"
git push
```

### Workspace placement rule

When the project scope is clear enough to name, keep BA deliverables in the repository's visible project tree rather than primarily in hidden scratch or orchestration paths.

Use this sequence:
1. Bootstrap or confirm the visible project directory (for example, `projects/<project>/`).
2. Write BA artifacts directly into its `UR/`, `BRD/`, and later `FSD/` directories.
3. Keep durable orchestration/progress tracking in that project directory (for example, `orchestration/`).
4. Use hidden plan directories only as temporary scratch space while the formal project location is genuinely undecided.

### Greenfield whole-platform decomposition rule

When a broad BRD starts without shared foundations (such as common/core, auth, audit, notification, or master data), do **not** default to one omnibus FSD.

1. Assess separable business capabilities, actor groups, lifecycle/state models, rule ownership, dependencies, and change cadence, plus cross-cutting governance, reporting, or notification behavior.
2. Split where those evidence dimensions require independently reviewable and changeable specifications; consolidate where they share one coherent lifecycle, rule set, ownership model, and review cadence. Do not target a document count.
3. Keep approval/escalation, auditability, notification audiences, access visibility, tenant/company isolation, and master ownership behavior explicit in BA artifacts.
4. Never say a need is "handled by platform" unless that capability exists and is in scope.

See `references/greenfield-whole-platform-fsd-decomposition.md` for the supporting heuristic.

### Business behavior discovery

Before finalizing BRD/FSD scope, discover and trace the business behavior below without prescribing architecture, storage, APIs, frameworks, infrastructure, or implementation:

| Discovery view | BA questions/output |
|---|---|
| Capability | What business outcome must each actor be able to achieve, and what is explicitly out of scope? |
| Business invariants | Which business truths must always hold before, during, and after a process? Record source/owner; do not invent a rule. |
| State | What business lifecycle states are meaningful, who may initiate each transition, and what business preconditions/postconditions apply? |
| Failure | Which business-visible rejection, conflict, timeout, unavailability, or partial-completion outcomes must be handled? |
| Recovery | What may the actor retry, resume, correct, cancel, reverse, reconcile, or escalate, and under whose authority? |
| Trace metadata | Which requirement, rule, actor, decision, event/time, reason, correlation/reference, and source evidence must remain traceable for business/audit purposes? |

Connect each confirmed item to `UR` → `BR` → `F` → `FR` IDs and to relevant main/alternative/exception flows or state transitions. Mark unknown items `[CLARIFY]` with owner and impact. Keep business-required auditability and trace metadata conceptual; SA/TSD decides technical representation.

## Anti-Patterns (never do)

❌ Skip stage without explicit user confirmation
❌ Generate BRD before URs confirmed
❌ Generate FSD before BRD baselined
❌ Invent business rules to fill gaps
❌ Prescribe technical representation for capabilities, invariants, states, failures, recovery, or trace metadata
❌ Add technology content (framework names, DB types) to BRD/FSD
❌ Use ASCII flow diagrams when Mermaid is required
❌ Mark draft as final before DoD passes
❌ Hide assumptions — mark with `[UNCONFIRMED]` or `[CLARIFY]`

## Phase F Enrichment — Product Capability and Research Patterns

Adapted benchmark patterns: product-capability, market/deep research, content-research-writer.

- Before drafting BRD/FSD, name the product capability, target users, measurable outcome, constraints, and unresolved assumptions.
- For market/domain claims, prefer cited EKSAD/project evidence or mark `[SOURCE GAP]`; never invent market facts.
- Keep research and product insight as BA evidence; technical architecture remains SA/TL-owned.
- Add a handoff note when findings affect UI/UX, data analysis, content, or project scope.
