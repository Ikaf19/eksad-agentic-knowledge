# Provider Matrix

This matrix is a planning artifact. It does not endorse a specific provider or store credentials.

| Provider family | Typical use | Data-boundary notes | Gateway binding |
|---|---|---|---|
| OpenAI-compatible generic | First-class contract for Hermes/future harnesses | Use organization-approved endpoint only | `/v1` base URL + key in runtime env |
| LiteLLM virtual models | Reference implementation for alias routing | Keys isolated in LiteLLM runtime | `model_name` maps to EKSAD alias |
| Anthropic | reasoning, long-context | Verify data retention and region policy | via LiteLLM/provider adapter |
| OpenAI | general, vision, embeddings | Verify enterprise/privacy settings | via LiteLLM/provider adapter |
| Gemini | long-context/multimodal candidate | Verify data and regional constraints | via LiteLLM/provider adapter |
| Z.AI / GLM | optional provider diversity | Verify legal/security approval | via LiteLLM/provider adapter |
| MiniMax | optional provider diversity | Verify legal/security approval | via LiteLLM/provider adapter |
| Local/Ollama | development or internal embeddings | Capacity and quality must be evaluated | behind RAG service/gateway |

Provider selection must pass security, cost, and quality review before runtime activation.
