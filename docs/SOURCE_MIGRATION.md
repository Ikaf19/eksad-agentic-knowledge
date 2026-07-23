# Source Migration Notes

## Origin

Initial repository content is curated from the previous brainstorming/source clone:

```text
~/.hermes/knowledge/eksad/
```

Previous source included:

```text
EKSAD/gpt/                  # imported
role-system-instructions/   # imported into agent-adapters/hermes/
hermes-skills/              # imported into agent-adapters/hermes/
scripts/                    # imported into agent-adapters/hermes/
per-role-knowledge-index.md # imported into agent-adapters/hermes/
TIA/                        # intentionally excluded
USED-CAR/                   # intentionally excluded
```

## Exclusions

`TIA/` and `USED-CAR/` are not part of the initial curated base repository because they are project-specific or on hold. They can be activated later via explicit project-specific migration.

## New split

This repository introduces:

- `portable/` for agent-agnostic knowledge.
- `agent-adapters/hermes/` for Hermes-specific runtime adapter files.
- `portable/mcp/` for MCP capability governance.
- `agent-adapters/hermes/mcp/` for Hermes MCP examples/templates/scripts.

## Migration status

| Migration item | Current status |
|---|---|
| Normalize portable role cards against `EKSAD/gpt/*` | Completed for the 13-role baseline; validators enforce coverage. |
| Make Hermes skills reference portable workflows | Partial: portable workflows exist for all current specialist domains and Phase E role skills link explicitly. Legacy role skills still require reference normalization; adapters must not override portable policy meanwhile. |
| Update Hermes resync for curated layout | Completed; the source script accepts the curated repository root and maps all 13 roles. Runtime apply remains a separate approval. |
| Add portable/adapter consistency validators | Completed for current role, source, roadmap, Portal, MCP, RAG, and LLM scopes. |
| Add future adapters | Still future work; add only after portable contracts remain stable and a runtime has been explicitly selected. |

Historical references to the former source remain valid only as provenance. All new operational setup must use `github.com/Ikaf19/eksad-agentic-knowledge` branch `main`.
