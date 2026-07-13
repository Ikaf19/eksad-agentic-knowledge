# OpenAPI Contract MCP

| Field | Value |
|---|---|
| Server ID | `openapi-contract` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `medium` |
| Default enabled | `false` |

## Capabilities

- `api-contract`
- `openapi-validation`

## Role policy

Allowed:

- `system-analyst`
- `developer-backend`
- `developer-frontend`
- `qa-engineer`
- `technical-leader`

Optional/conditional:

- `devops-engineer`

Forbidden by default:

- `business-analyst`
- `project-manager`
- `general-coordinator`

## Notes

Can also run as file-based validator in non-MCP harnesses.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
