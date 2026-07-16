# UI/UX Workflow

Runtime-neutral workflow for UX discovery, wireframe-level specification, usability review, and frontend handoff.

## Stages

1. **Context intake** — identify target users, jobs-to-be-done, task frequency, constraints, and source requirements.
2. **Journey/task flow** — map entry point, primary path, alternate path, exception path, and completion signal.
3. **Information architecture** — define navigation, grouping, terminology, empty/loading/error states, and progressive disclosure.
4. **Interaction model** — specify form behavior, validation, permissions, status transitions, notifications, and accessibility concerns.
5. **Wireframe/handoff spec** — produce screen inventory, component intent, content hierarchy, and FE acceptance criteria.
6. **Usability review** — identify friction, ambiguity, accessibility risks, and test questions.
7. **Handoff** — route business rule gaps to BA, API/data gaps to SA/Dev, implementation details to Developer Frontend, and verification to QA.

## Output standards

- Preserve business requirement IDs when available.
- Distinguish design recommendation from confirmed requirement.
- Prefer text-first wireframe specs unless a design tool artifact is provided.
- Never invent business rules to make a screen flow look complete.

## Stop conditions

Stop and ask when a core user goal, permission model, required field, state transition, or content/legal constraint is unknown.
