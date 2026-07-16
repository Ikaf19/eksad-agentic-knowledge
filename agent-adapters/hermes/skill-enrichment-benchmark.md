# Skill Enrichment Benchmark — Phase F

This file records external skill-pattern references used for EKSAD Hermes skill enrichment. It is not a vendored copy of external repositories.

## Sources checked

- AwesomeSkill marketplace (`https://awesomeskill.ai/`) — public catalog of agent skills such as browser automation, web design guidelines, content research, React best practices, planning-with-files, and UI/UX design intelligence.
- `affaan-m/ECC` (`https://github.com/affaan-m/ecc`) — MIT-licensed agent harness optimization system with skills for API design, backend/frontend patterns, E2E testing, security review, MLE workflow, eval harness, verification loop, product capability, market research, content engine, and documentation lookup.

## Adaptation rule

Use these sources as benchmark patterns only. EKSAD skills must remain:

- role-boundary aware;
- MCP/RAG optional and fallback-safe;
- citation/evidence oriented;
- approval-gated;
- Git source-of-truth only;
- free of runtime secrets or provider-specific assumptions.

## Mapping highlights

| EKSAD role | Benchmark patterns adapted |
|---|---|
| General Coordinator | agent-sort, planning-with-files, verification-loop |
| Business Analyst | product-capability, market-research, deep-research, content-research-writer |
| System Analyst | api-design, mcp-server-patterns, documentation-lookup |
| Technical Leader | verification-loop, eval-harness, security-review |
| Developer Backend | backend-patterns, tdd-workflow, api-design |
| Developer Frontend | frontend-patterns, react-best-practices, web-design-guidelines |
| QA Engineer | e2e-testing, verification-loop, browser automation |
| Project Manager | product-capability, prioritization, planning-with-files |
| DevOps Engineer | mcp-server-patterns, security-review, verification-loop |
| Data Analyst | benchmark-methodology, data quality, dashboard evidence |
| Data Scientist | mle-workflow, benchmark-methodology, eval-harness |
| UI/UX Designer | web-design-guidelines, ui-ux-pro-max, visual evidence review |
| Content Creator | article-writing, brand-voice, content-engine, SEO/release-note governance |
