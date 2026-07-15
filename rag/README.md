# EKSAD RAG Foundation

This folder is the canonical **retrieval-augmented generation (RAG) desired-state** entrypoint for the EKSAD Agentic Knowledge repository.

It defines how this Git knowledge source may be indexed, retrieved, cited, evaluated, and adapted into Hermes or other agentic harnesses. Phase C enriches this with a read-only RAG API and MCP tool contract for future Milvus/Ollama/MinIO-backed retrieval. It does **not** contain runtime indexes, embeddings, vector databases, API keys, or live service configuration.

## Layering

```text
rag/                         # discoverable RAG desired-state catalog and setup flow
portable/rag/                # runtime-neutral RAG policy/matrix for all adapters
portable/policies/rag-policy.md
agent-adapters/hermes/rag/   # Hermes-specific guidance/snippets only
agent-adapters/chatbot-projects/ # upload/search fallback mode
```

## What belongs here

- Corpus manifests that say what may be indexed.
- Chunking, retrieval, citation, and security contracts.
- RAG API, tool, auth/RBAC, runtime component, query pipeline, evidence, failure-mode, and observability contracts.
- Desired-state MCP wrapper contract for `rag-api-readonly`.
- Role retrieval boundaries.
- Read-only validation and ingestion-plan scripts.
- Evaluation fixtures for citations, abstention, and role boundaries.
- Adapter examples for Hermes, generic harnesses, and chatbot projects.

## What does not belong here

- Vector databases (`*.lancedb`, Qdrant/Chroma directories, pgvector dumps).
- Embedding caches or reranker caches.
- Provider API keys or LiteLLM master keys.
- Customer/project-private raw dumps.
- Live `~/.hermes/config.yaml`, live RAG server config, or runtime logs.

## Quick navigation

| Need | Start here |
|---|---|
| Understand architecture | `ARCHITECTURE.md` |
| Corpus schema | `CORPUS_MANIFEST_SCHEMA.md` |
| What can be indexed | `corpora/*.manifest.json` |
| Chunking profiles | `CHUNKING_PROFILES.md` |
| Retrieval rules | `RETRIEVAL_CONTRACT.md` |
| RAG API contract | `RAG_API_CONTRACT.md` and `openapi/rag-api.openapi.yaml` |
| RAG MCP/tool contract | `RAG_TOOL_CONTRACT.md` and `../mcp/servers/rag-api-readonly/` |
| Runtime components | `RAG_RUNTIME_COMPONENTS.md` |
| Auth/RBAC | `RAG_AUTH_AND_RBAC.md` |
| Citation rules | `CITATION_POLICY.md` |
| Security model | `SECURITY_MODEL.md` |
| Evaluation plan | `EVALUATION_PLAN.md` and `../eval/rag/` |
| Validate corpora | `scripts/validate-rag-corpus.py` |
| Validate API/tool contracts | `scripts/validate-rag-api-contract.py` |
| Render ingestion plan | `scripts/render-ingestion-plan.py` |
| Render RAG MCP summary | `scripts/render-rag-mcp-manifest.py` |

## Current status

This folder is **setup-ready as desired-state documentation and templates**. Runtime indexing and runtime RAG API/MCP activation are separate explicit approval gates.

Recommended future runtime shape:

```text
Hermes role profile
  -> EKSAD RAG retrieval skill
  -> rag-api-readonly MCP server
  -> RAG API
  -> Milvus + Ollama embeddings + MinIO artifact metadata
```
