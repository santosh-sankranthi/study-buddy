"""Self-check for the Agent Loops exercise.

    python .../agent_loops/solution/check.py             # checks your exercise
    python .../agent_loops/solution/check.py --solution  # checks the reference
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

    same = [{"name": "search", "arguments": "q1"},
            {"name": "search", "arguments": "q1"}]
    different = [{"name": "search", "arguments": "q1"},
                 {"name": "search", "arguments": "q2"}]
    single = [{"name": "search", "arguments": "q1"}]

    assert module.detect_repetition(same) is True, "identical consecutive calls must repeat"
    assert module.detect_repetition(different) is False, "different args are not a repeat"
    assert module.detect_repetition(single) is False, "one call cannot repeat"

    print("OK - repetition detected for identical calls, not for different ones")


if __name__ == "__main__":
    main()
