# RAG Agent Evals

This repository is the evaluation layer for the multi-cloud retail agent demo. The live application stays in the main app repo, while this repo focuses on benchmarking, regression testing, and demo-ready scoring.

## Why this repo exists

The main project is the actual retail assistant:

- business logic
- LangGraph orchestration
- policy and product retrieval
- multi-provider LLM integration
- cloud deployment assets

This repo is intentionally separate so the evaluation workflow can be reused as a standalone GitHub demo artifact:

- curated golden Q&A dataset
- rubric-driven scoring
- factual coverage checks
- a rubric for a later judge (correctness, groundedness, completeness, helpfulness, tone)
- JSON reporting from `scripts/run_eval.py`

## Demo positioning

For GitHub demo purposes, the recommended split is:

1. Keep the agent in [multi-cloud-retail-agent](https://github.com/affanahmed373/multi-cloud-retail-agent)
2. Keep evals, scoring, and benchmarking here in this repo
3. Point the eval suite at a local or deployed agent URL

This makes the story clear:

- app repo = product experience
- eval repo = quality assurance and demo evidence

## Repo structure

```text
rag-agent-evals/
├─ README.md
├─ pyproject.toml
├─ requirements.txt
├─ data/
│  ├─ golden_qa.json
│  └─ rubric.yaml
├─ rag_agent_evals/
│  ├─ __init__.py
│  └─ dataset.py
└─ scripts/
   └─ run_eval.py
```

## Quick start

```bash
cd rag-agent-evals
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then point the script at the agent you want to evaluate:

```bash
python3 scripts/run_eval.py \
  --base-url http://localhost:8000 \
  --chat-path /chat \
  --provider mock \
  --limit 10 \
  --output results.json
```

For a cloud deployment:

```bash
python3 scripts/run_eval.py \
  --base-url https://your-app-url \
  --chat-path /chat \
  --provider openai \
  --limit 20 \
  --output cloud_eval_report.json
```

## What is evaluated

The dataset is built around the multi-cloud retail agent's core domains:

- shipping and returns policies
- payment and size guidance
- product inventory and recommendations
- festive / occasion-based shopping guidance

Each item includes:

- id
- question
- expected_answer
- required_facts
- source_type
- source_ids
- difficulty

## Metrics

`scripts/run_eval.py` scores **facts coverage**: it checks whether each item's required facts appear in the agent's answer, marks a row as passed at 0.75 or above, and writes `results.json`. It calls a running agent. This repository has no saved run, so no score is published here.

`data/rubric.yaml` lists correctness, groundedness, completeness, helpfulness, and tone for a later judge. The script does not fill those dimensions.

## Recommended demo flow

### Local demo

```bash
git clone https://github.com/affanahmed373/multi-cloud-retail-agent.git
cd multi-cloud-retail-agent
uv run uvicorn backend.api.main:app --reload
```

Then from this repo:

```bash
python3 scripts/run_eval.py --base-url http://localhost:8000 --provider mock --limit 10
```

### Cloud demo

- deploy the app repo to a cloud endpoint
- run this eval repo against that public URL
- save generated JSON to show before/after performance on a known golden set

## Environment variables

The eval repo reads the following optional settings:

```bash
AGENT_BASE_URL=http://localhost:8000
AGENT_CHAT_PATH=/chat
JUDGE_PROVIDER=openai
OPENAI_API_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
```

`scripts/run_eval.py` scores facts coverage against the agent URL. It does not call a judge, and it does not read these keys.

## Deliverable intent

This is meant to be a clean, reusable evaluation package for GitHub demos: a separate repo that proves the agent is not just a chatbot, but a benchmarked RAG system with observable quality checks.

The app repo shows the experience. The eval repo shows the evidence.
