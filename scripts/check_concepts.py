#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

MODULE_CONCEPTS = [
    ("Module 01", Path("modules/module_01/CONCEPT.md")),
    ("Module 02", Path("modules/module_02/CONCEPT.md")),
]
PLACEHOLDER = "{{ISULAT_DITO}}"
MIN_CHARS = 30


def extract_answer(line: str) -> str:
    if "**Sagot ko:**" not in line:
        return ""
    answer = line.split("**Sagot ko:**", 1)[1]
    # strip markdown emphasis/underscores/colons
    answer = answer.replace("_", "").replace("*", "").replace(":", "")
    return answer.strip()


def main() -> None:
    errors: list[str] = []
    for label, path in MODULE_CONCEPTS:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if PLACEHOLDER in content:
            errors.append(f"{label}: Palitan lahat ng placeholder na `{PLACEHOLDER}` sa {path}.")
            continue
        lines = [line for line in content.splitlines() if line.startswith("**Sagot ko:**")]
        if not lines:
            errors.append(f"{label}: Walang nakitang linya na nagsisimula sa `**Sagot ko:**` sa {path}.")
            continue
        for idx, line in enumerate(lines, start=1):
            answer = extract_answer(line)
            if len(answer) < MIN_CHARS:
                errors.append(
                    f"{label}: Kulang ang sagot #{idx} (kailangan ≥ {MIN_CHARS} chars). Gamitin ang sariling paliwanag."
                )
    if errors:
        for message in errors:
            print(f"❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
