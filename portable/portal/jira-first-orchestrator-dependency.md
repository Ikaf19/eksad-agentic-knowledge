# JIRA-First Delivery: Orchestrator Dependency

**Status:** Future/orchestrator-dependent  
**Last updated:** 2026-07-16  
**Current baseline:** Link-only or manual agent-assisted JIRA usage  
**Runtime mutation policy:** This document does not approve JIRA runtime write integration.

---

## 1. Decision

JIRA-first delivery is **not** a Phase 1 execution mode while EKSAD uses independent Hermes role agents without a central orchestrator.

Current safe mode:

```text
JIRA issue link
  -> Web Portal/chat context
  -> human/operator selects Hermes role agent
  -> role agent produces artifact/handoff
  -> human/operator updates JIRA manually if needed
```

Future orchestrated mode:

```text
Approved JIRA card
  -> Portal/orchestrator validates gate
  -> orchestrator dispatches role graph
  -> role agents produce artifacts/evidence
  -> Portal/JIRA show linked evidence
```

---

## 2. Why an orchestrator is required

JIRA-first delivery needs a component that can safely own workflow state:

| Required capability | Why independent role agents are insufficient |
|---|---|
| Delivery profile resolution | Role agents should not decide global project workflow on their own. |
| JIRA approval gate validation | A card link alone is not proof of user approval. |
| Role graph sequencing | UI/UX, SA, TL, Dev, QA, and DevOps have dependent handoffs. |
| HITL gate engine | User/TL/QA/DevOps decisions must pause/unlock stages explicitly. |
| Handoff/evidence registry | Downstream roles need verified inputs and artifact references. |
| Audit state | The system must know who approved what and when. |
| Failure/rollback handling | A failed role run must not silently transition external workflow state. |

---

## 3. Current allowed behavior

| Behavior | Allowed now? | Notes |
|---|---:|---|
| Store/link JIRA issue key and URL | Yes | Through `ExternalWorkItemLink`; no credentials. |
| Use JIRA link as manual role-agent context | Yes | Human/operator provides or verifies evidence. |
| Manually record non-authoritative status snapshot | Yes | Must not be treated as provider truth. |
| Read JIRA via approved read-only connector | Future pilot | Requires MCP/API read-only contract and runtime approval. |
| Create JIRA card from Portal | No | Future work only. |
| Update JIRA status from Portal/agent | No | Future work only. |
| Agent writes comments to JIRA | No | Future work only. |
| Approved JIRA card auto-starts role workflow | No | Requires orchestrator. |

---

## 4. Future activation prerequisites

Before `jira-first-orchestrated` can become active, Git source-of-truth must define:

1. orchestrator source-of-truth and runtime contract;
2. role workflow graph for JIRA-first delivery;
3. gate state machine and approval evidence schema;
4. handoff/evidence registry model;
5. JIRA read-only integration contract;
6. Portal unavailable/disabled-state behavior when prerequisites are missing;
7. security model for any future write integration;
8. validation script that fails if JIRA write behavior is implied without approval.

---

## 5. No-write principle

The current baseline explicitly avoids JIRA runtime write integration:

```text
No create card
No update status
No assign user
No comment writeback
No transition workflow
No attachment upload
No sprint mutation
```

If a future phase proposes any write behavior, it must be a separate design with:

- named owner and approver;
- least-privilege service account model;
- secret storage boundary;
- audit event schema;
- failure/rollback behavior;
- rate limit and idempotency rules;
- non-prod pilot before production.
