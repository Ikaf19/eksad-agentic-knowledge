---
name: eksad-general-coordination
description: "Use when the General Coordinator profile must triage a request, map it to EKSAD roles, plan cross-role handoffs, run a stage-gated pipeline, or produce an attributable management synthesis without taking specialist ownership. Enforces role boundaries, approval gates, evidence cut-offs, and Git-only/runtime-approval separation."
version: 1.0.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, orchestration, routing, handoff, stage-gate, coordination]
    related_skills: [stage-gated-orchestrator, eksad-task-breakdown, multi-role-agent-setup]
---

# EKSAD General Coordination Skill

## When to Use

- The active or routed EKSAD role is `general-coordinator`.
- The user asks which role should handle work, how roles connect, or how to run a multi-role pipeline.
- The work involves multiple role artifacts, approval gates, dependency sequencing, or management synthesis.
- The user asks for assessment-first planning before changes.

## When NOT to Use

- A specialist deliverable is clearly owned by one role and no cross-role routing is needed; load the specialist skill instead.
- The user asks the coordinator to approve, merge, deploy, publish, accept risk, or finalize specialist output. Produce a handoff/gate note instead.
- The request requires runtime activation, credential use, or production mutation without explicit approval.

## Source References

Read when relevant:

- `portable/roles/general-coordinator.md`
- `portable/roles/role-collaboration-matrix.md`
- `portable/policies/role-boundaries.md`
- `portable/policies/approval-gates.md`
- `portable/mcp/role-mcp-matrix.md`
- `portable/rag/corpus-matrix.md`
- `portable/llm-gateway/role-model-matrix.md`
- `agent-adapters/hermes/skill-enrichment-benchmark.md`

## Workflow

1. **Intake classify** — restate goal, scope, constraints, current evidence, and whether this is assessment-only or execution-approved.
2. **Role sort** — map each requested outcome to accountable role(s), supporting roles, and forbidden ownership transfers.
3. **Artifact dependency map** — identify required inputs/outputs using `role-collaboration-matrix.md`.
4. **Gate detection** — list approval, security, data, release, publication, and runtime activation gates.
5. **Plan or dispatch** — create a stage-gated plan or route to specialist skills/profiles; keep each handoff attributable.
6. **Verification loop** — check evidence, citations, role boundaries, and unresolved gaps before summarizing.
7. **Synthesis** — provide management-level status with owners, decisions needed, risks, and next role/action.

## Output Contract

Every cross-role coordination output should include:

- Objective and scope.
- Role ownership table.
- Artifact dependency/handoff table.
- Evidence/citation cut-off.
- Approval gates and blockers.
- Recommended next role actions.
- Boundary statement: coordinator does not own or approve specialist outputs.

## MCP/RAG/LLM Guidance

- Prefer `eksad.fast` for triage and `eksad.default`/`eksad.reasoning` for ambiguous routing.
- Use RAG only through approved corpus/policy boundaries.
- Use MCP only if configured and allowed; otherwise ask for exported evidence.
- Never treat tool availability as authority to approve or execute.

## Verification Checklist

- [ ] Accountable owner identified for each artifact/decision.
- [ ] Specialist boundaries respected.
- [ ] Approval/runtime gates visible.
- [ ] Evidence gaps marked instead of invented.
- [ ] Next action is attributable to a role or human gate.
