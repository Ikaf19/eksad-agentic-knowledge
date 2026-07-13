# Jenkins Read-only MCP

| Field | Value |
|---|---|
| Server ID | `jenkins-readonly` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `medium` |
| Default enabled | `false` |

## Capabilities

- `ci-evidence`
- `pipeline-read-only`

## Role policy

Allowed:

- `devops-engineer`
- `project-manager`
- `technical-leader`
- `qa-engineer`

Optional/conditional:

- `developer-backend`
- `developer-frontend`

Forbidden by default:

- `business-analyst`
- `general-coordinator`

## Notes

Evidence only; no job trigger/deploy by default.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
