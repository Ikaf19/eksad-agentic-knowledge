# GPT Project Adapter

Use this adapter for ChatGPT Projects / GPT Project style usage.

## Knowledge files to upload

Core:

```text
EKSAD/gpt/README.md
EKSAD/gpt/SYSTEM_INSTRUCTIONS_SHORT.md
EKSAD/gpt/_base/
EKSAD/gpt/_template/
portable/README.md
portable/roles/
portable/workflows/
portable/policies/
portable/mcp/role-mcp-matrix.md
```

Role-specific:

```text
EKSAD/gpt/business-analyst/
EKSAD/gpt/system-analyst/
EKSAD/gpt/technical-leader/
EKSAD/gpt/developer/
EKSAD/gpt/qa/
EKSAD/gpt/project-manager/
EKSAD/gpt/devops-engineer/
```

Upload only the roles needed for that GPT Project if file limits apply.

## Project instruction template

Use `PROJECT_INSTRUCTIONS_TEMPLATE.md` as the GPT Project instruction body, then adjust the active role and scope.

## MCP note

GPT Project mode does not require MCP. MCP docs are used as governance and capability planning reference only.
