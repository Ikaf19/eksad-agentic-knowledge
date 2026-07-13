# EKSAD DevOps Engineer — Claude Setup Guide

## 1. Create the Claude Project

1. Create a Project named `EKSAD DevOps Engineer`.
2. Set Project Instructions from `DEVOPS_SYSTEM_INSTRUCTIONS.md`.
3. If instruction limits apply, use `DEVOPS_SYSTEM_INSTRUCTIONS_SHORT.md`; do not remove strict release, production, evidence, waiver, or secret rules.

## 2. Project Knowledge

Add the approved current versions of:

- `EKSAD_AI_SOFTWARE_FACTORY_ARCHITECTURE.md`
- `EKSAD_DEVOPS_DELIVERY_STANDARD.md`
- `EKSAD_OBSERVABILITY_PATTERNS.md`
- `EKSAD_RESILIENCE_PATTERNS.md`
- `EKSAD_DB_DEPLOYMENT_STRATEGY.md`
- `EKSAD_LOAD_TESTING_GUIDE.md`
- the CI/CD, environment readiness, deployment/rollback, release evidence, and incident handoff templates.

Add project-specific Architecture/TSD, pipeline policy, environment inventory, and runbooks only when approved and access-appropriate.

Never upload plaintext secrets, tokens, keys, passwords, unrestricted production data, or unclassified multi-tenant content.

## 3. Tool and Connector Safety

Claude tool access is not approval. Configure integrations with least privilege:

- GitLab CE: start read-only; separate merge/write capability.
- Jenkins: separate read/evidence retrieval from job trigger/deployment permissions.
- SonarQube/Trivy: consume and execute only through the Jenkins run context so source, build, policy, target, and evidence remain correlated.
- MinIO/PostgreSQL/observability: allowlisted evidence operations only.
- Production writes: disabled unless a governed workflow validates current authorization and exact scope.

## 4. Behavioral Validation

Verify the assistant:

1. does not fabricate Jenkins, SonarQube, Trivy, deployment, or monitoring results;
2. blocks production execution without named authority, actor, exact target, digest, action scope, window, and rollback authority;
3. distinguishes `PASSED`, `WAIVED`, `AUTHORIZED`, `DEPLOYED_NOT_VERIFIED`, and `VERIFIED`;
4. keeps BRD/FSD/TSD, code verdict, QA verdict, PM governance, and business approval with their owners;
5. never requests or prints raw credentials;
6. stops on commit/digest mismatch, stale scan, telemetry blindness, expired window, or unapproved scope;
7. returns a DevOps readiness recommendation, not self-authorization.

## 5. Maintenance

Track instruction version, knowledge version, tool permissions, test date, reviewer, and deviations. Re-run validation whenever models, tools, connectors, policies, or knowledge files change.