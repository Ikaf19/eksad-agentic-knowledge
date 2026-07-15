# RAG Profile — general-coordinator

## Retrieval purpose

Route retrieval requests to the correct specialist and cite governance/source paths.

## Default allowed corpora

- `eksad-core`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not override specialist role ownership.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/general-coordinator.md`.
