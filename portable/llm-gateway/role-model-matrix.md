# Role Model Matrix

This matrix is desired state. Runtime environment policy can restrict aliases further. Role agents request stable `eksad.*` capability aliases, not provider-specific model names.

## Normalized role defaults

| Role | Primary | Fallback | Escalate | Large artifact | Visual input | Guardrail |
|---|---|---|---|---|---|---|
| General Coordinator | `eksad.fast` | `eksad.default` | `eksad.reasoning` | `eksad.long_context` | - | `eksad.guardrail` |
| Business Analyst | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| System Analyst | `eksad.reasoning` | `eksad.default` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| Technical Leader | `eksad.reasoning` | `eksad.default` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| Developer Backend | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | - | `eksad.guardrail` |
| Developer Frontend | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| QA Engineer | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| Project Manager | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | - | `eksad.guardrail` |
| DevOps Engineer | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | - | `eksad.guardrail` |
| Data Analyst | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| Data Scientist | `eksad.reasoning` | `eksad.default` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| UI/UX Designer | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| Content Creator | `eksad.default` | `eksad.fast` | `eksad.reasoning` | `eksad.long_context` | `eksad.visual_input` | `eksad.guardrail` |
| RAG Service | `eksad.embedding` | - | - | - | - | - |

## Compatibility aliases

- `eksad.visual_input` is the preferred alias for screenshot, diagram, chart, wireframe, and scanned-artifact understanding.
- `eksad.vision` remains a compatibility alias for older runtime bindings and should not be used as a role `primary` default.
- Service aliases `eksad.embedding` and `eksad.reranker` remain owned by the RAG service, not role-agent chat flows.

## Routing boundaries

Model routing does not change role accountability. A role may use `visual_input`, `guardrail`, or `large_artifact` aliases only for the relevant task class; it must still hand off approval-gated decisions to the owning role/human gate.
