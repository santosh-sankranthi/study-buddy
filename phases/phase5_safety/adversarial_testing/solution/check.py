"""Self-check for Phase 5.5 Adversarial Testing."""
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
    spec = importlib.util.spec_from_file_location("adv_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "run_redteam_tests", None)
    assert fn is not None, "run_redteam_tests function must be defined"

    results = fn()
    assert isinstance(results, dict), "Must return a dictionary"
    assert len(results) >= 3, "Must run at least 3 redteam tests"
    assert all(results.values()), f"All redteam defenses must pass, got: {results}"

    print(f"✅ Adversarial testing check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
