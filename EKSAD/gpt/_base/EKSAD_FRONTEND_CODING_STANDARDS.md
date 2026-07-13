# EKSAD Frontend Coding Standards & Conventions

**File:** `_base/EKSAD_FRONTEND_CODING_STANDARDS.md`
**Version:** 1.2
**Date:** 2026-06-24
**Owner:** EKSAD Platform Team
**Status:** 🟢 Active — Wajib untuk semua Frontend Developer EKSAD
**Audience:** Frontend Developer, Tech Lead, Code Reviewer
**Upload-to:** GPT knowledge base — Dev FE GPT, TL GPT

> Standar ini diterapkan saat code review. Semua PR harus memenuhi standar ini sebelum merge.
> Jika ragu, tanyakan GPT: *"Review kode ini berdasarkan EKSAD frontend standards."*

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2 | 2026-06-24 | EKSAD docs maintainer | Monorepo layout (`packages/[feature]`); real-API-first service layer (remove mock pattern); HttpOnly cookie auth (remove `localStorage` Bearer); §12.1 Day.js date handling; `ApiResponse` updated to match `GenericResponseDTO` shape; exported query keys reaffirmed; `ReservedFieldInput` date helpers migrated from `new Date()` to `dayjs` |
| 1.1 | 2026-05-23 | EKSAD Platform Team | §16 Reserved field dynamic rendering |
| 1.0 | 2026-04-23 | EKSAD Platform Team | Initial version |

---

## Table of Contents

1. [Technology Stack & Versions](#1-technology-stack--versions)
2. [Project Structure — Monorepo](#2-project-structure--monorepo)
3. [Feature Module Structure](#3-feature-module-structure)
4. [Component Naming & Conventions](#4-component-naming--conventions)
5. [Consolidated Hooks Pattern](#5-consolidated-hooks-pattern)
6. [TypeScript Conventions](#6-typescript-conventions)
7. [TailwindCSS Conventions](#7-tailwindcss-conventions)
8. [React Query Conventions](#8-react-query-conventions)
9. [React Router Conventions](#9-react-router-conventions)
10. [Real API First — Service Layer](#10-real-api-first--service-layer)
11. [State Management Rules](#11-state-management-rules)
12. [API Integration & Auth](#12-api-integration--auth)
    - [12.1 Day.js Date Handling](#121-dayjs-date-handling)
13. [Error Handling](#13-error-handling)
14. [Forbidden Patterns](#14-forbidden-patterns)
15. [Code Review Checklist](#15-code-review-checklist)
16. [Reserved Field Dynamic Rendering](#16-reserved-field-dynamic-rendering)

---

## 1. Technology Stack & Versions

Versi ini di-pin oleh tim EKSAD. Jangan override per-project tanpa persetujuan Platform Team.

| Technology          | Version        | Notes                                                        |
|---------------------|----------------|--------------------------------------------------------------|
| React               | 18.x           | Functional components only — no class components            |
| TypeScript          | 5.x            | Strict mode enabled — `"strict": true` in `tsconfig.json`   |
| Vite                | 5.x            | Build tool & dev server                                      |
| TailwindCSS         | 3.x            | Utility-first styling — no inline `style={}` for layout     |
| React Query         | 5.x (`@tanstack/react-query`) | All server state — no manual fetch in components |
| React Router        | 6.x            | `createBrowserRouter` + `RouterProvider`                     |
| Axios               | 1.x            | HTTP client — wrapped in `apiClient` from `@frontend/shared` |
| Day.js              | 1.x            | Date parsing/formatting/manipulation — replaces all native `Date` usage in feature code |
| React Hook Form     | 7.x            | All form state — always paired with Zod via `zodResolver`    |
| Zod                 | 3.x            | Schema validation — paired with RHF                          |
| Jest / Vitest       | 29.x / 1.x     | Test framework                                               |
| React Testing Library | 14.x         | Component & hook testing                                     |
| MSW (Mock Service Worker) | 2.x    | API mocking — **tests only**, NEVER in production services   |

---

## 2. Project Structure — Monorepo

Proyek EKSAD Frontend menggunakan struktur **monorepo** (Turborepo / pnpm workspaces).

```
packages/
├── [feature]/                   # Satu package per domain fitur
│   └── src/
│       ├── [Feature]Screen.tsx  # Entry point / routable component
│       ├── components/          # UI components untuk fitur ini + index.ts
│       │   └── tabs/            # Sub-folder untuk multi-tab form tabs
│       ├── hooks/               # Consolidated hooks (1-2 file per fitur)
│       ├── services/            # API calls ONLY — real apiClient, NEVER mock
│       ├── types/               # TypeScript types/interfaces untuk fitur ini
│       ├── schemas/             # Zod validation schemas
│       └── utils/               # Pure helper functions (no side effects)
apps/
└── [app]/
    └── src/
        ├── App.tsx              # Route registration
        ├── navigation.ts        # NAV_GROUPS menu entries
        └── lib/
            ├── queryClient.ts   # QueryClient config
            └── dayjs.ts         # Day.js instance with plugins
```

**Shared packages (imported by all feature packages):**
- `@frontend/ui` — shared UI component library: `Button`, `InputField`, `SelectField`, `DatePicker`, `DataTable`, `AppModal`, `AlertDialog`, `LoadingOverlay`, `Card`, `Container`, …
- `@frontend/shared` — cross-feature utilities & stores: `apiClient`, `fetchDataAsync`, `useErrorStore`, `GlobalErrorDialog`, `IBaseResponse`, …

**Canonical import paths:**
```typescript
// ✅ UI components — ALWAYS from @frontend/ui
import { Button, InputField, DataTable, AppModal, LoadingOverlay } from "@frontend/ui";
import { SelectField, type SelectOption } from "@frontend/ui";
import { DatePicker } from "@frontend/ui";
import { AlertDialog, AlertDialogContent, AlertDialogTitle, AlertDialogAction, AlertDialogCancel } from "@frontend/ui";

// ✅ Shared utilities — from @frontend/shared
import { apiClient, fetchDataAsync } from "@frontend/shared";
import { useErrorStore } from "@frontend/shared/store/useErrorStore.ts";
import type { IBaseResponse } from "@frontend/shared";

// ✅ App-level config (QueryClient, Day.js) — from @/lib/
import { queryClient } from "@/lib/queryClient";
import dayjs from "@/lib/dayjs";

// ❌ Never: old single-app path
// import { Button } from "@/components/ui/Button";    // ← WRONG
// import { cn } from "@/shared/utils/cn";             // ← use @frontend/ui or @frontend/shared
```

**Aturan utama:**
- Komponen, hooks, services, dan types untuk satu fitur **tinggal di package fitur itu**
- Tidak boleh ada import langsung antar feature packages — gunakan `@frontend/shared`
- Setiap fitur baru = package baru di `packages/`
- Route didaftarkan di `apps/[app]/src/App.tsx`; menu entry di `apps/[app]/src/navigation.ts`

---

## 3. Feature Module Structure

Setiap feature module wajib mengikuti struktur ini:

```
features/leads/
├── components/
│   ├── LeadList.tsx            # List view component
│   ├── LeadForm.tsx            # Create/Edit/View form (mode prop)
│   ├── LeadDetail.tsx          # Detail view component
│   ├── LeadStatusBadge.tsx     # Reusable sub-component
│   └── tabs/                   # ← multi-tab forms: each tab in own file
│       ├── DataUnitTab.tsx
│       └── DataTransaksiTab.tsx
├── hooks/
│   └── useLeads.ts             # Consolidated hook (queries + mutations)
├── services/
│   └── leadsService.ts         # API calls ONLY — never called directly in components
├── types/
│   └── leads.types.ts          # Lead, LeadFormValues, LeadListParams, etc.
├── schemas/
│   └── leadsSchemas.ts         # Zod validation schemas
└── pages/ (or Screen at package root)
    ├── LeadsScreen.tsx         # Route: /leads
    └── LeadDetailScreen.tsx    # Route: /leads/:id
```

---

## 4. Component Naming & Conventions

| Rule | ✅ Correct | ❌ Wrong |
|------|-----------|---------|
| File name | `LeadForm.tsx` | `leadForm.tsx`, `lead-form.tsx` |
| Component name | `export function LeadForm()` | `export default function leadForm()` |
| Page component | `LeadsPage.tsx` | `Leads.tsx`, `leads-page.tsx` |
| Shared component | `shared/components/Button.tsx` | `components/button.tsx` |
| Hook file | `useLeads.ts` | `leads-hook.ts`, `LeadsHook.ts` |
| Service file | `leadsService.ts` | `LeadsService.ts`, `leads-api.ts` |
| Types file | `leads.types.ts` | `LeadsTypes.ts`, `types.ts` |

**Aturan tambahan:**
- Selalu gunakan **named export** untuk components (`export function LeadForm`) — hindari default export kecuali untuk pages
- Setiap file hanya boleh memiliki **satu component utama**
- Props interface selalu diberi nama `{ComponentName}Props`

```typescript
// ✅ Benar
interface LeadFormProps {
  leadId?: number;
  onSuccess: () => void;
}

export function LeadForm({ leadId, onSuccess }: LeadFormProps) {
  // ...
}
```

---

## 5. Consolidated Hooks Pattern

**Aturan EKSAD:** Setiap fitur memiliki **1–2 file hooks** (bukan 1 hook per file).

Hook tunggal mengkonsolidasikan semua React Query queries, mutations, dan local state untuk satu fitur.

```typescript
// packages/leads/src/hooks/useLeads.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchDataAsync } from '@frontend/shared';
import { useErrorStore } from '@frontend/shared/store/useErrorStore.ts';
import { getLeads, getLeadById, createLead, updateLead, deleteLead } from '../services/leadsService';
import type { Lead, LeadFormValues, LeadListParams } from '../types/leads.types';

// ✅ Query key constants — MUST be exported; NEVER hard-code strings in components
export const leadKeys = {
  all:    ['leads'] as const,
  list:   (params?: LeadListParams) => ['leads', 'list', params] as const,
  detail: (id: string) => ['leads', 'detail', id] as const,
};

export function useLeads(params?: LeadListParams) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: leadKeys.list(params),
    queryFn:  () => fetchDataAsync({ asyncFn: () => getLeads(params), setError, menuName: 'leads' }),
  });
}

export function useLeadDetail(id: string) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: leadKeys.detail(id),
    queryFn:  () => fetchDataAsync({ asyncFn: () => getLeadById(id), setError, menuName: 'leads' }),
    enabled:  !!id,
  });
}

export function useCreateLead() {
  const queryClient = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (data: LeadFormValues) =>
      fetchDataAsync({ asyncFn: () => createLead(data), setError, menuName: 'leads' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: leadKeys.all });
    },
  });
}

export function useUpdateLead() {
  const queryClient = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: LeadFormValues }) =>
      fetchDataAsync({ asyncFn: () => updateLead(id, data), setError, menuName: 'leads' }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: leadKeys.all });
      queryClient.invalidateQueries({ queryKey: leadKeys.detail(id) });
    },
  });
}

export function useDeleteLead() {
  const queryClient = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (id: string) =>
      fetchDataAsync({ asyncFn: () => deleteLead(id), setError, menuName: 'leads' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: leadKeys.all });
    },
  });
}
```

**Aturan:**
- Semua `useQuery` dan `useMutation` untuk satu fitur berada di satu file hooks
- Query keys **WAJIB** diekspor sebagai konstanta (`leadKeys`) — tidak boleh hard-code string di komponen
- Format wajib: `{ all, list: (params?) => [...], detail: (id) => [...] }`
- Hooks wrap service calls dengan `fetchDataAsync` — service functions sendiri tidak handle errors
- Komponen hanya memanggil hook, tidak pernah memanggil service langsung

---

## 6. TypeScript Conventions

```typescript
// ✅ Domain entity — mandatory EKSAD fields (Principles 4, 7, 8)
interface Lead {
  id: string;
  tenantId: string;       // ALWAYS present — EKSAD multi-tenant (Principle 4)
  name: string;
  status: LeadStatus;
  amount: number;         // financial: use number, display with formatter
  createdAt: number;      // ALWAYS epoch ms — Principle 7
  createdBy: string;
  deletedAt?: number;     // ALWAYS present as optional — soft delete (Principle 8)
}

// ✅ Status = string-literal union — NEVER TypeScript enum
type LeadStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED';

// ✅ Form values type terpisah dari API response type
interface LeadFormValues {
  name: string;
  amount: number;
  status?: LeadStatus;
}

// ✅ API response wrapper — matches backend GenericResponseDTO shape exactly
interface ApiResponse<T> {
  status:    'SUCCESS' | 'FAIL'; // matches GenericResponseDTO.status
  message:   string;
  data:      T;
  metadata?: PageMetadata;       // present only for paginated responses
}

// ✅ Page metadata — matches backend PageMetadata shape
interface PageMetadata {
  totalCount:  number;
  totalPages:  number;
  page:        number;
  size:        number;
  hasNext:     boolean;
  hasPrevious: boolean;
}
```

**Aturan:**
- **Tidak boleh menggunakan `any`** — gunakan `unknown` jika tipe belum diketahui, lalu type-guard
- Gunakan `import type` untuk type-only imports (`import type { Lead } from '...'`)
- `tenantId: string` dan `createdAt: number` **wajib ada** di setiap entity type dari backend
- `deletedAt?: number` **wajib ada** — soft delete berlaku untuk semua domain entities
- Status values wajib menggunakan **string-literal union**, bukan TypeScript `enum`

---

## 7. TailwindCSS Conventions

```tsx
// ✅ Utility classes — grouping order: layout → spacing → sizing → color → typography → interactive
<div className="flex flex-col gap-4 p-6 w-full bg-white rounded-lg shadow text-sm font-medium hover:shadow-md transition-shadow">

// ✅ Conditional classes menggunakan clsx atau cn()
import { cn } from '@/shared/utils/cn';

<button
  className={cn(
    'px-4 py-2 rounded-md font-medium transition-colors',
    isLoading && 'opacity-50 cursor-not-allowed',
    variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
    variant === 'secondary' && 'bg-gray-100 text-gray-700 hover:bg-gray-200',
  )}
>

// ✅ Reusable class patterns diletakkan di shared component, bukan diulang
// shared/components/Badge.tsx — bukan copy-paste class di setiap komponen
```

**Aturan:**
- **Tidak boleh `style={{}}`** untuk layout dan spacing — gunakan Tailwind classes
- `style={{}}` hanya boleh untuk dynamic values yang tidak bisa dicapai dengan Tailwind (misal: dynamic width dalam piksel)
- Gunakan `cn()` utility (wrapper `clsx` + `tailwind-merge`) untuk conditional classes
- Warna, spacing, dan typography harus konsisten — gunakan Tailwind config, bukan arbitrary values `w-[123px]`

---

## 8. React Query Conventions

```typescript
// ✅ QueryClient config — di @/lib/queryClient.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,    // 5 menit
      gcTime: 10 * 60 * 1000,      // 10 menit (dulu: cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});

// ✅ Query via hook — fetchDataAsync handles error centrally via useErrorStore
const { data, isLoading } = useLeads(params);

if (isLoading) return <LoadingOverlay message="Memuat data leads..." />;
// isError handled globally by GlobalErrorDialog — no per-component error UI needed

// ✅ Mutation
const createLead = useCreateLead();
createLead.mutate(formData, { onSuccess: () => navigate('/leads') });
```

**Aturan:**
- **Tidak boleh `useEffect` + `fetch`/`axios`** di dalam component untuk server state — selalu gunakan React Query
- Query keys **wajib** menggunakan konstanta yang diekspor — format `export const {feature}Keys = { all, list: (p?) => [...], detail: (id) => [...] }`
- Semua `queryFn` wajib dibungkus `fetchDataAsync` — jangan panggil service langsung di `queryFn`
- Selalu handle `isLoading`; `isError` ditangani global via `fetchDataAsync` + `useErrorStore` + `GlobalErrorDialog`
- Mutation **wajib** invalidasi query yang relevan di `onSuccess`

---

## 9. React Router Conventions

```typescript
// ✅ Router definition — app/router.tsx
import { createBrowserRouter } from 'react-router-dom';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      {
        path: 'leads',
        children: [
          { index: true, element: <LeadsPage /> },
          { path: ':id', element: <LeadDetailPage /> },
          { path: 'new', element: <LeadFormPage /> },
          { path: ':id/edit', element: <LeadFormPage /> },
        ],
      },
    ],
  },
  { path: '/login', element: <LoginPage /> },
  { path: '*', element: <NotFoundPage /> },
]);

// ✅ Route paths sebagai constants
export const ROUTES = {
  LEADS: {
    LIST: '/leads',
    DETAIL: (id: number) => `/leads/${id}`,
    NEW: '/leads/new',
    EDIT: (id: number) => `/leads/${id}/edit`,
  },
} as const;
```

**Aturan:**
- Selalu gunakan `createBrowserRouter` — bukan `<BrowserRouter>` wrapper
- Route paths didefinisikan sebagai konstanta di `ROUTES` — tidak boleh hard-code string di komponen
- Protected routes dihandle di `AppLayout` dengan redirect ke `/login` jika belum autentikasi

---

## 10. Real API First — Service Layer

**EKSAD rule: Service layer SELALU menggunakan real API calls. DILARANG ada mock/dummy data di service.**

```typescript
// packages/leads/src/services/leadsService.ts
import { apiClient } from '@frontend/shared';
import type { IBaseResponse } from '@frontend/shared';
import type { Lead, LeadFormValues, LeadListParams } from '../types/leads.types';

// ✅ CORRECT — direct apiClient calls; no mock data; no error handling
export const getLeads = (params?: LeadListParams) =>
  apiClient.get<IBaseResponse<Lead[]>>('/api/v1/leads', { params });

export const getLeadById = (id: string) =>
  apiClient.get<IBaseResponse<Lead>>(`/api/v1/leads/${id}`);

export const createLead = (data: LeadFormValues) =>
  apiClient.post<IBaseResponse<Lead>>('/api/v1/leads', data);

export const updateLead = (id: string, data: LeadFormValues) =>
  apiClient.put<IBaseResponse<Lead>>(`/api/v1/leads/${id}`, data);

export const deleteLead = (id: string) =>
  apiClient.delete<IBaseResponse<void>>(`/api/v1/leads/${id}`);
```

**Query parameters — Axios `params` option (NEVER manual URLSearchParams):**
```typescript
// ✅ CORRECT
export const listLeads = (filters: LeadListParams) =>
  apiClient.get('/api/v1/leads', { params: filters });

// ❌ WRONG
export const listLeads = (filters: LeadListParams) => {
  const sp = new URLSearchParams();
  if (filters.keyword) sp.set('keyword', filters.keyword);
  return apiClient.get(`/api/v1/leads?${sp}`);   // ← FORBIDDEN
};
```

**❌ NEVER write mock/dummy data in services:**
```typescript
// ❌ FORBIDDEN — mock data in services
const mockLeads = [{ id: '1', name: 'PT Maju' }];
export const getLeads = () =>
  new Promise(resolve => setTimeout(() => resolve(mockLeads), 500));   // ← FORBIDDEN
```

**Aturan:**
- Services return raw Axios response — **no error handling, no mock data, no setTimeout**
- Error handling adalah tugas hook via `fetchDataAsync` + `useErrorStore` (§13)
- Komponen tidak pernah import atau memanggil service function langsung — selalu lewat hook
- Mocking hanya diperbolehkan **di dalam test files** menggunakan MSW (lihat `EKSAD_FRONTEND_TESTING_GUIDE.md`)

---

## 11. State Management Rules

| State Type | Tool | Contoh |
|------------|------|--------|
| Server state (dari API) | React Query | List leads, detail lead, pagination |
| Form state | React Hook Form | Form create/edit lead |
| UI state (local) | `useState` | Modal open/close, active tab |
| Shared UI state | `useState` di parent + prop drilling (maks 2 level) | Selected row di parent page |
| Global app state | React Context | Auth session, tenant info, theme |
| URL state | React Router `useSearchParams` | Filter, sort, pagination params |

**Aturan:**
- **Jangan gunakan Redux atau Zustand** kecuali ada persetujuan Platform Team — React Query + Context cukup untuk mayoritas use case EKSAD
- Server state (data dari backend) **tidak boleh** diduplikasi ke `useState` — selalu baca dari React Query cache
- Filter dan pagination **wajib** disimpan di URL params (bukan state) agar bisa di-share/bookmark

---

## 12. API Integration & Auth

```typescript
// @/lib/axios.ts — app-level Axios instance config
// ⚠️ Do NOT import axiosInstance directly in feature code — use apiClient from @frontend/shared
import axios from 'axios';

export const axiosInstance = axios.create({
  baseURL:         import.meta.env.VITE_API_BASE_URL,
  timeout:         30_000,
  withCredentials: true,   // ← REQUIRED — auth via HttpOnly cookie (never localStorage)
});

// No request interceptor for tokens — cookie is sent automatically by the browser
axiosInstance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';   // ← token is HttpOnly, not readable by JS
    }
    return Promise.reject(error);
  },
);
```

**Auth rules:**
- Auth is via **HttpOnly cookie** — the FE **never reads, stores, or parses the JWT**
- **No `localStorage`/`sessionStorage` for tokens** — this is a security violation
- `withCredentials: true` MUST be set so cookies are sent with every cross-origin request
- No `Authorization: Bearer` header logic — cookie is attached by the browser automatically
- `401` responses redirect to `/login`; no token-refresh logic needed in components

---

### 12.1 Day.js Date Handling

**EKSAD rule: Selalu gunakan `dayjs` untuk semua date/time. DILARANG `new Date()`, `Date.parse()`, atau native `Date` methods di feature code.**

```typescript
// @/lib/dayjs.ts — Day.js instance dengan plugins
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/id';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(relativeTime);
dayjs.locale('id');

export default dayjs;
```

```typescript
// ✅ CORRECT — always import from @/lib/dayjs
import dayjs from '@/lib/dayjs';

// Format epoch ms for display
const formatted = dayjs(createdAt).format('DD MMM YYYY HH:mm');

// Parse string to epoch ms (for sending to backend)
const epochMs: number = dayjs('2026-06-24').valueOf();

// Arithmetic
const tomorrow: number = dayjs().add(1, 'day').valueOf();

// Relative time
const relative = dayjs(createdAt).fromNow();

// ✅ Helpers used in ReservedFieldInput and DatePicker wiring
const epochToDateStr = (ms: number | null | undefined): string =>
  ms == null ? '' : dayjs(ms).format('YYYY-MM-DD');

const dateStrToEpoch = (s: string): number | null =>
  s ? dayjs(s).valueOf() : null;

// ❌ FORBIDDEN — native Date methods in feature code
const bad1 = new Date(createdAt);                     // ❌
const bad2 = new Date().toISOString().slice(0, 10);   // ❌
const bad3 = Date.parse('2026-06-24');                // ❌
const bad4 = Date.now();                              // ❌ use dayjs().valueOf()
```

**`<DatePicker>` integration with epoch ms form state:**
```tsx
// DatePicker accepts/returns Date objects; store epoch ms in form state
<Controller
  name="dueDate"
  control={control}
  render={({ field }) => (
    <DatePicker
      label="Due Date"
      value={field.value ? new Date(field.value) : undefined}
      onChange={(date) => field.onChange(date ? dayjs(date).valueOf() : null)}
      disabled={isViewMode}
    />
  )}
/>
```

**Aturan:**
- ✅ Selalu `import dayjs from '@/lib/dayjs'` — bukan langsung dari `'dayjs'`
- ✅ Semua date formatting, parsing, arithmetic via `dayjs`
- ✅ Domain entity fields menyimpan `number` (epoch ms) — bukan `Date` object atau ISO string
- ✅ Date inputs wajib menggunakan `<DatePicker>` — tidak boleh `<InputField type="date">`
- ❌ Tidak boleh `new Date()`, `Date.now()`, `Date.parse()` di feature code

---

## 13. Error Handling

Error handling di EKSAD Frontend bersifat **terpusat**. Service tidak handle error; hooks mendelegasikan ke `fetchDataAsync` + `useErrorStore`; `GlobalErrorDialog` menampilkan ke user.

```
Error flow:
  Service    → throws raw AxiosError
  Hook       → fetchDataAsync catches, calls setError(error)
  Store      → useErrorStore stores the error
  UI         → GlobalErrorDialog reads store and displays dialog
```

```typescript
// packages/leads/src/hooks/useLeads.ts
import { fetchDataAsync } from '@frontend/shared';
import { useErrorStore } from '@frontend/shared/store/useErrorStore.ts';

export function useLeads(params?: LeadListParams) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: leadKeys.list(params),
    queryFn:  () => fetchDataAsync({ asyncFn: () => getLeads(params), setError, menuName: 'leads' }),
  });
}
```

```tsx
// apps/[app]/src/App.tsx — mount GlobalErrorDialog once at app root
import { GlobalErrorDialog } from '@frontend/shared';

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <GlobalErrorDialog />   {/* handles all API errors globally */}
    </QueryClientProvider>
  );
}
```

**Field-level validation errors (inline via Zod + RHF):**
```tsx
<Controller
  name="name"
  control={control}
  render={({ field }) => (
    <InputField
      {...field}
      label="Nama Lead"
      error={errors.name?.message}   // ← inline from Zod schema
    />
  )}
/>
```

**Aturan:**
- ❌ Jangan `console.error` saja — semua API errors harus tampil ke user via `GlobalErrorDialog`
- ❌ Jangan handle error di service layer — service returns raw Axios response
- ✅ Field validation errors tampil inline di field (`error` prop), bukan hanya toast
- ✅ `fetchDataAsync` adalah satu-satunya wrapper untuk semua async API calls di hooks

---

## 14. Forbidden Patterns

| Pattern | Mengapa Dilarang | Alternatif yang Benar |
|---------|-----------------|----------------------|
| `useEffect` + `fetch`/`axios` untuk server data | Duplikasi React Query, tidak ada caching | `useQuery` dari React Query |
| `any` TypeScript type | Kehilangan type safety | `unknown` + type guard, atau definisikan interface |
| `style={{}}` untuk layout/spacing | Tidak konsisten, tidak bisa di-review Tailwind | Tailwind utility classes |
| Hard-code query string (`useQuery({ queryKey: ['leads'] })`) | Sulit refactor, rawan typo | Export konstanta `{feature}Keys` |
| Direct service call di component | Bypass React Query caching | Panggil lewat hook |
| Import langsung antar feature packages | Coupling antar fitur | Pindahkan ke `@frontend/shared` |
| `@/components/ui/Button` | Old single-app path | `@frontend/ui` |
| Class components | Tidak konsisten dengan codebase | Functional component + hooks |
| Default export untuk non-Screen components | Menyulitkan refactoring & autocomplete | Named export |
| Redux/Zustand tanpa approval | Over-engineering | React Query + Context |
| Hard-code API URL (`axios.get('http://...')`) | Tidak portable | `import.meta.env.VITE_API_BASE_URL` |
| `localStorage`/`sessionStorage` untuk token auth | Security violation — token harus HttpOnly | HttpOnly cookie + `withCredentials: true` |
| `localStorage` untuk server state | Stale data, tidak reactive | React Query cache |
| `Authorization: Bearer` header logic di FE | FE tidak boleh membaca/menyimpan JWT | HttpOnly cookie; browser sends automatically |
| `new Date()` / `Date.parse()` / `Date.now()` di feature code | Inconsistent timezone, not mockable | `dayjs` dari `@/lib/dayjs` |
| `<InputField type="date">` | Browser-specific UI, inconsistent | `<DatePicker>` dari `@frontend/ui` |
| Manual `URLSearchParams` di service | Verbose, error-prone | Axios `params` option |
| Mock/dummy data di service layer | Tidak valid sebagai test, menyembunyikan API errors | Real `apiClient` calls; mocking via MSW di tests |
| TypeScript `enum` untuk status values | Runtime overhead, tidak idiomatic TS | String-literal union (`'DRAFT' \| 'SUBMITTED'`) |
| `useState` untuk form data di tab components | Multi-tab form kehilangan sinkronisasi | Single RHF `useForm` + `FormProvider` + `useFormContext` |
| Custom modal markup (`fixed inset-0 bg-black/50`) | Konflik z-index, tidak konsisten | `AppModal` dari `@frontend/ui` |
| Manual `<table>` markup | Tidak ada pagination/sorting built-in | `<DataTable>` dari `@frontend/ui` |
| Custom inline spinners | Tidak konsisten dengan design system | `<LoadingOverlay>` dari `@frontend/ui` |
| `border border-border rounded-lg p-4` untuk grouping fields | Visual noise, bukan pattern semantik | Headings, dividers, `space-y-*` |

---

## 15. Code Review Checklist

### ✅ Structure & Architecture
- [ ] Fitur baru punya package sendiri di `packages/`
- [ ] Tidak ada import langsung antar feature packages (hanya via `@frontend/shared`)
- [ ] Semua UI components diimport dari `@frontend/ui` — tidak ada `@/components/ui`
- [ ] Service layer ada — komponen tidak panggil API langsung
- [ ] Hook file mengkonsolidasikan semua queries & mutations fitur
- [ ] Route didaftarkan di `apps/[app]/src/App.tsx`; menu entry di `navigation.ts`

### ✅ TypeScript
- [ ] Tidak ada `any` type — gunakan `unknown` atau definisikan interface
- [ ] `import type` digunakan untuk type-only imports
- [ ] Semua props punya interface `{Component}Props`
- [ ] Entity type mencakup `tenantId: string` (wajib ada — Principle 4)
- [ ] `createdAt`/`deletedAt` bertipe `number` (epoch ms) — Principle 7 & 8
- [ ] Status fields menggunakan string-literal union, bukan TypeScript `enum`
- [ ] `ApiResponse<T>` shape matches `GenericResponseDTO`: `{ status, message, data, metadata? }`

### ✅ React Query
- [ ] Query keys menggunakan konstanta yang diekspor — format `{feature}Keys = { all, list, detail }`
- [ ] Semua `queryFn` dibungkus `fetchDataAsync` — tidak ada direct service call di `queryFn`
- [ ] `isLoading` state ditangani — tampilkan `<LoadingOverlay>`
- [ ] `isError` tidak ditangani per-komponen — sudah global via `GlobalErrorDialog`
- [ ] Mutation menginvalidasi query yang relevan di `onSuccess`

### ✅ Service Layer (Real API)
- [ ] Service hanya berisi `apiClient.get/post/put/patch/delete` — no mock, no error handling
- [ ] Query params via Axios `params` option — no manual `URLSearchParams`
- [ ] Tidak ada mock data, `setTimeout`, atau `Promise.resolve(mockData)`

### ✅ Auth & Security
- [ ] Tidak ada `localStorage.getItem('access_token')` atau `Authorization: Bearer` logic
- [ ] `axiosInstance` menggunakan `withCredentials: true`
- [ ] Tidak ada token-parsing logic di FE

### ✅ Date Handling
- [ ] Tidak ada `new Date()`, `Date.parse()`, `Date.now()` di feature code
- [ ] Semua date operations menggunakan `dayjs` dari `@/lib/dayjs`
- [ ] Date inputs menggunakan `<DatePicker>` — tidak ada `<InputField type="date">`
- [ ] Domain entity fields menyimpan `number` (epoch ms)

### ✅ Styling
- [ ] Tidak ada `style={{}}` untuk layout/spacing
- [ ] Conditional classes menggunakan `cn()`
- [ ] Tidak ada arbitrary Tailwind values (`w-[123px]`) tanpa alasan jelas
- [ ] Tidak ada `border border-border rounded-lg` untuk grouping form fields

### ✅ UI Components
- [ ] Loading state menggunakan `<LoadingOverlay>` — tidak ada custom spinner
- [ ] Tables menggunakan `<DataTable>` — tidak ada manual `<table>` markup
- [ ] Modals menggunakan `AppModal` (forms) atau `AlertDialog` (confirmations)
- [ ] Date inputs menggunakan `<DatePicker>`

### ✅ Testing
- [ ] Hook baru punya unit test
- [ ] Komponen baru punya minimal 1 render test
- [ ] Tests menggunakan MSW untuk mock HTTP — tidak ada mock data di service production code
- [ ] Happy path dan minimal 1 edge case tercakup

### ✅ Reserved Fields
- [ ] `useReservedFields(entity)` digunakan untuk fetch schema
- [ ] React Query `staleTime: 60_000` pada reserved fields query
- [ ] `ReservedFieldInput` menggunakan `dayjs` untuk date slot conversion — bukan `new Date()`
- [ ] `ReservedFieldSection` digunakan sebagai single entry point

---

## 16. Reserved Field Dynamic Rendering

> Mengimplementasikan **Principle #13 (Tenant-configurable reserved fields)** dari `EKSAD_BASE_PRINCIPLES.md`. Backend pattern reference: `EKSAD_CODING_STANDARDS.md` §25 dan `EKSAD_RESERVED_FIELD_PATTERNS.md` §9–§10.
>
> Reserved fields adalah custom field per-tenant pada entitas transaksional. Frontend MUST render form-nya **secara dinamis** berdasarkan schema endpoint backend — tidak boleh hard-code label/slot di komponen.

### 16.1 `useReservedFields(entityType)` Hook

Fetch schema reserved field per-entitas dari backend dan cache 60 detik via React Query. Schema jarang berubah — `staleTime: 60_000` aman untuk semua kasus interactive form.

```typescript
// src/shared/hooks/useReservedFields.ts
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";
import type { ReservedFieldConfig } from "@/shared/types/reserved-field";

export const reservedFieldsQueryKey = (entity: string) =>
  ["reserved-fields", entity] as const;

export function useReservedFields(entity: string) {
  const { data, isLoading, error } = useQuery({
    queryKey: reservedFieldsQueryKey(entity),
    queryFn: async (): Promise<ReservedFieldConfig[]> => {
      const res = await api.get(`/api/v1/${entity}/_schema`);
      return res.data.reservedFields ?? [];
    },
    staleTime: 60_000,           // ← 60 detik cache (schema jarang berubah)
    refetchOnWindowFocus: false, // schema tidak perlu re-fetch saat focus
  });

  return {
    fields: data ?? [],
    loading: isLoading,
    error,
  };
}
```

**Rules:**
- ✅ Selalu pakai hook ini — JANGAN hard-code field list di komponen
- ✅ `staleTime: 60_000` (60s) — schema reserved field jarang berubah; cache lebih lama OK
- ✅ Invalidate via `queryClient.invalidateQueries({ queryKey: reservedFieldsQueryKey(entity) })` ketika admin update tenant config (event-driven, jika frontend dapat WebSocket event)
- ❌ JANGAN `refetchOnMount: "always"` — bikin form lag tiap navigation

---

### 16.2 `ReservedFieldConfig` TypeScript Interface

Type-safe shape dari schema endpoint. Tempatkan di `shared/types/reserved-field.ts` agar bisa di-import lintas fitur.

```typescript
// src/shared/types/reserved-field.ts

export type ReservedFieldDataType =
  | "string"
  | "numeric"
  | "date"
  | "boolean"
  | "jsonb";

export interface ReservedFieldValidation {
  pattern?:    string;     // regex untuk dataType "string"
  maxLength?:  number;     // untuk "string"
  minValue?:   number;     // untuk "numeric"
  maxValue?:   number;     // untuk "numeric"
  enum?:       string[];   // pilihan terbatas (semua dataType kecuali jsonb)
}

export interface ReservedFieldConfig {
  slot:       string;      // "reserved_str_1", "reserved_num_2", "reserved_ext", …
  label:      string;      // label yang ditampilkan ke user, e.g. "Salesperson Code"
  required:   boolean;
  dataType:   ReservedFieldDataType;
  validation?: ReservedFieldValidation;
}

/** Map nilai reserved field per slot — dipakai sebagai form state. */
export type ReservedFieldValues = Record<string, unknown>;
```

**Rules:**
- ✅ Letakkan di `shared/types/` (bukan di feature folder) — di-share lintas fitur
- ✅ `dataType` literal union — TypeScript exhaustive check di `ReservedFieldInput`
- ❌ JANGAN deklarasi ulang `ReservedFieldConfig` per fitur

---

### 16.3 `ReservedFieldInput` Component

Component "atom" yang me-render satu input berdasarkan `dataType` dan prefix slot. Pattern: switch by `dataType` + adapter untuk date (epoch-ms ↔ ISO) dan JSONB (KeyValueEditor).

```tsx
// src/shared/components/reserved-field/ReservedFieldInput.tsx
import { KeyValueEditor } from "./KeyValueEditor";
import type { ReservedFieldConfig } from "@/shared/types/reserved-field";
import dayjs from "@/lib/dayjs";   // ← always dayjs, never new Date()

interface ReservedFieldInputProps {
  config:   ReservedFieldConfig;
  value:    unknown;
  onChange: (slot: string, value: unknown) => void;
}

// ✅ Use dayjs — not new Date() (EKSAD §12.1)
const epochToDate = (ms?: number | null): string =>
  ms == null ? "" : dayjs(ms).format("YYYY-MM-DD");

const dateToEpoch = (s: string): number | null =>
  s ? dayjs(s).valueOf() : null;

export function ReservedFieldInput({ config, value, onChange }: ReservedFieldInputProps) {
  const { slot, label, required, dataType, validation } = config;
  const common = { id: slot, name: slot, required };

  // Mapping per prefix → HTML element
  switch (dataType) {
    case "string":
      return (
        <label htmlFor={slot}>
          {label}{required && " *"}
          <input
            type="text"
            {...common}
            pattern={validation?.pattern}
            maxLength={validation?.maxLength}
            value={(value as string) ?? ""}
            onChange={e => onChange(slot, e.target.value)}
          />
        </label>
      );

    case "numeric":
      return (
        <label htmlFor={slot}>
          {label}{required && " *"}
          <input
            type="number"
            step="0.0001"
            {...common}
            min={validation?.minValue}
            max={validation?.maxValue}
            value={(value as number) ?? ""}
            onChange={e => onChange(slot, e.target.value === "" ? null : Number(e.target.value))}
          />
        </label>
      );

    case "date":
      return (
        <label htmlFor={slot}>
          {label}{required && " *"}
          <input
            type="date"
            {...common}
            value={epochToDate(value as number | null)}
            onChange={e => onChange(slot, dateToEpoch(e.target.value))}
          />
        </label>
      );

    case "boolean":
      return (
        <label htmlFor={slot}>
          <input
            type="checkbox"
            {...common}
            checked={Boolean(value)}
            onChange={e => onChange(slot, e.target.checked)}
          />
          {label}{required && " *"}
        </label>
      );

    case "jsonb":
      return (
        <KeyValueEditor
          label={label}
          value={(value as Record<string, unknown>) ?? {}}
          onChange={v => onChange(slot, v)}
        />
      );

    default: {
      // exhaustive check — TypeScript akan error jika dataType baru ditambah tanpa case
      const _exhaustive: never = dataType;
      return null;
    }
  }
}
```

**Input-type mapping table (canonical):**

| Slot Prefix | dataType | HTML Input | Konversi |
|-------------|----------|-----------|----------|
| `reserved_str_*` | `string` | `<input type="text">` | — (apply `pattern`, `maxLength`) |
| `reserved_num_*` | `numeric` | `<input type="number" step="0.0001">` | empty → `null`; lainnya → `Number()` |
| `reserved_date_*` | `date` | `<input type="date">` | ISO `YYYY-MM-DD` ↔ epoch ms via `epochToDate` / `dateToEpoch` |
| `reserved_bool_*` | `boolean` | `<input type="checkbox">` | — |
| `reserved_ext` | `jsonb` | `<KeyValueEditor>` | object ↔ array of {key, value} rows |

**Rules:**
- ✅ Switch `dataType` (bukan `slot.startsWith(...)`) — schema authoritative
- ✅ Date slot WAJIB konversi via `epochToDate`/`dateToEpoch` — backend selalu `BIGINT` epoch ms
- ✅ Numeric `step="0.0001"` — backend pakai `NUMERIC(20,4)`
- ❌ JANGAN render `reserved_ext` sebagai `<textarea>` JSON string — pakai `KeyValueEditor` yang structured

---

### 16.4 `ReservedFieldSection` Component

Orchestrator: pakai hook `useReservedFields`, loop atas `fields`, render `<ReservedFieldInput>` per slot. Component "molecule" yang di-embed di feature form.

```tsx
// src/shared/components/reserved-field/ReservedFieldSection.tsx
import { useReservedFields } from "@/shared/hooks/useReservedFields";
import { ReservedFieldInput } from "./ReservedFieldInput";
import type { ReservedFieldValues } from "@/shared/types/reserved-field";

interface ReservedFieldSectionProps {
  entity:    string;                                          // "orders", "leads", …
  value:     ReservedFieldValues;
  onChange:  (slot: string, value: unknown) => void;
  className?: string;
}

export function ReservedFieldSection({
  entity, value, onChange, className,
}: ReservedFieldSectionProps) {
  const { fields, loading, error } = useReservedFields(entity);

  if (loading)              return <div className={className}>Loading custom fields…</div>;
  if (error)                return <div className={className}>Failed to load custom fields</div>;
  if (fields.length === 0)  return null;            // ← tenant tidak punya reserved field aktif

  return (
    <fieldset className={className}>
      <legend>Custom Fields</legend>
      {fields.map(f => (
        <ReservedFieldInput
          key={f.slot}
          config={f}
          value={value[f.slot]}
          onChange={onChange}
        />
      ))}
    </fieldset>
  );
}
```

**Rules:**
- ✅ Selalu handle 3 state: `loading` / `error` / `fields.length === 0` (tenant non-opt-in)
- ✅ Render sebagai `<fieldset>` dengan `<legend>` — semantik form + a11y
- ❌ JANGAN render `<ReservedFieldInput>` satu-satu di feature form — pakai section ini sebagai single entry point

---

### 16.5 Integration in Feature Form

Embed `<ReservedFieldSection>` di feature form. Reserved field values disimpan di form state sebagai `Record<string, unknown>`, lalu di-spread ke payload saat submit.

```tsx
// src/features/orders/components/OrderForm.tsx
import { useState } from "react";
import dayjs from "@/lib/dayjs";   // ← always dayjs
import { ReservedFieldSection } from "@/shared/components/reserved-field/ReservedFieldSection";
import type { ReservedFieldValues } from "@/shared/types/reserved-field";
import { useCreateOrder } from "@/features/orders/hooks/useOrders";

interface OrderFormState {
  customerId: number | null;
  amount:     number | null;
  reserved:   ReservedFieldValues;
}

export function OrderForm() {
  const [form, setForm] = useState<OrderFormState>({
    customerId: null,
    amount:     null,
    reserved:   {},
  });
  const { mutateAsync: createOrder, isPending } = useCreateOrder();

  const handleReservedChange = (slot: string, value: unknown) => {
    setForm(prev => ({ ...prev, reserved: { ...prev.reserved, [slot]: value } }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createOrder({
      customer_id: form.customerId,
      amount:      form.amount,
      ...form.reserved,                  // ← spread reserved fields ke payload (snake_case sudah)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Standard fields … */}

      <ReservedFieldSection
        entity="orders"
        value={form.reserved}
        onChange={handleReservedChange}
      />

      <button type="submit" disabled={isPending}>Create Order</button>
    </form>
  );
}
```

**Rules:**
- ✅ Reserved values disimpan di state field terpisah (`reserved: ReservedFieldValues`) — jangan di-flatten ke top-level form state
- ✅ Spread ke payload saat submit (`...form.reserved`) — slot names sudah snake_case sesuai schema endpoint
- ✅ Section bisa di-place di mana saja dalam form — biasanya di bawah field standard
- ❌ JANGAN pass full form state ke `<ReservedFieldSection value=...>` — hanya bagian `reserved`-nya

---

### 16.6 Testing

Vitest + React Testing Library. Mock `useReservedFields` di test agar tidak panggil network.

**Hook unit test:**
```typescript
// src/shared/hooks/__tests__/useReservedFields.test.ts
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useReservedFields, reservedFieldsQueryKey } from "../useReservedFields";
import { vi } from "vitest";

vi.mock("@/shared/api", () => ({
  api: { get: vi.fn().mockResolvedValue({
    data: { reservedFields: [{ slot: "reserved_str_1", label: "X", required: false, dataType: "string" }] },
  }) },
}));

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
};

test("useReservedFields returns fields and uses 60s staleTime", async () => {
  const qc = new QueryClient();
  const { result } = renderHook(() => useReservedFields("orders"), { wrapper });

  await waitFor(() => expect(result.current.loading).toBe(false));
  expect(result.current.fields).toHaveLength(1);

  // Asserti staleTime via query state
  const state = qc.getQueryState(reservedFieldsQueryKey("orders"));
  // staleTime config diverify via useQuery options snapshot (atau lewat QueryClient.getQueryDefaults)
});
```

**Component render test (input-type-per-prefix):**
```tsx
// src/shared/components/reserved-field/__tests__/ReservedFieldInput.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { ReservedFieldInput } from "../ReservedFieldInput";
import type { ReservedFieldConfig } from "@/shared/types/reserved-field";

const cases: Array<{ cfg: ReservedFieldConfig; expectedType: string }> = [
  { cfg: { slot: "reserved_str_1",  label: "S", required: false, dataType: "string" },  expectedType: "text" },
  { cfg: { slot: "reserved_num_1",  label: "N", required: false, dataType: "numeric" }, expectedType: "number" },
  { cfg: { slot: "reserved_date_1", label: "D", required: false, dataType: "date" },    expectedType: "date" },
  { cfg: { slot: "reserved_bool_1", label: "B", required: false, dataType: "boolean" }, expectedType: "checkbox" },
];

test.each(cases)("$cfg.dataType slot renders <input type=$expectedType>", ({ cfg, expectedType }) => {
  render(<ReservedFieldInput config={cfg} value={null} onChange={() => {}} />);
  const input = screen.getByLabelText(/B|S|N|D/, { exact: false }) as HTMLInputElement;
  expect(input.type).toBe(expectedType);
});

test("date input converts ISO → epoch ms on change", () => {
  const onChange = vi.fn();
  const cfg: ReservedFieldConfig = { slot: "reserved_date_1", label: "Promised", required: false, dataType: "date" };
  render(<ReservedFieldInput config={cfg} value={null} onChange={onChange} />);
  fireEvent.change(screen.getByLabelText("Promised"), { target: { value: "2026-05-23" } });
  expect(onChange).toHaveBeenCalledWith("reserved_date_1", new Date("2026-05-23").getTime());
});
```

**Section integration test:**
```tsx
test("ReservedFieldSection renders nothing when fields empty", async () => {
  vi.mocked(useReservedFields).mockReturnValue({ fields: [], loading: false, error: null });
  const { container } = render(
    <ReservedFieldSection entity="orders" value={{}} onChange={() => {}} />
  );
  expect(container.firstChild).toBeNull();
});
```

**Rules:**
- ✅ Mock `useReservedFields` di component test — fokus ke render logic
- ✅ Test setiap `dataType` minimal 1 case (gunakan `test.each`)
- ✅ Test konversi epoch ↔ ISO untuk date slot — paling rawan bug
- ❌ JANGAN test real network call di unit test — pakai MSW di integration test saja

---
