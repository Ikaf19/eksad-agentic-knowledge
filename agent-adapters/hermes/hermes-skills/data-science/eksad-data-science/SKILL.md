---
name: eksad-data-science
description: "Use when the Data Scientist profile must frame an ML/statistical problem, design an experiment, evaluate a model, or produce an ML experiment report. Enforces baseline comparison, leakage/risk review, reproducibility notes, and no production deployment."
version: 1.0.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, data-science, workflow, role-expansion]
    related_skills: [multi-role-agent-setup]
---

# EKSAD Data Science Skill

Hermes adapter workflow for EKSAD data science work. This skill wraps the portable workflow while keeping Git as source of truth and runtime tool usage optional.

## When to Use

- User asks for data science deliverables or review.
- User provides source material and asks for structured analysis/spec/content.
- User asks the corresponding Phase E role agent to produce its standard output.

## When NOT to Use

- Request requires another role's authority; produce a handoff note instead.
- Request requires production mutation, external publication, model deployment, or approval authority not granted by the user.
- Request asks for secrets, unrestricted customer PII extraction, or unsupported claims.

## Source References

Read before working when available:

- `portable/workflows/data-science-workflow.md`
- `portable/deliverables/ml-experiment-report.md`
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

## Phase F Enrichment — MLE and Evaluation Patterns

Adapted benchmark patterns: MLE workflow, benchmark-methodology, eval-harness.

- Frame problem type, baseline, success metric, validation split, leakage risk, fairness/privacy concerns, and rollback criteria before experiment design.
- Use notebook sandbox only when explicitly configured and approved; otherwise provide reproducible pseudo-steps and data requirements.
- Model evaluation evidence is not production approval; hand off productionization to SA/TL/DevOps/business authority.
- Record assumptions, dataset cut-off, metric confidence, and failure modes in every ML experiment report.
