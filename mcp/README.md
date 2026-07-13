# EKSAD MCP Foundation

This folder is the **canonical MCP entrypoint** for the EKSAD Agentic Knowledge repository.

It is designed to work in two ways:

1. **Portable / agentic-harness neutral** — any future agent runtime can read this folder to understand desired MCP capabilities, security posture, server candidates, and setup phases.
2. **Hermes adapter** — Hermes-specific rendering uses `agent-adapters/hermes/mcp/` and the server adapter examples under each `mcp/servers/*/adapters/` directory.

## Layering

```text
mcp/                         # discoverable desired-state MCP catalog and setup flow
portable/mcp/                # canonical policy/capability matrix used by all adapters
agent-adapters/hermes/mcp/   # Hermes-specific config examples and helper scripts
agent-adapters/generic/      # generic non-Hermes harness guidance
```

## What belongs here

- MCP roadmap P0–Pn.
- Server manifests and install plans.
- Security model and environment contract.
- Role/profile MCP boundary docs.
- Scripts that validate or render config snippets.
- Adapter examples for Hermes and generic harnesses.

## What does not belong here

- Real secrets or tokens.
- Live `~/.hermes/config.yaml`.
- Downloaded MCP binaries.
- `node_modules`, `uv` caches, `.codebase-memory/` indexes, DB/cache artifacts.
- Production write config enabled by default.

## Quick navigation

| Need | Start here |
|---|---|
| Understand MCP phases | `ROADMAP_P0_TO_PN.md` |
| Setup flow | `SETUP_FLOW.md` |
| Security model | `SECURITY_MODEL.md` |
| Server catalog | `servers/` |
| Role access boundaries | `profiles/` |
| Validate catalog | `scripts/validate-mcp-catalog.py` |
| Render Hermes config snippet | `scripts/render-hermes-config.py` |

## Current status

This folder is **setup-ready as desired-state documentation and template**, not an auto-installer. Runtime apply is a separate explicit approval gate.
