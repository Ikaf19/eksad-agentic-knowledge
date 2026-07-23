# Roadmap — EKSAD Agentic Knowledge Source of Truth

**Status:** Current canonical roadmap  
**Last normalized:** 2026-07-23
**Runtime mutation policy:** This repository defines desired state, policies, contracts, templates, and validators only. Runtime activation of Hermes profiles, MCP tools, RAG services, LiteLLM, Keycloak, Web Portal, or provider credentials always requires a separate explicit approval gate.

---

## 1. Current baseline

The repository has moved beyond the initial bootstrap plan. The current mainline baseline is an **agentic knowledge source-of-truth** for EKSAD AI Software Factory work.

Current baseline includes:

| Area | Current state |
|---|---|
| Canonical knowledge pack | `EKSAD/gpt/` curated base and templates, excluding project-specific/on-hold material unless explicitly activated. |
| Portable layer | Runtime-neutral roles, workflows, deliverables, approval boundaries, MCP/RAG/LLM policy. |
| Role coverage | 13 canonical role definitions and source activation mappings: General Coordinator, BA, SA, TL, Dev-BE, Dev-FE, QA, PM, DevOps, Data Analyst, Data Scientist, UI/UX Designer, Content Creator. Live activation remains separate. |
| Hermes adapter | Role system instructions, EKSAD skills, per-role knowledge index, RAG/MCP guidance. |
| Chatbot project support | GPT/Claude project guidance where MCP/RAG/LLM gateway docs are governance/reference unless the platform provides tools. |
| MCP desired state | Top-level `mcp/` catalog with manifests, security/install/validation docs, adapters, profiles, renderer/doctor/validator. |
| RAG desired state | Top-level `rag/` corpus manifests, retrieval/citation/security policy, API/tool contracts, adapters, eval fixtures, validators. |
| LLM Gateway desired state | Top-level `llm-gateway/` LiteLLM/OpenAI-compatible alias/routing/budget/guardrail/fallback/observability policy. |
| Portable Portal foundation | `DeliveryProfile`, `ExternalWorkItemLink`, and JIRA-first orchestrator-dependency contracts; current JIRA mode is link-only/manual. |
| Future alignment backlog | Web Portal Control Plane and JIRA-First Orchestrated Delivery plans parked under `docs/future/`; JIRA-first depends on the future orchestrator layer. |

---

## 2. Source-of-truth layers

```text
Level 1 — Portable / agent-agnostic source of truth
  EKSAD/gpt/
  portable/roles/
  portable/workflows/
  portable/deliverables/
  portable/policies/
  portable/mcp/
  portable/rag/
  portable/llm-gateway/
  portable/portal/

Level 1.5 — Desired-state capability catalogs
  mcp/
  rag/
  llm-gateway/

Level 2 — Runtime adapters
  agent-adapters/hermes/
  agent-adapters/chatbot-projects/
  agent-adapters/generic/
  agent-adapters/<future>/

Level 3 — Runtime local state, never committed
  live Hermes config
  live MCP config
  RAG indexes / embedding cache / vector stores
  LiteLLM config / DB / keys / logs
  Keycloak realm exports containing secrets
  Web Portal runtime config / DB dumps
  provider credentials, tokens, passwords, PATs
```

---

## 3. Completed roadmap slices

| Slice | Status | Canonical evidence |
|---|---|---|
| Initial repository foundation | Completed | `README.md`, `docs/SOURCE_MIGRATION.md`, `portable/`, `agent-adapters/hermes/` |
| Chatbot project compatibility | Completed | `docs/USAGE_MODES.md`, `agent-adapters/chatbot-projects/` |
| MCP foundation | Completed | `mcp/README.md`, `mcp/servers/*/manifest.json`, `mcp/scripts/validate-mcp-catalog.py` |
| RAG foundation | Completed | `rag/README.md`, `rag/corpora/*.manifest.json`, `eval/rag/`, `rag/scripts/validate-rag-corpus.py` |
| RAG API/tool contract enrichment | Completed | `rag/RAG_API_CONTRACT.md`, `rag/RAG_TOOL_CONTRACT.md`, `mcp/servers/rag-api-readonly/` |
| LLM gateway foundation | Completed | `llm-gateway/README.md`, `llm-gateway/aliases/eksad-model-aliases.json`, `eval/llm-gateway/` |
| Role expansion to 13 roles | Completed | `portable/roles/`, `portable/workflows/`, `agent-adapters/hermes/role-system-instructions/` |
| Role matrix and skill hardening | Completed | `portable/roles/role-collaboration-matrix.md`, `agent-adapters/hermes/skill-enrichment-benchmark.md`, validators |
| Web Portal Control Plane future plan | Parked | `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` |
| Portable Portal delivery-mode foundation | Completed | `portable/portal/`, `scripts/validate-portal-delivery-mode.py`, PR #5 |
| Source-of-Truth Roadmap Normalization (NEXT-03) | Completed | `docs/ROADMAP.md`, `docs/PHASE_HISTORY.md`, `docs/NEXT_PHASE_CANDIDATES.md`, PR #5 |

See `docs/PHASE_HISTORY.md` for historical merge/phase detail.

---

## 4. Active next-phase candidates

The next active phase is selected explicitly by the user. The roadmap does not imply runtime activation.

| Candidate | Name | Purpose | Recommended before/after |
|---|---|---|---|
| NEXT-02 | Runtime Activation Readiness Blueprint | Define render/dry-run/apply boundaries for Hermes profiles, MCP manifests, RAG corpora, and LiteLLM aliases. | Before any runtime pilot. |
| NEXT-04 | RAG Ingestion and Evaluation Pilot Plan | Define corpus ingestion order, citation evals, role-boundary retrieval tests, and non-prod RAG blueprint. | After roadmap normalization or runtime readiness. |
| NEXT-05 | MCP Runtime Pilot Plan | Pick a small read-only MCP pilot set with access, approval, and observability rules. | After runtime readiness. |
| NEXT-06 | Web Portal Control Plane Source-of-Truth | Start WPC-01 from the parked Web Portal future plan. | After harness baseline is stable, unless user prioritizes portal earlier. |
| NEXT-07 | Orchestrator Layer Source-of-Truth | Define role workflow graph, HITL gates, handoff/evidence registry, and Portal -> Orchestrator contract. | Before JIRA-first can become active. |
| NEXT-08 | JIRA-First Orchestrated Delivery Mode | Start JFD-01 from the parked JIRA-first plan after orchestrator foundations exist. | After NEXT-07 / ORC foundation. |

See `docs/NEXT_PHASE_CANDIDATES.md` for detailed scope and exit criteria.

---

## 5. Parked future workstreams

| Workstream | Status | Canonical plan |
|---|---|---|
| Web Portal Control Plane | Parked future alignment plan | `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` |
| JIRA-First Orchestrated Delivery | Parked future alignment plan; depends on future orchestrator | `docs/future/FUTURE_ALIGN_JIRA_FIRST_ORCHESTRATED_DELIVERY.md` |
| Future runtime adapters | Future | Add only after portable contracts remain stable. |
| Project-specific domain activation | Future/explicit | TIA/USED-CAR or customer-specific material must be activated per project, not merged into the portable base by default. |

---

## 6. Validation entrypoints

Run the current source-of-truth validation suite from repo root:

```bash
./scripts/validate-all.sh
```

This canonical entrypoint includes role, skill-suite, portable, MCP, RAG, LLM Gateway, roadmap, Portal, source-consistency, isolated resync, and secret-scan gates. Validation is read-only and must not mutate active runtime state.
