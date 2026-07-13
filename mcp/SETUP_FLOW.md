# MCP Setup Flow

This flow is designed to be repeatable when moving between Hermes environments or future agentic harnesses.

## Setup gates

| Gate | Owner | Required before |
|---|---|---|
| Design/source approval | User / PM / TL | Runtime install |
| Security review | TL / DevOps / AppSec | Credentials or networked MCP |
| Runtime apply approval | User / DevOps | Editing live agent config |
| Verification | Hermes / DevOps | Declaring MCP ready |

## Generic flow

```text
git clone eksad-agentic-knowledge
→ read mcp/README.md and mcp/ROADMAP_P0_TO_PN.md
→ run mcp/scripts/doctor.sh
→ select server manifests from mcp/servers/*/manifest.json
→ review server install-plan.md and security.md
→ install approved server binary/package outside Git
→ create local env/secrets outside Git
→ render adapter-specific config snippet
→ ask approval to apply live config
→ restart/reload agent runtime
→ test server/tool discovery
→ record evidence in project docs or session summary
```

## Hermes-specific flow

```bash
cd /path/to/eksad-agentic-knowledge
bash mcp/scripts/doctor.sh
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py codebase-memory github-readonly > /tmp/eksad-mcp.yaml
# Review /tmp/eksad-mcp.yaml manually.
# Only after approval, merge into ~/.hermes/config.yaml under mcp_servers.
# Restart Hermes or run /reload-mcp if available for the current runtime.
hermes mcp list
hermes mcp test <server-name>
```

## Chatbot project mode

GPT Project / Claude Project cannot install MCP by themselves. In those environments:

- Treat this folder as governance/reference.
- Ask the user to provide evidence manually.
- Do not claim MCP tools are available unless the platform explicitly provides them.

## Fully agentic mode

Hermes or another tool-using harness may apply this folder as desired state, but runtime writes remain explicit and local.
