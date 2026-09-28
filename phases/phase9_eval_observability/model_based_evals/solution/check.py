"""Self-check for Phase 9.2 Model-Based Evals."""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    crit = getattr(mod, "TONE_CRITERIA", "")
    assert isinstance(crit, str) and len(crit.strip()) > 15, "TODO(1): Define TONE_CRITERIA"

    fn = getattr(mod, "evaluate_tone", None)
    assert fn is not None, "evaluate_tone must be defined"

    verdict = fn("Great effort! What role do you think chlorophyll plays in absorbing light?")
    assert 1 <= verdict.get("score", 0) <= 5, "Score must be between 1 and 5"

    print(f"✅ Model-based evals check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
