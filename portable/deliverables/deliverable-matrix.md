# Deliverable Matrix

This matrix separates **artifact/template availability** from **workflow maturity**. An available template does not mean its end-to-end runtime workflow or approval automation is active.

- **Canonical:** portable ownership/workflow and source template or artifact contract are defined; approvals and runtime actions remain human-owned unless separately activated.
- **Partial:** a source artifact/template exists, but the portable end-to-end workflow or evidence/gate contract still needs normalization.

| Deliverable | Primary role | Source/template | Template/artifact status | Workflow maturity |
|---|---|---|---|---|
| UR | Business Analyst | `EKSAD/gpt/_template/EKSAD_GENERIC_UR_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| BRD | Business Analyst | `EKSAD/gpt/_template/EKSAD_GENERIC_BRD_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| FSD | Business Analyst | `EKSAD/gpt/_template/EKSAD_GENERIC_FSD_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| TSD | System Analyst | `EKSAD/gpt/_template/EKSAD_GENERIC_TSD_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| FE-TSD | System Analyst / Frontend | `EKSAD/gpt/_template/EKSAD_GENERIC_FE_TSD_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| Architecture Doc | System Analyst | `EKSAD/gpt/_template/EKSAD_ARCHITECTURE_DOC_TEMPLATE.md` | Available | Partial; portable workflow is currently a generic skeleton |
| ADR | System Analyst or Technical Leader | `EKSAD/gpt/_template/EKSAD_GENERIC_ADR_TEMPLATE.md` + ADR skill | Available | Partial; governance gate remains human-owned |
| WBS | Project Manager | `EKSAD/gpt/_template/EKSAD_GENERIC_WBS_TEMPLATE.md` + PM skill | Available | Partial; planning/gate workflow remains human-owned |
| Test Plan / RTM | QA Engineer | `EKSAD/gpt/_template/EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` | Available | Partial; Mode A/evidence invariants still need portable workflow enrichment |
| Code Review Findings | Technical Leader | `portable/deliverables/code-review-findings.md` | Available | Partial; portable contract exists and workflow enrichment remains |
| Release Evidence | DevOps Engineer / Project Manager | `EKSAD/gpt/_template/EKSAD_GENERIC_RELEASE_EVIDENCE_TEMPLATE.md` | Available | Partial; release approval and runtime action remain gated |
| Data Analysis Report | Data Analyst | `portable/deliverables/data-analysis-report.md` | Available | Canonical |
| Dashboard Specification | Data Analyst | `portable/deliverables/dashboard-spec.md` | Available | Canonical |
| ML Experiment Report | Data Scientist | `portable/deliverables/ml-experiment-report.md` | Available | Canonical |
| UX Research Report | UI/UX Designer | `portable/deliverables/ux-research-report.md` | Available | Canonical |
| Wireframe Handoff | UI/UX Designer | `portable/deliverables/wireframe-handoff.md` | Available | Canonical |
| Content Brief | Content Creator | `portable/deliverables/content-brief.md` | Available | Canonical |
| Content Calendar | Content Creator | `portable/deliverables/content-calendar.md` | Available | Canonical |

## Canonical roles covered

`general-coordinator`, `business-analyst`, `system-analyst`, `technical-leader`, `developer-backend`, `developer-frontend`, `qa-engineer`, `project-manager`, `devops-engineer`, `data-analyst`, `data-scientist`, `ui-ux-designer`, `content-creator`.
