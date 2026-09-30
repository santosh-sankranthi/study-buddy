"""Self-check for the Regression Pass Rate exercise.

    .../metrics_regression/solution/check.py             # checks your exercise
    .../metrics_regression/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("metrics_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["metrics_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()
    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert len(module.EVAL_CASES) >= 5, "EVAL_CASES should hold at least 5 cases"

    cases = [
        {"expected_substr": "yes", "answer": "yes indeed"},
        {"expected_substr": "zzz", "answer": "not found here"},
    ]
    report = module.run_regression_suite(cases)
    assert report["total"] == 2 and report["passed"] == 1
    assert abs(report["pass_rate"] - 0.5) < 1e-9, "pass_rate must be computed"
    print("OK - regression pass rate computed from answers")


if __name__ == "__main__":
    main()
