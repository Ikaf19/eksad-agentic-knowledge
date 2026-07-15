# RAG Indexing Pipeline

This document defines the desired-state indexing pipeline. It is not an installer.

## Pipeline stages

```text
Git checkout / source export
  -> corpus manifest selection
  -> path/exclude expansion
  -> sensitivity and role policy validation
  -> chunking profile
  -> embedding via approved embedding service
  -> vector upsert into Milvus
  -> source/citation metadata write
  -> artifact metadata link into MinIO when applicable
  -> index freshness report
```

## Trigger policy

Indexing is not a default role-agent operation. It should be triggered by an approved runtime job or DevOps workflow.

Allowed trigger examples:

- scheduled non-production indexing job
- post-merge pipeline for approved corpora
- manual approved index rebuild

Disallowed by default:

- role agent ad-hoc index rebuild
- indexing uploaded customer data without activation
- committing generated vectors/embedding caches to Git

## Freshness metadata

Each indexed corpus should expose:

- corpus ID
- source commit SHA or artifact version
- chunking profile
- embedding model alias/version
- indexed_at timestamp
- document count
- chunk count
- warning count
