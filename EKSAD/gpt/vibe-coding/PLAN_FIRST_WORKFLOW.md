# EKSAD Vibe Coding — Plan-First Workflow

**Created:** 2026-05-16
**Updated:** 2026-05-17
**Owner:** EKSAD Platform Team
**Applies to:** All vibe coding instruction files — developer (BE), developer-fe, technical-leader, qa

> **This document is the single source of truth for the Plan-First Workflow.**
> All 9 vibe coding instruction files reference this workflow. When the workflow changes, update this file first, then update the instruction files.

---

## 🧭 The 5-Phase Workflow

Every implementation session **must** follow this sequence — no exceptions.

```
┌────────────────────────────────────────────────────────────────┐
│  ⓪ EXTRACT     AI reads TSD → generates PLAN_<MODULE>.md      │
│  ① BRIEF       User describes the task to the AI              │
│  ② PLAN        AI outputs a structured implementation plan     │
│  ③ REVIEW      Human reads the plan, asks questions if needed  │
│  ④ IMPLEMENT   Human approves → AI writes the code            │
└────────────────────────────────────────────────────────────────┘
```

| Phase | Actor | Output | Runs |
|-------|-------|--------|------|
| ⓪ Extract | 🤖 AI | `PLAN_<MODULE>.md` — persistent context file | First iteration only (or if file missing) |
| ① Brief | 🧑 Human | Natural language task description | Every iteration |
| ② Plan | 🤖 AI | Structured plan table + scope summary | Every iteration |
| ③ Review | 🧑 Human | Questions, changes, or approval | Every iteration |
| ④ Implement | 🤖 AI | Complete, compilable code | Every iteration |

> ⚠️ **The AI must never skip Phase ② and go directly to Phase ④**, even for "simple" tasks.
> Every task — large or small — requires a plan before code is written.
>
> ⚡ **Phase ⓪ runs only once per module.** On subsequent iterations, the AI loads `PLAN_<MODULE>.md` directly — no need to re-read the full TSD.

---

## ⓪ Phase 0 — Context Extraction

### When Phase 0 Runs

```
if docs/eksad/plans/PLAN_<MODULE>.md exists:
    → Read() that file only — skip TSD entirely — go to Phase ①
else:
    → Scan tsd/ folder → read all TSD files for this module
    → Generate PLAN_<MODULE>.md with all 6 sections
    → Write/save the file to docs/eksad/plans/
    → Confirm to user: "PLAN_<MODULE>.md created — context extraction complete."
    → Go to Phase ①
```

### Naming Convention

| TSD Filename | PLAN file |
|---|---|
| `TSD-01 — Auth & Gateway.md` | `PLAN_AUTH.md` |
| `TSD-02 — Submission.md` | `PLAN_SUBMISSION.md` |
| `TSD-03 — Approval.md` | `PLAN_APPROVAL.md` |
| `TSD-04 — Aggregation & Dashboard.md` | `PLAN_AGGREGATION.md` |
| `TSD-05 — Master Data.md` | `PLAN_MASTER_DATA.md` |

**Rule:** Take the module name after `— ` in the TSD filename → uppercase → replace spaces with `_` → prefix `PLAN_` → store in `docs/eksad/plans/`.

### `PLAN_<MODULE>.md` — Full Format (6 Sections)

All 6 sections are **mandatory**. This file is generated on Phase ⓪ and **continuously updated** throughout the project lifecycle.

---

```markdown
# PLAN_<MODULE> — [Module Name] Module Context

**Generated:** [date]
**Module:** [module name from TSD]
**Service:** [service name, e.g. eksad-svc-submission]
**TSD Source:** [filename, e.g. TSD-02 — Submission.md]
**Last Updated:** [date of last update]

---

## 1. Module Summary

[2–4 sentences: what this module does, its role in the system, and key business context.]

---

## 2. Key Entities & Relationships

| Entity | Table | Key Fields | Relationships |
|--------|-------|-----------|---------------|
| `SubmissionEntity` | `submission` | id, tenant_id, status, submitted_by | belongs to TenantEntity via tenant_id |
| … | … | … | … |

---

## 3. API Contracts

| Method | Path | Auth | Request Body | Response |
|--------|------|------|-------------|----------|
| `POST` | `/api/v1/submissions` | `ROLE_SUBMITTER` | `SubmissionDTO` | `201 SubmissionEntity` |
| `GET` | `/api/v1/submissions/{id}` | `ROLE_SUBMITTER, ROLE_APPROVER` | — | `200 SubmissionEntity` |
| … | … | … | … | … |

---

## 4. Business Rules

1. [Rule extracted from TSD — e.g. "A submission can only be approved if status = SUBMITTED."]
2. [Rule — e.g. "Only the original submitter or a ROLE_APPROVER can view a submission."]
3. [Add one rule per line — be specific and actionable]

---

## 5. Implementation Decisions

| Decision | Chosen Approach | Reason |
|----------|----------------|--------|
| Status field type | String literal constants in interface | EKSAD standard — no enum |
| Timestamp fields | `Long` (epoch ms) | EKSAD standard |
| Soft delete | `deleted_at BIGINT` + `deleted_by VARCHAR` from `BaseEntity` | EKSAD standard |
| … | … | … |

---

## 6. Implementation Tracker

> **AI must update this tracker immediately after every task is completed — do not batch.**
> Status values: `Pending` / `In Progress` / `Done` / `Skipped`

| # | Task | Status | Iteration | Notes |
|---|------|--------|-----------|-------|
| 1 | Create `SubmissionEntity.java` | Pending | — | — |
| 2 | Create `SubmissionModuleType.java` | Pending | — | — |
| 3 | Create `SubmissionDTO.java` | Pending | — | — |
| 4 | Create `SubmissionRepository.java` | Pending | — | — |
| 5 | Create `SubmissionService.java` | Pending | — | — |
| 6 | Create `SubmissionResource.java` | Pending | — | — |
| 7 | Create `V{N}__create_submission_table.sql` | Pending | — | — |
| 8 | Write unit tests for `SubmissionService` | Pending | — | — |
```

---

### Tracker Update Rule

After completing each task in Phase ④:
1. Update the task row: set `Status` to `Done`, set `Iteration` to the current iteration number (1, 2, 3…)
2. If a task was intentionally skipped: set `Status` to `Skipped` + note the reason in `Notes`
3. Save the file immediately — do not wait for end of session

> 🔒 **This ensures the tracker remains accurate even if the session is interrupted mid-way.**

---

## 📋 Standard Plan Output Format

When the AI outputs a plan (Phase ②), it **must** use exactly this format:

---

### 🗂️ Implementation Plan — [Task Name]

**Scope:** [1 sentence — what is being built and which service/module it belongs to]

| # | File | Action | Pattern / Approach | Risk / Notes |
|---|------|--------|--------------------|--------------|
| 1 | `relative/path/to/File.java` | Create | [EKSAD pattern being applied] | [Risk or "—"] |
| 2 | `relative/path/to/Other.java` | Modify | [what changes and why] | [Risk or "—"] |
| … | … | … | … | … |

**Depends on:** [list any existing classes/services this implementation depends on, or "—"]

⏸ **Waiting for approval — reply "proceed" to start implementation.**

---

### Column Definitions

| Column | What to Write |
|--------|--------------|
| **File** | Relative path from project root. Full path, not just filename. |
| **Action** | `Create` / `Modify` / `Delete` — what happens to this file |
| **Pattern / Approach** | The EKSAD pattern applied: e.g. `Entity extends BaseEntity + @SuperBuilder`, `extends BaseRepository<E,D,I> + createFlow/updateFlow/deleteFlow`, `V{N}__description.sql — adds tenant_id + deleted_at + version`, `@ApplicationScoped + @WithSession + @ReactiveTransactional on writes` |
| **Risk / Notes** | Non-obvious decisions, dependencies, potential issues, or `—` if none |

---

## 📝 Worked Example — Lead Entity Module

Below is what a correct plan looks like for: *"Implement the Lead entity module for eksad-svc-leads"*

---

### 🗂️ Implementation Plan — Lead Entity Module

**Scope:** Create the full Lead entity module for `eksad-svc-leads` — entity, repository, service, REST resource, module type constants, and Flyway DDL migration.

| # | File | Action | Pattern / Approach | Risk / Notes |
|---|------|--------|--------------------|--------------|
| 1 | `src/main/java/id/eksad/svc/leads/entity/LeadEntity.java` | Create | `extends BaseEntity` + `@SuperBuilder @Data @NoArgsConstructor @AllArgsConstructor` + `tenant_id VARCHAR(100) NOT NULL` + timestamps as `Long` (epoch ms) | Verify `BaseEntity` path matches project structure |
| 2 | `src/main/java/id/eksad/svc/leads/module/LeadModuleType.java` | Create | `interface` (never `enum`) — constants format: `EKSAD_SVC_LEADS.LEAD.CREATE/UPDATE/DELETE` | Must match prefix convention `EKSAD_SVC_{SERVICE_UPPER}` |
| 3 | `src/main/java/id/eksad/svc/leads/repository/LeadRepository.java` | Create | `extends BaseRepository<LeadEntity, LeadDTO, Long>` — implement all 5 abstract methods — CRUD via `createFlow`/`updateFlow`/`deleteFlow` only | `toNewEntity()` must set `tenantId` from `currentTenantId()` and `createdAt` as epoch ms |
| 4 | `src/main/java/id/eksad/svc/leads/dto/LeadDTO.java` | Create | Plain DTO with matching fields — no JPA annotations | — |
| 5 | `src/main/java/id/eksad/svc/leads/service/LeadService.java` | Create | `@ApplicationScoped + @WithSession` on class — `@ReactiveTransactional` on write methods only — returns `Uni<T>` | Never add `@ReactiveTransactional` to read methods |
| 6 | `src/main/java/id/eksad/svc/leads/resource/LeadResource.java` | Create | `@Path("/api/v1/leads")` — `@RolesAllowed` on every method — HTTP 201 for POST, 200 for GET/PUT/DELETE | `@RolesAllowed` cannot be missing — P1 violation |
| 7 | `src/main/resources/db/migration/V1__create_lead_table.sql` | Create | `BIGSERIAL PK` + `tenant_id VARCHAR(100) NOT NULL` + `deleted_at BIGINT` + `deleted_by VARCHAR` + indexes on `tenant_id` and `deleted_at` | Check current max Flyway version number in `db/migration/` |

**Depends on:** `BaseEntity`, `BaseRepository`, `currentTenantId()` utility — must exist in the project before implementation.

⏸ **Waiting for approval — reply "proceed" to start implementation.**

---

## ✅ Approval Rules

| Trigger | Meaning |
|---------|---------|
| `proceed` | Approved as-is — start implementation |
| `lanjut` | Same as "proceed" |
| `proceed, but [change]` | Approved with stated modification — apply change before coding |
| Any question or comment (not "proceed") | Still in Review phase — AI answers, updates plan if needed, re-posts waiting message |

> 🔒 **The AI must not interpret any non-approval response as approval.** If the user asks a question, answer it and re-post the plan with the waiting message.

---

## 🔄 Mid-Implementation Changes

If the user changes requirements **after** approving:
1. AI stops current implementation
2. AI outputs an **updated plan** (mark changed rows with `⚠️`)
3. AI re-posts the waiting message
4. User says "proceed" again before coding resumes

---

## 📂 Plan Files Location

All generated `PLAN_<MODULE>.md` files are stored in:
```
{project-root}/docs/eksad/plans/
├── PLAN_AUTH.md
├── PLAN_SUBMISSION.md
├── PLAN_APPROVAL.md
└── …
```

> 💡 **Tip:** Commit these files to the repo — every developer and TL can load module context without re-reading the TSD. They also serve as living progress trackers throughout the sprint.

---

## 📚 Reference

This workflow is applied in:
- `developer/CLAUDE_CODE_DEV_INSTRUCTIONS.md` — Step 2 section
- `developer/CURSOR_DEV_RULES.md` — Workflow Gate section
- `developer/COPILOT_DEV_INSTRUCTIONS.md` — Planning Gate section
- `developer-fe/CLAUDE_CODE_DEV_FE_INSTRUCTIONS.md` — Step 2 section
- `developer-fe/CURSOR_DEV_FE_RULES.md` — Workflow Gate section
- `developer-fe/COPILOT_DEV_FE_INSTRUCTIONS.md` — Planning Gate section
- `technical-leader/CLAUDE_CODE_TL_INSTRUCTIONS.md` — Step 2 section
- `technical-leader/CURSOR_TL_RULES.md` — Workflow Gate section
- `technical-leader/COPILOT_TL_INSTRUCTIONS.md` — Planning Gate section
- `qa/CLAUDE_CODE_QA_INSTRUCTIONS.md` — Step 2 Plan Gate (QA Mode B — test automation)
- `qa/CURSOR_QA_RULES.md` — Workflow Gate section (QA Mode B)
- `qa/COPILOT_QA_INSTRUCTIONS.md` — Planning Gate section (QA Mode B)

> **QA variant note:** the QA agent's plan table uses **test-oriented columns** (File · Action · Test Layer ·
> Coverage FSD-ref→cases · Notes) and the persistent context file is `TESTPLAN_<MODULE>.md` (not `PLAN_<MODULE>.md`),
> stored in `docs/eksad/testplans/`. The QA agent writes test code only — see `EKSAD_TESTING_GUIDE.md §2.1/§2.2`.
