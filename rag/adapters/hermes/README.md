# Hermes RAG Adapter Guidance

Hermes can consume this RAG foundation in three ways:

1. Direct file reading/search when no RAG runtime is configured.
2. Local/external RAG API exposed through a custom tool or MCP server.
3. Chatbot-style uploaded bundles for non-tool sessions.

## Runtime apply boundary

Do not edit `~/.hermes/config.yaml`, install a RAG server, or create vector indexes until explicitly approved.

## Suggested Hermes flow

```text
python3 rag/scripts/validate-rag-corpus.py
python3 rag/scripts/render-ingestion-plan.py
review ingestion plan
approve runtime index location and model gateway
build disposable index outside Git
configure Hermes/MCP retrieval adapter
run eval/rag fixtures
```

## Fallback

If no RAG runtime exists, Hermes should use file tools and cite paths directly.
