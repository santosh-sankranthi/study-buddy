"""Self-check -- Regression Testing exercise.

Run:
    python phases/phase7_production_evals/regression_testing/solution/check.py
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

print("Checking regression testing exercise ...\n")

report = ex.run_regression_benchmark(ex.GOLDEN_SET, min_pass_rate=80.0)

assert report["total"] == len(ex.GOLDEN_SET)
assert report["passed"] == report["total"], f"Expected 100% pass on golden set, got {report['passed']}/{report['total']}"
assert report["failed"] == 0
assert report["pass_rate_pct"] == 100.0
assert report["approved"] is True
print(f"✅  run_regression_benchmark correctly verified golden set: {report['pass_rate_pct']}% pass rate")

# Test failure threshold triggering
failing_cases = [
    {"type": "security", "input": "Benign question", "expected": True},  # will fail
    {"type": "tool", "input": "unknown_tool", "expected": True},         # will fail
]
fail_report = ex.run_regression_benchmark(failing_cases, min_pass_rate=80.0)
assert fail_report["approved"] is False
assert fail_report["pass_rate_pct"] == 0.0
print("✅  Failing benchmark correctly triggered approved=False")

print("\n✅  All checks passed!")
