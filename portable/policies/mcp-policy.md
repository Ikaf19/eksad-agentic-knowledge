# MCP Policy

## Position

MCP is treated as a portable tool capability layer, not as a Hermes-only feature.

## Defaults

1. Read-only first.
2. Role-scoped access.
3. No secrets in Git.
4. No auto-install from unreviewed third-party installers.
5. No auto-index/watch of all repositories by default.
6. Production write and deploy tools are forbidden by default.
7. Every MCP-assisted workflow must have a fallback path.

## Approval

MCP access does not grant approval authority. Merge, deploy, risk acceptance, and DB mutation remain separately gated.
