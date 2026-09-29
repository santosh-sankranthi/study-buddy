"""EXERCISE -- PII Scrubbing.

Practice: redact phone numbers from a message.
Task: finish scrub_international_phone() so it returns the clean text and the PII types found.
Check your work with: python phases/phase5_safety/privacy/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import scrub_pii

TEXT = "Contact me at +91 9876543210 or +44 7911123456"


def scrub_international_phone(text: str) -> tuple[str, list[str]]:
    """Return (text with phones redacted, list of PII types detected)."""
    # TODO: call scrub_pii(text) and return its (clean_text, detected) pair.
    raise NotImplementedError("scrub_international_phone")
