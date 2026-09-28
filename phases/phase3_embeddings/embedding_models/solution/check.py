"""Self-check for Phase 3.2 Embedding Models."""
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

    fn = getattr(mod, "get_sentence_embeddings", None)
    assert fn is not None, "get_sentence_embeddings must be defined"

    vecs = fn()
    assert isinstance(vecs, list) and len(vecs) >= 2, "Must return at least 2 embedding vectors"
    assert len(vecs[0]) > 0, "Embedding vector must not be empty"

    print(f"✅ Embedding models check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
