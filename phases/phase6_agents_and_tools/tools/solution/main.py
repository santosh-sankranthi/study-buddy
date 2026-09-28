"""SOLUTION -- Wire calculate_grade into TOOL_REGISTRY."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOL_REGISTRY, calculate_grade

if __name__ == "__main__":
    scores = [80.0, 90.0, 70.0]
    weights = [0.3, 0.4, 0.3]
    res = calculate_grade(scores, weights)
    print("Solution calculated grade:", res)
    assert "calculate_grade" in TOOL_REGISTRY
