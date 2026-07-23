# EKSAD Agentic Knowledge — Team Onboarding

**Status:** Canonical onboarding entrypoint
**Audience:** New team members, role specialists, knowledge contributors, Hermes operators, and Web Portal engineers
**Runtime policy:** Reading, validating, and contributing to this repository does not activate or modify any live runtime.

---

## 1. Start here

This repository is the Git source of truth for EKSAD AI-assisted delivery. Use this decision tree before opening individual knowledge files:

```text
I need EKSAD standards/templates only
  -> EKSAD/gpt/ + portable/

I use ChatGPT/Claude Projects without tools
  -> docs/USAGE_MODES.md
  -> agent-adapters/chatbot-projects/

I use an independent Hermes role agent
  -> choose a role below
  -> portable role card + role boundary + Hermes instruction + skill
  -> runtime activation remains a separate operator approval

I build the future Web Portal
  -> portable/portal/
  -> docs/future/FUTURE_ALIGN_WEB_PORTAL_CONTROL_PLANE.md

I want JIRA-first automation
  -> not active in the current baseline
  -> requires future Portal + Orchestrator foundations
  -> current mode is link-only/manual and JIRA writes are forbidden
```

If you are unsure which role owns a request, start with `general-coordinator`. It may route and summarize but cannot author or approve specialist-owned deliverables.

---

## 2. Understand the repository layers

| Layer | Purpose | Start path | Runtime implication |
|---|---|---|---|
| Curated standards and templates | EKSAD principles, patterns, role source material, and document templates | `EKSAD/gpt/` | Reference only |
| Portable source of truth | Runtime-neutral roles, workflows, deliverables, and policies | `portable/README.md` | No runtime activation |
| Desired-state capabilities | MCP, RAG, and LLM gateway catalogs/contracts | `mcp/`, `rag/`, `llm-gateway/` | Design/render/validate only |
| Runtime adapters | Packaging for Hermes, chatbot projects, or future harnesses | `agent-adapters/` | Apply only after explicit approval |
| Runtime-local state | Profiles, credentials, indexes, live configs, databases, logs | Outside this repository | Never commit |

### Source precedence

When sources disagree, use this order unless an approved project contract says otherwise:

1. Approved project artifact and named human gate.
2. Current portable policy/role/workflow contract.
3. Current canonical standard or template in `EKSAD/gpt/`.
4. Runtime adapter instruction or skill.
5. Example, historical note, or archived material.

Stop and escalate unresolved conflicts. No project artifact may override role authority, security/privacy controls, mandatory human approval gates, credential policy, production safety, or an explicit no-write boundary. Do not let an old example override a current approved contract.

---

## 3. Choose the owning role

| I need to... | Owning role | Start here | Primary skill |
|---|---|---|---|
| Route an unclear request or coordinate handoffs | General Coordinator | `portable/roles/general-coordinator.md` | `eksad-general-coordination` |
| Define UR, BRD, FSD, business rules, acceptance criteria | Business Analyst | `portable/roles/business-analyst.md` | `eksad-ba-workflow` |
| Define TSD, APIs, data, events, and system design | System Analyst | `portable/roles/system-analyst.md` | `eksad-tsd-design` |
| Review architecture/code and apply technical governance | Technical Leader | `portable/roles/technical-leader.md` | `eksad-code-review` |
| Implement Java/Quarkus/Spring backend changes | Developer Backend | `portable/roles/developer-backend.md` | `eksad-be-impl` |
| Implement React/TypeScript frontend changes | Developer Frontend | `portable/roles/developer-frontend.md` | `eksad-fe-impl` |
| Define test plan/RTM/evidence and QA verdict recommendation | QA Engineer | `portable/roles/qa-engineer.md` | `eksad-qa-delivery` |
| Plan delivery, RAID, status, change control, and gates | Project Manager | `portable/roles/project-manager.md` | `eksad-pm-delivery` |
| Define CI/CD, deployment, rollback, and release evidence | DevOps Engineer | `portable/roles/devops-engineer.md` | `eksad-devops-delivery` |
| Analyze data, metrics, and dashboard requirements | Data Analyst | `portable/roles/data-analyst.md` | `eksad-data-analysis` |
| Design/evaluate ML experiments and model evidence | Data Scientist | `portable/roles/data-scientist.md` | `eksad-data-science` |
| Research UX and produce design handoffs | UI/UX Designer | `portable/roles/ui-ux-designer.md` | `eksad-ui-ux-delivery` |
| Produce sourced content briefs, calendars, and drafts | Content Creator | `portable/roles/content-creator.md` | `eksad-content-creation` |

Always read these shared boundaries:

- `portable/policies/role-boundaries.md`
- `portable/roles/role-collaboration-matrix.md`
- `portable/deliverables/deliverable-matrix.md`

Tool, MCP, RAG, or model access never grants approval authority.

---

## 4. Role card vs instruction vs skill vs profile

These terms are related but not interchangeable:

| Object | Meaning | Canonical location |
|---|---|---|
| Role card | Runtime-neutral ownership and boundary contract | `portable/roles/<role>.md` |
| System instruction | Hermes-specific behavior packaging for a role | `agent-adapters/hermes/role-system-instructions/` |
| Skill | Reusable procedure invoked for a task type | `agent-adapters/hermes/hermes-skills/` |
| Runtime profile | Live Hermes identity/config generated or activated outside Git | `~/.hermes/profiles/` — never committed |
| Legacy Custom GPT setup | Document-centric ChatGPT configuration maintained for a subset of roles | `EKSAD/gpt/README.md` |

The canonical architecture has **13 roles**. A legacy Custom GPT guide may cover fewer configured GPTs; that does not reduce the canonical role set. Source files in Git also do not prove that matching runtime profiles are already activated.

---

## 5. Current operating model

The current initial operating model is:

```text
User/operator
  -> selects one independent Hermes role agent
  -> provides approved source/evidence
  -> role agent produces its owned artifact or handoff
  -> human/operator selects the next role and controls approvals
```

There is no active central orchestrator in this baseline. Therefore:

- role transitions are manual;
- agents must not self-approve;
- JIRA links are context/evidence only;
- JIRA create/update/comment/transition operations are not approved;
- production actions remain human-gated;
- Git desired state is not the same as live runtime state.

The source also contains `stage-gated-orchestrator`, an **optional session-local conductor/tracker skill**. It may be used only when the user explicitly requests a visible multi-role pipeline. It does not provide durable Portal orchestration, does not read or write JIRA, and does not change the default manual independent-profile model above.

Future direction:

```text
Web Portal -> DeliveryProfile / ExternalWorkItemLink
           -> future Orchestrator -> gated role graph
           -> future read-only JIRA-first pilot
```

Read `portable/portal/README.md` for the current boundary.

---

## 6. Validate a checkout

Prerequisites: Bash 4 or newer, Git, Python 3.11 or newer, and standard Unix tools used by the suite (`realpath`, `diff`, `cmp`, `grep`, and GNU/coreutils-compatible file utilities). No provider credential, Hermes runtime, MCP server, RAG database, LiteLLM instance, Portal, or JIRA connection is required.

For a fresh checkout:

```bash
git clone https://github.com/Ikaf19/eksad-agentic-knowledge.git
cd eksad-agentic-knowledge
```

From the repository root, run the unified read-only suite:

```bash
./scripts/validate-all.sh
```

The command validates source structure and contracts only. It must not create profiles, install MCP servers, ingest RAG corpora, write LiteLLM config, deploy the Portal, or call JIRA.

A change is not ready for review until this command passes and a high-confidence secret scan is clean.

Expected final line:

```text
PASS: complete EKSAD source-of-truth validation suite
```

If direct execution is unavailable because the executable bit was not preserved, run `bash scripts/validate-all.sh`. On failure, use the first `FAIL`/`ERROR` section as the owning validator; do not bypass the gate or activate runtime to “test” a source change.

---

## 7. Contribute safely

Before changing knowledge:

1. Read `CONTRIBUTING.md`.
2. Create a branch from current `origin/main`.
3. Identify all affected layers with the change-impact matrix.
4. Update source contracts before runtime adapters.
5. Add or update a validator for machine-checkable behavior.
6. Run `./scripts/validate-all.sh`.
7. Open a PR; do not activate runtime as part of the documentation PR.

Never commit:

- PATs, API keys, passwords, private keys, or connection strings;
- live Hermes/MCP/RAG/LiteLLM/Portal/JIRA config;
- customer dumps, vector stores, embedding caches, or runtime logs;
- production endpoints with credentials.

---

## 8. First-day checklist

- [ ] I understand the difference between portable knowledge and runtime adapters.
- [ ] I selected an owning role and read its role card.
- [ ] I read role boundaries and the collaboration matrix.
- [ ] I know which approved artifact/evidence is authoritative.
- [ ] I understand that current Hermes role execution is independent/manual.
- [ ] I understand that JIRA-first orchestration is future work and JIRA writes are disabled.
- [ ] I ran `./scripts/validate-all.sh` successfully.
- [ ] I know that runtime activation requires a separate explicit approval.

---

## 9. Escalation

Escalate instead of guessing when:

- ownership is unclear;
- source artifacts conflict;
- approval evidence is missing;
- a task crosses role boundaries;
- production, security, privacy, legal, billing, or credential impact exists;
- a setup instruction appears to reference the legacy `brainstorming` repository.

Use a handoff note with source artifact, requested output, owning role, approver, evidence cut-off, risks, assumptions, and recommended next role.
