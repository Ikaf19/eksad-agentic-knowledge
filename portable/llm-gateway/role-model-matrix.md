# Role Model Matrix

| Role | Primary alias | Escalation / special alias |
|---|---|---|
| General Coordinator | `eksad.fast` | `eksad.default`, `eksad.reasoning` |
| Business Analyst | `eksad.default` | `eksad.reasoning`, `eksad.long_context` |
| System Analyst | `eksad.reasoning` | `eksad.long_context` |
| Technical Leader | `eksad.reasoning` | `eksad.guardrail` |
| Developer Backend | `eksad.default` | `eksad.reasoning` |
| Developer Frontend | `eksad.default` | `eksad.reasoning`, `eksad.vision` |
| QA Engineer | `eksad.default` | `eksad.long_context`, `eksad.reasoning`, `eksad.vision` |
| Project Manager | `eksad.default` | `eksad.long_context`, `eksad.guardrail` |
| DevOps Engineer | `eksad.default` | `eksad.guardrail`, `eksad.reasoning` |
| Data Analyst | `eksad.default` | `eksad.long_context`, `eksad.reasoning` |
| Data Scientist | `eksad.reasoning` | `eksad.long_context`, `eksad.default` |
| UI/UX Designer | `eksad.vision` | `eksad.default`, `eksad.long_context` |
| Content Creator | `eksad.fast` | `eksad.default`, `eksad.long_context`, `eksad.guardrail` |
| RAG Service | `eksad.embedding` | `eksad.reranker` |

The matrix is desired state. Runtime environment policy can restrict aliases further. Role agents request stable `eksad.*` capability aliases, not provider-specific model names.
