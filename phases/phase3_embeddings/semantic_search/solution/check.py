"""Self-check for Phase 3.3 Semantic Search."""
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

    corpus = getattr(mod, "CUSTOM_CORPUS", [])
    assert len(corpus) >= 3, "TODO(1): CUSTOM_CORPUS must contain at least 3 sentences"

    fn = getattr(mod, "rank_custom_corpus", None)
    assert fn is not None, "rank_custom_corpus must be defined"

    ranked = fn("chloroplast")
    assert len(ranked) == len(corpus), "Ranked list must score all corpus items"
    assert ranked[0][1] >= ranked[-1][1], "Ranked list must be sorted descending"

    print(f"✅ Semantic search check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
