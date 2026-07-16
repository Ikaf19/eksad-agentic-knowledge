# Role Model Matrix

| Role | Primary alias | Escalation / special alias |
|---|---|---|
| General Coordinator | `eksad.fast` | `eksad.default`, `eksad.reasoning` |
| Business Analyst | `eksad.default` | `eksad.reasoning`, `eksad.long_context` |
| System Analyst | `eksad.reasoning` | `eksad.long_context` |
| Technical Leader | `eksad.reasoning` | `eksad.guardrail` |
| Developer Backend | `eksad.default` | `eksad.reasoning` |
| Developer Frontend | `eksad.default` | `eksad.reasoning` |
| QA Engineer | `eksad.default` | `eksad.long_context`, `eksad.reasoning` |
| DevOps Engineer | `eksad.default` | `eksad.guardrail`, `eksad.reasoning` |
| RAG Service | `eksad.embedding` | `eksad.reranker` |

The matrix is desired state. Runtime environment policy can restrict aliases further.
