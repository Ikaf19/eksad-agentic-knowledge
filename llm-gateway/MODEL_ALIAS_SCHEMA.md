# Model Alias Manifest Schema

Machine-readable alias manifests live at `llm-gateway/aliases/*.json`.

## Required top-level fields

| Field | Type | Description |
|---|---|---|
| `version` | string | Manifest version. |
| `required_aliases` | array[string] | Required EKSAD capability aliases. |
| `aliases` | array[object] | Alias definitions. |
| `role_defaults` | object | Role-to-alias defaults. |
| `environment_policy` | object | Environment-level budget/routing constraints. |

## Alias object fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `alias` | string | yes | Stable alias name, e.g. `eksad.reasoning`. |
| `capability` | string | yes | Human-readable capability description. |
| `default_enabled` | boolean | yes | Whether the alias is available by default in desired state. |
| `cost_tier` | string | yes | `low`, `medium`, or `high`. |
| `context_class` | string | yes | `standard`, `long`, `embedding`, `reranker`, `multimodal`, or `classifier`. |
| `litellm_model_env` | string | yes | Environment variable name for runtime model binding. |
| `api_key_env` | string | yes | Environment variable name for runtime provider key. |
| `api_base_env` | string | optional | Environment variable name for runtime provider base URL. |
| `fallback_aliases` | array[string] | yes | Ordered alias fallback list. |
| `allowed_roles` | array[string] | yes | Roles/services allowed to request the alias. |
| `typical_tasks` | array[string] | yes | Examples of intended usage. |
| `security_notes` | array[string] | yes | Guardrails and constraints. |

## Validation expectations

- Required aliases must exist exactly once.
- Fallbacks and role defaults must reference known aliases.
- Service-only aliases such as embedding/reranker must not be default role-agent chat aliases.
- No real secrets may appear in alias manifests.
