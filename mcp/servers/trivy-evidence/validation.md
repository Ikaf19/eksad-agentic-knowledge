# Validation — Trivy Evidence MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py trivy-evidence > /tmp/trivy-evidence.hermes.yaml
```

Review `/tmp/trivy-evidence.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test trivy_evidence
```

Expected result:

- Server appears as `trivy_evidence`.
- Tools are discovered with `mcp_trivy_evidence_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
