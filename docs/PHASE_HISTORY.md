# Phase History — EKSAD Agentic Knowledge

**Status:** Historical record  
**Last normalized:** 2026-07-23
**Scope:** Git source-of-truth evolution only. Runtime activation remains separate.

---

## 1. Mainline merge history

Current `origin/main` first-parent history at normalization time:

| Mainline commit | Event | Meaning |
|---|---|---|
| `f5a9cdc` | Initial commit | Repository created. |
| `ff2feb0` | Merge PR #1 from `feat/mcp-foundation` | Initial curated knowledge foundation and MCP source-of-truth merge. |
| `dbaa6d7` | Merge PR #2 from `feat/rag-foundation` | RAG desired-state foundation merged. |
| `38c7bd2` | Merge PR #3 from `feat/llm-gateway-foundation` | LLM Gateway/LiteLLM desired-state foundation merged. |
| `0a66076` | Merge PR #4 from `feat/role-expansion-pack` | Role expansion and Phase F matrix/skill hardening merged. |
| `7955ae3` | Merge PR #5 from `docs/portal-delivery-mode-foundation` | Roadmap normalization plus portable `DeliveryProfile`, `ExternalWorkItemLink`, and JIRA-first orchestrator dependency contracts merged. |

---

## 2. Functional phase history

| Functional slice | Branch / evidence | Outcome |
|---|---|---|
| Repository bootstrap | Initial repository and `docs/SOURCE_MIGRATION.md` | Established Git as source-of-truth and separated portable layer from Hermes adapter. |
| Chatbot project mode | `docs/USAGE_MODES.md`, `agent-adapters/chatbot-projects/` | Preserved Claude/GPT Project usability without assuming MCP/tools. |
| MCP foundation | `mcp/`, `portable/mcp/`, `mcp/scripts/validate-mcp-catalog.py` | Added discoverable MCP desired-state catalog, role profiles, manifests, renderers, and read-only validation. |
| RAG foundation | `rag/`, `portable/rag/`, `eval/rag/` | Added corpus manifests, retrieval/citation policy, evaluation fixtures, and chatbot/runtime adapter guidance. |
| RAG enrichment | `rag/RAG_API_CONTRACT.md`, `rag/RAG_TOOL_CONTRACT.md`, `mcp/servers/rag-api-readonly/` | Aligned RAG with Milvus/Ollama/MinIO/RAG-API architecture and tool contract. |
| LLM Gateway foundation | `llm-gateway/`, `portable/llm-gateway/`, `eval/llm-gateway/` | Added LiteLLM/OpenAI-compatible alias/routing/budget/fallback/guardrail desired state. |
| Role expansion | `portable/roles/`, `portable/workflows/`, Hermes role instructions | Expanded canonical role coverage from 9 to 13 roles. |
| Role matrix and skill hardening | `0834354 feat: harden role matrix and skills` included in PR #4 | Normalized role-model routing, collaboration matrix, skill enrichment, optional MCP manifests, RAG split manifests, validators. |
| Web Portal future alignment | `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` | Parked portal/control-plane architecture as future plan without reserving next phase labels. |
| Roadmap normalization | `docs/ROADMAP.md`, `docs/PHASE_HISTORY.md`, `docs/NEXT_PHASE_CANDIDATES.md` | Canonicalized current status and next-candidate queue. |
| Portal delivery-mode foundation | `portable/portal/`, `scripts/validate-portal-delivery-mode.py`, PR #5 | Added link-only external work item contracts, delivery profiles, and explicit future/orchestrator dependency for JIRA-first delivery without approving JIRA writes. |

---

## 3. Current canonical role set

```text
general-coordinator
business-analyst
system-analyst
technical-leader
developer-backend
developer-frontend
qa-engineer
project-manager
devops-engineer
data-analyst
data-scientist
ui-ux-designer
content-creator
```

All current role coverage should be validated with:

```bash
python3 scripts/validate-role-coverage.py
```

---

## 4. Historical documents vs current roadmap

`docs/GRAND_PLAN.md` remains as a historical grand plan and execution log. For current navigation, prefer:

- `docs/ROADMAP.md` — canonical current roadmap.
- `docs/PHASE_HISTORY.md` — historical phase/merge record.
- `docs/NEXT_PHASE_CANDIDATES.md` — candidate next phases.
- `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` — parked Web Portal future alignment plan.
- `docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md` — parked JIRA-first plan that depends on the future orchestrator layer.

Historical references to early branches, pending blockers, or initial “9 role” assumptions should be read in their original dated context, not as current operational status.
