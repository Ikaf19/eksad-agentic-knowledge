# Security and Secrets Policy

## Never commit

- API keys
- GitHub/GitLab tokens
- Passwords
- Private keys
- Production database URLs
- Kubeconfigs
- Runtime `.env` files
- Downloaded MCP binaries
- Cache/index artifacts

## Allowed in Git

- Env var names, e.g. `${GITHUB_TOKEN}`
- Redacted examples, e.g. `[REDACTED]`
- Non-sensitive local paths used as placeholders
- Read-only config templates

## Production safety

Production write capabilities are forbidden by default. Any production-write adapter requires explicit project-specific approval and audit trail.
