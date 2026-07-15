# RAG Profile — devops-engineer

## Retrieval purpose

Retrieve deployment/governance/security boundaries and runtime setup docs.

## Default allowed corpora

- `eksad-core`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not expose secrets or enable production writes by default.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/devops-engineer.md`.
