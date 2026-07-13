# Figma Read-only MCP

| Field | Value |
|---|---|
| Server ID | `figma-readonly` |
| Priority | `P2` |
| Status | `optional` |
| Risk | `medium` |
| Default enabled | `false` |

## Capabilities

- `design-context-read-only`

## Role policy

Allowed:

- `business-analyst`
- `system-analyst`
- `developer-frontend`

Optional/conditional:

- `technical-leader`
- `qa-engineer`

Forbidden by default:

- `developer-backend`
- `project-manager`
- `devops-engineer`
- `general-coordinator`

## Notes

Use only if Figma is source of design truth.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
