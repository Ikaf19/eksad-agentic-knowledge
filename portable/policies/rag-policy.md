# RAG Policy

RAG is allowed as an evidence-retrieval capability, not as an authority override.

## Required controls

- Index only active corpus manifests from `rag/corpora/`.
- Enforce role-based corpus access.
- Require citations for generated claims based on retrieval.
- Keep runtime indexes and caches outside Git.
- Do not index TIA/USED-CAR/customer-specific material unless explicitly activated.
- Treat retrieval output as evidence, not approval to write, deploy, merge, or accept risk.
- Prefer RAG API/MCP access from agent runtimes; do not give role agents direct Milvus, MinIO, or embedding-service credentials by default.
- Keep index/rebuild/delete operations disabled for role agents unless a separate admin approval gate enables them.

## Runtime apply gate

Any RAG runtime setup requires separate approval after:

1. Corpus manifest validation passes.
2. Ingestion plan is reviewed.
3. Security/sensitivity review is complete.
4. Runtime resource constraints are checked.
5. RAG API/MCP auth, RBAC, observability, and citation behavior are reviewed.
