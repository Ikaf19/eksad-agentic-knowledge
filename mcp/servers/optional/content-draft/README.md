# Content Draft MCP

Status: optional desired-state MCP server. Inclusion is not approval to install or enable.

## Capability

- `content-repository-draft`

## Allowed roles

- `content-creator`

## Optional roles

- `project-manager`
- `ui-ux-designer`

## Forbidden by default

- `general-coordinator`
- `business-analyst`
- `system-analyst`
- `technical-leader`
- `developer-backend`
- `developer-frontend`
- `qa-engineer`
- `devops-engineer`
- `data-analyst`
- `data-scientist`

## Boundary

Draft-only content repository access. Publishing or external posting always requires explicit approval.

Runtime activation requires explicit approval, least-privilege credentials, and a fallback path for chatbot/project modes where MCP does not exist.
