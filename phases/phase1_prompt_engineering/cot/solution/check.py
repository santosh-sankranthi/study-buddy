"""Self-check for the Chain of Thought exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("cot_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["cot_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    prompt = module.cot_prompt(module.PROBLEM)
    assert module.PROBLEM in prompt, "cot_prompt must keep the original problem"
    assert "step by step" in prompt.lower(), "cot_prompt must ask for step-by-step reasoning"
    assert module.extract_answer("reasoning <answer>82.67</answer>") == "82.67"
    assert module.extract_answer("no tags here") == "no tags here"
    print("OK - cot_prompt adds the instruction and extract_answer reads the tag")


if __name__ == "__main__":
    main()
