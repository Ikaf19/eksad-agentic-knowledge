# RAG API Contract

This contract defines the service boundary between EKSAD agent runtimes and the RAG system.

The RAG API is the only runtime component that should know how to talk to Milvus, Ollama embeddings, MinIO artifact storage, and any future retrieval pipeline. Hermes role agents should consume the RAG system through an MCP tool or a read-only REST adapter, not through direct vector-store credentials.

## Position in architecture

```text
Hermes role profile
  -> RAG retrieval skill / policy
  -> MCP tool or REST tool
  -> RAG API
  -> Milvus + Ollama embeddings + MinIO artifact metadata
  -> citation-backed retrieval result
```

## Non-goals

The API contract does not install or run the RAG service. It also does not define live credentials, production hostnames, vector indexes, or embedding caches.

## Minimum endpoints

| Method | Path | Purpose | Default access |
|---|---|---|---|
| `GET` | `/health` | Runtime health check | read-only |
| `GET` | `/v1/corpora` | List active corpora visible to the caller role | read-only |
| `POST` | `/v1/search` | Search snippets across allowed corpora | read-only |
| `POST` | `/v1/retrieve` | Retrieve larger cited context for selected result IDs | read-only |
| `GET` | `/v1/documents/{document_id}` | Fetch document metadata and safe text excerpt | read-only |
| `GET` | `/v1/artifacts/{artifact_id}/metadata` | Fetch artifact/evidence metadata, not raw bucket credentials | read-only |
| `POST` | `/v1/citations/resolve` | Resolve citation IDs to source path/section/line metadata | read-only |

Approval-gated endpoints for future admin flows:

| Method | Path | Purpose | Default access |
|---|---|---|---|
| `POST` | `/v1/index/jobs` | Submit corpus indexing job | disabled |
| `GET` | `/v1/index/jobs/{job_id}` | Inspect indexing job status | admin/read-only |
| `POST` | `/v1/feedback` | Submit retrieval feedback | disabled until policy approved |

## Request context

Every request from an agent runtime must include identity and scope fields, either in headers or body:

| Field | Required | Description |
|---|---:|---|
| `role` | yes | EKSAD role ID such as `business-analyst`, `system-analyst`, `developer-backend` |
| `user_id` | recommended | Platform user or mapped Keycloak subject. May be hashed in logs. |
| `tenant_id` | recommended | Tenant/project boundary when project-specific corpora are activated. |
| `session_id` | recommended | Agent session ID for audit tracing. |
| `corpus_ids` | optional | Requested corpus IDs; service must filter by role/corpus policy. |
| `citation_required` | yes | Must be true for knowledge-backed answers. |

## Search request example

```json
{
  "query": "Apa prinsip tenant isolation untuk EKSAD module?",
  "role": "system-analyst",
  "corpus_ids": ["eksad-core"],
  "top_k": 5,
  "citation_required": true,
  "filters": {
    "sensitivity_max": "internal",
    "project_scope": "global"
  }
}
```

## Search response example

```json
{
  "query": "Apa prinsip tenant isolation untuk EKSAD module?",
  "role": "system-analyst",
  "corpus_ids": ["eksad-core"],
  "results": [
    {
      "result_id": "res_001",
      "document_id": "doc_eksad_base_principles",
      "source_path": "EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md",
      "title": "EKSAD Base Principles",
      "snippet": "Tenant isolation must be explicit in every bounded context...",
      "score": 0.82,
      "citation": {
        "citation_id": "cit_001",
        "path": "EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md",
        "section": "Tenant isolation",
        "line_start": 10,
        "line_end": 24
      },
      "sensitivity": "internal",
      "corpus_id": "eksad-core"
    }
  ],
  "abstain": false,
  "warnings": []
}
```

## Required response invariants

A valid retrieval response must include:

1. `source_path` for every result.
2. `citation` with at least path and section or line range.
3. `corpus_id` for every result.
4. `sensitivity` for every result.
5. `score` or ranking metadata for every result.
6. `abstain=true` when no result meets the retrieval confidence threshold.

## Error contract

Use structured errors:

```json
{
  "error": {
    "code": "CORPUS_FORBIDDEN",
    "message": "Role qa-engineer cannot access corpus project-x-private.",
    "retryable": false,
    "audit_id": "rag_audit_20260714_0001"
  }
}
```

Recommended error codes:

- `INVALID_ROLE`
- `CORPUS_FORBIDDEN`
- `PROJECT_SCOPE_REQUIRED`
- `CITATION_UNAVAILABLE`
- `LOW_CONFIDENCE_ABSTENTION`
- `RAG_BACKEND_UNAVAILABLE`
- `ARTIFACT_METADATA_FORBIDDEN`
- `INDEXING_DISABLED`

## Runtime ownership

The RAG API owns:

- role/corpus filtering
- query embedding
- vector retrieval
- optional hybrid retrieval/reranking
- citation resolution
- artifact metadata lookup
- audit logging
- index status and freshness metadata

Hermes owns:

- role intent
- whether retrieval is required for the task
- calling the RAG tool
- interpreting cited results
- abstaining or asking for clarification when evidence is insufficient
