# MCP Profile — data-analyst

## Intent

Data Analyst may inspect governed data/BI artifacts, schema metadata, and RAG evidence for KPI/reporting analysis.

## Source of truth

- `portable/roles/data-analyst.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- `data-bi-readonly` — `data-bi-artifact-read-only` (P2/optional, risk: medium-high)
- `postgres-schema-readonly` — `db-schema-read-only`, `migration-inspection` (P1/planned, risk: high)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)
- `openapi-contract` — `api-contract`, `openapi-validation` (P1/planned, risk: medium)
- `notebook-sandbox` — `notebook-sandbox` (P2/optional, risk: high)
- `observability-readonly` — `logs-metrics-traces-read-only` (P2/Pn/optional, risk: high)

## Forbidden by default

`codebase-memory`, `content-draft`, `figma-readonly`, `playwright-browser`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
