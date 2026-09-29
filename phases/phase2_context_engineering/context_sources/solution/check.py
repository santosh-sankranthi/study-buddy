"""Self-check for the Context Sources exercise.

    python .../context_sources/solution/check.py             # checks your exercise
    python .../context_sources/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("sources_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sources_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    prompt = module.build_personalized_system_prompt("Charlie", "Master Calculus", "Monday, Oct 1")
    assert prompt.startswith("Today is Monday, Oct 1.")
    assert "Charlie" in prompt and "Master Calculus" in prompt

    default = module.build_personalized_system_prompt("Dana", "Ace Physics")
    assert default.startswith("Today is ") and "Dana" in default

    print("OK - prompt carries date, name and goal (with today as the default date)")


if __name__ == "__main__":
    main()
