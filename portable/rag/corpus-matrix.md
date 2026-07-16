# RAG Corpus Matrix

| Role | Default corpora | Conditional project corpora |
|---|---|---|
| `general-coordinator` | `eksad-core`, `eksad-portable-governance` | Corpus index/project activation metadata only after approval |
| `business-analyst` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-design-assets-example`, `project-release-content-example` after activation |
| `system-analyst` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-design-assets-example` after activation |
| `technical-leader` | `eksad-core`, `eksad-role-instructions`, `eksad-portable-governance` | all split project corpora after explicit review need |
| `developer-backend` | `eksad-core`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example` after implementation scope activation |
| `developer-frontend` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-design-assets-example` after implementation scope activation |
| `qa-engineer` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | all split project corpora after test/evidence scope activation |
| `project-manager` | `eksad-core`, `eksad-portable-governance` | `project-specs-example`, `project-data-evidence-example`, `project-release-content-example` after governance activation |
| `devops-engineer` | `eksad-core`, `eksad-portable-governance` | `project-specs-example`, `project-release-content-example` after release/evidence activation |
| `data-analyst` | `eksad-core`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-data-evidence-example` after data owner approval |
| `data-scientist` | `eksad-core`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-data-evidence-example` after data owner approval |
| `ui-ux-designer` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-design-assets-example`, `project-release-content-example` after design/content scope activation |
| `content-creator` | `eksad-core`, `eksad-templates`, `eksad-role-instructions`, `eksad-portable-governance` | `project-specs-example`, `project-design-assets-example`, `project-release-content-example` after publication/content approval |

Project-specific corpora are disabled by default. Activation requires explicit project scope, sensitivity review, and role access approval.
