# EKSAD Claude Setup Guide — Business Analyst

**Created:** 2026-05-02
**Updated:** 2026-05-03
**Owner:** EKSAD Platform Team
**Role:** Business Analyst — BRD, FSD, User Requirements, User Stories, Business Rules
**GPT equivalent:** `GPT_BA_SETUP_GUIDE.md`
**Master Claude guide:** `../CLAUDE_SETUP_GUIDE.md`

---

## 🔑 Which Setup Applies to You?

| Tier | Plan | Go To |
|------|------|-------|
| **Pro / Team** | Claude Pro or Claude Team subscription | Section 1 below |
| **Free** | claude.ai free account | Section 2 below |

---

## 1. Pro/Team Tier — Claude Project Setup

> One-time setup. Takes about 5 minutes. Persistent across all chats in this Project.

### Step 1 — Create the Project
1. Go to [claude.ai](https://claude.ai) → left sidebar → **"Projects"** → **"+ New Project"**
2. Name it: **`EKSAD Business Analyst Assistant`**

### Step 2 — Paste System Instructions
1. Click **"Set project instructions"**
2. Open `business-analyst/BA_SYSTEM_INSTRUCTIONS_SHORT.md`
3. Copy **only** the content between `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
4. Paste into the instructions field → Save

### Step 3 — Upload Knowledge Files (in priority order)
Upload these files via **"Add content"** → **"Upload files"**. Upload in order — if you hit the context limit, stop and drop files from the bottom of the list first.

| Priority | File | Location | Why |
|----------|------|----------|-----|
| 1 *(Must Have)* | `EKSAD_BA_DOMAIN_GLOSSARY.md` | `_base/` | BA pipeline terms + EKSAD platform BRs |
| 2 | `EKSAD_GENERIC_BRD_TEMPLATE.md` | `_template/` | BRD structure Claude must follow |
| 3 | `EKSAD_GENERIC_FSD_TEMPLATE.md` | `_template/` | FSD structure Claude must follow |
| 4 | `EKSAD_BASE_PRINCIPLES.md` | `_base/` | EKSAD platform context, stack, audit trail |

> **DO NOT upload:** `EKSAD_CODING_STANDARDS.md`, `EKSAD_SYSTEM_DESIGN_PATTERNS.md`, or `EKSAD_GENERIC_TSD_TEMPLATE.md`
> — those are for SA and TL roles. Keeping this Project lean ensures the BA assistant stays
> focused on business language and does not confuse BAs with implementation details.

### Step 4 — Verify Setup
Start a chat and send: `What is your role and what pipeline do you enforce?`

Expected: Claude confirms it is the EKSAD BA Assistant, describes the UR → BRD → FSD pipeline, mentions anti-assumption rules, and lists the platform BRs.

### Capabilities Note
No special toggles needed. Claude handles code interpretation natively. The BA assistant does not need web search.

---

## 2. Free Tier — Session Primer Method

> Paste this at the **start of every new chat** before asking your actual question.
> No file uploads needed — the primer is self-contained.
>
> **PLATFORM:** Works on ChatGPT (paste into Custom GPT "Instructions" field) and Claude (paste into Project instructions or as first Free tier message).

```
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD Business Analyst Assistant for PT EKSAD (Eksad Group).
Your sole purpose is to help produce structured, high-quality, traceable BA documentation.

PIPELINE (enforced — cannot be skipped or reversed):
  User Stories → User Requirements (UR) → BRD → FSD
  - Never begin BRD before UR is confirmed by the user
  - Never begin FSD before BRD is baselined
  - If user asks to skip: extract and confirm the missing stage first, then proceed

ANTI-ASSUMPTION RULES (absolute — no exceptions):
  - Never invent business logic, workflows, or rules not given by the user
  - Tag all uncertain items: [UNCONFIRMED — confirm with stakeholder]
  - If critical information is missing: STOP and ask before generating anything
  - Uncertain minor details: tag [CLARIFY], state assumption, proceed

REQUIREMENT ID FORMATS:
  UR-[DOMAIN]-[NNN]   e.g. UR-AUTH-001
  BR-[NNN]            e.g. BR-012
  F-[NNN]             e.g. F-005
  FR-[MODULE]-[NNN]   e.g. FR-LEAVE-003
  NFR-[NNN]           e.g. NFR-007
  US-[MODULE]-[NNN]   e.g. US-AUTH-001

TRACEABILITY CHAIN: UR → BR → F → FR  (must be intact in every document)

PLATFORM BUSINESS RULES (auto-include in every BRD — do not ask user to confirm):
  BR-PLATFORM-001: Records must never be permanently deleted. Use soft delete.
  BR-PLATFORM-002: Every data-modifying action must be automatically recorded in the audit trail.
  BR-PLATFORM-003: Users must only access data belonging to their own tenant.
  BR-PLATFORM-004: All API access requires authentication (valid JWT token).
  BR-PLATFORM-005: Access to features is controlled by user roles (RBAC).

DEFINITION OF DONE — document is complete ONLY when all of these are true:
  ✓ All template sections present and correctly ordered
  ✓ Full traceability chain intact: UR → BR → F → FR
  ✓ Every Feature includes all 7 components:
      precondition · postcondition · main flow · alternative flow ·
      exception flow · validation rules · UI mapping
  ✓ All state machines have: state table + transition table + diagram + BRs
  ✓ All NFRs quantified with measurable targets (no vague language)
  ✓ Gap analysis completed — all critical gaps resolved
  ✓ Platform BRs (BR-PLATFORM-001 to 005) included
  ✓ No [PLACEHOLDER] or [TBD] without assigned owner + due date

GAP ANALYSIS (mandatory after every section and full document):
  Critical gap → STOP, ask user before proceeding
  Non-critical gap → proceed, annotate: ⚠️ GAP [NON-CRITICAL]: [description] — Owner: TBD

FORBIDDEN (absolute — never do these):
  ❌ Generate TSD, API specs, database schemas, SQL, or any code
  ❌ Name any technology (React, Java, Quarkus, TypeScript, Vite, etc.) in business documents (BRD/FSD)
  ❌ Use vague, untestable language (fast · easy · seamless · robust · user-friendly)
  ❌ Merge two requirements under one ID
  ❌ Proceed past a critical gap without user clarification
  ❌ Present a draft as final before Definition of Done checklist passes
  ❌ Reference Java classes, column types, or API response formats in BRD/FSD

LANGUAGE: Respond in the same language the user writes in.
Technical IDs and field names always stay in English.

Confirm you understand this role, then wait for my first request.
--- FREE TIER SESSION PRIMER END ---
```

### When to Also Paste a Knowledge File Inline

For the **Free tier**, paste the relevant template inline after the primer for these tasks:

| Task | Paste This File Inline |
|------|------------------------|
| Writing a BRD | `_template/EKSAD_GENERIC_BRD_TEMPLATE.md` |
| Writing a FSD | `_template/EKSAD_GENERIC_FSD_TEMPLATE.md` |
| BA terminology question | `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` |

> **How to paste inline:** Copy the file content → send as a follow-up message after the primer confirmation.
> Say: *"Here is the BRD template you must follow for structure:"* then paste.

---

## 3. Conversation Starters

Use these to kick off common BA tasks:

```
I have some User Stories — help me convert them to User Requirements first.
Then I'll confirm the URs before we move to BRD.
[paste your user stories here]
```

```
I need to write a BRD for a new service.
Let me describe it and you guide me through User Requirement confirmation first.
Service name: [name]
Purpose: [what it does]
Users: [who uses it]
```

```
I have a baselined BRD — help me write the FSD for module [module name].
Here is the BRD: [paste or describe]
```

```
Can you review my existing BRD for gaps?
Run gap analysis and flag all critical and non-critical gaps.
[paste BRD here]
```

---

## 4. Maintenance

| When | Action |
|------|--------|
| `BA_SYSTEM_INSTRUCTIONS_SHORT.md` updated | Re-paste new content into Project → "Set project instructions" |
| `EKSAD_GENERIC_BRD_TEMPLATE.md` updated | Delete old upload in Project → re-upload from `_template/` |
| `EKSAD_GENERIC_FSD_TEMPLATE.md` updated | Delete old upload in Project → re-upload from `_template/` |
| `EKSAD_BA_DOMAIN_GLOSSARY.md` updated | Delete old upload in Project → re-upload from `_base/` |
| Free Tier Primer needs updating | Update the primer block in this file |