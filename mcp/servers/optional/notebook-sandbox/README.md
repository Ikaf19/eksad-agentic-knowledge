# Notebook Sandbox MCP

Status: optional desired-state MCP server. Inclusion is not approval to install or enable.

## Capability

- `notebook-sandbox`

## Allowed roles

- `data-scientist`

## Optional roles

- `data-analyst`

## Forbidden by default

- `general-coordinator`
- `business-analyst`
- `system-analyst`
- `technical-leader`
- `developer-backend`
- `developer-frontend`
- `qa-engineer`
- `project-manager`
- `devops-engineer`
- `ui-ux-designer`
- `content-creator`

## Boundary

Use only in isolated, non-production workspaces with approved data. No network or secret access by default.

Runtime activation requires explicit approval, least-privilege credentials, and a fallback path for chatbot/project modes where MCP does not exist.
