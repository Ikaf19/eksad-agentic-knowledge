# Hermes Role Model Policy

| Hermes profile | Primary alias | Escalation alias | Notes |
|---|---|---|---|
| `general-coordinator` | `eksad.fast` | `eksad.reasoning` | Routing/intake first. |
| `business-analyst` | `eksad.default` | `eksad.reasoning` / `eksad.long_context` | Use citations for BRD/FSD evidence. |
| `system-analyst` | `eksad.reasoning` | `eksad.long_context` | TSD/API/ERD decisions. |
| `technical-leader` | `eksad.reasoning` | `eksad.guardrail` | Review and approval gate. |
| `developer-backend` | `eksad.default` | `eksad.reasoning` | Code/design support, no direct prod action. |
| `developer-frontend` | `eksad.default` | `eksad.reasoning` | UI implementation/review. |
| `qa-engineer` | `eksad.default` | `eksad.long_context` | Test plan/RTM/evidence review. |
| `devops-engineer` | `eksad.default` | `eksad.guardrail` / `eksad.reasoning` | Production writes remain approval-gated. |

Profiles should not embed provider names or API keys. They may reference aliases only.
