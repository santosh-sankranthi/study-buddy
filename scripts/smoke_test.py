"""Section 1 smoke test: prove OpenRouter works before building anything else.

Run:  python scripts/smoke_test.py

If this prints a reply, your key and model config are good. If it fails, nothing
downstream will work -- fix this first.
"""

import sys
from pathlib import Path

# Make `common` importable when this script is run from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.llm import DEFAULT_MODEL, chat  # noqa: E402

def main():
    response = chat(
        [{"role": "user", "content": "Reply with exactly the word: pong"}],
        temperature=0,
    )
    print(f"model : {DEFAULT_MODEL}")
    print(f"reply : {response.strip()}")
    print("OK - OpenRouter is reachable and the key is valid.")


if __name__ == "__main__":
    main()

