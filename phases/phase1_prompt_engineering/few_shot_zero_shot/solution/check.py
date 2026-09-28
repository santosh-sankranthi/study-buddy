"""Self-check for Phase 1.2 Few-Shot / Zero-Shot."""
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

    exs = getattr(mod, "MY_EXAMPLES", [])
    assert len(exs) >= 2, "TODO(1): MY_EXAMPLES must contain at least 2 fill-in-the-blank examples"
    assert all("input" in e and "output" in e for e in exs), "Each example must have 'input' and 'output'"

    fn = getattr(mod, "generate_fill_in_the_blank", None)
    assert fn is not None, "generate_fill_in_the_blank must be defined"

    out = fn("The Calvin cycle")
    assert isinstance(out, str) and len(out.strip()) > 0, "Output must be a non-empty string"
    assert "_____" in out or "blank" in out.lower() or "answer" in out.lower(), "Expected fill-in-the-blank formatting"

    print(f"✅ Few-shot check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
