---
name: eksad-rag-retrieval-workflow
description: Use when an EKSAD Hermes role agent needs source-backed retrieval from the RAG system; defines when to search, cite, abstain, and respect role/corpus boundaries.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [eksad, rag, retrieval, citations, role-boundary]
    related_skills: [agentic-knowledge-repositories, native-mcp]
---

# EKSAD RAG Retrieval Workflow

## Overview

This skill governs how EKSAD role agents use a future RAG system. It is a behavior policy, not a runtime connector. Runtime calls should go through the `rag-api-readonly` MCP server or an approved read-only RAG API tool.

## When to Use

Use this skill when:

- drafting BRD/FSD/TSD/test plans from EKSAD standards
- checking architecture, API, ERD, coding, QA, DevOps, or governance rules
- validating claims against source-of-truth documents
- resolving conflicts between role instructions and base standards
- producing source-backed answers that need citations

Do not use this skill to:

- index corpora
- rebuild vector stores
- access project/customer corpora without activation
- fetch secrets or raw storage credentials

## Workflow

1. Identify the active role and task type.
2. Decide whether retrieval is required. Retrieval is required for policy, standards, architecture, compliance, or project-specific factual claims.
3. Select only allowed corpora for the role.
4. Call the RAG tool with `citation_required=true`.
5. Verify every result includes `source_path`, `citation`, `corpus_id`, `sensitivity`, and score.
6. If retrieval is empty or low confidence, abstain or ask the user for source material.
7. If retrieved sources conflict, present the conflict with citations and route to TL/human approval if decision-impacting.
8. In final output, cite source paths for evidence-backed claims.

## Role Notes

- BA: use RAG for BRD/FSD evidence, glossary, rules, and acceptance criteria.
- System Analyst: use RAG for TSD, ERD, API contract, integration, and architecture decisions.
- Developer Backend/Frontend: use RAG for coding standards, module patterns, and API contract evidence.
- QA: use RAG for test plan, RTM, acceptance criteria, and evidence references.
- DevOps: use RAG for CI/CD, observability, release, and infrastructure runbook references.
- Technical Leader: use RAG for cross-role review and governance checks.
- General Coordinator: use RAG only for task routing/context unless delegated to a specialist role.

## Citation Format

Prefer concise citations:

```text
[source: EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md#tenant-isolation]
```

If line ranges are available:

```text
[source: EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md:L10-L24]
```

## Abstention

If the RAG tool returns `abstain=true`, do not invent source-backed facts. Say what is missing and ask for evidence or approval to proceed with assumptions.

## Common Pitfalls

1. Treating RAG snippets as authoritative without citation metadata.
2. Querying project-specific corpora before activation.
3. Using RAG to perform indexing or write operations.
4. Hiding evidence conflicts instead of escalating them.
5. Giving Hermes direct Milvus/MinIO credentials instead of using the RAG API boundary.

## Verification Checklist

- [ ] Role is identified.
- [ ] Corpus scope is allowed.
- [ ] Retrieval result includes citations.
- [ ] Low-confidence results trigger abstention.
- [ ] Project/customer corpora are activated before use.
- [ ] Final answer distinguishes source-backed facts from assumptions.
