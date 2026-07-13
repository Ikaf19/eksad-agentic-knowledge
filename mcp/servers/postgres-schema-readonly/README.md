# PostgreSQL Schema Read-only MCP

| Field | Value |
|---|---|
| Server ID | `postgres-schema-readonly` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `high` |
| Default enabled | `false` |

## Capabilities

- `db-schema-read-only`
- `migration-inspection`

## Role policy

Allowed:

- `system-analyst`
- `developer-backend`
- `qa-engineer`
- `devops-engineer`

Optional/conditional:

- `technical-leader`

Forbidden by default:

- `business-analyst`
- `developer-frontend`
- `project-manager`
- `general-coordinator`

## Notes

No data mutation. Prefer schema-only role and masked samples.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
