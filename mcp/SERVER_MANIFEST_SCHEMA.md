# MCP Server Manifest Schema

Each server directory under `mcp/servers/` contains a `manifest.json` file.

Required fields:

```json
{
  "id": "codebase-memory",
  "display_name": "Codebase Memory MCP",
  "priority": "P0",
  "status": "candidate",
  "capabilities": ["code-intelligence"],
  "default_enabled": false,
  "risk": "medium-high",
  "roles": {
    "allowed": ["system-analyst"],
    "optional": ["qa-engineer"],
    "forbidden": ["business-analyst"]
  },
  "runtime": {
    "transport": "stdio",
    "implementation": "external",
    "source_url": "https://example.com",
    "install_location": "/opt/eksad-mcp/bin/example"
  },
  "env_contract": [
    {"name": "EXAMPLE_TOKEN", "required": true, "secret": true, "description": "..."}
  ],
  "hermes_config": {
    "server_name": "example",
    "command": "/opt/eksad-mcp/bin/example",
    "args": [],
    "env": {"EXAMPLE_TOKEN": "${EXAMPLE_TOKEN}"},
    "timeout": 120,
    "connect_timeout": 60,
    "sampling": {"enabled": false}
  }
}
```

Use JSON so validators/renderers can run with Python stdlib only.
