# EKSAD Role Boundaries

## Principle

Each EKSAD role owns specific decisions and deliverables. Tool access, MCP access, RAG access, or runtime agent capability must not expand role authority.

## Boundary rules

1. BA owns business requirements; SA owns technical design.
2. TL owns technical review/governance; Dev owns implementation.
3. QA owns test plan/evidence/verdict recommendation; QA does not own code implementation in Mode A.
4. PM owns coordination and stage gates; PM does not make specialist technical verdicts.
5. DevOps owns operational readiness/evidence; production action remains gated.
6. General Coordinator routes and summarizes; it does not own specialist deliverables.
7. Data Analyst owns metric/data analysis artifacts; business interpretation approval and data-source remediation remain with named owners.
8. Data Scientist owns experiment/evaluation evidence; production ML design, deployment, and promotion remain gated through SA/TL/DevOps/MLOps/business authority.
9. UI/UX Designer owns design intent and usability evidence; frontend implementation and technical feasibility verdicts remain with SA/Frontend/TL.
10. Content Creator owns sourced drafts and content planning; legal/regulatory/product approval and publication remain with named approvers.

## Escalation

When a task crosses role boundaries, produce a handoff note rather than silently taking ownership. A handoff note should include requested output, source artifacts, evidence cut-off, owner, approval/gate state, and unresolved gaps.
## Canonical roles covered

`general-coordinator`, `business-analyst`, `system-analyst`, `technical-leader`, `developer-backend`, `developer-frontend`, `qa-engineer`, `project-manager`, `devops-engineer`, `data-analyst`, `data-scientist`, `ui-ux-designer`, `content-creator`.
