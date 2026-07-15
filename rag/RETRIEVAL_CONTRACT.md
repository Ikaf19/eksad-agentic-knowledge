# Retrieval Contract

This contract applies to Hermes, generic harnesses, MCP retrieval servers, and any RAG service that uses this repository.

## Required behavior

1. Retrieval results must include `source_path`.
2. Retrieval results should include `heading_path` or equivalent section locator when available.
3. Agents must cite retrieved sources in user-facing answers when using RAG evidence.
4. Role access must be checked against corpus `allowed_roles`.
5. If retrieval returns no relevant cited source, the agent must say evidence is insufficient.
6. Project-specific corpora require explicit activation and must not leak into base EKSAD answers.
7. Runtime adapters may enrich metadata but must not override corpus policy.

## Conflict handling

If retrieved sources conflict:

1. Prefer active project-specific approved docs over generic docs.
2. Prefer portable policies over adapter docs.
3. Prefer `_base` standards over role shortcuts.
4. Prefer newer approved versions only when version metadata is clear.
5. If still unresolved, report the conflict with citations.

## Minimum retrieval result shape

```json
{
  "query": "What is the tenant isolation rule?",
  "results": [
    {
      "source_path": "EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md",
      "heading_path": ["Tenant Isolation"],
      "corpus_id": "eksad-core",
      "score": 0.82,
      "text": "...",
      "git_commit": "<sha>",
      "sensitivity": "internal"
    }
  ]
}
```

## Fallback behavior

If RAG runtime is not configured:

- Hermes/generic agents should read files directly when available.
- Chatbot projects should ask the user to upload/paste the relevant evidence.
- The agent must not pretend that retrieval was performed.
