# Validation — Kafka Read-only MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py kafka-readonly > /tmp/kafka-readonly.hermes.yaml
```

Review `/tmp/kafka-readonly.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test kafka_readonly
```

Expected result:

- Server appears as `kafka_readonly`.
- Tools are discovered with `mcp_kafka_readonly_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
