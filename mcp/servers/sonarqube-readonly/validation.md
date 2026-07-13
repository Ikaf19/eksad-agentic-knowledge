# Validation — SonarQube Read-only MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py sonarqube-readonly > /tmp/sonarqube-readonly.hermes.yaml
```

Review `/tmp/sonarqube-readonly.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test sonarqube_readonly
```

Expected result:

- Server appears as `sonarqube_readonly`.
- Tools are discovered with `mcp_sonarqube_readonly_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
