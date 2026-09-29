"""Self-check for the Tokens exercise.

    python .../tokens/solution/check.py             # checks your exercise
    python .../tokens/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("tokens_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tokens_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    small = module.count_tokens("one two three", "cl100k_base")
    assert small > 0, "count_tokens should return a positive number"

    a = module.count_tokens(module.TEXT, "cl100k_base")
    b = module.count_tokens(module.TEXT, "o200k_base")
    assert a > 0 and b > 0, "both encodings should produce a positive count"

    print(f"OK - cl100k={a} tokens, o200k={b} tokens")


if __name__ == "__main__":
    main()
