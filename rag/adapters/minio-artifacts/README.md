# MinIO Artifact Adapter Notes

MinIO stores artifacts and evidence such as QA reports, screenshots, release evidence, CI logs, exported PDFs, or scan reports.

## Boundary

- RAG API exposes artifact metadata and approved evidence references.
- Hermes should not receive bucket-wide MinIO credentials.
- Raw object download should be mediated by signed URLs or a policy-approved evidence endpoint.

## Recommended metadata

- `artifact_id`
- `bucket_alias`
- `object_key_redacted`
- `content_type`
- `checksum_sha256`
- `sensitivity`
- `created_at`
- `source_system`
- `citation`
