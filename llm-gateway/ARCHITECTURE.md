# LLM Gateway Architecture

## Position in EKSAD AI Software Factory

The LLM Gateway sits between role agents and model providers.

```text
Front door / Hermes / future harness
  → role profile + skill + task policy
  → model capability alias
  → LLM Gateway API
  → LiteLLM router or equivalent OpenAI-compatible gateway
  → provider/model
```

Hermes remains the role-agent runtime. Optional user-invoked session-local coordination may run inside Hermes, but the future durable Portal/central Orchestrator is a separate planned layer. LiteLLM or an equivalent gateway owns provider routing, key isolation, budget caps, rate limits, failover, and provider-specific quirks.

## Design principles

1. **Aliases are stable.** Role agents ask for `eksad.reasoning`, not a provider-specific model string.
2. **Provider binding is runtime state.** Actual model names and provider keys are configured outside Git.
3. **OpenAI-compatible first.** Hermes and future harnesses should be able to use the gateway through `/v1/chat/completions`, `/v1/embeddings`, and related compatible endpoints.
4. **LiteLLM is reference, not lock-in.** The desired-state contract should also work with another OpenAI-compatible router.
5. **RAG uses service aliases.** `eksad.embedding` and `eksad.reranker` are owned by the RAG service, not called directly by role agents by default.
6. **Human approvals remain outside model routing.** The gateway can classify or enforce budgets, but stage gates remain role/process governance.

## Runtime state not in Git

- Provider API keys.
- LiteLLM master keys or proxy auth keys.
- Live `config.yaml` with real model bindings.
- Raw prompt/response logs containing confidential data.
- Billing exports or usage records with user identifiers.
- Provider-specific allowlists containing secrets.

## Relationship to RAG

RAG retrieval and citations happen before or during model calls depending on the agent workflow:

```text
Role agent → RAG API/MCP → cited context → LLM alias → answer with citations
```

The gateway may provide embedding/reranking aliases to the RAG service, but role agents should not bypass the RAG API to generate embeddings or query vector stores directly.
