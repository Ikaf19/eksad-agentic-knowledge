# Chatbot Project RAG Guidance

GPT Project and Claude Project do not use this custom RAG runtime by default. They use their own uploaded-file/project-search behavior.

## Upload strategy

Use corpus manifests as upload guidance:

- Upload `eksad-core` for all projects.
- Upload `eksad-templates` when the role creates BRD/FSD/TSD/test-plan deliverables.
- Upload role instructions for the active role only when context limits are tight.
- Upload project-specific docs only after project activation.

## Behavior rules for chatbot projects

- Treat `rag/` as governance/reference, not a live RAG service.
- Ask the user to upload/paste missing evidence.
- Cite uploaded file names/paths where possible.
- Do not claim that MCP, vector DB, or Hermes tools are available.
