"""Self-check for Phase 3.5 Multi-Agent."""
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

    fn = getattr(mod, "critic", None)
    assert fn is not None, "critic must be defined"

    ok, _ = fn("Step 1", "Detailed answer about photosynthesis and light absorption.")
    assert ok is True, "Good result should be approved"

    bad, _ = fn("Step 1", "")
    assert bad is False, "Empty result should be rejected"

    print(f"✅ Multi-agent check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
