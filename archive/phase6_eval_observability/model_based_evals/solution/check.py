"""Self-check for the LLM-as-a-Judge exercise.

    .../model_based_evals/solution/check.py             # checks your exercise
    .../model_based_evals/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("judge_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["judge_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()
    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    assert module.parse_score("Score: 4") == 4
    assert module.parse_score("no number here") == 0
    verdict = module.evaluate_tone("Great effort! What do you think chlorophyll does?")
    assert 1 <= verdict["score"] <= 5, "judge score should be between 1 and 5"
    assert isinstance(verdict["reason"], str)
    print("OK - judge scored the answer with the model")


if __name__ == "__main__":
    main()
