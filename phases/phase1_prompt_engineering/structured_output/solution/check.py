"""Self-check for the Structured Output exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("structured_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["structured_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    days = module.parse_and_validate_plan([{"subject": "Math", "topics": ["Algebra"], "minutes": 120}])
    assert len(days) == 1 and days[0].subject == "Math" and days[0].minutes == 120
    try:
        module.parse_and_validate_plan([{"subject": "Math", "minutes": 60}])
    except Exception:
        pass
    else:
        raise AssertionError("a day with no topics should fail validation")
    print("OK - StudyPlanDay validates good rows and rejects bad ones")


if __name__ == "__main__":
    main()
