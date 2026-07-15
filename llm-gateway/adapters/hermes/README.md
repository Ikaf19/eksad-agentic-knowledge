# Hermes Adapter — LLM Gateway

Hermes should consume the gateway as an OpenAI-compatible provider using EKSAD aliases as model names.

Example flow:

```text
Hermes profile → model alias eksad.default → LiteLLM/OpenAI-compatible base URL → provider
```

Use `hermes.example.yaml` as a documentation snippet only. Do not copy it to live `~/.hermes/config.yaml` without runtime review and secret injection.

## Role binding

See `role-model-policy.md` for profile-to-alias defaults.
