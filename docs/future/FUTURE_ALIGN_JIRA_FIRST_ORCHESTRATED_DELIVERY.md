# Future Alignment Plan — JIRA-First Orchestrated Delivery

**Status:** Future candidate / parked backlog  
**Created:** 2026-07-16  
**Scope type:** Git source-of-truth planning, not runtime activation  
**Dependency:** Future orchestrator layer + Web Portal external work item support  
**Runtime mutation policy:** Do not create/update JIRA cards, write JIRA comments, transition JIRA workflow state, deploy an orchestrator, or mutate live Hermes/Web Portal/JIRA runtime from this plan without a separate explicit approval gate.

---

## 1. Why this is future work

EKSAD's current architecture starts with Git source-of-truth and independent Hermes role agents. Without a central orchestrator, JIRA-first delivery can only be **manual/link-assisted**, not automated.

Therefore:

```text
Now: JIRA-linked manual delivery
Later: JIRA-first orchestrated delivery
```

This plan parks the future orchestrated mode without changing the current Phase 1 baseline.

---

## 2. Current baseline

| Area | Current supported behavior |
|---|---|
| Git source-of-truth | Defines policies, role boundaries, templates, and delivery profile contracts. |
| Hermes role agents | Run per role when a human/operator invokes them. |
| Web Portal future plan | Can include generic project, agent, delivery profile, and external work item link concepts. |
| JIRA usage | Link-only/manual context through `ExternalWorkItemLink`; no write integration. |
| Orchestrator | Not yet active as a source-of-truth/runtime layer. |

---

## 3. Target future behavior

Future `jira-first-orchestrated` delivery should allow:

```text
Approved JIRA requirement card
  -> Portal validates DeliveryProfile + ExternalWorkItemLink
  -> Orchestrator validates approval gate and required fields
  -> Orchestrator dispatches UI/UX / SA / TL / Dev / QA / DevOps role graph
  -> Evidence is linked back to Portal/JIRA/Git artifacts
```

The approved card becomes a lightweight requirement baseline only after required gates pass.

---

## 4. Workstreams

| Workstream | Name | Intent |
|---|---|---|
| JFD-01 | JIRA Card Contract | Define required fields, approved statuses, evidence references, and status mapping. |
| JFD-02 | Delivery Profile Binding | Bind `jira-first-orchestrated` to required roles, BA escalation triggers, and gate semantics. |
| JFD-03 | Portal Work Item Integration | Define Portal handling of `ExternalWorkItemLink`, disabled states, read-only sync, and evidence linking. |
| JFD-04 | Orchestrator Workflow Contract | Define role graph, handoff manifest, gate state, retry/block behavior, and audit events. |
| JFD-05 | Controlled Read-Only Pilot | Prove approved-card intake using read-only JIRA metadata before any write behavior is considered. |

---

## 5. Explicit non-goals

This plan does not approve:

- JIRA card creation from Portal;
- JIRA status transitions from Portal or agents;
- JIRA comment writeback from agents;
- JIRA attachment upload;
- JIRA assignment/sprint mutation;
- JIRA API token storage in Git;
- production orchestrator deployment;
- automatic Dev execution from a linked card.

---

## 6. Required source-of-truth files before activation

```text
portable/portal/
  external-work-item-link-model.md
  delivery-profile-model.md
  jira-first-orchestrator-dependency.md

future orchestrator source-of-truth, later:
  orchestrator/README.md
  orchestrator/ROLE_GRAPH_MODEL.md
  orchestrator/GATE_STATE_MODEL.md
  orchestrator/HANDOFF_EVIDENCE_REGISTRY.md
  orchestrator/PORTAL_RUNTIME_CONTRACT.md

future JIRA integration source-of-truth, later:
  work-management/jira/README.md
  work-management/jira/JIRA_CARD_CONTRACT.md
  work-management/jira/JIRA_READONLY_CONNECTOR_CONTRACT.md
  work-management/jira/JIRA_WRITE_INTEGRATION_SECURITY_MODEL.md  # only if separately approved
```

---

## 7. Activation gate

`jira-first-orchestrated` remains disabled unless all are true:

- Orchestrator layer is defined and approved.
- Web Portal can store `ExternalWorkItemLink` safely.
- `DeliveryProfile` resolver can disable unavailable modes.
- JIRA read-only integration has explicit runtime approval.
- Human approval gates are recorded with actor/date/evidence.
- No write behavior is implied by read-only sync.

---

## 8. Relationship to Web Portal Control Plane

This plan extends `docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md` but should not overload WPC-01.

Recommended split:

```text
WPC = generic portal control-plane foundation
ORC = future orchestrator layer
JFD = JIRA-first delivery profile that depends on ORC + WPC
```
