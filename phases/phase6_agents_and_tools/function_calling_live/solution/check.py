"""Self-check -- Function Calling Live exercise.

Run:
    python phases/phase6_agents_and_tools/function_calling_live/solution/check.py
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

print("Checking function calling live exercise ...\n")

# Verify calculate_grade tool call
grade_res = ex.run_calculate_grade_call([80.0, 90.0, 100.0], [0.2, 0.3, 0.5])
assert "93.00%" in grade_res, f"Expected 93.00% weighted average, got: {grade_res}"
print("✅  execute_tool_call correctly calculated weighted grade: 93.00%")

# Verify malformed argument handling
err_res = ex.test_malformed_arguments()
assert "Error: could not parse arguments" in err_res
print("✅  execute_tool_call gracefully intercepted malformed JSON arguments")

print("\n✅  All checks passed!")
