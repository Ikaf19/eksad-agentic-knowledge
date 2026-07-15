# Hermes RAG Profile Tool Policy

Hermes profiles should use RAG through the `rag-api-readonly` MCP server after explicit runtime activation.

## Default profile policy

| Profile | RAG tools | Notes |
|---|---|---|
| `business-analyst` | search, retrieve, citations | BRD/FSD evidence only |
| `system-analyst` | search, retrieve, document, citations | architecture/API/ERD evidence |
| `developer-backend` | search, retrieve, document, citations | coding/API/backend standards |
| `developer-frontend` | search, retrieve, document, citations | frontend/API contract standards |
| `qa-engineer` | search, retrieve, artifact metadata, citations | test evidence and RTM |
| `devops-engineer` | search, retrieve, artifact metadata, citations | CI/CD/runbook/observability docs |
| `technical-leader` | all read-only RAG tools | review and governance |
| `general-coordinator` | search only by default | intake/routing context |
| `project-manager` | search and citations | deliverable/status evidence |

## Forbidden default actions

No profile should receive index/rebuild/delete/write tools by default.
