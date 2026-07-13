# EKSAD Frontend Patterns

**File:** `_base/EKSAD_FRONTEND_PATTERNS.md`
**Version:** 1.0
**Date:** 2026-06-24
**Owner:** EKSAD Platform Team
**Status:** 🟢 Active
**Audience:** Frontend Developer, Tech Lead, Code Reviewer
**Upload-to:** GPT knowledge base — Dev FE GPT, TL GPT

> Canonical implementation patterns for EKSAD frontend features.
> Source of truth: `need-to-update/patterns.md` + `need-to-update/fundamentals.md`.

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-24 | EKSAD docs maintainer | Initial version — form modes, multi-tab forms, read-only display, isSaved inline editing, nested modal z-index, Zod+RHF validation, service layer rules, error handling |

---

## Table of Contents

1. [Form Modes (create / edit / view)](#1-form-modes-create--edit--view)
2. [Multi-Tab Forms](#2-multi-tab-forms)
3. [Read-Only Detail Display](#3-read-only-detail-display)
4. [Inline Row Editing — isSaved Pattern](#4-inline-row-editing--isaved-pattern)
5. [Nested Modal Z-Index](#5-nested-modal-z-index)
6. [Form Validation — Zod + RHF](#6-form-validation--zod--rhf)
7. [Service Layer Rules](#7-service-layer-rules)
8. [Data Fetching & Error Handling](#8-data-fetching--error-handling)
9. [Do / Don't Quick Reference](#9-do--dont-quick-reference)

---

## 1. Form Modes (create / edit / view)

**One form component handles all three modes** via a `mode` prop. Never create separate Create/Edit/View components for the same entity.

```tsx
// packages/leads/src/components/LeadFormModal.tsx
import { AppModal, Button, InputField } from "@frontend/ui";
import { useForm, Controller, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { leadSchema } from "../schemas/leadsSchemas";
import type { Lead, LeadFormValues } from "../types/leads.types";

interface LeadFormModalProps {
  mode?:          "create" | "edit" | "view";
  open:           boolean;
  onOpenChange:   (open: boolean) => void;
  initialData?:   Lead;
  onSubmit?:      (data: LeadFormValues) => Promise<void>;
}

const defaultValues: LeadFormValues = { name: "", amount: 0, status: "DRAFT" };

export function LeadFormModal({
  mode = "create",
  open,
  onOpenChange,
  initialData,
  onSubmit,
}: LeadFormModalProps) {
  const isViewMode = mode === "view";

  const methods = useForm<LeadFormValues>({
    resolver:      zodResolver(leadSchema),
    defaultValues,
  });
  const { handleSubmit, reset, setValue, formState: { isSubmitting, errors } } = methods;

  // Populate form when opening with existing data
  useEffect(() => {
    if (!open) return;
    if (initialData) {
      Object.entries(initialData).forEach(([k, v]) =>
        setValue(k as keyof LeadFormValues, v as LeadFormValues[keyof LeadFormValues]),
      );
    } else {
      reset(defaultValues);
    }
  }, [initialData, open, setValue, reset]);

  const getTitle = () => {
    if (isViewMode)         return `Detail Lead${initialData ? ` — ${initialData.name}` : ""}`;
    if (mode === "edit")    return "Edit Lead";
    return "Tambah Lead";
  };

  return (
    <AppModal isOpen={open} onClose={() => onOpenChange(false)} title={getTitle()}>
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit!)} className="space-y-4">
          <Controller
            name="name"
            control={methods.control}
            render={({ field }) => (
              <InputField
                {...field}
                label="Nama Lead"
                disabled={isViewMode}
                error={errors.name?.message}
              />
            )}
          />
          {/* ... more fields ... */}

          <div className="flex justify-end gap-2 pt-4 border-t">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              {isViewMode ? "Tutup" : "Batal"}
            </Button>
            {!isViewMode && (
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Menyimpan..." : "Simpan"}
              </Button>
            )}
          </div>
        </form>
      </FormProvider>
    </AppModal>
  );
}
```

**Rules:**
- ✅ `mode === "view"` disables all inputs (`disabled={isViewMode}`) and hides submit button
- ✅ `mode === "edit"` pre-populates via `setValue` in `useEffect` keyed to `[initialData, open]`
- ✅ One component handles all three modes — derive title, button label, and disabled state from `mode`
- ❌ Never create separate `LeadCreateModal`, `LeadEditModal`, `LeadViewModal` — use `LeadFormModal`

---

## 2. Multi-Tab Forms

When a form has **2 or more tabs**, split each tab panel into its own file. The orchestrator owns only modal wrapping, RHF setup, and tab routing.

### File layout

```
packages/[feature]/src/components/
├── [Feature]FormModal.tsx          # orchestrator — modal + useForm + FormProvider + tabs
└── tabs/
    ├── DataUnitTab.tsx             # owns <TabsContent value="data-unit">
    └── DataTransaksiTab.tsx        # owns <TabsContent value="data-transaksi">
```

### Orchestrator (`<Feature>FormModal.tsx`)

Owns: modal wrapping, `useForm`/`FormProvider`, tab state routing, footer buttons.
Does NOT own: tab content, field rendering, array field handlers.

```tsx
// packages/leads/src/components/LeadFormModal.tsx
import { useState } from "react";
import { AppModal, Button } from "@frontend/ui";
import { Tabs, TabsList, TabsTrigger } from "@frontend/ui";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { leadFormSchema } from "../schemas/leadsSchemas";
import { DataUnitTab } from "./tabs/DataUnitTab";
import { DataTransaksiTab } from "./tabs/DataTransaksiTab";

export function LeadFormModal({ mode, open, onOpenChange, initialData, onSubmit }: FormProps) {
  const [tab, setTab] = useState("data-unit");

  const methods = useForm<FormData>({
    resolver:      zodResolver(leadFormSchema),
    defaultValues,
  });

  return (
    <AppModal isOpen={open} onClose={() => onOpenChange(false)} title={getTitle(mode)}>
      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(onSubmit!)} className="space-y-4">
          <Tabs value={tab} onValueChange={setTab}>
            <TabsList>
              <TabsTrigger value="data-unit">Data Unit</TabsTrigger>
              <TabsTrigger value="data-transaksi">Data Transaksi</TabsTrigger>
            </TabsList>
            <DataUnitTab mode={mode} />
            <DataTransaksiTab mode={mode} />
          </Tabs>

          <div className="flex justify-end gap-2 pt-4 border-t">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              {mode === "view" ? "Tutup" : "Batal"}
            </Button>
            {mode !== "view" && (
              <Button type="submit" disabled={methods.formState.isSubmitting}>
                Simpan
              </Button>
            )}
          </div>
        </form>
      </FormProvider>
    </AppModal>
  );
}
```

### Tab file (`tabs/DataUnitTab.tsx`)

Owns its `<TabsContent>` wrapper, reads shared form state via `useFormContext`, keeps tab-local state inside itself.

```tsx
// packages/leads/src/components/tabs/DataUnitTab.tsx
import { useFormContext, Controller } from "react-hook-form";
import { InputField, SelectField } from "@frontend/ui";
import { TabsContent } from "@frontend/ui";
import type { FormData } from "../../types/leads.types";

interface DataUnitTabProps {
  mode: "create" | "edit" | "view";
}

export function DataUnitTab({ mode }: DataUnitTabProps) {
  const { control, formState: { errors } } = useFormContext<FormData>();
  const isViewMode = mode === "view";

  return (
    <TabsContent value="data-unit" className="space-y-4 pt-4">
      <div className="grid grid-cols-2 gap-4">
        <Controller
          name="unitName"
          control={control}
          render={({ field }) => (
            <InputField {...field} label="Nama Unit" disabled={isViewMode} error={errors.unitName?.message} />
          )}
        />
        <Controller
          name="unitType"
          control={control}
          render={({ field }) => (
            <SelectField
              label="Tipe Unit"
              options={unitTypeOptions}
              value={field.value}
              onChange={field.onChange}
              disabled={isViewMode}
              error={errors.unitType?.message}
            />
          )}
        />
      </div>
    </TabsContent>
  );
}
```

### Tab with array fields (useFieldArray via useFormContext)

```tsx
// Tab that contains a list of nested items
import { useFormContext, useFieldArray, Controller } from "react-hook-form";

export function LineItemsTab({ mode }: { mode: string }) {
  const { control } = useFormContext<FormData>();
  const { fields, append, remove } = useFieldArray({ control, name: "lineItems" });
  const isViewMode = mode === "view";

  return (
    <TabsContent value="line-items" className="space-y-4 pt-4">
      {fields.map((field, index) => (
        <div key={field.id} className="grid grid-cols-3 gap-4 items-end">
          <Controller
            name={`lineItems.${index}.name`}
            control={control}
            render={({ f }) => <InputField {...f} label="Nama" disabled={isViewMode} />}
          />
          {!isViewMode && (
            <Button type="button" variant="destructive" size="sm" onClick={() => remove(index)}>
              Hapus
            </Button>
          )}
        </div>
      ))}
      {!isViewMode && (
        <Button type="button" variant="outline" onClick={() => append({ name: "" })}>
          Tambah Item
        </Button>
      )}
    </TabsContent>
  );
}
```

**Rules:**
- ✅ Orchestrator owns `useForm` + `FormProvider` + tab state + footer
- ✅ Tab files own `<TabsContent>` wrapper + field rendering
- ✅ Tabs read shared state via `useFormContext` — never local `useState` for form values
- ✅ Each tab file in `components/tabs/<Name>Tab.tsx`
- ❌ Never use `useState` for form field values inside tab components
- ❌ Never pass the entire form state down as props to tabs — use `useFormContext`

---

## 3. Read-Only Detail Display

Display entity details using **disabled input components** — not `<label>` + `<p>` combinations. This gives consistent form semantics, selectable text, and visual alignment.

```tsx
// ✅ CORRECT — disabled components for read-only display
import { InputField, SelectField, DatePicker } from "@frontend/ui";
import dayjs from "@/lib/dayjs";

// Text field
<InputField label="Cabang"    value={unit.cabangName} disabled />
<InputField label="No. Mesin" value={unit.noMesin}    disabled />

// Dropdown
<SelectField
  label="Tipe Unit"
  options={[{ value: unit.tipeUnit, label: unit.tipeUnit }]}
  value={unit.tipeUnit}
  disabled
/>

// Date (epoch ms → Date object for DatePicker)
<DatePicker
  label="Tanggal PDI"
  value={unit.tanggalPdi ? new Date(unit.tanggalPdi) : undefined}
  disabled
/>
```

**❌ WRONG — label + paragraph:**
```tsx
// ❌ FORBIDDEN
<label className="text-xs text-muted-foreground">Cabang</label>
<p className="font-medium">{unit.cabangName}</p>
```

**Grid layout for multi-column detail sections:**
```tsx
// 2-column form layout
<div className="grid grid-cols-2 gap-4">
  <Controller name="field1" control={control} render={({ field }) => (
    <InputField {...field} label="Field 1" disabled={isViewMode} />
  )} />
  <Controller name="field2" control={control} render={({ field }) => (
    <InputField {...field} label="Field 2" disabled={isViewMode} />
  )} />
</div>

// 3-column read-only detail section — muted background
<div className="grid grid-cols-3 gap-4 p-4 bg-muted rounded-lg mb-4">
  <InputField label="Cabang"  value={unit.cabangName} disabled />
  <InputField label="Warna"   value={unit.namaWarna}  disabled />
  <InputField label="No. FJ"  value={unit.noFj}       disabled />
</div>
```

**Rules:**
- ✅ Always use `disabled` input components for read-only display
- ✅ Use `bg-muted rounded-lg` for detail info sections that visually separate from editable fields
- ❌ Never `<label>` + `<p>` — inconsistent appearance, no selectable text behaviour

---

## 4. Inline Row Editing — isSaved Pattern

For table rows with inline editing (adding/editing items without a separate modal), use the `isSaved` boolean flag on each row item. Never create a separate add/edit modal per row.

```tsx
// Schema — isSaved is a frontend-only UI flag; strip before API call
const itemSchema = z.object({
  id:      z.string().optional(),
  name:    z.string().min(1, "Nama wajib diisi"),
  qty:     z.number().min(1),
  isSaved: z.boolean().optional(),   // ← frontend only, never sent to API
});
type Item = z.infer<typeof itemSchema>;
```

```tsx
// Component using isSaved pattern
const { control, setValue, watch } = useFormContext<FormData>();
const { fields, append, remove } = useFieldArray({ control, name: "items" });
const watchedItems = watch("items");

// Add new row — starts editable (isSaved: false)
const handleAdd = () => append({ id: undefined, name: "", qty: 1, isSaved: false });

// Confirm row — flip to read-only (isSaved: true)
const handleSaveRow = (index: number) => {
  setValue(`items.${index}.isSaved`, true);
};

// Edit existing row — flip back to editable
const handleEditRow = (index: number) => {
  setValue(`items.${index}.isSaved`, false);
};

return (
  <div className="space-y-2">
    {fields.map((field, index) => {
      const item = watchedItems?.[index];
      const isSaved = item?.isSaved ?? true;

      return (
        <div key={field.id} className="flex gap-2 items-end">
          <Controller
            name={`items.${index}.name`}
            control={control}
            render={({ f }) => (
              <InputField {...f} label="Nama" disabled={isSaved} />
            )}
          />
          <Controller
            name={`items.${index}.qty`}
            control={control}
            render={({ f }) => (
              <InputField {...f} label="Qty" type="number" disabled={isSaved} />
            )}
          />
          {isSaved ? (
            <Button type="button" size="sm" variant="outline" onClick={() => handleEditRow(index)}>
              Edit
            </Button>
          ) : (
            <Button type="button" size="sm" onClick={() => handleSaveRow(index)}>
              ✓
            </Button>
          )}
          <Button type="button" size="sm" variant="destructive" onClick={() => remove(index)}>
            Hapus
          </Button>
        </div>
      );
    })}
    <Button type="button" variant="outline" onClick={handleAdd}>
      + Tambah Item
    </Button>
  </div>
);
```

**Strip `isSaved` before sending to API:**
```tsx
const handleFormSubmit = async (data: FormData) => {
  const items = data.items.map(({ isSaved, ...rest }) => rest);  // ← strip isSaved
  await onSubmit({ ...data, items });
};
```

**Rules:**
- ✅ `isSaved: false` = editable row; `isSaved: true` = read-only row
- ✅ New rows appended with `isSaved: false`
- ✅ Strip `isSaved` in `handleSubmit` before sending to API
- ❌ Never create a separate add/edit modal per row item
- ❌ Never send `isSaved` to the backend

---

## 5. Nested Modal Z-Index

Wrap the app with `<ModalProvider>` once. `AppModal` automatically scales z-index by depth (`300 + depth × 100`). No manual `z-*` tuning needed.

```tsx
// apps/[app]/src/App.tsx
import { ModalProvider } from "@frontend/ui";  // or @frontend/shared

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ModalProvider>                     {/* ← wrap app once */}
        <RouterProvider router={router} />
        <GlobalErrorDialog />
      </ModalProvider>
    </QueryClientProvider>
  );
}
```

When a second modal is opened inside a first modal, `AppModal` detects its depth and assigns z-index automatically:
- Depth 1: `z-[300]`
- Depth 2: `z-[400]`
- Depth 3: `z-[500]`

**Rules:**
- ✅ Add `<ModalProvider>` once at app root
- ✅ Use `AppModal` for all modals — z-index handled automatically
- ❌ Never set `z-index` manually on modals
- ❌ Never nest `<ModalProvider>` inside feature components

---

## 6. Form Validation — Zod + RHF

All forms use **Zod** for schema definition and **React Hook Form** for state management, wired together via `zodResolver`.

### Schema definition

```typescript
// packages/leads/src/schemas/leadsSchemas.ts
import { z } from "zod";

export const leadSchema = z.object({
  name:   z.string().min(1, "Nama lead wajib diisi").max(100),
  amount: z.number({ required_error: "Nilai wajib diisi" }).min(1_000_000, "Nilai minimum Rp 1.000.000"),
  status: z.enum(["DRAFT", "SUBMITTED", "APPROVED", "REJECTED"]).optional(),
});

export type LeadFormValues = z.infer<typeof leadSchema>;
```

### Hook setup

```tsx
const {
  control,
  handleSubmit,
  reset,
  formState: { errors, isSubmitting },
} = useForm<LeadFormValues>({
  resolver:      zodResolver(leadSchema),
  defaultValues: { name: "", amount: 0 },
  mode:          "onSubmit",              // validate on submit; show inline on error
});
```

### Field wiring — always via Controller

```tsx
// ✅ Text input
<Controller
  name="name"
  control={control}
  render={({ field }) => (
    <InputField {...field} label="Nama Lead" error={errors.name?.message} disabled={isViewMode} />
  )}
/>

// ✅ Select
<Controller
  name="status"
  control={control}
  render={({ field }) => (
    <SelectField
      label="Status"
      options={statusOptions}
      value={field.value}
      onChange={field.onChange}
      error={errors.status?.message}
      disabled={isViewMode}
    />
  )}
/>

// ✅ DatePicker (epoch ms in form state)
<Controller
  name="dueDate"
  control={control}
  render={({ field }) => (
    <DatePicker
      label="Tanggal Jatuh Tempo"
      value={field.value ? new Date(field.value) : undefined}
      onChange={(date) => field.onChange(date ? dayjs(date).valueOf() : null)}
      error={errors.dueDate?.message}
      disabled={isViewMode}
    />
  )}
/>
```

**Rules:**
- ✅ Always define schema in `schemas/[feature]Schemas.ts`
- ✅ `type FormValues = z.infer<typeof schema>` — single source of truth
- ✅ `mode: "onSubmit"` default; use `"onChange"` only for real-time validation (e.g. password strength)
- ✅ Field errors shown via `error={errors.field?.message}` prop — not toast
- ❌ Never write manual validation logic in `handleSubmit` — put it in the Zod schema

---

## 7. Service Layer Rules

Services contain **only API calls**. No mock data. No error handling. No business logic.

```typescript
// packages/leads/src/services/leadsService.ts
import { apiClient } from "@frontend/shared";
import type { IBaseResponse } from "@frontend/shared";
import type { Lead, LeadFormValues, LeadListParams } from "../types/leads.types";

// ✅ Each function = one API call. That's all.
export const getLeads = (params?: LeadListParams) =>
  apiClient.get<IBaseResponse<Lead[]>>("/api/v1/leads", { params });

export const getLeadById = (id: string) =>
  apiClient.get<IBaseResponse<Lead>>(`/api/v1/leads/${id}`);

export const createLead = (data: LeadFormValues) =>
  apiClient.post<IBaseResponse<Lead>>("/api/v1/leads", data);

export const updateLead = (id: string, data: LeadFormValues) =>
  apiClient.put<IBaseResponse<Lead>>(`/api/v1/leads/${id}`, data);

export const deleteLead = (id: string) =>
  apiClient.delete<IBaseResponse<void>>(`/api/v1/leads/${id}`);
```

**Query parameters — Axios `params` option:**
```typescript
// ✅ Correct
export const listLeads = (filters: LeadListParams) =>
  apiClient.get("/api/v1/leads", { params: filters });
// Axios serialises: /api/v1/leads?page=1&size=10&status=DRAFT

// ❌ Never
const sp = new URLSearchParams();
if (filters.page) sp.set("page", String(filters.page));
return apiClient.get(`/api/v1/leads?${sp}`);   // ← FORBIDDEN
```

**Activity type constants (for audit-aware actions):**
```typescript
// packages/shared/src/constants/activity-type.ts
export const ACTIVITY_TYPE = {
  CREATE: "CREATE",
  READ:   "READ",
  UPDATE: "UPDATE",
  DELETE: "DELETE",
} as const;
```

**Rules:**
- ✅ Services return raw Axios response — no `.data.data` unwrapping in service
- ✅ Services do NOT catch errors — hooks handle errors via `fetchDataAsync`
- ✅ Use Axios `params` for query parameters — never manual string interpolation
- ❌ No `setTimeout`, no mock arrays, no `Promise.resolve(mockData)` in services
- ❌ Components never import from services directly — always via hooks

---

## 8. Data Fetching & Error Handling

**Pattern:** Service → Hook (`fetchDataAsync` + `useErrorStore`) → `GlobalErrorDialog`.

```typescript
// packages/leads/src/hooks/useLeads.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchDataAsync } from "@frontend/shared";
import { useErrorStore } from "@frontend/shared/store/useErrorStore.ts";
import { getLeads, createLead, updateLead, deleteLead } from "../services/leadsService";
import type { LeadFormValues, LeadListParams } from "../types/leads.types";

export const leadKeys = {
  all:    ["leads"] as const,
  list:   (p?: LeadListParams) => ["leads", "list", p] as const,
  detail: (id: string)         => ["leads", "detail", id] as const,
};

// ── Query ──────────────────────────────────────────────────────────────────
export function useLeads(params?: LeadListParams) {
  const setError = useErrorStore((s) => s.setError);
  return useQuery({
    queryKey: leadKeys.list(params),
    queryFn:  () => fetchDataAsync({ asyncFn: () => getLeads(params), setError, menuName: "leads" }),
  });
}

// ── Mutation ───────────────────────────────────────────────────────────────
export function useCreateLead() {
  const qc       = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (data: LeadFormValues) =>
      fetchDataAsync({ asyncFn: () => createLead(data), setError, menuName: "leads" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: leadKeys.all }),
  });
}

export function useUpdateLead() {
  const qc       = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: LeadFormValues }) =>
      fetchDataAsync({ asyncFn: () => updateLead(id, data), setError, menuName: "leads" }),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: leadKeys.all });
      qc.invalidateQueries({ queryKey: leadKeys.detail(id) });
    },
  });
}

export function useDeleteLead() {
  const qc       = useQueryClient();
  const setError = useErrorStore((s) => s.setError);
  return useMutation({
    mutationFn: (id: string) =>
      fetchDataAsync({ asyncFn: () => deleteLead(id), setError, menuName: "leads" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: leadKeys.all }),
  });
}
```

**Mount `GlobalErrorDialog` once at app root:**
```tsx
// apps/[app]/src/App.tsx
import { GlobalErrorDialog } from "@frontend/shared";

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ModalProvider>
        <RouterProvider router={router} />
        <GlobalErrorDialog />   {/* ← handles all API errors */}
      </ModalProvider>
    </QueryClientProvider>
  );
}
```

**Component usage:**
```tsx
function LeadList() {
  const { data, isLoading } = useLeads();
  const deleteLead = useDeleteLead();

  // isLoading → LoadingOverlay
  if (isLoading) return <LoadingOverlay message="Memuat data leads..." />;
  // isError is handled globally by GlobalErrorDialog — no per-component error UI

  return (
    <DataTable
      columns={columns}
      data={data?.data ?? []}
      serverSide
      totalRows={data?.metadata?.totalCount ?? 0}
      // ...pagination props
    />
  );
}
```

**Rules:**
- ✅ `fetchDataAsync` is the only wrapper for async calls in hooks
- ✅ `useErrorStore` + `GlobalErrorDialog` handle API errors globally — no `try/catch` in hooks
- ✅ Field validation errors shown inline via Zod + RHF (`error={errors.field?.message}`)
- ❌ No `try/catch` in service functions
- ❌ No `toast.error(getErrorMessage(error))` for API errors — `GlobalErrorDialog` handles this

---

## 9. Do / Don't Quick Reference

| ❌ Never | ✅ Always | Pattern |
|---------|----------|---------|
| Separate `CreateModal` + `EditModal` + `ViewModal` | Single `FormModal` with `mode` prop | Form Modes |
| Local `useState` for form values inside tab components | `useFormContext` reads from orchestrator's `useForm` | Multi-Tab Forms |
| Pass `props` for shared form state to tabs | `useFormContext<FormData>()` inside tab | Multi-Tab Forms |
| `<label>` + `<p>` for read-only details | `disabled` InputField/SelectField/DatePicker | Read-Only |
| Separate add/edit modal per row | `isSaved: boolean` inline editing | Inline Editing |
| Send `isSaved` to API | Strip it: `items.map(({ isSaved, ...rest }) => rest)` | Inline Editing |
| Manual `z-index` on modals | `ModalProvider` at app root + `AppModal` auto z-index | Z-Index |
| Manual validation in `handleSubmit` | Zod schema + `zodResolver` | Validation |
| Mock/dummy data in services | Real `apiClient.get/post/put/patch/delete` | Service |
| Manual `URLSearchParams` | Axios `params` option | Service |
| `try/catch` in service | Let service throw; hook handles via `fetchDataAsync` | Error Handling |
| Per-component error UI for API errors | `GlobalErrorDialog` mounted once at app root | Error Handling |
