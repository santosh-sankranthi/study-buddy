"""Self-check for the Deterministic Schema Check exercise.

    .../deterministic_evals/solution/check.py             # checks your exercise
    .../deterministic_evals/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("deterministic_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["deterministic_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()
    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert module.verify_study_plan_topics([{"topics": ["Algebra"]}]) is True
    assert module.verify_study_plan_topics([{"topics": []}]) is False
    assert module.verify_study_plan_topics([{"topics": [" "]}]) is False
    print("OK - deterministic schema check validated")


if __name__ == "__main__":
    main()
