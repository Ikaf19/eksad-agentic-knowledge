# Milvus Adapter Notes

Milvus is the target vector store in the architecture baseline. This directory documents expectations only; it does not include Milvus indexes or runtime config.

## Boundary

- RAG API talks to Milvus.
- Hermes does not receive Milvus credentials.
- Git stores collection naming policy and metadata expectations, not vectors.

## Suggested collection metadata

- `corpus_id`
- `document_id`
- `source_path`
- `chunk_id`
- `chunk_profile`
- `sensitivity`
- `allowed_roles`
- `source_commit`
- `citation_id`

## Default policy

Collections are read-only to agent query paths. Index creation and rebuild are DevOps/admin tasks, not role-agent default tools.
