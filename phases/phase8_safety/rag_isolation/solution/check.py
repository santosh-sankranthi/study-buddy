"""Self-check for Phase 8 RAG Isolation."""
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

    fn = getattr(mod, "build_isolated_context_block", None)
    assert fn is not None, "build_isolated_context_block must be defined"

    sample = [{"text": "Fact text", "metadata": {"filename": "note.md"}}]
    res = fn(sample)
    assert "UNTRUSTED" in res or "RETRIEVED CONTEXT" in res, "Must contain untrusted context boundary tags"
    assert "note.md" in res, "Must include source filename"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ RAG isolation check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
