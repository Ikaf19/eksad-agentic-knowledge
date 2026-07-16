# MCP Profile — content-creator

## Intent

Content Creator may inspect approved RAG/source evidence, optional design/browser evidence, and draft-only content repositories.

## Source of truth

- `portable/roles/content-creator.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Allowed MCP servers

- `content-draft` — `content-repository-draft` (P2/optional, risk: medium)
- `rag-api-readonly` — `rag-retrieval`, `citation-resolution`, `artifact-metadata`, `corpus-discovery` (P0/planned, risk: medium-high)

## Optional MCP servers

Optional capabilities require task justification, runtime approval, and a documented fallback path.

- `github-readonly` — `git-read-only`, `issues-read-only`, `pull-requests-read-only` (P0/candidate, risk: medium)
- `gitlab-readonly` — `git-read-only`, `merge-requests-read-only`, `issues-read-only` (P0/candidate, risk: medium)
- `figma-readonly` — `design-context-read-only` (P2/optional, risk: medium)
- `playwright-browser` — `browser-inspection`, `ui-test-evidence` (P1/planned, risk: medium-high)

## Forbidden by default

`codebase-memory`, `openapi-contract`, `data-bi-readonly`, `notebook-sandbox`, `observability-readonly`, `postgres-schema-readonly`

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, merge, risk-acceptance, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for exported evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after explicit runtime approval. Git contains desired-state contracts only.
