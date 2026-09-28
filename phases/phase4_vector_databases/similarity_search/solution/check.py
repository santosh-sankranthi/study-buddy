"""Self-check for Phase 4.2 Similarity Search."""
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

    fn_seed = getattr(mod, "seed_chemistry_notes", None)
    fn_search = getattr(mod, "search_chemistry", None)
    assert fn_seed is not None and fn_search is not None, "Functions must be defined"

    fn_seed()
    results = fn_search("acids and protons")
    assert len(results) > 0, "Must return matching chemistry notes"
    assert all(r["metadata"]["subject"] == "chemistry" for r in results), "All returned notes must have subject='chemistry'"

    print(f"✅ Metadata filtering check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
