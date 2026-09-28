"""Reset workshop runtime state between demo runs.

Git does NOT switch runtime state: the Chroma vector store lives in
``data/chroma/`` (git-ignored) and session memory lives in-process. So a
"clean" checkout can still serve notes indexed during a previous run. Run this
before each demo, then (re)start the server so session memory is empty too.

    python scripts/workshop_reset.py

What it clears:
  * ``data/chroma/``            — all indexed notes / vectors
  * ``data/groundedness_log.jsonl`` — the eval audit log
"""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = REPO_ROOT / "data" / "chroma"
GROUNDEDNESS_LOG = REPO_ROOT / "data" / "groundedness_log.jsonl"


def main() -> None:
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
        print(f"cleared {CHROMA_DIR.relative_to(REPO_ROOT)}/")
    else:
        print("no vector store to clear")

    if GROUNDEDNESS_LOG.exists():
        GROUNDEDNESS_LOG.unlink()
        print(f"cleared {GROUNDEDNESS_LOG.relative_to(REPO_ROOT)}")

    print("\nDone. Now restart uvicorn so in-process session memory is empty too:")
    print("  # Ctrl-C the running server, then:")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
