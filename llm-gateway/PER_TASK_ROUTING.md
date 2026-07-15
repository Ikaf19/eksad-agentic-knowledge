# Per-Task Routing

| Task class | Preferred alias | Fallback | Notes |
|---|---|---|---|
| Intake, triage, routing | `eksad.fast` | `eksad.default` | Keep cheap/fast. |
| Short summary/status update | `eksad.fast` | `eksad.default` | No deep reasoning expected. |
| BRD/FSD drafting | `eksad.default` | `eksad.reasoning` | Use RAG citations where applicable. |
| BRD/FSD readiness assessment | `eksad.reasoning` | `eksad.default` | Gate decisions must be evidence-backed. |
| TSD/architecture design | `eksad.reasoning` | `eksad.long_context` | Use long context only for large artifacts. |
| Large spec comparison | `eksad.long_context` | `eksad.reasoning` | Prefer retrieval over dumping full corpora. |
| Code explanation/refactor plan | `eksad.default` | `eksad.reasoning` | Code execution/tool usage remains separate. |
| Root-cause debugging | `eksad.reasoning` | `eksad.default` | Follow systematic debugging skill when applicable. |
| QA test plan / RTM | `eksad.default` | `eksad.long_context` | Use cited requirements/evidence. |
| Security/tool-risk classification | `eksad.guardrail` | `eksad.reasoning` | Advisory only; human gate still applies. |
| Screenshot/diagram reading | `eksad.vision` | ask user for text | Only if data classification allows. |
| RAG indexing/query embeddings | `eksad.embedding` | runtime operator decision | Service-only alias. |
| RAG reranking | `eksad.reranker` | no rerank / lexical fallback | Service-only alias. |

If the task contains customer-confidential or regulated data, apply `GUARDRAILS_POLICY.md` before routing.
