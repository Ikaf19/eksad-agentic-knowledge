# Data Science Workflow

Runtime-neutral workflow for statistical, predictive, optimization, and ML/AI experiment work.

## Stages

1. **Problem framing** — decide whether the task is descriptive analytics, prediction, classification, forecasting, clustering, optimization, or generative AI evaluation.
2. **Success metric design** — define business metric, model metric, baseline, acceptance threshold, and failure cost.
3. **Data requirement spec** — list candidate datasets, label source, feature windows, leakage risks, privacy constraints, and refresh cadence.
4. **Experiment plan** — choose baseline, split strategy, validation method, evaluation metrics, and reproducibility rules.
5. **Analysis/modeling** — summarize model candidates, assumptions, feature hypotheses, ablation plan, and error analysis.
6. **Risk review** — document bias, drift, explainability, privacy, security, and operational risks.
7. **Handoff** — produce model/experiment report and escalation notes for TL, DevOps/MLOps, AppSec, or business owner.

## Output standards

- Separate experiment design from production deployment.
- Include baseline comparison and negative results.
- State data limitations and leakage risks explicitly.
- Do not recommend deployment without evaluation evidence and approval gates.

## Stop conditions

Stop and escalate when the task requires production deployment, sensitive data use without approval, automated decisioning with legal/compliance implications, or unbounded customer data extraction.
