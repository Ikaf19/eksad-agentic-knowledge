# RAG Observability

RAG calls should be auditable without leaking sensitive query text or secrets.

## Recommended metrics

- request count by role
- request latency by endpoint
- retrieval hit count
- abstention rate
- corpus forbidden count
- citation missing count
- backend error count
- top corpus usage
- index freshness age

## Recommended logs

Each request should capture:

- audit ID
- timestamp
- user/session hash
- role
- corpus IDs requested and granted
- query hash, not raw query by default
- result document IDs and citation IDs
- abstention flag
- error code if failed

## Integration target

The architecture baseline places observability in Prometheus, Grafana, and Loki. Phase C only defines the contract; runtime wiring belongs to a later runtime blueprint/pilot phase.
