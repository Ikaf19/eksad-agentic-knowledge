# Trivy Evidence MCP

| Field | Value |
|---|---|
| Server ID | `trivy-evidence` |
| Priority | `P1` |
| Status | `planned` |
| Risk | `high` |
| Default enabled | `false` |

## Capabilities

- `security-evidence`
- `vulnerability-report-read-only`

## Role policy

Allowed:

- `devops-engineer`
- `technical-leader`
- `project-manager`

Optional/conditional:

- `qa-engineer`
- `developer-backend`
- `developer-frontend`

Forbidden by default:

- `business-analyst`
- `general-coordinator`

## Notes

Prefer CI artifacts. Do not scan broad filesystem by default.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
