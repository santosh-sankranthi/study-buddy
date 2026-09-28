"""Self-check for Phase 4.1 Indexing."""
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

    fn = getattr(mod, "index_cs_notes", None)
    assert fn is not None, "index_cs_notes must be defined"

    ids = fn()
    assert isinstance(ids, list) and len(ids) >= 2, "Must index at least 2 documents"
    assert all(isinstance(i, str) and len(i) > 0 for i in ids), "Doc IDs must be valid strings"

    print(f"✅ Vector database indexing check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
