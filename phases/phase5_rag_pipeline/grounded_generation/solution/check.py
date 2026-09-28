"""Self-check for Phase 5.4 Grounded Generation."""
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

    fn = getattr(mod, "build_rag_prompt_with_sources", None)
    assert fn is not None, "build_rag_prompt_with_sources must be defined"

    test_chunks = [{"text": "Mitosis overview", "metadata": {"filename": "cell_division.md"}}]
    prompt = fn("What is mitosis?", test_chunks)
    assert "[Source: cell_division.md]" in prompt, "Prompt must include [Source: filename] citation tags"
    assert "What is mitosis?" in prompt, "Prompt must include the student question"

    print(f"✅ Grounded generation check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
