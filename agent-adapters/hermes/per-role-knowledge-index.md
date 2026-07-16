# Per-Role Knowledge Index — EKSAD Pack

**Purpose:** Map each EKSAD role profile to the exact `_base/` and `_template/` files it should consult, plus the role-specific instructions and patterns to apply.

> When a role profile's SOUL.md says "consult EKSAD standards", point to the specific files listed below — not the whole pack. Keeps context lean and prevents overload.

**Pack location:** `~/.hermes/knowledge/eksad/EKSAD/gpt/`
**Pack version:** v31
**Source of truth:** Git clone from `github.com/Ikaf19/brainstorming` branch `feature/eksad-knowledge-v3`

**Canonical AppSec routing:** Any role may raise an AppSec trigger and supply evidence; the System Analyst or Technical Leader coordinates and invokes the shared `eksad-appsec-review` workflow; only the named risk authority accepts residual risk or grants a waiver. AppSec is not a profile.

---

## 🔵 Business Analyst (`business-analyst`)

**Profile SOUL.md:** `~/.hermes/profiles/business-analyst/SOUL.md` (751 lines, 21 sections)
**Custom skill:** `~/.hermes/skills/business-analysis/eksad-ba-workflow/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/business-analyst.md`

**Primary job:** BRD, FSD, UR, User Stories, Acceptance Criteria, Business Rules, Approval Workflow (business level).

### Knowledge files to consult

**Always read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BA_DOMAIN_GLOSSARY.md` — BA pipeline terms + EKSAD platform BRs
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — Tech stack + BR-PLATFORM-001..015 context (for awareness, NOT for writing tech content in BRD/FSD)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_REGISTRY.md` — 🔴 P0 domain map (Automotive, HRIS, Finance)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_GLOSSARY.md` — cross-check business + technical terms

**Templates (source of truth):**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_UR_TEMPLATE.md` — User Requirements (current)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_BRD_TEMPLATE.md` — v3.2 (current)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_REGULATORY_TEMPLATE.md` — Regulatory & Compliance Reference (standalone)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_FSD_TEMPLATE.md` — v3.0 (current)

**When asking reserved field questions:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_RESERVED_FIELD_PATTERNS.md`

**Does NOT load:** coding standards, CrudFlows, event catalog, FE patterns, TSD templates.

---

## 🟢 System Analyst (`system-analyst`)

**Profile SOUL.md:** `~/.hermes/profiles/system-analyst/SOUL.md` (208 lines)
**Custom skills:** `~/.hermes/skills/technical-design/eksad-tsd-design/`, `~/.hermes/skills/technical-design/eksad-adr-workflow/`; use shared `~/.hermes/skills/security/eksad-appsec-review/` when security triggers apply
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/system-analyst.md`

**Primary job:** TSD, system architecture, data model, Flyway DDL, API contracts, RabbitMQ event schemas, ERD (within TSD), API contract tables.

### Knowledge files to consult

**Always read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — 14 principles, stack profile axes
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_REGISTRY.md` — 🔴 P0 domain map

**When designing services:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` — architecture patterns (incl. ERD conventions)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_SPRING_BOOT_MAPPINGS.md` — Quarkus ↔ Spring Boot mapping
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md` — code reference (your design must enable compliance)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_PATTERN.md` — CrudFlows v2 reactive
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_JPA.md` — CrudFlows v2 blocking
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_GLOSSARY.md` — technical terms

**When working with specific patterns:**
- `_base/EKSAD_MASTER_DATA_PATTERNS.md` — svc-master-data
- `_base/EKSAD_CACHE_SYNC_PATTERNS.md` — denormalized cache
- `_base/EKSAD_EVENT_CATALOG.md` — exchange/routing-key registry
- `_base/EKSAD_MULTI_TENANCY_PATTERNS.md` — N-level tenant hierarchy
- `_base/EKSAD_CORE_AUTH_PATTERNS.md` — auth service patterns
- `_base/EKSAD_RESERVED_FIELD_PATTERNS.md` — tenant-configurable fields
- `_base/EKSAD_RESILIENCE_PATTERNS.md` — timeout/retry/circuit breaker
- `_base/EKSAD_OBSERVABILITY_PATTERNS.md` — logging/tracing/metrics
- `_base/EKSAD_DB_DEPLOYMENT_STRATEGY.md` — phased PG deployment
- `_base/EKSAD_CICD_CONTAINER_PATTERNS.md` — Docker/K8s

**Templates:**
- `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` — TSD structure (source of truth)
- `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` — FE-TSD structure
- `_template/EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` — project ARCHITECTURE.md skeleton
- `_template/EKSAD_GENERIC_ADR_TEMPLATE.md` — durable architecture decisions
- `_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md` — trust boundaries, threats, and mitigations

**Does NOT load:** BRD/FSD templates, BA glossary (unless clarifying requirements).

---

## 🟣 Technical Leader (`technical-leader`)

**Profile SOUL.md:** `~/.hermes/profiles/technical-leader/SOUL.md` (197 lines)
**Custom skills:** `~/.hermes/skills/code-review/eksad-code-review/`, `~/.hermes/skills/technical-design/eksad-adr-workflow/`; use shared `~/.hermes/skills/security/eksad-appsec-review/` for triggered AppSec review
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/technical-leader.md`

**Primary job:** Code review, mentoring, ADR writing, BaseRepository guidance, PR checklist enforcement.

### Knowledge files to consult

**Always read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — 14 principles, forbidden patterns
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md` — full BE code rules

**For BE code review:**
- `_base/EKSAD_CRUDFLOWS_PATTERN.md` — CrudFlows v2 reactive (paired interfaces, all flow methods, auditMutator)
- `_base/EKSAD_CRUDFLOWS_JPA.md` — CrudFlows v2 blocking
- `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md` — architecture patterns
- `_base/EKSAD_SPRING_BOOT_MAPPINGS.md` — SB mapping
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — tech terms
- `_base/EKSAD_RESILIENCE_PATTERNS.md` — review resilience annotations
- `_base/EKSAD_OBSERVABILITY_PATTERNS.md` — review logging/tracing
- `_base/EKSAD_TESTING_GUIDE.md` — test quality review
- `_base/EKSAD_CORE_AUTH_CLIENT_SDK.md` — SDK usage
- `_base/EKSAD_CICD_CONTAINER_PATTERNS.md` — Dockerfile / CI review

**For FE code review:**
- `_base/EKSAD_FRONTEND_CODING_STANDARDS.md` v1.2 (2026-06-24)
- `_base/EKSAD_FRONTEND_PATTERNS.md`
- `_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md`
- `_base/EKSAD_FRONTEND_TESTING_GUIDE.md` v1.1

**Decision/security templates:**
- `_template/EKSAD_GENERIC_ADR_TEMPLATE.md`
- `_template/EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md`

**Does NOT load:** BRD/FSD templates, BA glossary (unless clarifying requirements).

---

## 🟠 Backend Developer (`developer-backend`)

**Profile SOUL.md:** `~/.hermes/profiles/developer-backend/SOUL.md` (253 lines)
**Custom skill:** `~/.hermes/skills/software-development/eksad-be-impl/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/developer-backend.md`

**Primary job:** Write Java/Quarkus/Spring Boot code: entities, repositories, services, REST resources, Flyway DDL, tests.

### Knowledge files to consult

**Must read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — 14 principles, tech stack, audit trail, module type, DDL standards, API catalog format
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CODING_STANDARDS.md` — MUST comply
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_PATTERN.md` — CrudFlows v2 reactive (paired interfaces, all flow methods, auditMutator)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_CRUDFLOWS_JPA.md` — CrudFlows v2 blocking (for SB / Quarkus-imperative)

**When implementing:**
- `_base/EKSAD_SYSTEM_DESIGN_PATTERNS.md`
- `_base/EKSAD_TESTING_GUIDE.md` — REST Assured, Testcontainers patterns
- `_base/EKSAD_SPRING_BOOT_MAPPINGS.md` — when Spring Boot project
- `_base/EKSAD_DOMAIN_GLOSSARY.md`
- `_base/EKSAD_CORE_AUTH_CLIENT_SDK.md` — SDK for svc-user-management
- `_base/EKSAD_RESERVED_FIELD_PATTERNS.md` — when transactional entity opts in
- `_base/EKSAD_RESILIENCE_PATTERNS.md` — @Retry, @CircuitBreaker, @Bulkhead
- `_base/EKSAD_OBSERVABILITY_PATTERNS.md` — logging, correlation ID
- `_base/EKSAD_CICD_CONTAINER_PATTERNS.md` — Dockerfile reference

**Reference TSD** at `_template/EKSAD_GENERIC_TSD_TEMPLATE.md` (filled per project at `/workspace/projects/<project>/TSD/`).

**Does NOT load:** BRD/FSD templates, FE patterns, BA glossary.

---

## 🟡 Frontend Developer (`developer-frontend`)

**Profile SOUL.md:** `~/.hermes/profiles/developer-frontend/SOUL.md` (263 lines)
**Custom skill:** `~/.hermes/skills/frontend/eksad-fe-impl/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/developer-frontend.md`

**Primary job:** React 18 + TS + Vite + TailwindCSS + RQ + RR + Axios + Day.js code. Monorepo packages.

### Knowledge files to consult

**Must read first (v1.2 — current standard):**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_CODING_STANDARDS.md` — MUST comply
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_PATTERNS.md` — form modes, multi-tab forms, inline editing
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md` — `@frontend/ui` components (don't recreate)
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_FRONTEND_TESTING_GUIDE.md` — v1.1, MSW for HTTP mocking

**When working with API contracts:**
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — cross-check entity field names
- `_base/EKSAD_RESERVED_FIELD_PATTERNS.md` — useReservedFields hook implementation
- `_base/EKSAD_CORE_AUTH_PATTERNS.md` — cookie auth patterns
- `_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` — FE-TSD structure

**Does NOT load:** BE coding standards, CrudFlows, event catalog, BRD/FSD templates.

---

## 🔴 QA Engineer (`qa-engineer`)

**Profile SOUL.md:** `~/.hermes/profiles/qa-engineer/SOUL.md` (231 lines)
**Custom skill:** `~/.hermes/skills/quality-assurance/eksad-qa-delivery/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/qa-engineer.md`

**Primary job:** Mode A black-box Test Plan, RTM, Test Case Matrix, and State Machine Matrix design; this Hermes profile produces no test code. Mode B automation remains with the in-IDE QA agent.

### Knowledge files to consult

**Always read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` — auth test scenarios (401/403), audit trail behavior, soft delete
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_TESTING_GUIDE.md` — test ownership, Mode A design, Mode B handoff contract, and black-box coverage rules

**For FE testing:**
- `_base/EKSAD_FRONTEND_TESTING_GUIDE.md` — v1.1, MSW for HTTP mocking
- `_base/EKSAD_FRONTEND_CODING_STANDARDS.md` — to know what code patterns to test

**For test derivation:**
- `_template/EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` — Test Plan + RTM source of truth
- `_template/EKSAD_GENERIC_FSD_TEMPLATE.md` — your primary input
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — cross-check field/term names
- `_base/EKSAD_LOAD_TESTING_GUIDE.md` — k6 / Gatling patterns

**Mode B reference (for handoff):**
- `vibe-coding/qa/COPILOT_QA_INSTRUCTIONS.md`
- `vibe-coding/qa/CURSOR_QA_RULES.md`
- `vibe-coding/qa/CLAUDE_CODE_QA_INSTRUCTIONS.md`

**Does NOT load:** coding standards, CrudFlows, BRD template, event catalog.

---

## ⚪ General Coordinator (`eksad-general`)

**Profile SOUL.md:** `~/.hermes/profiles/eksad-general/SOUL.md` (141 lines)
**Custom skills:** `~/.hermes/skills/productivity/stage-gated-orchestrator/` for visible cross-role pipelines and `~/.hermes/skills/productivity/eksad-create-project/` for project bootstrap; route specialist work to the corresponding profile/skill below
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/general.md`

**Primary job:** Cross-role intake, routing, dependency sequencing, handoff tracking, management overview, and attributable synthesis. The profile does not author or approve specialist-owned artifacts.

### Knowledge files to consult

**Coordinator references (read only as needed):**
- `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` — role/component/handoff map
- `_base/EKSAD_BASE_PRINCIPLES.md` — shared constraints for routing and consistency checks
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — shared terminology for attributable synthesis
- `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md` — governance and gate awareness; PM remains owner
- `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md` — delivery handoff awareness; DevOps remains owner

**Does NOT load by default:** the full knowledge pack, specialist authoring templates, coding standards, implementation patterns, or test-automation source guidance. Defer role-specific deep dives and production to the accountable specialist profile.

**Routing:** BA→`eksad-ba-workflow`; SA→`eksad-tsd-design`/`eksad-adr-workflow`; TL→`eksad-code-review`; Backend→`eksad-be-impl`; Frontend→`eksad-fe-impl`; QA→`eksad-qa-delivery`; PM→its profile-local `eksad-pm-delivery`; DevOps→its profile-local `eksad-devops-delivery`; Data Analyst→`eksad-data-analysis`; Data Scientist→`eksad-data-science`; UI/UX→`eksad-ui-ux-delivery`; Content Creator→`eksad-content-creation`. General Coordinator coordinates and never owns specialist outputs. **Canonical AppSec routing:** Any role may raise an AppSec trigger and supply evidence; the System Analyst or Technical Leader coordinates and invokes the shared `eksad-appsec-review` workflow; only the named risk authority accepts residual risk or grants a waiver. AppSec is not a profile.

---

## 🟤 Project Manager (`project-manager`)

**Profile SOUL.md:** `~/.hermes/profiles/project-manager/SOUL.md`
**Custom skill:** `~/.hermes/profiles/project-manager/skills/project-management/eksad-pm-delivery/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/project-manager.md`

**Primary job:** Project Charter, Project Plan, PM-owned WBS artifact/approved baseline, RAID, RACI/governance, evidence-based status, Change Requests, decisions/escalations, dependencies, stage-gate coordination, release readiness, and closure. Specialists own and validate their WBS task content, technical estimates, assumptions, and acceptance evidence.

### Knowledge files to consult

**Always read first:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md` — lifecycle, role boundaries, RAG, RAID, RACI, change control, gates
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_base/EKSAD_DOMAIN_GLOSSARY.md` — shared EKSAD terminology

**Templates:**
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_RAID_LOG_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_WBS_TEMPLATE.md`
- `~/.hermes/knowledge/eksad/EKSAD/gpt/_template/EKSAD_GENERIC_PROJECT_CLOSURE_TEMPLATE.md`

**Coordination:**
- Load only the PM profile-local `eksad-pm-delivery` runtime skill for substantive PM work. Do not load its global mirror, `stage-gated-orchestrator`, `eksad-task-breakdown`, or another role's skill in the PM profile.
- WBS output uses `EKSAD_GENERIC_WBS_TEMPLATE.md` and exact filename `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md`; approval does not authorize commit or push.

**Does NOT own:** UR/BRD/FSD authoring, architecture/TSD, technical estimates, code review, implementation, test execution, or proxy approval.

---

## 🟦 DevOps Engineer (`devops-engineer`)

**Profile SOUL.md:** `~/.hermes/profiles/devops-engineer/SOUL.md`
**Profile-local runtime skill:** `~/.hermes/profiles/devops-engineer/skills/devops/eksad-devops-delivery/`
**Global mirrored copy:** `~/.hermes/skills/devops/eksad-devops-delivery/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/devops-engineer.md`

**Primary job:** GitLab CE/Jenkins integration, CI/CD reliability, SonarQube and Trivy evidence through Jenkins, immutable artifact promotion, environment readiness, deployment, rollback, observability, release evidence, and incident handoff.

### Knowledge files to consult

**Always read first:**
- `_base/EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md` — factory components, trust boundaries, role handoffs, traceability, and three-VM topology
- `_base/EKSAD_DEVOPS_DELIVERY_STANDARD.md` — pipeline, environment, gate, production, evidence, rollback, and incident rules

**Operational references:**
- `_base/EKSAD_OBSERVABILITY_PATTERNS.md`
- `_base/EKSAD_RESILIENCE_PATTERNS.md`
- `_base/EKSAD_DB_DEPLOYMENT_STRATEGY.md`
- `_base/EKSAD_LOAD_TESTING_GUIDE.md`
- `_base/EKSAD_CICD_CONTAINER_PATTERNS.md`

**Templates:**
- `_template/EKSAD_GENERIC_CICD_PIPELINE_TEMPLATE.md`
- `_template/EKSAD_GENERIC_DEPLOYMENT_ROLLBACK_RUNBOOK_TEMPLATE.md`
- `_template/EKSAD_GENERIC_ENVIRONMENT_READINESS_TEMPLATE.md`
- `_template/EKSAD_GENERIC_RELEASE_EVIDENCE_TEMPLATE.md`
- `_template/EKSAD_GENERIC_INCIDENT_HANDOFF_TEMPLATE.md`

**Coordination:**
- Load only the DevOps profile-local `eksad-devops-delivery` runtime skill for substantive DevOps work. Do not load its global mirror, `stage-gated-orchestrator`, or another role's skill in the DevOps profile; it remains fail-closed for production.
- GitLab CE is source/review truth; Jenkins is CI/CD execution authority; SonarQube and Trivy run through Jenkins.

**Does NOT own:** BRD/FSD/TSD, application implementation, code-review verdict, QA verdict, PM governance, business acceptance, security-risk acceptance, or production authorization.

---


---

## 📊 Data Analyst (`data-analyst`)

**Profile SOUL.md:** `~/.hermes/profiles/data-analyst/SOUL.md`
**Custom skill:** `~/.hermes/skills/data-analysis/eksad-data-analysis/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/data-analyst.md`

**Primary job:** KPI/metric definitions, read-only data profiling, data analysis reports, data quality findings, and dashboard specifications.

### Knowledge files to consult

**Always read first:**
- `portable/roles/data-analyst.md` — canonical role boundary
- `portable/workflows/data-analysis-workflow.md` — analysis workflow
- `portable/deliverables/data-analysis-report.md` — report contract
- `portable/deliverables/dashboard-spec.md` — dashboard contract
- `portable/policies/role-boundaries.md` — authority boundaries
- `portable/rag/corpus-matrix.md` — retrieval scope
- `portable/llm-gateway/role-model-matrix.md` — model alias defaults

**When analyzing EKSAD artifacts:**
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — metric/business term consistency
- Activated project BRD/FSD/TSD/data dictionary only after project-specific activation

**Does NOT own:** business approval, DB writes, ETL/ELT implementation, ML experiments, production reporting publication, QA/release verdict, or credential handling.

---

## 🧪 Data Scientist (`data-scientist`)

**Profile SOUL.md:** `~/.hermes/profiles/data-scientist/SOUL.md`
**Custom skill:** `~/.hermes/skills/data-science/eksad-data-science/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/data-scientist.md`

**Primary job:** ML/statistical problem framing, data readiness assessment, experiment design, model evaluation, reproducibility notes, and model-risk handoff.

### Knowledge files to consult

**Always read first:**
- `portable/roles/data-scientist.md` — canonical role boundary
- `portable/workflows/data-science-workflow.md` — experiment workflow
- `portable/deliverables/ml-experiment-report.md` — experiment report contract
- `portable/policies/role-boundaries.md` — authority boundaries
- `portable/rag/corpus-matrix.md` — retrieval scope
- `portable/llm-gateway/role-model-matrix.md` — model alias defaults

**When experimenting:**
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — business/domain term alignment
- Data Analyst outputs and activated project data dictionary only after project-specific activation

**Does NOT own:** production deployment, MLOps platform design, production model promotion, business acceptance, QA verdict, AppSec verdict, or credential handling.

---

## 🎨 UI/UX Designer (`ui-ux-designer`)

**Profile SOUL.md:** `~/.hermes/profiles/ui-ux-designer/SOUL.md`
**Custom skill:** `~/.hermes/skills/design/eksad-ui-ux-delivery/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/ui-ux-designer.md`

**Primary job:** UX research, journey/task flows, information architecture, wireframe specifications, usability findings, accessibility notes, and frontend handoff.

### Knowledge files to consult

**Always read first:**
- `portable/roles/ui-ux-designer.md` — canonical role boundary
- `portable/workflows/ui-ux-workflow.md` — UX workflow
- `portable/deliverables/ux-research-report.md` — UX research contract
- `portable/deliverables/wireframe-handoff.md` — FE handoff contract
- `portable/policies/role-boundaries.md` — authority boundaries
- `portable/llm-gateway/role-model-matrix.md` — model alias defaults

**When designing EKSAD UI:**
- `_base/EKSAD_FRONTEND_COMPONENT_LIBRARY.md` — component vocabulary
- `_base/EKSAD_FRONTEND_PATTERNS.md` — UI/interaction patterns
- Activated BRD/FSD/FE-TSD/design assets only after project-specific activation

**Does NOT own:** frontend code, API contracts, DB/backend design, final business/legal approval, or release sign-off.

---

## ✍️ Content Creator (`content-creator`)

**Profile SOUL.md:** `~/.hermes/profiles/content-creator/SOUL.md`
**Custom skill:** `~/.hermes/skills/content/eksad-content-creation/`
**Extracted SI:** `~/.hermes/knowledge/eksad/role-system-instructions/content-creator.md`

**Primary job:** content briefs, source-backed drafts, release notes, help/training material, FAQs, copy variants, and content calendar planning.

### Knowledge files to consult

**Always read first:**
- `portable/roles/content-creator.md` — canonical role boundary
- `portable/workflows/content-creation-workflow.md` — content workflow
- `portable/deliverables/content-brief.md` — brief contract
- `portable/deliverables/content-calendar.md` — calendar contract
- `portable/policies/role-boundaries.md` — authority boundaries
- `portable/rag/corpus-matrix.md` — retrieval scope
- `portable/llm-gateway/role-model-matrix.md` — model alias defaults

**When drafting EKSAD content:**
- `_base/EKSAD_DOMAIN_GLOSSARY.md` — product/domain term consistency
- Activated BRD/FSD/release evidence/product briefs only after project-specific activation

**Does NOT own:** legal/regulatory approval, pricing/product policy, technical decisions, publication approval, QA/release verdict, or external publishing by default.

---

## 🔧 Custom EKSAD Skills Summary

| Skill | Path | When to load |
|-------|------|--------------|
| `eksad-ba-workflow` | `~/.hermes/skills/business-analysis/eksad-ba-workflow/` | BA in UR→BRD→FSD pipeline |
| `eksad-tsd-design` | `~/.hermes/skills/technical-design/eksad-tsd-design/` | SA writing TSD |
| `eksad-adr-workflow` | `~/.hermes/skills/technical-design/eksad-adr-workflow/` | SA/TL recording a durable architecture decision |
| `eksad-code-review` | `~/.hermes/skills/code-review/eksad-code-review/` | TL reviewing PR |
| `eksad-be-impl` | `~/.hermes/skills/software-development/eksad-be-impl/` | Dev-BE implementing an approved design |
| `eksad-fe-impl` | `~/.hermes/skills/frontend/eksad-fe-impl/` | Dev-FE implementing feature |
| `eksad-qa-delivery` | `~/.hermes/skills/quality-assurance/eksad-qa-delivery/` | QA test design, automation handoff, and evidence |
| `eksad-appsec-review` | `~/.hermes/skills/security/eksad-appsec-review/` | Shared SA/TL workflow for triggered AppSec review; not a profile |
| `eksad-create-project` | `~/.hermes/skills/productivity/eksad-create-project/` | Bootstrap new project from template |
| `eksad-task-breakdown` | `~/.hermes/skills/technical-design/eksad-task-breakdown/` | WBS / sprint planning per role |
| `stage-gated-orchestrator` | `~/.hermes/skills/productivity/stage-gated-orchestrator/` | General Coordinator pipeline: HITL by default; optional no-gates mode; not installed in PM profile |
| `eksad-pm-delivery` | `~/.hermes/profiles/project-manager/skills/project-management/eksad-pm-delivery/` | Charter, Plan, PM-owned WBS baseline, RAID, status, changes, and delivery gates |
| `eksad-devops-delivery` | `~/.hermes/profiles/devops-engineer/skills/devops/eksad-devops-delivery/` (also mirrored globally) | GitLab/Jenkins delivery, quality/security evidence, deployment, rollback, and release readiness |
| `eksad-data-analysis` | `~/.hermes/skills/data-analysis/eksad-data-analysis/` | KPI definitions, read-only data analysis, data quality findings, and dashboard specs |
| `eksad-data-science` | `~/.hermes/skills/data-science/eksad-data-science/` | ML/statistical experiment design, evaluation, reproducibility, and model-risk handoff |
| `eksad-ui-ux-delivery` | `~/.hermes/skills/design/eksad-ui-ux-delivery/` | UX research, wireframes, usability findings, and frontend handoff |
| `eksad-content-creation` | `~/.hermes/skills/content/eksad-content-creation/` | Source-backed content drafts, release notes, help/training material, and content calendars |

---

## 📊 Coverage Matrix

| Pattern / Standard | BA | SA | TL | Dev-BE | Dev-FE | QA | PM | DevOps | General Coordinator |
|---------------------|----|----|----|----|----|----|----|----|----|
| BRD template | ✅ | — | — | — | — | — | Review/gate | Handoff only | Route only |
| FSD template | ✅ | — | — | — | — | ✅ | Review/gate | Consume NFRs | Route only |
| TSD / FE-TSD | — | ✅ | ✅ | ✅ | ✅ | — | Review/gate | Consume approved deployment design | Route only |
| Architecture doc | — | ✅ | ✅ | — | — | — | Review/gate | Implement approved operational design | Overview |
| AI Software Factory Architecture | Awareness | ✅ | ✅ | Awareness | Awareness | Awareness | Governance | ✅ | Overview/routing |
| Project Management Standard/templates | — | — | — | — | — | — | ✅ | Handoff only | Overview |
| DevOps Delivery Standard | — | Awareness | Review | Handoff | Handoff | Evidence consumer | Gate coordination | ✅ | Overview/routing |
| CI/CD Pipeline template | — | Input | Review | Input | Input | Evidence consumer | Track gate | ✅ | — |
| Environment / Deploy / Release / Incident templates | — | Input | Review | Handoff | Handoff | Evidence input | Track gate | ✅ | — |
| Base Principles | ✅ | ✅ | ✅ | ✅ | — | ✅ | Awareness | Awareness | Overview |
| Coding Standards (BE) | — | ✅ | ✅ | ✅ | — | — | — | Pipeline evidence only | — |
| Frontend Coding Standards | — | — | ✅ | — | ✅ | — | — | Pipeline evidence only | — |
| CrudFlows v2 | — | ✅ | ✅ | ✅ | — | — | — | Build/test evidence only | — |
| Domain Registry / Glossary | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Awareness | Overview |
| Master Data / Event / Reserved Fields | Varies | ✅ | Varies | Varies | Varies | Varies | Awareness | Operational implications | Route only |
| Testing Guides | — | — | ✅ | ✅ | ✅ | ✅ | — | Execute configured stages; no QA verdict | — |
| Load Testing | — | — | Review | — | — | ✅ | Track evidence | Environment/tooling evidence | — |
| Resilience Patterns | — | ✅ | ✅ | ✅ | — | Test input | Awareness | Operational verification | — |
| Observability | — | ✅ | ✅ | ✅ | — | Evidence input | Status evidence | ✅ | Overview |
| GitLab CE / Jenkins CI/CD | — | Design input | Review | Source handoff | Source handoff | Test evidence | Gate tracking | ✅ | Route only |
| SonarQube / Trivy via Jenkins | — | Policy/design input | Technical review | Remediation input | Remediation input | Evidence consumer | Gate tracking | ✅ | Route only |


### Phase E role extension coverage

| Pattern / Standard | Data Analyst | Data Scientist | UI/UX | Content Creator |
|---|---|---|---|---|
| Role boundary | ✅ | ✅ | ✅ | ✅ |
| Workflow contract | `data-analysis-workflow.md` | `data-science-workflow.md` | `ui-ux-workflow.md` | `content-creation-workflow.md` |
| Deliverables | Analysis report, dashboard spec | ML experiment report | UX research, wireframe handoff | Content brief, content calendar |
| RAG usage | Cited specs/data docs | Cited specs/data docs | Cited specs/design refs | Cited specs/release/product refs |
| MCP stance | Read-only data/BI | Sandbox/read-only data | Browser/design read-only | Draft-only content/read-only refs |
| Approval boundary | No business decision | No production promotion | No frontend implementation | No publication/legal approval |

---

**Last updated:** 2026-07-16
**Pack version:** v31 + Phase E Role Expansion Pack
**Source branch:** `feature/eksad-knowledge-v3`