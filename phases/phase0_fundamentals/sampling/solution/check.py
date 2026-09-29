"""Self-check for the Sampling exercise.

    python .../sampling/solution/check.py             # checks your exercise
    python .../sampling/solution/check.py --solution  # checks the reference

This one calls the live model, so pytest skips it unless you pass
``--run-llm-checks``; run it directly to try it.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("sampling_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sampling_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert module.build_messages() == [{"role": "user", "content": module.PROMPT}]
    assert module.TEMPERATURE == 1.0, "temperature must stay fixed at 1.0"

    replies = module.sample(0.5, 2)
    assert isinstance(replies, list) and len(replies) == 2, "sample() must return one reply per run"
    assert all(isinstance(r, str) and r.strip() for r in replies), "replies must be non-empty strings"

    print(f"OK - sampled {len(replies)} non-empty replies at top_p=0.5")


if __name__ == "__main__":
    main()
