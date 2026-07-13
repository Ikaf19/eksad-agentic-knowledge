# Regulatory & Compliance Reference
# {PROJECT_NAME} — Version {VERSION}

---

## Document Control

| Field | Value |
|---|---|
| **Document Title** | {PROJECT_NAME} — Regulatory & Compliance Reference |
| **Document Type** | Regulatory & Compliance Reference |
| **Project Name** | {PROJECT_NAME} |
| **Module / Domain** | {MODULE_OR_DOMAIN} |
| **Version** | {VERSION} |
| **Status** | 🔴 Draft / 🟡 In Review / 🟢 Approved *(pick one)* |
| **Organization** | PT EKSAD / {BUSINESS_UNIT} |
| **Classification** | Internal — Confidential |
| **Prepared By** | {PREPARED_BY} |
| **Reviewed By** | {REVIEWED_BY} |
| **Approved By** | {APPROVED_BY} |
| **Last Updated** | {DATE} |

> **Related Documents:**
> - `BRD_{PROJECT_CODE}_v{VERSION}.md` — Business Requirements Document
> - `{PROJECT_CODE}_PROJECT_CHARTER.md` — Project Charter

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | {DATE} | {AUTHOR} | Initial draft |
| {VERSION} | {DATE} | {AUTHOR} | {CHANGES} |

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Applicable Laws & Regulations](#2-applicable-laws--regulations)
3. [Data Protection & Privacy](#3-data-protection--privacy)
4. [Industry Standards & Certifications](#4-industry-standards--certifications)
5. [Internal Policies & Guidelines](#5-internal-policies--guidelines)
6. [Compliance Requirements per Business Process](#6-compliance-requirements-per-business-process)
7. [Audit & Reporting Obligations](#7-audit--reporting-obligations)
8. [Non-Compliance Risks](#8-non-compliance-risks)
9. [Compliance Checklist](#9-compliance-checklist)
10. [Glossary](#10-glossary)

---

## 1. Purpose & Scope

> *Jelaskan mengapa dokumen ini dibuat dan peraturan apa saja yang relevan untuk proyek ini. Dokumen ini bersifat referensi — digunakan oleh BA, SA, dan TL untuk memastikan sistem yang dibangun tidak melanggar kewajiban hukum atau kebijakan perusahaan.*

**Tujuan:** Dokumen ini mendokumentasikan seluruh regulasi, standar, dan kebijakan internal yang berlaku untuk proyek **{PROJECT_NAME}**, beserta kewajiban kepatuhan yang harus dipenuhi oleh sistem.

**Cakupan:**
- Modul / domain yang dicakup: {MODULE_OR_DOMAIN}
- Jenis data yang dikelola: {DATA_TYPES — contoh: data pribadi pengguna, data transaksi keuangan, dll.}
- Yurisdiksi yang berlaku: {JURISDICTION — contoh: Indonesia, ASEAN, dll.}

> **Catatan:** Dokumen ini **bukan bagian dari BRD**. Ia adalah referensi terpisah yang mendukung BRD. Setiap kewajiban yang berdampak pada fungsionalitas sistem harus di-cross-reference ke Business Rules (BR) atau Constraints (CON) di BRD.

---

## 2. Applicable Laws & Regulations

> *Daftarkan semua peraturan perundang-undangan yang berlaku. Setiap regulasi diberi ID agar bisa di-trace ke seksi selanjutnya.*

| ID | Nama Regulasi | Nomor / Versi | Otoritas | Relevansi ke Proyek |
|---|---|---|---|---|
| REG-001 | Undang-Undang Perlindungan Data Pribadi | UU No. 27 Tahun 2022 | DPR RI / Kominfo | Pengelolaan data pribadi pengguna |
| REG-002 | {NAMA_REGULASI} | {NOMOR} | {OTORITAS} | {RELEVANSI} |
| REG-003 | {NAMA_REGULASI} | {NOMOR} | {OTORITAS} | {RELEVANSI} |

> **Contoh regulasi yang mungkin berlaku (hapus yang tidak relevan):**
> - UU ITE No. 11/2008 jo. No. 19/2016 — jika ada transaksi elektronik
> - Peraturan OJK — jika menyentuh layanan keuangan
> - Peraturan BI — jika ada pemrosesan pembayaran
> - SNI ISO/IEC 27001 — jika ada persyaratan keamanan informasi formal
> - GDPR — jika ada pengguna dari wilayah Uni Eropa

---

## 3. Data Protection & Privacy

> *Bagian ini khusus untuk kewajiban terkait data pribadi. Wajib diisi jika sistem mengelola data pribadi pengguna dalam bentuk apapun.*

### 3.1 Klasifikasi Data yang Dikelola

| Jenis Data | Kategori | Contoh | Berlaku Regulasi |
|---|---|---|---|
| Data Identitas | 🔴 Sensitif | Nama lengkap, NIK, tanggal lahir | REG-001 (UU PDP) |
| Data Kontak | 🟡 Personal | Email, nomor HP | REG-001 (UU PDP) |
| Data Transaksi | 🟡 Personal | Riwayat pembelian, invoice | REG-001 (UU PDP) |
| Data Teknikal | 🟢 Non-personal | Log sistem, metadata teknis | — |
| {TIPE_DATA} | {KATEGORI} | {CONTOH} | {REGULASI} |

### 3.2 Kewajiban Perlindungan Data

| ID | Kewajiban | Sumber Regulasi | Implementasi yang Diperlukan |
|---|---|---|---|
| DP-001 | Persetujuan pengguna (consent) wajib diperoleh sebelum data pribadi dikumpulkan | UU PDP Pasal 20 | Form persetujuan / checkbox saat registrasi |
| DP-002 | Pengguna berhak mengakses, memperbaiki, dan menghapus data pribadinya | UU PDP Pasal 34 | Fitur "kelola data saya" di profil pengguna |
| DP-003 | Data pribadi tidak boleh disimpan melebihi tujuan pengumpulannya | UU PDP Pasal 26 | Kebijakan retensi data — max {N} tahun |
| DP-004 | Pelanggaran data (data breach) wajib dilaporkan dalam 14 hari | UU PDP Pasal 46 | Prosedur incident response |
| DP-005 | {KEWAJIBAN} | {SUMBER} | {IMPLEMENTASI} |

### 3.3 Data Residency

| Aspek | Ketentuan |
|---|---|
| Lokasi penyimpanan data | {LOKASI — contoh: server di Indonesia / cloud region ap-southeast-1} |
| Transfer data lintas negara | {DIIZINKAN / DILARANG / Perlu persetujuan khusus} |
| Dasar hukum transfer | {DASAR HUKUM jika transfer diizinkan} |

---

## 4. Industry Standards & Certifications

> *Daftarkan standar industri yang relevan. Kosongkan bagian ini jika tidak ada standar formal yang diwajibkan.*

| ID | Standar | Versi | Status | Berlaku Untuk |
|---|---|---|---|---|
| STD-001 | ISO/IEC 27001 — Information Security Management | 2022 | {Wajib / Opsional / Tidak berlaku} | Seluruh sistem |
| STD-002 | OWASP Top 10 | 2021 | Opsional — best practice | Endpoint API |
| STD-003 | {NAMA_STANDAR} | {VERSI} | {STATUS} | {CAKUPAN} |

---

## 5. Internal Policies & Guidelines

> *Kebijakan internal PT EKSAD yang berlaku untuk proyek ini.*

| ID | Nama Kebijakan | Nomor Dokumen | Berlaku Untuk | Catatan |
|---|---|---|---|---|
| POL-001 | Kebijakan Keamanan Informasi EKSAD | {DOC_NO} | Semua proyek | {CATATAN} |
| POL-002 | Kebijakan Retensi Data EKSAD | {DOC_NO} | Semua proyek yang mengelola data | {CATATAN} |
| POL-003 | Kebijakan Penggunaan Cloud & Infrastruktur | {DOC_NO} | Semua proyek berbasis cloud | {CATATAN} |
| POL-004 | {NAMA_KEBIJAKAN} | {DOC_NO} | {CAKUPAN} | {CATATAN} |

---

## 6. Compliance Requirements per Business Process

> *Mapping antara proses bisnis utama dengan kewajiban regulasi yang berlaku. Ini membantu BA dan SA memastikan setiap fitur memenuhi kewajiban yang relevan.*

| Proses Bisnis | Kewajiban yang Berlaku | Sumber (REG / STD / POL) | Catatan |
|---|---|---|---|
| Registrasi / onboarding pengguna | Wajib kumpulkan consent data pribadi | REG-001, DP-001 | Form consent harus eksplisit, bukan pre-checked |
| Login & autentikasi | Wajib gunakan enkripsi; credential tidak boleh disimpan plain-text | POL-001, STD-001 | Ditangani oleh EKSAD Auth Service |
| Penghapusan data pengguna | Wajib proses permintaan dalam {N} hari kerja | REG-001, DP-002 | Soft delete + jadwal purge |
| {PROSES_BISNIS} | {KEWAJIBAN} | {SUMBER} | {CATATAN} |

---

## 7. Audit & Reporting Obligations

> *Kewajiban pelaporan kepada otoritas eksternal atau internal yang harus dipenuhi.*

| ID | Kewajiban | Frekuensi | Pelapor | Penerima Laporan | Sumber |
|---|---|---|---|---|---|
| AUD-001 | Laporan insiden keamanan data (data breach) | Dalam 14 hari sejak kejadian | {PIC} | Kominfo / BSSN | REG-001 |
| AUD-002 | {KEWAJIBAN_PELAPORAN} | {FREKUENSI} | {PELAPOR} | {PENERIMA} | {SUMBER} |

---

## 8. Non-Compliance Risks

> *Apa yang terjadi jika kewajiban regulasi tidak dipenuhi. Digunakan sebagai input untuk Risk Register di BRD.*

| ID | Kewajiban yang Dilanggar | Potensi Sanksi | Tingkat Keparahan |
|---|---|---|---|
| NCR-001 | Tidak mengumpulkan consent data pribadi | Denda administratif hingga 2% dari pendapatan tahunan (UU PDP) | 🔴 Tinggi |
| NCR-002 | Tidak melaporkan data breach dalam 14 hari | Sanksi administratif dari Kominfo | 🔴 Tinggi |
| NCR-003 | {PELANGGARAN} | {SANKSI} | 🟡 Sedang / 🔴 Tinggi |

---

## 9. Compliance Checklist

> *Checklist ini digunakan saat review sebelum go-live. Setiap item harus diverifikasi dan ditandatangani oleh PIC yang bertanggung jawab.*

| # | Item Pemeriksaan | Sumber | Status | Verified By | Tanggal |
|---|---|---|---|---|---|
| 1 | Form consent data pribadi tersedia dan eksplisit sebelum pengumpulan data | REG-001 | ☐ Belum / ✅ OK | | |
| 2 | Fitur akses, koreksi, dan penghapusan data pengguna tersedia | REG-001 | ☐ Belum / ✅ OK | | |
| 3 | Prosedur pelaporan data breach terdokumentasi dan diuji | REG-001 | ☐ Belum / ✅ OK | | |
| 4 | Semua credential dan data sensitif dienkripsi at rest dan in transit | POL-001 | ☐ Belum / ✅ OK | | |
| 5 | Kebijakan retensi data diimplementasikan (data dihapus setelah masa retensi) | POL-002 | ☐ Belum / ✅ OK | | |
| 6 | {ITEM_PEMERIKSAAN} | {SUMBER} | ☐ Belum / ✅ OK | | |

---

## 10. Glossary

| Istilah | Definisi |
|---|---|
| Data Pribadi | Setiap data yang dapat mengidentifikasi seseorang secara langsung atau tidak langsung — mencakup nama, NIK, email, nomor HP, dll. (UU PDP) |
| Data Sensitif | Kategori khusus data pribadi yang memerlukan perlindungan lebih tinggi — mencakup data kesehatan, agama, biometrik, keuangan pribadi, dll. |
| Consent | Persetujuan yang diberikan secara sadar, eksplisit, dan bebas oleh subjek data sebelum data pribadinya dikumpulkan atau diproses |
| Data Breach | Insiden keamanan yang menyebabkan data pribadi bocor, diakses, dimodifikasi, atau dihancurkan tanpa otorisasi |
| Data Residency | Kewajiban menyimpan data di wilayah atau negara tertentu sesuai regulasi yang berlaku |
| Retention Period | Jangka waktu maksimum penyimpanan data sebelum wajib dihapus atau dianonimkan |
| {ISTILAH} | {DEFINISI} |
