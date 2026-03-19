"""Helpers for Module 06 (sales logs + state persistence)."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping


def save_sales(rows: Iterable[Mapping[str, object]], path: Path) -> Path:
    """Write a CSV file containing the provided sales rows and return its path."""
    raise NotImplementedError


def load_state(path: Path) -> dict:
    """Load the JSON state file (inventory, cash, etc.) and return it as a dict."""
    raise NotImplementedError
