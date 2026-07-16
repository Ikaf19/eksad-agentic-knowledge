# MCP Profile — general-coordinator

## Intent

General Coordinator routes work, detects approval gates, and requests evidence without owning specialist deliverables.

## Source of truth

- `portable/roles/general-coordinator.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- None by default.

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Forbidden by default

`codebase-memory`, `jenkins-readonly`, `openapi-contract`, `content-draft`, `data-bi-readonly`, `figma-readonly`, `kafka-readonly`, `mongodb-readonly`, `notebook-sandbox`, `observability-readonly`, `rabbitmq-readonly`, `playwright-browser`, `postgres-schema-readonly`, `sonarqube-readonly`, `trivy-evidence`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
