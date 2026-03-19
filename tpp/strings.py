"""Helpers for Module 05 (strings & menu formatting)."""

from __future__ import annotations

from typing import Iterable, Mapping


def sanitize_sku(raw: str) -> str:
    """Normalize an item name into an upper-case SKU."""
    raise NotImplementedError


def format_menu(items: Iterable[Mapping[str, object]]) -> str:
    """Return a multi-line string menu with numbering, price, and SKUs."""
    raise NotImplementedError
