# Grand Plan — EKSAD Agentic Knowledge Initial Repository

**Status:** ✅ APPROVED 2026-07-13 — user requested initial commit to `Ikaf19/eksad-agentic-knowledge` on branch `feat/initial-commit`  
**Workspace:** `/workspace`  
**Target repository:** `https://github.com/Ikaf19/eksad-agentic-knowledge`  
**Target branch:** `feat/initial-commit`  
**Runtime mutation policy:** Git-only source commit; do not install/configure runtime MCP, do not modify live Hermes profile/config unless separately approved.

---

## 1. Goal

Create a new curated Git source-of-truth repository for EKSAD agentic knowledge, separated from the older `brainstorming` repository.

The new repository should be usable by Hermes today and portable to other agentic runtimes later, including Claude Code, Codex, Cursor, OpenCode, ChatGPT/Claude Projects, or custom MCP-aware agents.

The repo must contain:

1. Canonical EKSAD knowledge pack.
2. Portable agent-agnostic role/workflow/policy layer.
3. Hermes adapter layer.
4. MCP design and migration plan from P0 to Pn.
5. Safe templates/examples only — no secrets, no runtime state, no binary/cache artifacts.

---

## 2. User-confirmed decisions

| # | Decision | Status |
|---:|---|---|
| 1 | Create a new repository instead of continuing inside `brainstorming`. | Confirmed |
| 2 | Repository name: `eksad-agentic-knowledge`. | Confirmed by user creating repo |
| 3 | Git remains source of truth. | Confirmed |
| 4 | Repo must support non-Hermes agentic runtimes later. | Confirmed |
| 5 | Split portable knowledge from Hermes-centric adapter. | Confirmed |
| 6 | Include MCP design in the grand plan through MCP Pn. | Confirmed |
| 7 | Commit branch should be `feat/initial-commit`. | Confirmed |

---

## 3. Source-of-truth layering model

```text
Level 1 — Portable / agent-agnostic source of truth
  EKSAD/gpt/_base/
  EKSAD/gpt/_template/
  portable/roles/
  portable/workflows/
  portable/deliverables/
  portable/policies/
  portable/mcp/

Level 2 — Agent adapters
  agent-adapters/hermes/
  agent-adapters/claude-code/    # future
  agent-adapters/codex/          # future
  agent-adapters/cursor/         # future
  agent-adapters/generic/        # future

Level 3 — Runtime local state, never committed
  ~/.hermes/config.yaml
  ~/.hermes/.env
  live MCP config
  tokens/passwords
  downloaded MCP binaries
  codebase-memory caches/indexes
  CI/CD credentials
```

Rules:

- Portable knowledge must not reference Hermes-only commands or paths.
- Hermes adapter may reference Hermes profiles, `SOUL.md`, SKILL.md, MCP config snippets, and resync scripts.
- Runtime config must be generated/applied locally from adapter templates and local env, not committed.
- Skills must be MCP-aware but fallback-safe.
- MCP use never implies approval to merge, deploy, write DB, or accept risk.

---

## 4. Initial repository shape

```text
.
├── README.md
├── .gitignore
├── docs/
│   ├── GRAND_PLAN.md
│   └── SOURCE_MIGRATION.md
├── EKSAD/
│   └── gpt/                         # copied canonical EKSAD pack only; excludes TIA/USED-CAR
├── portable/
│   ├── README.md
│   ├── roles/
│   ├── workflows/
│   ├── deliverables/
│   ├── policies/
│   └── mcp/
├── agent-adapters/
│   └── hermes/
│       ├── README.md
│       ├── per-role-knowledge-index.md
│       ├── role-system-instructions/
│       ├── hermes-skills/
│       ├── scripts/
│       └── mcp/
└── scripts/
    └── validate-portable.py
```

---

## 5. MCP Grand Plan P0–Pn

### P0 — Governance and safe foundation

| Item | Portable source | Hermes adapter | Success criteria |
|---|---|---|---|
| MCP policy | `portable/policies/mcp-policy.md` | linked from Hermes adapter docs | Read-only-first, no secrets, no prod write by default |
| Role MCP matrix | `portable/mcp/role-mcp-matrix.md` | referenced by Hermes role/SKILL docs later | All 9 roles mapped to allowed/optional/forbidden capabilities |
| Capability catalog | `portable/mcp/capability-catalog.md` | server examples map to capabilities | MCP described as capability, not Hermes feature |
| Codebase memory pilot | `portable/mcp/server-catalog.md` | `agent-adapters/hermes/mcp/servers/codebase-memory.hermes.example.yaml` | Controlled pilot only; no auto-index/global default |
| Git read-only capability | `portable/mcp/capability-catalog.md` | GitHub/GitLab examples later | Git evidence available without broad write permissions |

### P0.1 — Persona boundary integration

| Item | Target | Notes |
|---|---|---|
| Add MCP boundary section to portable role cards | `portable/roles/*.md` | Tool access does not change role accountability |
| Add Hermes references later | `agent-adapters/hermes/role-system-instructions/*.md` | Follow portable role cards; no runtime sync yet unless approved |
| Keep General profile as router | `portable/roles/general-coordinator.md` | Does not own specialist output |

### P0.2 — Skill MCP awareness

| Item | Target | Rule |
|---|---|---|
| Make Hermes skills MCP-aware | `agent-adapters/hermes/hermes-skills/**/SKILL.md` | Phrase: “If configured and allowed…” |
| Add fallback path | same | Every MCP step must have manual/file fallback |
| No hard dependency | same | Skill remains usable without MCP |

### P1 — Evidence and engineering capability expansion

| Capability | Roles | Portable doc | Hermes example | Boundary |
|---|---|---|---|---|
| Jenkins read-only | DevOps, PM, TL, QA | MCP catalog | `jenkins-readonly.hermes.example.yaml` | evidence only |
| SonarQube read-only | TL, DevOps, PM | MCP catalog | `sonarqube-readonly.hermes.example.yaml` | quality evidence only |
| Trivy/SBOM evidence | AppSec, TL, DevOps | MCP catalog | `trivy-evidence.hermes.example.yaml` | evidence does not equal risk acceptance |
| PostgreSQL schema read-only | SA, Dev-BE, QA, DevOps | MCP catalog | `postgres-schema-readonly.hermes.example.yaml` | schema only; no data mutation |
| OpenAPI contract | SA, Dev-BE, Dev-FE, QA | MCP catalog | `openapi-contract.hermes.example.yaml` | contract inspection/validation |
| Playwright/browser scoped | Dev-FE, QA | MCP catalog | `playwright-browser.hermes.example.yaml` | scoped URLs only |

### P2 — Optional integration capabilities

| Capability | Roles | When to add | Default |
|---|---|---|---|
| RabbitMQ read-only | SA, Dev-BE, DevOps, TL | Real event topology validation needed | Off |
| Kafka read-only | SA, Dev-BE, DevOps, TL | Real topic/consumer-group validation needed | Off |
| MongoDB read-only | SA, QA, DevOps | Audit schema/evidence needed | Off |
| Figma read-only | BA, FE, SA | Design source becomes active | Off |
| Observability read-only | DevOps, TL, QA, PM | Logs/metrics/traces evidence needed | Off |
| Jira/Linear/Notion read-only | PM, BA, General | Project tooling is standardized | Off |

### P3 — Validation and migration safety

| Item | Purpose |
|---|---|
| Portable validator | Ensure role cards, MCP matrix, and policy docs exist and cover all roles |
| Secret scanner | Reject committed token/password/connection-string patterns |
| Hermes adapter validator | Ensure Hermes examples/templates do not contain live secrets |
| Matrix consistency check | Ensure every role in `portable/roles` appears in MCP matrix |
| Adapter drift check | Ensure Hermes adapter references portable docs instead of becoming a second source of truth |

### P4 — Controlled runtime apply, explicitly approved only

| Item | Rule |
|---|---|
| MCP doctor | Read-only environment check |
| MCP render config | Generate local config snippet only |
| MCP print commands | Print exact `hermes mcp add` or config edit instructions |
| MCP apply | Optional future, default disabled/dry-run |
| Runtime sync | Separate approval gate from Git commit |

### Pn — Future runtime adapters and connectors

| Future area | Policy |
|---|---|
| Claude Code adapter | Add only after portable layer stabilizes |
| Codex adapter | Add only after portable layer stabilizes |
| Cursor rules | Add as adapter generated from portable role/workflow docs |
| OpenCode adapter | Add as adapter generated from portable docs |
| Additional MCP servers | Add capability first, then server example, then adapter config |
| Production-write MCP | Forbidden by default; requires explicit project-specific approval and audit trail |

---

## 6. Implementation phases

| Phase | Status | Output |
|---|---|---|
| Phase 1 — Local repo bootstrap | In progress | `/workspace/eksad-agentic-knowledge` on branch `feat/initial-commit` |
| Phase 2 — Copy canonical pack | Pending | `EKSAD/gpt/` only, excluding `TIA/` and `USED-CAR/` |
| Phase 3 — Add portable layer | Pending | `portable/*` docs and role/MCP matrix |
| Phase 4 — Add Hermes adapter layer | Pending | `agent-adapters/hermes/*` copied/organized plus MCP examples |
| Phase 5 — Validate safety | Pending | no secrets, no runtime cache, role matrix complete |
| Phase 6 — Commit local branch | Pending | local Git commit `feat: initial EKSAD agentic knowledge source` |
| Phase 7 — Push remote branch | Blocked until credential | `origin/feat/initial-commit` on GitHub |

---

## 7. Known blocker

At execution start, this environment had no GitHub auth:

- `gh` not installed.
- No `GITHUB_TOKEN` env.
- No `~/.hermes/.env` `GITHUB_TOKEN`.
- No `~/.git-credentials` GitHub credential.
- SSH GitHub auth failed.
- GitHub API returned 404 for unauthenticated repo lookup, likely because repo is private or not public-accessible.

Therefore, remote push requires one of:

1. User provides a GitHub PAT with repo write access.
2. User configures SSH key for GitHub on this environment.
3. User makes the repo public temporarily and provides write auth separately.
4. User pushes the prepared local branch manually from another machine.

Until then, complete all local source work and local commit.

---

## 8. Validation checklist

- [ ] No `.env` committed.
- [ ] No token/password/PAT/connection string committed.
- [ ] No `~/.hermes/config.yaml` committed.
- [ ] No runtime MCP binaries committed.
- [ ] No `.codebase-memory/` cache committed.
- [ ] `TIA/` excluded unless explicitly reactivated.
- [ ] `USED-CAR/` excluded unless project-specific activation requested.
- [ ] Portable docs do not contain Hermes-only path assumptions.
- [ ] Hermes adapter docs clearly marked as Hermes-specific.
- [ ] MCP P0–Pn appears in `docs/GRAND_PLAN.md`.
- [ ] Commit exists on branch `feat/initial-commit`.
- [ ] Remote branch verified after push.

---

## 9. Next-session continuation instructions

If a new session resumes this work:

1. Open this plan file first:
   `/workspace/.hermes/plans/2026-07-13_081105-eksad-agentic-knowledge-initial-repo.md`
2. Check local repo:
   `/workspace/eksad-agentic-knowledge`
3. Run:
   `git status && git branch --show-current && git log --oneline -5`
4. If local commit exists but push not done, resolve GitHub auth and push:
   `git push -u origin feat/initial-commit`
5. If source structure needs continuation, prioritize validators and MCP P1/P2 examples next.

---

## 10. Deferred work after initial commit

| Trigger | Action |
|---|---|
| User says “sync runtime Hermes” | Inspect resync script, update for new repo layout if needed, then ask approval before modifying live profiles/skills. |
| User says “enable MCP P0” | Run MCP doctor only; do not install until explicit runtime approval. |
| User says “add Claude/Codex/Cursor adapter” | Generate adapter from portable layer, do not fork portable source. |
| User says “activate TIA/USED-CAR” | Treat as project-specific activation; do not merge into portable base by default. |

---

## 11. Execution Update — 2026-07-13_084321 UTC

| Item | Result |
|---|---|
| Local repo path | `/workspace/eksad-agentic-knowledge` |
| Branch | `feat/initial-commit` |
| Local commit | Created on `feat/initial-commit`; run `git rev-parse --short HEAD` for the current SHA |
| Files committed | 239 files |
| Validation | `scripts/validate-portable.py` PASS; `agent-adapters/hermes/mcp/scripts/eksad-mcp-validate.py` PASS |
| Exclusions verified | `TIA/` and `USED-CAR/` excluded |
| Push status | PUSHED — `origin/feat/initial-commit` created on GitHub |
| Remote branch | `https://github.com/Ikaf19/eksad-agentic-knowledge/tree/feat/initial-commit` |
| PR URL | `https://github.com/Ikaf19/eksad-agentic-knowledge/pull/new/feat/initial-commit` |

### Remote delivery note

Push used a one-time GitHub PAT via temporary `GIT_ASKPASS` and `git -c credential.helper=`. The token was not written into `.git/config`, remote URL, or Git credential helper by this workflow.

### Next action for a new session

```bash
cd /workspace/eksad-agentic-knowledge
git status --short
git branch --show-current
git rev-parse --short HEAD
```

Then continue with one of:

1. Open/merge PR for `feat/initial-commit`.
2. Add P1 validators/scripts.
3. Start Hermes runtime resync assessment.
4. Start MCP P0 runtime assessment.

## Chatbot Project Mode Addition

User confirmed the repository must remain usable in both:

1. **Chatbot project mode** — GPT Project / Claude Project / uploaded knowledge project, no tools or MCP assumed.
2. **Fully agentic mode** — Hermes / Claude Code / Codex / Cursor / OpenCode, with optional tools and MCP governed by role matrix.

Added adapter scope:

```text
agent-adapters/chatbot-projects/
├── README.md
├── shared/PROJECT_USAGE_RULES.md
├── gpt-project/
│   ├── README.md
│   └── PROJECT_INSTRUCTIONS_TEMPLATE.md
└── claude-project/
    ├── README.md
    └── PROJECT_INSTRUCTIONS_TEMPLATE.md

agent-adapters/generic/README.md
docs/USAGE_MODES.md
```

Rule: GPT/Claude Project mode uses `EKSAD/gpt/` and `portable/` as uploaded knowledge exactly like the prior chatbot workflow, while MCP docs remain governance/reference only unless a platform provides actual tools.



## MCP Foundation Implementation Update

The next phase adds top-level `mcp/` as a reusable MCP desired-state template for both Hermes and future agentic harnesses.

Scope:

- `mcp/README.md` as canonical MCP entrypoint.
- `mcp/ROADMAP_P0_TO_PN.md`, `SETUP_FLOW.md`, `SECURITY_MODEL.md`, and `SERVER_MANIFEST_SCHEMA.md`.
- Machine-readable `manifest.json` per MCP server candidate.
- Per-server install, security, validation, Hermes adapter, and generic harness adapter files.
- Per-role MCP profile docs.
- Read-only scripts: `doctor.sh`, `validate-mcp-catalog.py`, `render-hermes-config.py`.

Runtime apply remains a separate explicit approval gate. No secrets, binaries, caches, or live config are committed.

## RAG Foundation Implementation Update

Phase B adds top-level `rag/` as a reusable retrieval desired-state template for Hermes, chatbot projects, and future agentic harnesses.

Scope:

- `rag/README.md` as canonical RAG entrypoint.
- RAG architecture, corpus schema, indexing policy, chunking profiles, retrieval contract, citation policy, security model, and evaluation plan.
- Machine-readable corpus manifests under `rag/corpora/*.manifest.json`.
- Per-role RAG profiles under `rag/profiles/`.
- Adapter guidance for Hermes, generic harnesses, and chatbot projects under `rag/adapters/`.
- Portable RAG governance under `portable/rag/` and `portable/policies/rag-policy.md`.
- Eval fixtures under `eval/rag/` for golden questions, expected citations, abstention, and role-boundary behavior.
- Read-only scripts: `rag/scripts/validate-rag-corpus.py`, `rag/scripts/render-ingestion-plan.py`, `rag/scripts/build-chatbot-upload-bundle.py`, and `eval/rag/scripts/validate-rag-eval.py`.

Runtime apply remains a separate explicit approval gate. No vector stores, embedding caches, customer dumps, secrets, provider keys, or live RAG config are committed.
