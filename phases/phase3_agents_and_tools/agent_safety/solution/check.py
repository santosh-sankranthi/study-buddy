"""Self-check for the Agent Safety exercise.

    python .../agent_safety/solution/check.py             # checks your exercise
    python .../agent_safety/solution/check.py --solution  # checks the reference
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

    halted, reason, steps = module.check_agent_safety(["a", "a"], 5)
    assert halted is True and reason == "loop_detected" and steps == 2

    halted, reason, steps = module.check_agent_safety(["a", "b", "c"], 3)
    assert halted is True and reason == "max_steps" and steps == 3

    halted, reason, steps = module.check_agent_safety(["a", "FINISH"], 5)
    assert halted is False and reason == "done"

    print("OK - loop_detected, max_steps and done guards all behave")


if __name__ == "__main__":
    main()
