"""Security middleware — input sanitization, PII scrubbing, output moderation.

Grows through the phases:
  Phase 2.5 — detect_injection(), sanitize_input()
  Phase 8.1 — extended injection patterns (HTML comment, unicode, code-block)
  Phase 8.2 — scrub_pii() with email, US phone, CC, IN mobile, UK mobile
  Phase 8.4 — moderate()
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Prompt injection, PII & moderation  [Phase 2.5 light / Phase 5 full]
# Defences for untrusted text: strip injected instructions (sanitize_input),
# redact personal data (scrub_pii), and moderate input + output (moderate).
# Wired into: /ask.
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import os
import re

from dotenv import load_dotenv

_HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(_HERE), ".env"))
load_dotenv()


# ── Phase 2.5 + 8.1: Prompt Injection Detection ───────────────────────────────

_INJECTION_PATTERNS: list[str] = [
    # Phase 2.5 — basic text patterns
    r"ignore\s+(previous|all|prior)\s+instructions?",
    r"disregard\s+(your|all|previous)\s+instructions?",
    r"you\s+are\s+now\s+",
    r"new\s+(system|persona|role)\s*:",
    r"forget\s+(what|everything)\s+you\s+(were told|know)",
    # Phase 8.1 — HTML comment injection
    r"<!--.*?(ignore|override|disregard|system\s*:).*?-->",
    # Phase 8.1 — Code-block injection
    r"```.*?ignore\s+previous.*?```",
    # Phase 8.1 — Unicode look-alike heuristic (common substitutions)
    r"ɪɢɴᴏʀᴇ\s+",
]

_INJECTION_RE = re.compile(
    "|".join(_INJECTION_PATTERNS), re.IGNORECASE | re.DOTALL
)


def detect_injection(text: str) -> tuple[bool, str]:
    """Detect obvious prompt injection in *text*.

    Returns:
        (True, "injection_type") if found, (False, "") otherwise.
    """
    m = _INJECTION_RE.search(text)
    if m:
        return True, m.group(0)[:80]
    return False, ""


def sanitize_input(text: str) -> tuple[str, bool]:
    """Replace injection patterns with [BLOCKED] and return (clean_text, was_sanitized)."""
    found = bool(_INJECTION_RE.search(text))
    clean = _INJECTION_RE.sub("[BLOCKED]", text) if found else text
    return clean, found


# ── Phase 8.2: PII Scrubbing ─────────────────────────────────────────────────

_PII_PATTERNS: dict[str, str] = {
    "EMAIL":    r"\b[\w.%+\-]+@[\w.\-]+\.[a-z]{2,}\b",
    "PHONE_IN": r"\+91[\s\-]?\d{10}\b",
    "PHONE_UK": r"\+44[\s\-]?\d{10}\b",
    "PHONE_US": r"\b(\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b",
    "CC":       r"\b(?:\d[ \-]?){15,16}\b",
}

_PII_RES: dict[str, re.Pattern] = {
    k: re.compile(v, re.IGNORECASE) for k, v in _PII_PATTERNS.items()
}


def scrub_pii(text: str) -> tuple[str, list[str]]:
    """Redact PII from *text*.

    Returns:
        (scrubbed_text, list_of_detected_pii_types)
    """
    detected: list[str] = []
    for pii_type, pattern in _PII_RES.items():
        if pattern.search(text):
            detected.append(pii_type)
            text = pattern.sub(f"[{pii_type}_REDACTED]", text)
    return text, detected


# ── Phase 8.4: Output Moderation ─────────────────────────────────────────────

def moderate(text: str) -> dict:
    """Call the OpenAI/OpenRouter moderation endpoint.

    Returns:
        {"flagged": bool, "categories": {category: bool, ...}}
    """
    from common.llm import client as llm_client  # provider-agnostic

    try:
        client = llm_client()
        result = client.moderations.create(input=text)
        cats   = result.results[0].categories
        flagged_cats = {
            k: v
            for k, v in cats.__dict__.items()
            if v and not k.startswith("_")
        }
        return {"flagged": result.results[0].flagged, "categories": flagged_cats}
    except Exception as exc:  # noqa: BLE001
        # Offline heuristic fallback for local test suites
        t = text.lower()
        is_flagged = any(w in t for w in ["hate", "violence", "threat", "kill", "harm", "weapon", "bomb", "attack", "toxic"])
        return {
            "flagged": is_flagged,
            "categories": {"violence": True} if is_flagged else {},
            "offline_mode": True,
        }


# NOTE: the RAG context-isolation wrapper (wrap_chunk_as_untrusted) lived here
# but was removed with the retrieval stack. It is preserved in archive/rag/.
