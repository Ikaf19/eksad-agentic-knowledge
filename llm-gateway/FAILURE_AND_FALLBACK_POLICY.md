# Failure and Fallback Policy

## Failure classes

| Class | Example | Behavior |
|---|---|---|
| Alias unavailable | no runtime binding | try fallback alias, then ask operator |
| Provider timeout | request exceeds SLA | retry once if idempotent, then fallback |
| Rate limit | provider or gateway quota | fallback if policy allows, else wait/ask |
| Budget block | role/env cap exceeded | do not bypass; ask approval/runtime operator |
| Policy block | sensitive data/provider disallowed | abstain and explain allowed path |
| Quality failure | model output unsupported by citations | retry with RAG/citations or escalate |

## Fallback rules

1. Only fallback to aliases listed in `aliases/eksad-model-aliases.json`.
2. Never fallback from an internal-only/local requirement to an external provider unless data policy allows it.
3. Do not fallback from service-only embedding/reranker aliases to role-agent chat aliases.
4. If fallback changes capability materially, tell the user/operator.
5. If all routes fail, return a clear abstention with next safe action.
