# Code Review Findings Contract

## Purpose

Define a runtime-neutral EKSAD deliverable for attributable technical review findings without depending on a specific agent runtime or review tool.

## Owner

- Primary owner: `technical-leader`.
- Security findings may be raised by any role, but AppSec review coordination remains with the System Analyst or Technical Leader and residual-risk acceptance remains with the named authority.

## Required inputs

- Immutable source identity: repository, branch, commit/PR, and review cut-off.
- Approved requirement/design references applicable to the change.
- Build, test, static-analysis, dependency, and security evidence available at review time.
- Declared review scope and explicit exclusions.

## Required sections

1. Review identity and evidence cut-off.
2. Scope, exclusions, and source references.
3. Findings grouped by severity.
4. For each finding: affected path/location, evidence, impact, required remediation, and accountable owner.
5. Positive confirmations and checks performed.
6. Open risks, assumptions, and unavailable evidence.
7. Verdict: `APPROVE`, `APPROVE_WITH_CONDITIONS`, `CHANGES_REQUIRED`, or `BLOCKED`.
8. Follow-up and handoff metadata.

## Invariants

- Never claim a check was run without attributable evidence.
- Absence of findings is not proof of security, correctness, or production readiness.
- Review verdict does not replace QA, security, release, business, or production approval.
- High/critical unresolved findings or missing mandatory evidence fail closed.
- Do not expose credentials, confidential source fragments, or raw sensitive logs.

## Runtime adapters

Adapters may add tool commands or formatting, but they must preserve this ownership, evidence, severity, verdict, and approval boundary. Runtime-specific implementation links belong in the adapter's own index, not in this portable contract.
