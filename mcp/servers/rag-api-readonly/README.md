# RAG API Readonly MCP

This MCP server is the preferred standard tool boundary between Hermes role agents and the EKSAD RAG API.

## Purpose

Expose read-only retrieval tools:

- `rag_search`
- `rag_retrieve`
- `rag_get_document`
- `rag_resolve_citation`
- `rag_get_artifact_metadata`
- `rag_healthcheck`

## Runtime boundary

The MCP server wraps the RAG API. It does not connect Hermes directly to Milvus, Ollama, or MinIO.

## Default posture

- `default_enabled: false`
- sampling disabled
- read-only tools only
- indexing/rebuild/delete disabled by default
- runtime activation requires explicit approval
