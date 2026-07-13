# TIA Reporting v2 — Domain Knowledge File (Updated)
# For: Business Analyst GPT (TIA Team Extension)

**Version:** 2.0
**Date:** 27 April 2026
**Owner:** EKSAD Platform Team / TIA Project
**Audience:** BA GPT (upload sebagai additional knowledge file)
**Based on:** `BRD — TIA Reporting System v2 (Client).md` · FSD-01 s/d FSD-08

> File ini di-upload sebagai **Custom GPT knowledge file** bersama file BA GPT standar.
> File ini meng-extend GPT dengan TIA-specific domain knowledge — business context, modul, role, business rules, user stories, dan error codes.
> **v2.0:** Update dari v1.0 — konten disesuaikan dengan dokumen FSD final (FSD-01 s/d FSD-08).

---

## Part 1 — Project & Business Context

### 1.1 Apa itu TIA Reporting?

**TIA Reporting** adalah platform konsolidasi keuangan dan pelaporan untuk **Triputra Group** — konglomerat Indonesia. Platform dioperasikan oleh **Triputra Investment Authority (TIA)**, divisi holding company. TIA mengumpulkan, mereview, menyetujui, dan menganalisis laporan keuangan periodik dari semua **perusahaan anak (SubCo)**.

**System codename:** `tia-reporting-v2`
**Architecture:** Java 21 + Quarkus 3.x, event-driven microservices (10 services)
**Database:** PostgreSQL per service + MongoDB Atlas (audit trail)

### 1.2 Siklus Pelaporan

| Siklus | Kode | Frekuensi | Sub-Reports |
|--------|------|-----------|-------------|
| Master Budget | MB | Tahunan | P&L, Tax Planning, BS, FAM, CF, LOCF, CAT |
| Monthly Report | MR | Bulanan | P&L, Tax Planning, BS, FAM, CF, LOCF, CAT, OI |
| Outlook PA | OPA | Tahunan | P&L, Tax Planning, BS, FAM, CF, LOCF, CAT |
| Rolling Outlook | RO | Kuartalan (Q1,Q2,Q3) | P&L, Tax Planning, BS, FAM, CF, LOCF, CAT |

### 1.3 Status Laporan

```
draft → submitted → approval_review → approved
                         ↓
                      rejected → (revisi baru, kembali ke draft)
```

---

## Part 2 — User Roles

| Role Code | Nama | Scope Akses | Catatan |
|-----------|------|-------------|---------|
| `ROLE_SUPERADMIN` | SuperAdmin | Semua modul, semua company, semua tenant | Bypass semua permission & approval |
| `ROLE_TIA` | User TIA | Semua laporan konsolidasi | Bisa approve/reject |
| `ROLE_SUBCO` | User SubCo | Company yang ditugaskan saja | Buat/edit/submit laporan |
| `ROLE_VIEWER` | View Only | Semua laporan — read only | Tidak ada aksi create/edit/submit |
| `ROLE_BOD` | Board of Directors | Dashboard & summary reports | Tidak ada aksi operasional |
| `ROLE_STAKEHOLDER` | Stakeholder | View terbatas per konfigurasi | External viewer |

### 2.1 Role CAFRM (11 roles)

| Role | Kategori | Scope |
|------|----------|-------|
| `ROLE_CAFRM_IA_SUBCO` | Internal Audit | Company yang ditugaskan |
| `ROLE_CAFRM_IA_TIA` | Internal Audit | Semua company |
| `ROLE_CAFRM_IA_BOD` | Internal Audit | View only semua company |
| `ROLE_CAFRM_AF_SUBCO` | Anti Fraud | Company yang ditugaskan |
| `ROLE_CAFRM_AF_TIA` | Anti Fraud | Semua company |
| `ROLE_CAFRM_AF_BOD` | Anti Fraud | View only semua company |
| `ROLE_CAFRM_RM_SUBCO` | Risk Management | Company yang ditugaskan |
| `ROLE_CAFRM_RM_TIA` | Risk Management | Semua company |
| `ROLE_CAFRM_RM_BOD` | Risk Management | View only semua company |
| (+ SuperAdmin) | — | Semua CAFRM |
| (User TIA biasa) | — | TIDAK ada akses CAFRM |

---

## Part 3 — Module Overview

| Modul | FSD | Service | Deskripsi |
|-------|-----|---------|-----------|
| Autentikasi & Gateway | FSD-01 | `tia-auth-service` + `tia-gateway` | JWT RS256 login/logout/refresh/reset password; routing dan rate limiting |
| Submission Laporan | FSD-02 | `tia-submission-service` | Buat, edit, import Excel, submit laporan; manajemen revisi; lampiran |
| Approval Workflow | FSD-03 | `tia-approval-service` | Unified engine: AND/OR multi-level; approval matrix; bypass SuperAdmin |
| Agregasi & Dashboard | FSD-04 | `tia-aggregation-service` | YTD, MTD, CPSM, Historical; ratio formula engine; dashboard |
| Master Data | FSD-05 | `tia-master-data-service` | Company, BU, User, Role, Item Report, Currency, Setting, Holiday, Approval Matrix, Feature Flag, Mail Template |
| Notifikasi & File | FSD-06 | `tia-notification-service` + `tia-file-service` | Email reminder H+1, approval alerts; upload/download lampiran; export Excel/ZIP |
| Audit Trail | FSD-07 | `tia-audit-service` | Append-only MongoDB audit; fire-and-forget; TTL 2 tahun |
| CAFRM | FSD-08 | `tia-cafrm-service` | Document vault IA/AF/RM; feature flag controlled |

---

## Part 4 — Business Rules Ringkas

### 4.1 Data Selection Rules (YTD)
- Hanya revisi terbaru (`ORDER BY revision DESC LIMIT 1`)
- Hanya data `current_status = 'approved'`
- Semua query **wajib diparameterisasi** — tidak ada hardcoded `company_id` atau `year`
- YTD bulan: `month <= target_month` (inklusif)
- YTD Rolling Outlook: sum 12 kolom bulan bernama (jan+feb+...+dec)

### 4.2 Period Rules
| Siklus | Aturan Periode |
|--------|----------------|
| MB | Jika bulan = Desember → tahun depan; lainnya → tahun ini |
| MR | Bulan saat ini - 1; jika Januari → Desember tahun lalu |
| OPA | Tahun berjalan |
| RO | Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep). Tidak ada Q4 |

### 4.3 Approval Rules
- AND operator: semua approver di level harus approve
- OR operator: satu approve → auto-approve peer → lanjut level berikutnya
- SuperAdmin: bypass semua level; keterangan "Superadmin"
- Approval matrix entry: hanya valid jika `start_date <= today <= end_date`
- Duplikasi approval dicegah: cek existing record sebelum inisiasi baru
- Semua sub-laporan harus ada detailnya sebelum bisa submit

### 4.4 Notification Rules
| Rule | Detail |
|------|--------|
| H+1 | Pengingat dikirim 1 hari setelah due date |
| Skip Minggu | H+1 = Minggu → geser ke Senin |
| Skip Libur | Jika tanggal pengingat = hari libur (`mst_holiday`) → geser +1 hari |
| Hanya draft/incomplete | Tidak kirim jika laporan sudah approved |
| No duplicate | `notif_reminder_history` mencegah kirim 2x di hari yang sama |

### 4.5 Tax Planning Rules
| Report Type | Kolom yang Digunakan |
|-------------|---------------------|
| MB | `amount_tbf` |
| MR | `mtd_tbf` |
| OPA, RO | `amount` |
| MB filter tambahan | `attr IN ('actual', 'periode') AND month <= target_month` |

### 4.6 Rolling Outlook Reference Values di MR
| Bulan MR | Referensi |
|----------|-----------|
| 1–3 | MB (fallback: MB) |
| 4–6 | RO Q1 (fallback: MB) |
| 7–9 | RO Q2 (fallback: MB) |
| 10–12 | RO Q3 (fallback: MB) |

---

## Part 5 — Error Code Registry

> Format error code: `{PREFIX}_{NOUN}_{ISSUE}` — selalu UPPER_SNAKE_CASE.

### 5.1 Auth (FSD-01)

| Code | HTTP | Trigger |
|------|------|---------|
| `AUTH_CREDENTIALS_INVALID` | 401 | Username/password salah |
| `AUTH_ACCOUNT_INACTIVE` | 401 | User dinonaktifkan |
| `AUTH_TOKEN_EXPIRED` | 401 | JWT kedaluwarsa |
| `AUTH_TOKEN_INVALID` | 401 | JWT tidak valid |
| `AUTH_REFRESH_TOKEN_INVALID` | 401 | Refresh token tidak valid / sudah dipakai |
| `AUTH_RESET_TOKEN_INVALID` | 400 | Token reset password tidak valid / expired |
| `AUTH_FORBIDDEN` | 403 | Tidak punya permission |
| `AUTH_PASSWORD_WEAK` | 400 | Password baru tidak memenuhi aturan |

### 5.2 Submission (FSD-02)

| Code | HTTP | Trigger |
|------|------|---------|
| `SUB_NOT_FOUND` | 404 | Laporan tidak ditemukan |
| `SUB_DUPLICATE` | 409 | Company/periode/tipe laporan sudah ada |
| `SUB_INVALID_STATE` | 422 | Aksi tidak valid untuk status saat ini |
| `SUB_CANNOT_SUBMIT` | 422 | Belum semua sub-laporan lengkap |
| `SUB_EXCEL_PARSE_ERROR` | 400 | File Excel tidak valid atau format salah |
| `SUB_EXCEL_VALIDATION_FAILED` | 400 | Data dalam Excel tidak lulus validasi |
| `SUB_ATTACHMENT_SIZE_EXCEEDED` | 413 | File lampiran > 100MB |
| `SUB_ATTACHMENT_TYPE_NOT_ALLOWED` | 415 | Tipe file tidak diizinkan |
| `SUB_ACCESS_FORBIDDEN` | 403 | Company tidak ditugaskan ke user |

### 5.3 Approval (FSD-03)

| Code | HTTP | Trigger |
|------|------|---------|
| `APR_NOT_FOUND` | 404 | Data approval tidak ditemukan |
| `APR_NOT_YOUR_LEVEL` | 403 | User bukan approver di level aktif |
| `APR_ALREADY_ACTED` | 422 | User sudah approve/reject laporan ini |
| `APR_DUPLICATE_INIT` | 409 | Approval sudah diinisiasi untuk laporan ini |
| `APR_INVALID_STATE` | 422 | Laporan tidak dalam status yang bisa di-approve |
| `APR_REASON_REQUIRED` | 400 | Alasan penolakan wajib diisi saat reject |

### 5.4 Aggregation (FSD-04)

| Code | HTTP | Trigger |
|------|------|---------|
| `AGG_NO_APPROVED_DATA` | 404 | Tidak ada data approved untuk periode yang diminta |
| `AGG_INVALID_PERIOD` | 400 | Kombinasi year/month/quarter tidak valid |
| `AGG_FORMULA_ERROR` | 500 | Error evaluasi formula ratio di GraalVM JS |

### 5.5 Master Data (FSD-05)

| Code | HTTP | Trigger |
|------|------|---------|
| `MD_NOT_FOUND` | 404 | Entity tidak ada |
| `MD_COMPANY_NAME_DUPLICATE` | 409 | Nama company tidak unik |
| `MD_COMPANY_CODE_DUPLICATE` | 409 | Kode company tidak unik |
| `MD_USERNAME_DUPLICATE` | 409 | Username tidak unik |
| `MD_EMAIL_DUPLICATE` | 409 | Email tidak unik |
| `MD_ROLE_NOT_FOUND` | 404 | Role tidak ditemukan |
| `MD_BU_NOT_FOUND` | 404 | Business Unit tidak ditemukan |
| `MD_ITEM_CODE_DUPLICATE` | 409 | Kode item laporan tidak unik |
| `MD_COMPANY_IN_USE` | 422 | Company tidak bisa dihapus; masih dipakai dalam laporan |

### 5.6 File (FSD-06)

| Code | HTTP | Trigger |
|------|------|---------|
| `FILE_NOT_FOUND` | 404 | File tidak ditemukan |
| `FILE_SIZE_EXCEEDED` | 413 | File > 100MB |
| `FILE_TYPE_NOT_ALLOWED` | 415 | MIME type tidak diizinkan |
| `FILE_ACCESS_FORBIDDEN` | 403 | User tidak punya akses ke company pemilik laporan |
| `FILE_ALREADY_DELETED` | 422 | File sudah dihapus sebelumnya |
| `FILE_DELETE_FORBIDDEN` | 422 | Laporan bukan draft; file tidak bisa dihapus |
| `EXPORT_NOT_FOUND` | 404 | Export ID tidak ada |
| `EXPORT_EXPIRED` | 410 | File export sudah > 3 hari; sudah dihapus |
| `EXPORT_LIMIT_EXCEEDED` | 429 | > 5 export aktif bersamaan |

### 5.7 Audit (FSD-07)

| Code | HTTP | Trigger |
|------|------|---------|
| `AUDIT_NOT_FOUND` | 404 | Dokumen audit tidak ditemukan |
| `AUDIT_ACCESS_FORBIDDEN` | 403 | Bukan SuperAdmin |

### 5.8 CAFRM (FSD-08)

| Code | HTTP | Trigger |
|------|------|---------|
| `CAFRM_MODULE_DISABLED` | 404 | Feature flag CAFRM = disabled |
| `CAFRM_NOT_FOUND` | 404 | Dokumen/mapping tidak ditemukan |
| `CAFRM_COMPANY_INVALID` | 403 | Company tidak di mapping atau tidak ditugaskan ke user |
| `CAFRM_CATEGORY_INVALID` | 400 | Nilai category_code tidak dikenal |
| `CAFRM_CROSS_CATEGORY_FORBIDDEN` | 403 | Role IA mencoba akses kategori AF atau RM |
| `CAFRM_FILE_INVALID` | 400 | Tipe file tidak diizinkan |
| `CAFRM_FILE_SIZE_EXCEEDED` | 413 | File > 100MB |
| `CAFRM_DELETE_FORBIDDEN` | 403 | BOD role atau bukan pemilik dokumen |

---

## Part 6 — Daftar Module Type (Audit Log)

> Format: `EKSAD_TIA.<MODULE>.<ACTION>` — digunakan sebagai nilai `log_activity_type` di audit trail.

| Module | Module Type |
|--------|-------------|
| Login berhasil | `EKSAD_TIA.AUTH.LOGIN` |
| Login gagal | `EKSAD_TIA.AUTH.LOGIN_FAILED` |
| Password reset | `EKSAD_TIA.AUTH.PASSWORD_RESET` |
| Buat laporan | `EKSAD_TIA.SUBMISSION.CREATE` |
| Submit laporan | `EKSAD_TIA.SUBMISSION.SUBMIT` |
| Import Excel | `EKSAD_TIA.SUBMISSION.IMPORT` |
| Approve | `EKSAD_TIA.APPROVAL.APPROVE` |
| Reject | `EKSAD_TIA.APPROVAL.REJECT` |
| Superadmin approve | `EKSAD_TIA.APPROVAL.SUPERADMIN_APPROVE` |
| Buat company | `EKSAD_TIA.MASTERDATA.COMPANY.CREATE` |
| Update user | `EKSAD_TIA.MASTERDATA.USER.UPDATE` |
| Upload lampiran | `EKSAD_TIA.ATTACHMENT.UPLOAD` |
| Export file | `EKSAD_TIA.FILE.EXPORT` |
| Upload CAFRM | `EKSAD_TIA.CAFRM.DOCUMENT.UPLOAD` |
| Download CAFRM | `EKSAD_TIA.CAFRM.DOCUMENT.DOWNLOAD` |

---

## Part 7 — API Endpoint Quick Reference

> **Base URL:** `https://{HOST}/api/v2/`
> Semua endpoint memerlukan `Authorization: Bearer {JWT}` kecuali yang ditandai PUBLIC.

| Method | Path | Auth | FSD |
|--------|------|------|-----|
| `POST` | `/auth/login` | PUBLIC | FSD-01 |
| `POST` | `/auth/refresh` | PUBLIC | FSD-01 |
| `POST` | `/auth/forgot-password` | PUBLIC | FSD-01 |
| `POST` | `/auth/reset-password` | PUBLIC | FSD-01 |
| `POST` | `/auth/logout` | Bearer | FSD-01 |
| `GET` | `/auth/me` | Bearer | FSD-01 |
| `POST` | `/submission/master-budget` | SubCo, Admin | FSD-02 |
| `PATCH` | `/submission/master-budget/{id}/submit` | SubCo, Admin | FSD-02 |
| `POST` | `/submission/monthly-report` | SubCo, Admin | FSD-02 |
| `POST` | `/submission/outlook-pa` | SubCo, Admin | FSD-02 |
| `POST` | `/submission/rolling-outlook` | SubCo, Admin | FSD-02 |
| `POST` | `/submission/*/import-excel` | SubCo, Admin | FSD-02 |
| `PATCH` | `/approval/{reportId}/approve` | TIA, Admin | FSD-03 |
| `PATCH` | `/approval/{reportId}/reject` | TIA, Admin | FSD-03 |
| `GET` | `/approval/pending` | TIA, Admin | FSD-03 |
| `GET` | `/aggregation/ytd` | All roles | FSD-04 |
| `GET` | `/aggregation/mtd` | All roles | FSD-04 |
| `GET` | `/aggregation/summary/pl` | TIA, Admin, Viewer, BOD | FSD-04 |
| `GET` | `/dashboard` | TIA, Admin, Viewer, BOD | FSD-04 |
| `GET` | `/masterdata/companies` | All roles | FSD-05 |
| `POST` | `/masterdata/companies` | Admin | FSD-05 |
| `GET` | `/masterdata/approval-matrix/active` | Admin, TIA | FSD-05 |
| `POST` | `/files/attachments` | SubCo, Admin | FSD-06 |
| `GET` | `/files/attachments/{id}/download` | All roles (scoped) | FSD-06 |
| `POST` | `/files/export/excel` | TIA, SubCo, Admin, Viewer | FSD-06 |
| `GET` | `/audit` | Admin | FSD-07 |
| `GET` | `/audit/{id}` | Admin | FSD-07 |
| `POST` | `/cafrm/documents` | CAFRM roles, Admin | FSD-08 |
| `GET` | `/cafrm/documents` | CAFRM roles, Admin | FSD-08 |
| `GET` | `/cafrm/documents/{id}/download` | CAFRM roles, Admin | FSD-08 |

---

## Part 8 — Feature Flags

| Kode | Default | Mengontrol |
|------|---------|-----------|
| `CORE_REPORTING` | Enabled | MB, MR, OPA, RO submission + approval + aggregation |
| `CAFRM` | **Disabled** | Seluruh endpoint `tia-cafrm-service` |
| `HR` | Disabled | `tia-hr-service` (masa depan) |
| `ROLLING_OUTLOOK` | Enabled | Tipe laporan Rolling Outlook |
| `OPERATING_INDICATOR` | Enabled | Sub-laporan Operating Indicator |

---

## Part 9 — Sub-Report Type Codes

| Kode | Nama Lengkap | Tersedia di |
|------|-------------|-------------|
| `PL` | Profit & Loss | MB, MR, OPA, RO |
| `BS` | Balance Sheet | MB, MR, OPA, RO |
| `TP` | Tax Planning | MB, MR, OPA, RO |
| `FAM` | Fixed Assets Movement | MB, MR, OPA, RO |
| `CF` | Cash Flow | MB, MR, OPA, RO |
| `LOCF` | List of Credit Facilities | MB, MR, OPA, RO |
| `CAT` | Corporate Annual Target | MB, MR, OPA, RO |
| `OI` | Operating Indicator | MR saja |

---

## Part 10 — Glossary

| Term | Definisi |
|------|----------|
| TIA | Triputra Investment Authority — divisi investasi holding company |
| SubCo | Subsidiary Company — perusahaan anak |
| BU | Business Unit — pengelompokan SubCo terkait |
| MB | Master Budget — rencana anggaran tahunan |
| MR | Monthly Report — hasil keuangan aktual bulanan |
| OPA | Outlook PA — outlook tahunan Performance Appraisal |
| RO | Rolling Outlook — forecast rolling kuartalan (Q1, Q2, Q3) |
| YTD | Year-to-Date — kumulatif dari Januari ke bulan target |
| MTD | Month-to-Date — angka bulan tunggal |
| CPSM | Company Performance Summary Monthly |
| P&L | Profit and Loss statement |
| TP | Tax Planning |
| BS | Balance Sheet |
| CF | Cash Flow |
| FAM | Fixed Assets Movement |
| LOCF | List of Credit Facilities |
| CAT | Corporate Annual Target |
| OI | Operating Indicator |
| CAFRM | Corporate Audit, Fraud & Risk Management |
| H+1 | Satu hari setelah batas waktu pengiriman |
| Revision | Versi ulang laporan setelah ditolak; nomor revision bertambah |
| Soft Delete | Penghapusan logis — `deleted_at` di-set; data tidak dihapus fisik |
| Fire-and-forget | Pola async event yang tidak memblokir operasi utama |
| TTL | Time To Live — expiry otomatis dokumen MongoDB |
| Feature Flag | Switch on/off modul platform tanpa deployment ulang |
| Module Type | String identifier audit: `EKSAD_TIA.<MODULE>.<ACTION>` |
