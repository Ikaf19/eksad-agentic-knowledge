---
name: eksad-code-review
description: "Use when the user asks the Technical Leader profile to review code or a PR against EKSAD standards. Produces evidence- and confidence-qualified findings with unchanged BLOCKER/MAJOR/MINOR/NIT labels, separate verdict dimensions, false-positive suppression, dependency/supply-chain checks, and AppSec/threat-model escalation when triggered."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native adaptation)
license: MIT
metadata:
  hermes:
    tags: [eksad, code-review, tl, pr-checklist, severity, confidence, evidence, appsec, supply-chain, mentor]
    related_skills: [multi-role-agent-setup, eksad-appsec-review, eksad-adr-workflow]
---

# EKSAD Code Review Skill

Code review workflow for EKSAD Technical Leader. Produces severity-labeled findings against EKSAD principles, coding standards, and forbidden patterns. Always explains **why** a finding matters, not just the rule.

## When to Use

- User asks "review this code"
- User asks to walk through a PR checklist
- User wants EKSAD compliance check on entity/repo/service/resource
- User wants architecture decision rationale (ADR)
- User wants mentoring on a specific EKSAD pattern

## When NOT to Use

- Authoring new code → switch to `developer-backend` or `developer-frontend`
- Architecture design → switch to `system-analyst` profile + `eksad-tsd-design` skill
- Business requirements → switch to `business-analyst` profile

## Knowledge References

Primary:
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — 14 principles, forbidden patterns
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md` — v1.2, full rules
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_PATTERN.md` — CrudFlows v2 reactive
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_JPA.md` — CrudFlows v2 blocking

For FE code:
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_CODING_STANDARDS.md` — v1.2 (current)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_PATTERNS.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_TESTING_GUIDE.md` — v1.1

Supporting:
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_RESILIENCE_PATTERNS.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_OBSERVABILITY_PATTERNS.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_TESTING_GUIDE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CORE_AUTH_CLIENT_SDK.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CICD_CONTAINER_PATTERNS.md`
- `~/.hermes/knowledge/eksad/hermes-skills/security/eksad-appsec-review/SKILL.md` — security review and threat-model escalation
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md` — threat model structure

## Evidence and Confidence Gate

Every finding must include: exact `file:line` (or component/config location), observed behavior, a reachable failure/abuse path, impact, violated EKSAD rule or approved requirement, and a concrete fix or verification step. Review the actual diff plus enough surrounding call/configuration flow to establish reachability; a pattern match alone is not a finding.

Label confidence independently from severity:

| Confidence | Evidence threshold | Reporting rule |
|---|---|---|
| **High** | Directly demonstrated by code/config/contract or reproducible evidence | May support merge-blocking action at the applicable severity |
| **Medium** | Strong evidence and credible reachable path; one bounded fact needs confirmation | Report as a finding, explicitly naming the missing confirmation |
| **Low** | Hypothesis, incomplete context, or generic pattern only | Put under `Questions / Investigation`; do not use as a merge-blocking finding |

**False-positive suppression:** before reporting, inspect callers, framework behavior, generated/test-only scope, environment/profile reachability, guards, tenant/authorization enforcement, validation, and compensating controls at the correct boundary. Suppress the candidate when the path is unreachable, an effective control is evidenced, code cannot ship, or the claim is only generic. Do not suppress because a test merely exists—verify that it exercises the path and assertion. Record a short suppression note only when it is material to auditability.

Absence of evidence is `Unknown`, not proof of compliance. Ask for the exact missing artifact rather than inventing behavior. Preserve all existing EKSAD non-negotiables and severity meanings.

## Severity Levels (ALWAYS label)

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 **BLOCKER** | Violates a principle; will break in production; security issue | Reject — must fix before merge |
| 🟠 **MAJOR** | Pattern violation; will cause tech debt | Fix before merge |
| 🟡 **MINOR** | Style / convention drift | Fix or note for follow-up |
| 🟢 **NIT** | Subjective preference | Optional |

## Review Order (Always Follow)

1. **Architecture / principles** — any of the 14 violated?
2. **Security** — JWT validation, RBAC, tenant isolation, audit trail
3. **Data model** — `BaseEntity`/`BaseTransactionalEntity`, columns, constraints, indexes
4. **Repository** — `BaseRepository` extension, flow methods, auditMutator
5. **Service layer** — `@ReactiveTransactional`, `@WithSession`, `UserContextProvider` injection
6. **REST resource** — `@RolesAllowed`, return type, status codes
7. **Module type constants** — paired interfaces, PREFIX, action labels
8. **Reactive correctness** — no blocking on event loop, proper `Uni` chaining
9. **Tests** — coverage of auth (401/403), state machine, validation, audit
10. **Build / POM** — `eksad-parent` parent, version pins, annotation processors
11. **Dependencies / supply chain** — necessity; approved source; pinned/locked direct and transitive identity; provenance/checksum/signature where policy requires; vulnerability/license evidence freshness; build plugin/script/image privilege; maintainer/support status; safe upgrade and rollback path

## AppSec and Threat-Model Trigger

Invoke `eksad-appsec-review` and create/update `EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md` when the change affects authentication/session/JWT, authorization or ownership, tenant isolation, sensitive data, secrets/cryptography, external APIs/webhooks, file upload/download or parsers, privileged/admin flows, event trust, dynamic query/command/deserialization, material dependencies/supply-chain inputs, or any trust boundary.

For a low-risk refactor with no changed security surface, record `Threat model impact: none` and cite the inspected diff/control evidence. Do not silently skip. AppSec provides a security recommendation; only the named security/risk authority can accept residual risk or approve a waiver.

### Dependency and Supply-Chain Review

- Compare manifest and lockfile; identify newly resolved transitives, repositories/registries, plugins, build actions, base images, and runtime-loaded modules.
- Require a business/technical purpose and least privilege for install/build/runtime scripts.
- Bind scan/provenance/license evidence to the reviewed version/digest and record tool/evidence freshness; unavailable evidence is `Unknown` or `Blocked` under approved policy, never fabricated pass.
- Check supported version, maintainer/ownership, known-vulnerability exposure, package-name confusion/source drift, and whether removal/upgrade changes behavior.
- Require compatibility, rollout, rollback, and monitoring for a material upgrade. Do not recommend `latest` or an unpinned mutable artifact.

## Common Pitfalls (Reference Table)

| Pitfall | Severity | Why it breaks |
|---------|----------|---------------|
| `extends BaseEntity` without `@SuperBuilder` | 🔴 BLOCKER | `@Builder` breaks inheritance |
| Missing `tenant_id` column | 🔴 BLOCKER | Cross-tenant data leakage |
| `String` for financial amounts | 🔴 BLOCKER | Should be `BigDecimal` |
| `Date`/`LocalDateTime` for timestamps | 🟠 MAJOR | Should be `Long` (epoch ms) |
| Calling `persist()` directly | 🔴 BLOCKER | Bypasses audit trail |
| Business logic in repository | 🟠 MAJOR | Belongs in Service layer |
| `@Transactional` on repository | 🟠 MAJOR | Should be `@ReactiveTransactional` on Service |
| Manual `LogActivityDTO` construction | 🟠 MAJOR | Should use `LogHandler` via flow |
| Static JWT parse in repository/service | 🟠 MAJOR | Not mockable — use `UserContextProvider` |
| `ddl-auto=update` in `application.properties` | 🔴 BLOCKER | Forbidden — use Flyway |
| `FLOAT`/`DOUBLE`/`VARCHAR` for money | 🔴 BLOCKER | Use `NUMERIC(20,4)` |
| Hard-coded credentials | 🔴 BLOCKER | Use `${ENV_VAR}` |
| Missing `@RolesAllowed` on endpoint | 🔴 BLOCKER | Open endpoint (security violation) |
| `enum` for module type | 🟠 MAJOR | Should be interface (paired) |
| Wrong business jargon in service names | 🟠 MAJOR | Use domain-agnostic `svc-{function}` |

### FE-specific pitfalls

| Pitfall | Severity | Why |
|---------|----------|-----|
| `useEffect` + `fetch` for server state | 🔴 BLOCKER | Should use React Query |
| `any` TypeScript type | 🟠 MAJOR | Should use `unknown` + type guard |
| `localStorage` for auth tokens | 🔴 BLOCKER | Should be HttpOnly cookie |
| `new Date()` in feature code | 🟠 MAJOR | Should use dayjs |
| Mock data in production service layer | 🔴 BLOCKER | Use real apiClient, MSW in tests |
| Direct service call in component | 🟠 MAJOR | Should go through hook |
| `<InputField type="date">` | 🟡 MINOR | Should use `<DatePicker>` |
| TypeScript `enum` for status | 🟠 MAJOR | Should use string-literal union |

## Output Template

```markdown
# Code Review — <PR title or commit hash>

## Summary
<1-2 sentences: what this PR does>

## Verdict Dimensions

| Dimension | Verdict | Evidence / basis |
|---|---|---|
| EKSAD correctness / maintainability | Approve / Approve with comments / Request changes / Blocked / Not reviewed | <reference> |
| Security implementation | Pass / Pass with findings / Fail / Blocked / Not reviewed | <reference or AppSec report> |
| Test evidence | Sufficient / Gaps / Blocked / Not reviewed | <reference> |
| Dependency / supply chain | Pass / Pass with findings / Fail / Blocked / Not applicable | <reference> |
| Threat-model impact | Complete / Partial / Missing / Not required (with evidence) | <reference> |

**Merge recommendation:** 🟢 Approve / 🟡 Approve with comments / 🔴 Request changes / ⚪ Blocked

Do not collapse the dimensions: passing code style does not pass security, available tests are not a QA verdict, and a complete threat model can describe failing controls.

## Findings

### 🔴 BLOCKER
- [file:line] **<issue>** — Confidence: High/Medium — Evidence: <reachable path/control> — <why it breaks>
  **Fix:** <suggested code snippet>

### 🟠 MAJOR
- ...

### 🟡 MINOR
- ...

### 🟢 NIT
- ...

## Questions / Investigation (Low Confidence)
- [file:line] <question> — missing evidence: <artifact/behavior to confirm>

## Suppressed Candidates (only when material)
- <candidate> — suppressed because <unreachable/effective control/non-shipping/generic-only>; evidence: <reference>

## Checklist
- [ ] All 14 principles honored
- [ ] Security: JWT, RBAC, tenant isolation
- [ ] Data model compliant
- [ ] Repository uses flow methods
- [ ] Service uses @ReactiveTransactional
- [ ] @RolesAllowed on every endpoint
- [ ] Module types correct (paired interfaces)
- [ ] Reactive correctness (no blocking)
- [ ] Tests cover auth scenarios (401, 403, wrong tenant, wrong role)
- [ ] Audit trail verified for every write
- [ ] Build / POM clean
- [ ] Every finding meets evidence threshold and has confidence
- [ ] False-positive/compensating controls checked
- [ ] Dependency and supply-chain delta reviewed
- [ ] AppSec/threat-model trigger resolved with evidence
- [ ] Verdict dimensions reported separately
```

## Mentoring Style

When reviewing, **always explain the why**:
- ❌ "This is wrong, use BaseRepository"
- ✅ "Direct persist() bypasses the audit trail — every CRUD must go through createFlow/updateFlow/deleteFlow so eksad-core-audittrail captures the action. Here's the fix:..."

**Be opinionated but pragmatic.** When unsure, say so explicitly and ask the developer or another role.

## Anti-Patterns (never do)

❌ Vague findings ("this looks off")
❌ Findings without severity labels
❌ Findings without "why it breaks"
❌ Findings without suggested fix
❌ Merge-blocking a low-confidence hypothesis
❌ Reporting a generic scanner/pattern match without a reachable path
❌ Collapsing correctness, security, tests, supply chain, and threat-model status into one verdict
❌ Treating a waiver, unavailable evidence, or unreviewed scope as pass
❌ Personal attacks on developer style
❌ Accepting "the system works" as evidence of compliance
