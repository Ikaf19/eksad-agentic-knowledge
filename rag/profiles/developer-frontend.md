# RAG Profile — developer-frontend

## Retrieval purpose

Retrieve FE standards, FE-TSD guidance, UI/API contracts, and approved design evidence.

## Default allowed corpora

- `eksad-core`
- `eksad-templates`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not invent backend contracts without SA/API evidence.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/developer-frontend.md`.
