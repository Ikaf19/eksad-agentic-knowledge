# EKSAD DevOps Engineer — Chat Starters

Use these starters with the EKSAD DevOps Engineer. Replace placeholders with real references; do not paste credentials.

## Pipeline Design

1. `Design a Jenkins pipeline for GitLab CE project <project>. Pin full commit SHA, run tests, SonarQube, and Trivy through Jenkins, publish an immutable artifact, and identify every gate/evidence record. Mark unknown policy values TBD with owner and due date.`
2. `Review this Jenkinsfile for source identity, build-once promotion, credential masking, mandatory scan behavior, retry safety, and evidence publication. Do not execute or modify anything.`
3. `Create a CI/CD Pipeline Design using the EKSAD template for <service>. Inputs are <references>. Do not invent thresholds or approvals.`

## Quality and Security Gates

4. `Assess Jenkins build <job/build> for release readiness using its SonarQube task and Trivy report. Distinguish failed, blocked, passed, and waived controls.`
5. `Prepare a time-bounded exception request for finding <ID>. Do not approve it; identify required authority, accepted risk, compensating controls, expiry, and follow-up owner/date.`
6. `Explain why this SonarQube/Trivy evidence cannot authorize artifact <digest>. Identify exact identity or freshness mismatches.`

## Environment Readiness

7. `Assess the three-VM Docker Compose environment using the EKSAD Environment Readiness template. Cover inventory, network, access, capacity, backup/restore, dependencies, drift, observability, deployment, and rollback.`
8. `Review this environment inventory for single points of failure. Do not claim high availability merely because three VMs exist.`
9. `Create an allowlisted network-flow and credential-reference checklist for Hermes, LiteLLM, Keycloak, PostgreSQL, Milvus, MinIO, Redis, Jenkins, SonarQube, Prometheus, Grafana, and Loki.`

## Deployment and Rollback

10. `Draft a deployment and rollback runbook for <environment>, release <version>, commit <SHA>, artifact <digest>. Label every command NOT RUN and list the production authorization metadata still required.`
11. `Validate whether this production request is executable. Check named authority, acting person, authority evidence, exact target, digest, actions/exclusions, change reference, window, rollback triggers/authority, and participants.`
12. `Compare deployed digest <observed> with authorized digest <approved>. Provide a fail-closed response and incident/escalation handoff if they differ.`
13. `Prepare post-deployment verification using Prometheus, Grafana, and Loki references. Keep state DEPLOYED_NOT_VERIFIED until declared evidence passes.`

## Release Evidence

14. `Assemble a Release Evidence pack for <release>. Bind GitLab SHA/MR, Jenkins build, SonarQube, Trivy, artifact digest, QA evidence, environment readiness, rollback, authorization, deployment, and verification.`
15. `Audit this release evidence pack for mutable links, missing identity, stale evidence, hidden waivers, missing owners/dates, and conflated pass/approval claims.`
16. `Return READY, NOT_READY, or BLOCKED for this release. Do not authorize production.`

## Incident and Recovery

17. `Create an Incident Handoff from these observed facts and evidence. Separate confirmed facts, hypotheses, and ruled-out causes; do not invent root cause.`
18. `Assess whether rollback is authorized and safe using this runbook and current evidence. Stop if scope, authority, data implications, or target are ambiguous.`
19. `Prepare a restore-test plan for <asset>. Distinguish backup job success from proven recovery and leave RTO/RPO as TBD unless approved.`

## Architecture and Handoffs

20. `Validate the end-to-end handoff PM → BA → System Analyst → TL → Developer → QA → DevOps. Identify missing artifact versions, owners, evidence, and gate authorities.`
21. `Map objective → requirements → design → task → commit/MR → Jenkins build → tests/scans → digest → named release authorization → deployment → operational verification → release closure.`
22. `Review whether this request belongs to DevOps. If it asks for BRD/FSD/TSD, application implementation, QA verdict, PM governance, or business approval, route it to the accountable role and provide only the DevOps handoff.`

## Secret and Access Safety

23. `Review this configuration for secret exposure. Redact values and recommend credential IDs/secret references; do not repeat discovered secrets.`
24. `Design least-privilege service identities for GitLab-to-Jenkins, Jenkins-to-registry, Jenkins deployment, and observability evidence access. Leave exact permissions TBD when policy is absent.`