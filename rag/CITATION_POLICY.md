# Citation Policy

## Rule

Any answer materially based on RAG evidence must cite the repository source path.

Preferred citation shape:

```text
Source: `EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md` → "Tenant Isolation"
```

For concise answers, path-only citation is acceptable:

```text
(`EKSAD/gpt/_base/EKSAD_BASE_PRINCIPLES.md`)
```

## Citation requirements by source

| Source type | Citation required | Notes |
|---|---:|---|
| `_base` standards | Yes | Binding rules. |
| `_template` docs | Yes | Output contracts. |
| portable policies/workflows | Yes | Governance and process rules. |
| adapter docs | Yes when used | Adapter docs are implementation guidance only. |
| project-specific docs | Yes | Include project/corpus id if active. |
| runtime observations | Yes | Cite tool output, PR, CI, or evidence handle where possible. |

## No-citation response

If no citation can be produced, the agent should say:

```text
Saya belum menemukan evidence/citation di knowledge repo untuk klaim itu.
```

Do not fabricate file paths or section names.
