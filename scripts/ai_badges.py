#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
from statistics import mean
from typing import Dict, List

from ai_client import call_openai

AI_ENABLED = os.getenv("AI_BADGES", "0") == "1"
TARGET_FILES = [Path("main.py")]


def gather_metrics(files: List[Path]) -> Dict[str, float]:
    stats = {
        "function_count": 0,
        "avg_function_length": 0.0,
        "functions_with_docstring": 0,
        "if_statements": 0,
        "input_calls": 0,
    }
    lengths: List[int] = []

    for file in files:
        if not file.exists():
            continue
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stats["function_count"] += 1
                body_len = len(getattr(node, "body", []))
                lengths.append(body_len)
                doc = ast.get_docstring(node)
                if doc:
                    stats["functions_with_docstring"] += 1
            if isinstance(node, ast.If):
                stats["if_statements"] += 1
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":
                stats["input_calls"] += 1
    if lengths:
        stats["avg_function_length"] = mean(lengths)
    return stats


def deterministic_badge(stats: Dict[str, float]) -> str:
    notes = []
    if stats["function_count"] >= 3:
        notes.append("May malinaw na decomposition ng code.")
    if stats["functions_with_docstring"] == 0:
        notes.append("Dagdagan pa ng docstrings para mas guided ang bata.")
    if stats["if_statements"] == 0:
        notes.append("Pwede pang magdagdag ng branching para sa edge cases.")
    if not notes:
        notes.append("Solid ang base structure—ituloy lang ang refactors.")
    return " ".join(notes)


def ai_badge(stats: Dict[str, float]) -> str:
    if not AI_ENABLED:
        return "(AI badge disabled; set AI_BADGES=1)"
    payload = json.dumps(stats)
    reply, error = call_openai(
        [
            {
                "role": "system",
                "content": "Summarize code quality for a beginner Python CLI in ≤30 words (Taglish).",
            },
            {
                "role": "user",
                "content": f"Metrics JSON: {payload}",
            },
        ],
        max_tokens=60,
        temperature=0.2,
    )
    if error:
        return f"(AI badge skipped: {error})"
    return reply


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute adaptive badges for M01–M02 submissions.")
    parser.add_argument("--output", default="badges/latest.json", help="Where to store the metrics + badge text.")
    args = parser.parse_args()

    stats = gather_metrics(TARGET_FILES)
    badge = deterministic_badge(stats)
    ai_text = ai_badge(stats)

    payload = {
        "files": [str(p) for p in TARGET_FILES],
        "metrics": stats,
        "deterministic_badge": badge,
        "ai_badge": ai_text,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
