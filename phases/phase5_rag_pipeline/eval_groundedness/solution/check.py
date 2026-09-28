"""Self-check for Phase 5.5 Groundedness Eval."""
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

    fn = getattr(mod, "evaluate_rag_test_suite", None)
    assert fn is not None, "evaluate_rag_test_suite must be defined"

    results = fn()
    assert results.get("good_answer_passed") is True, "Good answer must pass"
    assert results.get("bad_answer_failed") is True, "Uncited answer must fail"

    print(f"✅ RAG groundedness eval check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
