"""Self-check for Phase 5.3 Retrieval."""
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

    fn = getattr(mod, "evaluate_thresholds", None)
    assert fn is not None, "evaluate_thresholds must be defined"

    counts = fn()
    assert len(counts) == 3, "Must test 3 thresholds"
    assert counts[0.10] >= counts[0.95], "Lower threshold must return at least as many chunks as high threshold"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Retrieval check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
