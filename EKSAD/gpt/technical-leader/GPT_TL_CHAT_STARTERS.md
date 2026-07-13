# EKSAD Technical Leader GPT — Chat Starters

> **How to use this file:**
> In your TL Custom GPT editor → **"Conversation starters"** field.
> Pick the **Top 4** for the GPT UI. Full library below for reference.

---

## 🟢 Recommended Top 4 (Technical Leader Daily Use)

```
Review entity class ini — apakah sudah sesuai EKSAD standards? [paste class]
```
```
Review implementasi BaseRepository ini — cek createFlow/updateFlow/deleteFlow: [paste class]
```
```
Review Flyway DDL ini — tenant_id, BaseEntity columns, timestamps, indexes: [paste SQL]
```
```
Jalankan PR checklist lengkap untuk code ini: [paste code atau deskripsi PR]
```

---

## 📋 Full TL Starter Library

### Code Review

**Full PR Review**
```
Tolong jalankan full EKSAD code review checklist untuk PR berikut. Files yang diubah: [list files]. Kode: [paste kode atau deskripsi perubahan].
```

**Entity Class Review**
```
Review entity class ini — cek: extends BaseEntity, @SuperBuilder, tenant_id, field types (Long timestamp, BigDecimal financial), tidak ada business logic: [paste entity class].
```

**Repository Class Review**
```
Review BaseRepository implementation ini — cek: 5 abstract methods, createFlow/updateFlow/deleteFlow usage, toNewEntity sets tenantId dan createdAt, module type format: [paste repository class].
```

**Service Class Review**
```
Review service class ini — cek: @ApplicationScoped, @WithSession, @ReactiveTransactional, returns Uni<T>, tidak ada business logic yang harusnya di repository: [paste service class].
```

**Resource/Controller Review**
```
Review REST resource class ini — cek: @RolesAllowed pada setiap endpoint, returns Uni<Response>, HTTP status codes benar, API path convention: [paste resource class].
```

**Flyway DDL Review**
```
Review Flyway migration file ini — cek: naming convention, tenant_id, BaseEntity columns (6 kolom), timestamps BIGINT, financial NUMERIC(20,4), indexes: [paste SQL file].
```

**application.properties Review**
```
Review application.properties ini — cek: ddl-auto bukan 'update', flyway config, semua secrets pakai ${ENV_VAR}, JWT config, RabbitMQ config: [paste properties file].
```

**POM Review**
```
Review pom.xml ini — cek: parent = eksad-parent, eksad-core-common dependency, annotation processor order (Lombok + MapStruct), tidak ada version override yang tidak perlu: [paste pom.xml].
```

---

### Implementation Guidance

**How to Implement BaseRepository**
```
Tunjukkan cara implementasi BaseRepository dari eksad-core-common untuk entity [nama entity] dengan ID type [Long/UUID]. Operations: [CREATE, UPDATE, DELETE, dan custom actions jika ada].
```

**How to Implement commandFlow**
```
Tunjukkan cara pakai commandFlow untuk implementasi [APPROVE/REJECT/custom action] pada entity [nama entity]. Guard condition: [kondisi yang harus dipenuhi].
```

**How to Write Module Type Constants**
```
Buatkan ModuleType interface constants untuk service [nama service]. Modules: [list]. Actions per module: [list].
```

**How to Write a Reactive Service Method**
```
Tunjukkan cara menulis reactive service method yang benar untuk [operasi: create/update/approve/dll] menggunakan Mutiny Uni. Context: [deskripsi operasi].
```

**How to Handle Guard Failure**
```
Bagaimana cara menulis guard yang benar di updateFlow untuk kondisi: [deskripsi kondisi]. Entity: [nama entity]. Error message: [pesan error yang diinginkan].
```

**How to Implement Soft Delete Query**
```
Bagaimana cara menulis custom query di repository untuk [deskripsi query] yang secara otomatis filter deleted_at IS NULL dan filter tenant_id dari UserContext?
```

---

### Pitfall Detection & Fix

**Detect P1 Issues**
```
Scan kode berikut untuk critical issues (P1): ddl-auto=update, missing tenant_id, direct persist() bypass, hardcoded credentials, missing @RolesAllowed, Double/Float financial fields: [paste kode].
```

**Fix ThreadLocal Issue**
```
Kode ini menggunakan AuthContextStore.getToken() di dalam reactive chain. Tolong tunjukkan bagaimana memperbaikinya agar aman di Vert.x event loop context.
```

**Fix @Builder vs @SuperBuilder**
```
Entity ini extend BaseEntity tapi pakai @Builder, bukan @SuperBuilder. Apa masalahnya dan bagaimana cara fix-nya?
```

**Fix Missing tenant_id**
```
toNewEntity() ini tidak set tenantId. Di mana dan bagaimana cara fix-nya dengan benar?
```

**Fix Blocking in Reactive Chain**
```
Ada suspek blocking operation di dalam flatMap() ini. Tolong identifikasi dan tunjukkan fix reaktif-nya: [paste kode].
```

---

### Coding Standards Q&A

**Why Long for Timestamps**
```
Kenapa EKSAD pakai Long (epoch milliseconds) untuk timestamps, bukan Instant atau LocalDateTime? Apa tradeoff-nya?
```

**Why String for ModuleType**
```
Kenapa EKSAD pakai String constants interface untuk module type, bukan enum? Apa masalahnya kalau pakai enum?
```

**Why Soft Delete**
```
Kenapa semua entity harus soft delete? Kapan boleh hard delete?
```

**Why No Cross-Service JOIN**
```
Kenapa tidak boleh ada cross-service database JOIN di EKSAD? Apa alternatifnya?
```

**Why Fire-and-Forget for Audit**
```
Kenapa audit trail pakai fire-and-forget? Apa risikonya? Bagaimana kita handle kalau RabbitMQ down?
```

**When to Use commandFlow vs updateFlow**
```
Kapan saya harus pakai commandFlow vs updateFlow di BaseRepository? Apa perbedaannya?
```

---

### Architecture Decision Records (ADR)

**Write an ADR**
```
Bantu saya tulis Architecture Decision Record (ADR) untuk keputusan teknis berikut: [deskripsi keputusan]. Opsi yang dipertimbangkan: [list opsi]. Keputusan: [opsi yang dipilih]. Alasan: [deskripsi singkat].
```

**Review a Technical Decision**
```
Review keputusan teknis berikut dari sisi EKSAD standards dan long-term maintainability: [deskripsi keputusan dan alasannya].
```

---

### Testing

**Write Unit Test**
```
Tunjukkan cara menulis unit test yang benar untuk service method [nama method] di [nama service]. Scenarios: [list test scenarios: happy path + failure cases].
```

**Write Integration Test**
```
Tunjukkan cara menulis @QuarkusTest integration test untuk endpoint [HTTP method] [path]. Expected: [deskripsi behavior].
```

**Review Test Quality**
```
Review test class ini — cek: test naming (methodName_scenario_expectedResult), mock setup benar, semua failure scenarios ter-cover, tidak ada test yang selalu pass: [paste test class].
```

---

## 💡 Tips for TL GPT

- **Always paste the code** — this GPT gives the best review when it can see actual code
- **Specify the severity focus** — say "focus on P1 issues only" for quick pre-merge checks
- **Ask for the "why"** — any standard that seems arbitrary, ask "why does EKSAD require this?"
- **Use for mentoring** — "explain this to a junior developer" gives simplified explanations
- **PR comment format** — ask "format this as PR comments" for copy-paste ready review notes
