"""Self-check for the Context Windows exercise.

    python .../context_window/solution/check.py             # checks your exercise
    python .../context_window/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("context_window_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["context_window_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    expected = count_tokens(module.SYSTEM_PROMPT)
    for question, answer in module.HISTORY:
        expected += count_tokens(question) + count_tokens(answer)

    used = module.tokens_used_so_far()
    assert used == expected, f"tokens_used_so_far() = {used}, expected {expected}"

    left = module.CONTEXT_BUDGET - module.REPLY_RESERVE_TOKENS - expected
    expected_words = max(0, int(left * module.WORDS_PER_TOKEN))
    words = module.note_budget_words()
    assert words == expected_words, f"note_budget_words() = {words}, expected {expected_words}"

    print(f"OK - fixed={used} tokens, {words} words of notes fit")


if __name__ == "__main__":
    main()
