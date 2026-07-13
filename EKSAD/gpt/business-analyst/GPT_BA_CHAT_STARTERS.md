# EKSAD Business Analyst GPT — Chat Starters

> **How to use this file:**
> In your BA Custom GPT editor → **"Conversation starters"** field.
> Pick the **Top 4** for the GPT UI. Full library below for reference.

---

## 🟢 Recommended Top 4 (Business Analyst Daily Use)

```
Bantu saya tulis BRD untuk service baru: [nama dan tujuan service]
```
```
Draft FSD untuk modul [nama modul] — saya akan jelaskan alurnya
```
```
Buatkan user stories dan acceptance criteria untuk fitur [nama fitur]
```
```
Identifikasi business rules dari alur berikut: [deskripsi proses bisnis]
```

---

## 📋 Full BA Starter Library

### BRD Writing

**Start a Full BRD from Scratch**
```
Saya ingin membuat BRD baru. Nama systemnya: [nama]. Tolong tanyakan saya semua yang kamu butuhkan sebelum mulai menulis.
```

**Write BRD Executive Summary**
```
Bantu saya tulis Executive Summary untuk BRD ini. Sistem ini adalah: [deskripsi singkat].
```

**Define Problem Statement**
```
Bantu saya tulis Problem Statement untuk BRD. Masalah bisnis yang ada sekarang adalah: [jelaskan situasi saat ini dan pain pointnya].
```

**Define Objectives**
```
Bantu saya tulis objectives SMART untuk project ini. Tujuan bisnis utamanya adalah: [deskripsi tujuan].
```

**Define Scope**
```
Bantu saya definisikan In Scope dan Out of Scope untuk project [nama project]. Fitur yang direncanakan: [list fitur].
```

**Stakeholder Analysis**
```
Bantu saya buat stakeholder table untuk project ini. Tim yang terlibat: [list tim/role].
```

**Write Functional Requirements**
```
Bantu saya tulis functional requirements untuk modul [nama modul]. Alur bisnisnya: [deskripsi alur].
```

**Write Non-Functional Requirements**
```
Bantu saya tulis non-functional requirements standar EKSAD untuk project [nama project].
```

**Write Business Rules**
```
Dari alur bisnis berikut, tolong identifikasi dan format semua business rules dengan ID BR-{N}: [deskripsi alur].
```

---

### FSD Writing

**Start a Full FSD**
```
Saya ingin membuat FSD dari BRD berikut. Tolong tanyakan apa yang kamu butuhkan: [paste BRD atau rangkumannya].
```

**Write User Stories for a Module**
```
Buatkan user stories format US-{MODULE}-{N} untuk modul [nama modul]. Actors yang terlibat: [list actors]. Fungsi utama: [deskripsi].
```

**Write Acceptance Criteria**
```
Buatkan acceptance criteria yang testable untuk user story ini: [paste user story].
```

**Document an Approval Workflow**
```
Bantu saya dokumentasikan approval workflow untuk [nama entity/dokumen]. Prosesnya: [jelaskan siapa yang submit, siapa yang approve, berapa level, apa yang terjadi kalau reject].
```

**Document a State Machine**
```
Buatkan state machine diagram dan tabel transisi untuk entity [nama entity]. Status yang ada: [list status]. Siapa yang bisa trigger tiap transisi: [deskripsi].
```

**Define Validation Rules**
```
Buatkan field validation rules table untuk form [nama form/module]. Fields yang ada: [list field dan tipe datanya].
```

**Write Error Scenarios**
```
Tolong dokumentasikan semua error scenarios dan pesan error untuk modul [nama modul]. Happy path-nya: [deskripsi].
```

---

### Review & Improvement

**Review Existing BRD**
```
Tolong review BRD berikut — cari gaps, ambiguous requirements, missing business rules, dan incomplete scope: [paste BRD].
```

**Review Existing FSD**
```
Tolong review FSD berikut — cari user stories yang tidak testable, state machine yang tidak lengkap, dan validation rules yang ambigu: [paste FSD].
```

**Clarify Ambiguous Requirement**
```
Requirement ini ambigu menurut saya: "[paste requirement]". Tolong bantu saya tulis ulang menjadi lebih spesifik dan testable.
```

**Find Missing Business Rules**
```
Dari FSD modul [nama modul] ini, apakah ada business rules yang belum saya dokumentasikan? [paste modul section].
```

---

### Specific Scenarios

**Multi-Tenant Consideration**
```
Fitur [nama fitur] ini perlu mempertimbangkan multi-tenancy. Tolong bantu saya tulis business rules untuk tenant isolation pada modul ini.
```

**Audit Trail Requirement**
```
Tolong bantu saya tulis functional requirements untuk audit trail di modul [nama modul]. Aksi apa saja yang harus di-log?
```

**Role-Based Access**
```
Tolong buatkan access matrix untuk modul [nama modul]. Roles yang ada: [list roles]. Fitur yang ada: [list fitur].
```

**Report / Dashboard Requirement**
```
Tolong bantu saya tulis requirements untuk fitur laporan/dashboard [nama]. Data yang ditampilkan: [deskripsi]. User yang mengakses: [roles].
```

---

## 💡 Tips for BA GPT

- **Always describe the "why"** — the more business context you give, the better the output
- **One module at a time** — when writing FSD, do one module per conversation for best quality
- **Paste your drafts** — say "review this" to get gap analysis, not just generation
- **Ask for a checklist** — say "what information do I still need to complete this BRD?" anytime
- **Use "Bahasa Indonesia"** — this GPT is fully bilingual; switch any time

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
