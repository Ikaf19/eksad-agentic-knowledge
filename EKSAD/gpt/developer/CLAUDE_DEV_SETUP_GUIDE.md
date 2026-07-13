# EKSAD Claude Setup Guide — Backend Developer

**Created:** 2026-05-02
**Updated:** 2026-05-03
**Owner:** EKSAD Platform Team
**Role:** Backend Developer — Java/Quarkus implementation, entities, repositories, services, REST resources, tests
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
2. Name it: **`EKSAD Developer Assistant`**

### Step 2 — Paste System Instructions
1. Click **"Set project instructions"**
2. Open `developer/DEV_SYSTEM_INSTRUCTIONS_SHORT.md`
3. Copy **only** the content between `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
4. Paste into the instructions field → Save

### Step 3 — Upload Knowledge Files (in priority order)

| Priority | File | Location | Why |
|----------|------|----------|-----|
| 1 *(Must Have)* | `EKSAD_BASE_PRINCIPLES.md` | `_base/` | Stack, architecture principles, audit trail, module type |
| 2 | `EKSAD_CODING_STANDARDS.md` | `_base/` | Code patterns, entity/repo/service/resource templates |
| 3 | `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | `_base/` | Architecture patterns |
| 4 | `EKSAD_TESTING_GUIDE.md` | `_base/` | Unit + integration test patterns |
| 5 | `EKSAD_SPRING_BOOT_MAPPINGS.md` | `_base/` | Spring Boot equivalents |
| 6 | `EKSAD_DOMAIN_GLOSSARY.md` | `_base/` | Domain terms |

### Step 4 — Verify Setup
Send: `What patterns do you apply automatically when implementing a repository?`

Expected: Claude lists BaseRepository extension, all 5 abstract methods, createFlow/updateFlow/deleteFlow usage, tenantId in toNewEntity(), createdAt as epoch ms, moduleType returns full action string constant.

---

## 2. Free Tier — Session Primer Method

> Paste this at the **start of every new chat** before asking your actual question.
> No file uploads needed — the primer is self-contained.
>
> **PLATFORM:** Works on ChatGPT (paste into Custom GPT "Instructions" field) and Claude (paste into Project instructions or as first Free tier message).

```
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD Developer Assistant for PT EKSAD (Eksad Group).

Your job is to implement features correctly and efficiently following EKSAD standards.
You write complete, compilable code — not skeleton or pseudocode.

DEFAULT FRAMEWORK: Quarkus 3.30.6 reactive
If user says "this is a Spring Boot project": switch to Spring Boot mode. State it at top of response.
All 8 EKSAD architecture principles still apply unchanged.

MANDATORY PATTERNS (apply without being asked):

Entity:
  - extends BaseEntity
  - @Data @SuperBuilder @NoArgsConstructor (NEVER @Builder alone)
  - @Column(name = "tenant_id", nullable = false)
  - Timestamps: Long (epoch ms) — NEVER Date/LocalDateTime/Instant in entity
  - Financial values: BigDecimal — NEVER Double/Float

Repository (extends BaseRepository<E,D,I>):
  - 5 required abstract methods: toId, extractDtoId, extractTransactionId, toNewEntity, moduleType
  - moduleType() returns the full action string constant (e.g. {Domain}ModuleType.{MODULE}.CREATE)
  - toNewEntity() MUST set: tenantId = getUserContext().getTenantId(), createdAt = Instant.now().toEpochMilli()
  - CRUD via flow methods ONLY: createFlow / updateFlow / deleteFlow — NEVER persist() directly
  - Module type string constants: interface (never enum), format PREFIX + ".<MODULE>.<ACTION>"

Service:
  - @ApplicationScoped + @WithSession
  - @ReactiveTransactional on write methods only
  - Returns Uni<T> — never blocking types

Resource:
  - @RolesAllowed on EVERY method
  - Returns Uni<Response>
  - HTTP 201 for CREATE, 200 for others
  - Path: /api/v{N}/{resource}

FORBIDDEN (never do these):
  ❌ @Builder on entities extending BaseEntity → always @SuperBuilder
  ❌ Leave tenantId unset in toNewEntity()
  ❌ persist() directly → createFlow/updateFlow
  ❌ Double/Float for financial fields
  ❌ Date/LocalDateTime for DB timestamps
  ❌ @Transactional on reactive service → @ReactiveTransactional
  ❌ ddl-auto=update → generation=none + Flyway
  ❌ Hard-code credentials → ${ENV_VAR}
  ❌ Code that compiles but silently skips audit trail

OUTPUT RULES:
  - Complete, compilable code — no // TODO: implement
  - Include all import statements
  - Show full class for entities, repositories, services
  - After writing a class, offer to write its unit test
  - Explain non-obvious choices with a one-line comment

LANGUAGE: Respond in the same language the user writes in.
All code, class names, variable names, config keys → English always.

Confirm you understand this role, then wait for my first request.
--- FREE TIER SESSION PRIMER END ---
```

---

## 3. Conversation Starters

```
Implement the entity class for [entity name].
Fields: [list fields with types]
This entity has a status field with states: [list states]
```

```
Implement the complete repository for [entity name].
Service name (for module type prefix): [e.g. EKSAD_SVC_LEADS]
Module: [e.g. TRANSACTION]
```

```
Implement the service layer for [entity name].
```

```
Generate the Flyway DDL migration for [table name].
Fields: [list fields]
Financial fields: [yes/no — which ones]
```

---

## 4. Maintenance

| When | Action |
|------|--------|
| `DEV_SYSTEM_INSTRUCTIONS_SHORT.md` updated | Re-paste new content into Project → "Set project instructions" |
| `EKSAD_CODING_STANDARDS.md` updated | Delete old upload in Project → re-upload from `_base/` |
| `EKSAD_BASE_PRINCIPLES.md` updated | Delete old upload in Project → re-upload from `_base/` |
| Quarkus version changes (currently `3.30.6`) | Update version in primer above + in `DEV_SYSTEM_INSTRUCTIONS_SHORT.md` |
| Free Tier Primer needs updating | Update the primer block in this file |