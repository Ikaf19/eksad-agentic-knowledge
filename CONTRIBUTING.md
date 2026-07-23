# Contributing to EKSAD Agentic Knowledge

This repository is a source-of-truth and desired-state repository. A documentation, policy, template, validator, or adapter change may affect multiple roles and runtimes even when no application code changes.

Read `docs/ONBOARDING.md` before contributing.

---

## 1. Non-negotiable boundaries

1. Git stores portable knowledge, policies, templates, schemas, examples, adapters, and read-only validators.
2. Git does not store live runtime state, credentials, customer dumps, vector stores, provider keys, JIRA tokens, billing exports, or production logs.
3. A Git change never grants runtime activation. Runtime activation requires a separate explicit approval.
4. Portable contracts are updated before or together with runtime adapters.
5. Role ownership and approval authority do not expand because a role receives MCP, RAG, model, or Portal access.
6. Current JIRA usage is link-only/manual. JIRA create/update/comment/transition behavior is out of scope until separately designed and approved after an orchestrator foundation exists.

---

## 2. Branch and pull-request workflow

Start from current main:

```bash
git fetch --prune origin
git checkout main
git pull --ff-only origin main
git checkout -b <type>/<short-description>
```

Use conventional prefixes:

```text
feat/  fix/  docs/  ci/  refactor/  test/  chore/
```

Do not make product changes directly on `main`. Keep a PR focused on one coherent source-of-truth slice.

A PR description must include:

- purpose and affected roles/layers;
- source artifact or decision authorizing the change;
- change-impact checklist;
- validation evidence;
- runtime impact (`none` unless a separately approved runtime change exists);
- security/secret assessment;
- unresolved decisions and follow-up work.

---

## 3. Change-impact matrix

Use this matrix before editing. “Review/update” means inspect every listed layer and update it when semantics changed; do not make mechanical edits when no impact exists.

| Change type | Required review/update |
|---|---|
| Add/rename/remove a role | `portable/roles/`, role boundaries, collaboration/deliverable matrices, workflows, Hermes instruction, Hermes skill, resync map, MCP profile/manifests, RAG matrix/manifests, LLM aliases/defaults, eval fixtures, onboarding, validators |
| Change role authority | Role card, `role-boundaries.md`, collaboration matrix, skill/system instruction, approval policy, eval forbidden behavior |
| Change a deliverable/template | Template, deliverable matrix/contract, owning workflow/skill, chatbot upload guide, RAG corpus manifest, citation/eval fixtures |
| Change an EKSAD standard | Affected role instructions/skills, setup guides, RAG corpora, examples, version/provenance notes |
| Change an MCP capability | Portable capability/role matrix, server manifest/security/validation, role profiles, adapter examples, MCP validator |
| Change RAG policy/corpus | Portable RAG policy/matrix, corpus manifests, retrieval/citation/security contracts, eval fixtures, RAG validators |
| Change model routing | Portable model matrix/policy, aliases, allowed roles, budgets/fallbacks/guardrails, adapter examples, LLM validator |
| Change Portal delivery model | `portable/portal/`, Portal/JIRA future plans, roadmap, Portal validator; preserve orchestrator dependency and no-write baseline |
| Change Hermes adapter/resync | Portable source contract, instruction/skill, all 13 profile mappings, isolated resync test, role coverage validator; no live apply |
| Change roadmap/status | Roadmap, phase history, candidate queue, relevant future plan, root navigation, roadmap validator |

When unsure, request review from the owning specialist and Technical Leader. General Coordinator may route the review but does not approve specialist semantics.

---

## 4. Review ownership

GitHub usernames or team handles are intentionally not invented in this repository. Until repository teams are configured, PR authors must identify named human reviewers in the PR description using these accountability rules:

| Area | Required semantic reviewer |
|---|---|
| UR/BRD/FSD/business terminology | Business Analyst or named business owner |
| TSD/API/data/event/architecture | System Analyst; Technical Leader for material architecture |
| Backend/frontend implementation guidance | Owning Developer plus Technical Leader |
| QA policy/evidence | QA Engineer |
| PM/gates/change control | Project Manager |
| CI/CD/deployment/release evidence | DevOps Engineer; QA/TL/PM for release gate |
| Data analysis/ML/UX/content | Owning specialist plus named approver from the collaboration matrix |
| Security/privacy/credentials | AppSec trigger owner and named risk authority |
| Cross-layer validators/adapter mechanics | Technical Leader or repository maintainer |

`CODEOWNERS` should be added only when real GitHub users/teams and escalation ownership have been approved.

---

## 5. Validation

Run from repository root:

```bash
./scripts/validate-all.sh
```

For Hermes resync changes, also run the isolated test explicitly:

```bash
bash agent-adapters/hermes/scripts/test-eksad-pack-resync.sh
```

Validators must remain read-only. They must not:

- create or mutate live Hermes profiles;
- install or enable MCP servers;
- build RAG indexes or call embedding providers;
- write live LiteLLM configuration or keys;
- deploy the Web Portal or orchestrator;
- call or write to JIRA.

---

## 6. Secret and sensitive-data policy

Never commit:

- GitHub/GitLab PATs or OAuth tokens;
- provider API keys or LiteLLM master/virtual keys;
- private keys, passwords, connection strings, kubeconfigs, or database exports;
- Keycloak client secrets or realm exports containing credentials;
- JIRA tokens, cookies, webhook secrets, or live card/customer data;
- vector stores, embedding caches, runtime prompts/responses, or billing exports.

Use placeholder environment variable names only. If a secret is exposed in chat, logs, or Git, revoke/rotate it; deletion from a later commit is not sufficient remediation.

---

## 7. Definition of Done

A source-of-truth change is done only when:

- [ ] Scope and owning role are explicit.
- [ ] Source precedence and approval evidence are identified.
- [ ] All affected layers in the change-impact matrix were reviewed.
- [ ] Portable contracts and runtime adapters remain separated.
- [ ] Role boundaries and human approval gates remain intact.
- [ ] Active operational instructions point to the curated repository and `main`.
- [ ] All 13 canonical roles remain covered where applicable.
- [ ] New machine-checkable behavior has validator/test coverage.
- [ ] `./scripts/validate-all.sh` passes.
- [ ] Secret scan is clean.
- [ ] No runtime activation occurred as a side effect.
- [ ] README/onboarding/roadmap/history were updated when navigation or status changed.
- [ ] PR reviewers and unresolved follow-ups are documented.

---

## 8. Runtime activation handoff

If a merged source-of-truth change should later be activated:

1. Create a separate runtime-readiness/apply task.
2. Render or dry-run the exact change.
3. Identify backup/rollback and affected environment.
4. Obtain explicit approval for the runtime scope.
5. Inject credentials locally from an approved secret store.
6. Apply and verify outside this documentation PR.
7. Record runtime evidence in the operational system, not as secrets in Git.
