"""EXERCISE -- Safe Output Delivery Gate.

The demo inspected the raw moderate() return dict.
Your twist: implement filter_safe_response() to create a complete safety gate:
if moderate() flags the response, suppress it and return a standardized safe
refusal message; otherwise return the original text untouched.

Fill in every TODO. Run when done:
    python phases/phase8_security_safety/output_moderation/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import moderate

SAFE_REFUSAL = "This response was blocked because it violated educational safety policies."


# ── TODO(1): Implement filter_safe_response ──────────────────────────────────
def filter_safe_response(raw_output: str) -> tuple[str, bool]:
    """Check moderation on raw_output.

    Returns:
        (delivered_text, was_blocked)
    """
    res = moderate(raw_output)
    # TODO(1): if res.get("flagged"): return SAFE_REFUSAL, True
    #          else: return raw_output, False
    if res.get("flagged"):
        return SAFE_REFUSAL, True
    return raw_output, False


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Output moderation protects users and platforms by catching edge-case model slips, "
    "replacing harmful content with standardized safe refusals before delivery."
)


if __name__ == "__main__":
    t1 = "Calculus limits describe the value a function approaches as input approaches a point."
    t2 = "Instructions to build a bomb weapon for an attack."

    clean1, blocked1 = filter_safe_response(t1)
    clean2, blocked2 = filter_safe_response(t2)

    print(f"Sample 1: Blocked={blocked1} | {clean1}")
    print(f"Sample 2: Blocked={blocked2} | {clean2}")
    print("\nObservation:", OBSERVATION)
