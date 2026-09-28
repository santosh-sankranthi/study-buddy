"""Self-check for Phase 6.1 Tools exercise."""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("tools_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "calculate_grade", None)
    assert fn is not None, "calculate_grade function must be defined"

    # Test execution
    res = fn([80.0, 90.0, 70.0], [0.3, 0.4, 0.3])
    assert isinstance(res, str), "Result must be a string"
    assert "80" in res or "81" in res or "%" in res, f"Expected grade in result, got: {res}"

    print(f"✅ Tools check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
