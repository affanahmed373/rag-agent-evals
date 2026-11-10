# Roadmap

Planned improvements. Each item lists the skill it proves and what "done" means.
Add the skill to the CV only after the item is pushed.

## 1. Publish results (priority: high)
Proves: evaluation with real numbers.
- [ ] Run `scripts/run_eval.py` against the retail agent for each provider and retrieval mode.
- [ ] Results table in the README: fact coverage, pass rate, latency, cost per question.
Done when: the README shows a dated results table.

## 2. LLM-as-judge (priority: high)
Proves: LLM-as-judge, rubric scoring.
- [ ] Implement the judge from `data/rubric.yaml` (correctness, groundedness, completeness, helpfulness, tone).
- [ ] Check judge agreement on 15-20 hand-labelled answers and report it.

## 3. RAGAS + promptfoo / DeepEval (priority: medium)
Proves: standard eval tooling, regression testing.
- [ ] RAGAS faithfulness, context precision and context recall using the retrieved contexts from the agent.
- [ ] promptfoo config with the golden set and red-team prompts (prompt injection, PII, off-topic).

## 4. CI eval gate (priority: high)
Proves: CI/CD release gates for LLM apps.
- [ ] GitHub Actions job runs the eval against the mock or a cheap provider on every PR.
- [ ] Fail the job when the pass rate drops below a threshold.
- [ ] CI badge and the latest pass rate at the top of the README. This repo has no app to host; the README table and badge are its demo.
- [ ] Optional: publish the HTML report of each run to GitHub Pages.

## 5. MLflow tracking (priority: medium)
Proves: MLflow experiment tracking.
- [ ] Log each eval run (provider, model, retrieval mode, prompt version) as an MLflow run with metrics and the JSON report as an artefact.
- [ ] Screenshot of the comparison view in the README.

## 6. One harness for both shop agents (priority: high)
Proves: a reusable eval harness, not a one-off script.
- [ ] Take over `backend/eval/` from `multi-cloud-retail-agent` so there is one golden set and one judge.
- [ ] Agent adapters: the clothing agent over HTTP (`/chat`) and `spice-shop-invoice-agent` over its Python API.
- [ ] Spice shop golden set from the synthetic demo bills, with exact expected prices and totals.
- [ ] README results table with one row per agent.
Done when: one command scores both agents and CI runs both.

## 7. Dataset growth (priority: medium)
- [ ] Add Urdu and German questions, multi-turn questions and adversarial questions.
- [ ] Version the dataset (`golden_qa_v2.json`) and note changes in the README.
