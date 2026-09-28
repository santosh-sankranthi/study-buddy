"""Self-check for the Context Windows exercise.

Run the reference solution:   python .../context_window/solution/check.py --solution
Check YOUR exercise skeleton: python .../context_window/solution/check.py

Behavioral checks: the fixed-token total must match an independent recount, and
the word budget must be consistent with the arithmetic the student was asked to
do. No exact-magic numbers.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT_DIR = HERE.parent


def load(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = (CONCEPT_DIR / "solution" / "main.py") if args.solution else (CONCEPT_DIR / "exercise" / "main.py")
    print(f"checking {'solution' if args.solution else 'exercise'}: {target}")
    module = load(target, "context_window_under_test")

    # Independent recount of the fixed overhead.
    expected = module.count_tokens(module.SYSTEM_PROMPT)
    for user_message, assistant_reply in module.HISTORY:
        expected += module.count_tokens(user_message)
        expected += module.count_tokens(assistant_reply)

    got = module.tokens_used_so_far()
    assert isinstance(got, int), "tokens_used_so_far() must return an int"
    assert got == expected, f"tokens_used_so_far() = {got}, expected {expected}"

    # The word budget must equal the (floored) arithmetic on the leftover tokens.
    left = module.CONTEXT_BUDGET - module.REPLY_RESERVE_TOKENS - expected
    expected_words = max(0, int(left * module.WORDS_PER_TOKEN))
    words = module.note_budget_words()
    assert isinstance(words, int), "note_budget_words() must return an int"
    assert words >= 0, "note_budget_words() must not be negative"
    assert words == expected_words, f"note_budget_words() = {words}, expected {expected_words}"

    print(f"OK - fixed={got} tokens, {words} words of notes fit (left={left} tokens)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
