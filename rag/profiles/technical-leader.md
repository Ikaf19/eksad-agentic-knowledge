# RAG Profile — technical-leader

## Retrieval purpose

Retrieve coding standards, architecture principles, review checklists, and evidence policies.

## Default allowed corpora

- `eksad-core`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not bypass PM/AppSec approval gates.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/technical-leader.md`.
