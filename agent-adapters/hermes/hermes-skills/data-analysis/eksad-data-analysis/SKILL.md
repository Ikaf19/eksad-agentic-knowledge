---
name: eksad-data-analysis
description: "Use when the Data Analyst profile must define KPIs, analyze data evidence, profile data quality, or draft dashboard/report specifications. Enforces read-only evidence, explicit metric formulas, source citations, and no production data mutation."
version: 1.0.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, data-analysis, workflow, role-expansion]
    related_skills: [multi-role-agent-setup]
---

# EKSAD Data Analysis Skill

Hermes adapter workflow for EKSAD data analysis work. This skill wraps the portable workflow while keeping Git as source of truth and runtime tool usage optional.

## When to Use

- User asks for data analysis deliverables or review.
- User provides source material and asks for structured analysis/spec/content.
- User asks the corresponding Phase E role agent to produce its standard output.

## When NOT to Use

- Request requires another role's authority; produce a handoff note instead.
- Request requires production mutation, external publication, model deployment, or approval authority not granted by the user.
- Request asks for secrets, unrestricted customer PII extraction, or unsupported claims.

## Source References

Read before working when available:

- `portable/workflows/data-analysis-workflow.md`
- `portable/deliverables/data-analysis-report.md`
- `portable/deliverables/dashboard-spec.md`
- `portable/policies/role-boundaries.md`
- `portable/policies/approval-gates.md`
- `portable/rag/corpus-matrix.md`
- `portable/mcp/role-mcp-matrix.md`
- `portable/llm-gateway/role-model-matrix.md`

## Workflow

1. Confirm the request, audience, source material, and approval owner.
2. Retrieve/read approved context only. If RAG/MCP tools are configured, use them only within the role matrix.
3. Mark missing evidence as `[SOURCE GAP]`, `[DATA GAP]`, or `[CLARIFY]` with owner and impact.
4. Produce the relevant deliverable using the portable contract.
5. Run a self-check for role boundary, evidence, approval gate, and publication/deployment risk.
6. End with handoff notes and next-step options.

## Output Requirements

- Cite source paths or provided artifact names for factual claims.
- Separate facts, assumptions, analysis/recommendation, and required approvals.
- Use Markdown tables/checklists where they improve review.
- Never present draft output as approved/final without explicit approval.

## Common Pitfalls

1. Treating tool access as role authority. Tool access only supplies evidence.
2. Filling missing facts with plausible content. Mark gaps instead.
3. Skipping approval owner for sensitive or externally visible artifacts.
4. Mixing specialist responsibilities; hand off rather than taking over.

## Verification Checklist

- [ ] Correct portable workflow was followed.
- [ ] Deliverable contract sections are present or gaps are explained.
- [ ] Evidence/citations are included for factual claims.
- [ ] Role boundary and approval gates are respected.
- [ ] Runtime actions remain read-only unless explicitly approved.
