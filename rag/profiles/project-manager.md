# RAG Profile — project-manager

## Retrieval purpose

Retrieve delivery workflow, role boundary, readiness gates, and progress governance.

## Default allowed corpora

- `eksad-core`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not approve technical/security risk without owner evidence.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/project-manager.md`.
