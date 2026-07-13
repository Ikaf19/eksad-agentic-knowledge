# MCP Runtime Adapter Guidance

This folder explains how `mcp/servers/*/manifest.json` should be mapped into runtime-specific MCP/tool configuration.

## Hermes

Use:

```bash
python3 mcp/scripts/render-hermes-config.py <server-id>...
```

Then manually merge the snippet into `~/.hermes/config.yaml` only after approval.

## Generic agentic harness

A generic harness should read each `manifest.json` and preserve:

- `id`
- `capabilities`
- `roles`
- `env_contract`
- `runtime.transport`
- `hermes_config` only as an example if the target harness also uses MCP stdio/HTTP.

Do not assume Hermes naming conventions in a non-Hermes runtime.
