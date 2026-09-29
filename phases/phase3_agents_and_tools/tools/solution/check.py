"""Self-check for the Tools exercise.

    python .../tools/solution/check.py             # checks your exercise
    python .../tools/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mod_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    result = module.calculate_grade([80.0, 90.0, 70.0], [0.3, 0.4, 0.3])
    assert isinstance(result, str), "calculate_grade should return a string"
    assert "81.00" in result, f"expected a weighted average of 81.00, got: {result}"

    assert "calculate_grade" in module.TOOL_REGISTRY, "calculate_grade must be registered"
    assert module.TOOL_REGISTRY["calculate_grade"] is module.calculate_grade

    print(f"OK - calculate_grade registered and returned {result}")


if __name__ == "__main__":
    main()
