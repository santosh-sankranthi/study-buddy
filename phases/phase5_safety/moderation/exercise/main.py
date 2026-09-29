"""EXERCISE -- Output Moderation.

Practice: screen an assistant answer before showing it.
Task: finish moderate_assistant_output() so unsafe answers are BLOCKED.
Check your work with: python phases/phase5_safety/moderation/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import moderate

SAFE_ANSWER = "Photosynthesis occurs in chloroplasts."


def moderate_assistant_output(answer: str) -> dict:
    """Return {"flagged": bool, "status": "APPROVED" | "BLOCKED"}."""
    # TODO: call moderate(answer), then map flagged to the status string.
    raise NotImplementedError("moderate_assistant_output")
