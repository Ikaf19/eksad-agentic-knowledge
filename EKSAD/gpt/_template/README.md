# EKSAD Document Templates (`_template/`)

**Purpose:** Generic document scaffolds for EKSAD requirements, design, architecture, regulatory, project-management, and DevOps operational artifacts.
These are **fill-in templates**. Do NOT store project-specific completed documents here.

---

## Files

| File | Document Type | Current Version | Primary Audience | Upload To GPT |
|------|--------------|----------------|-----------------|---------------|
| `EKSAD_GENERIC_BRD_TEMPLATE.md` | Business Requirements Document | v3.2 | Business Analyst | BA GPT, General GPT |
| `EKSAD_GENERIC_UR_TEMPLATE.md` | User Requirements | v1.0 | Business Analyst / Product Owner | BA GPT, General GPT |
| `EKSAD_GENERIC_REGULATORY_TEMPLATE.md` | Regulatory & Compliance Reference | v1.0 | BA / Compliance | BA GPT |
| `EKSAD_GENERIC_FSD_TEMPLATE.md` | Functional Specification Document | v3.0 | System Analyst / BA / QA | BA GPT, QA GPT, General GPT |
| `EKSAD_GENERIC_TSD_TEMPLATE.md` | Technical Specification Document — Backend | v3.0 | System Analyst / Tech Lead | SA GPT, TL GPT, Dev GPT, General GPT |
| `EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | Technical Specification Document — Frontend | v3.0 *(English-only)* | System Analyst / Tech Lead / FE Dev | SA GPT, TL GPT, Dev FE GPT |
| `EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` | Project Architecture Document | v1.0 | System Analyst / Architect / TL | SA GPT, TL GPT |
| `EKSAD_GENERIC_ADR_TEMPLATE.md` | Architecture Decision Record | v1.0 | System Analyst / Technical Leader | SA GPT, TL GPT |
| `EKSAD_GENERIC_THREAT_MODEL_TEMPLATE.md` | Application Security Threat Model | v1.0 | SA / TL / shared AppSec reviewer | SA GPT, TL GPT |
| `EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` | Test Plan and Requirement Traceability Matrix | v1.0 | QA Engineer | QA GPT |
| `EKSAD_GENERIC_WBS_TEMPLATE.md` | Work Breakdown Structure | v1.0 | PM / workstream leads | PM GPT |
| `EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md` | Project Charter | v1.0 | Project Manager / Sponsor | PM GPT |
| `EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md` | Project Plan | v1.0 | Project Manager / Workstream Leads | PM GPT |
| `EKSAD_GENERIC_RAID_LOG_TEMPLATE.md` | RAID Log | v1.0 | Project Manager / Owners | PM GPT |
| `EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md` | Project Status Report | v1.0 | Project Manager / Steering | PM GPT |
| `EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md` | Change Request | v1.0 | Project Manager / Decision Authority | PM GPT |
| `EKSAD_GENERIC_CICD_PIPELINE_TEMPLATE.md` | CI/CD Pipeline Design | v1.0 | DevOps / TL | DevOps GPT |
| `EKSAD_GENERIC_ENVIRONMENT_READINESS_TEMPLATE.md` | Environment Readiness | v1.0 | DevOps / Operations | DevOps GPT |
| `EKSAD_GENERIC_DEPLOYMENT_ROLLBACK_RUNBOOK_TEMPLATE.md` | Deployment/Rollback Runbook | v1.0 | DevOps / Release Authority | DevOps GPT |
| `EKSAD_GENERIC_RELEASE_EVIDENCE_TEMPLATE.md` | Release Evidence Pack | v1.0 | DevOps / PM / Release Authority | DevOps GPT |
| `EKSAD_GENERIC_INCIDENT_HANDOFF_TEMPLATE.md` | Incident Handoff | v1.0 | DevOps / Operations | DevOps GPT |
| `EKSAD_GENERIC_PROJECT_CLOSURE_TEMPLATE.md` | Project Closure Record | v1.0 | Project Manager / Sponsor | PM GPT |

---

## What's New in v3 (FSD, TSD, FE-TSD)

All three v3 templates share the following structural upgrades over v2:

| Improvement | Detail |
|---|---|
| **Document Control table** | Formal metadata block: Title, Type, Version, Status, System, Related BRD/FSD/TSD, Prepared/Reviewed/Approved By, Last Updated |
| **Revision History + Approval blocks** | Moved to top of document; Approval includes Lead SA / Tech Lead (TSD) or Tech Lead Frontend (FE-TSD) |
| **Introduction section** | Purpose, Scope, Intended Audience table |
| **Traceability Matrix** | Full chain: `FR ID → Feature ID → Class → Method` (TSD) or `FR ID → Feature ID → Screen → Component → Hook/Service Function` (FE-TSD) |
| **FR ref comments in code** | Every method in Java skeletons and TypeScript hooks/services includes `// FR-{MODULE}-{N}` comment |
| **`[STALE]` tagging convention** | Mark outdated Traceability Matrix rows; do not delete until resolved |
| **Global Rules section** | TRULE-001–011 (TSD) / FERULE-001–010 (FE-TSD) as enforceable rule tables |
| **Gap Analysis section** | Critical vs Non-Critical severity; blocks approval if Critical gaps remain |
| **Open Issues & Decisions Log** | Must be empty before status = Approved |
| **Glossary** | Full platform term definitions including `[STALE]`, `FR ID`, `Feature ID` |
| **FE-TSD: Feature Functional Requirements (Web)** | Per-feature web-scoped Given/When/Then, role-based rendering table, state machine rendering table |
| **FE-TSD: English-only** | Fully converted from Bahasa Indonesia; language policy note in Document Control |

---

## Usage

1. **Copy** the relevant template to your project folder (e.g., `TIA/`, `HR/`).
2. **Rename** following the convention below.
3. **Replace** all `{PLACEHOLDER}` tokens with actual project values.
4. **Never modify** the template originals in this folder.

---

## Document Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| UR | `UR_{PROJECT_CODE}_v{VERSION}.md` | `UR_TIA_v1.0.md` |
| BRD | `BRD_{PROJECT_CODE}_v{VERSION}.md` | `BRD_TIA_v1.0.md` |
| FSD | `FSD_{PROJECT_CODE}_v{VERSION}.md` | `FSD_TIA_v2.2.md` |
| TSD (Backend) | `TSD_{PROJECT_CODE}_v{VERSION}.md` | `TSD_TIA_v1.0.md` |
| TSD (Frontend) | `TSD_FE_{PROJECT_CODE}_v{VERSION}.md` | `TSD_FE_TIA_v1.0.md` |
| ADR | `ADR-{PROJECT_CODE}-{NNN}_{SHORT_TITLE}.md` | `ADR-TIA-001_AUTH_BOUNDARY.md` |
| Threat Model | `{PROJECT_CODE}_THREAT_MODEL_{SCOPE}_v{VERSION}.md` | `TIA_THREAT_MODEL_AUTH_v1.0.md` |
| Test Plan / RTM | `TESTPLAN_{MODULE_CODE}_v{VERSION}.md` | `TESTPLAN_AUTH_v1.0.md` |
| WBS | `{PROJECT_CODE}_WBS_{SCOPE}_v{VERSION}.md` | `TIA_WBS_AUTH_v1.0.md` |
| Project Charter | `{PROJECT_CODE}_PROJECT_CHARTER.md` | `TIA_PROJECT_CHARTER.md` |
| Project Plan | `{PROJECT_CODE}_PROJECT_PLAN.md` | `TIA_PROJECT_PLAN.md` |
| RAID Log | `{PROJECT_CODE}_RAID_LOG.md` | `TIA_RAID_LOG.md` |
| Status Report | `{PROJECT_CODE}_STATUS_{YYYYMMDD}.md` | `TIA_STATUS_20260710.md` |
| Change Request | `{PROJECT_CODE}_CR_{NNN}.md` | `TIA_CR_001.md` |
| CI/CD Pipeline | `{PROJECT_CODE}_CICD_PIPELINE.md` | `TIA_CICD_PIPELINE.md` |
| Environment Readiness | `{PROJECT_CODE}_{ENV}_ENVIRONMENT_READINESS.md` | `TIA_PROD_ENVIRONMENT_READINESS.md` |
| Deployment/Rollback Runbook | `{PROJECT_CODE}_{ENV}_DEPLOYMENT_ROLLBACK_RUNBOOK.md` | `TIA_PROD_DEPLOYMENT_ROLLBACK_RUNBOOK.md` |
| Release Evidence | `{PROJECT_CODE}_{ENV}_RELEASE_EVIDENCE_{VERSION}.md` | `TIA_PROD_RELEASE_EVIDENCE_1.0.md` |
| Incident Handoff | `{PROJECT_CODE}_INCIDENT_{ID}_HANDOFF.md` | `TIA_INCIDENT_INC001_HANDOFF.md` |
| Project Closure | `{PROJECT_CODE}_PROJECT_CLOSURE_v{VERSION}.md` | `TIA_PROJECT_CLOSURE_v1.0.md` |

---

## Archive Policy

Previous versions of templates are preserved in [`archive/`](archive/). Do not delete archive files.

| File | Archived Version | Reason |
|------|----------------|--------|
| `archive/EKSAD_GENERIC_BRD_TEMPLATE_v2.0.md` | v2.0 | Superseded by current version |
| `archive/EKSAD_GENERIC_FSD_TEMPLATE_v2.0.md` | v2.0 | Superseded by v3.0 (2026-05-02) |
| `archive/EKSAD_GENERIC_TSD_TEMPLATE_v2.0.md` | v2.0 | Superseded by v3.0 (2026-05-02) |
| `archive/EKSAD_GENERIC_FE_TSD_TEMPLATE_v2.0.md` | v2.0 | Superseded by v3.0 (2026-05-02) |

---

> See `gpt/README.md` for the full GPT setup guide and maintenance policy.