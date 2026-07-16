# Model Alias Policy

## Policy

All EKSAD role agents must route model usage through **capability aliases**.

Good:

```text
Use eksad.reasoning for TSD architecture review.
```

Avoid:

```text
Use provider X model Y directly from the role prompt.
```

## Why aliases

- Keep role instructions portable across providers.
- Let runtime operators change providers without rewriting skills.
- Enable budget, fallback, and observability at the gateway boundary.
- Support generic OpenAI-compatible gateways, not only LiteLLM.

## Required alias set

| Alias | Purpose | Default owner |
|---|---|---|
| `eksad.fast` | low-latency routing/classification/light summarization | role agents |
| `eksad.default` | balanced general work | role agents |
| `eksad.reasoning` | high-reasoning analysis/review/design | role agents with approval-aware usage |
| `eksad.long_context` | long document synthesis | selected roles |
| `eksad.embedding` | embedding generation | RAG service only by default |
| `eksad.reranker` | retrieval reranking | RAG service only by default |
| `eksad.vision` | screenshot/diagram/scanned artifact interpretation | selected roles |
| `eksad.guardrail` | policy/risk classification | coordinator/TL/DevOps gate |

## Role default principle

Role prompts and skills may name preferred aliases, but runtime configs decide actual model bindings. If an alias is unavailable, the agent must follow `FAILURE_AND_FALLBACK_POLICY.md` rather than inventing a provider.
