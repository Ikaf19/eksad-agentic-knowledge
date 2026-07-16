# Budget and Rate Limit Policy

## Scope

This policy defines desired-state budget behavior. Actual limits are set in runtime LiteLLM/gateway config, not in Git.

## Budget dimensions

| Dimension | Examples |
|---|---|
| Environment | local, dev, staging, prod |
| Role | BA, SA, TL, Dev-BE, Dev-FE, QA, DevOps, coordinator |
| Alias | `eksad.fast`, `eksad.reasoning`, etc. |
| Task class | intake, drafting, review, debugging, RAG embedding |
| Data sensitivity | public, internal, project-confidential, restricted |

## Desired defaults

- `eksad.fast`: broad access, low cost, high rate limit.
- `eksad.default`: normal workhorse, moderate budget.
- `eksad.reasoning`: budgeted and justification-aware.
- `eksad.long_context`: restricted to large-artifact workflows.
- `eksad.vision`: disabled unless the role and data classification allow it.
- `eksad.embedding` / `eksad.reranker`: service-only and metered through RAG service.

## Runtime enforcement examples

- Per-role monthly budget.
- Per-alias request/token cap.
- Per-environment high-cost alias allowlist.
- Alert thresholds before hard cutoff.
- Separate budget for RAG service aliases.

Never store billing exports or live usage data in this repo.
