# MCP Capability Catalog

| Capability | Description | Primary roles | Risk | Example server/tooling |
|---|---|---|---|---|
| Code intelligence | Search/query code graph, architecture, symbol paths | SA, TL, Dev-BE, Dev-FE, QA, DevOps | Medium | `codebase-memory-mcp` |
| Git read-only | Issues, PR/MR, branches, status, diffs | General, PM, TL, Dev, DevOps | Medium | GitHub/GitLab MCP/API |
| CI evidence | Pipeline status, test artifacts | DevOps, PM, TL, QA | Medium | Jenkins |
| Quality evidence | Static analysis and quality gates | TL, DevOps, PM | Medium | SonarQube |
| Security evidence | SBOM/vulnerability reports | AppSec, TL, DevOps, PM | High | Trivy |
| Schema read-only | Inspect DB schema/migrations | SA, Dev-BE, QA, DevOps | High | PostgreSQL read-only |
| Contract inspection | OpenAPI/Swagger validation | SA, Dev-BE, Dev-FE, QA | Medium | OpenAPI tooling |
| Browser inspection | Scoped UI automation/inspection | Dev-FE, QA | Medium-High | Playwright |
| Event topology read-only | Queue/topic/exchange metadata | SA, Dev-BE, DevOps, TL | High | RabbitMQ/Kafka read-only |
| Observability read-only | Logs/metrics/traces evidence | DevOps, TL, QA, PM | High | Grafana/Prometheus/APM |
