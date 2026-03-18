#!/usr/bin/env python3
"""Update gradeboard/roster.json from a roster-signup issue body."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ROSTER_PATH = ROOT / "gradeboard" / "roster.json"

def load_roster() -> list[dict]:
    if ROSTER_PATH.exists():
        with ROSTER_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    return []

def save_roster(rows: list[dict]) -> None:
    ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ROSTER_PATH.open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2)

def extract_field(body: str, label: str) -> str | None:
    pattern = rf"-\s*{re.escape(label)}:\s*(.+)"
    match = re.search(pattern, body, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def normalize_repo(repo_value: str) -> str:
    repo_value = repo_value.strip()
    if repo_value.startswith("http://") or repo_value.startswith("https://"):
        parsed = urlparse(repo_value)
        repo_value = parsed.path.strip("/")
    if "/" not in repo_value:
        raise ValueError("Repo must be in owner/name format")
    return repo_value

def main() -> None:
    body = os.environ.get("ISSUE_BODY", "")
    title = os.environ.get("ISSUE_TITLE", "")
    if not body:
        raise SystemExit("ISSUE_BODY env var missing")

    handle = extract_field(body, "GitHub handle")
    if not handle and "Roster signup:" in title:
        handle = title.split(":", 1)[1].strip()
    repo_value = extract_field(body, "Repo")

    if not handle:
        raise SystemExit("Could not find GitHub handle in issue body")
    if not repo_value:
        raise SystemExit("Could not find repo entry in issue body")

    handle = handle.strip()
    repo_value = normalize_repo(repo_value)

    roster = load_roster()
    updated = False
    for entry in roster:
        if entry.get("handle") == handle:
            entry["repo"] = repo_value
            updated = True
            break
    if not updated:
        roster.append({"handle": handle, "repo": repo_value})

    # Keep roster sorted for readability
    roster.sort(key=lambda row: row.get("handle", ""))
    save_roster(roster)
    print(f"Roster updated for handle: {handle}")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"roster automation failed: {exc}", file=sys.stderr)
        sys.exit(1)
