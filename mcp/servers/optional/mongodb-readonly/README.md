# MongoDB Read-only MCP

| Field | Value |
|---|---|
| Server ID | `mongodb-readonly` |
| Priority | `P2` |
| Status | `optional` |
| Risk | `high` |
| Default enabled | `false` |

## Capabilities

- `audit-data-read-only`

## Role policy

Allowed:

- `system-analyst`
- `qa-engineer`
- `devops-engineer`

Optional/conditional:

- `technical-leader`
- `developer-backend`

Forbidden by default:

- `business-analyst`
- `developer-frontend`
- `project-manager`
- `general-coordinator`

## Notes

Avoid sensitive data dumps; prefer metadata/evidence queries.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
