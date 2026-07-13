# Usage Modes — Chatbot Project and Fully Agentic

This repository supports two first-class usage modes.

## Mode A — Chatbot Project Mode

Use this when working with GPT Project, Claude Project, or another document-centric chatbot project.

Characteristics:

- No local runtime setup required.
- No MCP required.
- No filesystem/git/tool execution assumed.
- User uploads or attaches knowledge files into the chatbot project.
- The chatbot drafts/specifies/reviews based on provided files and user-provided evidence.

Recommended project knowledge upload set:

```text
EKSAD/gpt/README.md
EKSAD/gpt/SYSTEM_INSTRUCTIONS_SHORT.md
EKSAD/gpt/_base/
EKSAD/gpt/_template/
EKSAD/gpt/<role>/... relevant role instruction files
portable/roles/<role>.md
portable/workflows/<workflow>.md
portable/policies/
portable/mcp/role-mcp-matrix.md       # governance reference only; no MCP runtime assumed
```

Use existing GPT/Claude setup files as before:

```text
EKSAD/gpt/CLAUDE_SETUP_GUIDE.md
EKSAD/gpt/GPT_CHAT_STARTERS.md
EKSAD/gpt/business-analyst/CLAUDE_BA_SETUP_GUIDE.md
EKSAD/gpt/system-analyst/CLAUDE_SA_SETUP_GUIDE.md
EKSAD/gpt/technical-leader/CLAUDE_TL_SETUP_GUIDE.md
EKSAD/gpt/developer/CLAUDE_DEV_SETUP_GUIDE.md
EKSAD/gpt/developer/CLAUDE_DEV_FE_SETUP_GUIDE.md
EKSAD/gpt/qa/CLAUDE_QA_SETUP_GUIDE.md
```

MCP in chatbot mode:

- Treat MCP docs as policy/capability reference only.
- Do not assume MCP tools exist.
- Ask the user to paste/export evidence if needed.

## Mode B — Fully Agentic Runtime Mode

Use this when running Hermes, Claude Code, Codex, Cursor, OpenCode, or another tool-using agent.

Characteristics:

- Repo is cloned locally.
- Adapter-specific instructions are used.
- Agent may access files/git/tools/MCP if configured and allowed.
- Secrets and runtime config remain local.

Recommended flow:

```text
git clone eksad-agentic-knowledge
→ read portable layer
→ select runtime adapter
→ run adapter doctor/validator
→ configure local secrets/runtime separately
→ enable MCP only if allowed by role and approved
```

## Mode C — Hybrid

Use chatbot projects for BA/SA/PM specification work and an agentic runtime for implementation/review/evidence collection.

Example:

```text
GPT Project drafts BRD/FSD
→ Claude Project reviews TSD wording
→ Hermes/Codex/Claude Code inspects repo/code with tools
→ QA/PM consumes evidence and updates deliverables
```

## Non-negotiable portability rule

Portable source remains canonical. Adapters must render from or reference portable docs. Do not let GPT Project instructions, Claude Project instructions, Hermes SOUL, or Hermes SKILL.md become separate competing sources of truth.
