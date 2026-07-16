# MCP Profile — business-analyst

## Intent

Business Analyst may use approved knowledge/design/data evidence for UR/BRD/FSD work but does not approve technical or release decisions.

## Source of truth

- `portable/roles/business-analyst.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- `figma-readonly` — `design-context-read-only` (P2/optional, risk: medium)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)

## Forbidden by default

`codebase-memory`, `jenkins-readonly`, `openapi-contract`, `content-draft`, `data-bi-readonly`, `kafka-readonly`, `mongodb-readonly`, `notebook-sandbox`, `observability-readonly`, `rabbitmq-readonly`, `playwright-browser`, `postgres-schema-readonly`, `sonarqube-readonly`, `trivy-evidence`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
