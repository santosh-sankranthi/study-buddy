"""Self-check for the ReAct Trace exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("react_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["react_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    trace = module.run_full_trace()
    assert len(trace) == 3, "trace should have 3 steps"
    assert set(trace[0]) == {"thought", "action", "observation"}
    assert "81.00" in trace[0]["observation"], "grade step must use the real tool result"
    assert trace[1]["observation"].startswith("Math exam")
    assert trace[2]["action"].startswith("FINISH("), "trace must end with FINISH"
    print("OK - ReAct trace has 3 steps and ends with FINISH")


if __name__ == "__main__":
    main()
