"""Self-check for Phase 9.5 Tracing."""
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

    fn = getattr(mod, "summarize_trace", None)
    assert fn is not None, "summarize_trace must be defined"

    summary = fn()
    assert summary.get("total_duration_ms") > 0, "total_duration_ms must be > 0"
    assert summary.get("total_tokens") > 0, "total_tokens must be > 0"
    assert summary.get("total_cost_usd") > 0.0, "total_cost_usd must be > 0"

    print(f"✅ Tracing check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
