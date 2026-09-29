"""Self-check for the Token-Budget Memory exercise.

    python .../memory/solution/check.py             # checks your exercise
    python .../memory/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("memory_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["memory_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    total = module.total_history_tokens(module.SAMPLE_HISTORY)
    assert total > 0, "total tokens must be positive"

    trimmed = module.trim_to_token_budget(module.SAMPLE_HISTORY, 20)
    assert 0 < len(trimmed) < len(module.SAMPLE_HISTORY), "trimming should drop messages"
    assert trimmed[-1] == module.SAMPLE_HISTORY[-1], "the newest message must be kept"
    assert module.total_history_tokens(trimmed) <= 20, "the trim must respect the budget"

    print(f"OK - kept {len(trimmed)} of {len(module.SAMPLE_HISTORY)} messages under 20 tokens")


if __name__ == "__main__":
    main()
