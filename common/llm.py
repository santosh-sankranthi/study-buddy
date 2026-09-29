"""Shared LLM client used by every phase.

Everything downstream calls ``chat`` (or ``chat_raw`` for tool-calling) so that
provider selection, retries and fallbacks live in exactly one place.

Two OpenAI-compatible providers are supported:

* **openrouter** — the default for the workshop. ``OPENROUTER_*`` env vars.
* **opencode** — the OpenCode Zen Go gateway. ``OPENCODE_*`` env vars (the API
  key may also come from ``OPENAI_API_KEY``). It additionally requires an
  ``x-opencode-session`` header, which we set automatically.

Pick the primary with ``LLM_PROVIDER=openrouter|opencode``. Whichever provider
you do not pick becomes the fallback, so a provider outage degrades instead of
dying. Free-tier rate limits are handled with retry/backoff per model.
"""

from __future__ import annotations

import os
import random
import time
import uuid
from dataclasses import dataclass, field

from dotenv import load_dotenv
from openai import OpenAI

# The repo root is the parent of this file's folder (common/llm.py -> common/ -> repo).
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)

# Load .env no matter which directory the script is launched from.
load_dotenv(os.path.join(_REPO_ROOT, ".env"))
load_dotenv()  # also honour a .env in the current working directory

# HTTP status codes worth retrying: timeouts, rate limits, server hiccups.
_RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}


@dataclass
class Provider:
    """One OpenAI-compatible endpoint and how to reach it."""

    name: str
    base_url: str
    api_key: str
    default_model: str
    fallback_models: list[str] = field(default_factory=list)
    extra_headers: dict[str, str] = field(default_factory=dict)

    @property
    def configured(self) -> bool:
        return bool(self.api_key)


def _csv_env(name: str) -> list[str]:
    return [m.strip() for m in os.getenv(name, "").split(",") if m.strip()]


def _make_openrouter() -> Provider:
    return Provider(
        name="openrouter",
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.getenv("OPENROUTER_API_KEY", "").strip(),
        default_model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        fallback_models=_csv_env("OPENROUTER_FALLBACK_MODELS") or [
            "qwen/qwen-2.5-72b-instruct:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "openai/gpt-oss-20b:free",
        ],
    )


# A stable per-process session id: the gateway uses it for routing, so it must
# not change between requests.
_OPENCODE_SESSION = os.getenv("OPENCODE_SESSION") or f"study-buddy-{uuid.uuid4().hex[:12]}"


def _make_opencode() -> Provider:
    # The gateway is OpenAI-compatible but demands a routing session header.
    return Provider(
        name="opencode",
        base_url=os.getenv("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1"),
        api_key=(os.getenv("OPENCODE_API_KEY") or os.getenv("OPENAI_API_KEY", "")).strip(),
        default_model=os.getenv("OPENCODE_MODEL", "qwen3.7-plus"),
        fallback_models=_csv_env("OPENCODE_FALLBACK_MODELS") or ["deepseek-v4-flash", "glm-5.3"],
        extra_headers={"x-opencode-session": _OPENCODE_SESSION},
    )


def _all_providers() -> dict[str, Provider]:
    return {"openrouter": _make_openrouter(), "opencode": _make_opencode()}


def _provider_order() -> list[Provider]:
    """Configured providers, primary first. Only providers with a key are used."""
    every = _all_providers()
    preferred = os.getenv("LLM_PROVIDER", "openrouter").strip().lower()
    order = [preferred] + [name for name in every if name != preferred]
    return [every[name] for name in order if name in every and every[name].configured]


def _client_for(provider: Provider) -> OpenAI:
    kwargs: dict = {"base_url": provider.base_url, "api_key": provider.api_key or "missing-key"}
    if provider.extra_headers:
        kwargs["default_headers"] = provider.extra_headers
    return OpenAI(**kwargs)


# ── Backwards-compatible module-level names ──────────────────────────────────

_PRIMARY = (_provider_order() or [_all_providers()["openrouter"]])[0]
BASE_URL = _PRIMARY.base_url
API_KEY = _PRIMARY.api_key
DEFAULT_MODEL = _PRIMARY.default_model
FALLBACK_MODELS = [m for p in _provider_order() for m in ([p.default_model] + p.fallback_models)]


def provider_info() -> dict:
    """Describe the active provider chain (safe to expose; contains no secrets)."""
    order = _provider_order()
    if not order:
        return {"provider": None, "model": None, "fallbacks": []}
    return {
        "provider": order[0].name,
        "model": order[0].default_model,
        "fallbacks": [p.name for p in order[1:]],
    }


def client() -> OpenAI:
    """Client for the primary provider (used for non-chat endpoints like moderation)."""
    order = _provider_order()
    if not order:
        raise RuntimeError(
            "No LLM provider is configured. Set OPENROUTER_API_KEY, or set "
            "LLM_PROVIDER=opencode and provide OPENCODE_API_KEY (or OPENAI_API_KEY)."
        )
    return _client_for(order[0])


# ── Errors / retries ─────────────────────────────────────────────────────────

def _status_code(exc: Exception) -> int | None:
    return getattr(exc, "status_code", None)


def _is_retryable(exc: Exception) -> bool:
    code = _status_code(exc)
    if code in _RETRYABLE_STATUS:
        return True
    text = str(exc).lower()
    return "rate limit" in text or "timeout" in text or "overloaded" in text


def _backoff(attempt: int) -> None:
    """Exponential backoff with jitter: ~1s, 2s, 4s, 8s ... capped at 30s."""
    time.sleep(min(2**attempt, 30) + random.uniform(0, 0.5))


def _candidates(explicit_model: str | None):
    """(provider, model) pairs to try, primary first."""
    order = _provider_order()
    if not order:
        raise RuntimeError(
            "No LLM provider is configured. Copy .env.example to .env and set an "
            "API key, then run scripts/smoke_test.py."
        )
    for i, provider in enumerate(order):
        models: list[str] = []
        if i == 0 and explicit_model:
            models.append(explicit_model)
        models += [provider.default_model] + provider.fallback_models
        for model in models:
            yield provider, model


def chat_raw(messages: list[dict], model: str | None = None, max_retries: int = 5, **kwargs):
    """Send a chat request and return the raw assistant *message* object.

    Unlike :func:`chat`, this preserves ``tool_calls`` (and any other fields),
    which is what the agent loop needs.
    """
    last_error: Exception | None = None
    for provider, candidate in _candidates(model):
        for attempt in range(max_retries):
            try:
                response = _client_for(provider).chat.completions.create(
                    model=candidate, messages=messages, **kwargs
                )
                return response.choices[0].message
            except Exception as exc:  # noqa: BLE001 - re-raised after the loop
                last_error = exc
                if _is_retryable(exc) and attempt < max_retries - 1:
                    _backoff(attempt)
                    continue
                break  # this model is not worth retrying; try the next candidate
    raise RuntimeError(f"All providers/models failed. Last error: {last_error}") from last_error


def chat(messages: list[dict], model: str | None = None, max_retries: int = 5, **kwargs) -> str:
    """Send a chat request and return the assistant's text.

    ``messages`` is the usual OpenAI list. Any extra keyword arguments
    (temperature, top_p, response_format, tools, ...) pass straight through.
    """
    message = chat_raw(messages, model=model, max_retries=max_retries, **kwargs)
    return message.content or ""
