# DeliveryProfile Model

**Status:** Portable contract / Git-only desired state  
**Last updated:** 2026-07-16  
**Primary consumer:** Future Web Portal, orchestrator, General Coordinator, Project Manager, and role-agent routing policy  
**Runtime mutation policy:** Delivery profiles define allowed workflow behavior. They do not activate runtime integrations or mutate JIRA, Hermes, LiteLLM, MCP, RAG, Keycloak, or Git remotes.

---

## 1. Intent

`DeliveryProfile` defines how a project turns intake into role-agent work while preserving EKSAD role boundaries and approval gates.

It answers:

- what the requirement source is;
- whether formal BA artifacts are mandatory;
- which roles are active by default;
- which human approval gate unlocks downstream work;
- whether an orchestrator is required;
- whether external work-management integration is read-only or write-capable.

---

## 2. Canonical fields

```yaml
delivery_profile:
  id: formal-spec-driven | manual-agent-assisted | jira-linked-manual | jira-first-orchestrated
  name: <human-readable-name>
  status: active | planned | disabled
  requirement_source: git_artifact | user_prompt | external_work_item | mixed
  formal_ba_artifacts_required: true | false | conditional
  ba_involvement: required | trigger_based | optional
  orchestrator_required: true | false
  external_work_item_required: true | false
  external_work_item_sync_mode: none | manual_snapshot | read_only | orchestrator_managed
  jira_write_allowed: false
  approval_gate:
    type: document_approval | user_approved_card | manual_user_decision | orchestrator_gate
    unlocks:
      - ui_ux_triage
      - system_analysis
      - tl_review
      - development_handoff
      - qa_verification
      - devops_readiness
  active_roles:
    - project-manager
    - ui-ux-designer
    - system-analyst
    - technical-leader
    - developer-backend
    - developer-frontend
    - qa-engineer
    - devops-engineer
  optional_roles:
    - business-analyst
  escalation_triggers:
    business-analyst:
      - ambiguous requirement
      - missing acceptance criteria
      - multi-stakeholder conflict
      - regulatory or contractual impact
      - epic spans multiple modules or sprints
```

---

## 3. Baseline delivery profiles

| Profile | Status | Use when | Orchestrator required? | JIRA write allowed? |
|---|---|---|---:|---:|
| `formal-spec-driven` | Active | Project follows UR/BRD/FSD/TSD/WBS gate flow. | No | No |
| `manual-agent-assisted` | Active | User/operator manually routes work to role agents from chat/portal context. | No | No |
| `jira-linked-manual` | Active | A JIRA issue is linked as context/evidence, but humans manually route Hermes role work. | No | No |
| `jira-first-orchestrated` | Planned / disabled until orchestrator exists | Approved JIRA card should drive role graph execution. | Yes | No in current baseline |

---

## 4. Active profile: `jira-linked-manual`

This profile is the safe Phase 1-compatible bridge.

```yaml
delivery_profile:
  id: jira-linked-manual
  status: active
  requirement_source: external_work_item
  formal_ba_artifacts_required: conditional
  ba_involvement: trigger_based
  orchestrator_required: false
  external_work_item_required: true
  external_work_item_sync_mode: manual_snapshot
  jira_write_allowed: false
  approval_gate:
    type: manual_user_decision
```

Behavior:

1. User/operator links a JIRA issue through `ExternalWorkItemLink`.
2. Web Portal or chat displays the issue key/link as context.
3. Human/operator chooses the role agent to run next.
4. Role output cites the JIRA issue and artifact evidence.
5. Human/operator updates JIRA manually outside the agent runtime if needed.

---

## 5. Future profile: `jira-first-orchestrated`

This profile is intentionally future/orchestrator-dependent.

```yaml
delivery_profile:
  id: jira-first-orchestrated
  status: planned
  requirement_source: external_work_item
  formal_ba_artifacts_required: conditional
  ba_involvement: trigger_based
  orchestrator_required: true
  external_work_item_required: true
  external_work_item_sync_mode: orchestrator_managed
  jira_write_allowed: false
  approval_gate:
    type: user_approved_card
```

Activation prerequisites:

- orchestrator role graph exists;
- handoff/evidence registry exists;
- gate engine records attributable human decisions;
- JIRA/external work connector is at least read-only and approved;
- Portal can show blocked/unavailable state when prerequisites are missing;
- runtime write operations remain disabled unless a later, separately approved workstream explicitly designs them.

---

## 6. Guardrails

- A linked JIRA card is not automatically an approved requirement.
- `approved` state must cite human/provider evidence.
- Dev work must not start only because a JIRA card exists.
- BA may be trigger-based in lightweight profiles, but BA remains canonical for formal requirement work.
- JIRA write operations are out of scope for the current baseline.
- Runtime apply/deploy/config changes require separate approval.
