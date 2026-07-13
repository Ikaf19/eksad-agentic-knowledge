# Technical Specification Document (TSD) — Frontend
# {PROJECT_NAME} — Web Application
# Versi {VERSION}

**Versi Dokumen:** {VERSION}
**Tanggal:** {DATE}
**Dibuat oleh:** {PREPARED_BY}
**Sistem:** `{ARTIFACT_ID}` — Web Application (`{APP_NAME}`)
**Organisasi:** PT EKSAD / {BUSINESS_UNIT}
**Klasifikasi:** Internal — Confidential
**Status:** 🔴 Draft / 🟡 In Review / 🟢 Approved *(pilih salah satu)*

> **Dokumen Terkait:**
> - `BRD_{PROJECT_CODE}_v{VERSION}.md` — Persyaratan bisnis
> - `FSD_{PROJECT_CODE}_v{VERSION}.md` — Spesifikasi fungsional
> - `TSD_{PROJECT_CODE}_v{VERSION}.md` — Technical spec backend

---

## Daftar Isi

1. [Overview Arsitektur Frontend](#1-overview-arsitektur-frontend)
2. [Tech Stack & Versi](#2-tech-stack--versi)
3. [Struktur Project](#3-struktur-project)
4. [Konfigurasi Vite & Environment](#4-konfigurasi-vite--environment)
5. [Routing Design](#5-routing-design)
6. [Katalog Feature Modules](#6-katalog-feature-modules)
7. [Katalog Komponen](#7-katalog-komponen)
8. [React Query Key Conventions](#8-react-query-key-conventions)
9. [API Consumption Contract](#9-api-consumption-contract)
10. [Mock Data Layer](#10-mock-data-layer)
11. [Authentication & Authorization (Frontend)](#11-authentication--authorization-frontend)
12. [State Management Design](#12-state-management-design)
13. [Error Handling Strategy](#13-error-handling-strategy)
14. [Strategi Testing](#14-strategi-testing)

---

## 1. Overview Arsitektur Frontend

> *Jelaskan posisi web app ini dalam platform EKSAD secara keseluruhan: siapa yang menggunakannya, backend service mana yang dikonsumsi, dan bagaimana flow autentikasi bekerja.*

**{PROJECT_NAME} Web Application** adalah antarmuka berbasis browser untuk {SHORT_DESCRIPTION}. Aplikasi ini dikonsumsi oleh {USER_GROUP} dan berkomunikasi dengan backend service `{SERVICE_NAME}`.

### Diagram Interaksi

```
Browser (React App)
    │
    ├── Auth: JWT dari {AUTH_SERVICE} via /auth/login
    │         Token disimpan di localStorage / httpOnly cookie
    │
    ├── API: {SERVICE_NAME} → {BASE_URL}/api/{domain}
    │
    └── Static Assets: Vite build → {CDN / Nginx / Static Host}
```

**Keputusan arsitektur utama:**
- Arsitektur: Modular feature-based (satu folder per domain fitur)
- Server state: React Query (bukan Redux/Zustand)
- Routing: React Router v6 dengan `createBrowserRouter`
- Backend saat ini: Mock data layer → akan diganti dengan API calls nyata saat backend siap

---

## 2. Tech Stack & Versi

| Technology | Versi | Peran |
|------------|-------|-------|
| React | 18.x | UI framework |
| TypeScript | 5.x (strict) | Type safety |
| Vite | 5.x | Build tool & dev server |
| TailwindCSS | 3.x | Utility-first styling |
| React Query (`@tanstack/react-query`) | 5.x | Server state management |
| React Router | 6.x | Client-side routing |
| Axios | 1.x | HTTP client (wrapped) |
| Jest | 29.x | Test framework |
| React Testing Library | 14.x | Component & hook testing |

---

## 3. Struktur Project

```
src/
├── app/
│   ├── App.tsx
│   ├── router.tsx                  # Definisi semua routes
│   └── providers.tsx               # QueryClientProvider, AuthProvider
├── features/
│   ├── {feature-1}/
│   │   ├── components/
│   │   ├── hooks/
│   │   │   └── use{Feature}.ts     # Consolidated hook
│   │   ├── services/
│   │   │   ├── {feature}Service.ts # Service layer (mock atau API)
│   │   │   └── {feature}.mock.ts   # Mock data
│   │   ├── types/
│   │   │   └── {feature}.types.ts
│   │   ├── utils/
│   │   └── pages/
│   └── {feature-2}/
│       └── ...
├── shared/
│   ├── components/                 # Button, Modal, Table, Badge, dll.
│   ├── hooks/                      # useAuth, usePagination, dll.
│   ├── types/                      # ApiResponse, PaginatedResponse, dll.
│   ├── utils/                      # formatCurrency, getErrorMessage, dll.
│   └── constants/
├── lib/
│   ├── queryClient.ts
│   └── axios.ts
└── main.tsx
```

---

## 4. Konfigurasi Vite & Environment

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

| Variable | Development | Production | Keterangan |
|----------|-------------|------------|-----------|
| `VITE_API_BASE_URL` | `http://localhost:{BACKEND_PORT}` | `https://{PROD_DOMAIN}/api` | Base URL backend |
| `VITE_APP_NAME` | `{APP_NAME} (Dev)` | `{APP_NAME}` | Nama app untuk display |
| `VITE_AUTH_TOKEN_KEY` | `access_token` | `access_token` | Key untuk localStorage |

> **Aturan:** Semua environment variable WAJIB diawali `VITE_` agar ter-expose ke browser. Jangan menyimpan secret di frontend.

---

## 5. Routing Design

### Route Structure

```typescript
// app/router.tsx
export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,       // Protected layout dengan auth check
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

| Path | Komponen | Deskripsi | Auth Required | Roles |
|------|----------|-----------|--------------|-------|
| `/` | `DashboardPage` | Halaman utama / dashboard | ✅ | {ROLES} |
| `/{feature}` | `{Feature}ListPage` | List {feature} | ✅ | {ROLES} |
| `/{feature}/new` | `{Feature}FormPage` | Form tambah {feature} | ✅ | {ROLES} |
| `/{feature}/:id` | `{Feature}DetailPage` | Detail {feature} | ✅ | {ROLES} |
| `/{feature}/:id/edit` | `{Feature}FormPage` | Form edit {feature} | ✅ | {ROLES} |
| `/login` | `LoginPage` | Halaman login | ❌ | Public |

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

## 6. Katalog Feature Modules

Daftar semua feature modules yang ada di aplikasi ini:

| Feature Module | Folder | Deskripsi | Fitur FSD | Status |
|---------------|--------|-----------|----------|--------|
| {Feature 1} | `features/{feature-1}/` | {Deskripsi singkat} | FR-{MODULE}-{N} | 🔴 Draft / 🟡 Dev / 🟢 Done |
| {Feature 2} | `features/{feature-2}/` | {Deskripsi singkat} | FR-{MODULE}-{N} | 🔴 Draft / 🟡 Dev / 🟢 Done |
| Shared | `shared/` | Komponen dan utilities lintas fitur | — | 🟢 Done |

### Detail per Feature Module

#### Feature: {Feature 1}

```
features/{feature-1}/
├── components/
│   ├── {Feature1}List.tsx
│   ├── {Feature1}Form.tsx
│   ├── {Feature1}Detail.tsx
│   └── {Feature1}StatusBadge.tsx
├── hooks/
│   └── use{Feature1}.ts          # useQuery + useMutation dikonsolidasikan
├── services/
│   ├── {feature1}Service.ts
│   └── {feature1}.mock.ts
├── types/
│   └── {feature1}.types.ts
└── pages/
    ├── {Feature1}ListPage.tsx
    ├── {Feature1}DetailPage.tsx
    └── {Feature1}FormPage.tsx
```

**Hooks yang diekspor dari `use{Feature1}.ts`:**

| Hook | Tipe | Query Key | Keterangan |
|------|------|-----------|-----------|
| `use{Feature1}List(params?)` | Query | `['{feature1}', 'list', params]` | Ambil semua data dengan pagination |
| `use{Feature1}Detail(id)` | Query | `['{feature1}', 'detail', id]` | Ambil detail by ID |
| `useCreate{Feature1}()` | Mutation | — | Buat data baru |
| `useUpdate{Feature1}()` | Mutation | — | Update data |
| `useDelete{Feature1}()` | Mutation | — | Soft delete data |

---

## 7. Katalog Komponen

### Shared Components

| Komponen | Path | Props Utama | Keterangan |
|----------|------|-------------|-----------|
| `Button` | `shared/components/Button.tsx` | `variant`, `isLoading`, `onClick` | Primary, secondary, danger variants |
| `Modal` | `shared/components/Modal.tsx` | `isOpen`, `onClose`, `title` | Konfirmasi, form, info |
| `Table` | `shared/components/Table.tsx` | `columns`, `data`, `isLoading` | Sortable, dengan pagination |
| `Badge` | `shared/components/Badge.tsx` | `variant`, `label` | Status badges |
| `LoadingSpinner` | `shared/components/LoadingSpinner.tsx` | `size` | Loading state |
| `ErrorMessage` | `shared/components/ErrorMessage.tsx` | `error`, `onRetry` | Error display |
| `EmptyState` | `shared/components/EmptyState.tsx` | `message`, `action` | Empty data state |
| `Pagination` | `shared/components/Pagination.tsx` | `page`, `totalPages`, `onPageChange` | Pagination control |

### Feature Components — {Feature 1}

| Komponen | Props | Keterangan |
|----------|-------|-----------|
| `{Feature1}List` | `onEdit`, `onDelete` | List view dengan aksi |
| `{Feature1}Form` | `{feature1}Id?`, `onSuccess` | Create/Edit form |
| `{Feature1}Detail` | `{feature1}Id` | Detail view read-only |
| `{Feature1}StatusBadge` | `status` | Color-coded status badge |

---

## 8. React Query Key Conventions

Semua query keys didefinisikan sebagai konstanta dan diekspor dari file hooks:

```typescript
// Konvensi penamaan query key
export const {feature}Keys = {
  all: ['{feature}'] as const,
  list: (params?: {Feature}ListParams) => ['{feature}', 'list', params] as const,
  detail: (id: number) => ['{feature}', 'detail', id] as const,
};
```

**Daftar query keys per fitur:**

| Feature | Key Constant | Struktur Key |
|---------|-------------|--------------|
| {Feature 1} | `{feature1}Keys` | `['{feature1}', 'list', params]` / `['{feature1}', 'detail', id]` |
| {Feature 2} | `{feature2}Keys` | `['{feature2}', 'list', params]` / `['{feature2}', 'detail', id]` |

---

## 9. API Consumption Contract

> **Catatan:** Tabel ini menggambarkan API backend yang akan dikonsumsi frontend saat integrasi.
> Selama mock data layer aktif, kolom ini berfungsi sebagai kontrak desain.
> Lihat TSD backend (`TSD_{PROJECT_CODE}_v{VERSION}.md`) untuk spesifikasi lengkap endpoint.

### {Feature 1} — API Endpoints

| Method | Path | Request Body / Params | Response | Hook yang Memanggil | Status Integrasi |
|--------|------|-----------------------|----------|---------------------|-----------------|
| `GET` | `/api/{feature1}` | `?page=&size=&status=` | `PaginatedResponse<{Feature1}>` | `use{Feature1}List()` | 🔴 Mock |
| `GET` | `/api/{feature1}/:id` | — | `ApiResponse<{Feature1}>` | `use{Feature1}Detail(id)` | 🔴 Mock |
| `POST` | `/api/{feature1}` | `{Feature1}FormValues` | `ApiResponse<{Feature1}>` | `useCreate{Feature1}()` | 🔴 Mock |
| `PUT` | `/api/{feature1}/:id` | `{Feature1}FormValues` | `ApiResponse<{Feature1}>` | `useUpdate{Feature1}()` | 🔴 Mock |
| `DELETE` | `/api/{feature1}/:id` | — | `ApiResponse<void>` | `useDelete{Feature1}()` | 🔴 Mock |

**Status Integrasi Legend:**
- 🔴 Mock — menggunakan mock data layer
- 🟡 In Progress — sedang diintegrasikan
- 🟢 Integrated — sudah terhubung ke backend

### TypeScript Types untuk API

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
  tenantId: string;           // EKSAD multi-tenant — selalu ada
  {FIELD_1}: {TYPE_1};
  {FIELD_2}: {TYPE_2};
  status: {Feature1}Status;
  createdAt: number;          // epoch milliseconds
  createdBy: string;
  updatedAt?: number;
  updatedBy?: string;
  deletedAt?: number;         // soft delete
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

## 10. Mock Data Layer

Selama backend belum siap, semua service menggunakan mock data layer:

```typescript
// Contoh: features/{feature1}/services/{feature1}.mock.ts
import type { {Feature1} } from '../types/{feature1}.types';

export const mock{Feature1}s: {Feature1}[] = [
  {
    id: 1,
    tenantId: 'tenant-001',
    {FIELD_1}: {SAMPLE_VALUE_1},
    status: 'DRAFT',
    createdAt: 1700000000000,
    createdBy: 'user-001',
  },
  // tambah sample data sesuai kebutuhan demo
];
```

**Semua fungsi dalam service file yang masih menggunakan mock harus ditandai:**
```typescript
// TODO: [BACKEND INTEGRATION] {HTTP_METHOD} {ENDPOINT_PATH}
```

---

## 11. Authentication & Authorization (Frontend)

### Flow Autentikasi

```
1. User akses app → AppLayout cek token di localStorage
2. Token tidak ada / expired → redirect ke /login
3. User login → POST /auth/login → terima JWT
4. JWT disimpan di localStorage dengan key: VITE_AUTH_TOKEN_KEY
5. Axios interceptor menyertakan token di setiap request: Authorization: Bearer {token}
6. Backend return 401 → interceptor clear token + redirect /login
```

### JWT Claims yang Digunakan Frontend

| Claim | Tipe | Penggunaan |
|-------|------|-----------|
| `eksad_tenant_id` | string | Ditampilkan di header, dikirim jika perlu |
| `eksad_user_id` | string | Untuk "dibuat oleh", profil user |
| `eksad_role` | string | Untuk conditional rendering (show/hide fitur per role) |
| `exp` | number | Cek expiry sebelum request |

### Role-Based Rendering

```typescript
// shared/hooks/useAuth.ts
export function useAuth() {
  const token = localStorage.getItem(import.meta.env.VITE_AUTH_TOKEN_KEY);
  const payload = token ? parseJwt(token) : null;
  return {
    isAuthenticated: !!payload && payload.exp * 1000 > Date.now(),
    tenantId: payload?.eksad_tenant_id,
    userId: payload?.eksad_user_id,
    role: payload?.eksad_role,
  };
}

// Penggunaan di komponen
const { role } = useAuth();
{role === 'MANAGER' && <button>Approve</button>}
```

---

## 12. State Management Design

| State | Tool | Lokasi | Keterangan |
|-------|------|--------|-----------|
| Server data (lists, detail) | React Query | Otomatis di QueryClient cache | Stale time 5 menit |
| Form state | React Hook Form | Lokal di form component | |
| Auth session | Context (`AuthContext`) | `app/providers.tsx` | JWT payload |
| Modal open/close | `useState` | Komponen parent | |
| Pagination & filter | `useSearchParams` | URL query params | Bisa di-bookmark |
| Theme / locale | Context (`AppContext`) | `app/providers.tsx` | Jika ada multi-bahasa |

---

## 13. Error Handling Strategy

| Skenario | Penanganan | Komponen |
|---------|-----------|---------|
| Query gagal (network error) | Tampilkan `<ErrorMessage>` di tempat komponen | `isError` dari `useQuery` |
| Mutation gagal | Toast error dengan pesan dari server | `onError` callback di `mutate()` |
| Form validation error | Error inline di bawah field | React Hook Form `errors` |
| 401 Unauthorized | Redirect ke `/login`, clear token | Axios response interceptor |
| 403 Forbidden | Toast "Tidak punya izin akses" | Axios response interceptor |
| 404 Not Found | Tampilkan `<NotFoundPage>` | Router catch-all |
| Uncaught error | React ErrorBoundary di `AppLayout` | Error boundary |

---

## 14. Strategi Testing

### Coverage Targets

| Layer | Target | Tool |
|-------|--------|------|
| Hooks (queries & mutations) | ≥ 90% | Jest + `renderHook` |
| Utility functions | ≥ 95% | Jest |
| Komponen (interaksi user) | ≥ 80% | React Testing Library |
| Pages (smoke test) | ≥ 60% | React Testing Library |

### Test Strategy per Feature

Untuk setiap feature module, wajib ada:

1. **Hook test** — test semua queries (happy path, error, loading) dan mutations (success, error)
2. **Form component test** — test submit valid, validasi field kosong, error dari service, loading state
3. **List component test** — test render data, empty state, loading state, error state

### Menjalankan Test

```bash
# Semua test
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

Lihat `_base/EKSAD_FRONTEND_TESTING_GUIDE.md` untuk pola lengkap dan contoh kode.
