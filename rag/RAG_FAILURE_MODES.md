# RAG Failure Modes

| Failure | Expected behavior |
|---|---|
| RAG API unavailable | role agent states retrieval unavailable and asks whether to proceed with assumptions |
| corpus forbidden | role agent does not bypass role policy; route to approval if needed |
| citation missing | retrieval result is unusable for evidence-backed answer |
| low confidence | abstain or ask for more source material |
| stale index | include freshness warning and prefer source-path verification |
| artifact metadata forbidden | do not infer artifact contents |
| conflicting evidence | present conflict with citations and ask human/TL if decision-impacting |

## Agent behavior rule

A role agent may summarize retrieved evidence, but it must not claim a fact is source-backed unless the RAG result includes usable citation metadata.
