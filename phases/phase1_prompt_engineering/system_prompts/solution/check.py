"""Self-check for the System Prompts exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("system_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["system_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    prompt = module.FLASHCARD_SYSTEM_PROMPT
    assert isinstance(prompt, str) and len(prompt.strip()) > 20, "write the system prompt"
    assert "json" in prompt.lower(), "the prompt should ask for JSON"
    messages = module.build_messages("Photosynthesis")
    assert [m["role"] for m in messages] == ["system", "user"]
    assert messages[0]["content"] == prompt and messages[1]["content"] == "Photosynthesis"
    print("OK - system prompt is used as the first, system message")


if __name__ == "__main__":
    main()
