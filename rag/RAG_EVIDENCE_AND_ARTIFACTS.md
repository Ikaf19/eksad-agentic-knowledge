# RAG Evidence and Artifacts

RAG answers must be traceable to source documents and, when relevant, artifacts stored outside Git.

## Source evidence

For Git-backed knowledge, citation metadata should include:

- source path
- section heading
- line range when available
- source commit/version if indexed
- corpus ID

## Artifact evidence

For artifacts such as PDFs, screenshots, CI evidence, scan reports, or release artifacts, the RAG API should expose metadata through:

```text
GET /v1/artifacts/{artifact_id}/metadata
```

The metadata endpoint should not leak bucket-wide MinIO credentials.

## Artifact metadata shape

```json
{
  "artifact_id": "artifact_test_report_001",
  "title": "QA Evidence Report",
  "storage": "minio",
  "bucket_alias": "evidence-readonly",
  "object_key_redacted": "qa/evidence/...",
  "content_type": "application/pdf",
  "checksum_sha256": "placeholder-sha256",
  "sensitivity": "internal",
  "created_at": "2026-07-14T00:00:00Z",
  "citation": {
    "path": "minio://evidence-readonly/qa/evidence/...",
    "section": "Summary"
  }
}
```

Use bucket aliases and metadata. Avoid exposing raw bucket credentials to role agents.
