# RAG Auth and RBAC

RAG access must be role-scoped, project-scoped, and auditable.

## Identity chain

```text
Keycloak/user identity or platform identity
  -> frontdoor/session mapping
  -> Hermes role profile
  -> MCP rag-api-readonly request
  -> RAG API role/corpus filter
```

## Required controls

1. Caller role must be explicit.
2. Corpus allowlist must be enforced server-side.
3. Project-specific corpora must be inactive by default.
4. RAG API tokens must not grant write/index/delete permissions by default.
5. MinIO object access should be mediated by artifact metadata or short-lived signed URLs, not bucket-wide credentials in Hermes.
6. Audit logs should include user/session/role/corpus/query hash/result citation IDs.

## Corpus access defaults

| Corpus type | Default access |
|---|---|
| EKSAD core standards | role allowlist |
| Templates | BA/SA/TL/QA/Dev as relevant |
| Role instructions | same role + TL/general coordinator |
| Portable governance | all roles read-only |
| Project-specific customer data | disabled until activated |

## Forbidden defaults

- Agent-side DB writes.
- Agent-side index rebuild.
- Agent-side corpus activation.
- Broad secrets access.
- Retrieval from customer/project corpus without explicit activation.
