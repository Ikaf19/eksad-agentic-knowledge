# EKSAD Frontend Component Library

**File:** `_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md`
**Version:** 1.0
**Date:** 2026-06-24
**Owner:** EKSAD Platform Team
**Status:** 🟢 Active
**Audience:** Frontend Developer, Tech Lead, Code Reviewer
**Upload-to:** GPT knowledge base — Dev FE GPT, TL GPT

> All shared UI components live in `@frontend/ui`. Never recreate them from scratch.
> Source of truth: `need-to-update/components.md` + `need-to-update/fundamentals.md`.

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-24 | EKSAD docs maintainer | Initial version — AppModal, AlertDialog, LoadingOverlay, SelectField, DatePicker, DataTable, InputField |

---

## Table of Contents

1. [Import Reference](#1-import-reference)
2. [AppModal — Forms & Detail Views](#2-appmodal--forms--detail-views)
3. [AlertDialog — Confirmations Only](#3-alertdialog--confirmations-only)
4. [LoadingOverlay — All Loading States](#4-loadingoverlay--all-loading-states)
5. [SelectField — Dropdown with Modes](#5-selectfield--dropdown-with-modes)
6. [DatePicker — Date Input](#6-datepicker--date-input)
7. [DataTable — All Table Markup](#7-datatable--all-table-markup)
8. [InputField — Text / Number / Read-Only](#8-inputfield--text--number--read-only)
9. [Do / Don't Quick Reference](#9-do--dont-quick-reference)

---

## 1. Import Reference

```typescript
// All UI components from @frontend/ui — never from @/components/ui
import { Button, InputField }       from "@frontend/ui";
import { SelectField }              from "@frontend/ui";
import type { SelectOption }        from "@frontend/ui";
import { DatePicker }               from "@frontend/ui";
import { DataTable }                from "@frontend/ui";
import type { ColumnDef }           from "@tanstack/react-table";   // TanStack Table type
import { AppModal, LoadingOverlay } from "@frontend/ui";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
}                                   from "@frontend/ui";
import { Card, Container, Page, Row, Section } from "@frontend/ui";
```

---

## 2. AppModal — Forms & Detail Views

Use `AppModal` for any modal that contains **user input or substantial content**: create/edit forms, filter panels, detail view, confirmation dialogs that require explanation.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `isOpen` | `boolean` | ✅ | Controls visibility |
| `onClose` | `() => void` | ✅ | Called when modal should close |
| `title` | `string` | ✅ | Modal header title |
| `children` | `ReactNode` | ✅ | Modal content |

### Usage

```tsx
import { AppModal } from "@frontend/ui";

function LeadFormModal({ open, onOpenChange, mode, initialData }: LeadFormModalProps) {
  return (
    <AppModal
      isOpen={open}
      onClose={() => onOpenChange(false)}
      title={mode === "create" ? "Tambah Lead" : mode === "edit" ? "Edit Lead" : `Detail Lead`}
    >
      {/* form or detail content */}
      <form className="space-y-4">
        {/* ... */}
        <div className="flex justify-end gap-2 pt-4 border-t">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {mode === "view" ? "Tutup" : "Batal"}
          </Button>
          {mode !== "view" && (
            <Button type="submit">Simpan</Button>
          )}
        </div>
      </form>
    </AppModal>
  );
}
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| Use `AppModal` for create/edit forms | Use `AlertDialog` for forms |
| Use `AppModal` for detail views | Build custom `fixed inset-0 bg-black/50` backdrop |
| Use `AppModal` for filter panels | Use `AppModal` for simple yes/no confirmations |

---

## 3. AlertDialog — Confirmations Only

Use `AlertDialog` **only** for brief yes/no confirmations: delete confirmation, destructive action warning. No forms, no substantial content.

```tsx
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
} from "@frontend/ui";

function DeleteLeadDialog({ open, onOpenChange, onConfirm, leadName }: DeleteLeadDialogProps) {
  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogTitle>Hapus Lead</AlertDialogTitle>
        <AlertDialogDescription>
          Apakah Anda yakin ingin menghapus lead <strong>{leadName}</strong>?
          Tindakan ini tidak dapat dibatalkan.
        </AlertDialogDescription>
        <div className="flex justify-end gap-2 mt-4">
          <AlertDialogCancel>Batal</AlertDialogCancel>
          <AlertDialogAction onClick={onConfirm} className="bg-red-600 hover:bg-red-700">
            Hapus
          </AlertDialogAction>
        </div>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| Use for delete confirmation | Use for create/edit forms |
| Use for destructive action warning | Use for detail views |
| Keep content brief (title + 1–2 sentences) | Use for complex multi-field dialogs |

---

## 4. LoadingOverlay — All Loading States

Use `LoadingOverlay` for **all** loading states. Never create custom spinners or inline loading indicators.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `message` | `string` | ✅ | Descriptive loading message shown to user |

### Usage

```tsx
import { LoadingOverlay } from "@frontend/ui";

// ✅ CORRECT — full component/overlay replacement during fetch
function LeadList() {
  const { data, isLoading } = useLeads();

  if (isLoading) {
    return <LoadingOverlay message="Memuat data leads..." />;
  }

  return <DataTable columns={columns} data={data?.data ?? []} />;
}

// ✅ In modal — replaces entire modal content during fetch
function LeadDetailModal({ id, open, onOpenChange }: Props) {
  const { data, isLoading } = useLeadDetail(id);

  return (
    <AppModal isOpen={open} onClose={() => onOpenChange(false)} title="Detail Lead">
      {isLoading ? (
        <LoadingOverlay message="Memuat detail lead..." />
      ) : (
        <LeadDetailContent data={data} />
      )}
    </AppModal>
  );
}
```

**❌ WRONG — custom inline spinner:**
```tsx
// ❌ FORBIDDEN
if (isLoading) {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="animate-spin">
        <RefreshCwIcon className="size-8" />
      </div>
    </div>
  );
}
```

**Rules:**
1. Use descriptive messages: `"Memuat data unit..."`, `"Menyimpan perubahan..."`, not generic `"Loading..."`
2. Wrap the entire component/overlay — not just a spinner inside existing content
3. For modal, replaces entire modal content
4. For fast form submissions, use `button disabled` state; only add `LoadingOverlay` if operation takes ≥ 500 ms

---

## 5. SelectField — Dropdown with Modes

Portal-based dropdown that escapes overflow containers. Three modes available.

### Modes

| Mode | Behaviour | Returns | When to Use |
|------|-----------|---------|-------------|
| `default` | Searchable single-select | `string` value | Standard dropdowns with search |
| `multi` | Searchable multi-select | `string[]` values | Multi-value selection |
| `simple` | Radix non-searchable | `SelectOption` object | Short option lists, toggles with explicit values |

### Props (key)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `mode` | `"default" \| "multi" \| "simple"` | `"default"` | Select behaviour |
| `options` | `SelectOption[]` | — | `{ value: string, label: string }[]` |
| `value` | `string \| string[] \| SelectOption` | — | Controlled value |
| `onChange` | `(value) => void` | — | Change handler |
| `label` | `string` | — | Field label |
| `error` | `string` | — | Field-level error message |
| `disabled` | `boolean` | `false` | Disabled / read-only state |
| `dropdownPosition` | `"top" \| "bottom" \| "auto"` | `"auto"` | Portal positioning override |

### Usage — default mode (searchable single)

```tsx
import { SelectField } from "@frontend/ui";

<Controller
  name="status"
  control={control}
  render={({ field }) => (
    <SelectField
      label="Status"
      options={[
        { value: "DRAFT",     label: "Draft" },
        { value: "SUBMITTED", label: "Diajukan" },
        { value: "APPROVED",  label: "Disetujui" },
      ]}
      value={field.value}
      onChange={field.onChange}
      error={errors.status?.message}
      disabled={isViewMode}
    />
  )}
/>
```

### Usage — multi mode

```tsx
<SelectField
  mode="multi"
  label="Tags"
  options={tagOptions}
  value={field.value}       // string[]
  onChange={field.onChange} // (values: string[]) => void
/>
```

### Usage — simple mode (non-searchable, returns SelectOption object)

```tsx
// ✅ Use simple mode for short constrained lists — NOT button toggles (see §14 Forbidden)
<SelectField
  mode="simple"
  label="Kondisi"
  options={[
    { value: "OK",     label: "OK" },
    { value: "NOT_OK", label: "Tidak OK" },
  ]}
  value={field.value}            // SelectOption object
  onChange={field.onChange}
/>
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| Use `SelectField` for all dropdown inputs | Create custom `<select>` markup |
| Use `mode="simple"` for constrained short lists | Use button toggles for OK/Not OK — use `SelectField mode="simple"` |
| Pass `disabled={true}` for read-only display | Use `<label>` + `<p>` for read-only dropdown values |

---

## 6. DatePicker — Date Input

Always use `<DatePicker>` for date inputs. **Never `<InputField type="date">`.**

`DatePicker` accepts and returns a `Date` object. Store timestamps as `number` (epoch ms) in form state and convert at the boundary.

### Props (key)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `label` | `string` | ✅ | Field label |
| `value` | `Date \| undefined` | — | Controlled value (Date object) |
| `onChange` | `(date: Date \| undefined) => void` | — | Change handler |
| `disabled` | `boolean` | `false` | Read-only state |
| `error` | `string` | — | Field-level error message |

### Usage with RHF (epoch ms in form state)

```tsx
import { DatePicker } from "@frontend/ui";
import dayjs from "@/lib/dayjs";

// Form state stores epoch ms (number); DatePicker works with Date objects
<Controller
  name="dueDate"
  control={control}
  render={({ field }) => (
    <DatePicker
      label="Tanggal Jatuh Tempo"
      value={field.value ? new Date(field.value) : undefined}
      onChange={(date) => field.onChange(date ? dayjs(date).valueOf() : null)}
      disabled={isViewMode}
      error={errors.dueDate?.message}
    />
  )}
/>
```

### Usage — read-only display

```tsx
// ✅ Disabled DatePicker for read-only detail view
<DatePicker
  label="Tanggal PDI"
  value={unit.tanggalPdi ? new Date(unit.tanggalPdi) : undefined}
  disabled={true}
/>
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| `<DatePicker>` for all date fields | `<InputField type="date">` |
| Convert epoch ms ↔ `Date` at the boundary | Store `Date` objects in form state |
| Use `disabled={true}` for read-only display | Use `<label>` + `<p>` for read-only date |
| `dayjs(date).valueOf()` to get epoch ms from `Date` | `date.getTime()` — use dayjs instead |

---

## 7. DataTable — All Table Markup

Never write manual `<table>` markup. `DataTable` is built on **TanStack Table** and handles empty states, sorting, and server-side pagination automatically.

### Props (key)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `columns` | `ColumnDef<T>[]` | ✅ | TanStack Table column definitions |
| `data` | `T[]` | ✅ | Row data |
| `serverSide` | `boolean` | — | Enable server-side pagination mode |
| `page` | `number` | server | Current page (1-based) |
| `rowsPerPage` | `number` | server | Rows per page |
| `totalRows` | `number` | server | Total row count from backend |
| `onPageChange` | `(page: number) => void` | server | Page change callback |
| `onRowsPerPageChange` | `(size: number) => void` | server | Rows per page callback |

### Column definition — use `meta.className` with `min-w-*`

```tsx
import type { ColumnDef } from "@tanstack/react-table";

const columns: ColumnDef<Lead>[] = [
  {
    id: "no",
    header: "No",
    cell: ({ row }) => row.index + 1,
    meta: { className: "min-w-12" },          // ← min-w-*, not w-*
  },
  {
    accessorKey: "name",
    header: "Nama Lead",
    meta: { className: "min-w-48" },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => <LeadStatusBadge status={row.original.status} />,
    meta: { className: "min-w-32" },
  },
  {
    id: "actions",
    header: "Aksi",
    cell: ({ row }) => (
      <div className="flex gap-2">
        <Button size="sm" onClick={() => onEdit(row.original)}>Edit</Button>
        <Button size="sm" variant="destructive" onClick={() => onDelete(row.original.id)}>Hapus</Button>
      </div>
    ),
    meta: { className: "min-w-32 text-center" },
  },
];
```

**Why `min-w-*` not `w-*`:** DataTable uses HTML auto table layout. `min-width` is always enforced and lets columns grow with longer content. `width` is only a hint and gets overridden when content is wider or narrower. When total min-widths exceed the container, the table extends horizontally and the parent's `overflow-auto` provides scroll.

**Per-cell or per-header override:**
```tsx
meta: {
  className:       "min-w-32",          // applied to both <th> and <td>
  headerClassName: "text-right",        // applied to <th> only
  cellClassName:   "font-mono text-sm", // applied to <td> only
}
```

**❌ WRONG — don't wrap content in a div with w-*:**
```tsx
// ❌ WRONG
cell: ({ row }) => <div className="w-48">{row.original.name}</div>

// ✅ CORRECT — width on the column via meta.className
meta: { className: "min-w-48" }
```

### Server-side pagination

```tsx
import { DataTable } from "@frontend/ui";
import { useState } from "react";

function LeadsTable() {
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const { data, isLoading } = useLeads({ page, size: rowsPerPage });

  if (isLoading) return <LoadingOverlay message="Memuat data leads..." />;

  return (
    <DataTable
      columns={columns}
      data={data?.data ?? []}
      serverSide
      page={page}
      rowsPerPage={rowsPerPage}
      totalRows={data?.metadata?.totalCount ?? 0}
      onPageChange={setPage}
      onRowsPerPageChange={(size) => { setRowsPerPage(size); setPage(1); }}
    />
  );
}
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| `<DataTable>` for all tabular data | Manual `<table>` / `<thead>` / `<tbody>` markup |
| `meta.className` with `min-w-*` | Wrap cell content in `<div className="w-...">` |
| `serverSide` + `totalRows` from backend `metadata.totalCount` | Implement client-side pagination manually |
| Return `<LoadingOverlay>` when `isLoading` before rendering `DataTable` | Pass empty array and rely on DataTable's internal loading state |

---

## 8. InputField — Text / Number / Read-Only

Standard text input. Also the canonical component for read-only detail display (via `disabled`).

### Props (key)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `label` | `string` | ✅ | Field label |
| `value` | `string \| number` | — | Controlled value |
| `onChange` | RHF `field.onChange` | — | Change handler |
| `disabled` | `boolean` | `false` | Read-only state |
| `error` | `string` | — | Field-level error message (inline) |
| `type` | `"text" \| "number" \| "email" \| "password"` | `"text"` | Input type — **never `"date"`** |

### Usage with RHF

```tsx
<Controller
  name="name"
  control={control}
  render={({ field }) => (
    <InputField
      {...field}
      label="Nama Lead"
      error={errors.name?.message}
      disabled={isViewMode}
    />
  )}
/>
```

### Read-only display (disabled)

Use `disabled={true}` for displaying read-only entity details inside modals and forms.

```tsx
// ✅ CORRECT — disabled InputField for read-only display
<InputField label="Cabang" value={unit.cabangName} disabled={true} />

// ❌ WRONG — label + paragraph
<label className="text-xs text-muted-foreground">Cabang</label>
<p className="font-medium">{unit.cabangName}</p>
```

**Layout — grid for multi-column form / detail sections:**
```tsx
// 2-column form
<div className="grid grid-cols-2 gap-4">
  <Controller name="field1" ... render={({ field }) => <InputField {...field} label="Field 1" />} />
  <Controller name="field2" ... render={({ field }) => <InputField {...field} label="Field 2" />} />
</div>

// 3-column detail section — muted background
<div className="grid grid-cols-3 gap-4 p-4 bg-muted rounded-lg mb-4">
  <InputField label="Cabang"  value={unit.cabangName} disabled />
  <InputField label="Warna"   value={unit.namaWarna}  disabled />
  <InputField label="No. FJ"  value={unit.noFj}       disabled />
</div>
```

### ✅ Do / ❌ Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| `disabled={true}` for read-only display | `<label>` + `<p>` for read-only detail |
| `error={errors.field?.message}` for validation | Show validation errors only as toast |
| `type="number"` for numeric input | Use `<InputField type="date">` — use `<DatePicker>` |

---

## 9. Do / Don't Quick Reference

| ❌ Never | ✅ Always | Component |
|---------|----------|-----------|
| Custom `fixed inset-0 bg-black/50` backdrop | `AppModal` | Modal |
| `AlertDialog` for forms | `AppModal` for forms | Modal |
| `AppModal` for yes/no confirmations | `AlertDialog` for confirmations | Modal |
| Custom inline spinner / loading div | `LoadingOverlay` | Loading |
| Custom `<select>` markup | `SelectField` | Dropdown |
| Button toggles for constrained values | `SelectField mode="simple"` | Dropdown |
| `<InputField type="date">` | `<DatePicker>` | Date |
| Manual `<table>` / `<thead>` / `<tbody>` | `<DataTable>` | Table |
| `w-*` on column cell content `<div>` | `meta.className: "min-w-*"` | Table |
| `<label>` + `<p>` for read-only detail | `<InputField disabled>` / `<SelectField disabled>` | Read-only |
| `new Date(epochMs)` directly | `dayjs(epochMs).format(...)` | Dates |
| `import { Button } from "@/components/ui"` | `import { Button } from "@frontend/ui"` | Imports |
