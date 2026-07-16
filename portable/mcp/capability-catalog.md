# MCP Capability Catalog

| Capability | Description | Primary roles | Risk | Example server/tooling |
|---|---|---|---|---|
| Code intelligence | Search/query code graph, architecture, symbol paths | SA, TL, Dev-BE, Dev-FE, QA, DevOps | Medium | `codebase-memory-mcp` |
| Git read-only | Issues, PR/MR, branches, status, diffs, approved source docs | General, PM, TL, Dev, DevOps, Data Analyst, Content Creator | Medium | GitHub/GitLab MCP/API |
| CI evidence | Pipeline status, test artifacts | DevOps, PM, TL, QA | Medium | Jenkins |
| Quality evidence | Static analysis and quality gates | TL, DevOps, PM | Medium | SonarQube |
| Security evidence | SBOM/vulnerability reports | AppSec, TL, DevOps, PM | High | Trivy |
| Schema/data read-only | Inspect DB schema, migrations, governed data extracts, or read-only analytics views | SA, Dev-BE, QA, DevOps, Data Analyst, Data Scientist | High | PostgreSQL read-only / governed data API |
| Contract inspection | OpenAPI/Swagger validation | SA, Dev-BE, Dev-FE, QA, Data Analyst | Medium | OpenAPI tooling |
| Browser/UI inspection | Scoped UI automation/inspection | Dev-FE, QA, UI/UX, Content Creator | Medium-High | Playwright |
| Event topology read-only | Queue/topic/exchange metadata | SA, Dev-BE, DevOps, TL | High | RabbitMQ/Kafka read-only |
| Observability read-only | Logs/metrics/traces evidence | DevOps, TL, QA, PM, Data Analyst | High | Grafana/Prometheus/APM |
| Data/BI artifact read-only | Read approved CSV, spreadsheet, BI export, dashboard metadata, or data dictionary | Data Analyst, Data Scientist, PM | Medium-High | Sheets/Drive/BI connector |
| Notebook sandbox | Execute reproducible analysis in isolated, approved workspace | Data Scientist, Data Analyst | High | Jupyter sandbox |
| Design asset read-only | Inspect approved design files, component inventory, screenshots, or prototypes | UI/UX, Dev-FE, QA | Medium | Figma/design MCP |
| Content repository draft | Create or edit draft-only content artifacts with approval workflow | Content Creator, PM | Medium | Docs/CMS draft connector |
