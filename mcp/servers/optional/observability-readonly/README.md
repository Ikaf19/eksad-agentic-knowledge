# Observability Read-only MCP

| Field | Value |
|---|---|
| Server ID | `observability-readonly` |
| Priority | `P2/Pn` |
| Status | `optional` |
| Risk | `high` |
| Default enabled | `false` |

## Capabilities

- `logs-metrics-traces-read-only`

## Role policy

Allowed:

- `devops-engineer`
- `technical-leader`

Optional/conditional:

- `qa-engineer`
- `project-manager`

Forbidden by default:

- `business-analyst`
- `system-analyst`
- `developer-backend`
- `developer-frontend`
- `general-coordinator`

## Notes

High privacy risk; redaction and scoped queries required.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
