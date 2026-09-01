#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_agent_evals.dataset import load_dataset


def call_agent(base_url: str, chat_path: str, query: str, provider: str | None = None) -> Dict[str, Any]:
    url = base_url.rstrip("/") + (chat_path if chat_path.startswith("/") else f"/{chat_path}")
    payload: Dict[str, Any] = {"query": query}
    if provider:
        payload["provider"] = provider

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return {
        "answer": data.get("answer", ""),
        "sources": data.get("sources", []),
        "tool_info": data.get("tool_info", ""),
        "guardrail": data.get("guardrail", {"blocked": False}),
    }


def facts_coverage(answer: str, required_facts: List[str]) -> float:
    lowered = answer.lower()
    if not required_facts:
        return 1.0

    matches = 0
    for fact in required_facts:
        normalized = fact.lower().replace("_", " ")
        if normalized in lowered or fact.lower() in lowered:
            matches += 1
    return round(matches / len(required_facts), 2)


def run_eval(base_url: str, chat_path: str, provider: str | None, dataset_path: str | Path, limit: int | None) -> Dict[str, Any]:
    dataset = load_dataset(dataset_path)
    if limit is not None:
        dataset = dataset[:limit]

    items: List[Dict[str, Any]] = []
    for item in dataset:
        answer_payload = call_agent(base_url, chat_path, item["question"], provider=provider)
        answer_text = answer_payload["answer"]
        score = facts_coverage(answer_text, item.get("required_facts", []))
        items.append(
            {
                "id": item["id"],
                "question": item["question"],
                "expected_answer": item.get("expected_answer", ""),
                "answer": answer_text,
                "required_facts": item.get("required_facts", []),
                "facts_coverage": score,
                "passed": score >= 0.75,
                "sources": answer_payload.get("sources", []),
                "guardrail": answer_payload.get("guardrail", {"blocked": False}),
            }
        )

    avg_score = sum(row["facts_coverage"] for row in items) / len(items) if items else 0.0
    return {
        "base_url": base_url,
        "provider": provider,
        "count": len(items),
        "average_facts_coverage": round(avg_score, 2),
        "results": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run evaluation against the retail agent API.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for the agent API")
    parser.add_argument("--chat-path", default="/chat", help="Chat endpoint path")
    parser.add_argument("--provider", default=None, help="Provider name to pass through to the agent")
    parser.add_argument("--dataset", default="data/golden_qa.json", help="Path to the JSON dataset")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for number of eval rows")
    parser.add_argument("--output", default="results.json", help="Path to write JSON results")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_eval(
        base_url=args.base_url,
        chat_path=args.chat_path,
        provider=args.provider,
        dataset_path=Path(args.dataset),
        limit=args.limit,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, ensure_ascii=False, indent=2)

    print(json.dumps({
        "count": results["count"],
        "average_facts_coverage": results["average_facts_coverage"],
        "output": str(output_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
