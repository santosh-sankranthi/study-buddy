"""Self-check for Phase 1.1 System Prompts."""
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

    prompt = getattr(mod, "FLASHCARD_SYSTEM_PROMPT", "")
    assert isinstance(prompt, str) and len(prompt.strip()) > 20, "TODO(1): Define FLASHCARD_SYSTEM_PROMPT"

    fn = getattr(mod, "generate_flashcard", None)
    assert fn is not None, "generate_flashcard must be defined"

    card = fn("Photosynthesis")
    assert isinstance(card, dict), "Result must be a dict"
    assert "front" in card and "back" in card, "Dict must have 'front' and 'back' keys"

    print(f"✅ System prompts check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
