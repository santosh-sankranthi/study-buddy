"""Self-check for the Few-Shot / Zero-Shot exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("few_shot_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["few_shot_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert len(module.MY_EXAMPLES) >= 2, "provide at least 2 examples"
    assert all("input" in ex and "output" in ex for ex in module.MY_EXAMPLES)
    messages = module.messages_for("The Calvin cycle")
    assert messages[-1] == {"role": "user", "content": "The Calvin cycle"}
    assert len(messages) == 2 * len(module.MY_EXAMPLES) + 1
    print("OK - few-shot messages end with the topic and alternate with examples")


if __name__ == "__main__":
    main()
