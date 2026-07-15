# RAG Profile — developer-backend

## Retrieval purpose

Retrieve backend implementation standards, API/data/event contracts, and accepted templates.

## Default allowed corpora

- `eksad-core`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not modify DB/production based only on retrieval.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/developer-backend.md`.
