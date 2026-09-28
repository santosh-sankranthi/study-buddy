"""Self-check for Phase 3.1 Deterministic Evals."""
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

    fn = getattr(mod, "verify_study_plan_topics", None)
    assert fn is not None, "verify_study_plan_topics must be defined"

    good = [{"subject": "Physics", "topics": ["Kinematics", "Optics"], "minutes": 90}]
    res = fn(good)
    assert res.get("passed") is True, "Valid plan must pass"

    bad = [{"subject": "Physics", "topics": [""], "minutes": 90}]
    res_bad = fn(bad)
    assert res_bad.get("passed") is False, "Empty topic string must fail"

    print(f"✅ Deterministic evals check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
