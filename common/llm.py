"""Shared OpenRouter client used by every phase.

Everything downstream imports ``chat`` from here so that three things live in
one place instead of being copy-pasted 40 times:

1. **env loading** -- the repo-level ``.env`` is read automatically.
2. **model fallback** -- we ask for a model, and if it is unavailable we walk a
   fallback list instead of dying.
3. **retry / backoff** -- free-tier rate limits are a fact of life (roughly
   20 req/min), so a 429 during a live class must not kill the demo.

We use the official ``openai`` package pointed at OpenRouter's base URL. OpenRouter
speaks the OpenAI wire format verbatim, so nothing here is OpenRouter-specific
except the base URL -- which is exactly why the *app* code never has to look
non-standard.
"""

from __future__ import annotations

import os
import random
import time

from dotenv import load_dotenv
from openai import OpenAI

# The repo root is the parent of this file's folder (common/llm.py -> common/ -> repo).
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)

# Load .env no matter which directory the script is launched from.
load_dotenv(os.path.join(_REPO_ROOT, ".env"))
load_dotenv()  # also honour a .env in the current working directory

BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# Hardcoded fallbacks for when the router (or a specific free model) is down.
# Free model IDs rotate -- re-check https://openrouter.ai/models if these 404.
_DEFAULT_FALLBACKS = [
    "qwen/qwen-2.5-72b-instruct:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "openai/gpt-oss-20b:free",
]
_env_fallbacks = [m.strip() for m in os.getenv("OPENROUTER_FALLBACK_MODELS", "").split(",") if m.strip()]
FALLBACK_MODELS = _env_fallbacks or _DEFAULT_FALLBACKS

# HTTP status codes worth retrying: timeouts, rate limits, server hiccups.
_RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Build the OpenAI client once, on first use.

    Lazy so that simply *importing* this module (e.g. in a test that only checks
    token counting) works even if no API key is configured yet.
    """
    global _client
    if _client is None:
        # An empty key would raise; a placeholder lets the real auth error come
        # back from the server with a helpful message instead.
        _client = OpenAI(base_url=BASE_URL, api_key=API_KEY or "missing-openrouter-key")
    return _client


def _status_code(exc: Exception) -> int | None:
    """Best-effort extraction of an HTTP status from an SDK exception."""
    return getattr(exc, "status_code", None)


def _is_retryable(exc: Exception) -> bool:
    """Rate limit / server / timeout errors are worth sleeping and retrying."""
    code = _status_code(exc)
    if code in _RETRYABLE_STATUS:
        return True
    text = str(exc).lower()
    return "rate limit" in text or "timeout" in text or "overloaded" in text


def _backoff(attempt: int) -> None:
    """Exponential backoff with jitter: ~1s, 2s, 4s, 8s ... capped at 30s."""
    delay = min(2**attempt, 30) + random.uniform(0, 0.5)
    time.sleep(delay)


def chat(
    messages: list[dict],
    model: str | None = None,
    max_retries: int = 5,
    **kwargs,
) -> str:
    """Send a chat request and return the assistant's text.

    ``messages`` is the usual OpenAI list: [{"role": "system"|"user"|"assistant",
    "content": "..."}]. Any extra keyword arguments (temperature, top_p,
    response_format, ...) are passed straight through to the API, which is how
    the demos show those knobs working.

    On a rate limit we sleep and retry the same model. If a model keeps failing
    for a non-retryable reason, we move to the next fallback model. Only if every
    model is exhausted do we raise.
    """
    if not API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Copy .env.example to .env and paste "
            "your key, then run scripts/smoke_test.py."
        )

    models = [model or DEFAULT_MODEL] + [m for m in FALLBACK_MODELS if m != (model or DEFAULT_MODEL)]
    last_error: Exception | None = None

    for current_model in models:
        for attempt in range(max_retries):
            try:
                response = get_client().chat.completions.create(
                    model=current_model, messages=messages, **kwargs
                )
                return response.choices[0].message.content or ""
            except Exception as exc:  # noqa: BLE001 - we re-raise the last one below
                last_error = exc
                if _is_retryable(exc) and attempt < max_retries - 1:
                    _backoff(attempt)
                    continue
                # Not worth retrying this model; try the next fallback.
                break

    raise RuntimeError(f"All models failed. Last error: {last_error}") from last_error
