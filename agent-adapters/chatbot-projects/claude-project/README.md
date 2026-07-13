# Claude Project Adapter

Use this adapter for Claude Project style usage.

## Knowledge files to add

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

Role-specific Claude guides already exist in `EKSAD/gpt/`, for example:

```text
EKSAD/gpt/CLAUDE_SETUP_GUIDE.md
EKSAD/gpt/business-analyst/CLAUDE_BA_SETUP_GUIDE.md
EKSAD/gpt/system-analyst/CLAUDE_SA_SETUP_GUIDE.md
EKSAD/gpt/technical-leader/CLAUDE_TL_SETUP_GUIDE.md
EKSAD/gpt/developer/CLAUDE_DEV_SETUP_GUIDE.md
EKSAD/gpt/developer/CLAUDE_DEV_FE_SETUP_GUIDE.md
EKSAD/gpt/qa/CLAUDE_QA_SETUP_GUIDE.md
```

## Project instruction template

Use `PROJECT_INSTRUCTIONS_TEMPLATE.md` as the Claude Project instruction body, then adjust active role and scope.

## MCP note

Claude Project mode does not require MCP. MCP docs are used as governance and capability planning reference only.
