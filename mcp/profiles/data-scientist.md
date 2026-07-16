# MCP Profile — data-scientist

## Intent

Data Scientist may use RAG, dataset/catalog read-only, notebook sandbox, optional code intelligence, and optional experiment evidence tools when explicitly configured.

## Source of truth

- `portable/roles/data-scientist.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after approval.
