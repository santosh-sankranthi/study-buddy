"""Self-check -- Structured Output exercise.

Run:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

spec = importlib.util.spec_from_file_location(
    "ex", Path(__file__).resolve().parents[1] / "exercise" / "main.py"
)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

print("Checking structured output exercise ...\n")

from app.schemas import StudyPlanDay

# Test parse_and_validate_plan
test_json = '[{"subject": "Biology", "topics": ["Cells", "Mitosis"], "minutes": 45}]'
parsed = ex.parse_and_validate_plan(test_json)
assert len(parsed) == 1, "Expected 1 item in parsed list"
assert isinstance(parsed[0], StudyPlanDay), "Item must be an instance of StudyPlanDay"
assert parsed[0].minutes == 45
print("✅  parse_and_validate_plan correctly validates valid input")

# Test validation rejection
caught = ex.verify_catches_invalid()
assert caught is True, "verify_catches_invalid() should return True when bad item is rejected"
print("✅  verify_catches_invalid() properly caught negative minutes")

print("\n✅  All checks passed!")
