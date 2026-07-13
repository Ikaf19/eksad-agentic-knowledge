# GitHub Read-only MCP

| Field | Value |
|---|---|
| Server ID | `github-readonly` |
| Priority | `P0` |
| Status | `candidate` |
| Risk | `medium` |
| Default enabled | `false` |

## Capabilities

- `git-read-only`
- `issues-read-only`
- `pull-requests-read-only`

## Role policy

Allowed:

- `technical-leader`
- `developer-backend`
- `developer-frontend`
- `qa-engineer`
- `project-manager`
- `devops-engineer`

Optional/conditional:

- `system-analyst`
- `general-coordinator`

Forbidden by default:

- `business-analyst`

## Notes

Use read-only scopes. Prefer repo-limited token when possible.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
