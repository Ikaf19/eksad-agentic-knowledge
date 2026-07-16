# MCP Profile — developer-backend

## Intent

Developer Backend may inspect source, contracts, schema, and event topology evidence for backend implementation support.

## Source of truth

- `portable/roles/developer-backend.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- `codebase-memory` — `code-intelligence`, `architecture-query`, `code-graph` (P0/candidate-pilot, risk: medium-high)
- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)
- `openapi-contract` — `api-contract`, `openapi-validation` (P1/planned, risk: medium)
- `kafka-readonly` — `event-topology-read-only` (P2/optional, risk: high)
- `rabbitmq-readonly` — `event-topology-read-only` (P2/optional, risk: high)
- `postgres-schema-readonly` — `db-schema-read-only`, `migration-inspection` (P1/planned, risk: high)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `jenkins-readonly` — `ci-evidence`, `pipeline-read-only` (P1/planned, risk: medium)
- `mongodb-readonly` — `audit-data-read-only` (P2/optional, risk: high)
- `sonarqube-readonly` — `quality-evidence`, `static-analysis-read-only` (P1/planned, risk: medium)
- `trivy-evidence` — `security-evidence`, `vulnerability-report-read-only` (P1/planned, risk: high)

## Forbidden by default

`content-draft`, `data-bi-readonly`, `figma-readonly`, `notebook-sandbox`, `observability-readonly`, `playwright-browser`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
