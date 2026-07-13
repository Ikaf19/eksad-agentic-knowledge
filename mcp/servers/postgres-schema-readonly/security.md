# Security — PostgreSQL Schema Read-only MCP

## Risk

`high`

## Default

This server is not enabled by default.

## Required controls

- Use least privilege credentials.
- Keep real env values outside Git.
- Disable sampling unless explicitly reviewed.
- Scope network/filesystem access to the minimum necessary.
- Preserve role boundaries from `portable/mcp/role-mcp-matrix.md`.

## Server-specific note

No data mutation. Prefer schema-only role and masked samples.

## Forbidden by default

- Production write/deploy.
- Broad secrets access.
- Destructive actions.
- Persisting cache/index artifacts into Git.
