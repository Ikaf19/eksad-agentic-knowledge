# EKSAD Frontend Testing Guide
# React + TypeScript — Unit, Component & Integration Testing Patterns

**File:** `_base/EKSAD_FRONTEND_TESTING_GUIDE.md`
**Version:** 1.1
**Date:** 2026-06-24
**Owner:** EKSAD Platform Team
**Audience:** Frontend Developer, QA Engineer, Technical Leader
**Upload-to:** GPT knowledge base — Dev FE GPT, QA GPT (frontend), TL GPT

> File ini diupload sebagai **GPT knowledge file** untuk Dev FE GPT, QA GPT (frontend), dan TL GPT.

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-06-24 | EKSAD docs maintainer | §1 philosophy: service-layer mocking is forbidden; §8 renamed "Mocking in Tests (MSW)" — MSW replaces `jest.mock` on service module for all tests; §11 coverage: services row updated (no mock layer — test via MSW) |
| 1.0 | 2026-04-23 | EKSAD Platform Team | Initial version |

---

## Table of Contents

1. [Testing Philosophy](#1-testing-philosophy)
2. [Test Layer Overview](#2-test-layer-overview)
3. [Setup & Configuration](#3-setup--configuration)
4. [Unit Tests — Hooks (React Query)](#4-unit-tests--hooks-react-query)
5. [Unit Tests — Utility Functions](#5-unit-tests--utility-functions)
6. [Component Tests — Render & Interaction](#6-component-tests--render--interaction)
7. [Component Tests — Form Validation](#7-component-tests--form-validation)
8. [Mocking in Tests (MSW)](#8-mocking-in-tests-msw)
9. [Testing Loading & Error States](#9-testing-loading--error-states)
10. [Test Naming Convention](#10-test-naming-convention)
11. [Coverage Targets](#11-coverage-targets)
12. [QA: Deriving Test Cases from FSD](#12-qa-deriving-test-cases-from-fsd)
13. [QA: Test Plan Template](#13-qa-test-plan-template)

---

## 1. Testing Philosophy

**Filosofi EKSAD Frontend Testing:**

> *"Test behavior, not implementation. Uji apa yang user lihat dan lakukan — bukan bagaimana kode diorganisir."*

Prioritas testing (dari tertinggi ke terendah):
1. **Hook tests** — semua queries dan mutations via `renderHook` + MSW server
2. **Component interaction tests** — user click, form submit, navigation
3. **Component render tests** — tampilan berdasarkan state (loading, error, data)
4. **Utility function tests** — pure functions, formatters, validators
5. *(Opsional)* **Integration tests** — full page flow dengan MSW

**Mocking rules:**
- ✅ **MSW (`setupServer`)** — canonical method for mocking HTTP in all tests (hooks, components, integration)
- ✅ **`jest.mock` on service module** — allowed only when isolating a specific hook unit test and MSW setup is not warranted (e.g. testing invalidation logic only)
- ❌ **Mock/dummy data in service files** — **FORBIDDEN**. Services always call real `apiClient`. Never write `setTimeout(() => resolve(mockData))` or mock arrays in `services/*.ts` — that is a production code violation, not a test strategy
- ❌ **`jest.mock` to stub the service with fake data** — prefer MSW; if `jest.mock` is used, mock the module function, not by embedding dummy data inside the service file itself

**Yang TIDAK perlu di-test:**
- Implementation detail internal (nama state variable, fungsi private)
- Tailwind class names
- Library third-party (React Query, React Router sudah punya test sendiri)

---

## 2. Test Layer Overview

| Layer | Tool | Scope | Speed |
|-------|------|-------|-------|
| Unit — Hooks | Jest + `renderHook` + MSW | React Query hooks, invalidation logic | ⚡ Fast |
| Unit — Utils | Jest | Pure functions, formatters, validators | ⚡ Fast |
| Component | Jest + React Testing Library + MSW | Render, user interaction, form submit | ⚡ Fast |
| Integration (opsional) | Jest + RTL + MSW | Full page flow dengan mock HTTP | 🐢 Slower |

---

## 3. Setup & Configuration

### jest.config.ts

```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterFramework: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',    // path alias
    '\\.(css|less|scss)$': 'identity-obj-proxy',
  },
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/features/**/*.{ts,tsx}',
    'src/shared/**/*.{ts,tsx}',
    '!src/**/*.types.ts',
    '!src/**/*.mock.ts',
    '!src/**/index.ts',
  ],
};

export default config;
```

### src/test/setup.ts

```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest'; // atau jest

afterEach(() => {
  cleanup();
});
```

### Test Wrapper — QueryClient untuk testing

```typescript
// src/test/testUtils.tsx
import { ReactNode } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

interface TestWrapperProps {
  children: ReactNode;
}

export function TestWrapper({ children }: TestWrapperProps) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Custom render dengan wrapper
export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) {
  return render(ui, { wrapper: TestWrapper, ...options });
}
```

---

## 4. Unit Tests — Hooks (React Query)

### Pattern Dasar

```typescript
// packages/leads/src/hooks/__tests__/useLeads.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { TestWrapper } from '@/test/testUtils';
import { useLeads, useCreateLead } from '../useLeads';

// ✅ MSW server — mock at the HTTP layer, not the service module
const server = setupServer(
  http.get('/api/v1/leads', () =>
    HttpResponse.json({
      status: 'SUCCESS',
      message: 'Process succeeded',
      data: [
        { id: '1', name: 'PT Maju', status: 'DRAFT', tenantId: 'tenant-1', createdAt: 1700000000000 },
        { id: '2', name: 'CV Jaya', status: 'SUBMITTED', tenantId: 'tenant-1', createdAt: 1700000001000 },
      ],
    }),
  ),
);

beforeAll(()  => server.listen());
afterEach(()  => server.resetHandlers());
afterAll(()   => server.close());

describe('useLeads', () => {
  // ✅ Happy path
  it('harus mengembalikan list leads ketika query berhasil', async () => {
    const { result } = renderHook(() => useLeads(), { wrapper: TestWrapper });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data?.data).toHaveLength(2);
    expect(result.current.data?.data[0].name).toBe('PT Maju');
  });

  // ✅ Error state — override handler for this test
  it('harus masuk error state ketika API mengembalikan 500', async () => {
    server.use(
      http.get('/api/v1/leads', () => HttpResponse.error()),
    );

    const { result } = renderHook(() => useLeads(), { wrapper: TestWrapper });

    await waitFor(() => expect(result.current.isError).toBe(true));
  });

  // ✅ Loading state
  it('harus menampilkan loading state saat query berjalan', () => {
    server.use(
      http.get('/api/v1/leads', async () => {
        await new Promise(() => {}); // never resolves
        return HttpResponse.json({});
      }),
    );

    const { result } = renderHook(() => useLeads(), { wrapper: TestWrapper });

    expect(result.current.isLoading).toBe(true);
  });
});
```

### Mutation Hook Test

```typescript
describe('useCreateLead', () => {
  it('harus memanggil POST /api/v1/leads dengan data yang benar', async () => {
    const newLead = { id: '99', name: 'PT Baru', status: 'DRAFT', tenantId: 'tenant-1', createdAt: Date.now() };

    server.use(
      http.post('/api/v1/leads', async ({ request }) => {
        const body = await request.json() as Record<string, unknown>;
        expect(body.name).toBe('PT Baru');
        return HttpResponse.json({ status: 'SUCCESS', message: 'Process succeeded', data: newLead });
      }),
    );

    const { result } = renderHook(() => useCreateLead(), { wrapper: TestWrapper });

    result.current.mutate({ name: 'PT Baru', amount: 5_000_000 });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data?.data).toEqual(newLead);
  });

  it('harus masuk error state jika API create gagal', async () => {
    server.use(
      http.post('/api/v1/leads', () => HttpResponse.json({ status: 'FAIL', message: 'Validation failed' }, { status: 422 })),
    );

    const { result } = renderHook(() => useCreateLead(), { wrapper: TestWrapper });

    result.current.mutate({ name: '', amount: 0 });

    await waitFor(() => expect(result.current.isError).toBe(true));
  });
});
```

---

## 5. Unit Tests — Utility Functions

```typescript
// features/leads/utils/__tests__/leads.utils.test.ts
import { formatLeadStatus, formatCurrency } from '../leads.utils';

describe('formatLeadStatus', () => {
  it.each([
    ['DRAFT', 'Draft'],
    ['SUBMITTED', 'Diajukan'],
    ['APPROVED', 'Disetujui'],
    ['REJECTED', 'Ditolak'],
  ])('harus format status %s menjadi %s', (input, expected) => {
    expect(formatLeadStatus(input)).toBe(expected);
  });

  it('harus mengembalikan status asli jika tidak dikenali', () => {
    expect(formatLeadStatus('UNKNOWN')).toBe('UNKNOWN');
  });
});

describe('formatCurrency', () => {
  it('harus format angka menjadi format Rupiah', () => {
    expect(formatCurrency(5000000)).toBe('Rp 5.000.000');
  });

  it('harus handle nilai 0', () => {
    expect(formatCurrency(0)).toBe('Rp 0');
  });

  it('harus handle nilai negatif', () => {
    expect(formatCurrency(-1000)).toBe('-Rp 1.000');
  });
});
```

---

## 6. Component Tests — Render & Interaction

### Render Test

```typescript
// features/leads/components/__tests__/LeadStatusBadge.test.tsx
import { render, screen } from '@testing-library/react';
import { LeadStatusBadge } from '../LeadStatusBadge';

describe('LeadStatusBadge', () => {
  it('harus render badge DRAFT dengan warna abu-abu', () => {
    render(<LeadStatusBadge status="DRAFT" />);
    const badge = screen.getByText('Draft');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-gray-100');
  });

  it('harus render badge APPROVED dengan warna hijau', () => {
    render(<LeadStatusBadge status="APPROVED" />);
    const badge = screen.getByText('Disetujui');
    expect(badge).toHaveClass('bg-green-100');
  });

  it('harus render badge REJECTED dengan warna merah', () => {
    render(<LeadStatusBadge status="REJECTED" />);
    expect(screen.getByText('Ditolak')).toHaveClass('bg-red-100');
  });
});
```

### Interaction Test — Button Click

```typescript
// packages/leads/src/components/__tests__/LeadList.test.tsx
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { renderWithProviders } from '@/test/testUtils';
import { LeadList } from '../LeadList';

const mockLeads = [
  { id: '1', name: 'PT Maju', status: 'DRAFT', tenantId: 'tenant-1', createdAt: 1700000000000 },
];

// ✅ MSW server — mock at HTTP layer
const server = setupServer(
  http.get('/api/v1/leads', () =>
    HttpResponse.json({ status: 'SUCCESS', message: 'Process succeeded', data: mockLeads }),
  ),
);

beforeAll(()  => server.listen());
afterEach(()  => server.resetHandlers());
afterAll(()   => server.close());

describe('LeadList', () => {
  it('harus menampilkan list leads setelah data loaded', async () => {
    renderWithProviders(<LeadList />);

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('PT Maju')).toBeInTheDocument();
    });
  });

  it('harus memanggil onEdit ketika tombol Edit diklik', async () => {
    const user = userEvent.setup();
    const handleEdit = jest.fn();

    renderWithProviders(<LeadList onEdit={handleEdit} />);

    await waitFor(() => screen.getByText('PT Maju'));

    await user.click(screen.getByRole('button', { name: /edit/i }));

    expect(handleEdit).toHaveBeenCalledWith('1');
  });
});
```

---

## 7. Component Tests — Form Validation

```typescript
// packages/leads/src/components/__tests__/LeadForm.test.tsx
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { renderWithProviders } from '@/test/testUtils';
import { LeadForm } from '../LeadForm';

const server = setupServer();
beforeAll(()  => server.listen());
afterEach(()  => server.resetHandlers());
afterAll(()   => server.close());

describe('LeadForm — Create', () => {
  const user = userEvent.setup();

  // ✅ Happy path — form submit berhasil
  it('harus submit form dan memanggil onSuccess ketika data valid', async () => {
    server.use(
      http.post('/api/v1/leads', () =>
        HttpResponse.json({ status: 'SUCCESS', message: 'Process succeeded',
          data: { id: '1', name: 'PT Baru', status: 'DRAFT', tenantId: 'tenant-1', createdAt: Date.now() } }),
      ),
    );
    const onSuccess = jest.fn();

    renderWithProviders(<LeadForm onSuccess={onSuccess} />);

    await user.type(screen.getByLabelText('Nama Lead'), 'PT Baru');
    await user.type(screen.getByLabelText('Nilai'), '5000000');
    await user.click(screen.getByRole('button', { name: /simpan/i }));

    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalledTimes(1);
    });
  });

  // ✅ Edge case — validasi field kosong (Zod client-side, no HTTP call)
  it('harus menampilkan error validasi ketika nama kosong', async () => {
    renderWithProviders(<LeadForm onSuccess={jest.fn()} />);

    await user.click(screen.getByRole('button', { name: /simpan/i }));

    expect(await screen.findByText('Nama lead wajib diisi')).toBeInTheDocument();
  });

  // ✅ Edge case — API error
  it('harus menampilkan error ketika API gagal', async () => {
    server.use(
      http.post('/api/v1/leads', () =>
        HttpResponse.json({ status: 'FAIL', message: 'Server error' }, { status: 500 }),
      ),
    );

    renderWithProviders(<LeadForm onSuccess={jest.fn()} />);

    await user.type(screen.getByLabelText('Nama Lead'), 'PT Gagal');
    await user.click(screen.getByRole('button', { name: /simpan/i }));

    // GlobalErrorDialog handles API errors — check dialog appears
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });
  });

  // ✅ Edge case — loading state saat submit
  it('harus disable tombol Simpan saat submission sedang berjalan', async () => {
    server.use(
      http.post('/api/v1/leads', async () => {
        await new Promise(() => {}); // never resolves
        return HttpResponse.json({});
      }),
    );

    renderWithProviders(<LeadForm onSuccess={jest.fn()} />);

    await user.type(screen.getByLabelText('Nama Lead'), 'PT Loading');
    await user.click(screen.getByRole('button', { name: /simpan/i }));

    expect(screen.getByRole('button', { name: /menyimpan/i })).toBeDisabled();
  });
});
```

---

## 8. Mocking in Tests (MSW)

**EKSAD rule:** Services ALWAYS call real `apiClient`. There is no mock data layer in production service files. All mocking happens **inside tests** at the HTTP level via MSW.

### Canonical pattern — MSW `setupServer`

```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  // Default handlers — happy path responses
  http.get('/api/v1/leads', () =>
    HttpResponse.json({
      status:   'SUCCESS',
      message:  'Process succeeded',
      data:     mockLeads,
      metadata: { totalCount: 2, totalPages: 1, page: 0, size: 10, hasNext: false, hasPrevious: false },
    }),
  ),
  http.post('/api/v1/leads', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>;
    return HttpResponse.json({ status: 'SUCCESS', message: 'Process succeeded', data: { id: '99', ...body } });
  }),
);

beforeAll(()  => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(()  => server.resetHandlers());   // ← reset per-test overrides
afterAll(()   => server.close());

// Override for specific test
it('harus handle API error', async () => {
  server.use(
    http.get('/api/v1/leads', () => HttpResponse.error()),
  );
  // ... test
});
```

### When `jest.mock` on service is acceptable

`jest.mock` on a service module is acceptable **only** when:
- Testing a hook in complete isolation (e.g. verifying `queryClient.invalidateQueries` call count)
- The test does not need to assert HTTP request/response details

```typescript
// ✅ Acceptable — isolating hook invalidation logic
jest.mock('../services/leadsService', () => ({
  createLead: jest.fn().mockResolvedValue({ status: 'SUCCESS', data: mockLead }),
}));
```

**❌ FORBIDDEN in all cases:**
```typescript
// ❌ FORBIDDEN — mock data inside the service FILE (production code)
// leadsService.ts:
export const getLeads = () =>
  new Promise(resolve => setTimeout(() => resolve(mockLeads), 500));   // ← never
```

### MSW setup file

```typescript
// src/test/mswSetup.ts
import { setupServer } from 'msw/node';

// Re-export a shared server instance for shared default handlers
export const mswServer = setupServer();
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { mswServer } from './mswSetup';
import { afterEach, beforeAll, afterAll } from 'vitest';

beforeAll(()  => mswServer.listen({ onUnhandledRequest: 'warn' }));
afterEach(()  => { cleanup(); mswServer.resetHandlers(); });
afterAll(()   => mswServer.close());
```

**Strategi:**
- ✅ Default: MSW `setupServer` per test file (or shared via `mswSetup.ts`)
- ✅ Override single endpoint per test via `server.use(http.get(...))`
- ✅ `jest.mock` only for isolating hook/service module internals (not for embedding fake data)
- ❌ Never write mock data in `services/*.ts` — that is production code violation, not a test strategy

---

## 9. Testing Loading & Error States

```typescript
it('harus menampilkan loading spinner saat data belum tersedia', () => {
  server.use(
    http.get('/api/v1/leads', async () => {
      await new Promise(() => {}); // never resolves
      return HttpResponse.json({});
    }),
  );
  renderWithProviders(<LeadList />);
  expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
});

it('harus menampilkan pesan error saat query gagal', async () => {
  server.use(
    http.get('/api/v1/leads', () => HttpResponse.error()),
  );
  renderWithProviders(<LeadList />);
  await waitFor(() => {
    // GlobalErrorDialog shown via useErrorStore
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
});

it('harus menampilkan empty state ketika data kosong', async () => {
  server.use(
    http.get('/api/v1/leads', () =>
      HttpResponse.json({ status: 'SUCCESS', message: 'Process succeeded', data: [] }),
    ),
  );
  renderWithProviders(<LeadList />);
  await waitFor(() => {
    expect(screen.getByText('Belum ada data leads')).toBeInTheDocument();
  });
});
```

---

## 10. Test Naming Convention

Format: `[unit] harus [expected behavior] ketika [condition]`

```
✅ 'harus mengembalikan list leads ketika query berhasil'
✅ 'harus menampilkan error toast ketika service gagal'
✅ 'harus disable tombol Simpan saat submission sedang berjalan'
✅ 'harus format status APPROVED menjadi Disetujui'

❌ 'test leads'
❌ 'works correctly'
❌ 'leadsService getAll'
```

**Struktur `describe`:**
```typescript
describe('{ComponentName | hookName | functionName}', () => {
  describe('{scenario/kondisi khusus}', () => { // opsional, jika perlu nested
    it('harus [behavior] ketika [condition]', () => { ... });
  });
});
```

---

## 11. Coverage Targets

| Layer | Target | Keterangan |
|-------|--------|-----------|
| Hooks | ≥ 90% | Semua queries, mutations, dan edge cases — tested via MSW |
| Components (interaction) | ≥ 80% | Focus pada interaksi user dan conditional rendering |
| Utility functions | ≥ 95% | Pure functions harus hampir 100% |
| Pages / Screens | ≥ 60% | Smoke test — pastikan render tanpa crash |
| Services | ≥ 80% | Tested via MSW integration tests — no mock data in service files |

**Menjalankan coverage:**
```bash
npx jest --coverage
# atau
npm run test:coverage
```

---

## 12. QA: Deriving Test Cases from FSD

Saat menulis test cases untuk fitur baru, ikuti langkah berikut berdasarkan FSD:

### Step 1 — Identifikasi User Stories

Untuk setiap US di FSD, buat minimal:
- 1 happy path test
- 1 validation/edge case test
- 1 error state test (service fail)

### Step 2 — Identifikasi Business Rules (BR)

Setiap `BR-{N}` di FSD harus punya test yang membuktikannya:

```typescript
// FSD: BR-3 — Lead tidak bisa disubmit jika nilai < Rp 1.000.000
it('harus menampilkan error ketika nilai lead di bawah minimum [BR-3]', async () => {
  renderWithProviders(<LeadForm onSuccess={jest.fn()} />);
  await user.type(screen.getByLabelText('Nilai'), '500000');
  await user.click(screen.getByRole('button', { name: /simpan/i }));
  expect(await screen.findByText('Nilai minimum adalah Rp 1.000.000')).toBeInTheDocument();
});
```

### Step 3 — Identifikasi State Transitions

Untuk fitur dengan approval workflow, test setiap transisi status:
```
DRAFT → SUBMITTED: test tombol Submit
SUBMITTED → APPROVED: test tombol Approve (role check)
SUBMITTED → REJECTED: test tombol Reject (+ alasan wajib)
```

---

## 13. QA: Test Plan Template

```markdown
## Test Plan — {Feature Name}

**Feature:** {nama fitur}
**FSD Reference:** FR-{MODULE}-{N} s.d. FR-{MODULE}-{M}
**Prepared by:** {nama QA}
**Date:** {tanggal}

### Test Cases

| ID | Deskripsi | Precondition | Steps | Expected Result | Type |
|----|-----------|-------------|-------|-----------------|------|
| TC-{F}-001 | [Happy path utama] | Data tersedia | 1. ... 2. ... | Berhasil, data tampil | Happy Path |
| TC-{F}-002 | [Validasi field wajib] | Form kosong | Submit tanpa isi | Error "wajib diisi" | Edge Case |
| TC-{F}-003 | [Service error] | Service mock return error | Submit form valid | Toast error tampil | Error State |
| TC-{F}-004 | [Empty state] | Data kosong | Load halaman | "Belum ada data" tampil | Edge Case |
| TC-{F}-005 | [Loading state] | Service lambat | Load halaman | Spinner tampil | Edge Case |

### Coverage Matrix

| User Story | Happy Path | Validation | Error State | Status |
|------------|-----------|------------|-------------|--------|
| US-{F}-001 | TC-{F}-001 | TC-{F}-002 | TC-{F}-003 | ✅ Covered |
```
