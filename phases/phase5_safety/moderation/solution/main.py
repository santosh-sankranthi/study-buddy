"""SOLUTION -- Output Content Moderation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import moderate

def moderate_assistant_output(answer: str) -> dict:
    mod = moderate(answer)
    flagged = mod.get("flagged", False)
    return {
        "flagged": flagged,
        "status": "BLOCKED" if flagged else "APPROVED"
    }

if __name__ == "__main__":
    print(moderate_assistant_output("Photosynthesis occurs in chloroplasts."))
