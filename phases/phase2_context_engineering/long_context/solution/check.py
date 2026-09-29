"""Self-check for the Long Context exercise.

    python .../long_context/solution/check.py             # checks your exercise
    python .../long_context/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("longcontext_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["longcontext_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert abs(module.calculate_cost(1_000_000, 1.50) - 1.50) < 1e-9
    assert abs(module.calculate_cost(500_000) - 0.25) < 1e-9
    assert abs(module.calculate_cost(0) - 0.0) < 1e-9

    print("OK - 1M tokens at $1.50 costs $1.50; 500k costs $0.25")


if __name__ == "__main__":
    main()
