"""Self-check for Phase 2.4 Long Context."""
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

    fn = getattr(mod, "calculate_cost", None)
    assert fn is not None, "calculate_cost must be defined"

    cost = fn(1_000_000, 1.50)
    assert abs(cost - 1.50) < 0.001, f"Expected 1.50, got {cost}"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Long context check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
