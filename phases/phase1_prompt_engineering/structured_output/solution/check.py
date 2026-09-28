"""Self-check for Phase 1.4 Structured Output."""
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

    cls = getattr(mod, "StudyPlanDay", None)
    assert cls is not None, "StudyPlanDay class must be defined"

    fn = getattr(mod, "parse_and_validate_plan", None)
    assert fn is not None, "parse_and_validate_plan function must be defined"

    test_data = [{"subject": "Math", "topics": ["Algebra", "Calculus"], "minutes": 120}]
    validated = fn(test_data)
    assert len(validated) == 1, "Must validate 1 day"
    assert validated[0].subject == "Math"
    assert validated[0].minutes == 120

    print(f"✅ Structured output check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
