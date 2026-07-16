# Portable Alias Policy

Role agents must use capability aliases instead of provider-specific model names.

Required aliases:

- `eksad.fast`
- `eksad.default`
- `eksad.reasoning`
- `eksad.long_context`
- `eksad.embedding`
- `eksad.reranker`
- `eksad.visual_input`
- `eksad.vision` (compatibility alias; prefer `eksad.visual_input` for new role defaults)
- `eksad.guardrail`

Provider/model binding is runtime state and must remain outside portable role instructions.

## Role-default routing fields

Role defaults should use these capability-oriented fields:

- `primary` — normal work mode for the role.
- `fallback` — lower-cost/safe fallback when primary is unavailable.
- `escalate` — deeper reasoning for high-impact or ambiguous work.
- `large_artifact` — long-context synthesis over many specs/evidence files.
- `visual_input` — screenshots, diagrams, charts, wireframes, or scanned artifacts.
- `guardrail` — safety, sensitivity, policy, or approval-gate classification.

Do not make a special capability alias such as `eksad.vision` or `eksad.visual_input` the primary identity of a role. UI/UX design is a workflow/role; visual input is only one modality.
