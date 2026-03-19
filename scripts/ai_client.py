"""Tiny helper to call the OpenAI Chat Completions API with guardrails."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Iterable, Optional

_API_URL = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1/chat/completions")
_DEFAULT_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")


def call_openai(
    messages: Iterable[dict],
    *,
    model: Optional[str] = None,
    max_tokens: int = 120,
    temperature: float = 0.3,
) -> tuple[Optional[str], Optional[str]]:
    """Return (text, error). If API key missing or call fails, error is non-None."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY is not set"

    payload = {
        "model": model or _DEFAULT_MODEL,
        "messages": list(messages),
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        _API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            parsed = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:  # pragma: no cover - network errors are side effects
        try:
            detail = exc.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            detail = exc.reason if hasattr(exc, "reason") else str(exc)
        return None, f"HTTP {exc.code}: {detail}"
    except urllib.error.URLError as exc:  # pragma: no cover
        return None, f"Network error: {exc.reason}"

    choices = parsed.get("choices", [])
    if not choices:
        return None, "No choices returned by OpenAI"
    message = choices[0].get("message", {}).get("content")
    if not message:
        return None, "Empty completion"
    return message.strip(), None
