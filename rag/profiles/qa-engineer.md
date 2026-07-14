# RAG Profile — qa-engineer

## Retrieval purpose

Retrieve acceptance criteria, test plan/RTM templates, QA workflow, and evidence policies.

## Default allowed corpora

- `eksad-core`
- `eksad-templates`
- `eksad-role-instructions`
- `eksad-portable-governance`

Project-specific corpora require explicit activation and must cite the active project manifest.

## Boundary

Does not treat retrieval as test execution evidence.

## Required answer behavior

- Cite repository paths for retrieved claims.
- Surface conflicts instead of silently choosing.
- Say evidence is insufficient when no citation is found.
- Respect role ownership from `portable/roles/qa-engineer.md`.
