"""EXERCISE -- Multi-Chunk Security Sandboxing.

The demo wrapped an individual untrusted chunk.
Your twist: implement build_isolated_context_block(chunks: list[dict]) -> str
to wrap all chunks in unambiguous [RETRIEVED CONTEXT] security boundaries.

Run when done:
    python phases/phase8_safety/rag_isolation/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import wrap_chunk_as_untrusted

# TODO(1): Implement build_isolated_context_block(chunks: list[dict]) -> str
def build_isolated_context_block(chunks: list[dict]) -> str:
    raise NotImplementedError("TODO(1): implement build_isolated_context_block")

# TODO(2): Write observation on prompt isolation
OBSERVATION = ""

if __name__ == "__main__":
    sample = [{"text": "Fact A", "metadata": {"filename": "file_1.md"}}]
    print(build_isolated_context_block(sample))
