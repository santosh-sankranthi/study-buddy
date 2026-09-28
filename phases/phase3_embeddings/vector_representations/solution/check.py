"""Self-check for Phase 3.1 Vector Representations."""
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

    fn = getattr(mod, "verify_invariants", None)
    assert fn is not None, "verify_invariants must be defined"

    inv = fn()
    assert inv["identity"] == 1.0, f"Expected identity == 1.0, got {inv['identity']}"
    assert inv["orthogonal"] == 0.0, f"Expected orthogonal == 0.0, got {inv['orthogonal']}"
    assert inv["opposite"] == -1.0, f"Expected opposite == -1.0, got {inv['opposite']}"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Vector representations check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
