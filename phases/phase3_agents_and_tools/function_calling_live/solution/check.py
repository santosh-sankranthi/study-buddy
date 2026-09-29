"""Self-check for the Function Calling exercise.

    python .../function_calling_live/solution/check.py             # your exercise
    python .../function_calling_live/solution/check.py --solution  # the reference
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

    result = module.dispatch_grade_tool([80.0, 90.0, 70.0], [0.3, 0.4, 0.3])
    assert isinstance(result, str), "dispatch_grade_tool should return a string"
    assert "81.00" in result, f"the real tool should compute 81.00, got: {result}"
    assert "%" in result, "the tool result should be a percentage"

    print(f"OK - dispatched tool call returned {result}")


if __name__ == "__main__":
    main()
