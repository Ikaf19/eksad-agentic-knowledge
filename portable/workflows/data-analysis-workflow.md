# Data Analysis Workflow

Runtime-neutral workflow for Data Analyst work. Use it for KPI definitions, dashboard requirements, profiling notes, and decision-ready analytical reports.

## Stages

1. **Question framing** — restate the business question, decision to support, audience, timeframe, and grain of analysis.
2. **Source inventory** — list available tables/files/reports, ownership, freshness, sensitivity, and known quality gaps.
3. **Metric contract** — define numerator, denominator, filters, time window, grouping dimensions, exclusions, and owner.
4. **Evidence plan** — choose read-only queries or provided files. Mark unavailable data as `[DATA GAP]` with owner and impact.
5. **Analysis** — produce profiling, trend, segmentation, variance, and root-cause hypotheses with caveats.
6. **Recommendation** — separate observed facts, interpretations, recommended decisions, and required follow-up.
7. **Handoff** — create dashboard/report spec or BA/SA/PM handoff notes as needed.

## Output standards

- Cite every data source or RAG document used.
- Never claim causality from correlation without experiment/design evidence.
- Quantify uncertainty and data quality limitations.
- Use business-readable tables before technical query details.

## Stop conditions

Stop and ask when the requested analysis requires production data mutation, unrestricted sensitive data extraction, unknown metric ownership, or an ambiguous decision target.
