# EKSAD QA GPT — Mode A Chat Starters

> Pick the **Top 4** for the GPT UI. This assistant designs tests and prepares Mode B handoff metadata; it does not write automation source.

---

## 🟢 Recommended Top 4

```text
Buatkan Test Plan, RTM, dan stable TC-NNN test cases dari FSD ini:
[paste FSD section, requirement IDs, dan acceptance criteria]
```

```text
Buatkan state-machine test matrix untuk entity [nama entity].
States/transitions/actors: [list]
```

```text
Review Test Plan ini dan identifikasi coverage gap untuk requirement, auth,
tenant isolation, validasi, soft delete, audit, dan state transition:
[paste Test Plan/RTM]
```

```text
Siapkan Mode B automation handoff metadata untuk TC IDs berikut:
[list TC IDs, source artifact/version, target repo/module, environment]
Jangan tulis test source.
```

---

## 📋 Full Mode A Starter Library

### Test Plan and RTM

```text
Buatkan Test Plan dan RTM untuk modul [nama modul] di service [nama service].
Source: [path/version/state atau paste FSD]. Environment: [list].
```

```text
Trace setiap requirement dan acceptance criterion berikut ke stable TC-NNN IDs.
Tandai requirement yang belum testable atau belum punya expected result:
[paste requirements]
```

```text
Buatkan regression test checklist untuk perubahan berikut dan kaitkan setiap item
ke requirement/TC ID yang terdampak: [deskripsi perubahan atau PR evidence].
```

```text
Buatkan UAT checklist dari BRD/FSD berikut. Pertahankan source IDs dan named
business authority: [paste section relevan].
```

### Test-Case Derivation

```text
Dari user stories berikut, buatkan black-box test cases lengkap: happy path,
failure, boundary, dan exact expected result. Jangan tulis automation source.
[paste user stories]
```

```text
Dari validation-rules table berikut, buatkan boundary test cases per field dan
pertahankan rule IDs: [paste validation table].
```

```text
Dari business rules berikut, buatkan test cases untuk setiap rule. Catat gap jika
precondition, actor, atau expected result belum jelas: [paste BR-{N} list].
```

```text
Dari error-code catalog berikut, buatkan test cases untuk memicu setiap error code
beserta exact status/body expectation: [paste error catalog].
```

### State-Machine Testing

```text
Buatkan full valid/invalid state-machine matrix untuk entity [nama entity].
States: [list]. Transitions dan actor: [list]. Expected status/error: [if known].
```

```text
Review approval workflow ini untuk missing transition, forbidden transition,
role/tenant boundary, dan revision loop: [paste workflow].
```

### API and Security Scenario Design

```text
Buatkan black-box test cases untuk [HTTP method] [path].
Contract/version: [reference]. Roles/tenant rules: [list]. Jangan tulis source code.
```

```text
Buatkan auth scenario matrix untuk endpoint berikut: no session, expired session,
wrong role, wrong tenant, dan valid role+tenant. Auth browser wajib memakai
HttpOnly Secure SameSite cookies; jangan menyarankan token browser storage.
[list endpoints]
```

```text
Buatkan soft-delete test cases untuk entity [nama entity]: list exclusion, GET by ID,
repeat delete, tenant isolation, dan audit existence.
```

```text
Buatkan multi-tenant isolation matrix untuk tenant A/B pada endpoints berikut.
Catat expected status dan data-leak assertions: [list endpoints].
```

### Mode B Automation Handoff Metadata

```text
Ubah approved TC IDs berikut menjadi Mode B handoff manifest. Sertakan source IDs,
automation target, suggested framework as metadata, target repo/module, permitted
test-only path, fixtures, roles/tenant, expected evidence, dependencies, gate state,
known gaps, owner, dan next action. Jangan tulis executable test source.
[paste approved TC rows]
```

```text
Pisahkan TC IDs berikut menjadi batch API, FE E2E, cross-service E2E, performance,
dan security untuk in-IDE QA agent. Jelaskan dependency order dan evidence yang
harus dikembalikan: [paste TC IDs].
```

```text
Review Mode B handoff manifest ini. Tandai missing/stale source version, unstable
TC IDs, unclear expected results, missing fixtures/cleanup, unauthorized output
paths, secret values, dan unresolved gate state: [paste manifest].
```

### Bug Reporting and Evidence

```text
Bantu tulis bug report dengan requirement ID, TC ID, build/artifact identity,
environment, precondition, exact steps, expected, actual, evidence links, severity,
dan owner: [paste observations].
```

```text
Classify severity untuk bug ini dan jelaskan release impact tanpa mengklaim verdict
atau approval yang belum diberikan: [deskripsi + evidence].
```

```text
Review execution evidence ini. Update status hanya untuk TC IDs yang punya
attributable evidence; sisanya tandai unknown/blocked: [paste evidence references].
```

---

## 💡 Tips for QA GPT

- Paste source artifact path/version/state and preserve requirement IDs.
- Use stable `TC-NNN` IDs before preparing a Mode B handoff.
- State exact expected status, body, UI state, event, or evidence.
- Record assumptions as gaps with an owner; do not silently invent missing facts.
- Keep Mode A code-free. The in-IDE Mode B agent writes automation in permitted test-only paths.
- Never include secret values in test cases or handoff metadata.
