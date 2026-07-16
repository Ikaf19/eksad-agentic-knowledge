# Hermes Adapter

This directory contains Hermes-specific runtime adapter files derived from the portable EKSAD source.

## Contents

| Path | Purpose |
|---|---|
| `role-system-instructions/` | Source instructions rendered into Hermes profiles/SOUL. |
| `hermes-skills/` | Git-tracked Hermes SKILL.md workflows. |
| `scripts/` | Hermes resync/runtime helper scripts. |
| `per-role-knowledge-index.md` | Hermes-oriented role/knowledge index. |
| `mcp/` | Hermes MCP config examples, templates, doctor scripts. |
| `../../llm-gateway/adapters/hermes/` | Hermes LLM Gateway alias/provider snippet examples. |

## Boundary

This adapter may reference Hermes concepts like `SOUL.md`, SKILL.md, profiles, and `mcp_servers`. It must not become the only canonical source for role/workflow policy. Canonical role/workflow/policy lives in `portable/` and `EKSAD/gpt/`.

## Runtime sync warning

Do not run resync scripts or modify live `~/.hermes/` runtime until explicitly approved. Git commit and runtime sync are separate gates.


## Phase E roles

The Hermes adapter now includes extracted role system instructions and SKILL.md templates for:

- `data-analyst` → `eksad-data-analysis`
- `data-scientist` → `eksad-data-science`
- `ui-ux-designer` → `eksad-ui-ux-delivery`
- `content-creator` → `eksad-content-creation`

Runtime sync remains a separate approval gate; these files are desired-state adapter sources only.
