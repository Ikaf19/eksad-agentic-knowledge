# EKSAD Developer GPT — Chat Starters

> Pick the **Top 4** for the GPT UI. Full library below.

---

## 🟢 Recommended Top 4

```
Implementasikan BaseRepository untuk entity [nama entity] dengan ID type Long
```
```
Buatkan full entity class untuk [nama entity] dengan fields: [list fields]
```
```
Buatkan unit test untuk service method [nama method] — happy path + failure
```
```
Flyway DDL migration untuk tabel [nama tabel] dengan columns: [list]
```

---

## 📋 Full Developer Starter Library

### Entity Implementation
```
Buatkan full entity class [nama entity] extends BaseEntity dengan fields: [list fields dan types]. Table name: [{table_name}].
```
```
Buatkan DTO classes untuk entity [nama entity]: CreateDTO, UpdateDTO, dan ResponseDTO.
```
```
Buatkan MapStruct mapper untuk [nama entity] antara [{Entity}Entity] dan [{Entity}DTO].
```

### Repository Implementation
```
Implementasikan BaseRepository untuk entity [nama entity]. Operations: CREATE, UPDATE, DELETE[, tambah: SUBMIT/APPROVE/REJECT jika ada]. Module: [nama module].
```
```
Bagaimana cara implementasi commandFlow untuk action APPROVE pada entity [nama entity]? Guard: [kondisi yang harus true sebelum approve].
```
```
Buatkan custom query di repository untuk mencari [nama entity] berdasarkan [filter fields], dengan filter tenant_id dan deleted_at secara otomatis.
```

### Service & Resource
```
Buatkan service class untuk [nama entity] — CREATE, UPDATE, DELETE, findById, dan findAll dengan pagination.
```
```
Buatkan REST resource class untuk [nama entity] dengan endpoints: POST, GET/{id}, GET (list), PUT/{id}, DELETE/{id}. Roles: [list roles].
```
```
Bagaimana cara implementasi approval endpoint PATCH /{id}/approve dan PATCH /{id}/reject pada resource class?
```

### Module Type & Constants
```
Buatkan ModuleType interface constants untuk service [nama service] dengan modules: [list modules] dan actions per module: [list actions].
```

### Flyway DDL
```
Buatkan Flyway DDL file V1__init_{domain}.sql untuk tabel [nama tabel] dengan columns: [list]. Sertakan BaseEntity columns, tenant_id, dan indexes.
```
```
Buatkan Flyway DDL untuk menambahkan kolom [nama kolom] ke tabel [nama tabel]. Ini migration ke-[N].
```

### Configuration
```
Buatkan application.properties lengkap untuk service baru [nama service] yang connect ke PostgreSQL, RabbitMQ, dan validasi JWT.
```
```
Buatkan pom.xml untuk service baru [nama service] yang extends eksad-parent. Dependencies tambahan: [list].
```

### Testing
```
Buatkan unit test lengkap untuk [nama service] — test CREATE, UPDATE, DELETE, dan semua failure scenarios. Mock repository-nya.
```
```
Buatkan integration test @QuarkusTest untuk endpoint [path]. Scenarios: happy path, 401, 403, 422.
```
```
Bagaimana cara mock UserContext di integration test agar mengembalikan tenant "test-tenant" dan user "test-user"?
```
```
Bagaimana cara test reactive Uni yang diharapkan fail dengan ValidationException?
```

### Reactive Patterns
```
Bagaimana cara chain dua Uni secara sequential? Pertama cek entity A, kemudian update entity B berdasarkan hasilnya.
```
```
Bagaimana cara handle kasus entity tidak ditemukan (findById returns null) dengan cara yang benar di reactive chain?
```
```
Bagaimana cara run dua operasi Uni secara parallel dan combine hasilnya?
```

### Spring Boot (if applicable)
```
Ini project Spring Boot imperative. Implementasikan service class untuk [nama entity] — CREATE, UPDATE, DELETE dengan audit trail menggunakan @Async RabbitTemplate.
```
```
Ini project Spring Boot. Buatkan UserContext class yang baca eksad_tenant_id dari Spring Security JWT.
```
```
Ini project Spring Boot. Konversi repository berikut dari Quarkus BaseRepository ke Spring Boot pattern: [paste kode].
```

### Debugging
```
Kode ini throw error: [paste stack trace atau error message]. Tolong bantu debug dan fix.
```
```
Kenapa Uni ini selalu return null padahal data ada di database? [paste kode].
```
```
@ReactiveTransactional tidak bekerja — transaction tidak di-commit. Kode: [paste].
```

## 💡 Tips for Dev GPT

- **Always paste your TSD** — the richer the design context, the more accurate the generated code
- **Say your entity fields** — "fields: userId String, amount BigDecimal, status String" gives complete code
- **Ask for tests immediately** — after getting a service class, say "now write the unit test for this"
- **Mention Spring Boot if applicable** — by default GPT generates Quarkus; say "Spring Boot" to switch
- **Ask for the full class** — say "full class with all imports" to get copy-paste-ready code

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
