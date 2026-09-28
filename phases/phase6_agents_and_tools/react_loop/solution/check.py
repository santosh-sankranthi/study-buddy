"""Self-check for Phase 6.3 ReAct Loop."""
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

    q = getattr(mod, "TWO_TOOL_QUESTION", "")
    assert isinstance(q, str) and len(q.strip()) > 20, "TODO(1): TWO_TOOL_QUESTION must be a non-empty question"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ ReAct loop check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
