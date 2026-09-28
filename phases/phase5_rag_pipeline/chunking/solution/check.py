"""Self-check for Phase 5.1 Chunking."""
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

    fn = getattr(mod, "get_paragraph_chunks", None)
    assert fn is not None, "get_paragraph_chunks must be defined"

    chunks = fn()
    assert len(chunks) == 2, f"Expected 2 paragraph chunks, got {len(chunks)}"
    assert "Mitosis" in chunks[0] and "Meiosis" in chunks[1]

    print(f"✅ Chunking check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
