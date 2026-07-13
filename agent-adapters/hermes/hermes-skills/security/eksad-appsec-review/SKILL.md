---
name: eksad-appsec-review
description: Use for EKSAD application-security design or review when a change affects authentication, authorization, tenant isolation, sensitive data, trust boundaries, external integrations, file handling, secrets, cryptography, dependencies, privileged operations, or material abuse paths. Produces evidence-based AppSec findings and a threat model without accepting risk on behalf of the named authority.
version: 1.0.0
author: EKSAD Platform Team
license: MIT
metadata:
  hermes:
    tags: [eksad, appsec, security-review, threat-model, trust-boundary, abuse-path, supply-chain]
    related_skills: [eksad-tsd-design, eksad-code-review, eksad-adr-workflow]
---

# EKSAD AppSec Review

## Purpose and Boundary

Review EKSAD application design/code for credible security failure and document threat treatment. This skill supplies findings, threat-model completeness, and residual-risk recommendations. It does not approve architecture, merge code, grant a waiver, accept residual risk, or authorize production. Those decisions remain with the named accountable authorities.

Resolve `<EKSAD_PACK_ROOT>` from `EKSAD_PACK_SRC` when valid, otherwise the active shared EKSAD deployment, otherwise `~/.hermes/knowledge/eksad`.

## Required References

- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_CORE_AUTH_PATTERNS.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_MULTI_TENANCY_PATTERNS.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md`
- `<EKSAD_PACK_ROOT>/EKSAD/gpt/_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md`
- Approved BRD/FSD/TSD, ADRs, API/event contracts, data classification, dependency manifests/lockfiles, deployment architecture, and relevant test/scan evidence.

Name a generated threat-model file exactly `{PROJECT_CODE}_THREAT_MODEL_{SCOPE}_v{VERSION}.md`.

## Mandatory Triggers

### Canonical routing and authority

- Any role may raise a mandatory trigger and supply scoped evidence.
- The System Analyst or Technical Leader owns coordination and invocation of this shared review workflow. The assigned security review function performs the review; AppSec is not a profile or independent delivery owner.
- Only the named risk authority may accept residual risk or grant a waiver. Review coordination, a reviewer recommendation, or an implementation verdict conveys no such authority.

Perform AppSec review and create/update a threat model when a change:

- adds or changes login, JWT/session handling, `@RolesAllowed`, permission/state transition, service identity, or privileged/admin behavior;
- changes tenant isolation, ownership checks, object lookup, data classification/retention, encryption, secrets, or audit behavior;
- crosses a new trust boundary or adds an internet-facing API, webhook, third-party integration, broker consumer, upload/download, parser, template, redirect, or callback;
- introduces executable content, deserialization, dynamic query/command construction, cryptography, payment/financial processing, or high-impact workflow;
- adds/updates a dependency, image, plugin, package source, build action, or other supply-chain input with material exposure;
- materially changes service/data boundaries, deployment topology, abuse surface, or an accepted ADR's security assumptions.

A low-risk refactor with no changed surface may record `Threat model impact: none` with evidence. Do not create ceremony without changed risk.

## Evidence and Confidence

Every reported finding must include exact component/location, observed behavior, reachable preconditions/attack path, impact, violated requirement/control, and a concrete mitigation or verification step.

Confidence labels:

- **High:** directly demonstrated by code/config/contract or reproducible evidence.
- **Medium:** strong evidence and a credible reachable path, with one bounded fact still requiring confirmation.
- **Low:** hypothesis or incomplete context; record as a question/investigation item, not a merge-blocking finding.

Suppress a candidate finding when the allegedly vulnerable path is unreachable, an effective control is evidenced at the correct boundary, the code is generated/test-only and cannot ship, or the claim relies only on a generic pattern with no EKSAD-specific path. Record material suppressed candidates briefly when auditability matters. Absence of evidence is `Unknown`, not proof of safety.

## Severity Labels

Use the existing EKSAD labels unchanged:

| Severity | Meaning | Action |
|---|---|---|
| 🔴 **BLOCKER** | Violates a principle; will break in production; security issue | Reject — must fix before merge |
| 🟠 **MAJOR** | Pattern violation; will cause tech debt | Fix before merge |
| 🟡 **MINOR** | Style / convention drift | Fix or note for follow-up |
| 🟢 **NIT** | Subjective preference | Optional |

Severity represents impact/required action; confidence represents evidence strength. Never inflate severity to compensate for low confidence.

## Workflow

### 1. Scope and Evidence Inventory

Pin review target/ref, changed components, environments, identities, data classes, entry points, dependencies, and evidence versions. List missing context and owner. Never request or reproduce raw secrets or sensitive production data.

### 2. Model the System

Use `EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md` to identify:

- protected assets and security objectives;
- human/service/external attackers and their capabilities;
- components, data stores, entry/exit points, and data flows;
- trust boundaries, authentication transitions, tenant context, and privilege changes;
- credible abuse paths, preconditions, impact, existing controls, gaps, and mitigations.

Model asynchronous consumers, scheduled jobs, admin/support paths, storage/CDN links, and CI/dependency inputs—not only REST endpoints.

### 3. Review Controls

Check at minimum:

1. **Identity/session:** JWT signature, issuer/audience/expiry, key rotation, cookie/token storage, service identity.
2. **Authorization/tenancy:** `@RolesAllowed`, object ownership, tenant derivation and filtering, cross-tenant cache/event/file isolation, privileged state transitions.
3. **Input/output:** schema and business validation, query/command construction, parsing/deserialization, upload type/size/storage, output encoding, redirect/callback controls, error leakage.
4. **Data/secrets/crypto:** minimization, classification, logs/audit redaction, transit/at-rest protection, approved algorithms/key management, environment/credential references.
5. **API/events:** replay/idempotency, rate/abuse limits, webhook authenticity, event publisher/consumer authorization, envelope tenant/actor integrity.
6. **Dependencies/supply chain:** necessity, declared source, pinned/locked version, provenance/signature/checksum where policy requires, known-vulnerability and license evidence, transitive exposure, maintainer/support status, build-script/plugin/image risk, and safe upgrade/rollback path.
7. **Detection/recovery:** security-relevant audit events, alert owner/signal, tamper resistance, investigation correlation, revocation/containment path.

Preserve EKSAD non-negotiables: tenant isolation, endpoint authorization, audit flows, Flyway-only schema changes, soft delete/audit columns, approved timestamp/money types, fixed service names, and all other base principles.

### 4. Validate Abuse Paths and Findings

Trace source → boundary → missing/failed control → protected asset/operation → impact. Search for compensating controls and tests before reporting. Separate confirmed findings from questions and accepted exceptions. A waiver must name authority, scope, rationale, compensating controls, expiry, and evidence; `Waived` is never `Passed`.

### 5. Recommend Treatment and Retest

For each threat choose `Mitigate`, `Avoid`, `Transfer`, or `Accept by named authority`; the reviewer cannot self-accept. Assign owner, due date, validation evidence, and residual risk. Retest the exact path after mitigation and preserve evidence.

## Deterministic Security-Implementation Verdict

Evaluate the reviewed scope in this precedence order so the result is fail-closed and reproducible:

1. **FAIL** — one or more confirmed, unresolved `BLOCKER` or `MAJOR` findings exist, or a mandatory security control is evidenced as missing or ineffective.
2. **BLOCKED** — no `FAIL` condition is established, but mandatory scope, target identity, evidence, access, owner response, or required retest is unavailable or incomplete enough that the implementation verdict cannot be determined safely.
3. **PASS WITH FINDINGS** — review is complete enough to determine the verdict, no `FAIL` condition exists, and one or more unresolved `MINOR` or `NIT` findings remain.
4. **PASS** — review is complete for the declared scope, mandatory controls are evidenced effective, and no unresolved findings remain.
5. **NOT REVIEWED** — no security implementation review was performed for the declared scope; never use this as a passing result.

A waiver or residual-risk acceptance is recorded only in the residual-risk dimension. It does not remove a finding, change its severity, or convert `FAIL`/`BLOCKED` to `PASS` or `PASS WITH FINDINGS`.

## Separate Verdict Dimensions

Report independently:

- **Security implementation:** `PASS | PASS WITH FINDINGS | FAIL | BLOCKED | NOT REVIEWED`
- **Threat-model completeness:** `COMPLETE | PARTIAL | MISSING | NOT REQUIRED (with evidence)`
- **Residual-risk decision:** `NOT REQUIRED | AWAITING AUTHORITY | ACCEPTED | REJECTED | EXPIRED`

Do not collapse these into one green/red result. A complete threat model can describe failing controls; passing reviewed code does not accept residual risk.

## Completion Checklist

- [ ] Exact target, scope, data, actors, flows, and trust boundaries recorded
- [ ] Tenant/auth/ownership boundaries and privileged transitions reviewed
- [ ] Credible abuse paths linked to assets and evidence
- [ ] Dependencies and supply-chain inputs reviewed
- [ ] Every finding has severity, confidence, evidence, impact, and mitigation
- [ ] Low-confidence hypotheses are questions, not blockers
- [ ] Compensating controls and false-positive conditions checked
- [ ] Threat treatments have owners, due dates, validation, and residual risk
- [ ] Separate verdict dimensions and named authorities recorded
- [ ] No raw secret or sensitive production data appears

## Output

Return scope/evidence, threat-model reference, verdict dimensions, findings grouped by existing EKSAD severity, investigation items, suppressed candidates if material, residual risks/authority state, and retest actions. Never claim safety for unreviewed scope.
