---
name: eksad-fe-impl
description: "Use when the user asks the Frontend Developer profile to implement a React feature, scaffold a new package in the EKSAD monorepo, write a consolidated hook, design a service layer, or fix a FE pattern violation. Triggers on phrases like 'create a feature package', 'implement useLeads hook', 'add a new screen', 'review my React component', 'fix this FE pattern'. Enforces EKSAD FE v1.2 (2026-06-24): monorepo packages layout, consolidated hooks, real API in services (no mocks), HttpOnly cookie auth, dayjs for dates, MSW in tests."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, frontend, react, typescript, vite, tailwind, react-query, monorepo, dayjs]
    related_skills: [multi-role-agent-setup]
---

# EKSAD Frontend Implementation Skill

React/TypeScript feature implementation workflow for EKSAD FE standards v1.2 (2026-06-24). Produces feature package scaffolds, consolidated hooks, service layers, components, and tests.

## When to Use

- User asks to create a new feature package in the monorepo
- User asks to implement a hook (`use{Feature}`)
- User asks to add a new screen or component
- User asks to fix a FE pattern violation
- User asks to set up reserved field rendering
- User asks to write a unit test for a hook or component

## When NOT to Use

- Backend implementation → switch to `developer-backend` profile
- Architecture / FE-TSD → switch to `system-analyst` profile + `eksad-tsd-design` skill
- Business requirements → switch to `business-analyst` profile
- FE code review → switch to `technical-leader` profile + `eksad-code-review` skill

## Knowledge References

Primary (v1.2 — current standard):
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_CODING_STANDARDS.md` — MUST comply
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_PATTERNS.md` — form modes, multi-tab, inline editing
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md` — `@frontend/ui` components
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_TESTING_GUIDE.md` — v1.1, MSW for HTTP mocking

For API contracts:
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_RESERVED_FIELD_PATTERNS.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CORE_AUTH_PATTERNS.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md`

## Stack (Default — v1.2)

React 18 + TypeScript 5 (strict) + Vite 5 + TailwindCSS 3 + React Query 5 + React Router 6 + Axios 1 + Day.js 1 + RHF 7 + Zod 3 + Jest/Vitest + RTL 14 + MSW 2.

## Monorepo Layout (per Feature)

```
packages/
└── [feature]/
    └── src/
        ├── [Feature]Screen.tsx       # routable entry
        ├── components/
        │   ├── {Feature}List.tsx
        │   ├── {Feature}Form.tsx     # mode = 'create' | 'edit' | 'view'
        │   ├── {Feature}Detail.tsx
        │   └── tabs/                 # multi-tab form tabs
        ├── hooks/
        │   └── use{Feature}.ts       # ONE file, all queries + mutations
        ├── services/
        │   └── {feature}Service.ts   # real apiClient — no mocks
        ├── types/
        │   └── {feature}.types.ts    # types + status unions + ApiResponse<T>
        └── schemas/
            └── {feature}Schemas.ts   # Zod validation
```

**Import paths:**
- `@frontend/ui` for shared components (Button, AppModal, AlertDialog, DataTable, DatePicker, InputField, SelectField, LoadingOverlay)
- `@frontend/shared` for `apiClient`, `fetchDataAsync`, `useErrorStore`, `GlobalErrorDialog`, `IBaseResponse`
- `@/lib/queryClient`, `@/lib/dayjs` for app config
- ❌ NEVER `@/components/ui/...` (old single-app path)

## Implementation Order (5 Steps)

### 1. Types (`types/{feature}.types.ts`)

```typescript
export interface {Feature} {
  id: string;
  tenantId: string;          // ALWAYS — Principle 4
  name: string;
  status: {Feature}Status;
  amount: number;
  createdAt: number;         // ALWAYS epoch ms — Principle 7
  createdBy: string;
  deletedAt?: number;        // soft delete
}
export type {Feature}Status = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED';

export interface {Feature}FormValues {
  name: string;
  amount: number;
  status?: {Feature}Status;
}

export interface ApiResponse<T> {
  status: 'SUCCESS' | 'FAIL';
  message: string;
  data: T;
  metadata?: PageMetadata;
}
```

### 2. Service Layer (`services/{feature}Service.ts`)

**Real API only. NO mocks.**

```typescript
import { apiClient } from '@frontend/shared';
import type { IBaseResponse } from '@frontend/shared';
import type { {Feature}, {Feature}FormValues, {Feature}ListParams } from '../types/{feature}.types';

export const get{Feature}s = (params?: {Feature}ListParams) =>
  apiClient.get<IBaseResponse<{Feature}[]>>('/api/v1/{feature}', { params });

export const get{Feature}ById = (id: string) =>
  apiClient.get<IBaseResponse<{Feature}>>(`/api/v1/{feature}/${id}`);

export const create{Feature} = (data: {Feature}FormValues) =>
  apiClient.post<IBaseResponse<{Feature}>>('/api/v1/{feature}', data);

export const update{Feature} = (id: string, data: {Feature}FormValues) =>
  apiClient.put<IBaseResponse<{Feature}>>(`/api/v1/{feature}/${id}`, data);

export const delete{Feature} = (id: string) =>
  apiClient.delete<IBaseResponse<void>>(`/api/v1/{feature}/${id}`);
```

### 3. Hooks (`hooks/use{Feature}.ts`)

**One file per feature. All queries + mutations + keys.**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchDataAsync } from '@frontend/shared';
import { useErrorStore } from '@frontend/shared/store/useErrorStore';
import {
  get{Feature}s, get{Feature}ById, create{Feature}, update{Feature}, delete{Feature}
} from '../services/{feature}Service';
import type { {Feature}, {Feature}FormValues, {Feature}ListParams } from '../types/{feature}.types';

// ✅ Exported query keys — NEVER hard-code strings in components
export const {feature}Keys = {
  all:    ['{feature}'] as const,
  list:   (params?: {Feature}ListParams) => ['{feature}', 'list', params] as const,
  detail: (id: string) => ['{feature}', 'detail', id] as const,
};

export function use{Feature}s(params?: {Feature}ListParams) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: {feature}Keys.list(params),
    queryFn: () => fetchDataAsync({ asyncFn: () => get{Feature}s(params), setError, menuName: '{feature}' }),
  });
}

export function use{Feature}Detail(id: string) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: {feature}Keys.detail(id),
    queryFn: () => fetchDataAsync({ asyncFn: () => get{Feature}ById(id), setError, menuName: '{feature}' }),
    enabled: !!id,
  });
}

export function useCreate{Feature}() {
  const qc = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (data: {Feature}FormValues) =>
      fetchDataAsync({ asyncFn: () => create{Feature}(data), setError, menuName: '{feature}' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: {feature}Keys.all }),
  });
}

export function useUpdate{Feature}() {
  const qc = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: {Feature}FormValues }) =>
      fetchDataAsync({ asyncFn: () => update{Feature}(id, data), setError, menuName: '{feature}' }),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: {feature}Keys.all });
      qc.invalidateQueries({ queryKey: {feature}Keys.detail(id) });
    },
  });
}

export function useDelete{Feature}() {
  const qc = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (id: string) =>
      fetchDataAsync({ asyncFn: () => delete{Feature}(id), setError, menuName: '{feature}' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: {feature}Keys.all }),
  });
}
```

### 4. Components (`components/`)

Always handle 3 states:
```tsx
const { data, isLoading, isError, error } = use{Feature}s(params);
if (isLoading) return <LoadingOverlay message="Memuat data..." />;
// isError handled globally via GlobalErrorDialog
if (!data?.length) return <EmptyState message="No data yet" />;
```

Form modes (ONE component, three modes):
```tsx
interface {Feature}FormModalProps {
  mode?: 'create' | 'edit' | 'view';
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialData?: {Feature};
  onSubmit?: (data: {Feature}FormValues) => Promise<void>;
}
```

Use `<AppModal>` for forms, `<AlertDialog>` for confirmations, `<DataTable>` for tables, `<DatePicker>` for date inputs.

#### Interaction, accessibility, and runtime-state controls

Apply WCAG 2.2 requirements applicable to the approved UI and design system; do not claim conformance from component choice alone.

- **Keyboard/focus:** all interactive behavior is keyboard operable; use semantic controls, visible focus, logical order, no keyboard traps, focus restoration after modal/route actions, and intentional focus on validation or asynchronous failure.
- **Forms:** associate labels/instructions/errors programmatically, preserve entered values after failure, identify required fields without color alone, summarize and focus invalid submissions, and announce status changes through the approved accessible pattern.
- **Runtime states:** define and test initial loading, background refresh, mutation pending, recoverable/error, permission-denied, empty-first-use, empty-filtered, and success states as applicable. Prevent duplicate mutation and expose a safe retry; never replace a real API integration with service-layer mock data.
- **Rendering security:** render untrusted API/user content as text by default. Do not inject raw HTML or URLs; if an approved requirement needs rich content, use the repository-approved sanitizer/allowlist and safe link handling. Never expose secrets or sensitive error payloads in UI/logs.
- **Performance evidence:** use repository-approved budgets and real measurements (for example profiler, bundle, or browser evidence) before claiming improvement. Record scenario, build/device/network context, before/after result, and evidence location; do not invent thresholds or optimize from intuition alone.

Tests cover keyboard operation, focus behavior, accessible form errors, relevant runtime states, and safe rendering. Real-API-first remains mandatory: MSW is confined to tests.

### 5. Tests (MSW-based)

**Hook test:**
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { use{Feature}s } from './use{Feature}';

const server = setupServer(
  http.get('/api/v1/{feature}', () => HttpResponse.json({
    status: 'SUCCESS', message: '', data: [/* mock */],
  }))
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('fetches {feature}s', async () => {
  const { result } = renderHook(() => use{Feature}s(), { wrapper: QueryClientWrapper });
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
});
```

**Component test:**
```typescript
it('shows loading then data', async () => {
  render(<{Feature}List />);
  expect(screen.getByText(/memuat/i)).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText('Test Lead')).toBeInTheDocument());
});
```

## Date Handling (Day.js Only)

```typescript
import dayjs from '@/lib/dayjs';

// ✅ Epoch to display string
dayjs(createdAt).format('DD MMM YYYY HH:mm');

// ✅ String to epoch ms (for sending to backend)
const epochMs: number = dayjs('2026-06-24').valueOf();

// ❌ NEVER new Date(), Date.now(), Date.parse() in feature code
```

## Reserved Field Rendering

```typescript
import { useReservedFields } from '@/shared/hooks/useReservedFields';

const { fields, loading } = useReservedFields('{entity}');
// 60s staleTime — schema rarely changes

// In form, render dynamic fields based on schema:
// <ReservedFieldSection fields={fields} control={methods.control} />
// <ReservedFieldInput slot="string_1" type="string" />
```

## Commit Pattern

```bash
cd /workspace/projects/<project>
git add packages/{feature}/src/...
git commit -m "feat(<scope>): <change>"
git push
```

## Forbidden Patterns

❌ `useEffect` + `fetch`/`axios` for server data (use React Query)
❌ `any` TypeScript type (use `unknown` + type guard)
❌ `style={{}}` for layout/spacing (use Tailwind)
❌ Hard-coded query strings (use exported `{feature}Keys`)
❌ Direct service call in component (call via hook)
❌ Import langsung antar feature packages (use `@frontend/shared`)
❌ `@/components/ui/Button` (use `@frontend/ui`)
❌ Class components
❌ Redux/Zustand without approval
❌ `localStorage` for auth tokens (security violation — use HttpOnly cookie)
❌ `new Date()` in feature code (use dayjs)
❌ `<InputField type="date">` (use `<DatePicker>`)
❌ Manual `URLSearchParams` (use Axios `params`)
❌ Mock data in service layer (use MSW in tests)
❌ Inaccessible keyboard/focus/form behavior or color-only errors
❌ Raw untrusted HTML/URL rendering without an approved sanitizer/allowlist
❌ Performance claims without reproducible measurement evidence
❌ TypeScript `enum` for status (use string-literal union)
❌ Custom modal markup (use `AppModal` or `AlertDialog`)
❌ Manual `<table>` markup (use `<DataTable>`)

## Phase F Enrichment — Frontend/UI Evidence Patterns

Adapted benchmark patterns: frontend-patterns, React best practices, web-design-guidelines.

- Validate React/TS changes against FE-TSD, API contract, accessibility states, error/empty/loading states, and existing component library usage.
- Use `visual_input`/Figma/browser evidence only as input; UI/UX owns design intent and QA owns test verdicts.
- Avoid mock-only implementations when the approved contract exists; use real apiClient integration boundaries.
- Include performance/accessibility risks in handoff notes when they affect UX or QA acceptance.
