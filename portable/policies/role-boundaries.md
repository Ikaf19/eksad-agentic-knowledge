# EKSAD Role Boundaries

## Principle

Each EKSAD role owns specific decisions and deliverables. Tool access, MCP access, or runtime agent capability must not expand role authority.

## Boundary rules

1. BA owns business requirements; SA owns technical design.
2. TL owns technical review/governance; Dev owns implementation.
3. QA owns test plan/evidence/verdict recommendation; QA does not own code implementation in Mode A.
4. PM owns coordination and stage gates; PM does not make specialist technical verdicts.
5. DevOps owns operational readiness/evidence; production action remains gated.
6. General Coordinator routes and summarizes; it does not own specialist deliverables.

## Escalation

When a task crosses role boundaries, produce a handoff note rather than silently taking ownership.
