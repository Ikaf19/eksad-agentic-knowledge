# Validation — Playwright Browser MCP

## Pre-apply

```bash
python3 mcp/scripts/validate-mcp-catalog.py
python3 mcp/scripts/render-hermes-config.py playwright-browser > /tmp/playwright-browser.hermes.yaml
```

Review `/tmp/playwright-browser.hermes.yaml` manually.

## Hermes runtime validation

After approved config apply and restart:

```bash
hermes mcp list
hermes mcp test playwright_browser
```

Expected result:

- Server appears as `playwright_browser`.
- Tools are discovered with `mcp_playwright_browser_...` prefix.
- No credentials are printed in logs or errors.

## Evidence

Record:

- Runtime environment name.
- Server version/source.
- Config snippet path.
- Validation date.
- Any role/tool restrictions applied.
