"""Self-check -- Function Calling exercise.

Run:
    python phases/phase1_prompt_engineering/function_calling_concept/solution/check.py
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

print("Checking function calling exercise ...\n")

# Verify calculate_grade schema
schema = ex.get_calculate_grade_schema()
assert schema["type"] == "function"
assert schema["function"]["name"] == "calculate_grade"
print("✅  calculate_grade tool schema exists")

# Verify required fields
req = ex.get_required_fields()
assert "scores" in req and "weights" in req, f"Expected scores and weights in required. Got: {req}"
print("✅  Required fields include scores and weights")

# Verify property types
props = ex.check_property_types()
assert props.get("scores") == "array" and props.get("weights") == "array"
print("✅  Property types are both 'array'")

print("\n✅  All checks passed!")
