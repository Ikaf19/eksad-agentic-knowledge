# RAG Security Model

## Defaults

- Indexing disabled until explicitly approved.
- Active corpora only; example corpora are not indexed.
- Role-scoped retrieval enforced by corpus manifest.
- Citations required for active corpora.
- Runtime caches and vector DBs are never committed.

## Forbidden in Git

- Vector DB files, embedding caches, reranker caches.
- API keys, LiteLLM master keys, bearer tokens, PATs.
- Customer dumps, database exports, logs with user prompts/responses.
- Runtime-local config containing live endpoints plus credentials.

## Sensitive source handling

| Sensitivity | Allowed default behavior |
|---|---|
| `public` | May be uploaded to chatbot projects if license permits. |
| `internal` | May be indexed in approved internal runtime. |
| `confidential` | Requires project/environment approval. |
| `project-confidential` | Only within explicitly activated project corpus. |

## Leakage controls

- Do not mix project-specific and base corpora in the same unrestricted index.
- Do not expose raw chunk dumps to users unless asked and authorized.
- Redact secrets from runtime logs.
- Avoid broad “search everything” endpoints in multi-tenant environments.
- Prefer per-corpus and per-role filters at retrieval time.

## Audit expectations

A production RAG runtime should log:

- corpus id
- source path
- git commit/index version
- requesting role/profile
- query hash or redacted query
- returned citation paths

Do not log full prompts/responses by default.
