# Corpus Manifest Schema

Corpus manifests live under `rag/corpora/*.manifest.json`.

JSON is used instead of YAML so validators run with Python stdlib only. A future renderer may emit YAML for humans or specific runtimes.

## Required fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable corpus identifier. |
| `version` | string | Manifest version, not document version. |
| `description` | string | Human-readable corpus purpose. |
| `status` | `active` or `example` | Active corpora can be indexed; example corpora are templates only. |
| `source_layer` | string | `canonical-pack`, `portable`, `adapter`, `project-specific`, etc. |
| `indexable` | boolean | Whether this corpus may be indexed. |
| `sensitivity` | string | `public`, `internal`, `confidential`, or `project-confidential`. |
| `paths` | array[string] | Git-relative paths or glob patterns. |
| `exclude` | array[string] | Git-relative exclusion glob patterns. |
| `default_chunk_profile` | string | One of `CHUNKING_PROFILES.md`. |
| `allowed_roles` | array[string] | Portable role ids allowed to retrieve this corpus. |
| `citation_required` | boolean | Must be true for active corpora. |
| `freshness` | object | Reindex expectations. |
| `activation` | object | Optional project/runtime activation gate. |

## Required active-corpus rules

- `citation_required` must be `true`.
- `allowed_roles` must be non-empty and must match `portable/roles/*.md` ids.
- At least one `paths` glob must resolve to tracked files.
- `exclude` must cover project-specific/off-hold areas unless the manifest itself is project-specific.
- No manifest may contain live credentials, connection strings, or provider keys.

## Runtime-local fields

Do not add runtime-local fields to Git manifests:

- concrete vector store URL
- API key value
- LiteLLM master key
- embedding cache path outside example placeholders
- live customer connection strings

Use env var names and adapter examples instead.
