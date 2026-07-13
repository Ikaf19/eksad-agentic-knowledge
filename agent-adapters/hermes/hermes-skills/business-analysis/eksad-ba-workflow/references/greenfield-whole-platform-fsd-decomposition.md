# Greenfield Whole-Platform FSD Decomposition Heuristic

Use this note when the BRD belongs to a **greenfield whole-platform** project where shared foundations are not already available (for example: no common/core module, auth foundation, audit trail, or shared notification/master-data baseline).

## Why this matters

If BA keeps the FSD too consolidated, cross-cutting business behavior gets hidden inside one large transactional document. The SA/TSD lane may then underestimate the shared-foundation design still required.

## Heuristic

- **Do not default to one FSD** for a broad BRD in a greenfield whole-platform project.
- Choose FSD boundaries from evidence: separable business capabilities/outcomes, distinct actor or rule ownership, independent lifecycle/state models, dependency and approval boundaries, and materially different change/review cadence.
- Split when those dimensions need independent review, baselining, traceability, or change; consolidate when they form one coherent lifecycle and rule set. Do not prescribe or optimize for a document count.
- Keep **cross-cutting business behavior explicit** in BA artifacts even if technical implementation later uses shared services.

## Cross-cutting behavior that must stay visible

- approval behavior and escalation points
- auditability expectations for business actions
- notification triggers and audience rules
- access scope, branch, region, or company visibility rules
- tenant/company data-isolation behavior
- customer/master ownership behavior when shared master data may later be introduced

## Candidate decomposition pattern

Evaluate clusters such as these; use only boundaries supported by the capability, lifecycle, business-rule ownership, dependency, and change-cadence evidence:
1. acquisition / intake
2. conversion / sales initiation
3. settlement / payment / invoice / refund
4. operational readiness / pricing / quality control / reconditioning
5. administration / handover documents
6. governance / reporting / notification / master data / access behavior

## BA → SA handoff reminder

BA describes the **business behavior** of these cross-cutting concerns. SA/TSD later decides the **technical boundaries** for common/core/auth/audit/master-data/notification services.

## Pitfall

Do **not** hide greenfield platform gaps with phrases such as "handled by platform" unless that platform capability actually exists and is in scope. If the foundation does not exist, the BA artifact must make the need visible.
