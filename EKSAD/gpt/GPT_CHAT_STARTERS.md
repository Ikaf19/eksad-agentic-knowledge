# EKSAD GPT — Chat Starters

> **How to use this file:**
> In your Custom GPT editor, go to **"Conversation starters"** and paste each starter below (one per field, max 4 shown at a time).
> Choose the 4 most relevant for your team's daily use. The full list is here for reference.

---

## 🟢 Recommended Top 4 (General / BA Focus)

```
Buatkan BRD untuk microservice baru: [nama service dan tujuannya]
```
```
Draft FSD dengan user stories dan API contract untuk modul [nama modul]
```
```
Review entity class ini — apakah sudah sesuai EKSAD standards?
```
```
Jelaskan bagaimana auto audit trail CrudFlows bekerja di EKSAD
```

---

## 📋 Full Starter Library

### Business Analysis & Documentation

**BRD Writing**
```
Buatkan BRD untuk microservice baru: [nama service]. Tujuannya adalah [deskripsi singkat].
```

**FSD Writing**
```
Draft FSD lengkap untuk modul [nama modul], termasuk user stories, business rules, dan API endpoint catalog.
```

**User Stories**
```
Tulis user stories format US-{MODULE}-{N} untuk fitur [nama fitur]. Actors: [daftar actor].
```

**Business Rules**
```
Identifikasi dan tulis business rules format BR-{N} untuk alur [nama alur bisnis].
```

**Approval Workflow**
```
Rancang approval workflow state machine untuk modul [nama modul]. States yang mungkin: [list states].
```

---

### Technical Design & Architecture

**TSD Writing**
```
Buatkan TSD skeleton untuk service baru bernama [nama service]. Stack: Quarkus 3.30.6, PostgreSQL, RabbitMQ.
```

**Database Schema**
```
Buatkan Flyway DDL (V1__init.sql) untuk entity [nama entity] dengan fields: [list fields]. Sertakan BaseEntity columns.
```

**API Contract**
```
Tulis API contract table untuk endpoint [HTTP method] [path]. Request: [deskripsi]. Response: [deskripsi].
```

**RabbitMQ Event Schema**
```
Rancang RabbitMQ event schema untuk domain event [nama event]. Payload data: [deskripsi data].
```

**JWT Design**
```
Rancang JWT payload structure untuk service [nama service]. User roles: [list roles]. Permissions needed: [list permissions].
```

---

### Code Review & Standards

**Entity Review**
```
Review entity class ini apakah sudah sesuai EKSAD standards (BaseEntity, tenant_id, Long timestamp, soft delete):

[paste your entity class here]
```

**Repository Review**
```
Review implementasi BaseRepository ini — apakah createFlow/updateFlow/deleteFlow sudah benar?

[paste your repository class here]
```

**application.properties Review**
```
Review application.properties ini — apakah sudah sesuai EKSAD conventions? Service name: [nama service].

[paste your application.properties here]
```

---

### Learning & Explanation

**Architecture Pattern**
```
Jelaskan pola multi-tenant dengan tenant_id yang dipakai EKSAD, beserta contoh implementasi di entity dan query.
```

**Audit Trail Flow**
```
Jelaskan end-to-end bagaimana auto audit trail bekerja dari CRUD di service sampai tersimpan di MongoDB.
```

**Module Type Convention**
```
Jelaskan konvensi penamaan logActivityModuleType di EKSAD dan berikan 5 contoh untuk service [nama service].
```

**BaseRepository Usage**
```
Tunjukkan cara mengimplementasikan BaseRepository dari eksad-core-common untuk entity [nama entity] dengan ID type [Long/UUID/String].
```

**Reactive Programming**
```
Jelaskan perbedaan Uni dan Multi di Mutiny, dan kapan harus pakai masing-masing di EKSAD service.
```

---

## 🔵 Team-Specific Starters (Add When Creating Team GPT)

> When you create a team-specific Custom GPT (e.g., TIA Reporting GPT, HR GPT),
> replace the top 4 starters with domain-specific ones like these:

**TIA Reporting Team**
```
Buatkan BRD untuk siklus laporan [Master Budget / Monthly Report / Outlook PA / Rolling Outlook].
```
```
Rancang approval engine untuk submission [jenis laporan] dengan tenant [nama tenant].
```

**Finance/Consolidation Team**
```
Tulis business rules untuk kalkulasi YTD [jenis metrik keuangan].
```
```
Rancang data model untuk konsolidasi laporan keuangan dari [N] anak perusahaan.
```
