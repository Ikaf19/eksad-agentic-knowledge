---
name: eksad-ui-ux-delivery
description: "Use when the UI/UX profile must create UX research notes, journey maps, wireframes, usability findings, or frontend handoff packages. Enforces requirement traceability, accessibility states, and no frontend implementation."
version: 0.1.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, uiux, design, wireframe, handoff]
    related_skills: [stage-gated-orchestrator]
---

# EKSAD UI/UX Delivery Skill

## When to Use

- The active or routed EKSAD role is `ui-ux-designer`.
- The user asks for an output governed by `portable/roles/ui-ux-designer.md`.
- The work requires traceable evidence, explicit assumptions, and approval-safe handoff.

## When NOT to Use

- The request is owned by BA, SA, TL, Developer, QA, PM, DevOps, AppSec, business/legal, or another named authority.
- The user asks to mutate production data, publish externally, deploy/promote a model, or bypass approval gates.
- Required source evidence or approval owner is missing and cannot be recovered; produce a gap/handoff instead.

## Knowledge References

Read these first:

- `portable/roles/ui-ux-designer.md`
- `portable/workflows/ui-ux-workflow.md`
- `portable/policies/role-boundaries.md`
- `portable/policies/approval-gates.md`
- `portable/rag/corpus-matrix.md`
- `portable/llm-gateway/role-model-matrix.md`

Default deliverables:

- `portable/deliverables/ux-research-report.md`
- `portable/deliverables/wireframe-handoff.md`

## Workflow

1. **Intake** — restate objective, role boundary, source artifacts, data/design/content access constraints, output path, and approval owner.
2. **Evidence inventory** — list cited sources and mark gaps before drafting.
3. **Draft/analysis** — produce the role-owned artifact only; keep assumptions and confidence/caveats visible.
4. **Quality gate** — verify traceability, boundary compliance, and no credential/production mutation.
5. **Handoff** — route any downstream decision, implementation, approval, or operational step to the accountable owner.

## Output Contract

Every substantive output must include:

- Objective and scope.
- Source artifacts and evidence cut-off.
- Assumptions and open gaps.
- Role-owned artifact body.
- Approval/handoff owner.
- Boundary statement when the output is a draft, recommendation, or analysis rather than an approval/verdict.

## Prohibitions

- Do not invent facts, metrics, model results, user research findings, content claims, approvals, or owners.
- Do not expose secrets or request credentials.
- Do not mutate production systems or publish external content.
- Do not claim another EKSAD role's verdict or approval.
