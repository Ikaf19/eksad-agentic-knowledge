# MCP Server Catalog

This catalog lists candidate MCP server implementations. Inclusion here is not approval to install or enable.

| Server/candidate | Capability | Priority | Default | Notes |
|---|---|---:|---|---|
| `codebase-memory-mcp` | Code intelligence | P0 | Pilot only | Use controlled root, no auto-watch, no global default. |
| GitHub/GitLab read-only | Git RO | P0 | Optional | Prefer least-privilege token. |
| Jenkins read-only | CI evidence | P1 | Optional | Evidence only. |
| SonarQube read-only | Quality evidence | P1 | Optional | Quality gate evidence. |
| Trivy evidence | Security evidence | P1 | Optional | Prefer artifacts from CI. |
| PostgreSQL schema read-only | DB schema RO | P1 | Optional | Schema-only, no mutation. |
| OpenAPI tooling | Contract inspection | P1 | Optional | File/API contract validation. |
| Playwright browser | Browser inspection | P1 | Optional | Scoped URLs only. |
| RabbitMQ/Kafka read-only | Event topology | P2 | Off | Add when event topology evidence is needed. |
| MongoDB read-only | Audit evidence | P2 | Off | Avoid sensitive data dumps. |
| Figma read-only | Design context | P2 | Off | Add only if Figma is source. |
| Data/BI read-only | Data/BI artifacts | P2 | Off | Approved exports, dashboards, metadata, and data dictionaries only. |
| Notebook sandbox | Reproducible analysis sandbox | P2 | Off | Isolated workspace; no production data or secrets by default. |
| Content draft | Draft-only content repository | P2 | Off | Draft artifacts only; publication remains approval-gated. |
| Observability read-only | Operational evidence | P2/Pn | Off | Logs/metrics/traces evidence only. |
