# BA GPT Setup Guide

> **Version:** 1.0
> **Date:** 2026-05-02
> **Keep this file for your own reference — do not upload it to the GPT.**

---

## Step 1 — Create the Custom GPT

1. Go to [chat.openai.com](https://chat.openai.com) → profile → **My GPTs** → **Create a GPT**
2. Switch to the **Configure** tab
3. Fill in:

| Field | Value |
|---|---|
| **Name** | `EKSAD Business Analyst Assistant` |
| **Description** | `Helps BAs write BRD, FSD, User Requirements, business rules, and acceptance criteria following EKSAD standards.` |
| **Model** | GPT-4o |

---

## Step 2 — Paste the System Instructions

1. Open `GPT_BA_SYSTEM_INSTRUCTIONS_SHORT.md` (this folder)
2. Copy everything **between** `---SYSTEM PROMPT START---` and `---SYSTEM PROMPT END---`
3. Paste into the **Instructions** field in the Configure tab

> **Why the SHORT version?** ChatGPT's Instructions field has a character limit. The SHORT version (≤ 8K chars) is purpose-built for this. The LONG version (`GPT_BA_SYSTEM_INSTRUCTIONS.md`) is for offline reference and team documentation.

---

## Step 3 — Upload Knowledge Files

In the **Configure** tab → scroll to **Knowledge** → upload the following 4 files **in this order:**

| # | File | Location | Why It's Needed |
|---|---|---|---|
| 1 | `GPT_BA_SYSTEM_INSTRUCTIONS.md` | `business-analyst/` | Full governing rules — pipeline, quality controls, prohibited behaviours (long reference) |
| 2 | `EKSAD_GENERIC_BRD_TEMPLATE.md` | `_template/` | Exact BRD structure the GPT must follow |
| 3 | `EKSAD_GENERIC_FSD_TEMPLATE.md` | `_template/` | Exact FSD structure the GPT must follow |
| 4 | `EKSAD_BA_DOMAIN_GLOSSARY.md` | `_base/` | BA pipeline terms + EKSAD platform business rules |

> **Upload as `.md` files.** Do not convert to PDF or Word — the GPT reads plain text most reliably from `.md`.

---

## Step 4 — Set Capabilities

In the **Configure** tab under **Capabilities:**

| Capability | Setting | Reason |
|---|---|---|
| Web Browsing | **Off** | The GPT should only use your uploaded knowledge, not search the web |
| DALL·E Image Generation | **Off** | Not needed for documentation work |
| Code Interpreter | **On** | Needed for Mermaid diagram generation and table formatting |

---

## Step 5 — Add Conversation Starters

Add these in the **Conversation Starters** section (pick 4):

1. `I have some User Stories — help me turn them into User Requirements`
2. `Bantu saya tulis BRD untuk service baru: [nama dan tujuan service]`
3. `I have a BRD ready — help me write the FSD for module [name]`
4. `Can you review my existing BRD for gaps?`
5. `Draft FSD untuk modul [nama modul] — saya akan jelaskan alurnya`
6. `Identify business rules from this process: [describe process]`

---

## Step 6 — Test After Setup

Run these test prompts after setup to verify the GPT is behaving correctly:

| Test Prompt | Expected Behaviour |
|---|---|
| `Write me a BRD` | GPT asks for User Requirements first — does NOT immediately write a BRD |
| `Write me an FSD` | GPT asks if BRD is baselined — does NOT immediately write an FSD |
| `Design me a database schema` | GPT refuses and redirects to data requirements in the FSD |
| `Write me a Technical Spec` | GPT refuses and explains scope boundary |
| `I have these User Stories: [paste stories]` | GPT derives User Requirements and asks for confirmation before proceeding |
| `Review my BRD: [paste BRD]` | GPT produces a structured gap report, not a silent rewrite |

---

## How to Update Knowledge Files Later

1. Go to your GPT → **Edit** → **Configure** tab
2. Under **Knowledge**, click **×** next to the file you want to replace
3. Upload the new version
4. Click **Save**

> Always increment the version number inside the file before re-uploading so you can track which version is live.

---

## Team-Specific Extension

To create a project-specific BA GPT (e.g., TIA Reporting BA GPT, HR BA GPT):

1. Start from this base GPT setup
2. Upload one additional domain knowledge file from `business-analyst/teams/{team}/`
3. Update the GPT **Name** and **Description** to reflect the project

Example:
```
EKSAD BA GPT  +  teams/tia/TIA_DOMAIN_KNOWLEDGE.md  →  TIA Reporting BA GPT
EKSAD BA GPT  +  teams/hr/HR_DOMAIN_KNOWLEDGE.md    →  HR System BA GPT
```
