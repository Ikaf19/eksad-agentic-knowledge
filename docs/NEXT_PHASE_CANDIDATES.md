# Next Phase Candidates

**Status:** Candidate queue / not auto-approved  
**Last normalized:** 2026-07-16  
**Rule:** A candidate becomes active only after explicit user selection. Runtime apply/deploy remains a separate approval gate.

---

## Selection guidance

Pick the next phase by deciding whether the priority is **runtime readiness**, **RAG pilot**, **MCP pilot**, or **Web Portal source-of-truth**.

```text
If goal is safer runtime adoption -> NEXT-02
If goal is doc/status cleanup -> NEXT-03
If goal is retrieval quality -> NEXT-04
If goal is tool access pilot -> NEXT-05
If goal is portal/control plane -> NEXT-06 / WPC-01
```

---

## NEXT-02 — Runtime Activation Readiness Blueprint

**Purpose:** Define the safe path from Git desired-state to runtime configuration without applying changes by default.

**Scope:**

- Render/dry-run/apply policy for Hermes profiles and skills.
- MCP manifest to runtime config render flow.
- RAG corpus manifest to ingestion plan render flow.
- LLM Gateway alias manifest to LiteLLM/OpenAI-compatible config render flow.
- Approval gates for runtime writes, provider keys, production tool access, DB access, and deployment actions.
- Operator checklist and rollback/restore notes.

**Non-goals:**

- No live Hermes profile mutation.
- No MCP installation.
- No RAG index build.
- No LiteLLM config write or key creation.

**Exit criteria:**

- Operators can see exactly what would be rendered/applied.
- Default mode is dry-run/read-only.
- Runtime apply steps require explicit approval and local secret injection.

---

## NEXT-03 — Source-of-Truth Roadmap Normalization

**Purpose:** Keep navigation, phase history, and candidate roadmap aligned with the current 13-role/MCP/RAG/LLM baseline.

**Scope:**

- `docs/ROADMAP.md`
- `docs/PHASE_HISTORY.md`
- `docs/NEXT_PHASE_CANDIDATES.md`
- README navigation updates.
- `docs/GRAND_PLAN.md` historical/current-status clarification.
- Optional roadmap consistency validator.

**Exit criteria:**

- Current baseline is clear from README and docs.
- Historical initial-plan wording is not mistaken for active status.
- Web Portal is parked as future workstream, not forced into Phase G/H/I/J.
- Validation suite and secret scan pass.

---

## NEXT-04 — RAG Ingestion and Evaluation Pilot Plan

**Purpose:** Prepare a non-prod RAG pilot with reliable corpus selection, citation quality, and role-boundary tests.

**Scope:**

- Corpus ingestion priority and environment boundary.
- Golden-question expansion per role.
- Citation/abstention tests.
- Role-boundary retrieval tests.
- Render-only ingestion plan improvements.
- Pilot success metrics for retrieval quality and evidence traceability.

**Non-goals:**

- No Milvus collection creation.
- No embedding run.
- No customer data ingestion.
- No live RAG API deployment.

**Exit criteria:**

- Non-prod RAG pilot can be reviewed before runtime activation.
- Evaluation cases cover correctness, abstention, citation, and role-boundary behavior.

---

## NEXT-05 — MCP Runtime Pilot Plan

**Purpose:** Select a small, read-only MCP pilot set and define runtime access, approval, and observability before enabling tools.

**Candidate pilot servers:**

- `github-readonly` or `gitlab-readonly`
- `openapi-contract`
- `postgres-schema-readonly`
- `rag-api-readonly`
- optionally `observability-readonly`

**Scope:**

- Pilot role allowlist.
- Runtime environment prerequisites.
- Approval gate and fallback process.
- Audit/observability requirements.
- Failure and rollback procedure.

**Non-goals:**

- No production write tools.
- No broad secret access.
- No default global enablement.

**Exit criteria:**

- MCP pilot is safe, role-scoped, read-only-first, and reversible.

---

## NEXT-06 — Web Portal Control Plane Source-of-Truth

**Purpose:** Start WPC-01 from the parked Web Portal future plan.

**Canonical future plan:**

- `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md`

**Scope:**

- Add top-level `portal/` desired-state docs.
- Define Keycloak OIDC contract.
- Define Portal -> LiteLLM admin/control-plane contract.
- Define budget, routing, fallback, approval, audit, observability, and project-agent model.
- Add portal validator.

**Non-goals:**

- No Web Portal deployment.
- No Keycloak mutation.
- No LiteLLM virtual key creation.
- No provider key storage.

**Exit criteria:**

- Web Portal is first-class in Git source-of-truth and still runtime-safe.
