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
- optional LLM-as-a-judge evaluation
- CSV/JSON reporting for demos and comparison runs

## Demo positioning

For GitHub demo purposes, the recommended split is:

1. Keep the agent in [multi-cloud-retail-agent](../multi-cloud-retail-agent)
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
├─ .env.example
├─ data/
│  ├─ golden_qa.json
│  └─ rubric.yaml
├─ rag_agent_evals/
│  ├─ __init__.py
│  ├─ dataset.py
│  ├─ judge.py
│  ├─ cli.py
│  └─ report.py
└─ scripts/
   └─ run_eval.py
```

## Quick start

```bash
cd rag-agent-evals
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
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

This repo includes two main layers:

1. Rule-based factual coverage
   - checks whether the required facts appear in the answer
   - gives a quick pass/fail signal for demo runs

2. Optional LLM-as-a-judge
   - uses the rubric stored under data/rubric.yaml
   - scores correctness, groundedness, completeness, helpfulness, and tone
   - outputs a summary report with average scores and pass/fail flags

## Recommended demo flow

### Local demo

```bash
cd ../multi-cloud-retail-agent
uv run uvicorn backend.api.main:app --reload
```

Then from this repo:

```bash
cd ../rag-agent-evals
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

If no judge key is present, the runner falls back to fact-coverage scoring so the demo still works offline.

## Deliverable intent

This is meant to be a clean, reusable evaluation package for GitHub demos: a separate repo that proves the agent is not just a chatbot, but a benchmarked RAG system with observable quality checks.

The app repo shows the experience. The eval repo shows the evidence.
