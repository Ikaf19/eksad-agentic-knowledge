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

## Next migration work

1. Normalize portable role cards against `EKSAD/gpt/*` source files.
2. Make Hermes skills reference portable workflows instead of duplicating policy.
3. Update Hermes resync scripts for this new repo layout.
4. Add validators for portable/adapters consistency.
5. Add future adapters only after portable layer stabilizes.
