"""Self-check for Phase 1.3 CoT."""
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

    r_no = getattr(mod, "results_no_cot", [])
    r_cot = getattr(mod, "results_cot", [])
    assert len(r_no) == 3, "TODO(1): results_no_cot must have 3 entries"
    assert len(r_cot) == 3, "TODO(2): results_cot must have 3 entries"

    obs = getattr(mod, "OBSERVATION", "")
    assert isinstance(obs, str) and len(obs.strip()) > 20, "TODO(3): OBSERVATION must be > 20 characters"

    print(f"✅ CoT check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
