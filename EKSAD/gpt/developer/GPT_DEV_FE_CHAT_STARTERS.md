# EKSAD Frontend Developer GPT — Chat Starters

> Pilih **Top 4** untuk GPT UI. Library lengkap di bawah untuk referensi.

---

## 🟢 Recommended Top 4

```
Scaffold feature module baru untuk [nama fitur] dengan fields: [list fields dan types]
```
```
Buatkan consolidated hook untuk fitur [nama fitur] — queries: list + detail, mutations: create + update + delete
```
```
Buatkan unit test untuk hook [nama hook] — happy path + error + loading state
```
```
Buatkan form component untuk [nama fitur] dengan fields: [list fields]. Validasi: [list rules]
```

---

## 📋 Full Frontend Developer Starter Library

### Feature Module Scaffold

```
Scaffold feature module lengkap untuk [nama fitur]. Fields entity: [list fields dan types]. Ada approval workflow? [ya/tidak]. Route base path: /[path].
```
```
Buatkan struktur folder dan file untuk feature [nama fitur] — components, hooks, services, types, pages. Jelaskan isi tiap file.
```

### TypeScript Types

```
Buatkan TypeScript types untuk entity [nama entity] dengan fields: [list]. Status yang mungkin: [list status]. Sertakan FormValues dan ListParams types.
```
```
Buatkan shared ApiResponse dan PaginatedResponse wrapper types untuk response envelope dari backend EKSAD.
```

### Consolidated Hooks

```
Buatkan consolidated hook use[NamaFitur].ts untuk fitur [nama fitur]. Operations: GET list dengan pagination, GET detail by ID, POST create, PUT update, DELETE (soft delete).
```
```
Buatkan hook untuk fitur [nama fitur] yang punya approval workflow — tambahkan mutation untuk SUBMIT, APPROVE, dan REJECT.
```
```
Bagaimana cara buat dependent query di React Query — query B hanya jalan setelah query A berhasil dan ada hasilnya?
```
```
Bagaimana cara invalidate query yang tepat setelah mutation berhasil? Saya punya list query dan detail query untuk [nama fitur].
```

### Service Layer & Mock Data

```
Buatkan service layer (mock data) untuk [nama fitur] dengan operations: getAll, getById, create, update, delete. Tandai semua dengan TODO BACKEND INTEGRATION.
```
```
Buatkan mock data realistis untuk entity [nama entity] — minimal 5 sample records. Fields: [list].
```
```
Bagaimana cara migrasi service [nama fitur] dari mock data layer ke Axios API calls? Endpoint yang tersedia: [list endpoints].
```

### React Components

```
Buatkan list component untuk [nama fitur] — tampilkan data dalam tabel/card, handle loading + error + empty state. Gunakan TailwindCSS.
```
```
Buatkan detail component untuk [nama fitur] dengan fields: [list]. Tampilkan status badge dan timestamps yang diformat.
```
```
Buatkan StatusBadge component untuk [nama entity] dengan status: [list status]. Setiap status punya warna berbeda.
```
```
Buatkan komponen tabel yang reusable dengan props: columns, data, isLoading, onEdit, onDelete. Support pagination.
```

### Form Components

```
Buatkan form component untuk create/edit [nama fitur] menggunakan React Hook Form. Fields: [list fields + tipe + validasi]. Setelah submit sukses: [aksi].
```
```
Buatkan confirmation modal untuk delete [nama entity] — tampilkan nama item yang akan dihapus, tombol Batal dan Hapus.
```
```
Bagaimana cara handle form yang sama untuk create dan edit (mode detection berdasarkan ada tidaknya ID)?
```

### React Router

```
Buatkan route definition untuk feature [nama fitur] dengan routes: list, detail, new, edit. Sertakan ROUTES constants.
```
```
Bagaimana cara buat protected route yang redirect ke /login jika user belum autentikasi?
```

### Pages

```
Buatkan page component [nama fitur]ListPage — layout dengan header, tombol tambah, filter/search bar, dan list component.
```
```
Buatkan page component [nama fitur]DetailPage — layout dengan breadcrumb, header dengan action buttons (edit, delete, submit/approve jika ada workflow).
```

### Testing — Hooks

```
Buatkan unit test lengkap untuk hook use[NamaFitur] — test setiap query dan mutation: happy path, error state, loading state.
```
```
Bagaimana cara test React Query hook yang punya dependent query (query B enabled berdasarkan hasil query A)?
```
```
Bagaimana cara test mutation yang invalidate query setelah berhasil?
```

### Testing — Components

```
Buatkan component test untuk [nama component] — test render data, loading state, error state, empty state, dan user interaction.
```
```
Buatkan form test untuk [nama form] — test submit valid, validasi field kosong, error dari service, loading state tombol submit.
```
```
Bagaimana cara mock service module di Jest saat testing component yang menggunakan mock data layer?
```

### Backend Integration Migration

```
Ini backend API sudah siap. Bantu saya migrasi service [nama service] dari mock ke real API. Endpoint tersedia: [list endpoints dengan method dan path]. Response format: [paste contoh response].
```
```
Bagaimana cara setup Axios instance dengan interceptor untuk: (1) tambah JWT token di header, (2) handle 401 redirect ke login?
```
```
Ini response dari backend: [paste response JSON]. Buatkan TypeScript types yang sesuai dan update service-nya.
```

### Debugging

```
Kode ini throw error: [paste error message atau stack trace]. Tolong bantu debug dan fix.
```
```
React Query saya selalu refetch padahal data masih fresh. Config saya: [paste config]. Bagaimana cara fix?
```
```
Form saya tidak menampilkan error validasi meski field kosong saat submit. Kode: [paste].
```
```
Query ini selalu return undefined tapi data ada di mock: [paste hook dan service code]. Apa yang salah?
```

### TailwindCSS

```
Buatkan layout halaman [nama halaman] dengan TailwindCSS: sidebar navigasi kiri + konten utama + header. Responsive mobile.
```
```
Bagaimana cara buat conditional TailwindCSS classes yang clean menggunakan cn() utility?
```

## 💡 Tips untuk Dev FE GPT

- **Selalu paste FSD atau TSD** — semakin lengkap konteks, semakin akurat kode yang dihasilkan
- **Sebutkan fields entity** — "fields: name string, amount number, status LeadStatus" → kode lengkap langsung
- **Minta test setelah kode** — setelah dapat hook atau service, langsung bilang "sekarang buatkan unit test-nya"
- **Sebutkan jika ada approval workflow** — GPT akan otomatis tambahkan mutations untuk SUBMIT, APPROVE, REJECT
- **Tanya mock-to-API migration** — saat backend sudah siap, GPT bisa panduan migrasi step by step
