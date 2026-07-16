# MCP Profile — content-creator

## Intent

Content Creator may use RAG, Git/document read-only, optional browser evidence, and content draft tooling. It does not publish externally without approval.

## Source of truth

- `portable/roles/content-creator.md`.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification and never grant write, publication, deployment, or approval authority.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after approval.
