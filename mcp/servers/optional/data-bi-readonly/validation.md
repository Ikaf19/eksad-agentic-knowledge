# Validation — Data/BI Read-only MCP

Before enabling:

- Confirm command path exists only in the runtime environment.
- Confirm all required env vars are present in runtime secret manager.
- Confirm role allowlist matches `manifest.json`.
- Confirm dry-run/list/read operations work without write permissions.
- Confirm fallback workflow is documented for chatbot/project mode.
