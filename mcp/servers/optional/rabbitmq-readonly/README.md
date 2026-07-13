# RabbitMQ Read-only MCP

| Field | Value |
|---|---|
| Server ID | `rabbitmq-readonly` |
| Priority | `P2` |
| Status | `optional` |
| Risk | `high` |
| Default enabled | `false` |

## Capabilities

- `event-topology-read-only`

## Role policy

Allowed:

- `system-analyst`
- `developer-backend`
- `devops-engineer`
- `technical-leader`

Optional/conditional:

- `qa-engineer`

Forbidden by default:

- `business-analyst`
- `developer-frontend`
- `project-manager`
- `general-coordinator`

## Notes

Topology only; no publish/consume/purge by default.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
