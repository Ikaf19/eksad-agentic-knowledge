# Portable Portal Layer

**Status:** Portable source-of-truth extension  
**Last updated:** 2026-07-16  
**Runtime mutation policy:** This directory defines portal-facing contracts only. It must not contain live Portal, JIRA, Keycloak, Hermes, LiteLLM, RAG, MCP, database, or credential configuration.

---

## Purpose

`portable/portal/` holds runtime-neutral contracts that a Web Portal, chat frontend, or future orchestrator can consume without depending on a specific UI/backend implementation.

The current scope is intentionally small:

| Contract | Purpose |
|---|---|
| `external-work-item-link-model.md` | Defines how a project or agent run can reference an external work item such as a JIRA issue without duplicating the work system. |
| `delivery-profile-model.md` | Defines the `DeliveryProfile` concept and profiles such as formal spec-driven, manual agent-assisted, and future orchestrated JIRA-first modes. |
| `jira-first-orchestrator-dependency.md` | Marks JIRA-first delivery as future/orchestrator-dependent and explicitly forbids JIRA write integration in the current baseline. |

---

## Layering rule

```text
Git source-of-truth
  -> portable portal contracts
  -> future Web Portal implementation
  -> future orchestrator runtime
  -> external work-management systems such as JIRA
```

Git defines the policy, schema, required gates, and safe boundaries. Runtime systems hold live cards, statuses, credentials, comments, assignees, sprints, and sync state.

---

## Current baseline

The current EKSAD source-of-truth supports **link-only external work item references**:

```text
Project / AgentRun / Artifact
  -> ExternalWorkItemLink
  -> JIRA issue URL/key or another work-management item
```

This does **not** mean:

- automatic role-agent orchestration from JIRA;
- automatic JIRA card creation;
- automatic JIRA status transition;
- agent-written comments to JIRA;
- storage of JIRA API tokens;
- runtime Web Portal deployment.

Those require a future orchestrator layer, work-management integration contract, and explicit runtime approval.

---

## Required future consumers

A future Web Portal or orchestrator should consume these contracts to decide:

1. which delivery profile a project uses;
2. whether an external work item is merely linked, read-only validated, or eligible for orchestrated delivery;
3. which human approval gates must be satisfied before role-agent work starts;
4. whether JIRA-first behavior is disabled because the orchestrator is not available.
