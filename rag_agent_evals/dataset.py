from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_dataset(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"Dataset at {path} must be a JSON list of objects")
    return payload


def load_rubric(path: str | Path) -> Dict[str, Any]:
    import yaml

    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
