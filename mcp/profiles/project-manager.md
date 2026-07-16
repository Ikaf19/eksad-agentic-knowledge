# MCP Profile — project-manager

## Intent

Project Manager may inspect planning, Git, CI, quality/security, observability, and content/delivery evidence for governance.

## Source of truth

- `portable/roles/project-manager.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)
- `jenkins-readonly` — `ci-evidence`, `pipeline-read-only` (P1/planned, risk: medium)
- `sonarqube-readonly` — `quality-evidence`, `static-analysis-read-only` (P1/planned, risk: medium)
- `trivy-evidence` — `security-evidence`, `vulnerability-report-read-only` (P1/planned, risk: high)

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `content-draft` — `content-repository-draft` (P2/optional, risk: medium)
- `data-bi-readonly` — `data-bi-artifact-read-only` (P2/optional, risk: medium-high)
- `observability-readonly` — `logs-metrics-traces-read-only` (P2/Pn/optional, risk: high)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Forbidden by default

`codebase-memory`, `openapi-contract`, `figma-readonly`, `kafka-readonly`, `mongodb-readonly`, `notebook-sandbox`, `rabbitmq-readonly`, `playwright-browser`, `postgres-schema-readonly`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
