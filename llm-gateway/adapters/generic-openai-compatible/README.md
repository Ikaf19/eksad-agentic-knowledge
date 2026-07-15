# Generic OpenAI-Compatible Adapter

Any future harness can consume the EKSAD LLM Gateway through OpenAI-compatible endpoints.

Expected minimum:

```text
base_url = <gateway>/v1
api_key  = runtime secret
model    = eksad.default or another approved alias
```

Do not require LiteLLM-specific behavior in portable role docs. LiteLLM is the reference implementation, not the portable contract.
