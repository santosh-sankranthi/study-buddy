"""Self-check for the Context Compaction exercise.

    python .../context_compaction/solution/check.py             # checks your exercise
    python .../context_compaction/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("compaction_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["compaction_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    long = module.compact_keep_last2(module.CONVERSATION)
    assert len(long) == 3, "should be a summary plus the last two messages"
    assert long[0]["role"] == "system" and "[SUMMARY]" in long[0]["content"]
    assert long[-2:] == module.CONVERSATION[-2:], "last two messages must survive verbatim"

    short = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    assert module.compact_keep_last2(short) == short, "short chats stay unchanged"

    print(f"OK - compressed {len(module.CONVERSATION)} messages down to {len(long)}")


if __name__ == "__main__":
    main()
