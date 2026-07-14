# Validation — RAG API Readonly MCP

Before activation:

- [ ] `rag_healthcheck` works.
- [ ] `rag_search` returns `source_path`, `citation`, `sensitivity`, `corpus_id`, and score.
- [ ] forbidden corpus returns structured `CORPUS_FORBIDDEN` error.
- [ ] empty/low-confidence query returns `abstain=true`.
- [ ] artifact metadata endpoint does not expose bucket-wide credentials.
- [ ] write/index/delete tools are absent or disabled.
- [ ] sampling is disabled.
- [ ] role boundary fixtures pass.
