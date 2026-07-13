# EKSAD Claude Setup Guide — Master Guide for 9 Assistants

**Created:** 2026-05-02
**Updated:** 2026-07-11
**Owner:** EKSAD Platform Team
**Applies to:** All EKSAD team members using Claude (claude.ai)
**GPT equivalent:** See the nine ChatGPT role setup sections in `README.md`; PM and DevOps also have per-role GPT setup guides.

---

## 📖 What Is This?

This guide shows you how to set up Claude as your EKSAD AI assistant — the same way the team uses Custom GPTs on ChatGPT. The active setup has exactly nine assistants: one General Coordinator plus eight role-specific assistants for Business Analyst, System Analyst, Technical Leader, Backend Developer, Frontend Developer, QA Engineer, Project Manager, and DevOps Engineer.

**Two paths depending on your subscription:**

| Tier | Plan | Method |
|------|------|--------|
| **Pro / Team** | Claude Pro or Claude Team | Create a **Claude Project** — one-time setup, persistent across all chats |
| **Free** | claude.ai free account | Paste a **Session Primer** at the start of every new chat — no setup needed |

> 💡 **Free tier members:** Your role guide has a ready-to-copy **Free Tier Session Primer** block.
> Paste it as your first message in any new Claude chat. It's self-contained — no file uploads needed.
> When budget is approved for Pro/Team, switch to the Project method for a better experience.

---

## 🔄 Claude vs Custom GPT — Concept Mapping

| Custom GPT Concept | Claude Equivalent | Notes |
|---|---|---|
| Custom GPT | Claude Project | Pro/Team tier only |
| "Instructions" field | Project → "Set instructions" | Paste `_SHORT` file content (between START/END markers) |
| Knowledge files upload | Project → "Add content" → upload files | Same `.md` files, same purpose |
| Conversation Starters | Bookmark/pin favourite prompts | No native equivalent in Claude |
| Code Interpreter ON | Default behaviour | Claude interprets code natively |
| Web Search OFF | Default behaviour | Claude does not browse unless you add a tool |
| Free tier (no Projects) | Manual session primer | Paste primer block at start of each new chat |

---

## 🧭 Role Architecture — All 9 Claude Assistants

```
EKSAD has exactly 9 active Claude Assistants:

┌───────────────────────────────────────────────────────────────────────┐
│                    EKSAD General Coordinator  (⚪)                    │
│   Intake · routing · cross-role sequencing · attributable synthesis   │
│   Coordinates specialists; does not replace specialist ownership      │
│   Setup: Section 5 of this file                                        │
└───────────────────────────────────────────────────────────────────────┘
                │              │              │              │
                ▼              ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ 🟢 Business    │ │ 🔵 System      │ │ 🔴 Technical   │ │ 🟠 Backend     │
│ Analyst        │ │ Analyst        │ │ Leader         │ │ Developer      │
│ BRD/FSD        │ │ TSD/design     │ │ Code review    │ │ Java/Quarkus   │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
                │              │              │              │
                ▼              ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ 🟡 Frontend    │ │ 🟣 QA          │ │ 🟤 Project     │ │ 🛠️ DevOps     │
│ Developer      │ │ Engineer       │ │ Manager        │ │ Engineer       │
│ React/TS       │ │ Mode A+handoff │ │ Governance     │ │ CI/CD/release  │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
```

| # | Role | Claude Project Name | Per-Role Guide |
|---|------|---------------------|----------------|
| 1 | ⚪ General Coordinator | `EKSAD General Coordinator` | Section 5 below |
| 2 | 🟢 Business Analyst | `EKSAD Business Analyst Assistant` | `business-analyst/CLAUDE_BA_SETUP_GUIDE.md` |
| 3 | 🔵 System Analyst | `EKSAD System Analyst Assistant` | `system-analyst/CLAUDE_SA_SETUP_GUIDE.md` |
| 4 | 🔴 Technical Leader | `EKSAD Technical Leader Assistant` | `technical-leader/CLAUDE_TL_SETUP_GUIDE.md` |
| 5 | 🟠 Backend Developer | `EKSAD Developer Assistant` | `developer/CLAUDE_DEV_SETUP_GUIDE.md` |
| 6 | 🟡 Frontend Developer | `EKSAD Frontend Developer Assistant` | `developer/CLAUDE_DEV_FE_SETUP_GUIDE.md` |
| 7 | 🟣 QA Engineer | `EKSAD QA Assistant` | `qa/CLAUDE_QA_SETUP_GUIDE.md` |
| 8 | 🟤 Project Manager | `EKSAD Project Manager Assistant` | `project-manager/CLAUDE_PM_SETUP_GUIDE.md` |
| 9 | 🛠️ DevOps Engineer | `EKSAD DevOps Engineer` | `devops-engineer/CLAUDE_DEVOPS_SETUP_GUIDE.md` |

---

## 🚀 Pro/Team Tier — Creating a Claude Project (Step-by-Step)

> Do this **once per role**. Takes about 5 minutes. All chats in the project inherit your setup.

1. Go to [claude.ai](https://claude.ai) → left sidebar → **"Projects"** → **"+ New Project"**
2. Give it a name from the table above (e.g., `EKSAD Business Analyst Assistant`)
3. Click **"Set project instructions"** → paste the content from the role's `_SHORT` file
   - Copy only what is **between** `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
   - Do NOT include the header/footer outside those markers
4. Click **"Add content"** → **"Upload files"** → upload the knowledge files listed in your role guide
   - Upload in **priority order** (most important first — see Section 7)
   - If you hit the context limit, stop uploading and drop files from the bottom of the priority list
5. Click **"Start chat"** — your setup persists across every conversation in this Project

> ⚠️ **Claude Projects do NOT auto-sync files.** When a knowledge file is updated in the repo,
> delete the old upload in the Project and re-upload the new version manually.

---

## 🆓 Free Tier — Manual Session Primer (Step-by-Step)

> Do this at the **start of every new chat**. No account setup required.

1. Open [claude.ai](https://claude.ai) → **"New chat"**
2. Find your role's **Free Tier Session Primer** block in your role guide (in each subfolder)
3. **Copy the entire primer block** — it is clearly marked with `--- FREE TIER SESSION PRIMER START ---`
4. **Paste it as your first message** in the new chat
5. Wait for Claude to reply confirming it understood the role
6. Then ask your actual question or paste your document

**For knowledge-heavy tasks** (e.g., writing a BRD, or implementing a full module):
- Your role guide specifies **which knowledge file to also paste inline** and when
- Copy the relevant file content and paste it as a follow-up message before your actual request

> ⚠️ **Free tier chats do NOT persist instructions.** Repeat the primer in every new chat session.
> Keep your role's setup guide bookmarked for fast access to the primer.

---

## ⚪ General Coordinator Claude — Setup

Use General Coordinator for intake, cross-role sequencing, routing, and synthesis when a request spans multiple roles or the correct specialist is unclear. General Coordinator must preserve role ownership: it coordinates specialist work but does not impersonate a specialist, create specialist-owned deliverables, approve gates, or proxy named decision authorities.

**Pro/Team — Project Setup:**
- **Project name:** `EKSAD General Coordinator`
- **Instructions:** paste the coordinator contract from the primer below into Project instructions
- **Knowledge files (priority order):**
  1. `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md`
  2. `_base/EKSAD_BASE_PRINCIPLES.md`
  3. `_base/EKSAD_DOMAIN_GLOSSARY.md`
  4. `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md`
  5. `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md`

**Free Tier Session Primer:**

> **PLATFORM:** Works on ChatGPT (paste into Custom GPT "Instructions" field) and Claude (paste into Project instructions or as first Free tier message).

```
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD General Coordinator for PT EKSAD (Eksad Group).
You coordinate intake and cross-role work while preserving specialist ownership
and named decision authority. You never replace an accountable specialist.

YOUR RESPONSIBILITIES:
- Intake: collect scope, source artifacts, constraints, requested outputs, evidence,
  owners, dependencies, and unresolved authority gaps without inventing content.
- Routing: direct BA work to Business Analyst; architecture/TSD to System Analyst;
  technical and code review to Technical Leader; implementation to Backend or
  Frontend Developer; test delivery to QA; governance to Project Manager; and
  CI/CD, environment, release, deployment, rollback, and incident work to DevOps.
- Coordination: sequence cross-role stages, preserve gates, and track handoffs.
- Synthesis: combine attributable specialist outputs while retaining source links,
  verdicts, disagreements, open gaps, and named authorities.

ROLE BOUNDARY: Do not create or approve specialist-owned deliverables, execute
production work, fabricate evidence, invent business rules or commitments, expose
credentials, accept residual risk, grant waivers, or proxy authorization.

TECH STACK: Java 21 · Quarkus 3.30.6 · Hibernate Reactive Panache · PostgreSQL · Flyway · RabbitMQ ·
SmallRye JWT (RS256) · Lombok · MapStruct · React 18 · TypeScript 5 · Vite 5 · TailwindCSS 3 · React Query 5

CORE RULES (non-negotiable):
- tenant_id on every DB table, every JWT claim, every RabbitMQ event
- Flyway only — never ddl-auto=update
- Soft delete — never hard delete (deleted_at + deleted_by columns)
- Audit trail — all CRUD via BaseRepository createFlow/updateFlow/deleteFlow (auto-fires to RabbitMQ → MongoDB)
- Long epoch ms for all timestamps (BIGINT in PostgreSQL, Long in Java)
- NUMERIC(20,4) / BigDecimal for all financial values
- BA pipeline enforced: UR → BRD → FSD — route each stage to BA; never invent business logic
- BRD must NOT name frontend tech — describe as "browser-based web application"

MODULE TYPE FORMAT: <PROJECT>.<MODULE>.<ACTION> (e.g., EKSAD_SVC_LEADS.TRANSACTION.CREATE)

FORBIDDEN: impersonating specialists · producing or approving role-owned artifacts ·
proxying authority · fabricating evidence · ddl-auto=update · hard-coded credentials ·
Double/Float for money · TIMESTAMP columns (use BIGINT) · cross-service DB JOINs ·
missing tenant_id · skipping audit trail · naming React/TS/Vite in BRD

LANGUAGE: respond in the same language the user writes in.
Confirm you understand before I begin.
--- FREE TIER SESSION PRIMER END ---
```

---

## 📁 Knowledge File Upload Priority (All Roles)

> Upload in this order. If you hit Claude's context limit, stop uploading — drop from the **bottom** of the list first.

| Role | Priority 1 *(Must Have)* | Priority 2 | Priority 3 | Priority 4 | Priority 5 | Priority 6 | Priority 7 |
|------|--------------------------|------------|------------|------------|------------|------------|------------|
| 🟢 BA | `EKSAD_BA_DOMAIN_GLOSSARY.md` | `EKSAD_GENERIC_BRD_TEMPLATE.md` | `EKSAD_GENERIC_FSD_TEMPLATE.md` | `EKSAD_BASE_PRINCIPLES.md` | — | — | — |
| 🟤 PM | `EKSAD_PROJECT_MANAGEMENT_STANDARD.md` | `EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md` | `EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md` | `EKSAD_GENERIC_WBS_TEMPLATE.md` | `EKSAD_GENERIC_RAID_LOG_TEMPLATE.md` | `EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md` | `EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md` |
| 🔵 SA | `EKSAD_BASE_PRINCIPLES.md` | `EKSAD_GENERIC_TSD_TEMPLATE.md` | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | `EKSAD_CODING_STANDARDS.md` | `EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | `EKSAD_FRONTEND_CODING_STANDARDS.md` | — |
| 🔴 TL | `EKSAD_CODING_STANDARDS.md` | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | `EKSAD_FRONTEND_CODING_STANDARDS.md` | `EKSAD_DOMAIN_GLOSSARY.md` | `EKSAD_GENERIC_TSD_TEMPLATE.md` | — | — |
| ⚪ General Coordinator | `EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` | `EKSAD_BASE_PRINCIPLES.md` | `EKSAD_DOMAIN_GLOSSARY.md` | `EKSAD_PROJECT_MANAGEMENT_STANDARD.md` | `EKSAD_DEVOPS_DELIVERY_STANDARD.md` | — | — |
| 🟠 Dev BE | `EKSAD_CODING_STANDARDS.md` | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | `EKSAD_TESTING_GUIDE.md` | `EKSAD_SPRING_BOOT_MAPPINGS.md` | `EKSAD_DOMAIN_GLOSSARY.md` | — | — |
| 🟡 Dev FE | `EKSAD_FRONTEND_CODING_STANDARDS.md` | `EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | `EKSAD_FRONTEND_TESTING_GUIDE.md` | `EKSAD_BASE_PRINCIPLES.md` | `EKSAD_DOMAIN_GLOSSARY.md` | — | — |
| 🟣 QA | `EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` | `EKSAD_TESTING_GUIDE.md` | `EKSAD_GENERIC_FSD_TEMPLATE.md` | `EKSAD_BASE_PRINCIPLES.md` | `EKSAD_DOMAIN_GLOSSARY.md` | — | — |
| 🛠️ DevOps | `EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` | `EKSAD_DEVOPS_DELIVERY_STANDARD.md` | `EKSAD_OBSERVABILITY_PATTERNS.md` | `EKSAD_RESILIENCE_PATTERNS.md` | `EKSAD_DB_DEPLOYMENT_STRATEGY.md` | `EKSAD_LOAD_TESTING_GUIDE.md` | — |

> All files are in `_base/` or `_template/` subfolders. See the folder structure in `README.md`.

---

## 💬 Which Claude Role to Use for What

| I need to... | Use This Role |
|---|---|
| Write or review a **BRD** | 🟢 BA |
| Write or review a **FSD** / user stories / business rules | 🟢 BA |
| Convert **User Stories → User Requirements → BRD** | 🟢 BA |
| Write or review a **TSD** / database schema / API contract | 🔵 SA |
| Design **frontend architecture** — feature modules, routing, component catalog | 🔵 SA |
| Design **RabbitMQ event schema** or service boundaries | 🔵 SA |
| **Review Java/Quarkus code** against EKSAD standards (PR review) | 🔴 TL |
| **Review React/TypeScript code** against EKSAD frontend standards | 🔴 TL |
| **Review Flyway DDL** or `application.properties` | 🔴 TL |
| Implement **BaseRepository** or any CRUD flow | 🟠 Dev BE |
| Write **entity, service, REST resource** implementation code | 🟠 Dev BE |
| Write **backend unit tests or integration tests** | 🟠 Dev BE |
| Implement a **real-API-first React feature module** (hooks, components, services, types) | 🟡 Dev FE |
| Write **React Query hooks** or a **real API client layer** | 🟡 Dev FE |
| Write **Jest tests** for React hooks or components | 🟡 Dev FE |
| Add **test-only MSW handlers** for deterministic frontend tests | 🟡 Dev FE |
| Integrate **HttpOnly cookie authentication** without browser token storage | 🟡 Dev FE |
| **Derive test cases** from FSD / user stories | 🟣 QA |
| Write a **test plan** or **state machine test matrix** | 🟣 QA |
| Prepare **Mode B automation handoff metadata** for approved TC IDs; the in-IDE QA agent writes automation source | 🟣 QA |
| Create or govern a **Project Charter, Plan, RAID log, status report, Change Request, or stage gate** | 🟤 PM |
| Design or review **GitLab CE/Jenkins CI/CD**, **SonarQube/Trivy evidence**, or artifact promotion | 🛠️ DevOps |
| Assess **environment readiness, deployment, rollback, observability, release evidence, or incident handoff** | 🛠️ DevOps |
| Coordinate a **cross-role** request, route unclear work, or synthesize attributable specialist outputs | ⚪ General Coordinator |
| Project uses **Spring Boot** (any role) | Same role — just say "this is a Spring Boot project" |
| Project uses **React frontend** (any role) | SA/TL auto-switch; Dev FE for implementation |

---

## 🔄 Maintenance — Keeping Claude Projects Up to Date

> **Single Source of Truth:** Standards files live in `_base/`. Templates live in `_template/`.
> Never edit Claude Project instructions directly without updating the source `_SHORT` file first.

| When | Action |
|------|--------|
| Any `_base/` file is updated | Re-upload updated file to all relevant Claude Projects |
| Any `_template/` file is updated | Re-upload to relevant Claude Projects |
| Role instructions (`_SHORT` file) updated | Paste new content into Project → "Set project instructions" → Save |
| New role or assistant added | Create new `CLAUDE_{ROLE}_SETUP_GUIDE.md` in role subfolder + add row to architecture table above |
| Free Tier Primer needs updating | Update primer block in the relevant `CLAUDE_{ROLE}_SETUP_GUIDE.md` |
| Team gets Pro/Team subscription | Follow Pro tier steps in each role guide — same knowledge files, same instructions |
| **Quarkus version upgrade** | Update version in `EKSAD_BASE_PRINCIPLES.md` + all `*_SYSTEM_INSTRUCTIONS_SHORT.md` primers + `CLAUDE_SETUP_GUIDE.md` General Coordinator primer |

---

## 🔁 How to Resume Implementation in a New Chat

If implementation was interrupted, open a new chat and say:

> *"Read `<path-to-workspace>/brainstorming/EKSAD/gpt/PLAN_INSTRUCTIONS_IMPROVEMENT.md`
> and continue from the first 🔲 To Do step in the Progress Tracker."*
