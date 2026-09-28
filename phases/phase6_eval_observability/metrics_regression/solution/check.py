"""Self-check for Phase 3.4 Metrics & Regression."""
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

    cases = getattr(mod, "EVAL_CASES", [])
    assert len(cases) >= 5, "TODO(1): EVAL_CASES must have at least 5 test cases"

    fn = getattr(mod, "run_regression_suite", None)
    assert fn is not None, "run_regression_suite must be defined"

    rep = fn(cases)
    assert rep.get("total") >= 5, "Total must be at least 5"
    assert 0.0 <= rep.get("pass_rate", -1.0) <= 1.0, "Pass rate must be between 0 and 1"

    print(f"✅ Regression testing check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
