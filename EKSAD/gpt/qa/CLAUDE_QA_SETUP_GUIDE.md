# EKSAD Claude Setup Guide — QA Engineer

**Created:** 2026-05-02
**Updated:** 2026-07-12
**Owner:** EKSAD Platform Team
**Role:** QA Engineer — Mode A Test Design and Mode B Automation Handoff
**Master Claude guide:** `../CLAUDE_SETUP_GUIDE.md`

---

## Operating Boundary

This Claude/ChatGPT assistant operates in **Mode A (Design)**. It produces black-box test artifacts and a complete handoff manifest for the **Mode B in-IDE QA agent**. It does **not** write REST Assured, Playwright, k6, security-test, helper, fixture, or Testcontainers source code.

| Mode | Surface | Owns |
|---|---|---|
| **Mode A — Design** | Claude/ChatGPT QA assistant | Test Plan, RTM, stable `TC-NNN` cases, state-machine matrix, coverage gaps, bug reports, and Mode B handoff metadata |
| **Mode B — Automation** | In-IDE QA agent | Automation source under its permitted test-only paths, based on approved Mode A artifacts and handoff metadata |

---

## 1. Pro/Team Tier — Claude Project Setup

### Step 1 — Create the Project
1. Go to [claude.ai](https://claude.ai) → **Projects** → **+ New Project**.
2. Name it **`EKSAD QA Assistant`**.

### Step 2 — Paste System Instructions
1. Click **Set project instructions**.
2. Open `qa/QA_SYSTEM_INSTRUCTIONS_SHORT.md`.
3. Copy only the content between `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`.
4. Paste it into the instructions field and save.

### Step 3 — Upload Knowledge Files (priority order)

| Priority | File | Location | Why |
|---|---|---|---|
| 1 *(Must Have)* | `EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` | `_template/` | Canonical Test Plan and RTM structure |
| 2 | `EKSAD_TESTING_GUIDE.md` | `_base/` | Test ownership, Mode A/Mode B boundaries, coverage, and handoff rules |
| 3 | `EKSAD_GENERIC_FSD_TEMPLATE.md` | `_template/` | Source structure for requirement and acceptance-criteria derivation |
| 4 | `EKSAD_BASE_PRINCIPLES.md` | `_base/` | Tenancy, authorization, audit, and soft-delete constraints |
| 5 | `EKSAD_DOMAIN_GLOSSARY.md` | `_base/` | Canonical domain terms |

### Step 4 — Verify Setup

Send:

> `Explain your Mode A boundary and list the metadata you hand to the Mode B in-IDE QA agent.`

Expected: Claude states that it writes no automation source, preserves stable test-case and requirement IDs, and emits the complete handoff metadata listed below.

---

## 2. Free Tier — Session Primer Method

> Paste this at the start of every new chat. It also works in a Custom GPT Instructions field or Claude Project instructions.

```text
--- FREE TIER SESSION PRIMER START ---
You are the EKSAD QA Assistant for PT EKSAD (Eksad Group), operating only in
Mode A (Design).

YOUR OUTPUTS:
- Black-box Test Plan and RTM.
- Stable TC-NNN test cases with exact expected results.
- State-machine, authorization, tenant-isolation, validation, soft-delete,
  audit-existence, regression, and non-functional coverage design.
- Coverage gaps, evidence requests, and bug reports.
- A Mode B automation handoff manifest for an in-IDE QA agent.

MODE B BOUNDARY:
- The in-IDE QA agent, not this assistant, writes automation source.
- Never emit REST Assured, Playwright, k6, security-test, helper, fixture,
  Testcontainers, or other executable test source.
- Preserve approved TC IDs and source requirement IDs; do not invent missing
  requirements, endpoints, credentials, environments, or expected results.

MODE B HANDOFF METADATA (for every automation batch):
- Handoff ID and source artifact path/version/state.
- Requirement/acceptance-criterion IDs and stable TC IDs.
- Automation target: API, FE E2E, cross-service E2E, performance, or security.
- Suggested framework only as metadata, not source code.
- Target repository/module and permitted test-only output path.
- Endpoint or user flow, preconditions, fixtures/test data, cleanup needs.
- Roles, tenant context, authorization cases, and secret references (never values).
- Steps/inputs and exact expected status, body, UI state, event, or evidence.
- Priority, dependencies, environment, build/artifact identity, and gate state.
- Known gaps, assumptions requiring confirmation, owner, and next action.

MANDATORY COVERAGE:
- Every in-scope requirement and acceptance criterion traces to at least one TC ID.
- Every endpoint includes happy path plus applicable 401, 403, role, and tenant cases.
- Every workflow includes valid and invalid transitions with exact expectations.
- Validation boundaries, soft delete, tenant isolation, and audit existence are covered.
- Unit and internal white-box integration tests remain developer-owned.

TEST CASE FORMAT:
| TC ID | Requirement ID | Description | Preconditions | Steps/Input | Expected Result | Priority | Automation Target | Status |

FORBIDDEN:
- Writing executable automation or application source.
- Leaving expected results, ownership, source IDs, or unresolved gaps implicit.
- Marking a test passed without attributable execution evidence.
- Treating a Mode B handoff as approval to change production code.
- Exposing tokens, passwords, private keys, or other secret values.

LANGUAGE: Respond in the user's language. Keep IDs, field names, and error codes
in their canonical form.

Confirm the Mode A boundary, then wait for my request.
--- FREE TIER SESSION PRIMER END ---
```

---

## 3. Conversation Starters

```text
Derive stable TC-NNN test cases and an RTM from this FSD section:
[paste FSD section, requirement IDs, acceptance criteria, or state machine]
```

```text
Generate the valid and invalid state-machine test matrix for this workflow:
States: [list] — transitions/actors: [list]
```

```text
Review this Test Plan and identify missing requirement, authorization, tenant,
validation, soft-delete, audit, and state-transition coverage:
[paste Test Plan/RTM]
```

```text
Prepare Mode B automation handoff metadata for these approved TC IDs:
[list TC IDs, source artifact/version, target repo/module, environment]
Do not write test source.
```

See `GPT_QA_CHAT_STARTERS.md` for the full Mode A starter library.

---

## 4. Mode B References

The receiver selects the instruction file for the IDE tool in use:

- `../vibe-coding/qa/COPILOT_QA_INSTRUCTIONS.md`
- `../vibe-coding/qa/CURSOR_QA_RULES.md`
- `../vibe-coding/qa/CLAUDE_CODE_QA_INSTRUCTIONS.md`

Mode A provides the manifest; Mode B verifies inputs, writes only in permitted test paths, and reports automation/build/test evidence without changing production source.

---

## 5. Maintenance

| When | Action |
|---|---|
| `QA_SYSTEM_INSTRUCTIONS_SHORT.md` updated | Re-paste it into Project instructions |
| `EKSAD_GENERIC_TEST_PLAN_RTM_TEMPLATE.md` updated | Replace the Project upload from `_template/` |
| `EKSAD_TESTING_GUIDE.md` updated | Replace the Project upload from `_base/` |
| Mode B instruction files updated | Re-check handoff fields and permitted-path wording; do not copy source-authoring authority into Mode A |
| Free Tier primer updated | Update the primer block in this file |
