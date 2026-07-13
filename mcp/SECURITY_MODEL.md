# MCP Security Model

## Defaults

1. No MCP server is enabled by default.
2. Read-only evidence capabilities come before write capabilities.
3. Role access is scoped by `portable/mcp/role-mcp-matrix.md`.
4. Secrets live in runtime env/config only, never Git.
5. Server binaries/packages are installed locally, never committed.
6. Production write/deploy MCP is forbidden unless a separate project-specific gate approves it.
7. Every MCP workflow must have a non-MCP fallback.

## Git allowed content

- Server IDs and descriptions.
- Capability mappings.
- Env var names.
- Placeholder config examples using `${ENV_VAR}`.
- Install plans and validation steps.
- Adapter snippets.

## Git forbidden content

- GitHub/GitLab/Jenkins/Sonar/Figma tokens.
- Database passwords or connection strings.
- Private keys/kubeconfigs.
- Downloaded binaries.
- Cache/index DBs.
- Production endpoint credentials.

## Codebase-memory specific controls

- `CBM_ALLOWED_ROOT=/workspace` or narrower.
- `CBM_WORKERS=1` in constrained VPS environments.
- No global auto-index/watch by default.
- Prefer `persistence=false` unless artifact use is explicitly reviewed.
- Tool selection should exclude destructive/project-delete tools unless approved.

## Adapter rule

A runtime adapter may make tool names different, but it must preserve the same capability boundary and role authorization.
