# Install Plan — PostgreSQL Schema Read-only MCP

## Gate

Do not install or enable this MCP server until the user explicitly approves runtime setup.

## Runtime location

Recommended binary/package location:

```text
/opt/eksad-mcp/bin/postgres-schema-readonly
```

This path is local runtime state and must not be committed.

## Environment contract

- `POSTGRES_SCHEMA_READONLY_URL` — required=true, secret=true: Read-only/schema-only PostgreSQL connection URL.

## Steps

1. Read `manifest.json` and `security.md`.
2. Confirm this server is allowed for the active role/task.
3. Install the approved MCP server implementation outside Git.
4. Create local env variables/secrets outside Git.
5. Render adapter config:

```bash
python3 mcp/scripts/render-hermes-config.py postgres-schema-readonly
```

6. Review output manually.
7. Apply to live runtime only after approval.
8. Restart/reload runtime and run validation checklist.
