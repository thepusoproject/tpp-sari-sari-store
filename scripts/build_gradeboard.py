#!/usr/bin/env python3
"""Fetch student grade JSON files and build a consolidated gradeboard."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER_PATH = ROOT / "gradeboard" / "roster.json"
OUTPUT_JSON = ROOT / "docs" / "grades.json"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def load_roster() -> list[dict]:
    if not ROSTER_PATH.exists():
        raise FileNotFoundError(f"Roster file missing: {ROSTER_PATH}")
    with ROSTER_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def fetch_grade(repo: str) -> tuple[dict | None, str]:
    url = f"https://raw.githubusercontent.com/{repo}/main/grades/latest.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            payload = json.load(resp)
            return payload, "ok"
    except urllib.error.HTTPError as err:
        return {"error": f"HTTP {err.code}"}, "error"
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}, "error"


def fetch_profile_name(handle: str | None) -> str | None:
    if not handle:
        return None
    url = f"https://api.github.com/users/{handle}"
    request = urllib.request.Request(url)
    if GITHUB_TOKEN:
        request.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
        request.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(request, timeout=10) as resp:
            data = json.load(resp)
            return data.get("name") or handle
    except Exception:  # noqa: BLE001
        return handle


def build_gradeboard() -> dict:
    roster = load_roster()
    rows = []
    for entry in roster:
        grade_data, status = fetch_grade(entry["repo"])
        display_name = entry.get("displayName") or fetch_profile_name(entry.get("handle"))
        handle = entry.get("handle")
        row = {
            "handle": handle,
            "displayName": display_name or handle,
            "profileUrl": f"https://github.com/{handle}" if handle else None,
            "repo": entry["repo"],
            "status": status,
        }
        if status == "ok" and grade_data:
            row.update(
                module=grade_data.get("module"),
                title=grade_data.get("title"),
                passed=grade_data.get("passed"),
                total=grade_data.get("total"),
                score=grade_data.get("score"),
                updated_at=grade_data.get("updated_at"),
            )
        else:
            row["error"] = grade_data.get("error") if grade_data else "unknown"
        rows.append(row)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "students": rows,
    }


def main() -> None:
    board = build_gradeboard()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(board, fh, indent=2)
    print(f"Wrote {len(board['students'])} rows to {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"gradeboard build failed: {exc}", file=sys.stderr)
        sys.exit(1)
