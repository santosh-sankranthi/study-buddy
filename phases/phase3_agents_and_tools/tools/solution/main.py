"""SOLUTION -- Tools: register a real function.

The repo's real implementation lives in app/tools.py; here we show it wired
into a TOOL_REGISTRY the same way an agent dispatcher looks tools up by name.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOL_REGISTRY, calculate_grade

SCORES = [80.0, 90.0, 70.0]
WEIGHTS = [0.3, 0.4, 0.3]


if __name__ == "__main__":
    print(calculate_grade(SCORES, WEIGHTS))
    print("Registered tools:", list(TOOL_REGISTRY))
