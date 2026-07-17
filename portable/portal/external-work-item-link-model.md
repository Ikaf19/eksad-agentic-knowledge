# ExternalWorkItemLink Model

**Status:** Portable contract / Git-only desired state  
**Last updated:** 2026-07-16  
**Primary consumer:** Future Web Portal, future orchestrator, and role-agent handoff tooling  
**Runtime mutation policy:** This model is link/reference only. It must not store live work-management credentials, raw comments, full issue payloads, sprint data, or provider tokens in Git.

---

## 1. Intent

`ExternalWorkItemLink` is the canonical way to associate an EKSAD project, agent run, artifact, PR, test evidence, or release evidence with a work item managed outside Git.

Typical examples:

- JIRA issue such as `EKSAD-123`;
- GitLab issue;
- Linear issue;
- manual work item recorded by a customer system.

The model keeps EKSAD source-of-truth generic and avoids making JIRA a hard dependency of Phase 1.

---

## 2. Boundary

| System | Owns |
|---|---|
| Git source-of-truth | Link model, allowed providers, field requirements, approval policy, validation rules. |
| Web Portal runtime | Project-local link records, normalized status snapshot, audit pointer, sync timestamps. |
| JIRA / external system | Actual card, comments, assignee, sprint, workflow status, attachments, and approval records. |
| Orchestrator runtime | Future role workflow state and evidence registry derived from approved work items. |

Git must not duplicate the live external work item.

---

## 3. Canonical fields

```yaml
external_work_item_link:
  id: <portal-generated-link-id>
  tenant_id: <tenant-id>
  project_id: <project-id>
  provider: jira | gitlab | linear | manual | other
  external_key: <provider-native-key>        # Example: EKSAD-123
  external_url: <provider-url-or-redacted>   # URL only; no embedded credentials
  external_type: epic | story | task | bug | change | other
  normalized_status: draft | needs_clarification | ready_for_review | approved | ready_for_delivery | in_progress | blocked | done | cancelled | unknown
  approval_state: not_required | not_requested | awaiting_user | approved | rejected | waived | unknown
  linked_entity_type: project | agent_run | artifact | pull_request | test_evidence | release_evidence
  linked_entity_id: <internal-id-or-artifact-ref>
  last_synced_at: <timestamp-or-null>
  sync_mode: none | manual_snapshot | read_only | orchestrator_managed
  source_of_truth: external_system
```

### Field rules

| Field | Rule |
|---|---|
| `provider` | Must be an allowlisted provider value; JIRA is one provider, not the only model. |
| `external_key` | Provider-native identifier; never include secret material. |
| `external_url` | Must not embed username, password, token, or query secrets. |
| `normalized_status` | Portal/orchestrator mapping only; it does not overwrite provider status. |
| `approval_state` | Captures normalized gate state, not a replacement for provider audit evidence. |
| `sync_mode` | Must remain `none`, `manual_snapshot`, or `read_only` until an orchestrator layer is approved. |
| `source_of_truth` | Defaults to `external_system`; Git and Portal should reference rather than duplicate. |

---

## 4. Current allowed sync modes

| Mode | Current status | Meaning |
|---|---|---|
| `none` | Allowed | Static link only. |
| `manual_snapshot` | Allowed | Human/operator records a non-authoritative status snapshot. |
| `read_only` | Future pilot | Portal/Hermes reads external metadata through an approved read-only connector. |
| `orchestrator_managed` | Future only | Requires orchestrator layer and explicit runtime approval. |

`orchestrator_managed` must not be used in Phase 1.

---

## 5. Link-only flow for Phase 1

```text
User or operator provides JIRA issue key/link
  -> Web Portal stores ExternalWorkItemLink metadata
  -> Hermes role agent may receive the link as context
  -> human/operator manually opens JIRA or provides exported evidence
  -> generated artifacts cite the issue key/link
```

There is no automatic JIRA mutation in this flow.

---

## 6. Validation checklist

- [ ] Link has provider, key, URL/reference, and project scope.
- [ ] URL contains no embedded credentials or sensitive query parameters.
- [ ] Status snapshot is clearly non-authoritative unless read-only sync is approved.
- [ ] Approval state is backed by a provider/user evidence reference.
- [ ] Role-agent output links back to the external work item when used as input.
- [ ] No external work item payload, comments, attachments, or runtime token is committed to Git.
