# LLM Gateway Foundation

This directory defines the desired-state contract for EKSAD model routing and LLM gateway integration.

The gateway is an **external runtime service**. Git stores policies, aliases, examples, validators, and render-only snippets. It does not store live LiteLLM config, API keys, billing data, prompt logs, or provider secrets.

## Canonical flow

```text
Hermes role profile / future agentic runtime
  → capability alias, e.g. eksad.reasoning
  → OpenAI-compatible LLM Gateway endpoint
  → LiteLLM reference implementation
  → provider/model selected by runtime policy
  → response + metadata back to role agent
```

## Contents

| Path | Purpose |
|---|---|
| `ARCHITECTURE.md` | Gateway boundaries and runtime topology. |
| `MODEL_ALIAS_POLICY.md` | Stable alias design and role binding rules. |
| `MODEL_ALIAS_SCHEMA.md` | JSON contract for alias manifests. |
| `aliases/eksad-model-aliases.json` | Required EKSAD capability aliases. |
| `PROVIDER_MATRIX.md` | Provider family comparison and data-boundary notes. |
| `ROUTING_POLICY.md` | Routing, fallback, and escalation rules. |
| `PER_TASK_ROUTING.md` | Task-type to alias mapping. |
| `BUDGET_AND_RATE_LIMIT_POLICY.md` | Environment/role-based budget governance. |
| `GUARDRAILS_POLICY.md` | Safety, approval, and data handling rules. |
| `OBSERVABILITY.md` | Metrics/logging/tracing contract. |
| `FAILURE_AND_FALLBACK_POLICY.md` | Timeout, outage, fallback, and abstention behavior. |
| `SECURITY_MODEL.md` | Secret and runtime state boundaries. |
| `litellm/` | LiteLLM reference examples only. |
| `adapters/` | Hermes, generic OpenAI-compatible, and chatbot-project guidance. |
| `scripts/` | Read-only validators/renderers. |

## Required aliases

- `eksad.fast`
- `eksad.default`
- `eksad.reasoning`
- `eksad.long_context`
- `eksad.embedding`
- `eksad.reranker`
- `eksad.visual_input`
- `eksad.vision` (compatibility alias; prefer `eksad.visual_input` for new role defaults)
- `eksad.guardrail`

Role agents must request aliases, not hardcoded provider/model names. Runtime operators bind aliases to actual providers per environment.

## Validation

```bash
python3 llm-gateway/scripts/validate-llm-gateway-config.py
python3 llm-gateway/scripts/render-litellm-config.py
```

The renderer prints an example config to stdout only. It must not write runtime config and must not read or print secret values.
