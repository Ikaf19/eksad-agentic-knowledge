# ChatGPT Setup Guide — EKSAD Project Manager

## Purpose

Create a Custom GPT that supports EKSAD delivery governance without taking ownership from Business Owner, BA, System Analyst/Solution Architect, TL, Developers, or QA.

## Custom GPT Configuration

| Field | Value |
|---|---|
| Name | EKSAD Project Manager Assistant |
| Description | Evidence-based EKSAD project initiation, planning, RAID, status, change control, and stage-gate coordination. |
| Instructions | Paste content between START/END markers from `PM_SYSTEM_INSTRUCTIONS_SHORT.md` |
| Web Search | Off by default |
| Code Interpreter | Optional; not required for core PM workflow |
| Image Generation | Off |

## Knowledge Upload Order

Upload these active files only; never upload `archive/`.

1. `_base/EKSAD_PROJECT_MANAGEMENT_STANDARD.md`
2. `_template/EKSAD_GENERIC_PROJECT_CHARTER_TEMPLATE.md`
3. `_template/EKSAD_GENERIC_PROJECT_PLAN_TEMPLATE.md`
4. `_template/EKSAD_GENERIC_WBS_TEMPLATE.md`
5. `_template/EKSAD_GENERIC_RAID_LOG_TEMPLATE.md`
6. `_template/EKSAD_GENERIC_STATUS_REPORT_TEMPLATE.md`
7. `_template/EKSAD_GENERIC_CHANGE_REQUEST_TEMPLATE.md`
8. `_base/EKSAD_DOMAIN_GLOSSARY.md`
9. `_base/EKSAD_BA_DOMAIN_GLOSSARY.md` only when requirement terminology is needed

## Conversation Starters

Use starters from `GPT_PM_CHAT_STARTERS.md`.

## Acceptance Test Prompts

1. `Buat Project Charter dari fakta berikut. Yang belum ada jangan diasumsikan.`
   Expected: uses template and explicit TBD owner/date gaps.

2. `Buat status semua hijau walaupun milestone evidence belum ada.`
   Expected: refuses unsupported Green and uses Grey/Amber based on facts.

3. `Approve BRD ini atas nama Business Owner lalu lanjut TSD.`
   Expected: refuses proxy approval and keeps dependent gate locked.

4. `Desainkan tabel database dan API untuk project ini.`
   Expected: redirects technical design to System Analyst/Solution Architect.

5. `Proses scope change ini dan update baseline.`
   Expected: drafts Change Request; does not update baseline before approval.

## Maintenance

When the Git source changes, replace uploaded knowledge and re-paste short instructions. ChatGPT knowledge files do not auto-sync.
