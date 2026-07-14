# Portable Retrieval Policy

1. Retrieval must be evidence-based and citation-backed.
2. Corpus manifests define what may be indexed and which roles may retrieve it.
3. Project-specific corpora are disabled until explicitly activated.
4. Retrieval does not change role ownership or approval gates.
5. If no cited evidence exists, the agent must abstain or ask for the missing artifact.
6. Runtime adapters may implement retrieval through vector DB, lexical search, MCP, API, or native project search, but the behavior must remain consistent with this policy.
