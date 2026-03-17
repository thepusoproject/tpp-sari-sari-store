#!/usr/bin/env python3
"""Check all student repos for module PRs that have been idle for too long."""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROSTER_PATH = ROOT / "gradeboard" / "roster.json"
THRESHOLD_HOURS = int(os.getenv("STALE_HOURS", "24"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def api_get(url: str) -> list | dict:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    if GITHUB_TOKEN:
        request.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    with urllib.request.urlopen(request, timeout=10) as resp:
        return json.load(resp)


def load_roster() -> list[dict]:
    with ROSTER_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_stale_prs(repo: str) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=50"
    pulls = api_get(url)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=THRESHOLD_HOURS)
    stale = []
    for pr in pulls:
        if pr.get("base", {}).get("ref") != "main":
            continue
        updated = pr.get("updated_at") or pr.get("created_at")
        if not updated:
            continue
        updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        if updated_dt < cutoff:
            stale.append(
                {
                    "repo": repo,
                    "title": pr.get("title"),
                    "url": pr.get("html_url"),
                    "updated_at": updated,
                }
            )
    return stale


def main() -> None:
    roster = load_roster()
    stale_prs: list[dict] = []
    for entry in roster:
        repo = entry["repo"]
        try:
            stale_prs.extend(find_stale_prs(repo))
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to inspect {repo}: {exc}", file=sys.stderr)
    if stale_prs:
        print("Stale module PRs detected (older than" f" {THRESHOLD_HOURS}h):")
        for pr in stale_prs:
            print(f"- {pr['repo']} :: {pr['title']} ({pr['url']}) — last update {pr['updated_at']}")
        sys.exit(1)
    print("No stale module PRs found.")


if __name__ == "__main__":
    main()
