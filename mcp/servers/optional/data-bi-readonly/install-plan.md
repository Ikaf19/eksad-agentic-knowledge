# Install Plan — Data/BI Read-only MCP

This is a desired-state placeholder. Do not install automatically.

1. Select an approved implementation.
2. Review source, license, and security posture.
3. Install outside Git under `/opt/eksad-mcp/bin/data-bi-readonly` or an environment-approved path.
4. Bind environment variables from a runtime secret manager, never from committed files.
5. Run `validation.md` checks.
6. Enable only for allowed/optional roles after explicit runtime approval.
