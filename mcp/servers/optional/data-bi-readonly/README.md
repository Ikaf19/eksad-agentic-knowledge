# Data/BI Read-only MCP

Status: optional desired-state MCP server. Inclusion is not approval to install or enable.

## Capability

- `data-bi-artifact-read-only`

## Allowed roles

- `data-analyst`
- `data-scientist`

## Optional roles

- `system-analyst`
- `technical-leader`
- `qa-engineer`
- `project-manager`

## Forbidden by default

- `general-coordinator`
- `business-analyst`
- `developer-backend`
- `developer-frontend`
- `devops-engineer`
- `ui-ux-designer`
- `content-creator`

## Boundary

Use only for approved analytics artifacts, exported datasets, BI metadata, or data dictionaries. No live production data mutation.

Runtime activation requires explicit approval, least-privilege credentials, and a fallback path for chatbot/project modes where MCP does not exist.
