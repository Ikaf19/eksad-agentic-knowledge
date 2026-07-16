# Role Expansion Evaluation Fixtures

These fixtures validate expected boundary behavior for Phase E roles:

- `data-analyst`
- `data-scientist`
- `ui-ux-designer`
- `content-creator`

They are schema/evidence fixtures only. They do not call an LLM, external API, MCP server, database, notebook runtime, design tool, or publishing system.

Run:

```bash
python3 scripts/validate-role-coverage.py
```
