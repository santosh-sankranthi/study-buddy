"""Self-check for Phase 2.1 Context Sources."""
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

    fn = getattr(mod, "build_personalized_system_prompt", None)
    assert fn is not None, "build_personalized_system_prompt must be defined"

    prompt = fn("Charlie", "Master Calculus", "Monday, Oct 1")
    assert "Charlie" in prompt, "Prompt must include student name"
    assert "Master Calculus" in prompt, "Prompt must include goal"
    assert "Monday, Oct 1" in prompt, "Prompt must include date"

    print(f"✅ Context sources check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
