# RAG Indexing Policy

## Default stance

Indexing is **off by default**. A runtime may index only after explicit approval and only from active corpus manifests.

## What may be indexed by default

- EKSAD canonical base standards under `EKSAD/gpt/_base/`.
- EKSAD templates under `EKSAD/gpt/_template/`.
- Portable role/workflow/deliverable/policy docs.
- Runtime adapter docs only as adapter guidance, not source-of-truth override.

## What is excluded by default

- `TIA/`, `USED-CAR/`, and any customer-specific deliverable corpus unless activated.
- Runtime state, generated bundles, caches, logs, DB dumps, binary files.
- Secrets or credentials, even if accidentally present in a source tree.
- Historical/archive content unless a role explicitly needs provenance comparison.

## Reindex triggers

Rebuild or refresh an index when any of these change:

- `EKSAD/gpt/_base/**`
- `EKSAD/gpt/_template/**`
- `portable/**`
- `rag/corpora/*.manifest.json`
- chunking or citation policy files
- approved project-specific corpus manifests

## Runtime index naming

Suggested runtime naming convention:

```text
eksad-<environment>-<corpus-id>-<git-short-sha>
```

The git SHA makes indexes traceable and disposable.

## No auto-watch by default

Do not run file watchers or automatic re-indexers by default on small VPS environments. Prefer explicit rebuild commands or scheduled jobs after resource assessment.
