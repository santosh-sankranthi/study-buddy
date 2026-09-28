"""Self-check for Agent Loops exercise."""
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
    spec = importlib.util.spec_from_file_location("loops_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "detect_repetition", None)
    assert fn is not None, "detect_repetition must be defined"

    calls_same = [
        {"name": "search", "arguments": "q1"},
        {"name": "search", "arguments": "q1"}
    ]
    calls_diff = [
        {"name": "search", "arguments": "q1"},
        {"name": "search", "arguments": "q2"}
    ]

    assert fn(calls_same) is True, "Must return True for identical consecutive calls"
    assert fn(calls_diff) is False, "Must return False for different consecutive calls"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write OBSERVATION"

    print(f"✅ Agent loops check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
