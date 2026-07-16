# Routing Policy

## Decision order

1. Determine task class from role workflow.
2. Select capability alias using `PER_TASK_ROUTING.md`.
3. Apply role permission from `aliases/eksad-model-aliases.json`.
4. Apply environment policy and budget cap.
5. Route through LLM Gateway.
6. If unavailable, use fallback aliases in order.
7. If all fallbacks fail or policy blocks the task, abstain and ask for human/runtime operator input.

## Role escalation

- `general-coordinator` starts with `eksad.fast`, escalates to `eksad.default` or `eksad.reasoning` when routing is ambiguous.
- BA/SA/TL use `eksad.reasoning` for readiness/design/review gates.
- Developer roles use `eksad.default` for implementation support and `eksad.reasoning` for architecture/debugging review.
- QA uses `eksad.default` for test authoring and `eksad.long_context` for large evidence/RTM review.
- DevOps uses `eksad.guardrail` for risky action classification and must keep production writes approval-gated.

## Non-routing rule

Routing cannot override approval gates. A powerful model cannot approve its own deployment, merge, production change, data export, or security exception.
