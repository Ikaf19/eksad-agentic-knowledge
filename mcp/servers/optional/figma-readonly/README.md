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
- `ui-ux-designer`

Optional/conditional:

- `technical-leader`
- `qa-engineer`
- `content-creator`

Forbidden by default:

- `general-coordinator`
- `developer-backend`
- `project-manager`
- `devops-engineer`
- `data-analyst`
- `data-scientist`

## Notes

Use only if Figma is source of design truth. Figma access is read-only design context, not permission to publish designs, approve UI, or bypass BA/SA/FE/QA gates.

## Files

- `manifest.json` — machine-readable desired-state contract.
- `install-plan.md` — human/agent setup plan.
- `security.md` — security boundaries.
- `validation.md` — verification checklist.
- `adapters/hermes.example.yaml` — Hermes config snippet.
- `adapters/generic-harness.example.json` — generic runtime binding shape.
