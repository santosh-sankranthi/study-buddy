"""Self-check for Phase 5 Indexing."""
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

    fn = getattr(mod, "index_note_file", None)
    assert fn is not None, "index_note_file must be defined"

    sample = "Quantum mechanics governs atomic scales. Uncertainty limits precision."
    ids = fn(sample, "quantum.md", "physics", chunk_size=10, overlap=2)
    assert isinstance(ids, list) and len(ids) >= 1, "Must return list of indexed IDs"

    print(f"✅ Indexing pipeline check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
