# Generic Agent Adapter

Use this adapter for any AI assistant or agentic runtime that is not yet explicitly supported.

## Pattern

1. Load `EKSAD/gpt/` as the domain standards/templates source.
2. Load `portable/roles/` for role boundaries.
3. Load `portable/workflows/` for workflow contracts.
4. Load `portable/policies/` for governance.
5. Load `portable/mcp/` for capability policy if the runtime supports tools/MCP.
6. Keep runtime secrets/config local.

## Modes

- Chatbot-only: use `agent-adapters/chatbot-projects/` guidance.
- Tool-using/agentic: use runtime-specific adapter or derive one from this generic adapter.
