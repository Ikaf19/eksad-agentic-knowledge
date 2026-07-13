# EKSAD Skill Suite Provenance

**Release:** v31 — 2026-07-11  
**Scope:** `hermes-skills/` workflows and their catalog metadata

Unless a passage explicitly attributes or quotes an external source, wording, role boundaries, gates, paths, templates, examples, and decisions in this suite are **EKSAD-native**. External material was used for discovery and conceptual comparison, not copied as an operational contract. License status below applies to the referenced external repository/site, not automatically to EKSAD-authored content. This repository contains no vendored snapshot or license evidence for the listed external sources, so no external license is asserted as repository-verified.

| External source | Concepts consulted/adapted | License status |
|---|---|---|
| [AwesomeSkill.ai](https://www.awesomeskill.ai/) | Skill discovery and taxonomy ideas | **Needs verification** — discovery site; no repository-wide license asserted |
| [affaan-m/everything-claude-code (ECC)](https://github.com/affaan-m/everything-claude-code) | Concise skill packaging, trigger descriptions, validation/checklist ideas | **Needs verification** — an MIT claim was observed during discovery but is not evidenced by a vendored license or pinned source snapshot in this repository |
| [Anthropic knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Knowledge-work routing and specialist workflow decomposition | **Needs verification** before copying any text or code |
| [OpenAI curated security skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) | Security-review triggers and evidence-oriented review framing | **Needs verification** before copying any text or code |
| [Trail of Bits skills](https://github.com/trailofbits/skills) | Threat modeling, trust-boundary, abuse-path, and evidence concepts | **Needs verification** before copying any text or code |
| [wshobson/agents](https://github.com/wshobson/agents) | Role specialization, routing, and review workflow concepts | **Needs verification** before copying any text or code |
| [GitHub awesome-copilot](https://github.com/github/awesome-copilot) | Instruction/skill catalog discovery and reusable prompt organization | **Needs verification** before copying any text or code |

## Rejected assumptions

The v31 curation explicitly rejected these external or environment-specific assumptions:

- Claude-specific runtime directories such as `.claude/`; canonical EKSAD runtime paths are Hermes paths.
- A fixed local conductor endpoint such as `localhost:9876`; orchestration is file/evidence driven and environment-neutral.
- Mock-first frontend production implementation; EKSAD is real-API-first, with MSW confined to tests.
- Automatic/no-gate continuation as the PM or DevOps default; their profile-local workflows remain strict and fail closed.
- Treating AppSec as a tenth role profile; canonical routing is: any role may raise an AppSec trigger and supply evidence; the System Analyst or Technical Leader coordinates and invokes the shared `eksad-appsec-review` workflow; only the named risk authority accepts residual risk or grants a waiver. AppSec is not a profile.
- Importing external role names, infrastructure, approval authorities, risk thresholds, or toolchain defaults as EKSAD facts.
- Assuming repository/site discovery implies permission to copy; direct reuse requires license verification and explicit attribution.
