# Install Plan — RAG API Readonly MCP

This is a desired-state install plan, not an executed setup.

1. Confirm RAG API endpoint and auth mode.
2. Select transport:
   - HTTP MCP endpoint: set `RAG_API_MCP_URL` and `RAG_API_MCP_TOKEN`.
   - Local stdio wrapper: install approved wrapper binary/script under `/opt/eksad-mcp/bin/rag-api-readonly`.
3. Store runtime secrets outside Git, e.g. Hermes `.env` or a deployment secret manager.
4. Add Hermes MCP config from `adapters/hermes.example.yaml` to the target profile only after approval.
5. Restart Hermes and verify `rag_healthcheck`.
6. Run role-boundary tests before allowing project-specific corpora.
