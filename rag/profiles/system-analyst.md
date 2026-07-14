# RAG Profile — system-analyst

## Retrieval purpose

Retrieve architecture principles, TSD templates, API/data/event standards, and role handoff rules.

## Default allowed corpora

- `eksad-core`
- `eksad-templates`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not accept security/production risk alone.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/system-analyst.md`.
