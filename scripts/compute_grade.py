#!/usr/bin/env python3
"""Compute module grades from the pytest JSON report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

MODULE_ID = "M01"
MODULE_TITLE = "Sukli Calculator"


def load_report(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Pytest JSON report not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def summarize_tests(report: Dict[str, Any]) -> tuple[int, int]:
    tests = report.get("tests", [])
    total = len(tests)
    passed = sum(1 for test in tests if test.get("outcome") == "passed")
    return passed, total


def write_grade_json(passed: int, total: int, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    score = round((passed / total) * 100, 2) if total else 0.0
    payload = {
        "module": MODULE_ID,
        "title": MODULE_TITLE,
        "passed": passed,
        "total": total,
        "score": score,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    with destination.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return payload


def write_gradebook_md(data: Dict[str, Any], destination: Path) -> None:
    destination_text = f"""# Gradebook\n\n| Module | Title | Passed | Total | Score | Updated |\n| ------ | ----- | ------ | ----- | ----- | ------- |\n| {data['module']} | {data['title']} | {data['passed']} | {data['total']} | {data['score']}% | {data['updated_at']} |\n"""
    destination.write_text(destination_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute grades from pytest JSON report.")
    parser.add_argument(
        "report",
        type=Path,
        default=Path("grade_report.json"),
        nargs="?",
        help="Path to pytest JSON report (default: grade_report.json)",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("grades/latest.json"),
        help="Where to write the machine-readable grade file.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("GRADEBOOK.md"),
        help="Where to write the Markdown gradebook.",
    )
    args = parser.parse_args()

    report = load_report(args.report)
    passed, total = summarize_tests(report)
    grade_data = write_grade_json(passed, total, args.json_output)
    write_gradebook_md(grade_data, args.markdown_output)
    print(
        f"Grade computed for {grade_data['module']}: {grade_data['passed']}/{grade_data['total']} "
        f"tests passed ({grade_data['score']}%)."
    )


if __name__ == "__main__":
    main()
