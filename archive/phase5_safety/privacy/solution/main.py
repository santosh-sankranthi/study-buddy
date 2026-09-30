"""SOLUTION -- PII Scrubbing.

Reference answer: app.security.scrub_pii already redacts IN and UK phone numbers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import scrub_pii

TEXT = "Contact me at +91 9876543210 or +44 7911123456"


def scrub_international_phone(text: str) -> tuple[str, list[str]]:
    """Return (text with phones redacted, list of PII types detected)."""
    return scrub_pii(text)


if __name__ == "__main__":
    print(scrub_international_phone(TEXT))
