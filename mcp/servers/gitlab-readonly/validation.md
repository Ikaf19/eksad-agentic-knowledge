# Validation — GitLab Read-only MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py gitlab-readonly > /tmp/gitlab-readonly.hermes.yaml
```

Review `/tmp/gitlab-readonly.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test gitlab_readonly
```

Expected result:

- Server appears as `gitlab_readonly`.
- Tools are discovered with `mcp_gitlab_readonly_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
