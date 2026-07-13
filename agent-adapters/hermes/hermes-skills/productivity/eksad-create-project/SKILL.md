---
name: eksad-create-project
description: "Use when the user asks to create a new EKSAD project workspace (via any channel — CLI, Telegram, web). Triggers on phrases like 'create new project', 'new service project', 'init project', 'setup project workspace'. Streamlines the workflow: copy template from /workspace/projects/_example_/, fill PROJECT.md, init git, optional first commit + remote setup."
version: 1.0.0
author: EKSAD Platform Team (Hermes-native)
license: MIT
metadata:
  hermes:
    tags: [eksad, project, workspace, init, telegram, cli]
---

# EKSAD Create Project Skill

Streamlines EKSAD project workspace creation. Works on any Hermes surface (CLI, Telegram, WebUI).

## When to Use

- User says "create new project", "new service project", "init project", "setup project workspace"
- User provides project name, domain, owner
- User wants to bootstrap from the `_example_` template

## When NOT to Use

- Adding docs/code to an EXISTING project → just `cd` to it
- Modifying an existing project's metadata → edit `PROJECT.md` directly
- Creating a non-EKSAD project → use plain `git init`

## Workflow

### Step 1 — Gather Required Inputs

Ask user (or extract from message):
- **Project name** (e.g., `svc-leads`, `tia-v3`, `used-car-dashboard`)
- **Domain** (Automotive / HRIS / Finance / Other)
- **Owner** (name + email)
- **Project code** (short ID for docs, e.g., `LEADS`, `TIA`)
- **Stack Profile** (Quarkus/SB, Reactive/Imperative, RabbitMQ/Kafka) — optional, SA decides later

If missing, ask. Don't fabricate.

### Step 2 — Copy Template

```bash
SRC="/workspace/projects/_example_"
DST="/workspace/projects/<project-name>"
cp -r "$SRC" "$DST"
```

### Step 3 — Fill PROJECT.md

Edit `/workspace/projects/<project-name>/PROJECT.md`:

```markdown
## Project Metadata

| Field | Value |
|-------|-------|
| **Project Name** | <user-provided> |
| **Project Code** | <user-provided> |
| **Owner** | <user-provided> |
| **Domain** | <user-provided> |
| **Git Remote** | (pending — add when ready) |
| **Status** | Draft |
| **Created** | <YYYY-MM-DD> |
| **Last Updated** | <YYYY-MM-DD> |
```

### Step 4 — Fill .hermes.md

Edit `/workspace/projects/<project-name>/.hermes.md` — update "Owner" and "Domain" sections.

### Step 5 — Initialize Git

```bash
cd "/workspace/projects/<project-name>"
git init
git branch -M main
git config user.name "Hermes Agent"
git config user.email "hermes@eksad.local"
git add .
git commit -m "chore: initialize <project-name>"
```

### Step 6 — Report & Next Steps

Output to user:
```
✅ Project created at /workspace/projects/<project-name>/

Files:
- PROJECT.md          (owner, scope, status)
- .hermes.md          (anchors profile context)
- BRD/ FSD/ UR/ TSD/ testplans/ CODE/  (empty folders)

Git: initialized locally, 1 commit on main

📌 Next steps:
1. cd /workspace/projects/<project-name>/
2. Start BA work:  hermes -p business-analyst
3. Or via Telegram: send /profile business-analyst then start

🔗 Remote setup (when ready):
   git remote add origin <your-repo-url>
   git push -u origin main
```

## Telegram-Specific Adaptations

When running via Telegram:
- Use shorter output (avoid long bash output dumps)
- Show ✅/❌ status markers
- For long operations, stream progress or use summary at end
- Never dump PAT or secrets in output

## Multi-Project Considerations

- One project per `cp -r` from `_example_`
- Don't symlink across projects — each needs own git repo
- If user creates project with same name → ask before overwriting
- If `/workspace/projects/_example_/` is missing → suggest `hermes knowledge pack refresh` or recreate template

## Forbidden

❌ Initialize project without confirming name, owner, domain
❌ Push to remote without explicit user instruction
❌ Modify `PROJECT.md` of existing projects without user request
❌ Delete files from `_example_/` (it's the template source)

## Commit Pattern (per project)

```bash
cd /workspace/projects/<project-name>/
git add <file>
git commit -m "<type>(<scope>): <change>"
git push   # only after first remote setup
```