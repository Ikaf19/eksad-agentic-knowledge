# RAG Architecture

## Goal

Make EKSAD knowledge searchable with citation-backed retrieval while keeping Git as source of truth and runtime indexes disposable.

## Components

```text
Git source-of-truth
  ├─ EKSAD/gpt/                 # canonical standards/templates/role pack
  ├─ portable/                  # runtime-neutral role/workflow/policy layer
  ├─ mcp/                       # MCP desired-state catalog
  └─ rag/                       # RAG desired-state catalog

RAG runtime (not committed)
  ├─ corpus loader
  ├─ chunker
  ├─ embedder
  ├─ vector store / lexical index
  ├─ optional reranker
  └─ retrieval API / MCP / agent adapter
```

## Design principles

1. **Git is canonical; indexes are rebuildable.** If an index disagrees with Git, rebuild the index.
2. **Citation-first.** Retrieved answers must cite repository paths and, where possible, section headings.
3. **Role-scoped retrieval.** A role may only retrieve corpora allowed by manifest and policy.
4. **Project activation is explicit.** TIA/USED-CAR/customer-specific corpora are excluded unless activated by project manifest.
5. **No runtime secrets in Git.** Embedding/gateway credentials live in local env or secret manager.
6. **Adapters do not own knowledge.** Hermes, generic harnesses, and chatbot projects consume the same manifests.

## RAG modes

| Mode | Retrieval source | Runtime requirement | Notes |
|---|---|---|---|
| Chatbot Project | Native platform project search over uploaded files | None | Upload bundle guidance only; no custom vector DB assumed. |
| Hermes local | Local/external RAG service or MCP retrieval server | Explicit runtime setup | Use manifests to build index; apply config only after approval. |
| Generic harness | OpenAI-compatible retrieval API, MCP, or local library | Harness-specific | Must honor corpus manifests and citations. |
| Hybrid | Chatbot for drafting + Hermes for evidence | Optional | Use citations to transfer evidence between modes. |

## Source precedence during retrieval conflicts

1. Project-specific approved documents for the active project.
2. `portable/policies/` and `portable/rag/` governance.
3. `EKSAD/gpt/_base/` canonical standards.
4. `EKSAD/gpt/_template/` templates.
5. Role-specific instructions.
6. Runtime adapter guidance.

If two sources conflict and precedence does not resolve it, the agent must surface the conflict instead of choosing silently.
