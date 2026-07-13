# EKSAD Company GPT — Project Tracker & Setup Guide

**Created:** 2026-04-23
**Owner:** EKSAD Platform Team
**Last Updated:** 2026-07-11 (v31 — full curated skill suite; UR, Test Plan/RTM, ADR, WBS, Project Closure, and Threat Model templates; FE real-API-first alignment; BA greenfield decomposition; canonical wiring and validation.)
**Active source branch:** `feature/eksad-knowledge-v3`

**Previous:** 2026-07-11 (v30 — DevOps role, GitLab CE/Jenkins/SonarQube/Trivy delivery contract, AI Software Factory architecture, five operational templates, Hermes profile, and fail-closed delivery skill.)

**Previous:** 2026-06-09 (v28 — BRD template v3.2: removed technical NFR/assumption/dependency scope from BRD; added Project Charter and Regulatory references; added standalone Regulatory & Compliance template.)

**Previous:** 2026-06-02 (v27 — Follow-up dari v26: `_base/EKSAD_CRUDFLOWS_JPA.md` dibuat — blocking counterpart dari `EKSAD_CRUDFLOWS_PATTERN.md`, mendokumentasikan `BaseJpaRepository` untuk Spring Boot + Quarkus-imperative (artifact `eksad-core-jpa`); mencakup flow surface, worked examples kedua runtime, tabel reactive-vs-blocking, transaction boundary, dan forbidden patterns. `ADR_EKSAD_CORE_COMMON_SPLIT.md` dipindahkan dari `_plan/` ke `_base/` (lebih tepat sebagai knowledge file untuk diupload ke GPT). Keduanya didaftarkan di knowledge tree + upload table README.)

**Previous:** 2026-06-02 (v26 — Brainstorming decisions D1–D5 / G1–G5 applied: `tenant_id` locked to `String`/`VARCHAR(100)`, `version` column removed, `deleted_by` → `VARCHAR(100)`, `getUserContext()` → `currentTenantId()` helpers; `CURSOR_DEV_RULES.md` re-derived to CrudFlows v2 (4 contract methods, paired interfaces, `auditMutator`); corrected "BaseRepository used in Spring Boot too" claim — imperative uses `eksad-core-jpa` artifact; Quarkus `3.18.1` → `3.30.6` across all active primers; SA `EKSAD_CODING_STANDARDS.md` policy resolved — read-only design reference allowed; `EKSAD_CRUDFLOWS_PATTERN.md` + `ADR_EKSAD_CORE_COMMON_SPLIT.md` registered in knowledge tree.)

**Previous:** 2026-05-31 (v25 — QA enablement Step 4 (vibe-coding docs alignment): `vibe-coding/PLAN_VIBE_CODING.md` → added **Phase 6 — QA Automation Agent** (folder tree `qa/`, tasks 39–45, 6 handoff decisions, maintenance-policy row, status header); `vibe-coding/VIBE_CODING_SETUP_GUIDE.md` → QA Engineer row added to Role→File map + two-surface note (Mode A GPT vs Mode B in-IDE agent, test-code-only); `vibe-coding/PLAN_FIRST_WORKFLOW.md` → `qa` added to "Applies to" + 3 QA files in Reference list + QA variant note (`TESTPLAN_<MODULE>.md` in `docs/eksad/testplans/`). QA enablement (Steps 1–4) now complete.)

**Previous:** 2026-05-31 (v24 — QA enablement Step 3 (Mode A GPT alignment): `qa/QA_SYSTEM_INSTRUCTIONS.md` + `qa/QA_SYSTEM_INSTRUCTIONS_SHORT.md` updated — framed as **Mode A (Design)** companion vs Mode B in-IDE agent (`vibe-coding/qa/`); added Two-Operating-Modes table + handoff rule (emit stable `TC-NNN` IDs for the Mode B agent); referenced `§2.1` ownership (unit + internal integration are developer-owned, not QA) and `§2.2`; added **RTM** as first Mode A deliverable (new Step 0 + Output Rule + scope item, ref `§12.0`); clarified "Outside Your Scope" now excludes unit/internal-integration tests and script-authoring.)

**Previous:** 2026-05-31 (v23 — QA enablement Step 2 (vibe-coding QA agent): new `vibe-coding/qa/` folder with 3 in-IDE instruction files — `COPILOT_QA_INSTRUCTIONS.md`, `CLAUDE_CODE_QA_INSTRUCTIONS.md`, `CURSOR_QA_RULES.md`. QA **Mode B (Automation)** agent: writes test code only (REST Assured / Playwright / k6), reads prod code read-only, operates on staging branches, writes confined to `src/test/**` · `e2e/**` · `perf/**` · `security/**`; Phase 0 generates `TESTPLAN_<MODULE>.md` (Scope · Env · RTM · Test Case Matrix · State Machine Matrix · Automation Tracker); Plan Gate before writing tests; mandatory coverage checklist (401/403/cross-tenant/validation/state-machine/soft-delete/audit-exists); bug-report-instead-of-fixing-prod rule; Stack-Profile aware. Mirrors `vibe-coding/developer/` structure.)

**Previous:** 2026-05-31 (v22 — QA enablement Step 1 (Test Ownership + Modes): `EKSAD_TESTING_GUIDE.md` → v1.3 (new §2.1 **Test Ownership Matrix** — developer owns unit + internal integration (white-box), QA owns API/acceptance + cross-service E2E + FE E2E (Playwright) + non-functional (k6) black-box; overlap rule resolved; new §2.2 **QA Operating Modes A (Design, FSD→test plan/RTM/matrix) & B (Automation, TSD+PLAN→REST Assured/E2E)** with Mode-B in-IDE agent scope = test-code-only, read prod read-only, staging branches, writes confined to `src/test/**` etc.; new §12.0 **RTM (Requirement Traceability Matrix) template**; TOC + version bumped). Decisions: FE E2E default = Playwright (provisional, team to confirm); QA agent read-only on prod code.)

**Previous:** 2026-05-31 (v21 — CSRF stateless clarification + optional Redis upgrade path: `EKSAD_CORE_AUTH_PATTERNS.md` → v1.3 (§11.3.1 reworded to state default is **stateless / zero-infra, no Redis** — security from same-origin policy; added plain vs **signed double-submit** variants table — signed = `HMAC(jti, EKSAD_AUTH_SIGNING_KEY_SECRET)`, recomputed from JWT `jti`, still stateless; clarified no separate XSRF revocation needed — sign-out already covered by refresh-token revoke + cookie clear; new §11.3.2 **Stateful Synchronizer Token via Redis** optional upgrade — when to use, `xsrf:{sessionId}` key schema, TTL aligned to refresh-token lifetime (avoids mid-session expiry), rotate/DEL lifecycle for self-revocation on sign-out, shared-Redis + fail-closed rules; 3 new env vars `EKSAD_AUTH_CSRF_STORE` / `EKSAD_AUTH_CSRF_REDIS_KEY_PREFIX` / `EKSAD_AUTH_CSRF_REDIS_TTL_DAYS`).)

**Previous:** 2026-05-31 (v20 — CSRF protection + glossary alignment: `EKSAD_CORE_AUTH_PATTERNS.md` → v1.2 (added §11.3.1 CSRF Protection double-submit cookie for browser/cookie mode; 3 new env vars `EKSAD_AUTH_COOKIE_XSRF_NAME` / `EKSAD_AUTH_CSRF_ENABLED` / `EKSAD_AUTH_CSRF_HEADER_NAME`; `XSRF-TOKEN` Set-Cookie added to §13 cookie login/refresh/revoke flows — non-HttpOnly, set at login, rotated on refresh, cleared on revoke); `EKSAD_DOMAIN_GLOSSARY.md` → v1.2 (A.4 renamed "Messaging (RabbitMQ & Kafka)" + Kafka terms: Topic / Partition Key / Consumer Group / DLT / Dual-Ingress; new A.4b Stack Profiles — Stack Profile / Tier-1 / Tier-2 / Transport-Agnostic Envelope).)

**Previous:** 2026-05-31 (v19 — Stack Profile + dual-broker support: `EKSAD_BASE_PRINCIPLES.md` → v1.2 (added Stack Profiles section — 3 independent axes Framework/Paradigm/Broker + Tier-1/Tier-2, broker-agnostic Principle #3, dual-ingress audit flow, replaced "Spring Boot Exception" with "Stack Profiles — Framework & Paradigm Mappings"); `EKSAD_EVENT_CATALOG.md` → v1.1 (Transport column, §1.1 Kafka Topic Registry, §6 audit dual-ingress + `AUDIT_KAFKA_ENABLED`, §11 split into 11.1 RabbitMQ / 11.2 Kafka naming convention / 11.3 transport-independent, §12 broker-aware); `EKSAD_GENERIC_TSD_TEMPLATE.md` (new §3.1 Stack Profile Decision + §10.4 Kafka Transport); SA + BA system instructions (SA Stack Profile Selection step; BA §7.1 business-language async NFR signal); vibe-coding developer + technical-leader instructions for Copilot/Claude/Cursor (Stack-Profile-aware, broker-agnostic). Default profile unchanged = Quarkus · Reactive · RabbitMQ — fully additive, no impact to existing RabbitMQ services.)

**Previous:** 2026-05-26 (v18 — `EKSAD_CORE_AUTH_PATTERNS.md` updated to v1.1: added §13 Browser-Facing Cookie Token API — `CookieTokenResource` endpoints `/cookie/login|issue|refresh|revoke`, two-API-mode comparison table, cookie security flags + env var config, Quarkus CORS + permission policy config, frontend integration guide; updated §3 endpoint table, §9 login flows, §11.3 session/cookie config)

**Previous:** 2026-05-24 (v17 — Knowledge Update Plan executed: added 16 new `_base/` knowledge files covering master data, cache sync, event catalog, CQRS, DB deployment, multi-tenancy, core-auth, core-auth client SDK, resilience, observability, reserved fields, CI/CD, load testing, frontend testing, domain registry; moved `EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` to `_template/`; updated SA + BA glossaries + coding standards + testing guide + base principles; SA instructions updated with reserved-field opt-in rule, service naming finalization, and JWKS infrastructure rule)

**Previous:** 2026-05-16 (v16 — Cleanup: deleted 10 stale files — 5 redirect stubs, 2 placeholder README_STUBs, 2 completed PLAN files, 1 raw chat log)

**Previous:** 2026-05-04 (v15 — Vibe Coding Phase 3 done: TL guides created for GitHub Copilot, Cursor, and Claude Code in `vibe-coding/technical-leader/`; all 3 phases complete; `PLAN_VIBE_CODING.md` updated to ✅ All Phases Complete)

**Previous:** 2026-05-03 (v11 — All `GPT_*_SYSTEM_INSTRUCTIONS*.md` renamed to role-prefixed AI-agnostic names (e.g. `BA_SYSTEM_INSTRUCTIONS.md`); originals archived with `_legacy-gpt-naming` suffix; all instruction files fully rewritten to be AI-agnostic (work on both ChatGPT and Claude); Quarkus version corrected to `3.18.1`; content gaps fixed: BA FORBIDDEN rule, moduleType() clarification, TL FE P2 pitfalls, QA audit trail mandatory, General Coordinator §7 table; all CLAUDE guides + master CLAUDE_SETUP_GUIDE updated; `PLAN_INSTRUCTIONS_IMPROVEMENT.md` added; `GPT_BA_SETUP_GUIDE.md` renamed to `GPT_SETUP_GUIDE.md`)

**Previous:** 2026-05-02 (v9 — BA GPT upgraded to v2.0: new comprehensive system instructions (PARTS A–E: pipeline, quality controls, gap analysis, anti-assumption rules, definition of done, prohibited behaviours); `EKSAD_BA_DOMAIN_GLOSSARY.md` added to `_base/`; `GPT_BA_SETUP_GUIDE.md` added to `business-analyst/`; `archive/` folder added to `business-analyst/`; fixed `from this folder` path references in SA, QA, TL, Dev instruction files → now correctly reference `_template/`)

> 🤖 **Using Claude instead of ChatGPT?**
> See [`CLAUDE_SETUP_GUIDE.md`](CLAUDE_SETUP_GUIDE.md) for complete Claude setup instructions.
> Covers **Pro/Team tier** (Claude Projects — persistent) and **Free tier** (manual session primer — no setup needed).
> Per-role Claude guides are in each role subfolder alongside the GPT guides.

> 📋 **ChatGPT setup:** Use the nine role setup sections in this README for General Coordinator, BA, SA, TL, Backend, Frontend, and QA. PM and DevOps also have maintained per-role GPT setup guides in their folders. There is no separate master GPT setup file.

> 🖥️ **Using an IDE (VS Code / Cursor / Claude Code)?**
> See [`vibe-coding/VIBE_CODING_SETUP_GUIDE.md`](vibe-coding/VIBE_CODING_SETUP_GUIDE.md) — drop a config file into your project repo and get AI code assist that auto-applies EKSAD standards as you type.
> Supports: **GitHub Copilot**, **Cursor**, **Claude Code**. Phase 1 (BE Developer) is ready.

---

## 🧭 GPT Architecture Overview

```
EKSAD has exactly 9 Custom GPTs: one General Coordinator plus eight specialists.

┌───────────────────────────────────────────────────────────────────────┐
│                    EKSAD General Coordinator GPT                      │
│   Intake · routing · cross-role sequencing · attributable synthesis   │
│   Coordinates specialists; does not author specialist deliverables    │
└───────────────────────────────────────────────────────────────────────┘
                │              │              │              │
                ▼              ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Business       │ │ System         │ │ Technical      │ │ Backend        │
│ Analyst        │ │ Analyst        │ │ Leader         │ │ Developer      │
│ UR/BRD/FSD     │ │ TSD/design     │ │ Code review    │ │ Java/Quarkus   │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
                │              │              │              │
                ▼              ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Frontend       │ │ QA Engineer    │ │ Project        │ │ DevOps         │
│ Developer      │ │ Mode A design  │ │ Manager        │ │ Engineer       │
│ React/TS       │ │ + Mode B handoff│ │ Governance     │ │ CI/CD/release  │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘

Each specialist GPT can be extended with a team-specific domain file:
  BA GPT + TIA_DOMAIN_KNOWLEDGE.md  →  TIA Reporting BA GPT
  SA GPT + HR_DOMAIN_KNOWLEDGE.md   →  HR System SA GPT
```

---

## 🗂️ Folder Structure

```
gpt/
├── README.md                               ← This file — master tracker & setup guide
├── CLAUDE_SETUP_GUIDE.md                  ← Master Claude guide (all roles, both tiers)
│
├── SYSTEM_INSTRUCTIONS.md                 ← 🆕 General Coordinator AI-agnostic system instructions (long)
├── SYSTEM_INSTRUCTIONS_SHORT.md           ← 🆕 General Coordinator short (paste into GPT/Claude)
├── GPT_CHAT_STARTERS.md                   ← General Coordinator chat starters (GPT only)
│
├── archive/                               ← ⚠️ Do NOT upload to GPT/Claude
│   ├── GPT_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│   └── GPT_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│
├── _base/                                  ← ✅ Standards & references — upload to relevant GPTs
│   ├── EKSAD_BASE_PRINCIPLES.md           → ALL GPTs
│   ├── EKSAD_SYSTEM_DESIGN_PATTERNS.md    → SA, TL, Dev
│   ├── EKSAD_DOMAIN_GLOSSARY.md           → ALL GPTs
│   ├── EKSAD_BA_DOMAIN_GLOSSARY.md        → BA GPT only (BA pipeline terms + EKSAD platform BRs)
│   ├── EKSAD_CODING_STANDARDS.md          → TL, Dev
│   ├── EKSAD_CRUDFLOWS_PATTERN.md         → TL, Dev (CrudFlows v2 — reactive, Quarkus)
│   ├── EKSAD_CRUDFLOWS_JPA.md             → TL, Dev (CrudFlows v2 — blocking JPA; Spring Boot & Quarkus-imperative)
│   ├── ADR_EKSAD_CORE_COMMON_SPLIT.md     → TL, Dev (decision: eksad-core-api / -reactive / -jpa split)
│   ├── EKSAD_TESTING_GUIDE.md             → TL, Dev, QA
│   ├── EKSAD_SPRING_BOOT_MAPPINGS.md      → SA, TL, Dev
│   ├── EKSAD_FRONTEND_CODING_STANDARDS.md → SA, TL, Dev FE
│   ├── EKSAD_FRONTEND_TESTING_GUIDE.md    → TL, Dev FE
│   │  🆕 Added 2026-05-23/24 (Knowledge Update Plan):
│   ├── EKSAD_DOMAIN_REGISTRY.md           → ALL GPTs (canonical service / port / DB registry)
│   ├── EKSAD_MASTER_DATA_PATTERNS.md      → SA, TL, Dev
│   ├── EKSAD_CACHE_SYNC_PATTERNS.md       → SA, TL, Dev
│   ├── EKSAD_EVENT_CATALOG.md             → SA, TL, Dev (exchange/routing-key registry)
│   ├── EKSAD_CQRS_PATTERNS.md             → SA, TL, Dev (RESERVED — Sprint 4+)
│   ├── EKSAD_DB_DEPLOYMENT_STRATEGY.md    → SA, TL, Dev
│   ├── EKSAD_MULTI_TENANCY_PATTERNS.md    → ALL GPTs
│   ├── EKSAD_CORE_AUTH_PATTERNS.md        → SA, TL, Dev
│   ├── EKSAD_CORE_AUTH_CLIENT_SDK.md      → TL, Dev (SDK reference for svc-user-management & adapters)
│   ├── EKSAD_RESERVED_FIELD_PATTERNS.md   → BA, SA, TL, Dev, Dev FE
│   ├── EKSAD_RESILIENCE_PATTERNS.md       → SA, TL, Dev
│   ├── EKSAD_OBSERVABILITY_PATTERNS.md    → SA, TL, Dev
│   ├── EKSAD_CICD_CONTAINER_PATTERNS.md   → TL, Dev (DevOps reference)
│   ├── EKSAD_LOAD_TESTING_GUIDE.md        → QA, TL
│   ├── EKSAD_PROJECT_MANAGEMENT_STANDARD.md → PM
│   ├── EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md → ALL GPTs (role/component/handoff awareness)
│   ├── EKSAD_DEVOPS_DELIVERY_STANDARD.md    → DevOps, PM/TL awareness
│
├── _template/                              ← ✅ Generic document scaffolds — single source of truth
│   ├── EKSAD_GENERIC_BRD_TEMPLATE.md      → BA                   ← source of truth (v3.2)
│   ├── EKSAD_GENERIC_UR_TEMPLATE.md       → BA
│   ├── EKSAD_GENERIC_REGULATORY_TEMPLATE.md → BA, SA            ← 🆕 Regulatory & Compliance Reference (standalone, not part of BRD)
│   ├── EKSAD_GENERIC_FSD_TEMPLATE.md      → BA, QA               ← source of truth (v3.0)
│   ├── EKSAD_GENERIC_TSD_TEMPLATE.md      → SA, TL, Dev           ← source of truth
│   ├── EKSAD_GENERIC_FE_TSD_TEMPLATE.md   → SA, TL, Dev FE       ← source of truth
│   ├── EKSAD_ARCHITECTURE_DOC_TEMPLATE.md → SA, TL (🆕 moved from `_base/` 2026-05-24)
│   ├── EKSAD_GENERIC_ADR_TEMPLATE.md      → SA, TL
│   ├── EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md → SA, TL, shared AppSec workflow
│   ├── EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md → QA
│   ├── EKSAD_GENERIC_WBS_TEMPLATE.md      → PM, workstream leads
│   ├── EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md → PM
│   ├── EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md → PM
│   ├── EKSAD_GENERIC_RAID_LOG_TEMPLATE.md → PM
│   ├── EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md → PM
│   ├── EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md → PM
│   ├── EKSAD_GENERIC_CICD_PIPELINE_TEMPLATE.md → DevOps
│   ├── EKSAD_GENERIC_ENVIRONMENT_READINESS_TEMPLATE.md → DevOps
│   ├── EKSAD_GENERIC_DEPLOYMENT_ROLLBACK_RUNBOOK_TEMPLATE.md → DevOps
│   ├── EKSAD_GENERIC_RELEASE_EVIDENCE_TEMPLATE.md → DevOps, PM
│   ├── EKSAD_GENERIC_INCIDENT_HANDOFF_TEMPLATE.md → DevOps
│   ├── EKSAD_GENERIC_PROJECT_CLOSURE_TEMPLATE.md → PM
│   └── archive/                           ← ⚠️ Do NOT upload to GPTs
│       ├── EKSAD_GENERIC_BRD_TEMPLATE_v2.0.md
│       └── EKSAD_GENERIC_FSD_TEMPLATE_v2.0.md
│
├── business-analyst/                       ← BA GPT/Claude files
│   ├── BA_SYSTEM_INSTRUCTIONS.md          ← 🆕 AI-agnostic long version (reference / offline use)
│   ├── BA_SYSTEM_INSTRUCTIONS_SHORT.md    ← 🆕 AI-agnostic short (paste into GPT/Claude)
│   ├── CLAUDE_BA_SETUP_GUIDE.md           ← Claude setup + Free Tier Session Primer
│   ├── GPT_BA_CHAT_STARTERS.md            ← GPT-only chat starters
│   ├── archive/                           ← ⚠️ Do NOT upload to GPTs
│   │   ├── GPT_BA_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│   │   ├── GPT_BA_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│   │   ├── GPT_BA_SETUP_GUIDE_legacy-gpt-naming.md
│   │   └── GPT_BA_SYSTEM_INSTRUCTIONS_v1.0.md
│   └── teams/                             ← team-specific domain knowledge files
│
├── system-analyst/                         ← SA GPT/Claude files
│   ├── SA_SYSTEM_INSTRUCTIONS.md          ← 🆕 AI-agnostic long version
│   ├── SA_SYSTEM_INSTRUCTIONS_SHORT.md    ← 🆕 AI-agnostic short
│   ├── CLAUDE_SA_SETUP_GUIDE.md           ← Claude setup + Free Tier Session Primer
│   ├── GPT_SA_CHAT_STARTERS.md            ← GPT-only chat starters
│   └── archive/                           ← ⚠️ Do NOT upload
│       ├── GPT_SA_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│       └── GPT_SA_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│
├── technical-leader/                       ← TL GPT/Claude files
│   ├── TL_SYSTEM_INSTRUCTIONS.md          ← 🆕 AI-agnostic long version
│   ├── TL_SYSTEM_INSTRUCTIONS_SHORT.md    ← 🆕 AI-agnostic short
│   ├── CLAUDE_TL_SETUP_GUIDE.md           ← Claude setup + Free Tier Session Primer
│   ├── GPT_TL_CHAT_STARTERS.md            ← GPT-only chat starters
│   └── archive/                           ← ⚠️ Do NOT upload
│       ├── GPT_TL_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│       └── GPT_TL_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│
├── developer/                              ← Backend + Frontend Dev GPT/Claude files
│   ├── DEV_SYSTEM_INSTRUCTIONS.md         ← 🆕 AI-agnostic long (backend)
│   ├── DEV_SYSTEM_INSTRUCTIONS_SHORT.md   ← 🆕 AI-agnostic short (backend)
│   ├── DEV_FE_SYSTEM_INSTRUCTIONS.md      ← 🆕 AI-agnostic long (frontend)
│   ├── DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md← 🆕 AI-agnostic short (frontend)
│   ├── CLAUDE_DEV_SETUP_GUIDE.md          ← Claude setup (backend) + Free Tier Session Primer
│   ├── CLAUDE_DEV_FE_SETUP_GUIDE.md       ← Claude setup (frontend) + Free Tier Session Primer
│   ├── GPT_DEV_CHAT_STARTERS.md           ← GPT-only backend starters
│   ├── GPT_DEV_FE_CHAT_STARTERS.md        ← GPT-only frontend starters
│   └── archive/                           ← ⚠️ Do NOT upload
│       ├── GPT_DEV_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│       ├── GPT_DEV_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│       ├── GPT_DEV_FE_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│       └── GPT_DEV_FE_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│
├── qa/                                     ← QA GPT/Claude files
│   ├── QA_SYSTEM_INSTRUCTIONS.md          ← 🆕 AI-agnostic long version
│   ├── QA_SYSTEM_INSTRUCTIONS_SHORT.md    ← 🆕 AI-agnostic short
│   ├── CLAUDE_QA_SETUP_GUIDE.md           ← Claude setup + Free Tier Session Primer
│   ├── GPT_QA_CHAT_STARTERS.md            ← GPT-only chat starters
│   └── archive/                           ← ⚠️ Do NOT upload
│       ├── GPT_QA_SYSTEM_INSTRUCTIONS_legacy-gpt-naming.md
│       └── GPT_QA_SYSTEM_INSTRUCTIONS_SHORT_legacy-gpt-naming.md
│
├── project-manager/                        ← PM GPT/Claude files
│   ├── PM_SYSTEM_INSTRUCTIONS.md
│   ├── PM_SYSTEM_INSTRUCTIONS_SHORT.md
│   ├── GPT_PM_SETUP_GUIDE.md
│   ├── CLAUDE_PM_SETUP_GUIDE.md
│   └── GPT_PM_CHAT_STARTERS.md
│
├── devops-engineer/                         ← DevOps GPT/Claude files
│   ├── DEVOPS_SYSTEM_INSTRUCTIONS.md
│   ├── DEVOPS_SYSTEM_INSTRUCTIONS_SHORT.md
│   ├── GPT_DEVOPS_SETUP_GUIDE.md
│   ├── CLAUDE_DEVOPS_SETUP_GUIDE.md
│   └── GPT_DEVOPS_CHAT_STARTERS.md
│
└── vibe-coding/                           ← 🆕 IDE Vibe Coding configs (Tier 3)
    ├── PLAN_VIBE_CODING.md                ← 🆕 Living plan + handoff doc (read first!)
    ├── VIBE_CODING_SETUP_GUIDE.md         ← 🆕 Master guide — all tools, all roles
    │
    ├── developer/                         ← ✅ Phase 1: BE Developer
    │   ├── COPILOT_DEV_INSTRUCTIONS.md    ← drop → .github/copilot-instructions.md
    │   ├── CURSOR_DEV_RULES.md            ← drop → .cursor/rules/eksad-dev.mdc
    │   └── CLAUDE_CODE_DEV_INSTRUCTIONS.md← drop → CLAUDE.md (project root)
    │
    ├── developer-fe/                      ← ✅ Phase 2: FE Developer
    │   ├── COPILOT_DEV_FE_INSTRUCTIONS.md ← drop → .github/copilot-instructions.md
    │   ├── CURSOR_DEV_FE_RULES.md         ← drop → .cursor/rules/eksad-dev-fe.mdc
    │   └── CLAUDE_CODE_DEV_FE_INSTRUCTIONS.md ← drop → CLAUDE.md
    │
    └── technical-leader/                  ← ✅ Phase 3: Technical Leader
        ├── COPILOT_TL_INSTRUCTIONS.md     ← drop → .github/copilot-instructions.md
        ├── CURSOR_TL_RULES.md             ← drop → .cursor/rules/eksad-tl.mdc
        └── CLAUDE_CODE_TL_INSTRUCTIONS.md ← drop → CLAUDE.md
```

---

## 🧰 Hermes Skill Suite (v31)

The source-controlled catalog contains 13 skills under `hermes-skills/`: `eksad-ba-workflow`, `eksad-tsd-design`, `eksad-adr-workflow`, `eksad-code-review`, `eksad-be-impl`, `eksad-fe-impl`, `eksad-qa-delivery`, `eksad-appsec-review`, `eksad-pm-delivery`, `eksad-devops-delivery`, `stage-gated-orchestrator`, `eksad-create-project`, and `eksad-task-breakdown`.

There are exactly nine role profiles: General Coordinator (`eksad-general`), BA, SA, TL, Backend, Frontend, QA, PM, and DevOps. **Canonical AppSec routing:** Any role may raise an AppSec trigger and supply evidence; the System Analyst or Technical Leader coordinates and invokes the shared `eksad-appsec-review` workflow; only the named risk authority accepts residual risk or grants a waiver. AppSec is not a profile. PM and DevOps use only their profile-local delivery skill at runtime.

See the repository root `README.md`, `per-role-knowledge-index.md`, and `hermes-skills/PROVENANCE.md` for canonical paths, role wiring, and provenance.

---

## 📋 File Status Tracker

### General Coordinator GPT (Coordination Only)
| # | File | Status | Purpose |
|---|------|--------|---------|
| 1 | `SYSTEM_INSTRUCTIONS.md` | Maintained | Long coordinator contract; no specialist production authority |
| 1b | `SYSTEM_INSTRUCTIONS_SHORT.md` | Maintained | Short coordinator contract for GPT/Claude |
| 2 | `GPT_CHAT_STARTERS.md` | Maintained | Intake, routing, sequencing, and synthesis starters |
| 3 | `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` | Reference only | Role, component, handoff, and evidence map |
| 4 | `_base/EKSAD_BASE_PRINCIPLES.md` | Reference only | Shared constraints for routing and consistency checks |
| 5 | `_base/EKSAD_DOMAIN_GLOSSARY.md` | Reference only | Shared terminology for cross-role synthesis |
| 6 | `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md` | Reference only | Governance and stage-gate awareness; PM remains owner |
| 7 | `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md` | Reference only | Delivery handoff awareness; DevOps remains owner |

### Business Analyst GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 8 | `business-analyst/BA_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | AI-agnostic BA system prompt (long reference) |
| 8b | `business-analyst/BA_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | **Paste into GPT/Claude** (≤8K chars) |
| 9 | `business-analyst/GPT_BA_CHAT_STARTERS.md` | ✅ Done | BA starters (GPT only) |

| 10 | `_template/EKSAD_GENERIC_BRD_TEMPLATE.md` | ✅ Done v3.2 🆕 | BRD knowledge ← upload from `_template/` (v3.2: removed NFR/Assumptions/Dependencies; added Regulatory & Charter refs) |
| 10b | `_template/EKSAD_GENERIC_REGULATORY_TEMPLATE.md` | ✅ Done 🆕 | Regulatory & Compliance Reference ← companion doc, maintained separately from BRD |
| 11 | `_template/EKSAD_GENERIC_FSD_TEMPLATE.md` | ✅ Done v3.0 | FSD knowledge ← upload from `_template/` |
| 11b | `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` | ✅ Done | BA pipeline terms + EKSAD platform BRs ← upload from `_base/` |

### System Analyst GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 12 | `system-analyst/SA_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | AI-agnostic SA system prompt (long reference) |
| 12b | `system-analyst/SA_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | **Paste into GPT/Claude** (≤8K chars) |
| 13 | `system-analyst/GPT_SA_CHAT_STARTERS.md` | ✅ Done | SA starters (GPT only) |
| 14 | `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` | ✅ Done | TSD knowledge ← upload from `_template/` |

### Technical Leader GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 15 | `technical-leader/TL_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | AI-agnostic TL system prompt (long reference) |
| 15b | `technical-leader/TL_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | **Paste into GPT/Claude** (≤8K chars) |
| 16 | `technical-leader/GPT_TL_CHAT_STARTERS.md` | ✅ Done | TL starters (GPT only) |
| 17 | `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` | ✅ Done | TSD reference ← upload from `_template/` |

### Developer GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 18 | `developer/DEV_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | AI-agnostic backend system prompt (long reference) |
| 18b | `developer/DEV_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | **Paste into GPT/Claude** (≤8K chars) |
| 19 | `developer/GPT_DEV_CHAT_STARTERS.md` | ✅ Done | Dev starters (GPT only) |

### QA GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 20 | `qa/QA_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | Mode A test-design and Mode B handoff contract (long reference) |
| 20b | `qa/QA_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | Mode A code-free contract for GPT/Claude |
| 21 | `qa/GPT_QA_CHAT_STARTERS.md` | ✅ Done | Mode A design and handoff-metadata starters |

### Project Manager GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| PM-1 | `project-manager/PM_SYSTEM_INSTRUCTIONS.md` | ✅ Done | Full PM role contract |
| PM-2 | `project-manager/PM_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done | Paste into GPT/Claude |
| PM-3 | `project-manager/GPT_PM_SETUP_GUIDE.md` | ✅ Done | ChatGPT Custom GPT setup and behavioral tests |
| PM-4 | `project-manager/CLAUDE_PM_SETUP_GUIDE.md` | ✅ Done | Claude Project + Free Tier primer |
| PM-5 | `project-manager/GPT_PM_CHAT_STARTERS.md` | ✅ Done | PM conversation starters |
| PM-6 | `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md` | ✅ Done | PM lifecycle, RAG, RAID, RACI, changes, gates |
| PM-7 | `_template/EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md` | ✅ Done | Charter template |
| PM-8 | `_template/EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md` | ✅ Done | Plan template |
| PM-9 | `_template/EKSAD_GENERIC_RAID_LOG_TEMPLATE.md` | ✅ Done | RAID template |
| PM-10 | `_template/EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md` | ✅ Done | Status template |
| PM-11 | `_template/EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md` | ✅ Done | Change template |

### DevOps Engineer GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| DO-1 | `devops-engineer/DEVOPS_SYSTEM_INSTRUCTIONS.md` | ✅ Done | Full DevOps role and strict production contract |
| DO-2 | `devops-engineer/DEVOPS_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done | Paste into GPT/Claude |
| DO-3 | `devops-engineer/GPT_DEVOPS_SETUP_GUIDE.md` | ✅ Done | ChatGPT setup and behavioral validation |
| DO-4 | `devops-engineer/CLAUDE_DEVOPS_SETUP_GUIDE.md` | ✅ Done | Claude project and connector safety |
| DO-5 | `devops-engineer/GPT_DEVOPS_CHAT_STARTERS.md` | ✅ Done | DevOps conversation starters |
| DO-6 | `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` | ✅ Done | Components, roles, evidence, topology, and conformance |
| DO-7 | `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md` | ✅ Done | GitLab/Jenkins/scans/release/production standard |
| DO-8 | `_template/EKSAD_GENERIC_CICD_PIPELINE_TEMPLATE.md` | ✅ Done | Pipeline design |
| DO-9 | `_template/EKSAD_GENERIC_ENVIRONMENT_READINESS_TEMPLATE.md` | ✅ Done | Environment readiness |
| DO-10 | `_template/EKSAD_GENERIC_DEPLOYMENT_ROLLBACK_RUNBOOK_TEMPLATE.md` | ✅ Done | Deployment and rollback |
| DO-11 | `_template/EKSAD_GENERIC_RELEASE_EVIDENCE_TEMPLATE.md` | ✅ Done | Release evidence pack |
| DO-12 | `_template/EKSAD_GENERIC_INCIDENT_HANDOFF_TEMPLATE.md` | ✅ Done | Incident handoff |

### Shared Base Files (`_base/`)
| # | File | Status | Upload To |
|---|------|--------|-----------|
| 22 | `_base/EKSAD_BASE_PRINCIPLES.md` | ✅ Done | **ALL GPTs** |
| 23 | `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` | ✅ Done | SA GPT + TL GPT + Dev GPT |
| 24 | `_base/EKSAD_DOMAIN_GLOSSARY.md` | ✅ Done | All GPTs (technical + business terms) |
| 24b | `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` | ✅ Done 🆕 | **BA GPT only** — BA pipeline terms + EKSAD platform BRs |
| 25 | `_base/EKSAD_CODING_STANDARDS.md` | ✅ Done | TL GPT + Dev GPT |
| 25b | `_base/EKSAD_CRUDFLOWS_PATTERN.md` | ✅ Done 🆕 | TL GPT + Dev GPT — CrudFlows v2 (flow methods, paired interfaces, auditMutator) |
| 25c | `_base/EKSAD_CRUDFLOWS_JPA.md` | ✅ Done 🆕 | TL GPT + Dev GPT — CrudFlows v2 **blocking** (Spring Boot + Quarkus-imperative; `eksad-core-jpa` artifact) |
| 25d | `_base/ADR_EKSAD_CORE_COMMON_SPLIT.md` | ✅ Done 🆕 | TL GPT + Dev GPT — architectural decision: `eksad-core-common` split into `eksad-core-api` / `-reactive` / `-jpa` / starters |
| 26 | `_base/EKSAD_TESTING_GUIDE.md` | ✅ Done | TL GPT + Dev GPT + QA GPT |
| 27 | `_base/EKSAD_SPRING_BOOT_MAPPINGS.md` | ✅ Done | SA GPT + TL GPT + Dev GPT |
| 28 | `_base/EKSAD_FRONTEND_CODING_STANDARDS.md` | ✅ Done 🆕 | SA GPT + TL GPT + Dev FE GPT |
| 29 | `_base/EKSAD_FRONTEND_TESTING_GUIDE.md` | ✅ Done 🆕 | TL GPT + Dev FE GPT |
| 30 | `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | ✅ Done | SA GPT + TL GPT + Dev FE GPT (source of truth) |

### Shared Base Files — Added 2026-05-23/24 (Knowledge Update Plan v17)
| # | File | Status | Upload To |
|---|------|--------|-----------|
| 34 | `_base/EKSAD_DOMAIN_REGISTRY.md` | ✅ Done 🆕 | ALL GPTs — canonical service/port/DB registry |
| 35 | `_base/EKSAD_MASTER_DATA_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev |
| 36 | `_base/EKSAD_CACHE_SYNC_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev |
| 37 | `_base/EKSAD_EVENT_CATALOG.md` | ✅ Done 🆕 | SA + TL + Dev — exchange/routing-key registry |
| 38 | `_base/EKSAD_CQRS_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev (RESERVED — Sprint 4+) |
| 39 | `_base/EKSAD_DB_DEPLOYMENT_STRATEGY.md` | ✅ Done 🆕 | SA + TL + Dev |
| 40 | `_base/EKSAD_MULTI_TENANCY_PATTERNS.md` | ✅ Done 🆕 | ALL GPTs |
| 41 | `_base/EKSAD_CORE_AUTH_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev |
| 42 | `_base/EKSAD_CORE_AUTH_CLIENT_SDK.md` | ✅ Done 🆕 | TL + Dev — SDK reference for `svc-user-management` & external adapters |
| 43 | `_base/EKSAD_RESERVED_FIELD_PATTERNS.md` | ✅ Done 🆕 | BA + SA + TL + Dev + Dev FE |
| 44 | `_base/EKSAD_RESILIENCE_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev |
| 45 | `_base/EKSAD_OBSERVABILITY_PATTERNS.md` | ✅ Done 🆕 | SA + TL + Dev |
| 46 | `_base/EKSAD_CICD_CONTAINER_PATTERNS.md` | ✅ Done 🆕 | TL + Dev — DevOps reference |
| 47 | `_base/EKSAD_LOAD_TESTING_GUIDE.md` | ✅ Done 🆕 | QA + TL |
| 48 | `_template/EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` | ✅ Done 🆕 | SA + TL — project `ARCHITECTURE.md` skeleton (moved from `_base/` 2026-05-24) |

### Frontend Developer GPT
| # | File | Status | Purpose |
|---|------|--------|---------|
| 31 | `developer/DEV_FE_SYSTEM_INSTRUCTIONS.md` | ✅ Done 🆕 | AI-agnostic frontend system prompt (long reference) |
| 31b | `developer/DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md` | ✅ Done 🆕 | **Paste into GPT/Claude** (≤8K chars) |
| 32 | `developer/GPT_DEV_FE_CHAT_STARTERS.md` | ✅ Done | Dev FE starters (GPT only) |
| 33 | `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | ✅ Done | FE TSD knowledge ← upload from `_template/` |

### Pending
| # | File | Status | When |
|---|------|--------|------|
| P1 | `NEXUS_PUBLISH_GUIDE.md` | 🔲 Pending | When Nexus is ready |
| P2 | Team domain files (`teams/{team}/`) | 🔲 Per request | When team-specific GPT needed |

---

### 🖥️ Vibe Coding Guides (IDE — Tier 3)

> Drop config files into your project repo for AI code assist that auto-applies EKSAD standards.
> See `vibe-coding/VIBE_CODING_SETUP_GUIDE.md` for full setup steps.

#### Phase 1 — BE Developer ✅ Done

| # | File | Status | Deploy To |
|---|------|--------|-----------|
| V1 | `vibe-coding/PLAN_VIBE_CODING.md` | ✅ Done | — living plan, do not deploy |
| V2 | `vibe-coding/VIBE_CODING_SETUP_GUIDE.md` | ✅ Done | — master guide, do not deploy |
| V3 | `vibe-coding/developer/COPILOT_DEV_INSTRUCTIONS.md` | ✅ Done | `.github/copilot-instructions.md` |
| V4 | `vibe-coding/developer/CURSOR_DEV_RULES.md` | ✅ Done | `.cursor/rules/eksad-dev.mdc` |
| V5 | `vibe-coding/developer/CLAUDE_CODE_DEV_INSTRUCTIONS.md` | ✅ Done | `CLAUDE.md` (project root) |

#### Phase 2 — FE Developer ✅ Done

| # | File | Status | Deploy To |
|---|------|--------|-----------|
| V6 | `vibe-coding/developer-fe/COPILOT_DEV_FE_INSTRUCTIONS.md` | ✅ Done | `.github/copilot-instructions.md` |
| V7 | `vibe-coding/developer-fe/CURSOR_DEV_FE_RULES.md` | ✅ Done | `.cursor/rules/eksad-dev-fe.mdc` |
| V8 | `vibe-coding/developer-fe/CLAUDE_CODE_DEV_FE_INSTRUCTIONS.md` | ✅ Done | `CLAUDE.md` (project root) |

#### Phase 3 — Technical Leader ✅ Done

| # | File | Status | Deploy To |
|---|------|--------|-----------|
| V9 | `vibe-coding/technical-leader/COPILOT_TL_INSTRUCTIONS.md` | ✅ Done | `.github/copilot-instructions.md` |
| V10 | `vibe-coding/technical-leader/CURSOR_TL_RULES.md` | ✅ Done | `.cursor/rules/eksad-tl.mdc` |
| V11 | `vibe-coding/technical-leader/CLAUDE_CODE_TL_INSTRUCTIONS.md` | ✅ Done | `CLAUDE.md` (project root) |

### 📋 ChatGPT Setup Guides
| # | File | Status | Purpose |
|---|------|--------|---------|
| G1 | `README.md` — GPT 1 section | ✅ Done | BA ChatGPT setup summary |
| G2 | `README.md` — GPT 2 section | ✅ Done | SA ChatGPT setup summary |
| G3 | `README.md` — GPT 3 section | ✅ Done | TL ChatGPT setup summary |
| G4 | `README.md` — GPT 5 section | ✅ Done | Backend ChatGPT setup summary |
| G5 | `README.md` — GPT 7 section | ✅ Done | Frontend ChatGPT setup summary |
| G6 | `README.md` — GPT 6 section | ✅ Done | QA Mode A ChatGPT setup summary |
| G7 | `project-manager/GPT_PM_SETUP_GUIDE.md` | ✅ Done | PM ChatGPT setup + behavioral validation |
| G8 | `devops-engineer/GPT_DEVOPS_SETUP_GUIDE.md` | ✅ Done | DevOps ChatGPT setup + behavioral validation |

### 🤖 Claude Setup Guides
| # | File | Status | Purpose |
|---|------|--------|---------|
| C1 | `CLAUDE_SETUP_GUIDE.md` | ✅ Done | **Master Claude guide** — all roles, both tiers (Pro/Team + Free) |
| C2 | `business-analyst/CLAUDE_BA_SETUP_GUIDE.md` | ✅ Done | BA Claude setup + Free Tier Session Primer |
| C3 | `system-analyst/CLAUDE_SA_SETUP_GUIDE.md` | ✅ Done | SA Claude setup + Free Tier Session Primer |
| C4 | `technical-leader/CLAUDE_TL_SETUP_GUIDE.md` | ✅ Done | TL Claude setup + Free Tier Session Primer |
| C5 | `developer/CLAUDE_DEV_SETUP_GUIDE.md` | ✅ Done | Dev (Backend) Claude setup + Free Tier Session Primer |
| C6 | `developer/CLAUDE_DEV_FE_SETUP_GUIDE.md` | ✅ Done | Dev (Frontend) Claude setup + Free Tier Session Primer |
| C7 | `qa/CLAUDE_QA_SETUP_GUIDE.md` | ✅ Done | QA Claude setup + Free Tier Session Primer |
| C8 | `project-manager/CLAUDE_PM_SETUP_GUIDE.md` | ✅ Done | PM Claude Project + Free Tier primer |
| C9 | `devops-engineer/CLAUDE_DEVOPS_SETUP_GUIDE.md` | ✅ Done | DevOps Claude Project + connector safety |

---

## 🚀 Setup Guide — All 9 GPTs

> Follow these steps **once per GPT**. Each GPT takes about 5 minutes to configure.

---

### 🟢 GPT 1: Business Analyst GPT

**Name:** `EKSAD Business Analyst Assistant`
**Description:** `Helps BAs write BRD, FSD, User Requirements, user stories, business rules, and acceptance criteria following EKSAD standards.`
**Model:** GPT-4o

**Instructions:** Copy from `business-analyst/BA_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

> 📖 **Setup source:** this GPT 1 section plus the maintained BA instruction, starter, template, and glossary files listed below.

**Conversation Starters** (pick 4 from `business-analyst/GPT_BA_CHAT_STARTERS.md`):
1. `I have some User Stories — help me turn them into User Requirements`
2. `Bantu saya tulis BRD untuk service baru: [nama dan tujuan service]`
3. `I have a BRD ready — help me write the FSD for module [name]`
4. `Can you review my existing BRD for gaps?`

**Knowledge Files to Upload (5 files):**
- [ ] `business-analyst/BA_SYSTEM_INSTRUCTIONS.md` ← long reference (upload as knowledge file)
- [ ] `_template/EKSAD_GENERIC_BRD_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_FSD_TEMPLATE.md`
- [ ] `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` 🆕
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ✅ ON | Image Generation ❌ OFF

---

### 🔵 GPT 2: System Analyst GPT

**Name:** `EKSAD System Analyst Assistant`
**Description:** `Helps System Analysts write TSD, design database schemas, API contracts, event schemas, and service architecture following EKSAD standards.`
**Model:** GPT-4o

**Instructions:** Copy from `system-analyst/SA_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters** (pick 4 from `system-analyst/GPT_SA_CHAT_STARTERS.md`):
1. `Buatkan TSD untuk service baru: [nama service]. Ini FSD-nya: [paste atau deskripsi FSD]`
2. `Design database schema (Flyway DDL) untuk entity [nama entity] dengan fields: [list fields]`
3. `Rancang API contract table untuk modul [nama modul] — saya jelaskan endpoint-nya`
4. `Rancang RabbitMQ event schema untuk domain event [nama event]`

**Knowledge Files to Upload (6 files):**
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_template/EKSAD_GENERIC_TSD_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md`
- [ ] `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- [ ] `_base/EKSAD_FRONTEND_CODING_STANDARDS.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ✅ ON | Image Generation ❌ OFF

---

### 🔴 GPT 3: Technical Leader GPT

**Name:** `EKSAD Technical Leader Assistant`
**Description:** `Helps Tech Leads review code against EKSAD standards, guide BaseRepository implementation, enforce coding conventions, and mentor developers.`
**Model:** GPT-4o

**Instructions:** Copy from `technical-leader/TL_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters** (pick 4 from `technical-leader/GPT_TL_CHAT_STARTERS.md`):
1. `Review entity class ini — apakah sudah sesuai EKSAD standards? [paste class]`
2. `Review implementasi BaseRepository ini — cek createFlow/updateFlow/deleteFlow: [paste class]`
3. `Review Flyway DDL ini — tenant_id, BaseEntity columns, timestamps, indexes: [paste SQL]`
4. `Jalankan PR checklist lengkap untuk code ini: [paste code atau deskripsi PR]`

**Knowledge Files to Upload (7 files):**
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_base/EKSAD_CODING_STANDARDS.md`
- [ ] `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- [ ] `_base/EKSAD_SPRING_BOOT_MAPPINGS.md`
- [ ] `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md`
- [ ] `_base/EKSAD_FRONTEND_CODING_STANDARDS.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ✅ ON | Image Generation ❌ OFF

---

### ⚪ GPT 4: General Coordinator GPT (Coordination Only)

**Name:** `EKSAD General Coordinator`
**Description:** `Coordinates EKSAD intake, routing, cross-role sequencing, handoffs, dependencies, and attributable synthesis without authoring or approving specialist-owned deliverables.`
**Model:** GPT-4o

**Instructions:** Copy from `SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters:** use only intake, routing, sequencing, dependency, or synthesis starters from `GPT_CHAT_STARTERS.md`; do not use specialist-production prompts.

**Coordinator Reference Files to Upload (5 files; reference only):**
- [ ] `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md`
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`
- [ ] `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md`
- [ ] `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md`

**Capabilities:** Web Search OFF | Code Interpreter OFF | Image Generation OFF. The coordinator has no specialist-production capability.

---

### 🟠 GPT 5: Developer GPT

**Name:** `EKSAD Developer Assistant`
**Description:** `Helps EKSAD backend developers implement entities, repositories, services, REST resources, Flyway DDL, unit tests, and integration tests following EKSAD standards. Defaults to Quarkus reactive; supports Spring Boot imperative on request.`
**Model:** GPT-4o

**Instructions:** Copy from `developer/DEV_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters** (pick 4 from `developer/GPT_DEV_CHAT_STARTERS.md`):
1. `Implementasikan BaseRepository untuk entity [nama entity] dengan ID type Long`
2. `Buatkan full entity class untuk [nama entity] dengan fields: [list fields]`
3. `Buatkan unit test untuk service method [nama method] — happy path + failure`
4. `Flyway DDL migration untuk tabel [nama tabel] dengan columns: [list]`

**Knowledge Files to Upload (6 files):**
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_base/EKSAD_CODING_STANDARDS.md`
- [ ] `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- [ ] `_base/EKSAD_TESTING_GUIDE.md`
- [ ] `_base/EKSAD_SPRING_BOOT_MAPPINGS.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ✅ ON | Image Generation ❌ OFF

---

### 🟣 GPT 6: QA GPT

**Name:** `EKSAD QA Assistant`
**Description:** `Mode A QA assistant for Test Plans, RTM, stable test cases, state-machine matrices, coverage gaps, and complete handoff metadata for the Mode B in-IDE QA automation agent; it writes no automation source.`
**Model:** GPT-4o

**Instructions:** Copy from `qa/QA_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters** (pick 4 from `qa/GPT_QA_CHAT_STARTERS.md`):
1. `Buatkan test cases dari FSD modul ini: [paste FSD section atau user stories]`
2. `Buatkan state machine test matrix untuk entity [nama entity] dengan states: [list states]`
3. `Buatkan test plan untuk modul [nama modul] service [nama service]`
4. `Siapkan Mode B automation handoff metadata untuk approved TC IDs ini; jangan tulis test source: [paste TC IDs]`

**Knowledge Files to Upload (5 files):**
- [ ] `_template/EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md`
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_base/EKSAD_TESTING_GUIDE.md`
- [ ] `_template/EKSAD_GENERIC_FSD_TEMPLATE.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search OFF | Code Interpreter OFF | Image Generation OFF. Mode B automation source is written only by the in-IDE QA agent.

---

### 🟡 GPT 7: Frontend Developer GPT 🆕

**Name:** `EKSAD Frontend Developer Assistant`
**Description:** `Helps EKSAD frontend developers implement real-API-first React features with TypeScript, React Query, React Router, TailwindCSS, test-only MSW handlers, and secure HttpOnly cookie authentication. Browser token storage is forbidden.`
**Model:** GPT-4o

**Instructions:** Copy from `developer/DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md` (between START/END markers)

**Conversation Starters** (pick 4 from `developer/GPT_DEV_FE_CHAT_STARTERS.md`):
1. `Scaffold feature module baru untuk [nama fitur] dengan fields: [list fields dan types]`
2. `Buatkan consolidated hook untuk fitur [nama fitur] — queries: list + detail, mutations: create + update + delete`
3. `Buatkan unit test untuk hook [nama hook] — happy path + error + loading state`
4. `Buatkan form component untuk [nama fitur] dengan fields: [list fields]. Validasi: [list rules]`

**Knowledge Files to Upload (5 files):**
- [ ] `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md`
- [ ] `_base/EKSAD_FRONTEND_CODING_STANDARDS.md`
- [ ] `_base/EKSAD_FRONTEND_TESTING_GUIDE.md`
- [ ] `_base/EKSAD_BASE_PRINCIPLES.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ✅ ON | Image Generation ❌ OFF

---

### 🟤 GPT 8: Project Manager GPT

**Name:** `EKSAD Project Manager Assistant`
**Description:** `Evidence-based EKSAD project initiation, planning, RAID, status, change control, dependencies, and stage-gate coordination.`

**Instructions:** Copy from `project-manager/PM_SYSTEM_INSTRUCTIONS_SHORT.md` between START/END markers.

**Conversation Starters:** pick from `project-manager/GPT_PM_CHAT_STARTERS.md`.

**Knowledge Files to Upload (8 files):**
- [ ] `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md`
- [ ] `_template/EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_WBS_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_RAID_LOG_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md`
- [ ] `_template/EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md`
- [ ] `_base/EKSAD_DOMAIN_GLOSSARY.md`

**Capabilities:** Web Search ❌ OFF | Code Interpreter ⚪ OPTIONAL | Image Generation ❌ OFF

> PM owns governance artifacts and gate coordination; BA/SA/TL/Dev/QA retain specialist artifact ownership.

---

### 🛠️ GPT 9: DevOps Engineer GPT

**Name:** `EKSAD DevOps Engineer`
**Description:** `Evidence-driven GitLab CE, Jenkins, SonarQube, Trivy, environment readiness, immutable promotion, deployment, rollback, release, and incident handoff assistant.`

**Instructions:** Copy from `devops-engineer/DEVOPS_SYSTEM_INSTRUCTIONS_SHORT.md` between START/END markers.

**Conversation Starters:** pick from `devops-engineer/GPT_DEVOPS_CHAT_STARTERS.md`.

**Knowledge and setup:** follow `devops-engineer/GPT_DEVOPS_SETUP_GUIDE.md`. DevOps remains fail-closed for production authorization and does not absorb PM, QA, TL, business, or security-risk authority.

> 💡 **How to create any GPT:** Go to [chat.openai.com](https://chat.openai.com) → profile → **My GPTs** → **Create a GPT** → **Configure** tab.

---

## 🧩 Team-Specific GPT Layers

When you need a GPT for a specific project/team (e.g., TIA Reporting, HR, Finance), create a **new Custom GPT** using the same role-based setup PLUS one additional domain knowledge file:

```
BA GPT (3 base files)  +  TIA_DOMAIN_KNOWLEDGE.md   →  TIA Reporting BA GPT
SA GPT (3 base files)  +  TIA_DOMAIN_KNOWLEDGE.md   →  TIA Reporting SA GPT
BA GPT (3 base files)  +  HR_DOMAIN_KNOWLEDGE.md    →  HR Team BA GPT
```

**Team domain knowledge file should contain:**
- Domain-specific business terms and processes
- Service-specific module type strings
- Domain-specific approval workflow descriptions
- Known business rules unique to that domain
- Entity/data model overview for the domain

Files will be created at: `gpt/business-analyst/teams/{team}/` or `gpt/system-analyst/teams/{team}/`

> **Come back anytime** and say: *"Create domain knowledge file for [project/team name]"*

---

## 🔄 Maintenance & Update Policy

> **📌 Single Source of Truth:** Standards/reference files live in `_base/`. Generic document scaffolds (BRD, FSD, TSD) live in `_template/`. **Never edit sub-folder copies** — sub-folders only contain GPT instructions and chat starters. When you update any file in `_base/` or `_template/`, re-upload it to the relevant GPTs.

| When | Action |
|------|--------|
| New service is added to EKSAD platform | Update `_base/EKSAD_DOMAIN_GLOSSARY.md` + re-upload to all GPTs |
| New BA terminology or platform BR added | Update `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` + re-upload to BA GPT only |
| BA GPT instructions change | Update `business-analyst/BA_SYSTEM_INSTRUCTIONS.md` and `BA_SYSTEM_INSTRUCTIONS_SHORT.md`, archive superseded material only when required, then update this README |
| Architecture principle changes | Update `_base/EKSAD_BASE_PRINCIPLES.md` + re-upload to all GPTs |
| Architecture pattern changes | Update `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` + re-upload to SA, TL, Dev GPTs |
| PM standard or template changes | Update `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md` or the affected PM template + re-upload to PM GPT/Claude; align long/short/Hermes instructions when behavior changes |
| File storage pattern changes (new provider, new env var, visibility rule, thumbnail behaviour) | Update `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` Section 10 **and** `_base/EKSAD_BASE_PRINCIPLES.md` + re-upload to SA, TL, Dev GPTs; General Coordinator receives only shared coordinator references |
| Coding standard changes (backend) | Update `_base/EKSAD_CODING_STANDARDS.md` + re-upload to TL and Dev GPTs |
| Coding standard changes (frontend) | Update `_base/EKSAD_FRONTEND_CODING_STANDARDS.md` + re-upload to SA, TL, Dev FE GPTs |
| BRD/FSD template changes | Update `_template/EKSAD_GENERIC_BRD_TEMPLATE.md` or `_template/EKSAD_GENERIC_FSD_TEMPLATE.md` + re-upload to BA and QA as applicable |
| BRD/FSD template major version upgrade | Archive current files to `_template/archive/` with `_v{X}.Y.md` suffix (git commit OK; do NOT upload archive to GPTs) → update both templates → update README Last Updated → re-upload to BA and QA as applicable |
| TSD template changes (backend) | Update `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` + re-upload to SA, TL, and Dev GPTs |
| TSD template changes (frontend) | Update `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` + re-upload to SA, TL, Dev FE GPTs |
| Frontend API contract added or changed | Keep production code real-API-first; update the API client against the approved contract, use MSW only in tests, and retain HttpOnly cookie authentication without browser token storage |
| New template needed (e.g., API Design Doc) | Create new file in `_template/`, upload to relevant GPTs |
| `eksad-core-common` version bumped | Update version references in `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` |
| Quarkus version upgrade | Update `_base/EKSAD_BASE_PRINCIPLES.md` stack table + `_base/EKSAD_CODING_STANDARDS.md` + all `*_SYSTEM_INSTRUCTIONS_SHORT.md` primers (7 files) + `CLAUDE_SETUP_GUIDE.md` General Coordinator primer |
| React / frontend dependency upgrade | Update `_base/EKSAD_FRONTEND_CODING_STANDARDS.md` stack table |
| New master data entity added to a domain | Update `_base/EKSAD_DOMAIN_REGISTRY.md` + `_base/EKSAD_EVENT_CATALOG.md` + re-upload to SA, TL, and Dev GPTs |
| New RabbitMQ exchange / routing key | Update `_base/EKSAD_EVENT_CATALOG.md` + re-upload to SA, TL, and Dev GPTs |
| New resilience / observability pattern adopted | Update `_base/EKSAD_RESILIENCE_PATTERNS.md` or `_base/EKSAD_OBSERVABILITY_PATTERNS.md` + re-upload to SA, TL, Dev |
| Reserved field schema change | Update `_base/EKSAD_RESERVED_FIELD_PATTERNS.md` + re-upload to BA, SA, TL, Dev, Dev FE GPTs |
| core-auth API / SDK change | Update `_base/EKSAD_CORE_AUTH_PATTERNS.md` + `_base/EKSAD_CORE_AUTH_CLIENT_SDK.md` + re-upload to SA, TL, Dev |
| New browser-facing cookie endpoint or cookie config change | Update `_base/EKSAD_CORE_AUTH_PATTERNS.md` §13 + re-upload to SA, TL, Dev |
| New tenancy hierarchy rule | Update `_base/EKSAD_MULTI_TENANCY_PATTERNS.md` + re-upload to ALL GPTs |
| CI/CD pipeline or Dockerfile convention change | Update `_base/EKSAD_CICD_CONTAINER_PATTERNS.md` + re-upload to TL, Dev |

> **Important:** After updating any knowledge file, go to the Custom GPT editor and **re-upload** the updated file. GPT does not auto-sync.

---

## 📌 Related Projects

| Project | Status | Description |
|---------|--------|-------------|
| `eksad-core-common` | 🟡 In Progress | Shared library: BaseRepository, CrudFlows, LogHandler, auto audit trail |
| `eksad-core-audittrail` | 🟡 In Progress | Audit trail service (MongoDB, RabbitMQ consumer) — rename from `bida-core-audittrail` |
| `eksad-core-storage` | 🟡 In Progress | File storage service (`:8090`) — file upload, `file_metadata` PostgreSQL table, CDN URL resolution (AWS S3 + CloudFront or Cloudflare R2 + CDN), async thumbnail generation (Thumbnailator + PDFBox) |
| `eksad-svc-leads` | 🟡 In Progress | Reference service skeleton — rename from `bida-svc-leads` |
| `eksad-parent` | 🔲 To Do | Company parent POM / BOM |
| Nexus Repository | 🔲 To Do | Internal Maven artifact server for publishing core libraries |

---

## 💬 Which GPT to Use for What

| I need to... | Use This GPT |
|---|---|
| Write or review a **BRD** | 🟢 BA GPT |
| Write or review a **FSD** / user stories / business rules | 🟢 BA GPT |
| Write or review a **TSD** / database schema / API contract | 🔵 SA GPT |
| Design **frontend TSD** — feature modules, routing, component catalog | 🔵 SA GPT |
| Design **RabbitMQ event schema** or service architecture | 🔵 SA GPT |
| **Review Java code** against EKSAD standards (PR review) | 🔴 TL GPT |
| **Review React/TypeScript code** against EKSAD frontend standards | 🔴 TL GPT |
| **Review Flyway DDL** or `application.properties` | 🔴 TL GPT |
| Get help implementing **BaseRepository** or any CRUD flow | 🟠 Dev GPT |
| Write **entity, service, REST resource** implementation code | 🟠 Dev GPT |
| Write **backend unit tests or integration tests** | 🟠 Dev GPT |
| Implement **React feature module** (hooks, components, services, types) | 🟡 Dev FE GPT 🆕 |
| Write **React Query hooks** or a **real API client layer** | 🟡 Dev FE GPT 🆕 |
| Write **Jest tests** for React hooks or components | 🟡 Dev FE GPT 🆕 |
| Add **test-only MSW handlers** for deterministic frontend tests | 🟡 Dev FE GPT 🆕 |
| Integrate **HttpOnly cookie authentication** without browser token storage | 🟡 Dev FE GPT 🆕 |
| **Derive test cases** from FSD / user stories | 🟣 QA GPT |
| Write a **test plan** or **state machine test matrix** | 🟣 QA GPT |
| Prepare **Mode B automation handoff metadata** for approved TC IDs | 🟣 QA GPT |
| Coordinate a **cross-role** request or synthesize attributable specialist outputs | ⚪ General Coordinator GPT |
| Project uses **Spring Boot** (any role) | Same role GPT — just say "Spring Boot" |
| Project uses **React frontend** (any role) | SA/TL auto-switch; Dev FE for implementation |
| **Implement code in your IDE** with EKSAD standards enforced | 🖥️ Vibe Coding — `vibe-coding/VIBE_CODING_SETUP_GUIDE.md` |
