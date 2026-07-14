# Hermes Adapter — RAG

This adapter points Hermes users to the portable RAG foundation in `rag/`.

- Desired-state manifests: `rag/corpora/*.manifest.json`
- Policy: `portable/policies/rag-policy.md`
- Role matrix: `portable/rag/corpus-matrix.md`
- Hermes example config: `rag/adapters/hermes/retrieval-config.example.yaml`
- RAG API/MCP example config: `agent-adapters/hermes/rag/mcp-rag-api.example.yaml`
- Profile tool policy: `agent-adapters/hermes/rag/profile-tool-policy.md`
- Role usage matrix: `agent-adapters/hermes/rag/role-usage-matrix.md`

Preferred runtime path after explicit approval:

```text
Hermes role profile
  -> EKSAD RAG retrieval workflow skill
  -> rag-api-readonly MCP server
  -> RAG API
  -> Milvus + Ollama embeddings + MinIO artifact metadata
```

Do not enable a RAG runtime until the user explicitly approves runtime apply.
