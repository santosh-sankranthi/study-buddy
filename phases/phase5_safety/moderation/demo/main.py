"""DEMO -- Output Moderation with app.security.moderate().

Live-code target: inspect model responses with moderate(), demonstrating
interception and suppression of policy-violating content.

Run:
    python phases/phase8_security_safety/output_moderation/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import moderate

SAFE_OUTPUT = (
    "Photosynthesis is a vital biological process that sustains plant life "
    "and replenishes oxygen in the atmosphere."
)

UNSAFE_OUTPUT = (
    "Here is an attack plan to kill people with a bomb and weapon."
)

print("=" * 60)
print("OUTPUT MODERATION DEMO")
print("=" * 60)

# 1. Screen safe output
print("\n1. Screening Safe Academic Output:")
res_safe = moderate(SAFE_OUTPUT)
print(f"  Flagged:    {res_safe.get('flagged')}")
print(f"  Categories: {res_safe.get('categories')}")

# 2. Screen unsafe output
print("\n2. Screening Harmful Output:")
res_unsafe = moderate(UNSAFE_OUTPUT)
print(f"  Flagged:    {res_unsafe.get('flagged')} (Expected: True)")
print(f"  Categories: {res_unsafe.get('categories')}")
