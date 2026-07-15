# RAG Evaluation Plan

RAG quality must be tested before runtime adoption.

## Evaluation dimensions

| Dimension | Goal | Fixture |
|---|---|---|
| Golden retrieval | Standard questions retrieve expected source paths. | `eval/rag/golden-questions.json` |
| Citation accuracy | Answers cite the right source files. | `eval/rag/expected-citations.json` |
| Abstention | Unknown/out-of-scope queries produce “insufficient evidence”. | `eval/rag/abstention-tests.json` |
| Role boundary | Roles do not retrieve or answer outside ownership. | `eval/rag/role-boundary-tests.json` |
| Project exclusion | TIA/USED-CAR excluded unless activated. | corpus manifests + abstention tests |

## Minimum acceptance before runtime pilot

- 100% corpus manifest validation.
- 100% eval fixture schema validation.
- No active corpus includes TIA/USED-CAR by default.
- Golden questions retrieve at least one expected citation in a pilot runtime.
- Abstention tests do not hallucinate sources.

## Pilot sequence

1. Validate manifests and fixtures.
2. Render ingestion plan from Git.
3. Build a local disposable index from active corpora.
4. Run golden/citation/abstention/role-boundary tests.
5. Record runtime cost/resource notes.
6. Only then consider scheduled re-indexing or MCP exposure.
