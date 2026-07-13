# Install Plan — Kafka Read-only MCP

## Gate

Do not install or enable this MCP server until the user explicitly approves runtime setup.

## Runtime location

Recommended binary/package location:

```text
/opt/eksad-mcp/bin/kafka-readonly
```

This path is local runtime state and must not be committed.

## Environment contract

- `KAFKA_READONLY_BOOTSTRAP` — required=true, secret=true: Read-only bootstrap/credential contract.

## Steps

1. Read `manifest.json` and `security.md`.
2. Confirm this server is allowed for the active role/task.
3. Install the approved MCP server implementation outside Git.
4. Create local env variables/secrets outside Git.
5. Render adapter config:

```bash
python3 mcp/scripts/render-hermes-config.py kafka-readonly
```

6. Review output manually.
7. Apply to live runtime only after approval.
8. Restart/reload runtime and run validation checklist.
