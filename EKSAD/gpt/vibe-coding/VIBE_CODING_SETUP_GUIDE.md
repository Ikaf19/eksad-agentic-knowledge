# EKSAD Vibe Coding Setup Guide — Master Guide

**Created:** 2026-05-04
**Owner:** EKSAD Platform Team
**Applies to:** All EKSAD developers using AI code assist inside their IDE/editor
**Related guides:**
- ChatGPT Custom GPT → per-role `GPT_*_SETUP_GUIDE.md` files listed in `../README.md`
- Claude Project / Free Tier → `../CLAUDE_SETUP_GUIDE.md`

---

## 📖 What Is Vibe Coding?

**Vibe coding** = AI writes code *with* you inside your IDE, reading your actual project files as it goes. Unlike chat-based GPT/Claude (where you paste snippets back and forth), vibe coding tools have direct access to your workspace — they see your entities, your services, your imports.

The EKSAD Vibe Coding setup extends that capability by also giving the AI your **EKSAD standards files** as permanent context, so it automatically applies:
- Correct `BaseRepository` patterns
- Proper `tenant_id` handling
- `@SuperBuilder` on entities
- Flyway DDL conventions
- All forbidden patterns enforced from day one

**No more reviewing PRs for `@Builder` vs `@SuperBuilder`.**

---

## 🔄 Official Usage Workflow

Every implementation session — regardless of tool or role — follows this 5-phase flow:

```
⓪ EXTRACT  →  ① BRIEF  →  ② PLAN  →  ③ REVIEW  →  ④ IMPLEMENT
   (AI)          (Human)      (AI)        (Human)        (AI)
```

| Phase | Who | What Happens | Runs |
|-------|-----|--------------|------|
| ⓪ Extract | 🤖 AI | Checks for `PLAN_<MODULE>.md` — if missing, scans `tsd/` and **generates the file** | First iteration only |
| ① Brief | 🧑 You | Describe the task: entity name, fields, service name, module name | Every iteration |
| ② Plan | 🤖 AI | Outputs a structured plan table — files, actions, patterns, risks. Then **stops and waits**. | Every iteration |
| ③ Review | 🧑 You | Read the plan. Ask questions or request changes. When happy → reply **"proceed"** | Every iteration |
| ④ Implement | 🤖 AI | Writes complete, compilable code per the approved plan. Updates tracker after each task. | Every iteration |

> ✅ **You are always in control.** The AI never writes code without your explicit approval.
> ⚡ **After the first iteration**, Phase ⓪ takes seconds — just loads `PLAN_<MODULE>.md` instead of re-reading TSD.
> 📄 Full workflow spec + format reference: `gpt/vibe-coding/PLAN_FIRST_WORKFLOW.md`

### Example Interaction

```
# First iteration — Phase ⓪ runs automatically
AI:   Scanning tsd/ for Submission module...
      Module plan created → docs/eksad/plans/PLAN_SUBMISSION.md
      "PLAN_SUBMISSION.md created — context extraction complete."

You:  Implement the Contract entity module for eksad-svc-contracts.
      Fields: contractNumber (String), amount (BigDecimal), startDate (Long), endDate (Long).

AI:   ### 🗂️ Implementation Plan — Contract Entity Module

      Scope: Create the full Contract module for eksad-svc-contracts (entity, module type,
      repository, DTO, service, resource, Flyway DDL).

      | # | File                                          | Action | Pattern / Approach                                      | Risk / Notes                         |
      |---|-----------------------------------------------|--------|---------------------------------------------------------|--------------------------------------|
      | 1 | src/.../entity/ContractEntity.java            | Create | extends BaseEntity + @SuperBuilder + tenant_id          | Verify BaseEntity import path        |
      | 2 | src/.../module/ContractModuleType.java         | Create | interface, PREFIX = EKSAD_SVC_CONTRACTS                 | —                                    |
      | 3 | src/.../dto/ContractDTO.java                   | Create | Plain DTO, no JPA annotations                           | —                                    |
      | 4 | src/.../repository/ContractRepository.java     | Create | extends BaseRepository + createFlow/updateFlow/deleteFlow | toNewEntity() must set tenantId     |
      | 5 | src/.../service/ContractService.java           | Create | @ApplicationScoped + @WithSession + @ReactiveTransactional on writes | —               |
      | 6 | src/.../resource/ContractResource.java         | Create | @Path /api/v1/contracts + @RolesAllowed on every method | @RolesAllowed cannot be missing      |
      | 7 | src/main/resources/db/migration/V2__create_contract_table.sql | Create | BIGSERIAL + tenant_id + deleted_at + version + indexes | Check current max Flyway version |

      Depends on: BaseEntity, BaseRepository, getUserContext() — must exist in project.

      ⏸ Waiting for approval — reply "proceed" to start implementation.

You:  proceed

AI:   [writes all 7 files completely]
      [updates PLAN_SUBMISSION.md tracker: tasks 1–7 → Done, Iteration 1]

# Second iteration — Phase ⓪ loads existing file in seconds
AI:   Module plan loaded from PLAN_SUBMISSION.md — context ready.
      [immediately ready for Phase ①]
```

---

## 🛠️ Supported Tools

| Tool | Config File | How Context Works |
|------|-------------|-------------------|
| **GitHub Copilot** | `.github/copilot-instructions.md` | Rules embedded directly — Copilot reads this file automatically in VS Code & JetBrains. Rules cannot reference external files. |
| **Cursor** | `.cursor/rules/eksad-dev.mdc` | Rules + `@file` references. Cursor attaches referenced files to context automatically when you open a file or start a chat. |
| **Claude Code** | `CLAUDE.md` (project root) | Fully reads referenced files via `Read()` at session start. Most powerful: can read all `_base/` files on demand. |

> 💡 **Recommendation:** Use **Claude Code** for the richest context (reads full standards files). Use **Cursor** for fast inline completions. Use **Copilot** if your team is already on GitHub Copilot and doesn't want another tool.

---

## 🧭 Role → File Map

| Role | Copilot | Cursor | Claude Code |
|------|---------|--------|-------------|
| **BE Developer** | `developer/COPILOT_DEV_INSTRUCTIONS.md` | `developer/CURSOR_DEV_RULES.md` | `developer/CLAUDE_CODE_DEV_INSTRUCTIONS.md` |
| **FE Developer** | `developer-fe/COPILOT_DEV_FE_INSTRUCTIONS.md` *(Phase 2)* | `developer-fe/CURSOR_DEV_FE_RULES.md` *(Phase 2)* | `developer-fe/CLAUDE_CODE_DEV_FE_INSTRUCTIONS.md` *(Phase 2)* |
| **Technical Leader** | `technical-leader/COPILOT_TL_INSTRUCTIONS.md` *(Phase 3)* | `technical-leader/CURSOR_TL_RULES.md` *(Phase 3)* | `technical-leader/CLAUDE_CODE_TL_INSTRUCTIONS.md` *(Phase 3)* |
| **QA Engineer** *(Mode B — Automation)* | `qa/COPILOT_QA_INSTRUCTIONS.md` *(Phase 6)* | `qa/CURSOR_QA_RULES.md` *(Phase 6)* | `qa/CLAUDE_CODE_QA_INSTRUCTIONS.md` *(Phase 6)* |

> **QA has two surfaces:** the **GPT/Claude assistant** (`gpt/qa/` — Mode A: Test Plan, RTM, test cases from FSD)
> and the **in-IDE agent above** (Mode B: turns `TC-NNN` cases into REST Assured / Playwright / k6 scripts).
> The QA agent writes **test code only** — reads production code read-only, never edits `src/main/**`.
> See `EKSAD_TESTING_GUIDE.md §2.1` (ownership) and `§2.2` (modes).

---

## 🚀 One-Time Project Setup (All Tools)

Before deploying any config file, do this **once per project repo**:

### Step 1 — Copy EKSAD Standards into the Repo

```bash
# From your project repo root:
mkdir -p docs/eksad

# Copy the entire _base/ folder from the curated knowledge repository:
cp -r /path/to/eksad-agentic-knowledge/EKSAD/gpt/_base  docs/eksad/_base
```

This gives you the knowledge files at a consistent path:
```
{project-root}/
└── docs/
    └── eksad/
        ├── _base/
        │   ├── EKSAD_BASE_PRINCIPLES.md
        │   ├── EKSAD_CODING_STANDARDS.md
        │   ├── EKSAD_SYSTEM_DESIGN_PATTERNS.md
        │   ├── EKSAD_TESTING_GUIDE.md
        │   ├── EKSAD_SPRING_BOOT_MAPPINGS.md
        │   ├── EKSAD_DOMAIN_GLOSSARY.md
        │   └── ...
        └── plans/                        ← auto-generated by AI on first iteration
            ├── PLAN_SUBMISSION.md        ← BE/FE: context + implementation tracker
            ├── PLAN_APPROVAL.md
            ├── PLAN_SUBMISSION_REVIEW.md ← TL: context + review findings tracker
            └── ...
```

> 💡 **Commit `docs/eksad/plans/` to your repo.** Every developer and TL on the team can load full module context instantly — without re-reading TSD. The tracker section also serves as a living progress log per sprint.

> ⚠️ **Add to `.gitignore` if you don't want these committed**, or commit them — either works. The files are read-only reference material.

### Step 2 — Add to `.gitignore` (Optional)

```gitignore
# EKSAD AI context files — local only
docs/eksad/
```

### Step 3 — Deploy the Config File for Your Tool + Role

Pick your tool from the table above and follow the tool-specific steps below.

---

## 🔵 Tool 1: GitHub Copilot

**Supported in:** VS Code (Copilot Chat), JetBrains IDEs (Copilot plugin)
**Not supported:** Eclipse (no `.github/copilot-instructions.md` support — use session primer method instead)

### Deploy Steps

```bash
# From project repo root:
mkdir -p .github
cp /path/to/eksad-agentic-knowledge/EKSAD/gpt/vibe-coding/developer/COPILOT_DEV_INSTRUCTIONS.md \
   .github/copilot-instructions.md
```

### How It Works

- VS Code reads `.github/copilot-instructions.md` automatically on every Copilot Chat interaction
- The rules apply to **all** Copilot interactions in that workspace — inline completions AND chat
- No further setup needed

### Limitations

- Copilot **cannot reference external files** — all rules must be embedded in the one file
- If `EKSAD_CODING_STANDARDS.md` changes, you must manually update the embedded rules
- Context window is shared with your code — keep the instructions concise (already done in the provided file)

---

## 🟢 Tool 2: Cursor

**Supported in:** Cursor editor (cursor.sh)

### Deploy Steps

```bash
# From project repo root:
mkdir -p .cursor/rules
cp /path/to/eksad-agentic-knowledge/EKSAD/gpt/vibe-coding/developer/CURSOR_DEV_RULES.md \
   .cursor/rules/eksad-dev.mdc
```

### How It Works

- Cursor reads `.cursor/rules/*.mdc` files as persistent rules for Cursor Agent and Chat
- The file uses `@file` syntax to reference `docs/eksad/_base/` files — Cursor attaches them automatically
- When you type in Cursor Chat, the AI already has EKSAD standards in context

### Tips

- Use **Cursor Agent** (Cmd+I / Ctrl+I) for multi-file generation (entity + repo + service in one go)
- The `@file` references in the rules file work best when `docs/eksad/_base/` files are in the same repo
- Cursor also supports `@codebase` to include all repo files — pair with the rules for best results

---

## 🟣 Tool 3: Claude Code

**Supported in:** Claude Code CLI (`claude` command) — works in any terminal/editor

### Deploy Steps

```bash
# From project repo root:
cp /path/to/eksad-agentic-knowledge/EKSAD/gpt/vibe-coding/developer/CLAUDE_CODE_DEV_INSTRUCTIONS.md \
   CLAUDE.md
```

### How It Works

- Claude Code reads `CLAUDE.md` at the **start of every session** automatically
- The file instructs Claude Code to `Read()` the `docs/eksad/_base/` files before writing code
- This gives Claude Code **full access** to all EKSAD standards, not just a condensed version
- Most powerful of the three tools for large-scale feature implementation

### Tips

- Claude Code can implement an entire feature module (entity + repo + service + resource + Flyway + tests) in one session
- Start sessions with: `Implement the [entity name] module. Check CLAUDE.md for EKSAD standards.`
- For code review: `Review all Java files in src/ for EKSAD compliance.`
- Use `--continue` flag to resume previous sessions without losing context

---

## 🔄 Maintenance Policy

| When | Action |
|------|--------|
| `_base/` files updated | Re-copy `docs/eksad/_base/` to project repos (`cp -r _base/ {project}/docs/eksad/_base/`) |
| Copilot instructions need update | Re-copy `COPILOT_DEV_INSTRUCTIONS.md` → `.github/copilot-instructions.md` |
| Cursor rules need update | Re-copy `CURSOR_DEV_RULES.md` → `.cursor/rules/eksad-dev.mdc` |
| Claude Code instructions need update | Re-copy `CLAUDE_CODE_DEV_INSTRUCTIONS.md` → `CLAUDE.md` |
| Quarkus version bumps | Update version in source files here, then re-deploy to all project repos |
| New module starts | AI auto-generates `docs/eksad/plans/PLAN_<MODULE>.md` on first iteration — commit it to repo |
| Module plan needs update | Edit `docs/eksad/plans/PLAN_<MODULE>.md` directly in the project repo — it's a living document |

> 📌 **Single source of truth:** Always edit files in `gpt/vibe-coding/` here, then re-deploy to project repos. Never edit `.github/copilot-instructions.md` / `.cursorrules` / `CLAUDE.md` directly in project repos — those are deployment targets, not sources.

---

## 📊 Tool Comparison

| Feature | Copilot | Cursor | Claude Code |
|---------|---------|--------|-------------|
| Reads external files | ❌ No | ✅ Via `@file` | ✅ Via `Read()` |
| Full standards context | ❌ Embedded only | ✅ Auto-attach | ✅ Full files |
| Inline completions | ✅ Best-in-class | ✅ Good | ⚠️ Terminal only |
| Multi-file generation | ⚠️ Limited | ✅ Agent mode | ✅ Best-in-class |
| Code review | ⚠️ Limited | ✅ Good | ✅ Best-in-class |
| Setup complexity | 🟢 Low | 🟡 Medium | 🟢 Low |
| Cost | GitHub Copilot license | Cursor subscription | Claude Pro / API |
