# Ollama Embedding Adapter Notes

Ollama is the local embedding runtime target in the architecture baseline.

## Boundary

- RAG API owns embedding calls.
- Hermes role agents do not call embedding models directly by default.
- Embedding model names and dimensions belong in runtime config, not in live Git secrets.

## Metadata to expose

The RAG API should expose index freshness metadata that includes embedding model alias/version and dimension so retrieval results are reproducible.
