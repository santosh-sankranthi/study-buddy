"""EXERCISE -- International PII Redaction & Audit Reporting.

The demo scrubbed domestic US phone numbers and emails.
Your twist: implement audit_pii_content() to scrub international student contacts
(India +91, UK +44) and verify that all identifiers are replaced with typed redaction tags.

Fill in every TODO. Run when done:
    python phases/phase8_security_safety/pii_scrubbing/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import scrub_pii


# ── TODO(1): Implement audit_pii_content ─────────────────────────────────────
def audit_pii_content(text: str) -> tuple[str, list[str]]:
    """Scrub PII from text and return (clean_text, detected_categories)."""
    # TODO(1): return scrub_pii(text)
    return scrub_pii(text)


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Typed redaction tokens (e.g. [EMAIL_REDACTED]) preserve syntactic structure for the LLM "
    "while ensuring zero leakage of student identifiers to external logging or APIs."
)


if __name__ == "__main__":
    sample = (
        "Contact me in London at +44 7911 123456 or in Bangalore at +91 9876543210. "
        "Official email: student@oxford.ac.uk."
    )
    clean, types = audit_pii_content(sample)
    print("Scrubbed:", clean)
    print("Categories:", types)
    print("\nObservation:", OBSERVATION)
