# MCP Profile — general-coordinator

## Intent

General Coordinator routes/summarizes only; MCP access is minimal and read-only if any.

## Source of truth

- `portable/roles/general-coordinator.md` when present.
- `portable/mcp/role-mcp-matrix.md`.
- `mcp/servers/*/manifest.json`.

## Runtime rule

A runtime may expose only MCP capabilities allowed or optional for this role. Optional capabilities require task justification.

## Chatbot mode

In GPT Project / Claude Project, this file is policy reference only. Ask the user for evidence instead of assuming tool access.

## Agentic mode

In Hermes or another agentic harness, use server manifests to render runtime config and apply only after approval.
