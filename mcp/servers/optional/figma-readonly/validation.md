# Validation — Figma Read-only MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py figma-readonly > /tmp/figma-readonly.hermes.yaml
```

Review `/tmp/figma-readonly.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test figma_readonly
```

Expected result:

- Server appears as `figma_readonly`.
- Tools are discovered with `mcp_figma_readonly_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
