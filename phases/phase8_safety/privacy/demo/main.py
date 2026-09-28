"""DEMO -- Personally Identifiable Information (PII) Scrubbing.

Live-code target: sanitize raw inputs with app.security.scrub_pii(),
demonstrating redaction of emails, US phone numbers, and payment cards.

Run:
    python phases/phase8_security_safety/pii_scrubbing/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import scrub_pii

SAMPLE_TEXT = (
    "Hi tutor, my name is Alex. You can email me at alex.smith@university.edu "
    "or text my cell at 415-555-2671. My study group card is 4111 2222 3333 4444."
)

print("=" * 60)
print("PII SCRUBBING DEMO")
print("=" * 60)

print("\nOriginal Text:")
print(SAMPLE_TEXT)

scrubbed, detected_types = scrub_pii(SAMPLE_TEXT)

print("\nScrubbed Output:")
print(scrubbed)

print("\nDetected PII Categories:")
for pii in detected_types:
    print(f"  🚨 {pii}")
