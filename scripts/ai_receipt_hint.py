#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Optional

from ai_client import call_openai

PATTERN_HINTS = {
    "Receipt header missing": "Mukhang wala pang 'Receipt' header. Lagyan ng malinaw na divider bago ang totals para pumasa sa tests.",
    "Could not find numeric value for 'Price'": "Siguraduhing may linyang `Price: <amount>` (may colon at spacing).",
    "Could not find numeric value for 'Change'": "I-echo ang cash at change na may labels (`Change: 12.50`).",
}

AI_ENABLED = os.getenv("AI_RECEIPT_HINTS", "0") == "1"


def extract_failure(data: dict) -> Optional[dict]:
    for test in data.get("tests", []):
        if test.get("outcome") == "failed":
            return test
    return None


def pattern_hint(message: str) -> Optional[str]:
    for needle, hint in PATTERN_HINTS.items():
        if needle in message:
            return hint
    return None


def ai_hint(crash_message: str) -> str:
    if not AI_ENABLED:
        return "(AI hint disabled; set AI_RECEIPT_HINTS=1)"
    excerpt = crash_message[-500:]
    reply, error = call_openai(
        [
            {
                "role": "system",
                "content": (
                    "You mentor Taglish beginner coders building a CLI receipt printer. "
                    "Respond with ≤40 words, Taglish, friendly tone."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Here is the failing pytest message/output excerpt. Give one actionable hint: "
                    f"\n{excerpt}"
                ),
            },
        ],
        max_tokens=80,
        temperature=0.2,
    )
    if error:
        return f"(AI hint skipped: {error})"
    return reply


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate mentor hints from pytest JSON report.")
    parser.add_argument("report", help="Path to grade_report.json")
    parser.add_argument("--output", help="Optional file to write the hint to.")
    args = parser.parse_args()

    data = json.loads(Path(args.report).read_text(encoding="utf-8"))
    failure = extract_failure(data)
    if not failure:
        print("✅ Walang failing tests. Wala nang hint na kailangan.")
        return

    crash = failure.get("call", {}).get("crash", {})
    message = crash.get("message", "")
    hint = pattern_hint(message)
    if not hint:
        hint = ai_hint(message or json.dumps(crash))

    print(f"🤖 Receipt mentor hint: {hint}")
    if args.output:
        Path(args.output).write_text(hint + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
