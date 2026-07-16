# EKSAD Agentic Knowledge

Curated, Git-backed source of truth for EKSAD AI-assisted delivery.

This repository separates **portable agent-agnostic knowledge** from **runtime-specific adapters** so the same EKSAD roles, workflows, templates, MCP/RAG governance, and model gateway policies can be used by Hermes today and by other agentic runtimes later.

## Repository layers

```text
Level 1 — Portable / agent-agnostic source of truth
  EKSAD/gpt/                  # canonical EKSAD standards/templates/role source pack
  portable/roles/             # runtime-neutral role cards
  portable/workflows/         # runtime-neutral workflow contracts
  portable/deliverables/      # deliverable contracts and matrix
  portable/policies/          # security, role, approval, MCP/RAG/LLM gateway policy
  portable/mcp/               # MCP capability catalog and role matrix
  portable/rag/               # RAG corpus matrix and retrieval policy
  portable/llm-gateway/       # runtime-neutral model alias and routing policy

Level 1.5 — Desired-state capability catalogs
  mcp/                         # MCP desired-state catalog and setup flow
  rag/                         # RAG corpus/API/tool contracts, indexing/retrieval/citation policy, eval fixtures
  llm-gateway/                 # model alias/routing/budget/guardrail desired-state catalog

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
  live LiteLLM/gateway config, DBs, logs, provider keys
```

## What this repo is

- Canonical EKSAD knowledge source for agentic delivery.
- Agent-agnostic role, workflow, deliverable, policy, MCP, RAG, and LLM gateway governance layer.
- Canonical role baseline with 13 role profiles, including Data Analyst, Data Scientist, UI/UX Designer, and Content Creator.
- RAG API/MCP desired-state contracts for future Milvus/Ollama/MinIO-backed retrieval.
- LLM Gateway desired-state contracts for LiteLLM/OpenAI-compatible model routing.
- Runtime adapter source for Hermes.
- Migration-safe foundation for future adapters, retrieval systems, and model gateways.

## What this repo is not

- Not a place for real secrets, tokens, passwords, or connection strings.
- Not a live runtime config directory.
- Not a build machine or application source repository.
- Not a project-specific TIA/USED-CAR deliverable repository unless explicitly activated later.

## Current navigation

Use the roadmap docs below as the current source-of-truth navigation. Historical bootstrap details remain in `docs/GRAND_PLAN.md`, but the current baseline is summarized in `docs/ROADMAP.md`.

See:

- `docs/ROADMAP.md` — current canonical roadmap and baseline status
- `docs/PHASE_HISTORY.md` — historical phase/merge record
- `docs/NEXT_PHASE_CANDIDATES.md` — candidate next active phases
- `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` — parked Web Portal future alignment plan
- `docs/GRAND_PLAN.md` — historical initial grand plan and execution log
- `docs/SOURCE_MIGRATION.md`
- `docs/USAGE_MODES.md`
- `portable/README.md`
- `portable/mcp/role-mcp-matrix.md`
- `rag/README.md`
- `rag/RAG_API_CONTRACT.md`
- `mcp/servers/rag-api-readonly/README.md`
- `llm-gateway/README.md`
- `llm-gateway/aliases/eksad-model-aliases.json`
- `portable/llm-gateway/role-model-matrix.md`
- `portable/rag/corpus-matrix.md`
- `scripts/validate-role-coverage.py`
- `eval/roles/role-expansion-tests.json`
- `agent-adapters/hermes/README.md`
- `agent-adapters/chatbot-projects/README.md`

## Safety rules

1. Git stores knowledge, policy, examples, templates, and validators.
2. Git does **not** store runtime state or secrets.
3. MCP is capability-governed, role-scoped, and read-only by default.
4. RAG is citation-governed, role-scoped, API-mediated, and index-off by default.
5. Hermes should access RAG through an approved RAG API/MCP boundary, not direct Milvus/MinIO/Ollama credentials.
6. LLM routing is alias-governed; role agents request `eksad.*` capability aliases, not provider-specific model names.
7. Provider API keys, LiteLLM master keys, live gateway config, and raw prompt/response logs are runtime state, never Git state.
8. Hermes-specific files must not become the only source of role/workflow truth.
9. Portable docs must not depend on Hermes-only paths or commands.


## MCP foundation

Top-level MCP desired-state catalog and setup flow: `mcp/README.md`.

## RAG foundation

Top-level RAG desired-state catalog, corpus manifests, retrieval/citation policy, RAG API contract, MCP `rag-api-readonly` wrapper contract, and evaluation fixtures: `rag/README.md`.

## LLM Gateway foundation

Top-level LLM Gateway desired-state catalog, stable EKSAD model aliases, LiteLLM reference examples, OpenAI-compatible adapter guidance, budget/routing/guardrail policy, and validators: `llm-gateway/README.md`.


## Current role baseline

Canonical role coverage now includes 13 role profiles:

```text
general-coordinator, business-analyst, system-analyst, technical-leader,
developer-backend, developer-frontend, qa-engineer, project-manager,
devops-engineer, data-analyst, data-scientist, ui-ux-designer,
content-creator
```

The role expansion adds portable role cards, workflows, deliverables, Hermes role system instructions, Hermes SKILL.md templates, and MCP/RAG/LLM matrix coverage for Data Analyst, Data Scientist, UI/UX Designer, and Content Creator. Phase F further hardens routing, skill enrichment, collaboration, RAG/MCP/LLM matrices, and validators.

## Future Alignment

Web Portal / Admin Control Panel / Landing Page work is parked as a future alignment plan, not as the next reserved phase:

- `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md`

Start it only after explicit selection of `NEXT-06` / `WPC-01`; the plan itself does not approve runtime deployment, Keycloak mutation, LiteLLM key creation, provider-key storage, or live runtime activation.
