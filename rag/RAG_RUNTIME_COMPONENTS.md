# RAG Runtime Components

Phase C documents the target runtime shape from the architecture baseline. It does not deploy it.

## Component map

| Component | Responsibility | Git content | Runtime state |
|---|---|---|---|
| Knowledge source | Markdown specs, standards, templates, code references | corpus manifests, path rules | repo checkout |
| RAG API | Retrieval service boundary | OpenAPI contract, client examples | service process, audit logs |
| Milvus | Vector store / ANN retrieval | adapter notes only | indexes, vectors |
| Ollama embedding | Local embedding model endpoint | adapter notes only | model cache/runtime |
| MinIO | Artifact/evidence metadata and object storage | bucket naming policy only | object buckets |
| MCP rag-api-readonly | Standard agent tool wrapper | manifest/examples | MCP service config |
| Hermes | Role agent runtime | profile/tool policy templates | live config outside Git |

## Runtime boundary

Hermes should not receive direct Milvus credentials. Hermes should not receive broad MinIO credentials. Hermes should not build embeddings directly by default. The RAG API owns those runtime integrations.

## Data flow

```text
Question/task
  -> role-specific RAG skill decides retrieval need
  -> Hermes calls MCP RAG tool
  -> MCP wrapper forwards to RAG API
  -> RAG API filters corpora by role/project policy
  -> RAG API embeds query and retrieves from Milvus
  -> RAG API resolves source/citation and artifact metadata
  -> Hermes receives cited evidence
  -> role agent writes answer/spec/review with citations
```
