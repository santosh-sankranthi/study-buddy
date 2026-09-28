"""Self-check for Phase 6.2 Live Function Calling."""
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

    fn = getattr(mod, "dispatch_grade_tool", None)
    assert fn is not None, "dispatch_grade_tool must be defined"

    res = fn([80.0, 90.0, 70.0], [0.3, 0.4, 0.3])
    assert "%" in res or "80" in res or "81" in res, f"Expected grade in result, got: {res}"

    print(f"✅ Function calling live check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
