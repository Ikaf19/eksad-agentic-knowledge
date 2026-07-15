# RAG Retrieval Workflow

Use this workflow when an EKSAD role agent needs source-backed evidence from the knowledge base.

## Steps

1. Determine whether the task needs retrieval.
2. Identify the active role and allowed corpus scope.
3. Query RAG with `citation_required=true`.
4. Inspect result confidence, source path, sensitivity, and citation metadata.
5. If results conflict, present the conflict with citations.
6. If results are empty/low-confidence, abstain or ask for missing source material.
7. Use retrieved evidence only with citation metadata.

## Role boundary

Do not query project-specific corpora unless explicitly activated for the current project/tenant.

## Output rule

Any source-backed claim must include a source path or citation reference. If citations are unavailable, mark the answer as assumption-based or ask for more evidence.
