"""Self-check for the Multi-Agent exercise.

    python .../multi_agent/solution/check.py             # checks your exercise
    python .../multi_agent/solution/check.py --solution  # checks the reference
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

    approved, reason = module.critic("Step 1", "Biology exam is scheduled for 2026-11-15.")
    assert approved is True, f"a useful result should be approved, got: {reason}"

    rejected, reason = module.critic("Step 1", "")
    assert rejected is False, "an empty result should be rejected"

    rejected, reason = module.critic("Step 1", "Error: could not find the date")
    assert rejected is False, "a result containing an error should be rejected"

    print("OK - critic approves good results and rejects weak ones")


if __name__ == "__main__":
    main()
