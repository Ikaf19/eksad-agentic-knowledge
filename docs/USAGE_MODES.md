# Usage Modes — Chatbot, Agentic, and Hybrid

This repository supports three usage modes: document-centric chatbot projects, fully agentic runtimes, and a hybrid that hands artifacts between both environments.

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
portable/rag/corpus-matrix.md         # retrieval guidance only; platform search is native
portable/llm-gateway/alias-policy.md  # model alias governance only; platform model is selected outside repo
rag/adapters/chatbot-projects/upload-bundle-guidance.md
llm-gateway/adapters/chatbot-projects/README.md
```


### Phase E role expansion in chatbot mode

For Data Analyst, Data Scientist, UI/UX Designer, or Content Creator chatbot projects, upload the matching files from:

```text
portable/roles/<role>.md
portable/workflows/<role-workflow>.md
portable/deliverables/<role-deliverable>.md
portable/mcp/role-mcp-matrix.md
portable/rag/corpus-matrix.md
portable/llm-gateway/role-model-matrix.md
```

Treat these roles as draft/analysis/design/content owners only. Business, legal, technical, QA, release, and publication approvals remain attributable gates.

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

RAG in chatbot mode:

- Treat `rag/` docs as upload/search governance, not as a live vector database.
- Use corpus manifests to choose which files to upload.
- Cite uploaded file names/paths when answering from project knowledge.
- Do not claim live `rag-api-readonly` MCP/API tools exist in chatbot-only mode.

LLM Gateway in chatbot mode:

- Treat `llm-gateway/` docs as model routing governance, not as a live LiteLLM endpoint.
- Do not claim `eksad.*` aliases are selectable unless the chatbot platform/runtime actually exposes them.
- Preserve alias names in deliverables so the work can migrate to Hermes/future runtime later.

## Mode B — Fully Agentic Runtime Mode

Use this when running Hermes, Claude Code, Codex, Cursor, OpenCode, or another tool-using agent.

Characteristics:

- Repo is cloned locally.
- Adapter-specific instructions are used.
- Agent may access files/git/tools/MCP if configured and allowed.
- Secrets and runtime config remain local.

Recommended flow:

```bash
git clone https://github.com/Ikaf19/eksad-agentic-knowledge.git
cd eksad-agentic-knowledge
./scripts/validate-all.sh
```

Then follow this sequence:

```text
read portable layer
→ select runtime adapter
→ run adapter doctor/validator
→ configure local secrets/runtime separately
→ bind LLM Gateway aliases through approved OpenAI-compatible/LiteLLM endpoint if allowed
→ enable MCP only if allowed by role and approved
→ bind RAG through approved RAG API/MCP tools only after approval
→ build RAG indexes only from active corpus manifests and only after approval
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


## MCP foundation

Top-level MCP desired-state catalog and setup flow: `mcp/README.md`.

## RAG foundation

Top-level RAG desired-state catalog, corpus manifests, retrieval/citation policy, RAG API/MCP contracts, and eval fixtures: `rag/README.md`.

Preferred agentic RAG path:

```text
role skill → MCP rag-api-readonly tool → RAG API → Milvus/Ollama/MinIO runtime
```

## LLM Gateway foundation

Top-level LLM Gateway desired-state catalog, aliases, LiteLLM examples, OpenAI-compatible adapter guidance, budget/routing/guardrail policy, and validators: `llm-gateway/README.md`.

Preferred agentic model path:

```text
role profile → eksad.* capability alias → OpenAI-compatible gateway → LiteLLM/provider runtime
```
