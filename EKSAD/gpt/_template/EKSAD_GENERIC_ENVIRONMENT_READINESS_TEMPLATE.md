# EKSAD Generic Environment Readiness Template

> Filename: `{PROJECT_CODE}_{ENV}_ENVIRONMENT_READINESS.md`
> Owner: DevOps Engineer
> Unknown evidence is `Unknown/Blocked`, never Ready.

# {PROJECT_NAME} — {ENVIRONMENT} Environment Readiness

## Document Control

| Field | Value |
|---|---|
| Version/status | {VERSION} / Draft / In Review / Approved / Superseded |
| Environment/classification | {ENVIRONMENT} / {NON_PROD_OR_PROD} |
| Owner/accountable | {DEVOPS_OWNER} / {DEVOPS_LEAD} |
| Architecture/TSD | {REFERENCE} |
| Evidence cut-off | {TIMESTAMP} |
| Readiness expiry | {TIMESTAMP_OR_POLICY} |
| Last updated | {DATE} |

## Revision History

| Version | Date | Author | Change | Review evidence |
|---|---|---|---|---|
| 0.1 | {DATE} | {AUTHOR} | Initial assessment | {REFERENCE_OR_PENDING} |

## 1. Readiness Summary

| Dimension | State | Evidence | Blocker/owner/due |
|---|---|---|---|
| Identity and inventory | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Network/TLS/DNS | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Capacity/storage | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Access/secrets | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Dependencies | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Backup/restore | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Observability | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Deployment/rollback | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Support/incident | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |
| Overall | Unknown / Ready / Not Ready / Blocked / Expired | {REFERENCE} | {DETAIL} |

Overall cannot be Ready when any mandatory dimension is Unknown, Not Ready, Blocked, or Expired.

## 2. Environment Inventory

| Component/service | VM/host | Compose project/container | Version/image digest | Data/volume | Owner | Evidence |
|---|---|---|---|---|---|---|
| Hermes | VM-01 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| LiteLLM | VM-01 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| Keycloak | VM-01 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| PostgreSQL | VM-02 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| Milvus | VM-02 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| MinIO | VM-02 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| Redis | VM-02 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| Jenkins | VM-03 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| SonarQube | VM-03 / {ACTUAL} | {NAME} | {VERSION/DIGEST} | {VOLUME} | {OWNER} | {REFERENCE} |
| Prometheus/Grafana/Loki | VM-03 / {ACTUAL} | {NAME} | {VERSIONS} | {VOLUMES} | {OWNER} | {REFERENCE} |

Three VMs do not imply HA. Record every single point of failure.

## 3. Network, DNS, and TLS

| Flow | Source | Destination/port | Purpose | Auth/TLS | Firewall owner | Evidence/result |
|---|---|---|---|---|---|---|
| {FLOW_ID} | {SOURCE} | {TARGET} | {PURPOSE} | {CONTROL} | {OWNER} | Not Run |

Administrative endpoints, data stores, Redis, Milvus, MinIO admin, Docker sockets, and Jenkins control/agent interfaces must not be exposed to untrusted networks.

## 4. Capacity and Storage

| Resource | Current | Required/approved | Headroom rule | Evidence | State |
|---|---|---|---|---|---|
| CPU | {VALUE} | {VALUE/TBD} | {POLICY/TBD_OWNER_DUE} | {REFERENCE} | Unknown |
| Memory | {VALUE} | {VALUE/TBD} | {POLICY/TBD_OWNER_DUE} | {REFERENCE} | Unknown |
| Persistent storage | {VALUE} | {VALUE/TBD} | {POLICY/TBD_OWNER_DUE} | {REFERENCE} | Unknown |
| Inodes/IO | {VALUE} | {VALUE/TBD} | {POLICY/TBD_OWNER_DUE} | {REFERENCE} | Unknown |

## 5. Identity, Access, and Secrets

| Credential/service account ID | Purpose | Target | Minimum permissions | Owner | Rotation/access-review evidence | State |
|---|---|---|---|---|---|---|
| {REFERENCE_ONLY} | {PURPOSE} | {SYSTEM} | {SCOPE} | {OWNER} | {REFERENCE} | Unknown |

Never record secret values. Verify Keycloak roles/service identities and Jenkins credential references.

## 6. Configuration and Drift

| Configuration | Approved source/version | Observed version/hash | Drift | Owner/action |
|---|---|---|---|---|
| Docker Compose | {GIT_REF} | {HASH} | Unknown | {OWNER} |
| Environment config | {REFERENCE} | {HASH} | Unknown | {OWNER} |
| Jenkins pipeline | {SHA} | {REVISION} | Unknown | {OWNER} |
| SonarQube/Trivy policy | {REFERENCE} | {IDENTITY} | Unknown | {OWNER} |

## 7. Dependencies and Compatibility

| Dependency | Provider | Consumer | Required version/outcome | Acceptance check | Fallback | State/evidence |
|---|---|---|---|---|---|---|
| {DEP_ID} | {PROVIDER} | {CONSUMER} | {REQUIREMENT} | {CHECK} | {FALLBACK} | Unknown |

## 8. Backup, Restore, and DR

| Asset | Backup method/location | Latest verified backup | Restore test | RPO/RTO | Owner | State |
|---|---|---|---|---|---|---|
| {ASSET} | {REFERENCE} | {TIMESTAMP} | {EVIDENCE} | {POLICY/TBD} | {OWNER} | Unknown |

Backup job success is not restore proof. Storage outside the protected failure domain is required unless explicitly waived.

## 9. Observability

| Service | Health | Metrics/Prometheus | Dashboard/Grafana | Logs/Loki | Alerts/runbook | Release marker | State |
|---|---|---|---|---|---|---|---|
| {SERVICE} | {CHECK} | {REFERENCE} | {REFERENCE} | {REFERENCE} | {REFERENCE} | {REFERENCE} | Unknown |

Telemetry blindness during a protected deployment blocks readiness unless an authorized exception defines compensating controls.

## 10. Deployment and Rollback

| Control | Reference | Last validated | Owner | State/evidence |
|---|---|---|---|---|
| Jenkins deploy job | {JOB} | {DATE} | {OWNER} | Unknown |
| Immutable artifact promotion | {PROCESS} | {DATE} | {OWNER} | Unknown |
| Deployment runbook | {VERSION} | {DATE} | {OWNER} | Unknown |
| Rollback artifact/procedure | {VERSION} | {DATE} | {OWNER} | Unknown |
| Maintenance/authorization | {POLICY} | {DATE} | {OWNER} | Unknown |

## 11. Support and Incident Readiness

| Item | Owner/contact reference | Coverage | Runbook/escalation | State |
|---|---|---|---|---|
| Deployment support | {OWNER} | {WINDOW} | {REFERENCE} | Unknown |
| Incident commander | {OWNER} | {WINDOW} | {REFERENCE} | Unknown |
| Communications | {OWNER} | {WINDOW} | {REFERENCE} | Unknown |

## 12. Risks, Exceptions, and TBDs

| ID | Type | Description | Blocking scope | Owner | Due/expiry | Evidence/state |
|---|---|---|---|---|---|---|
| TBD-ENV-001 | TBD | {DECISION} | {SCOPE} | {OWNER} | {DATE} | Open |

## 13. Recommendation and Decision

DevOps recommendation: Ready / Not Ready / Blocked / Expired.

| Decision | Named authority | Acting person | Date | Evidence | Accepted risk/follow-up |
|---|---|---|---|---|---|
| Approve readiness / Reject / Waive | {AUTHORITY} | {PERSON} | {DATE} | {REFERENCE} | {DETAIL} |

Readiness approval does not authorize a specific production deployment.