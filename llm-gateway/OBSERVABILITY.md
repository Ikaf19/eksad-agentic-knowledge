# Observability Contract

## Required telemetry

| Signal | Required fields |
|---|---|
| Request metadata | timestamp, request id, role, alias, environment, task class |
| Routing | selected provider/model class, fallback chain, retry count |
| Cost | prompt tokens, completion tokens, estimated cost bucket |
| Latency | queue time, provider time, total time |
| Safety | guardrail decision, redaction applied, blocked reason |
| Errors | timeout, provider error class, budget block, policy block |

## Logging constraints

- Do not log raw secrets.
- Do not log full prompts/responses by default.
- Do not commit gateway logs to Git.
- Redact user identifiers if platform privacy policy requires it.
- Link request ids to Hermes/session logs only in runtime observability systems, not this repo.

## Target stack alignment

The EKSAD AI Software Factory architecture can forward gateway metrics/logs to Prometheus/Grafana/Loki. This repo only defines the desired fields and examples.
