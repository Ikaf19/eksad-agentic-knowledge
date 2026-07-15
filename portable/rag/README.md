# Portable RAG Layer

Runtime-neutral retrieval policy for EKSAD knowledge.

This layer defines role/corpus boundaries and retrieval behavior without assuming Hermes, LiteLLM, a specific vector DB, or a specific MCP server.

| File | Purpose |
|---|---|
| `corpus-matrix.md` | Role-to-corpus retrieval matrix. |
| `retrieval-policy.md` | Runtime-neutral retrieval rules. |
| `../workflows/rag-retrieval-workflow.md` | Runtime-neutral role-agent workflow for retrieval/citation/abstention. |

Top-level `rag/` contains desired-state manifests, RAG API/MCP contracts, adapters, scripts, and evaluation fixtures.
