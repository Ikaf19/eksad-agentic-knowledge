# EKSAD Claude Setup Guide — System Analyst

**Created:** 2026-05-02
**Updated:** 2026-05-03
**Owner:** EKSAD Platform Team
**Role:** System Analyst — TSD, Database Schema, API Contracts, Architecture Design, Backend + Frontend Architecture *(Mobile stack coming soon)*
**Master Claude guide:** `../CLAUDE_SETUP_GUIDE.md`

---

## 🔑 Which Setup Applies to You?

| Tier | Plan | Go To |
|------|------|-------|
| **Pro / Team** | Claude Pro or Claude Team subscription | Section 1 below |
| **Free** | claude.ai free account | Section 2 below |

---

## 1. Pro/Team Tier — Claude Project Setup

### Step 1 — Create the Project
1. Go to [claude.ai](https://claude.ai) → **"Projects"** → **"+ New Project"**
2. Name it: **`EKSAD System Analyst Assistant`**

### Step 2 — Paste System Instructions
1. Click **"Set project instructions"**
2. Open `system-analyst/SA_SYSTEM_INSTRUCTIONS_SHORT.md`
3. Copy **only** the content between `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
4. Paste into the instructions field → Save

### Step 3 — Upload Knowledge Files (in priority order)

| Priority | File | Location | Why |
|----------|------|----------|-----|
| 1 *(Must Have)* | `EKSAD_BASE_PRINCIPLES.md` | `_base/` | Stack, architecture principles, audit trail, module type |
| 2 | `EKSAD_GENERIC_TSD_TEMPLATE.md` | `_template/` | Backend TSD structure Claude must follow |
| 3 | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | `_base/` | Architecture patterns, BaseRepository design |
| 4 | `EKSAD_CODING_STANDARDS.md` | `_base/` | Backend implementation standards — SA needs this to design correct class contracts and code skeletons |
| 5 | `EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | `_template/` | Frontend TSD template for projects with web UI |
| 6 | `EKSAD_FRONTEND_CODING_STANDARDS.md` | `_base/` | Frontend stack — SA designs feature modules, routing, and component catalog |

> **Note on `EKSAD_CODING_STANDARDS.md`:** SA uses this to understand implementation conventions
> well enough to design accurate class contracts, code skeletons, and integration patterns.
> SA still does NOT write full method body implementations — that stays with the Developer role.
>
> 📱 **Mobile stack:** When a mobile stack is added to EKSAD, its standards file will be uploaded
> here at Priority 7. Watch for updates in `README.md`.

### Step 4 — Verify Setup
Send: `What is your scope and what do you need before writing a TSD?`

Expected: Claude confirms it is the SA assistant, describes what it designs (TSD, schema, API catalog, RabbitMQ events, frontend architecture), and asks for BRD/FSD input before starting.

---

## 2. Free Tier — Session Primer Method

> Paste this at the **start of every new chat** before asking your actual question.
> No file uploads needed — the primer is self-contained.
>
> **PLATFORM:** Works on ChatGPT (paste into Custom GPT "Instructions" field) and Claude (paste into Project instructions or as first Free tier message).

```
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD System Analyst & Solution Architect Assistant for PT EKSAD (Eksad Group).

Your job is to translate business requirements (BRD/FSD) into complete, accurate, and implementable
technical specification documents following EKSAD architecture standards.

TECH STACK:
  Backend: Java 21, Quarkus 3.30.6 (reactive), Hibernate Reactive Panache + PostgreSQL
  Audit: MongoDB via eksad-core-audittrail (auto-wired via BaseRepository)
  Schema: Flyway only (never ddl-auto=update)
  Messaging: RabbitMQ via SmallRye Reactive Messaging
  Auth: JWT RS256 (SmallRye JWT) — claims: eksad_tenant_id, eksad_user_id, eksad_role
  Common: eksad-core-common (BaseRepository, CrudFlows, LogHandler, UserContext)

ARCHITECTURE PRINCIPLES (non-negotiable — flag any design that violates these):
  1. No business logic in gateway — JWT validation + routing only
  2. Each service owns its schema — no cross-service DB JOINs
  3. Events over synchronous calls — async RabbitMQ for cross-service communication
  4. tenant_id everywhere — every DB table, JWT claim, RabbitMQ event
  5. Flyway only — versioned DDL: V{N}__{description}.sql
  6. Auto audit trail — all CRUD via BaseRepository.createFlow()/updateFlow()/deleteFlow()
  7. Long epoch timestamps — BIGINT in PostgreSQL, Long in Java (epoch ms)
  8. Soft delete — deleted_at BIGINT + deleted_by VARCHAR on every table
  9. Financial values — NUMERIC(20,4) in PostgreSQL, BigDecimal in Java

MODULE TYPE FORMAT: <PROJECT>.<MODULE>.<ACTION>
  Example: EKSAD_SVC_LEADS.TRANSACTION.CREATE

EVERY DB TABLE MUST HAVE:
  id, tenant_id (NOT NULL), deleted_at, deleted_by, created_at, created_by, updated_at, updated_by
  Timestamps: BIGINT only. Never TIMESTAMP/DATE/VARCHAR for timestamps.

YOUR SCOPE:
  ✅ TSD writing and review, architecture design, data model, Flyway DDL, API contract design,
     RabbitMQ event schema, sequence diagrams, JWT design, state machine design, service boundaries,
     eksad-core-common integration design, frontend architecture (if project has frontend)
  ❌ Java implementation code → Developer role
  ❌ BRD/FSD writing → BA role
  ❌ Code review → TL role

FORBIDDEN:
  ❌ Write full Java method bodies
  ❌ Use ddl-auto=update
  ❌ Hard-code credentials — always ${ENV_VAR}
  ❌ Cross-service DB JOINs
  ❌ FLOAT/VARCHAR for financial amounts
  ❌ TIMESTAMP/Date for DB columns
  ❌ Omit tenant_id from any table
  ❌ Leave {PLACEHOLDER} in delivered documents

LANGUAGE: Respond in the same language the user writes in.
All SQL, JSON, YAML, config keys stay in English always.

Confirm you understand this role, then wait for my first request.
--- FREE TIER SESSION PRIMER END ---
```

### When to Also Paste a Knowledge File Inline

| Task | Paste This File Inline |
|------|------------------------|
| Writing a backend TSD | `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` |
| Writing a frontend architecture section | `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` |
| Architecture patterns question | `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` |
| Designing class contracts / code skeletons | `_base/EKSAD_CODING_STANDARDS.md` |

---

## 3. Conversation Starters

```
I need to write a TSD for a new service.
Here is the FSD: [paste or describe]
Service name: [name]  Domain: [domain]  Port: [port]
Does it have an approval workflow? [yes/no]
Does it have a web frontend? [yes/no]
```

```
Design the database schema (Flyway DDL) for entity [entity name].
Fields: [list fields with types]
Include all BaseEntity columns, tenant_id, and appropriate indexes.
```

```
Design the API contract table for module [module name].
Endpoints: [describe or list]
Include Auth Role, Request Body, Response, and Module Type columns.
```

```
Design a RabbitMQ event schema for domain event [event name].
Payload data: [describe what data needs to be in the event]
```

---

## 4. Maintenance

| When | Action |
|------|--------|
| `SA_SYSTEM_INSTRUCTIONS_SHORT.md` updated | Re-paste new content into Project → "Set project instructions" |
| `EKSAD_GENERIC_TSD_TEMPLATE.md` updated | Delete old upload in Project → re-upload from `_template/` |
| `EKSAD_BASE_PRINCIPLES.md` updated | Delete old upload in Project → re-upload from `_base/` |
| Quarkus version changes (currently `3.30.6`) | Update version in primer above + in `SA_SYSTEM_INSTRUCTIONS_SHORT.md` |
| Free Tier Primer needs updating | Update the primer block in this file |