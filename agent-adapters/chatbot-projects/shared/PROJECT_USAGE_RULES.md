# Shared Chatbot Project Usage Rules

## Scope

Use these rules for GPT Project, Claude Project, or any chatbot project that works by uploading knowledge files.

## Rules

1. Treat `EKSAD/gpt/` and `portable/` as the project knowledge source.
2. Do not assume tools, filesystem, Git, CI, database, or MCP access.
3. If evidence is needed, ask the user to provide/export it.
4. Keep role boundaries from `portable/roles/` and `portable/policies/role-boundaries.md`.
5. Keep MCP boundaries from `portable/mcp/role-mcp-matrix.md`, but do not call MCP tools unless the platform explicitly provides them.
6. Use EKSAD templates from `EKSAD/gpt/_template/` for deliverables.
7. Record assumptions and open questions when source evidence is missing.

## Recommended project upload bundle

Minimum:

```text
EKSAD/gpt/README.md
EKSAD/gpt/SYSTEM_INSTRUCTIONS_SHORT.md
EKSAD/gpt/_base/
EKSAD/gpt/_template/
portable/README.md
portable/roles/
portable/workflows/
portable/policies/
```

Role-specific add-on:

```text
EKSAD/gpt/<role>/
portable/roles/<role>.md
portable/workflows/<relevant-workflow>.md
```
