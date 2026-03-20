#!/usr/bin/env python3
"""Teacher helper: generate LLM feedback per module and save it as FEEDBACK.md."""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from ai_client import call_openai

ROOT = Path(__file__).resolve().parents[1]
MODULE_TEMPLATE = "modules/module_{module}/CONCEPT.md"
OUTPUT_TEMPLATE = "modules/module_{module}/FEEDBACK.md"


def extract_answers(content: str) -> List[str]:
    answers: List[str] = []
    for line in content.splitlines():
        if "**Sagot ko:**" not in line:
            continue
        answer = line.split("**Sagot ko:**", 1)[1].strip()
        answer = answer.replace("_", "")
        answers.append(answer)
    return answers


def generate_feedback(module_label: str, answers: List[str]) -> str:
    if not answers:
        raise ValueError("Walang sagot na nahanap sa CONCEPT.md")
    prompt = "\n\n".join(f"Q{idx+1}: {text}" for idx, text in enumerate(answers))
    messages = [
        {
            "role": "system",
            "content": (
                "You review Programming para sa Lahat reflections. "
                "Reply in Taglish with three short bullet points: Clarity, Personal example, Next step."),
        },
        {
            "role": "user",
            "content": (
                f"Module {module_label} reflections (Taglish):\n{prompt}\n"
                "Summarize in ≤120 words."),
        },
    ]
    summary, error = call_openai(messages, max_tokens=160, temperature=0.2)
    if error:
        raise RuntimeError(error)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"# Module {module_label} Feedback\n\n_Generated {timestamp}_\n\n{summary}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate teacher feedback for a module.")
    parser.add_argument("module", help="Module number (e.g., 01, 02)")
    parser.add_argument(
        "--output",
        help="Optional output path (defaults to modules/module_XX/FEEDBACK.md)",
    )
    args = parser.parse_args()
    module = args.module.zfill(2)
    concept_path = ROOT / MODULE_TEMPLATE.format(module=module)
    if not concept_path.exists():
        raise FileNotFoundError(f"Missing concept file: {concept_path}")
    content = concept_path.read_text(encoding="utf-8")
    answers = extract_answers(content)
    feedback = generate_feedback(f"M{module}", answers)
    output_path = Path(args.output) if args.output else ROOT / OUTPUT_TEMPLATE.format(module=module)
    output_path.write_text(feedback, encoding="utf-8")
    relative = output_path.relative_to(ROOT)
    print(f"Saved feedback to {relative}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")
    main()
