# Portable Alias Policy

Role agents must use capability aliases instead of provider-specific model names.

Required aliases:

- `eksad.fast`
- `eksad.default`
- `eksad.reasoning`
- `eksad.long_context`
- `eksad.embedding`
- `eksad.reranker`
- `eksad.vision`
- `eksad.guardrail`

Provider/model binding is runtime state and must remain outside portable role instructions.
