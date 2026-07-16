# Portable EKSAD Knowledge Layer

This directory is the runtime-neutral layer. It should be usable by Hermes, Claude Code, Codex, Cursor, OpenCode, ChatGPT/Claude Projects, or a custom agent.

Portable docs may reference EKSAD standards and templates, but must avoid Hermes-only concepts such as:

- `SOUL.md`
- `skill_view`
- `~/.hermes/...`
- Hermes profile commands
- Hermes MCP tool prefixes
- Hermes cron/kanban/gateway commands

## Subdirectories

| Path | Purpose |
|---|---|
| `roles/` | Canonical role cards, ownership boundaries, and `role-collaboration-matrix.md`. |
| `workflows/` | Runtime-neutral workflow contracts. |
| `deliverables/` | Deliverable contracts and matrix. |
| `policies/` | Role, approval, security, MCP, RAG, and LLM gateway policies. |
| `mcp/` | MCP capability catalog, server catalog, role matrix, environment/migration contracts. |
| `rag/` | Runtime-neutral corpus matrix, retrieval workflow, and RAG API/MCP policy. |
| `llm-gateway/` | Runtime-neutral model alias, role matrix, and routing policy. |

## Rule

Adapters must depend on this portable layer. The portable layer must not depend on any adapter.
