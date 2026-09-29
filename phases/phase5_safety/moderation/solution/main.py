"""SOLUTION -- Output Moderation.

Reference answer: moderate() flags the text, we turn that into a status.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import moderate

SAFE_ANSWER = "Photosynthesis occurs in chloroplasts."


def moderate_assistant_output(answer: str) -> dict:
    """Return {"flagged": bool, "status": "APPROVED" | "BLOCKED"}."""
    flagged = moderate(answer).get("flagged", False)
    return {"flagged": flagged, "status": "BLOCKED" if flagged else "APPROVED"}


if __name__ == "__main__":
    print(moderate_assistant_output(SAFE_ANSWER))
