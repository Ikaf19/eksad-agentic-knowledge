# SonarQube Read-only MCP

| Field | Value |
|---|---|
| Server ID | `sonarqube-readonly` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `medium` |
| Default enabled | `false` |

## Capabilities

- `quality-evidence`
- `static-analysis-read-only`

## Role policy

Allowed:

- `technical-leader`
- `devops-engineer`
- `project-manager`

Optional/conditional:

- `developer-backend`
- `developer-frontend`
- `qa-engineer`

Forbidden by default:

- `business-analyst`
- `general-coordinator`

## Notes

Quality gate evidence only.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
