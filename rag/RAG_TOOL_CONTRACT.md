# RAG Tool Contract

This document defines the callable tools that agent runtimes should use to reach the RAG API.

Preferred runtime shape:

```text
Hermes native MCP client -> rag-api-readonly MCP server -> RAG API
```

Direct REST tools are allowed for MVP fallback, but MCP remains the preferred standard access layer.

## Tool set

| Tool | Purpose | Default |
|---|---|---|
| `rag_search` | Search snippets across allowed corpora | enabled |
| `rag_retrieve` | Retrieve expanded context for selected result IDs | enabled |
| `rag_get_document` | Fetch safe document metadata/excerpt by ID | enabled |
| `rag_resolve_citation` | Resolve citation IDs to source metadata | enabled |
| `rag_get_artifact_metadata` | Fetch evidence/artifact metadata without bucket credentials | enabled |
| `rag_healthcheck` | Check RAG API/MCP availability | enabled |

Forbidden by default:

| Tool | Reason |
|---|---|
| `rag_index_corpus` | Mutates runtime index and may expose project data |
| `rag_rebuild_index` | Expensive and operationally risky |
| `rag_delete_document` | Destructive |
| `rag_write_annotation` | Writes runtime state; needs governance |

## Required input fields

Every retrieval tool must accept or infer:

- `role`
- `query` or a stable ID such as `document_id` / `citation_id`
- `corpus_ids` optional, always filtered server-side
- `tenant_id` / `project_id` optional for activated project corpora
- `citation_required`, default true

## Required output fields

Every result must include:

- `source_path`
- `citation`
- `sensitivity`
- `corpus_id`
- `retrieval_score` or `score`
- `abstain` indicator at envelope level

## Role behavior

The tool does not replace role judgment. Role skills decide when to call retrieval and how to use it.

| Role | Typical use |
|---|---|
| `business-analyst` | BRD/FSD evidence, business rules, glossary references |
| `system-analyst` | architecture principles, API/ERD standards, integration constraints |
| `developer-backend` | backend patterns, API contracts, coding standards |
| `developer-frontend` | frontend patterns, UX standards, API contract lookup |
| `qa-engineer` | RTM, acceptance criteria, test-plan evidence |
| `devops-engineer` | CI/CD, deployment, observability, runbook references |
| `technical-leader` | cross-role review and policy evidence |
| `general-coordinator` | task intake and routing evidence only |
| `project-manager` | timeline, deliverable, and status evidence |

## Abstention rule

If the tool returns `abstain=true`, the role agent must not invent missing facts. It should either ask for missing evidence, use only non-retrieval reasoning with explicit assumptions, or route to a human approval gate.
