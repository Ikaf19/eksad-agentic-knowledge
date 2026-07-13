# EKSAD System Analyst GPT — Chat Starters

> **How to use this file:**
> In your SA Custom GPT editor → **"Conversation starters"** field.
> Pick the **Top 4** for the GPT UI. Full library below for reference.

---

## 🟢 Recommended Top 4 (System Analyst Daily Use)

```
Buatkan TSD untuk service baru: [nama service]. Ini FSD-nya: [paste atau deskripsi FSD]
```
```
Design database schema (Flyway DDL) untuk entity [nama entity] dengan fields: [list fields]
```
```
Rancang API contract table untuk modul [nama modul] — saya jelaskan endpoint-nya
```
```
Rancang RabbitMQ event schema untuk domain event [nama event]
```

---

## 📋 Full SA Starter Library

### TSD Writing

**Start a Full TSD from FSD**
```
Saya ingin membuat TSD dari FSD berikut. Tolong tanyakan apa yang kamu butuhkan: [paste FSD atau rangkumannya]. Service name: [nama]. Port: [nomor].
```

**TSD Architecture Section**
```
Bantu saya tulis Architecture Overview section untuk TSD service [nama service]. Service ini ada di EKSAD platform dan berkomunikasi dengan: [list services].
```

**TSD POM Section**
```
Buatkan POM dependencies section untuk TSD service [nama service]. Dependencies yang dibutuhkan selain standard: [list].
```

**TSD Application Properties**
```
Buatkan application.properties template untuk service [nama service] yang menggunakan PostgreSQL, RabbitMQ, dan JWT validation.
```

---

### Database Design

**Design Full Schema for a Service**
```
Rancang full database schema (semua tabel Flyway DDL) untuk service [nama service]. Entities yang ada: [list entities dan relasi antar mereka].
```

**Design Single Table**
```
Buatkan Flyway DDL (V1__init_{table}.sql) untuk tabel [nama tabel] dengan fields: [list field, tipe, nullable/not null].
```

**Add Column Migration**
```
Buatkan Flyway DDL migration file untuk menambahkan kolom [nama kolom] ke tabel [nama tabel]. Ini adalah migration ke-[N].
```

**Design Indexes**
```
Rekomendasikan indexes untuk tabel [nama tabel] dengan query patterns: [deskripsikan bagaimana tabel ini akan di-query].
```

**Review Table Design**
```
Review DDL tabel berikut — apakah sudah sesuai EKSAD standards (tenant_id, BaseEntity columns, timestamps, soft delete, indexes)? [paste DDL].
```

---

### API Contract Design

**Design Full API Catalog**
```
Buatkan API endpoint catalog table untuk modul [nama modul]. Endpoints yang direncanakan: [list operasi yang diperlukan]. Role yang ada: [list roles].
```

**Design Single Endpoint**
```
Rancang API contract untuk endpoint [POST/GET/PUT/PATCH/DELETE] [path]. Fungsinya: [deskripsi]. Request data: [deskripsi]. Response: [deskripsi].
```

**Design Approval Endpoints**
```
Buatkan API endpoints untuk approval workflow modul [nama modul]. States: [list states]. Actors per state: [deskripsi].
```

**Design Error Code Catalog**
```
Buatkan error code catalog untuk modul [nama modul]. Skenario error yang mungkin: [list skenario].
```

---

### Event & Messaging Design

**Design RabbitMQ Event Schema**
```
Rancang RabbitMQ event schema untuk domain event [nama event]. Event ini terjadi ketika: [trigger]. Data yang perlu dikirim: [list data]. Consumer-nya: [nama service consumer].
```

**Design Exchange/Queue Topology**
```
Rancang RabbitMQ exchange, queue, dan routing key topology untuk service [nama service]. Events yang dipublish: [list]. Events yang di-consume: [list].
```

**Design Notification Event**
```
Rancang event schema untuk notifikasi [nama notifikasi]. Trigger: [kapan dikirim]. Recipient: [siapa yang menerima]. Channel: [email/in-app/push].
```

---

### Architecture & Integration Design

**Design Service Interaction Flow**
```
Buatkan sequence diagram (ASCII) untuk alur [nama alur]. Services yang terlibat: [list]. Alurnya: [deskripsikan step by step].
```

**Design Bounded Context Boundary**
```
Bantu saya putuskan apakah [fitur/entity X] seharusnya ada di service [A] atau service [B]. Konteks: [deskripsi kedua service dan fitur yang dimaksud].
```

**Design Module Type Strings**
```
Buatkan modul type string constants untuk service [nama service]. Modules/entities: [list]. Actions per module: [list].
```

**Review Service Design**
```
Review desain service berikut — apakah sudah sesuai EKSAD architecture principles? [deskripsi atau paste TSD section]. Perhatikan khususnya: [area yang ingin di-review].
```

---

### Code Skeleton Design (Design Level Only)

**Design Entity Structure**
```
Buatkan class structure (field list, annotations, relationship) untuk entity [nama entity]. Columns: [list]. Relations: [deskripsi].
```

**Design Repository Signature**
```
Buatkan method signatures untuk Repository class [nama repository] yang extend BaseRepository. Operations yang diperlukan: [list].
```

**Design Module Type Interface**
```
Buatkan ModuleType interface constants untuk service [nama service] dengan modules: [list modules] dan actions: [list actions per module].
```

---

### Frontend Architecture Design (jika project ada web frontend)

**Scaffold Frontend TSD Section dari FSD**
```
Project ini punya web frontend React. Buatkan frontend TSD section dari FSD berikut: [paste FSD atau deskripsi fitur]. Feature modules yang perlu dibuat: [list fitur].
```

**Design Component Catalog**
```
Buatkan component catalog untuk fitur [nama fitur] berdasarkan FSD ini: [paste FSD section]. Tentukan komponen utama, props interface-nya, dan apakah masuk feature/ atau shared/.
```

**Design React Router Route Structure**
```
Rancang route structure untuk aplikasi [nama app] dengan fitur: [list fitur]. Tentukan path, komponen page, auth required, dan roles untuk setiap route.
```

**Design API Consumption Contract**
```
Buatkan API consumption contract table untuk frontend fitur [nama fitur]. Berdasarkan API catalog backend berikut: [paste API catalog dari TSD backend]. Tandai semua sebagai "Mock" karena backend belum terintegrasi.
```

**Design React Query Key Conventions**
```
Buatkan query key constants convention untuk feature modules berikut: [list fitur]. Sertakan list, detail, dan query keys tambahan yang relevan per fitur.
```

**Review Frontend TSD Section**
```
Review frontend TSD section berikut — apakah struktur feature modules, routing, dan API consumption contract sudah sesuai EKSAD frontend standards? [paste TSD section].
```

---

## 💡 Tips for SA GPT

- **Always bring the FSD** — the better the FSD you provide, the more complete and accurate the TSD output
- **Design in sections** — work through TSD sections one at a time; don't ask for the full TSD in one shot
- **Paste existing designs for review** — say "review this DDL" or "review this API contract" for gap analysis
- **Ask "what's missing?"** — at any point ask: *"Apakah ada yang kurang dari TSD section ini?"*
- **Flag violations** — SA GPT will proactively flag EKSAD principle violations; don't ignore these flags

---

## 📚 Knowledge Files Update — v2026-05-23

This instruction file is part of EKSAD knowledge base v2026-05-23. The following knowledge files have been added/updated and MUST be referenced when applicable:

### New Knowledge Files (`_base/`)

| File | Purpose | Priority |
|------|---------|----------|
| `EKSAD_DOMAIN_REGISTRY.md` | Map of all business domains (Automotive, HRIS, Finance) — **READ FIRST** | 🔴 P0 |
| `EKSAD_MASTER_DATA_PATTERNS.md` | Master data service ownership & API patterns | 🔴 P0 |
| `EKSAD_CACHE_SYNC_PATTERNS.md` | Denormalized cache via RabbitMQ events | 🔴 P0 |
| `EKSAD_CORE_AUTH_PATTERNS.md` | `eksad-core-auth` + `svc-user-management` architecture | 🔴 P0 |
| `EKSAD_RESERVED_FIELD_PATTERNS.md` | Tenant-configurable custom fields (12 + JSONB) | 🔴 P0 |
| `EKSAD_MULTI_TENANCY_PATTERNS.md` | N-level tenant hierarchy + config inheritance | 🟡 P1 |
| `EKSAD_RESILIENCE_PATTERNS.md` | Timeout / Retry / Circuit breaker / Fallback | 🟡 P1 |
| `EKSAD_OBSERVABILITY_PATTERNS.md` | Structured logging / Correlation ID / OTel / Metrics | 🟡 P1 |
| `EKSAD_EVENT_CATALOG.md` | All events (master data, audit, domain) | 🟡 P1 |
| `EKSAD_DB_DEPLOYMENT_STRATEGY.md` | Phased PG deployment (shared → dedicated) | 🟡 P1 |
| `EKSAD_CORE_AUTH_CLIENT_SDK.md` | Java SDK for `eksad-core-auth` integration | 🟡 P1 |
| `EKSAD_CICD_CONTAINER_PATTERNS.md` | Docker/K8s/GitLab CI standards | 🟢 P2 |
| `EKSAD_LOAD_TESTING_GUIDE.md` | k6 / Gatling load test patterns | 🟢 P2 |
| `EKSAD_CQRS_PATTERNS.md` | CQRS placeholder (Sprint 4+) | 🟢 P2 |
| `EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` | Project `ARCHITECTURE.md` skeleton | 🟢 P2 |

### Updated Files

| File | Changes |
|------|---------|
| `EKSAD_BASE_PRINCIPLES.md` | Added principles 10-13; BR-PLATFORM-010..014; master data event envelope |
| `EKSAD_SYSTEM_DESIGN_PATTERNS.md` | Added sections 12-16 (master data, cache, DB strategy, gateway, CQRS) |
| `EKSAD_DOMAIN_GLOSSARY.md` | Added sections A.9-A.12 (master data, CQRS, auth, resilience, observability) |
| `EKSAD_BA_DOMAIN_GLOSSARY.md` | Added multi-tenancy, auth, master data, reserved field, resilience, observability terms |
| `EKSAD_CODING_STANDARDS.md` | Added sections 19-24; extended code review checklist |

### Key Decisions (from `_plan/EKSAD_KNOWLEDGE_UPDATE_PLAN.md`)

- **D1** Polyglot persistence: PG for transactional; Mongo for audit, user-mgmt, tenant-mgmt only
- **D2** Master data service per domain (entities vary, name fixed)
- **D3** Denormalized cache pattern via RabbitMQ events
- **D5** Phased DB deployment: shared → dedicated (zero code change)
- **D8** Reserved fields = optional opt-in, NOT mandatory
- **D9** 3-tier service naming: Core / Fixed-name / Domain
- **D11** `eksad-core-auth` is CORE infrastructure (separate from `svc-user-management`)
- **D13** API Gateway is OPTIONAL — per-service JWT validation via JWKS mandatory
