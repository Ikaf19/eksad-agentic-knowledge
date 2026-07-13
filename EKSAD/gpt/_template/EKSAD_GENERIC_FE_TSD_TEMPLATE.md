# Technical Specification Document (TSD) — Frontend
# {PROJECT_NAME} — Web Application — Version {VERSION}

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — Technical Specification Document (Frontend) |
| **Document Type** | Technical Specification Document (TSD) — Frontend |
| **Project Name** | {PROJECT_NAME} |
| **Module / Domain** | {MODULE_OR_DOMAIN} |
| **Version** | {VERSION} |
| **Status** | 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)* |
| **System** | `{APP_NAME}` — React Web Application |
| **Organization** | PT EKSAD / {BUSINESS_UNIT} |
| **Classification** | Internal — Confidential |
| **Related BRD** | `BRD_{PROJECT_CODE}_v{VERSION}.md` |
| **Related FSD** | `FSD_{PROJECT_CODE}_v{VERSION}.md` |
| **Related TSD (Backend)** | `TSD_{PROJECT_CODE}_v{VERSION}.md` |
| **Supersedes** | `TSD_FE_{PROJECT_CODE}_v{PREV_VERSION}.md` *(if applicable)* |
| **Prepared By** | {PREPARED_BY} |
| **Reviewed By** | {REVIEWED_BY} |
| **Approved By** | {APPROVED_BY} |
| **Last Updated** | {DATE} |

> **Audience:** System Analysts, Tech Leads, Frontend Developers.
> This document describes **HOW** the frontend is built — component design, routing, state management, API contracts, and testing.
> For **WHAT** the system does (user flows, business rules, acceptance criteria), see `FSD_{PROJECT_CODE}_v{VERSION}.md`.
>
> **Language policy:** This document is English-only from v3. Functional descriptions must follow the FSD authored by the BA/SA team. Do not restate or contradict FSD content — reference FR IDs instead.

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |

---

## Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Business Owner | | | |
| Project Manager | | | |
| Lead SA / System Analyst | | | |
| Tech Lead (Frontend) | | | |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Traceability Matrix](#2-traceability-matrix)
3. [Frontend Architecture Overview](#3-frontend-architecture-overview)
4. [Tech Stack & Versions](#4-tech-stack--versions)
5. [Project Structure](#5-project-structure)
6. [Vite Configuration & Environment Variables](#6-vite-configuration--environment-variables)
7. [Routing Design](#7-routing-design)
8. [Feature Module Catalog](#8-feature-module-catalog)
9. [Component Catalog](#9-component-catalog)
10. [React Query Key Conventions](#10-react-query-key-conventions)
11. [API Consumption Contract](#11-api-consumption-contract)
12. [Test-Only HTTP Simulation](#12-test-only-http-simulation)
13. [Authentication & Authorization (Frontend)](#13-authentication--authorization-frontend)
14. [State Management Design](#14-state-management-design)
15. [Error Handling Strategy](#15-error-handling-strategy)
16. [Testing Strategy](#16-testing-strategy)
17. [Global Frontend Rules](#17-global-frontend-rules)
18. [Gap Analysis](#18-gap-analysis)
19. [Open Issues & Decisions Log](#19-open-issues--decisions-log)
20. [Glossary](#20-glossary)
21. [Appendix — Change Log](#appendix--change-log)

---

## 1. Introduction

### 1.1 Purpose

> *Describe the purpose of this document. Explain that the FE-TSD translates the functional requirements from the FSD into concrete frontend implementation decisions: component design, routing, hook/service structure, API consumption contract. State which FSD version this document is derived from.*

### 1.2 Scope

> *Define the frontend boundary — which screens, feature modules, and integrations are covered and which are explicitly out of scope.*

### 1.3 Intended Audience

| Audience | Purpose |
|---|---|
| System Analyst / SA | Authoring frontend technical design aligned to FSD functional requirements |
| Tech Lead (Frontend) | Reviewing architecture, patterns, and code standards |
| Frontend Developer | Implementing components, hooks, and service layers described here |
| QA Engineer | Deriving browser-side test cases from the Feature Functional Requirements (§8.x.x) |

---

## 2. Traceability Matrix

> *Every frontend component must trace back to a named FR from the FSD. If a component cannot be traced to an FR, it must be escalated — either added to the FSD first, or flagged in Gap Analysis (§18).*
>
> **Columns:** `FR ID` — from FSD; `Feature ID` — parent feature; `Screen / Page` — React page component; `Component` — React component; `Hook / Service Function` — the hook or service method that implements the behaviour.
>
> **Maintenance note:** Function signatures are indicative — mark outdated rows with `[STALE]` and update at each sprint review. Do not delete stale rows until resolved.

| FR ID | Feature ID | Description | Screen / Page | Component | Hook / Service Function |
|---|---|---|---|---|---|
| FR-{MODULE}-001 | F-001 | {FR description — e.g. User can create {entity}} | `{Feature}FormPage` | `{Feature}Form` | `useCreate{Feature}()` → `{feature}Service.create(dto)` |
| FR-{MODULE}-002 | F-001 | {FR description — e.g. User can update {entity}} | `{Feature}FormPage` | `{Feature}Form` | `useUpdate{Feature}()` → `{feature}Service.update(id, dto)` |
| FR-{MODULE}-003 | F-001 | {FR description — e.g. User can soft-delete {entity}} | `{Feature}ListPage` | `{Feature}List` | `useDelete{Feature}()` → `{feature}Service.delete(id)` |
| FR-{MODULE}-004 | F-001 | {FR description — e.g. User can view {entity} list} | `{Feature}ListPage` | `{Feature}List` | `use{Feature}List(params?)` → `{feature}Service.getAll(params)` |
| FR-{MODULE}-005 | F-001 | {FR description — e.g. User can view {entity} detail} | `{Feature}DetailPage` | `{Feature}Detail` | `use{Feature}Detail(id)` → `{feature}Service.getById(id)` |
| FR-AUTH-001 | F-003 | Server-backed session validation — redirect to `/login` if unauthenticated | `AppLayout` | `ProtectedRoute` | `useAuth()` → `authService.getSession()` |
| FR-{MODULE}-{N} | F-{N} | {FR description} | `{Page}` | `{Component}` | `{hook}()` → `{service}.{method}({params})` |

---

## 3. Frontend Architecture Overview

> *Describe the position of this web app in the EKSAD platform: who uses it, which backend service it consumes, and how authentication flows.*

**{PROJECT_NAME} Web Application** is a browser-based interface for {SHORT_DESCRIPTION}. It is used by {USER_GROUP} and communicates with backend service `{SERVICE_NAME}`.

### System Interaction Diagram

```
Browser (React App)
    │
    ├── Auth: secure HttpOnly session cookies issued by {AUTH_SERVICE}
    │         Shared apiClient sends cookies with withCredentials: true
    │         GET {SESSION_ENDPOINT} returns browser-safe identity, tenant,
    │         roles, and permissions for AuthContext
    │         401 response → clear cached session + redirect to /login
    │
    ├── API: {SERVICE_NAME} → {BASE_URL}/api/v1/{domain}
    │         React Query manages caching, stale-time, refetch
    │
    └── Static Assets: Vite build → {CDN / Nginx / Static Host}
```

**Key architecture decisions:**
- Architecture: Modular feature-based (one folder per domain feature)
- Server state: React Query — no Redux/Zustand for server data
- Routing: React Router v6 with `createBrowserRouter`
- API layer: shared `apiClient` (Axios, `withCredentials: true`) → service functions → React Query hooks
- Integration: real approved API contracts from the first implementation; missing contracts are blocking gaps
- HTTP simulation: MSW handlers and fixtures exist in test support code only, never in production services

---

## 4. Tech Stack & Versions

| Technology | Version | Role |
|------------|---------|------|
| React | 18.x | UI framework |
| TypeScript | 5.x (strict) | Type safety |
| Vite | 5.x | Build tool & dev server |
| TailwindCSS | 3.x | Utility-first styling |
| React Query (`@tanstack/react-query`) | 5.x | Server state management |
| React Router | 6.x | Client-side routing |
| React Hook Form | 7.x | Form state management |
| Axios | 1.x | HTTP client (wrapped in `lib/axios.ts`) |
| Jest | 29.x | Test framework |
| React Testing Library | 14.x | Component & hook testing |

---

## 5. Project Structure

```
src/
├── app/
│   ├── App.tsx
│   ├── router.tsx                  # All route definitions
│   └── providers.tsx               # QueryClientProvider, AuthProvider
├── features/
│   ├── {feature-1}/
│   │   ├── components/
│   │   ├── hooks/
│   │   │   └── use{Feature}.ts     # Consolidated hook (queries + mutations)
│   │   ├── services/
│   │   │   └── {feature}Service.ts # Real API calls through shared apiClient
│   │   ├── types/
│   │   │   └── {feature}.types.ts
│   │   ├── utils/
│   │   └── pages/
│   └── {feature-2}/
│       └── ...
├── shared/
│   ├── components/                 # Button, Modal, Table, Badge, etc.
│   ├── hooks/                      # useAuth, usePagination, etc.
│   ├── types/                      # ApiResponse, PaginatedResponse, etc.
│   ├── utils/                      # formatCurrency, getErrorMessage, etc.
│   └── constants/
├── lib/
│   ├── queryClient.ts
│   └── axios.ts                    # App-level Axios config; withCredentials: true; feature code imports shared apiClient
└── main.tsx
```

---

## 6. Vite Configuration & Environment Variables

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: {PORT},
    proxy: {
      '/api': {
        target: '{BACKEND_BASE_URL}',
        changeOrigin: true,
      },
    },
  },
});
```

### Environment Variables

| Variable | Development | Production | Notes |
|----------|-------------|------------|-------|
| `VITE_API_BASE_URL` | `http://localhost:{BACKEND_PORT}` | `https://{PROD_DOMAIN}/api` | Backend base URL |
| `VITE_APP_NAME` | `{APP_NAME} (Dev)` | `{APP_NAME}` | App display name |

> **Rule:** All environment variables **must** be prefixed `VITE_` to be exposed to the browser. Never store secrets in frontend env files.

---

## 7. Routing Design

### Route Structure

```typescript
// app/router.tsx
export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,       // Protected layout with auth check
    children: [
      { index: true, element: <DashboardPage /> },
      // {FEATURE_ROUTES}
      {
        path: '{feature}',
        children: [
          { index: true, element: <{Feature}ListPage /> },
          { path: 'new', element: <{Feature}FormPage /> },
          { path: ':id', element: <{Feature}DetailPage /> },
          { path: ':id/edit', element: <{Feature}FormPage /> },
        ],
      },
    ],
  },
  { path: '/login', element: <LoginPage /> },
  { path: '*', element: <NotFoundPage /> },
]);
```

### Route Catalog

| Path | Component | Description | Auth Required | Roles |
|------|-----------|-------------|--------------|-------|
| `/` | `DashboardPage` | Main dashboard | ✅ | {ROLES} |
| `/{feature}` | `{Feature}ListPage` | List {feature} | ✅ | {ROLES} |
| `/{feature}/new` | `{Feature}FormPage` | Create {feature} form | ✅ | {ROLES} |
| `/{feature}/:id` | `{Feature}DetailPage` | {Feature} detail | ✅ | {ROLES} |
| `/{feature}/:id/edit` | `{Feature}FormPage` | Edit {feature} form | ✅ | {ROLES} |
| `/login` | `LoginPage` | Login page | ❌ | Public |

### ROUTES Constants

```typescript
export const ROUTES = {
  DASHBOARD: '/',
  {FEATURE_UPPER}: {
    LIST: '/{feature}',
    NEW: '/{feature}/new',
    DETAIL: (id: number) => `/{feature}/${id}`,
    EDIT: (id: number) => `/{feature}/${id}/edit`,
  },
} as const;
```

---

## 8. Feature Module Catalog

> *Repeat Section 8.x for each feature module. Every feature must include all required sub-sections.*

---

### 8.1 Feature Module: {Feature 1}

**FSD Source Feature:** F-001 — {Feature 1 Name}
**Folder:** `features/{feature-1}/`
**Status:** 🔴 Draft / 🟡 In Dev / 🟢 Done

#### 8.1.1 Folder Structure

```
features/{feature-1}/
├── components/
│   ├── {Feature1}List.tsx
│   ├── {Feature1}Form.tsx
│   ├── {Feature1}Detail.tsx
│   └── {Feature1}StatusBadge.tsx
├── hooks/
│   └── use{Feature1}.ts          # useQuery + useMutation consolidated
├── services/
│   └── {feature1}Service.ts       # Real API calls through shared apiClient
├── types/
│   └── {feature1}.types.ts
└── pages/
    ├── {Feature1}ListPage.tsx
    ├── {Feature1}DetailPage.tsx
    └── {Feature1}FormPage.tsx
```

#### 8.1.2 Hooks Exported from `use{Feature1}.ts`

| Hook | Type | Query Key | FR Ref | Description |
|------|------|-----------|--------|-------------|
| `use{Feature1}List(params?)` | Query | `['{feature1}', 'list', params]` | FR-{MODULE}-004 | Fetch all with pagination |
| `use{Feature1}Detail(id)` | Query | `['{feature1}', 'detail', id]` | FR-{MODULE}-005 | Fetch detail by ID |
| `useCreate{Feature1}()` | Mutation | — | FR-{MODULE}-001 | Create new record |
| `useUpdate{Feature1}()` | Mutation | — | FR-{MODULE}-002 | Update existing record |
| `useDelete{Feature1}()` | Mutation | — | FR-{MODULE}-003 | Soft-delete record |
| `useSubmit{Feature1}()` | Mutation | — | FR-{MODULE}-{N} | Submit for approval |
| `useApprove{Feature1}()` | Mutation | — | FR-{MODULE}-{N} | Approve record |
| `useReject{Feature1}()` | Mutation | — | FR-{MODULE}-{N} | Reject record |

#### 8.1.3 Feature Functional Requirements (Web)

> *This section maps each FR from the FSD to specific browser-side acceptance criteria. These are the conditions QA will verify in the browser — they are web-scoped (loading state, empty state, error state, role-based rendering) and complement the Given/When/Then in the FSD.*
>
> **Rule:** Every FR listed in the Traceability Matrix (§2) for this feature must have an entry here.

---

**FR-{MODULE}-001 — Create {Entity}**
*FSD Source: FR-{MODULE}-001 · Feature F-001*

| Criterion ID | Given | When | Then |
|---|---|---|---|
| WEB-{M}-001-01 | User is on `/{feature}/new` and has `ROLE_{X}` | Form is displayed | All required fields are visible and submit button is disabled until all required fields are filled |
| WEB-{M}-001-02 | User fills all required fields and submits | `useCreate{Feature1}()` mutation is called | Loading spinner appears on submit button; form becomes non-interactive |
| WEB-{M}-001-03 | Mutation succeeds | API returns `201` with created entity | User is redirected to `/{feature}` list; success toast is shown |
| WEB-{M}-001-04 | Mutation fails with `400` validation error | API returns error codes | Inline error messages appear under the relevant fields |
| WEB-{M}-001-05 | User has `ROLE_VIEWER` | They navigate to `/{feature}/new` | They are redirected away (route guard) or the create button is hidden from the list page |

**Role-based rendering:**
| Role | Create button visible | Form accessible |
|------|----------------------|----------------|
| Super Admin | ✅ | ✅ |
| Admin | ✅ | ✅ |
| {ROLE_1} | ✅ | ✅ |
| Viewer | ❌ | ❌ (redirect) |

---

**FR-{MODULE}-004 — List {Entity}**
*FSD Source: FR-{MODULE}-004 · Feature F-001*

| Criterion ID | Given | When | Then |
|---|---|---|---|
| WEB-{M}-004-01 | User navigates to `/{feature}` | Query `use{Feature1}List()` fires | Loading skeleton / spinner is shown |
| WEB-{M}-004-02 | Query returns data | Data loads successfully | Table renders with correct columns; pagination control shows total pages |
| WEB-{M}-004-03 | Query returns empty array | No data exists for tenant | Empty state component is shown with a "Create {Feature}" call-to-action (if role permits) |
| WEB-{M}-004-04 | Query fails | Network error or `5xx` | `<ErrorMessage>` with retry button is shown; table is not rendered |
| WEB-{M}-004-05 | User changes page | Pagination control clicked | URL query param `?page=N` updates; new page data loads |

---

**FR-{MODULE}-005 — View {Entity} Detail**
*FSD Source: FR-{MODULE}-005 · Feature F-001*

| Criterion ID | Given | When | Then |
|---|---|---|---|
| WEB-{M}-005-01 | User clicks a row or detail link | Navigation to `/{feature}/:id` | `use{Feature1}Detail(id)` query fires; loading state shown |
| WEB-{M}-005-02 | Query succeeds | API returns entity data | All fields rendered read-only; status badge shows current state |
| WEB-{M}-005-03 | `id` does not exist | API returns `404` | `<NotFoundPage>` or inline not-found message is shown |

---

**FR-{MODULE}-002 — Update {Entity}**
*FSD Source: FR-{MODULE}-002 · Feature F-001*

| Criterion ID | Given | When | Then |
|---|---|---|---|
| WEB-{M}-002-01 | User is on `/{feature}/:id/edit` | Form loads | Fields are pre-populated with existing entity values |
| WEB-{M}-002-02 | User submits changes | `useUpdate{Feature1}()` mutation fires | Loading spinner on submit button; form becomes non-interactive |
| WEB-{M}-002-03 | Mutation succeeds | API returns `200` | User is redirected to detail page; React Query cache for this ID is invalidated and refetched |
| WEB-{M}-002-04 | Entity is in `APPROVED` state | User tries to edit | Edit button is hidden or form is read-only; inline message explains the record is locked |

---

**FR-{MODULE}-003 — Delete {Entity}**
*FSD Source: FR-{MODULE}-003 · Feature F-001*

| Criterion ID | Given | When | Then |
|---|---|---|---|
| WEB-{M}-003-01 | User clicks delete | Confirmation modal opens | Modal shows entity name and warns that this action cannot be undone |
| WEB-{M}-003-02 | User confirms deletion | `useDelete{Feature1}()` mutation fires | Loading state on modal confirm button |
| WEB-{M}-003-03 | Mutation succeeds | API returns `200` | Modal closes; row removed from list; list cache invalidated |
| WEB-{M}-003-04 | User cancels | Cancel button clicked | Modal closes; no API call made |

---

#### 8.1.4 State Machine Rendering

> *Complete this section if the entity has statuses. Map each status to its visual representation and allowed actions in the UI.*

| Status | Badge Colour | Edit Allowed | Delete Allowed | Submit Allowed | Approve/Reject Allowed |
|--------|-------------|-------------|---------------|---------------|----------------------|
| `DRAFT` | Grey | ✅ | ✅ | ✅ | ❌ |
| `SUBMITTED` | Yellow | ❌ | ❌ | ❌ | ✅ (approver roles only) |
| `APPROVED` | Green | ❌ | ❌ | ❌ | ❌ |
| `REJECTED` | Red | ✅ (revise) | ✅ | ❌ | ❌ |

---

#### 8.1.5 Reserved Field Rendering

> **SA Action Required (FERULE-011):** This subsection is **mandatory** for every transactional entity feature. If the entity opts in to `BaseTransactionalEntity` (see Backend TSD §12.1), complete the sections below. If not applicable, write "N/A — entity does not opt in to reserved fields" and move on.
>
> See `EKSAD_FRONTEND_CODING_STANDARDS.md §16` for full implementation patterns and `EKSAD_RESERVED_FIELD_PATTERNS.md §9` for config endpoint contracts.

**Schema Endpoint in Use:**
```
GET /api/v1/{entity}/_schema
```
Returns a `ReservedFieldConfig[]` array describing active reserved field slots for this entity.
The `useReservedFields("{entity}")` hook (from `shared/hooks/useReservedFields.ts`) calls this endpoint and caches the result for 60 seconds (`staleTime: 60_000`).

**Hook Registration:**
```tsx
// In {Feature1}Form.tsx — always use the shared hook, never call _schema directly
const { fields, loading, error } = useReservedFields("{feature-entity-name}");
```

**Dynamic Form Rendering — rules SA must document for this feature:**

| Step | What to render | Notes |
|------|---------------|-------|
| Form mount | Call config endpoint via `useReservedFields()` | Show loading skeleton while fetching |
| Config loaded | Group fields by `form_section` and sort by `display_order` | Use `<ReservedFieldSection entity="{entity}" ... />` component |
| Per field | Select input type by `field_key` prefix: `reserved_str_*` → text, `reserved_num_*` → number, `reserved_date_*` → date (epoch-ms ↔ ISO convert), `reserved_bool_*` → checkbox, `reserved_ext` → key-value editor | Use `<ReservedFieldInput config={field} ... />` |
| Validation | Apply `validation_rule` from config (pattern, minValue, maxValue, enum) | Frontend validates; backend re-validates via `ReservedFieldValidator` |
| Conditional | Evaluate `when` clause from config; hide/show field accordingly | Evaluate client-side using same operator set (eq/neq/gt/in/notIn/isNull/isNotNull) |

**SA-defined slot assignments for this feature** *(fill in or write "None — reserved fields not activated for this entity")*:

| Slot | Label (from BA RFC) | Data Type | Required | Validation Rule | Section | Display Order |
|------|-------------------|-----------|----------|-----------------|---------|--------------|
| `reserved_str_1` | {label} | string | ✅/❌ | {rule or —} | {section} | {order} |
| `reserved_str_2` | {label} | string | ✅/❌ | {rule or —} | {section} | {order} |
| *(add rows per activated slot only — inactive slots not needed here)* | | | | | | |

> **Slot allocation source:** Obtain from `docs/eksad/reserved-fields/RFC_{TENANT}_{ENTITY}.md` produced during the BA Reserved Field Discovery session (`business-analyst/BA_SYSTEM_INSTRUCTIONS.md` §8.1).

**List / Table Rendering** *(complete if reserved fields must appear as table columns)*:

| Slot | Column Header | Visible by Default | Sortable | Notes |
|------|-------------|-------------------|---------|-------|
| `reserved_str_1` | {label} | ✅/❌ | ✅/❌ | Only show if `is_visible = true` in config AND tenant has activated this slot |
| *(add per slot as needed)* | | | | |

> Rule: Do NOT hardcode column headers — always derive the header from `config.display_label` returned by the schema endpoint. (FERULE-011)

**File-reference in `reserved_ext`** *(only if `reserved_ext` holds a `file_id`)*:
- If any value inside `reserved_ext` is a `file_id`, resolve the signed URL at render-time via `GET /api/v1/storage/{fileId}/url`.
- Never cache signed URLs in component state.
- Same render-time resolution as `{entity}.{field_name}_file_id` standard fields. (FERULE-012)

---

### 8.2 Feature Module: {Feature 2}

> *Repeat the full structure from §8.1 for each additional feature module. Every feature must have all sub-sections completed.*

---

## 9. Component Catalog

### Shared Components

| Component | Path | Key Props | Description |
|-----------|------|-----------|-------------|
| `Button` | `shared/components/Button.tsx` | `variant`, `isLoading`, `onClick` | Primary, secondary, danger variants |
| `Modal` | `shared/components/Modal.tsx` | `isOpen`, `onClose`, `title` | Confirmation, form, info |
| `Table` | `shared/components/Table.tsx` | `columns`, `data`, `isLoading` | Sortable, with pagination |
| `Badge` | `shared/components/Badge.tsx` | `variant`, `label` | Status badges |
| `LoadingSpinner` | `shared/components/LoadingSpinner.tsx` | `size` | Loading state |
| `ErrorMessage` | `shared/components/ErrorMessage.tsx` | `error`, `onRetry` | Error display with retry |
| `EmptyState` | `shared/components/EmptyState.tsx` | `message`, `action` | Empty data state |
| `Pagination` | `shared/components/Pagination.tsx` | `page`, `totalPages`, `onPageChange` | Pagination control |

### Feature Components — {Feature 1}

| Component | Key Props | FR Ref | Description |
|-----------|-----------|--------|-------------|
| `{Feature1}List` | `onEdit`, `onDelete` | FR-{MODULE}-004 | List view with actions |
| `{Feature1}Form` | `{feature1}Id?`, `onSuccess` | FR-{MODULE}-001, FR-{MODULE}-002 | Create / Edit form |
| `{Feature1}Detail` | `{feature1}Id` | FR-{MODULE}-005 | Detail view read-only |
| `{Feature1}StatusBadge` | `status` | FR-{MODULE}-004 | Colour-coded status badge |

---

## 10. React Query Key Conventions

All query keys are defined as constants and exported from the hooks file:

```typescript
// Naming convention
export const {feature}Keys = {
  all: ['{feature}'] as const,
  list: (params?: {Feature}ListParams) => ['{feature}', 'list', params] as const,
  detail: (id: number) => ['{feature}', 'detail', id] as const,
};
```

**Query keys per feature:**

| Feature | Key Constant | Structure |
|---------|-------------|-----------|
| {Feature 1} | `{feature1}Keys` | `['{feature1}', 'list', params]` / `['{feature1}', 'detail', id]` |
| {Feature 2} | `{feature2}Keys` | `['{feature2}', 'list', params]` / `['{feature2}', 'detail', id]` |

---

## 11. API Consumption Contract

> **Note:** This table describes the backend API that the frontend consumes.
> Frontend implementation starts with these approved real API contracts through the shared `apiClient`.
> Missing or ambiguous paths, methods, authentication/session behavior, or envelopes must be logged as blocking gaps; do not invent production fallbacks.
> See the backend TSD (`TSD_{PROJECT_CODE}_v{VERSION}.md`) for full endpoint specifications.

### {Feature 1} — API Endpoints

| Method | Path | Request Body / Params | Response | Hook | FR Ref | Contract Status |
|--------|------|-----------------------|----------|------|--------|-----------------|
| `GET` | `/api/v1/{feature1}` | `?page=&size=&status=` | `PaginatedResponse<{Feature1}>` | `use{Feature1}List()` | FR-{MODULE}-004 | 🟢 Approved |
| `GET` | `/api/v1/{feature1}/:id` | — | `ApiResponse<{Feature1}>` | `use{Feature1}Detail(id)` | FR-{MODULE}-005 | 🟢 Approved |
| `POST` | `/api/v1/{feature1}` | `{Feature1}FormValues` | `ApiResponse<{Feature1}>` | `useCreate{Feature1}()` | FR-{MODULE}-001 | 🟢 Approved |
| `PUT` | `/api/v1/{feature1}/:id` | `{Feature1}FormValues` | `ApiResponse<{Feature1}>` | `useUpdate{Feature1}()` | FR-{MODULE}-002 | 🟢 Approved |
| `DELETE` | `/api/v1/{feature1}/:id` | — | `ApiResponse<void>` | `useDelete{Feature1}()` | FR-{MODULE}-003 | 🟢 Approved |
| `PATCH` | `/api/v1/{feature1}/:id/submit` | — | `ApiResponse<{Feature1}>` | `useSubmit{Feature1}()` | FR-{MODULE}-{N} | 🟢 Approved |
| `PATCH` | `/api/v1/{feature1}/:id/approve` | `{ comment?: string }` | `ApiResponse<{Feature1}>` | `useApprove{Feature1}()` | FR-{MODULE}-{N} | 🟢 Approved |
| `PATCH` | `/api/v1/{feature1}/:id/reject` | `{ reason: string }` | `ApiResponse<{Feature1}>` | `useReject{Feature1}()` | FR-{MODULE}-{N} | 🟢 Approved |

**Contract Status Legend:**
- 🔴 Blocked — required contract detail is missing or unresolved; implementation must stop and the gap owner must be named
- 🟡 In Review — contract exists but is not yet approved; no endpoint behavior may be invented
- 🟢 Approved — implement directly through the shared `apiClient`

### Service Implementation Contract

```typescript
// features/{feature1}/services/{feature1}Service.ts
import { apiClient } from '@frontend/shared';
import type { ApiResponse, PaginatedResponse } from '@/shared/types/api.types';
import type { {Feature1}, {Feature1}FormValues, {Feature1}ListParams } from '../types/{feature1}.types';

export const {feature1}Service = {
  getAll: (params?: {Feature1}ListParams) =>
    apiClient.get<PaginatedResponse<{Feature1}>>('/api/v1/{feature1}', { params }),
  getById: (id: number) => apiClient.get<ApiResponse<{Feature1}>>(`/api/v1/{feature1}/${id}`),
  create: (data: {Feature1}FormValues) =>
    apiClient.post<ApiResponse<{Feature1}>>('/api/v1/{feature1}', data),
  update: (id: number, data: {Feature1}FormValues) =>
    apiClient.put<ApiResponse<{Feature1}>>(`/api/v1/{feature1}/${id}`, data),
  delete: (id: number) => apiClient.delete<ApiResponse<void>>(`/api/v1/{feature1}/${id}`),
};
```

> Replace placeholders only with values from an approved API contract. Do not create feature-specific credential handling; the shared client owns cookie and response-interceptor configuration.

### TypeScript Types

```typescript
// shared/types/api.types.ts
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  page: number;
  size: number;
}

// features/{feature1}/types/{feature1}.types.ts
export interface {Feature1} {
  id: number;
  tenantId: string;           // EKSAD multi-tenant — always present (FR-AUTH-001)
  {FIELD_1}: {TYPE_1};        // FR-{MODULE}-001
  {FIELD_2}: {TYPE_2};        // FR-{MODULE}-001
  status: {Feature1}Status;   // FR-{MODULE}-001
  createdAt: number;          // epoch milliseconds
  createdBy: string;
  updatedAt?: number;
  updatedBy?: string;
  deletedAt?: number;         // soft delete — null means active
}

export type {Feature1}Status = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED';

export interface {Feature1}FormValues {
  {FIELD_1}: {TYPE_1};
  {FIELD_2}: {TYPE_2};
}

export interface {Feature1}ListParams {
  page?: number;
  size?: number;
  status?: {Feature1}Status;
  search?: string;
}
```

---

## 12. Test-Only HTTP Simulation

Production services always call approved endpoints through the shared `apiClient`. They must not contain fixture arrays, artificial delays, HTTP stubs, or temporary backend-integration branches. If a required contract is unavailable, record a Critical gap in §18 with an owner and block implementation of the affected flow.

MSW handlers and fixtures are permitted only for automated tests and local test runners. Keep them under test support paths such as:

```text
src/test/
├── msw/
│   ├── handlers.ts
│   └── server.ts
└── fixtures/
    └── {feature1}.fixtures.ts
```

Handlers must mirror approved methods, paths, envelopes, status codes, and authorization outcomes. They must never be imported by production entry points or used as a runtime fallback. Component/unit mocks remain valid when they isolate the unit under test and do not replace the application service contract.

---

## 13. Authentication & Authorization (Frontend)

### Authentication Flow

```
1. User accesses app → AuthProvider requests {SESSION_ENDPOINT} through apiClient
2. apiClient sends secure HttpOnly cookies with withCredentials: true
3. Valid session → server returns browser-safe identity, tenant, roles, and permissions
4. AuthProvider stores only that session view in memory and exposes it through AuthContext
5. Missing/expired session or 401 → clear cached session view and redirect to /login
6. Login/logout/refresh are server-managed cookie flows; frontend code cannot inspect credentials
```

### Server Session View Used by Frontend

| Field | Type | Usage | FR Ref |
|-------|------|-------|--------|
| `tenantId` | string | Display context; backend derives authoritative tenant scope from the session | FR-AUTH-001 |
| `userId` | string | User profile and attribution display | FR-AUTH-001 |
| `roles` | string[] | Role-based rendering | FR-AUTH-001 |
| `permissions` | string[] | Action visibility and route UX; backend still enforces access | FR-AUTH-001 |

### Role-Based Rendering Pattern

```typescript
// shared/hooks/useAuth.ts
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

// Usage in component — FR-{MODULE}-001 (role-based action visibility)
const { permissions } = useAuth();
{permissions.includes('FEATURE_APPROVE') && <button>Approve</button>}
```

> **Security rule:** Configure the app-level Axios instance with `withCredentials: true`. The browser must not read, store, parse, or manually attach authentication credentials. Document cookie attributes, CORS credential policy, and CSRF controls in the backend/auth TSD. UI guards improve UX only; backend authorization is authoritative.

---

## 14. State Management Design

| State | Tool | Location | Notes |
|-------|------|----------|-------|
| Server data (lists, detail) | React Query | Automatic in QueryClient cache | Stale time 5 min |
| Form state | React Hook Form | Local in form component | |
| Auth session view | React Query + Context (`AuthContext`) | `app/providers.tsx` | Loaded from approved server session/profile endpoint; in-memory browser-safe fields only |
| Modal open/close | `useState` | Parent component | |
| Pagination & filters | `useSearchParams` | URL query params | Bookmarkable |
| Theme / locale | Context (`AppContext`) | `app/providers.tsx` | If multi-language |

---

## 15. Error Handling Strategy

| Scenario | Handling | Component | FR Ref |
|---------|----------|-----------|--------|
| Query fails (network error) | Show `<ErrorMessage>` inline | `isError` from `useQuery` | All read FRs |
| Mutation fails | Toast error with server message | `onError` callback on `mutate()` | All write FRs |
| Form validation error | Inline error under field | React Hook Form `errors` | All create/update FRs |
| 401 Unauthorized | Clear cached session view and redirect to `/login` | Shared `apiClient` response interceptor / AuthProvider | FR-AUTH-001 |
| 403 Forbidden | Toast "You do not have permission" | Axios response interceptor | FR-AUTH-001 |
| 404 Not Found | Show `<NotFoundPage>` | Router catch-all | All detail FRs |
| Uncaught error | React ErrorBoundary in `AppLayout` | Error boundary | All |

---

## 16. Testing Strategy

### Coverage Targets

| Layer | Target | Tool |
|-------|--------|------|
| Hooks (queries & mutations) | ≥ 90% | Jest + `renderHook` |
| Utility functions | ≥ 95% | Jest |
| Components (user interactions) | ≥ 80% | React Testing Library |
| Pages (smoke test) | ≥ 60% | React Testing Library |

### Test Strategy per Feature

For each feature module, the following tests are mandatory:

1. **Hook test** — test all queries (happy path, error, loading) and mutations (success, error). Add `// FR-{MODULE}-{N}` comment above each test case.
2. **Form component test** — test valid submit, empty field validation, error from service, loading state.
3. **List component test** — test data render, empty state, loading state, error state.
4. **Role-based rendering test** — test that restricted actions are hidden for roles without permission.
5. **HTTP contract test** — use test-only MSW handlers/fixtures to verify approved envelopes plus `401` and `403` behavior. Do not import test handlers into production entry points.

### Test Commands

```bash
# All tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

See `_base/EKSAD_FRONTEND_TESTING_GUIDE.md` for full patterns and code examples.

---

## 17. Global Frontend Rules

> *Rules that apply across all frontend components and features in this TSD.*

| Rule ID | Rule | Applies To |
|---|---|---|
| FERULE-001 | Every hook, service function, and page component must trace to at least one FR ID in the Traceability Matrix (§2). Components with no FR link must be flagged in Gap Analysis (§18). | All feature hooks and components |
| FERULE-002 | Server state must be managed exclusively by React Query. Do not use Redux, Zustand, or `useState` for data fetched from the API. | All feature hooks |
| FERULE-003 | All API calls must go through the service layer (`{feature}Service.ts`). No direct `axios` calls inside components or hooks. | All features |
| FERULE-004 | Role/permission-based rendering must use the server-backed session view from `useAuth()`. Do not hardcode roles or permissions outside `constants/`; backend authorization remains authoritative. | All components with conditional actions |
| FERULE-005 | All environment variables must be prefixed `VITE_`. No secrets in frontend environment files. | Configuration |
| FERULE-006 | Every production service function must call an approved endpoint through the shared `apiClient`. Missing or ambiguous contracts are Critical gaps; no fixture data, artificial delay, runtime HTTP stub, or temporary fallback is allowed. | All service functions |
| FERULE-007 | Signed URLs (for PRIVATE files from `eksad-core-storage`) must never be stored in state or localStorage. Call `GET /api/v1/storage/{fileId}/url` at render-time only. | All file-displaying components |
| FERULE-008 | Pagination and filter state must be stored in URL query params (`useSearchParams`) to allow bookmarking and browser back/forward. | All list pages |
| FERULE-009 | `[STALE]` tag must be applied to any Traceability Matrix row where the hook or service function has changed. Remove only after updating the row. | Traceability Matrix (§2) |
| FERULE-010 | Each test case must include a `// FR-{MODULE}-{N}` comment identifying the FR it verifies. | All test files |
| FERULE-011 | Reserved fields must be rendered dynamically from the schema config endpoint (`GET /api/v1/{entity}/_schema`). Never hardcode reserved field labels, visibility, or input types in component code. Use `useReservedFields(entityType)` hook and `<ReservedFieldSection>` component. Applies to all transactional entity feature forms. | All transactional feature forms and list pages |
| FERULE-012 | If a value stored in `reserved_ext` (JSONB) is a `file_id`, resolve its signed URL at render-time via `GET /api/v1/storage/{fileId}/url` — same pattern as standard `{entity}.{field}_file_id` fields. Never cache signed URLs in state, localStorage, or React Query. Applies to all file-handling features that use reserved JSONB overflow fields. | File-handling features using `reserved_ext` |
| FERULE-013 | Authentication uses secure HttpOnly cookies sent by the shared client with `withCredentials: true`. Browser code must not inspect credentials or implement token/header plumbing; session context comes from the approved server session/profile endpoint. | Auth provider, routing, and all API consumers |

---

## 18. Gap Analysis

> *Record all gaps identified during FE-TSD authoring. Critical gaps block FE-TSD approval.*

> **Rule:** No FE-TSD may be submitted for approval while a Critical gap remains unresolved.

| Gap ID | Description | Severity | Affected Section / Component | Owner | Resolution / Status |
|---|---|---|---|---|---|
| GAP-001 | {DESCRIPTION} | Critical / Non-Critical | {SECTION / COMPONENT} | {OWNER} | Open / Resolved / Deferred |

**Severity Definitions:**
- **Critical** — missing screen design for a core FR, undefined component for a required user flow, or missing API contract for a required integration. Blocks FE-TSD approval.
- **Non-Critical** — minor edge case undefined, non-blocking visual detail. Document may proceed with gap documented and owner assigned.

---

## 19. Open Issues & Decisions Log

> *Track all unresolved frontend questions and decisions tagged `[CLARIFY]` or `[UNCONFIRMED]`. This log must be empty before the document status changes to Approved.*

| Issue ID | Description | Raised By | Owner | Target Date | Status |
|---|---|---|---|---|---|
| ISS-001 | {DESCRIPTION} | {RAISED_BY} | {OWNER} | {DATE} | Open / Resolved / Deferred |

---

## 20. Glossary

| Term | Definition |
|------|------------|
| React Query | `@tanstack/react-query` — manages all server state: fetching, caching, invalidation, background refetch. |
| `useQuery` | React Query hook for read operations. Returns `{ data, isLoading, isError, refetch }`. |
| `useMutation` | React Query hook for write operations (create, update, delete). Returns `{ mutate, isPending, isError }`. |
| Query Key | Unique array identifier for a React Query cache entry. Defined as constants in `{feature}Keys`. |
| Service Layer | `{feature}Service.ts` — all API call functions. The only place Axios is called for a feature. |
| Test-Only HTTP Simulation | MSW handlers and fixtures under test support paths that mirror approved contracts and are excluded from production entry points. |
| `useAuth()` | Shared hook (`shared/hooks/useAuth.ts`) exposing the in-memory, browser-safe session view loaded from the approved server session/profile endpoint. |
| `ProtectedRoute` | Component in `AppLayout` that checks authentication and redirects to `/login` if not authenticated. |
| `[STALE]` | Tag applied to a Traceability Matrix row when the referenced hook or service function has changed. Remove only after updating the row. |
| FR ID | Functional Requirement identifier from the FSD. Format: `FR-{MODULE}-{N}`. |
| Feature ID | Feature identifier from the FSD. Format: `F-{N}`. |
| Signed URL | A time-limited URL for accessing a PRIVATE file from `eksad-core-storage`. Must not be cached or stored client-side. Call at render-time only. |
| `tenant_id` | Authoritative tenant scope enforced by the backend session; exposed to the browser as `tenantId` only when required for display/context. |
| Epoch Milliseconds | All timestamps from the backend are `BIGINT` — ms since 1970-01-01T00:00:00Z. Format with date utility functions before display. |
| Role-Based Rendering | Conditionally showing or hiding UI elements based on roles/permissions from the server-backed session view. Never rely solely on hidden elements for security — backend enforces authorization. |

---

## Appendix — Change Log

| Version | Date | Author | Summary of Changes |
|---------|------|--------|--------------------|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| 1.1 | 2026-04-28 | EKSAD Platform Team | Added `eksad-core-storage` file handling guidance; `file_id` / signed URL rules; `{feature}_file_id` in TypeScript types |
| 3.0 | 2026-05-02 | EKSAD Platform Team | Major upgrade to v3: Document converted to English-only; Document Control table, Revision History & Approval blocks; Introduction (§1); Traceability Matrix (§2) with FR ID → Feature ID → Screen → Component → Hook/Service Function columns; Feature Module Catalog restructured with Feature Functional Requirements (Web) sub-section per feature; FR ref columns and Global Frontend Rules added; Gap Analysis (§18), Open Issues & Decisions Log (§19), and Glossary (§20) added; all sections renumbered |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |
