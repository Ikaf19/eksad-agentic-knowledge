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
| Data quality / dashboard analysis | `eksad.default` | `eksad.reasoning` | Cite data source and limitations. |
| ML experiment design/evaluation | `eksad.reasoning` | `eksad.long_context` | Include assumptions, metrics, risks, and rollback criteria. |
| UX/design workflow | `eksad.default` | `eksad.reasoning` | Design ownership remains UI/UX, not model alias identity. |
| Source-grounded content drafting | `eksad.default` | `eksad.fast` | Use approved sources and cite internal artifacts where required. |
| Security/tool/data/publication-risk classification | `eksad.guardrail` | `eksad.reasoning` | Advisory only; human gate still applies. |
| Screenshot/diagram/chart/wireframe reading | `eksad.visual_input` | `eksad.default` or ask user for text | Only if data classification allows. `eksad.vision` is legacy compatibility. |
| RAG indexing/query embeddings | `eksad.embedding` | runtime operator decision | Service-only alias. |
| RAG reranking | `eksad.reranker` | no rerank / lexical fallback | Service-only alias. |

If the task contains customer-confidential or regulated data, apply `GUARDRAILS_POLICY.md` before routing.
