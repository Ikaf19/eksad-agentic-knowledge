# EKSAD Role Collaboration Matrix

This matrix defines how role agents may collaborate through artifacts. Collaboration does **not** transfer ownership or approval authority.

Legend:

- **Consumes** — role may read/use the artifact as evidence.
- **Produces** — role creates the artifact or handoff note.
- **Reviews** — role may review within its accountability boundary.
- **Approves** — role/human gate that can approve the artifact or decision.
- **Escalates** — role to notify when the current role cannot own the decision.

## Primary artifact flow

| Stage / artifact | Produces | Consumes | Reviews | Approves / gates | Escalates when |
|---|---|---|---|---|---|
| Intake / routing note | General Coordinator | All relevant roles | PM, owning role | User / PM for scope | ownership unclear, missing source, cross-role conflict |
| UR / BRD / FSD | Business Analyst | SA, TL, PM, QA, UI/UX, Content, Data roles | PM, SA/TL for feasibility comments | Business owner / BA gate | technical design required, ambiguity, scope conflict |
| TSD / architecture / API / ERD / event schema | System Analyst | TL, Dev-BE, Dev-FE, QA, DevOps, Data roles | TL, AppSec trigger owner | SA/TL technical gate | security risk, cross-service impact, data/privacy risk |
| ADR | System Analyst or Technical Leader | PM, Dev, QA, DevOps | TL | Architecture governance / named approver | irreversible trade-off, production/platform impact |
| Backend implementation handoff | Developer Backend | TL, QA, DevOps, PM | TL, QA | TL/code review + CI gate | design ambiguity, data/schema mismatch, security trigger |
| Frontend implementation handoff | Developer Frontend | TL, QA, UI/UX, PM | TL, QA, UI/UX for design intent | TL/code review + QA gate | design/contract mismatch, accessibility risk |
| Test plan / RTM / QA evidence | QA Engineer | PM, TL, Dev, DevOps, BA/SA | TL/PM for release readiness | QA verdict recommendation + release gate | missing acceptance criteria, unstable evidence, risk acceptance |
| Project plan / WBS / RAID / status | Project Manager | All roles | Owning specialists validate their pieces | PM/governance gate | estimate uncertainty, dependency/risk/change approval needed |
| Release evidence / operational readiness | DevOps Engineer | PM, TL, QA, Dev | TL/QA/PM | Release/deployment gate | production impact, rollback gap, security/compliance risk |
| Data analysis report / dashboard spec | Data Analyst | BA, PM, TL, QA, Data Scientist, Content | Data owner / BA/PM for business interpretation | Data owner / business owner | source quality issue, metric ambiguity, remediation needed |
| ML experiment report | Data Scientist | SA, TL, PM, Data Analyst, DevOps, QA | TL/Data owner | ML/business/platform approval gate | productionization, bias/fairness/privacy risk, rollback gap |
| UX research / wireframe handoff | UI/UX Designer | BA, SA, Dev-FE, QA, PM, Content | BA/PM for product fit; FE/TL for feasibility comments | Product/design owner | implementation feasibility issue, accessibility/usability conflict |
| Content brief / calendar / user guide / release notes | Content Creator | BA, PM, QA, UI/UX, DevOps | Product/legal/regulatory owner as applicable | Publication owner / PM | claim lacks approved source, regulated statement, release mismatch |

## Cross-role rules

1. A consuming role must cite the source artifact and evidence cut-off where required by RAG policy.
2. A reviewing role may annotate risks/gaps but does not become owner unless explicitly assigned.
3. Optional MCP/RAG/model access does not grant authority to approve, publish, merge, deploy, accept security risk, or export data.
4. When a role detects a boundary crossing, it must produce a handoff note instead of silently taking over.
5. General Coordinator may aggregate status and route tasks, but it does not author or approve specialist deliverables.

## Handoff note minimum fields

- Source artifact(s) and version/cut-off.
- Requested output or decision.
- Owning role and approver/gate.
- Evidence used and citation requirement.
- Open questions, risks, assumptions, and blockers.
- Recommended next role(s).
