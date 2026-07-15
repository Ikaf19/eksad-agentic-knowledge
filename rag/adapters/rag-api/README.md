# RAG API Adapter

This adapter describes the generic RAG API client contract for Hermes, MCP wrappers, and other agentic harnesses.

## Required environment variables for runtime implementations

- `RAG_API_BASE_URL` — base URL of the RAG API.
- `RAG_API_TOKEN` — runtime token used by the MCP wrapper or REST adapter. Do not commit real values.

## Recommended headers

```text
Authorization: Bearer ${RAG_API_TOKEN}
X-EKSAD-Role: <role-id>
X-EKSAD-Session: <session-id>
X-EKSAD-Tenant: <tenant-id when available>
```

## Client contract

See `client-contract.example.json` for a runtime-neutral client binding shape.
