# RAG Profile — business-analyst

## Retrieval purpose

Retrieve business rules, BRD/FSD templates, glossary, and approved project evidence.

## Default allowed corpora

- `eksad-core`
- `eksad-templates`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not decide implementation architecture.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/business-analyst.md`.
