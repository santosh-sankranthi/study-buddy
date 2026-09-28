"""Self-check for Phase 8.1 Prompt Injection."""
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

    fn = getattr(mod, "scan_batch_for_injections", None)
    assert fn is not None, "scan_batch_for_injections must be defined"

    res = fn()
    assert len(res) >= 4, "Must scan all test matrix items"
    assert all("flagged" in r and "expected" in r for r in res), "Results must include flagged and expected"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Prompt injection check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
