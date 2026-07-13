# Validation — RabbitMQ Read-only MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py rabbitmq-readonly > /tmp/rabbitmq-readonly.hermes.yaml
```

Review `/tmp/rabbitmq-readonly.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test rabbitmq_readonly
```

Expected result:

- Server appears as `rabbitmq_readonly`.
- Tools are discovered with `mcp_rabbitmq_readonly_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
