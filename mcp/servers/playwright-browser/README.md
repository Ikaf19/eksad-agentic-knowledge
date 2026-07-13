# Playwright Browser MCP

| Field | Value |
|---|---|
| Server ID | `playwright-browser` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `medium-high` |
| Default enabled | `false` |

## Capabilities

- `browser-inspection`
- `ui-test-evidence`

## Role policy

Allowed:

- `developer-frontend`
- `qa-engineer`

Optional/conditional:

- `technical-leader`

Forbidden by default:

- `business-analyst`
- `system-analyst`
- `developer-backend`
- `project-manager`
- `devops-engineer`
- `general-coordinator`

## Notes

Scoped URLs and test accounts only.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
