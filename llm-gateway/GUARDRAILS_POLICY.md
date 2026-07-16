# Guardrails Policy

## Gateway guardrail responsibilities

The gateway may enforce or assist with:

- Provider allowlists.
- Alias allowlists per environment.
- Token/rate/budget ceilings.
- Sensitive-data routing blocks.
- Prompt/response redaction before logs.
- Tool-risk classification support through `eksad.guardrail`.

## Agent/runtime responsibilities

Hermes and future agentic runtimes remain responsible for:

- Human approval gates.
- Tool permissioning.
- MCP capability scope.
- Role-specific workflow compliance.
- Not sending prohibited data to external providers.

## Restricted cases

Do not route without explicit approval when a request involves:

- Production deploy/rollback/credential changes.
- Customer-confidential documents outside an activated project corpus.
- Secrets, private keys, tokens, or raw connection strings.
- Database writes or destructive infrastructure action.
- Legal/regulatory commitments.

## Raw logs

Raw prompt/response logging is disabled by default. Prefer structured metadata logs: alias, role, environment, latency, token counts, status, fallback event, and redaction status.
