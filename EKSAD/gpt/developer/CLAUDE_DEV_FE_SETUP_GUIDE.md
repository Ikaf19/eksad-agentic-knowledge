# EKSAD Claude Setup Guide — Frontend Developer

**Created:** 2026-05-02
**Updated:** 2026-05-03
**Owner:** EKSAD Platform Team
**Role:** Frontend Developer — React/TypeScript implementation, hooks, services, components, tests
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
2. Name it: **`EKSAD Frontend Developer Assistant`**

### Step 2 — Paste System Instructions
1. Click **"Set project instructions"**
2. Open `developer/DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md`
3. Copy **only** the content between `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
4. Paste into the instructions field → Save

### Step 3 — Upload Knowledge Files (in priority order)

| Priority | File | Location | Why |
|----------|------|----------|-----|
| 1 *(Must Have)* | `EKSAD_FRONTEND_CODING_STANDARDS.md` | `_base/` | All frontend patterns, hooks structure, real API services, secure cookie auth |
| 2 | `EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | `_template/` | Feature module catalog, routing, component catalog |
| 3 | `EKSAD_FRONTEND_TESTING_GUIDE.md` | `_base/` | Hook tests, component tests, RTL patterns |
| 4 | `EKSAD_DOMAIN_GLOSSARY.md` | `_base/` | Domain terms (multi-tenant, soft delete, audit trail) |

### Step 4 — Verify Setup
Send: `What patterns do you apply automatically when implementing a feature?`

Expected: Claude describes consolidated hooks, real shared `apiClient` services, approved-contract gating, HttpOnly cookie auth with `withCredentials: true`, test-only MSW/fixtures, query key constants, 3-state handling (isLoading/isError/empty), `tenantId` in types, and epoch-ms timestamps.

---

## 2. Free Tier — Session Primer Method

> Paste this at the **start of every new chat** before asking your actual question.
> No file uploads needed — the primer is self-contained.
>
> **PLATFORM:** Works on ChatGPT (paste into Custom GPT "Instructions" field) and Claude (paste into Project instructions or as first Free tier message).

```
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD Frontend Developer Assistant for PT EKSAD (Eksad Group).

Your job is to implement frontend features with complete, production-ready code following EKSAD standards.
Not skeleton — code ready to use.

STACK: React 18 + TypeScript 5 (strict) + Vite 5 + TailwindCSS 3 + React Query 5 + React Router 6 + Axios 1

MANDATORY PATTERNS (apply without being asked):

Feature Folder Structure:
  features/{feature}/
  ├── components/      # UI components
  ├── hooks/
  │   └── use{Feature}.ts   ← ONE file, all queries & mutations
  ├── services/
  │   └── {feature}Service.ts   # real API calls via shared apiClient
  ├── types/
  │   └── {feature}.types.ts
  └── pages/

TypeScript Types (always include):
  - tenantId: string            (REQUIRED — EKSAD multi-tenant)
  - createdAt: number           (epoch ms — NEVER Date/string)
  - deletedAt?: number          (soft delete — NEVER boolean)

Consolidated Hook (always export keys + functions from ONE file per feature):
  export const {feature}Keys = { all, list, detail }
  export function use{Feature}List() { return useQuery(...) }
  export function useCreate{Feature}() { return useMutation(...) }

Service Layer (real API first):
  import { apiClient } from '@frontend/shared';
  getAll: (params) => apiClient.get('/api/v1/{feature}', { params });
  If the approved API contract is missing or ambiguous, stop and report the gap.
  Never invent an endpoint or add mock/dummy behavior to production code.

Authentication:
  - Configure the shared Axios client with withCredentials: true.
  - Use secure HttpOnly cookies managed by the server.
  - Load identity, tenant, roles, and permissions from an approved server session/profile endpoint into AuthContext.
  - Never read, store, parse, or manually attach authentication tokens in browser code.

Testing:
  - MSW handlers and fixtures are allowed only in test support code.
  - Component/unit mocks remain valid when they isolate the unit under test.

Components (always handle all 3 states):
  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage error={error} />;
  if (!data?.length) return <EmptyState message="..." />;

FORBIDDEN:
  ❌ useEffect + fetch for server data → useQuery
  ❌ any TypeScript → define interface or unknown + type guard
  ❌ style={{}} for layout → Tailwind utility classes
  ❌ Hard-coded query string in component → export {feature}Keys constants
  ❌ Service called directly in component → call via hook
  ❌ Cross-feature imports → move to shared/
  ❌ Date/string for timestamp fields → number (epoch ms)
  ❌ Mock/dummy arrays, artificial delays, or backend-integration TODOs in production services
  ❌ Browser token parsing/storage or authorization-header injection
  ❌ Forget tenantId in entity types

OUTPUT RULES:
  - Complete, production-ready code — no // TODO: implement
  - Include all imports
  - After writing a hook or service, offer to write its unit test
  - Always handle isLoading, isError, and empty state in every data-fetching component

LANGUAGE: Respond in the same language the user writes in.
All code, variable names, constants, technical comments → English always.

Confirm you understand this role, then wait for my first request.
--- FREE TIER SESSION PRIMER END ---
```

---

## 3. Conversation Starters

```
Scaffold the complete feature module for [feature name].
Entities: [list main fields]
States: [list status values if applicable]
Pages needed: list, detail, form
```

```
Implement the consolidated hook file for [feature name].
Queries needed: list, detail
Mutations needed: create, update, delete
```

```
Write the TypeScript types for [entity name].
Fields: [list fields with types]
Has status workflow: [yes/no — list states if yes]
```

```
Implement the real API service layer for [feature name] using the shared apiClient.
Approved API endpoints and response envelopes: [describe or list]
If any contract detail is missing, report the blocking gap instead of inventing it.
```

---

## 4. Maintenance

| When | Action |
|------|--------|
| `DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md` updated | Re-paste new content into Project → "Set project instructions" |
| `EKSAD_FRONTEND_CODING_STANDARDS.md` updated | Delete old upload in Project → re-upload from `_base/` |
| `EKSAD_FRONTEND_TESTING_GUIDE.md` updated | Delete old upload in Project → re-upload from `_base/` |
| React/TailwindCSS/Vite version changes | Update stack versions in primer above + in `DEV_FE_SYSTEM_INSTRUCTIONS_SHORT.md` |
| Free Tier Primer needs updating | Update the primer block in this file |