# Portable LLM Gateway Policy

## Rules

- Git stores alias policy and examples, not runtime secrets.
- Role agents request aliases, not provider-specific model names.
- Runtime operators bind aliases to providers through approved gateway config.
- High-cost, multimodal, and external-provider routes require environment approval.
- Raw prompt/response logging is disabled by default.
- Gateway routing cannot approve tool actions, production changes, deploys, merges, or security exceptions.

## Runtime apply gate

Before enabling a gateway for role agents:

1. Provider and data-processing approval is complete.
2. Alias bindings are reviewed.
3. Budget/rate limits are configured.
4. Observability/redaction is configured.
5. Hermes/future runtime adapter is tested against a non-production endpoint.
