"""Self-check for Phase 2.2 Memory."""
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

    fn_tot = getattr(mod, "total_history_tokens", None)
    fn_trim = getattr(mod, "trim_to_token_budget", None)
    assert fn_tot is not None and fn_trim is not None, "Functions must be defined"

    tot = fn_tot(mod.SAMPLE_HISTORY)
    assert tot > 0, "Total tokens must be > 0"

    trimmed = fn_trim(mod.SAMPLE_HISTORY, budget=15)
    assert len(trimmed) < len(mod.SAMPLE_HISTORY), "Trimmed list should be smaller than original"
    assert trimmed[-1]["content"] == mod.SAMPLE_HISTORY[-1]["content"], "Most recent message must be preserved"

    print(f"✅ Memory check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
