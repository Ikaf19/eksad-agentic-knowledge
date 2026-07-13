# Validation — OpenAPI Contract MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py openapi-contract > /tmp/openapi-contract.hermes.yaml
```

Review `/tmp/openapi-contract.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test openapi_contract
```

Expected result:

- Server appears as `openapi_contract`.
- Tools are discovered with `mcp_openapi_contract_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
