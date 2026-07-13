# EKSAD DevOps Production Safety

## Production Authorization Envelope

Before any production mutation, require all fields:

1. Named release/change authority.
2. Acting person using attributable identity.
3. Authority source and decision evidence.
4. Exact environment/account/VM/service/namespace/Compose target.
5. Release/version, full commit SHA, and immutable artifact digest.
6. Allowed actions and explicit exclusions.
7. Change/release reference.
8. Approved start/end window with timezone.
9. Required participants and communication channel.
10. Prechecks and stop conditions.
11. Rollback trigger, procedure, artifact, and rollback authority.
12. Current mandatory-gate and exception evidence.

Missing, ambiguous, unverifiable, mismatched, or expired data means `BLOCKED` before mutation.

## Immediate Preflight

Reconfirm immediately before execution:

- authenticated actor/build identity;
- current time is within approved window;
- target identity and environment classification;
- authorized SHA/digest equals candidate and command input;
- current deployed identity and health;
- Jenkins job/runbook revision is approved;
- mandatory gates remain eligible;
- backup/migration/rollback prerequisites are current;
- Prometheus/Grafana/Loki and health checks are available;
- required participants and incident escalation are reachable;
- command/action is inside allowed scope and exclusions.

Stop rather than reinterpret an authorization.

## Execution Discipline

1. Prefer the approved Jenkins production stage over ad-hoc commands.
2. Record target, purpose, effect, reversibility, and authorization before each mutation.
3. Use credential IDs/secret references only; disable unsafe tracing and redact output.
4. Execute one controlled step at a time and capture real exit/status evidence.
5. Stop on unexpected output, target, drift, failure, or scope expansion.
6. Never make a second unrelated change to “help” the release.
7. Never delete evidence or conceal deviations.

## Deployment State

`not_started → prechecking → deploying → deployed_not_verified → verified`.

Interrupt states: `failed`, `rolling_back`, `rolled_back`, `aborted`.

A successful command or Jenkins stage may establish `deployed_not_verified`; only declared operational verification establishes `verified`.

## Rollback

Rollback requires a recorded trigger and authority unless the approved emergency/runbook policy explicitly pre-authorizes automatic rollback for named conditions. Record:

- trigger evidence and decision time;
- deciding authority and actor/build;
- failed/new and prior/restored digests;
- rollback job/commands and exits;
- migration/data compatibility and actions;
- post-rollback health/telemetry;
- incident and communication references;
- residual risk, owner, and next action.

If rollback is unsafe, ambiguous, or fails, do not improvise destructive recovery. Escalate under the incident process.

## Data and Destructive Operations

Database migration, restore, deletion, cleanup, credential rotation, access change, and irreversible configuration require explicit scope beyond ordinary deployment approval. Validate backups and compatibility first. Never infer permission from shell access or a broad job credential.

## Emergency Change

Urgency does not remove identity, exact scope, audit, rollback, secret, or retrospective-review requirements. Use the documented emergency authority and record any abbreviated controls, accepted risk, expiry, and follow-up.

## Secret Exposure

If output/configuration reveals a secret:

1. do not repeat the value;
2. stop unsafe propagation;
3. notify the authorized security/credential owner;
4. revoke/rotate through the approved procedure;
5. identify affected systems/logs/artifacts without copying the secret;
6. open/update incident and preserve evidence;
7. verify replacement and access scope.

Deleting chat, logs, or Git text alone is not remediation.

## Final Verification

Record exact deployed digest, service/container state, health checks, smoke evidence supplied by accountable roles, metrics/logs/alerts, observation period, release marker, deviations/incidents, and handoff owner. Any absent required evidence remains `unknown/blocked`, never Green.