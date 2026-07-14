# RAG Query Pipeline

## Standard query flow

```text
role + query + optional corpus_ids
  -> normalize query
  -> enforce role/corpus policy
  -> embed query
  -> retrieve top_k candidates
  -> optional rerank
  -> filter by sensitivity/project scope
  -> resolve citation metadata
  -> return snippets/context with abstention flag
```

## Retrieval strategies

| Strategy | Use case |
|---|---|
| vector search | semantic lookup over standards/templates |
| keyword or BM25 hybrid | exact terms, API field names, glossary terms |
| metadata filter | role/corpus/project/sensitivity boundaries |
| reranking | long result list or high-risk decisions |

## Confidence and abstention

The API should return `abstain=true` when:

- no result meets threshold
- requested corpus is not active or not allowed
- citation metadata is unavailable
- retrieval backend is unavailable and no approved fallback exists

Hermes role agents must treat `abstain=true` as a hard evidence boundary.
