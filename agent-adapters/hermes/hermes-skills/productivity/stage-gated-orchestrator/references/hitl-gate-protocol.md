# HITL Gate Protocol — EKSAD Stage-Gated Orchestrator

## Purpose

A gate separates artifact production from downstream execution. Completing a document does not authorize the next role to begin. Verification opens the gate; a human decision resolves it.

## State Model

```text
pending → in_progress → validating → awaiting_review
                                  ↘ blocked
awaiting_review → approved → next stage unlocked
awaiting_review → revision_required → in_progress
awaiting_review → skipped → next stage unlocked
awaiting_review → aborted → pipeline stopped
```

When gates are disabled explicitly, `complete` transitions from validation directly to `approved` while preserving the verification event.

## Decisions

### APPROVE

Meaning: artifact is accepted as the baseline for the next stage.

Required behavior:

1. Record reviewer/user and note.
2. Mark current stage `approved`.
3. Unlock only the immediate next stage.
4. Pass the approved artifact path to the next worker.

Approval of an artifact does not authorize git commit or push.

### REVISE

Meaning: artifact is not accepted; the same stage must be revised.

Required behavior:

1. Record feedback verbatim or as a faithful concise summary.
2. Increment revision count.
3. Mark stage `revision_required`.
4. Re-dispatch the same role with original context plus feedback.
5. Re-run all verification checks.
6. Open a new gate after revision.

Do not start dependent work while revision is pending.

### ABORT

Meaning: stop the pipeline.

Required behavior:

1. Record the reason.
2. Mark current stage `aborted`.
3. Leave current and previous artifacts untouched.
4. Cancel dependent tasks.
5. Stop background workers associated only with this pipeline when possible.

### SKIP

Meaning: bypass human approval and unlock the next stage despite the current artifact not being formally approved.

Required behavior:

1. Require a note/reason.
2. Record decision as `skipped`, never as `approved`.
3. Warn the next worker that its source artifact was not approved.
4. Preserve this condition in the final report.

## User Prompt

After verification, ask:

```text
Gate <STAGE> siap direview.
Artifact: <path>
Verification: PASS

Pilih salah satu:
- APPROVE — baseline dan lanjut stage berikutnya
- REVISE <catatan> — revisi stage ini
- ABORT <alasan> — hentikan pipeline
- SKIP <alasan> — lanjut tanpa approval formal
```

Silence, “ok nanti”, or unrelated messages are not approval.

## Gate Invariants

- Exactly one active stage in a sequential pipeline.
- Downstream stages stay locked until APPROVE/SKIP.
- Verification must pass before `awaiting_review`.
- Every gate decision is timestamped and appended to `events.jsonl`.
- A user can change a prior decision only through a new explicit event; history is append-only.
- Document review and git authorization are separate gates.
