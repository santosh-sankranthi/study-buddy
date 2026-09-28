"""Self-check for Phase 3 Agent Safety."""
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

    fn = getattr(mod, "check_agent_safety", None)
    assert fn is not None, "check_agent_safety must be defined"

    halted, reason, steps = fn(["search('bio')", "search('bio')"], 5)
    assert halted is True and reason == "loop_detected", "Consecutive identical calls must trigger loop_detected"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Agent safety check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
