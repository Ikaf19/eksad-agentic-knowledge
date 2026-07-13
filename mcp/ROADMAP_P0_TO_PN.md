# MCP Roadmap P0–Pn

## Principle

Adopt MCP by evidence value and operational safety, not by quantity. Read-only and scoped evidence capabilities come first. Write/deploy/secret-heavy MCP remains forbidden by default.

## Phases

| Phase | Capability | Status | Default | Primary roles | Notes |
|---|---|---|---|---|---|
| P0 | Code intelligence via `codebase-memory-mcp` | Candidate pilot | Off | SA, TL, Dev-BE, Dev-FE, QA, DevOps | Controlled root, no auto-watch, no global indexing. |
| P0 | Git provider read-only | Candidate | Off | General, PM, TL, Dev, QA, DevOps | Prefer GitHub/GitLab least-privilege read token. |
| P1 | Jenkins read-only | Planned | Off | DevOps, PM, TL, QA | Pipeline/test evidence only. |
| P1 | SonarQube read-only | Planned | Off | TL, DevOps, PM | Quality gate evidence. |
| P1 | Trivy evidence | Planned | Off | AppSec, TL, DevOps, PM | Prefer CI artifacts; avoid broad filesystem scan by default. |
| P1 | PostgreSQL schema read-only | Planned | Off | SA, Dev-BE, QA, DevOps | Schema-only role; no data mutation. |
| P1 | OpenAPI contract tooling | Planned | Off | SA, Dev-BE, Dev-FE, QA | Contract validation/inspection. |
| P1 | Playwright scoped browser | Planned | Off | Dev-FE, QA | Scoped URLs and test accounts only. |
| P2 | RabbitMQ/Kafka topology read-only | Optional | Off | SA, Dev-BE, DevOps, TL | Add only when event topology evidence is required. |
| P2 | MongoDB read-only | Optional | Off | SA, QA, DevOps | Avoid sensitive data dumps. |
| P2 | Figma read-only | Optional | Off | BA, SA, Dev-FE | Add only if Figma is source of design truth. |
| P2/Pn | Observability read-only | Optional | Off | DevOps, TL, QA, PM | Logs/metrics/traces evidence with redaction. |
| Pn | Production write/deploy | Forbidden by default | Off | DevOps only by explicit gate | Requires separate project-specific approval and audit. |
| Pn | Broad secrets/Vault access | Forbidden by default | Off | None by default | Prefer env-name contracts and local runtime injection only. |

## P0 recommended pilot

1. Install/validate `codebase-memory-mcp` locally with `CBM_ALLOWED_ROOT=/workspace`.
2. Configure Git provider read-only after least-privilege token is available.
3. Render Hermes config snippet; do not apply automatically.
4. User approves runtime config change.
5. Restart/reload Hermes and test discovered tools.
6. Document observed resource usage and failure modes before P1.
