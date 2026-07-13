# Codebase Memory MCP

| Field | Value |
|---|---|
| Server ID | `codebase-memory` |
| Priority | `P0` |
| Status | `candidate-pilot` |
| Risk | `medium-high` |
| Default enabled | `false` |

## Capabilities

- `code-intelligence`
- `architecture-query`
- `code-graph`

## Role policy

Allowed:

- `system-analyst`
- `technical-leader`
- `developer-backend`
- `developer-frontend`

Optional/conditional:

- `qa-engineer`
- `devops-engineer`

Forbidden by default:

- `business-analyst`
- `project-manager`
- `general-coordinator`

## Notes

Use controlled pilot only. No auto-watch/global indexing. Prefer persistence=false.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
