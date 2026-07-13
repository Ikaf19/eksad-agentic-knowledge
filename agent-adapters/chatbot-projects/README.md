# Chatbot Project Adapters

This adapter family covers document-centric chatbot project environments such as:

- GPT Project / ChatGPT Projects
- Claude Project
- Similar hosted chatbot workspaces where knowledge files are uploaded/attached

These adapters are intentionally **non-agentic by default**:

- No MCP runtime assumed.
- No shell/filesystem execution assumed.
- No Git write assumed.
- Evidence must be provided by the user or exported from external systems.

Use these adapters when you want EKSAD to work “seperti sedia kala” in chatbot projects while keeping the same canonical knowledge as fully agentic runtimes.

## Folder guide

| Path | Purpose |
|---|---|
| `gpt-project/` | GPT Project / ChatGPT Project setup instructions. |
| `claude-project/` | Claude Project setup instructions. |
| `shared/` | Shared chatbot project rules. |

## Relationship to portable layer

Chatbot project instructions should reference:

- `EKSAD/gpt/`
- `portable/roles/`
- `portable/workflows/`
- `portable/policies/`
- `portable/mcp/` as governance reference only

They should not reference Hermes-only runtime paths or commands.
