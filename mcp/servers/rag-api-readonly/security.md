# Security — RAG API Readonly MCP

## Allowed by default

- read-only search
- read-only retrieval
- citation resolution
- document metadata/excerpt lookup
- artifact metadata lookup
- health checks

## Forbidden by default

- index rebuild
- corpus activation
- document deletion
- write annotations
- direct Milvus credentials in Hermes
- direct MinIO bucket credentials in Hermes
- broad project/customer corpus access

## Required controls

- role must be included in every request
- corpus filtering must be server-side
- project corpora disabled unless explicitly activated
- audit logs must capture role, corpus IDs, query hash, citation IDs, and result count
- all runtime tokens must live outside Git
