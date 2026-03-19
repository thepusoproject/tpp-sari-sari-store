#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List

from ai_client import call_openai

MODULE_CONCEPTS = [
    ("Module 01", Path("modules/module_01/CONCEPT.md")),
    ("Module 02", Path("modules/module_02/CONCEPT.md")),
]
PLACEHOLDER = "{{ISULAT_DITO}}"
MIN_CHARS = 30
AI_TRIAGE_ENABLED = os.getenv("AI_CONCEPT_TRIAGE", "0") == "1"


def extract_answer(line: str) -> str:
    if "**Sagot ko:**" not in line:
        return ""
    answer = line.split("**Sagot ko:**", 1)[1]
    answer = answer.replace("_", "").replace("*", "").replace(":", "")
    return answer.strip()


def ai_triage(label: str, answers: List[str]) -> str:
    if not AI_TRIAGE_ENABLED or not answers:
        return ""
    merged = "\n".join(answers)
    summary, error = call_openai(
        [
            {
                "role": "system",
                "content": (
                    "You are a bilingual (English + Filipino) reviewer for Programming para sa Lahat. "
                    "Return ≤40 words: Clarity, Personal example, Next step. Use Taglish."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Module: {label}. Learner reflections (Taglish ok):\n{merged}\n"
                    "Give a short verdict for mentors."
                ),
            },
        ],
        max_tokens=90,
        temperature=0.1,
    )
    if error:
        return f"(AI triage skipped: {error})"
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate concept reflections.")
    parser.add_argument("--ai-report", help="Optional file to store AI triage output.")
    args = parser.parse_args()

    errors: list[str] = []
    ai_notes: list[str] = []

    for label, path in MODULE_CONCEPTS:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        lines = [line for line in content.splitlines() if line.startswith("**Sagot ko:**")]
        placeholder_hits = [idx for idx, line in enumerate(lines, start=1) if PLACEHOLDER in line]
        if placeholder_hits:
            errors.append(
                f"{label}: Palitan lahat ng placeholder na `{PLACEHOLDER}` sa {path} (sagot #{placeholder_hits[0]})."
            )
            continue
        if not lines:
            errors.append(f"{label}: Walang nakitang linya na nagsisimula sa `**Sagot ko:**` sa {path}.")
            continue
        for idx, line in enumerate(lines, start=1):
            answer = extract_answer(line)
            if len(answer) < MIN_CHARS:
                errors.append(
                    f"{label}: Kulang ang sagot #{idx} (kailangan ≥ {MIN_CHARS} chars). Gamitin ang sariling paliwanag."
                )
        answers = [extract_answer(line) for line in lines]
        feedback = ai_triage(label, answers)
        if feedback:
            message = f"🤖 {label} AI triage: {feedback}"
            print(message)
            ai_notes.append(message)

    if errors:
        for message in errors:
            print(f"❌ {message}")
        sys.exit(1)

    if args.ai_report and ai_notes:
        Path(args.ai_report).write_text("\n".join(ai_notes) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
