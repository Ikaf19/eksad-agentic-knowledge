# MCP Profile — system-analyst

## Intent

System Analyst may use code intelligence, Git read-only, schema read-only, OpenAPI, and event topology evidence to produce TSD/ADR/contracts.

## Source of truth

- `portable/roles/system-analyst.md` when present.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after approval.
