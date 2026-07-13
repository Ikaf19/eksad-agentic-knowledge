# TIA Reporting v2 — SA Domain Knowledge (Updated)
# For: System Analyst GPT (TIA Team Extension)

**Version:** 2.0
**Date:** 27 April 2026
**Owner:** EKSAD Platform Team / TIA Project
**Audience:** SA GPT (upload sebagai additional knowledge file bersama SA base files)
**Based on:** `BRD — TIA Reporting System v2 (Client).md` · TSD-01 s/d TSD-08

> File ini meng-extend **SA GPT** dengan TIA-specific technical context — tanggung jawab service,
> DB schema ownership, RabbitMQ event contracts, API routing, dan key design decisions.
> Untuk business rules dan domain terminology, lihat BA variant (`business-analyst/teams/tia/TIA_BA_DOMAIN_KNOWLEDGE_v2.md`).
> **v2.0:** Update dari v1.0 — disesuaikan dengan TSD final (TSD-01 s/d TSD-08).

---

## Part 1 — System Identity

| Item | Value |
|------|-------|
| System Name | `tia-reporting-v2` |
| Group ID | `com.eksad.tia` |
| Quarkus Version | `3.8.0` |
| Java Version | `21` (GraalVM JDK 21 untuk formula engine) |
| Shared Library | `eksad-core-common` (`com.eksad.core:eksad-core-common:1.0.0-SNAPSHOT`) |
| Parent POM | `com.eksad.tia:tia-parent:2.0.0-SNAPSHOT` |

---

## Part 2 — Microservice Registry

| Service | Port | DB Schema | Responsibility |
|---------|------|-----------|----------------|
| `tia-gateway` | 8080 | — | JWT filter (RS256), routing, rate limiting, CORS |
| `tia-auth-service` | 8081 | `auth` | JWT issuance, login, refresh, password reset |
| `tia-master-data-service` | 8082 | `masterdata` | All config entities: company, user, role, item report, approval matrix, feature flags, mail templates |
| `tia-submission-service` | 8083 | `submission` | Report headers + detail values (MB/MR/OPA/RO), Excel import, attachments |
| `tia-approval-service` | 8084 | `approval` | Unified approval engine — AND/OR multi-level for all 4 report types |
| `tia-aggregation-service` | 8085 | `aggregation` | YTD/MTD/CPSM/Historical analytics, ratio formula engine (GraalVM JS) |
| `tia-notification-service` | 8086 | `notification` | Scheduled email reminders, approval alerts via RabbitMQ |
| `tia-file-service` | 8087 | `filestore` | Attachment upload/download, Excel/ZIP export, 3-day TTL cleanup |
| `tia-audit-service` | 8088 | MongoDB `tia_audit` | Append-only audit trail consumer (RabbitMQ → MongoDB) |
| `tia-cafrm-service` | 8089 | `cafrm` | Document vault — Internal Audit, Anti Fraud, Risk Management |

---

## Part 3 — RabbitMQ Topology

### 3.1 Exchange Registry

| Exchange | Type | Publisher | Consumers |
|----------|------|-----------|-----------|
| `exc-log-activity` | direct | Semua service (via `BaseRepository`) | `tia-audit-service` |
| `exc-tia-approval` | direct | `tia-submission-service` | `tia-approval-service` |
| `exc-tia-submission` | direct | `tia-approval-service` | `tia-submission-service`, `tia-aggregation-service` |
| `exc-tia-aggregation` | direct | `tia-approval-service` | `tia-aggregation-service` |
| `exc-tia-notification` | direct | `tia-approval-service`, `tia-auth-service` | `tia-notification-service` |

### 3.2 Queue Registry

| Queue | Routing Key | Consumer Service |
|-------|-------------|-----------------|
| `q-log-activity-eksad` | `r.q-log-activity-eksad` | `tia-audit-service` |
| `q-approval-start-approval` | `r.q-approval-start-approval` | `tia-approval-service` |
| `q-status-update-submission` | `r.q-status-update-submission` | `tia-submission-service` |
| `q-aggregation-recalc` | `r.q-aggregation-recalc` | `tia-aggregation-service` |
| `q-approval-notification` | `r.q-approval-notification` | `tia-notification-service` |
| `q-password-reset-notification` | `r.q-password-reset-notification` | `tia-notification-service` |

### 3.3 Standard Event Envelope

```json
{
  "eventType"  : "EKSAD_TIA.<MODULE>.<ACTION>",
  "eventId"    : "{uuid-v4}",
  "tenantId"   : "{tenant_id}",
  "actorId"    : "{user_id}",
  "actorName"  : "{username}",
  "occurredAt" : 1745280000000,
  "serviceId"  : "tia-{service-name}",
  "payload"    : { ... }
}
```

### 3.4 Key Event Types

| Event Type | Publisher | Trigger |
|-----------|-----------|---------|
| `EKSAD_TIA.SUBMISSION.SUBMIT` | submission | User submit laporan |
| `EKSAD_TIA.APPROVAL.APPROVED` | approval | Approval final selesai |
| `EKSAD_TIA.APPROVAL.REJECTED` | approval | Approval ditolak |
| `EKSAD_TIA.APPROVAL.APPROVE_STARTED` | approval | Approval diinisiasi |
| `EKSAD_TIA.AUTH.PASSWORD_RESET_REQUEST` | auth | Request reset password |

---

## Part 4 — Database Schema Ownership

### 4.1 PostgreSQL Schemas

| Service | Schema | Key Tables |
|---------|--------|-----------|
| `tia-auth-service` | `auth` | `auth_user`, `auth_refresh_token`, `auth_password_reset` |
| `tia-master-data-service` | `masterdata` | `mst_company`, `mst_user`, `mst_role`, `trx_role_privileges`, `mst_item_report`, `mst_setting`, `mst_holiday`, `mst_approval_type`, `mst_approval_matrix`, `mst_tenant`, `mst_feature_flag`, `mst_mail_template` |
| `tia-submission-service` | `submission` | `sub_master_budget`, `sub_mb_pl_value`, `sub_mb_tp_value`, `sub_monthly_report`, `sub_mr_pl_value`, `sub_mr_tp_value`, `sub_mr_cat_value`, `sub_mr_locf_value`, `sub_outlook_pa`, `sub_rolling_outlook`, `sub_ro_pl_value`, `sub_attachment` |
| `tia-approval-service` | `approval` | `tia_approval`, `tia_approval_detail`, `tia_approval_history` |
| `tia-aggregation-service` | `aggregation` | `agg_ytd_cache`, `agg_ratio_result`, `agg_summary_pl`, `agg_summary_bs`, `agg_summary_cf` |
| `tia-notification-service` | `notification` | `notif_reminder_history`, `notif_email_log` |
| `tia-file-service` | `filestore` | `file_attachment`, `file_export`, `file_export_detail` |
| `tia-cafrm-service` | `cafrm` | `cafrm_category`, `cafrm_company_mapping`, `cafrm_document` |

### 4.2 MongoDB

| Service | Database | Collection | TTL |
|---------|----------|-----------|-----|
| `tia-audit-service` | `tia_audit` | `audit_trail` | 730 hari (2 tahun) |

### 4.3 Common Column Pattern (Semua Tabel PostgreSQL)

```sql
tenant_id   VARCHAR(100)  NOT NULL,
deleted_at  BIGINT        NULL,     -- epoch ms; NULL = active
deleted_by  VARCHAR(100)  NULL,
created_at  BIGINT        NOT NULL, -- epoch ms
created_by  VARCHAR(100)  NOT NULL,
updated_at  BIGINT        NULL,
updated_by  VARCHAR(100)  NULL
```

> **Tidak ada kolom `TIMESTAMP WITH TIME ZONE`** — semua timestamp adalah `BIGINT` epoch milliseconds.

### 4.4 Key Schema Design Decisions

| Decision | Rationale |
|----------|-----------|
| `NUMERIC(20,4)` untuk semua nilai keuangan | Menggantikan TEXT yang ada di v1; eliminasi cast runtime dan aggregation failure |
| `tia_approval` satu tabel dengan kolom `report_type` polimorfik | Menggantikan 16 tabel (4 tipe × 4 tabel) di v1 |
| `sub_mr_*_value` split 4 tabel domain | Normalisasi mega-entity 40+ kolom dari v1 |
| `sub_ro_pl_value` dengan 12 kolom bulan bernama | YTD RO = sum(jan+feb+...+dec) |

---

## Part 5 — JWT Design

### 5.1 Payload

```json
{
  "iss"        : "tia-auth-service",
  "sub"        : "{username}",
  "jti"        : "{uuid-v4}",
  "iat"        : 1745280000000,
  "exp"        : 1745366400000,
  "groups"     : ["ROLE_TIA"],
  "tenant_id"  : "{tenant_id}",
  "user_id"    : "{user_id}",
  "role"       : "ROLE_TIA",
  "company_ids": ["{id1}", "{id2}"],
  "permissions": ["SUBMISSION_READ", "SUBMISSION_WRITE"]
}
```

> **`groups`** = SmallRye JWT standard claim untuk `@RolesAllowed`.
> Custom claims: `tenant_id`, `user_id`, `role`, `company_ids`, `permissions`.

### 5.2 Key Pair

- **Private key (PKCS8)**: hanya di `tia-auth-service`; inject via env var
- **Public key**: di-distribute ke semua service lain sebagai `META-INF/resources/tia-public-key.pem`
- Algorithm: RS256, 4096-bit

---

## Part 6 — Approval Engine Technical Design

### 6.1 Polimorfisme

Satu engine untuk semua tipe laporan. Kolom `report_type VARCHAR(10)` di `tia_approval` menentukan tipe.

### 6.2 State Machine

```
submit → initApproval (load matrix, buat detail records untuk level 1)
              │
              └─► user approve
                    │
                    ├─ OR operator: auto-approve semua peer → advance level
                    ├─ AND operator: tunggu semua peer → advance level
                    └─ Last level: finalize → publish approval.approved
              │
              └─► user reject
                    └─► publish approval.rejected → new revision dibuat
```

### 6.3 Approval Matrix Query

```sql
-- Hanya ambil entry yang valid hari ini
WHERE t.report_type = :reportType
  AND m.start_date  <= :now    -- epoch ms
  AND m.end_date    >= :now
  AND m.deleted_at IS NULL
ORDER BY m.level ASC, m.orders ASC
```

---

## Part 7 — YTD Query Rules (WAJIB)

> Anti-regression dari BUG v1 (`getytdoutlookpa` hardcoded values).

**Setiap query YTD WAJIB:**
1. `current_status = 'approved'` — hanya data approved
2. Subquery `ORDER BY revision DESC LIMIT 1` — hanya revisi terbaru
3. Parameter: `company_id`, `year`, `month`, `report_type` — **tidak pernah hardcoded**

**Contoh pattern JPQL (bukan DQL):**
```
WHERE r.tenantId    = :tenantId
  AND r.companyId   = :companyId    -- WAJIB parameterisasi
  AND r.periodYear  = :year          -- WAJIB parameterisasi
  AND r.currentStatus = 'approved'
  AND v.month       <= :targetMonth
  AND r.revision = (SELECT MAX(r2.revision) ... WHERE r2.currentStatus = 'approved')
```

---

## Part 8 — GraalVM Ratio Formula Engine

### 8.1 Mengapa GraalVM JS?

`javax.script.ScriptEngine` (v1) deprecated dan tidak thread-safe. GraalVM Polyglot API thread-safe jika implementasi benar.

### 8.2 Thread-Safe Pattern

```java
// ✅ BENAR: buat Context baru per evaluasi; share Engine
Engine SHARED_ENGINE = Engine.newBuilder("js").build();  // shared — thread-safe
Context ctx = Context.newBuilder("js").engine(SHARED_ENGINE).build();  // per evaluasi
// Selalu ctx.close() setelah selesai (gunakan try-with-resources)
```

### 8.3 Docker Base Image

```
ghcr.io/graalvm/jdk-community:21
```

---

## Part 9 — Notification Scheduler Logic

### 9.1 Daily Reminder (08:00 WIB)

```
cron: "0 0 8 * * *", timeZone: "Asia/Jakarta"

Per company, per report_type:
  1. due_date = mst_setting.due_date
  2. reminder = due_date + 1 hari
  3. IF reminder = Minggu → +1 hari (Senin)
  4. IF reminder ∈ mst_holiday → +1 hari lagi
  5. IF today = reminder
     AND laporan masih draft/incomplete
     AND tidak ada entry di notif_reminder_history untuk (company, type, today)
  THEN kirim email + insert notif_reminder_history
```

### 9.2 Export Cleanup (00:00 WIB)

```
cron: "0 0 0 * * *", timeZone: "Asia/Jakarta"
Delete exports where: created_at < now - 3_days
1. Delete file fisik dari filesystem
2. Update file_export.status = 'EXPIRED'
```

---

## Part 10 — File Storage Path Convention

```
/{tia.file.storage.base-path}
  /{tenant_id}
    /{company_id}
      /{report_type}              ← MB | MR | OPA | RO | CAFRM
        /{report_id}
          /{uuid}_{original_name}
```

**CAFRM path:**
```
/{base}/{tenant_id}/{company_id}/CAFRM/{category_code}/{uuid}_{filename}
```

---

## Part 11 — Feature Flag Guard Pattern

Setiap request ke `tia-cafrm-service` harus dicek feature flag:

```java
// Inject di service layer (bukan resource layer)
featureFlagGuard.requireCafrmEnabled(tenantId)
    .chain(() -> /* logika bisnis */)
```

Jika flag disabled → throw `WebApplicationException(404)` dengan code `CAFRM_MODULE_DISABLED`.

---

## Part 12 — CAFRM Access Control Matrix

| Role Suffix | Upload | List | Download | Delete | Scope |
|-------------|--------|------|----------|--------|-------|
| `*_SUBCO` | ✅ Own category & company | ✅ | ✅ | ✅ Own docs | Company yang ditugaskan |
| `*_TIA` | ✅ Own category | ✅ | ✅ | ✅ | Semua company |
| `*_BOD` | ❌ | ✅ | ✅ | ❌ | Semua company |
| `ROLE_SUPERADMIN` | ✅ | ✅ | ✅ | ✅ | Semua |

**Cross-category rule:** `ROLE_CAFRM_IA_*` tidak bisa akses kategori `ANTI_FRAUD` atau `RISK_MANAGEMENT`.

---

## Part 13 — Module Type String Registry

> Digunakan sebagai nilai `log_activity_type` di `AuditTrailDocument`.

```
EKSAD_TIA.AUTH.LOGIN
EKSAD_TIA.AUTH.LOGIN_FAILED
EKSAD_TIA.AUTH.LOGOUT
EKSAD_TIA.AUTH.PASSWORD_RESET_REQUEST
EKSAD_TIA.AUTH.PASSWORD_RESET
EKSAD_TIA.AUTH.USER.CREATE
EKSAD_TIA.AUTH.USER.UPDATE
EKSAD_TIA.AUTH.USER.DELETE

EKSAD_TIA.MASTERDATA.COMPANY.CREATE / UPDATE / DELETE
EKSAD_TIA.MASTERDATA.USER.CREATE / UPDATE / DELETE
EKSAD_TIA.MASTERDATA.ROLE.CREATE / UPDATE
EKSAD_TIA.MASTERDATA.ITEM_REPORT.CREATE / UPDATE / DELETE
EKSAD_TIA.MASTERDATA.APPROVAL_MATRIX.CREATE / UPDATE / DELETE

EKSAD_TIA.SUBMISSION.CREATE / UPDATE / SUBMIT / IMPORT
EKSAD_TIA.ATTACHMENT.UPLOAD / DELETE

EKSAD_TIA.APPROVAL.INIT
EKSAD_TIA.APPROVAL.APPROVE / REJECT
EKSAD_TIA.APPROVAL.AUTO_APPROVE
EKSAD_TIA.APPROVAL.SUPERADMIN_APPROVE

EKSAD_TIA.FILE.UPLOAD / DOWNLOAD / DELETE / EXPORT
EKSAD_TIA.NOTIFICATION.REMINDER_SENT / EMAIL_SENT

EKSAD_TIA.CAFRM.MAPPING.CREATE / DELETE
EKSAD_TIA.CAFRM.DOCUMENT.UPLOAD / DOWNLOAD / DELETE
```

---

## Part 14 — Testing Standards

| Layer | Tool | Scope |
|-------|------|-------|
| Unit | JUnit 5 + Mockito | Service & business logic |
| Integration | `@QuarkusTest` + REST Assured | REST endpoints (full stack) |
| DB | Testcontainers (PostgreSQL) | Repository queries |
| Messaging | Testcontainers (RabbitMQ) | Consumer/producer integration |
| Audit | Testcontainers (MongoDB) | Audit document persistence |

**Wajib di setiap service:**
- Unit test untuk setiap business rule
- Integration test untuk setiap REST endpoint (happy path + error cases)
- Test concurrency untuk components yang claim thread-safe (terutama `RatioFormulaEngine`)
