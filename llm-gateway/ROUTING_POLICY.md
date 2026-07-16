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

- `general-coordinator` starts with `eksad.fast`, uses `eksad.default` for structured planning, and escalates to `eksad.reasoning` when routing or ownership is ambiguous.
- BA uses `eksad.default` for drafting and `eksad.reasoning` for readiness gates or difficult requirement trade-offs.
- SA and TL use `eksad.reasoning` for TSD, architecture, API/data/event contracts, and review gates.
- Developer roles use `eksad.default` for implementation support and `eksad.reasoning` for architecture/debugging review.
- QA uses `eksad.default` for test authoring and `eksad.long_context` for large evidence/RTM review.
- Data Analyst uses `eksad.default` for analysis/reporting and escalates to `eksad.reasoning` for metric ambiguity, causality, or data-quality risk.
- Data Scientist uses `eksad.reasoning` for experiment/model design and `eksad.long_context` for large experiment/evidence packages.
- UI/UX Designer uses `eksad.default` for design workflow and `eksad.visual_input` only when interpreting screenshots, wireframes, diagrams, or design exports.
- Content Creator uses `eksad.default` for source-grounded content and `eksad.guardrail` for publication/sensitivity checks.
- DevOps uses `eksad.guardrail` for risky action classification and must keep production writes approval-gated.

## Visual input rule

`eksad.visual_input` is a task capability, not a role identity. Do not set visual aliases as `primary` for any role. `eksad.vision` remains a compatibility alias for older runtimes and should be migrated to `eksad.visual_input` in new docs/defaults.

## Non-routing rule

Routing cannot override approval gates. A powerful model cannot approve its own deployment, merge, production change, data export, publication, or security exception.
