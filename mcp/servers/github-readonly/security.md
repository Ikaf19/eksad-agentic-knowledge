# Security — GitHub Read-only MCP

## Risk

`medium`

## Default

This server is not enabled by default.

## Required controls

- Use least privilege credentials.
- Keep real env values outside Git.
- Disable sampling unless explicitly reviewed.
- Scope network/filesystem access to the minimum necessary.
- Preserve role boundaries from `portable/mcp/role-mcp-matrix.md`.

## Server-specific note

Use read-only scopes. Prefer repo-limited token when possible.

## Forbidden by default

- Production write/deploy.
- Broad secrets access.
- Destructive actions.
- Persisting cache/index artifacts into Git.
