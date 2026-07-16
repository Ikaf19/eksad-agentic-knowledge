# Hermes RAG Role Usage Matrix

| Role | Default corpora | Typical questions | Must cite? |
|---|---|---|---|
| General Coordinator | corpus index, governance | route task, identify active corpora, check approval gates | cite if using evidence |
| Business Analyst | core, templates, role instructions, governance | UR/BRD/FSD, scope, glossary, business rules | yes |
| System Analyst | core, templates, role instructions, governance | TSD, ERD, API contract, architecture, event schema | yes |
| Technical Leader | core, role instructions, governance, activated project corpora | architecture/code/security review and readiness gates | yes |
| Developer Backend | core, role instructions, activated specs/contracts | Quarkus/backend standards, APIs, persistence/event patterns | yes |
| Developer Frontend | core, templates, role instructions, activated specs/design evidence | React/TS implementation patterns, UI contract handoff | yes |
| QA Engineer | core, templates, role instructions, activated project corpora | RTM, test plan, test evidence lookup, regression risk | yes |
| Project Manager | core, governance, activated project/release corpora | plan, WBS, milestone evidence, release readiness | cite if using evidence |
| DevOps Engineer | core, governance, activated release/evidence corpora | CI/CD, observability, release evidence, environment constraints | yes |
| Data Analyst | core, role instructions, governance, activated data evidence | KPI definitions, data quality, dashboard/reporting analysis | yes |
| Data Scientist | core, role instructions, governance, activated data/experiment evidence | experiment design, model evaluation, assumptions, rollback criteria | yes |
| UI/UX Designer | core, templates, role instructions, activated design evidence | journey maps, usability findings, wireframe/frontend handoff | yes |
| Content Creator | core, templates, role instructions, activated release/content evidence | release notes, user guides, training/FAQ/source-grounded content | yes |

Project-specific corpora remain disabled unless a project activation file/policy explicitly enables them. Hermes must use the approved RAG API/MCP boundary and must not access vector stores or storage credentials directly.
