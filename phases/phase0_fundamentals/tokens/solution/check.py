"""Self-check for the Tokens exercise.

Run the reference solution:   python .../tokens/solution/check.py --solution
Check YOUR exercise skeleton: python .../tokens/solution/check.py

Checks are behavioral: they assert that a token count is a sane positive integer
and that the two encodings are both exercised -- never that it equals an exact
number, since that depends on which paragraph the student chose.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS_DIR = HERE.parent


def load(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--solution",
        action="store_true",
        help="check the reference solution instead of the exercise skeleton",
    )
    args = parser.parse_args()

    target = (TOKENS_DIR / "solution" / "main.py") if args.solution else (TOKENS_DIR / "exercise" / "main.py")
    label = "solution" if args.solution else "exercise"
    print(f"checking {label}: {target}")

    module = load(target, "tokens_under_test")

    # 1. The student's paragraph must actually be theirs and non-trivial.
    if not args.solution:
        assert "TODO" not in module.PARAGRAPH, "TODO(0): replace PARAGRAPH with your own text"
    assert len(module.PARAGRAPH.split()) >= 20, "paragraph should be at least ~20 words"

    # 2. count_tokens must return a positive integer for a known string.
    probe = module.count_tokens("one two three", "cl100k_base")
    assert isinstance(probe, int), "count_tokens must return an int"
    assert probe > 0, "count_tokens must be positive"

    # 3. main() must exercise BOTH encodings and return a mapping.
    counts = module.main()
    assert isinstance(counts, dict), "main() must return a dict of counts"
    for name in ("cl100k_base", "o200k_base"):
        assert name in counts, f"main() must report counts for {name!r}"
        assert isinstance(counts[name], int) and counts[name] > 0, f"{name} count must be a positive int"

    # o200k_base has a larger vocabulary, so it should never need MORE tokens
    # than cl100k_base on ordinary prose (equal is allowed for short strings).
    assert counts["o200k_base"] <= counts["cl100k_base"], (
        "unexpected: o200k_base produced more tokens than cl100k_base"
    )

    # 4. The explanation must be filled in (exercises only).
    if not args.solution:
        assert module.EXPLANATION.strip(), "TODO(3): write your one-sentence explanation"

    print("OK - token counts computed under both encodings:", counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
