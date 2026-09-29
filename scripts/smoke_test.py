"""Section 1 smoke test: prove the LLM provider works before anything else.

Run:  python scripts/smoke_test.py

If this prints a reply, your provider, key and model config are good. If it
fails, nothing downstream will work -- fix this first.

Works with either provider (see LLM_PROVIDER in .env).
"""

import sys
from pathlib import Path

# Make `common` importable when this script is run from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.llm import chat, provider_info  # noqa: E402


def main():
    info = provider_info()
    if not info.get("provider"):
        print("No provider configured. Copy .env.example to .env and set a key.")
        sys.exit(1)

    print(f"provider  : {info['provider']}")
    print(f"model     : {info['model']}")
    print(f"fallbacks : {', '.join(info['fallbacks']) or '(none)'}")

    response = chat(
        [{"role": "user", "content": "Reply with exactly the word: pong"}],
        temperature=0,
    )
    print(f"reply     : {response.strip()}")
    print("OK - the provider is reachable and the key is valid.")


if __name__ == "__main__":
    main()
