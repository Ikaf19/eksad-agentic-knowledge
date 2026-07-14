# EKSAD Agentic Knowledge

Curated, Git-backed source of truth for EKSAD AI-assisted delivery.

This repository separates **portable agent-agnostic knowledge** from **runtime-specific adapters** so the same EKSAD roles, workflows, templates, and MCP governance can be used by Hermes today and by other agentic runtimes later.

## Repository layers

```text
Level 1 — Portable / agent-agnostic source of truth
  EKSAD/gpt/                  # canonical EKSAD standards/templates/role source pack
  portable/roles/             # runtime-neutral role cards
  portable/workflows/         # runtime-neutral workflow contracts
  portable/deliverables/      # deliverable contracts and matrix
  portable/policies/          # security, role, approval, MCP/RAG policy
  portable/mcp/               # MCP capability catalog and role matrix
  portable/rag/               # RAG corpus matrix and retrieval policy

Level 1.5 — Desired-state capability catalogs
  mcp/                         # MCP desired-state catalog and setup flow
  rag/                         # RAG corpus/API/tool contracts, indexing/retrieval/citation policy, eval fixtures

Level 2 — Agent adapters
  agent-adapters/hermes/      # Hermes-specific SOUL/SKILL/MCP/resync adapter
  agent-adapters/<future>/    # Claude Code, Codex, Cursor, etc.

Level 3 — Local runtime state, never committed
  ~/.hermes/config.yaml
  ~/.hermes/.env
  live MCP config
  tokens/passwords
  downloaded MCP binaries
  codebase-memory indexes/caches
  RAG vector stores / embedding caches
```

## What this repo is

- Canonical EKSAD knowledge source for agentic delivery.
- Agent-agnostic role, workflow, deliverable, policy, MCP, and RAG governance layer.
- RAG API/MCP desired-state contracts for future Milvus/Ollama/MinIO-backed retrieval.
- Runtime adapter source for Hermes.
- Migration-safe foundation for future adapters, retrieval systems, and model gateways.

## What this repo is not

- Not a place for real secrets, tokens, passwords, or connection strings.
- Not a live runtime config directory.
- Not a build machine or application source repository.
- Not a project-specific TIA/USED-CAR deliverable repository unless explicitly activated later.

## Initial scope

The initial commit imports the EKSAD GPT pack and Hermes adapter artifacts from the prior brainstorming/source repository, while adding a portable layer and MCP grand plan.

See:

- `docs/GRAND_PLAN.md`
- `docs/SOURCE_MIGRATION.md`
- `docs/USAGE_MODES.md`
- `portable/README.md`
- `portable/mcp/role-mcp-matrix.md`
- `rag/README.md`
- `rag/RAG_API_CONTRACT.md`
- `mcp/servers/rag-api-readonly/README.md`
- `portable/rag/corpus-matrix.md`
- `agent-adapters/hermes/README.md`
- `agent-adapters/chatbot-projects/README.md`

## Safety rules

1. Git stores knowledge, policy, examples, templates, and validators.
2. Git does **not** store runtime state or secrets.
3. MCP is capability-governed, role-scoped, and read-only by default.
4. RAG is citation-governed, role-scoped, API-mediated, and index-off by default.
5. Hermes should access RAG through an approved RAG API/MCP boundary, not direct Milvus/MinIO/Ollama credentials.
6. Hermes-specific files must not become the only source of role/workflow truth.
7. Portable docs must not depend on Hermes-only paths or commands.


## MCP foundation

Top-level MCP desired-state catalog and setup flow: `mcp/README.md`.

## RAG foundation

Top-level RAG desired-state catalog, corpus manifests, retrieval/citation policy, RAG API contract, MCP `rag-api-readonly` wrapper contract, and evaluation fixtures: `rag/README.md`.
