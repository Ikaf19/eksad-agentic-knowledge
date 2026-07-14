# Chunking Profiles

RAG chunking must preserve document structure and traceability. Do not use a single naive token splitter for every file type.

| Profile | Intended files | Strategy | Notes |
|---|---|---|---|
| `markdown-headers` | Standards, policies, workflows | Split by heading hierarchy; include parent headings in metadata. | Default for `_base` and `portable`. |
| `template-preserve` | BRD/FSD/TSD/regulatory templates | Preserve top-level sections and numbering; avoid splitting requirement tables mid-row. | Templates are output contracts. |
| `role-instruction` | Role system instructions | Keep mission, boundaries, handoffs, and output style together. | Avoid separating “does not own” boundaries. |
| `manifest-json` | MCP/RAG/gateway manifests | Chunk by JSON object or whole file if small. | Preserve keys and ids. |
| `code-like-config` | YAML/JSON examples, config snippets | Keep code blocks intact. | Do not embed real secrets. |
| `project-deliverable` | Future BRD/FSD/TSD project docs | Split by numbered sections and traceability IDs. | Only after project activation. |

## Metadata every chunk should carry

```json
{
  "source_path": "EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md",
  "corpus_id": "eksad-core",
  "chunk_profile": "markdown-headers",
  "heading_path": ["Architecture Principles", "Tenant Isolation"],
  "git_commit": "<runtime-resolved-sha>",
  "sensitivity": "internal",
  "allowed_roles": ["system-analyst", "technical-leader"]
}
```

## Chunk size guidance

- Start with 600–1,200 tokens for prose standards.
- Keep templates larger if sections are tightly coupled.
- Use reranking rather than over-small chunks when precision is low.
- Always prefer correct citation over aggressive compression.
