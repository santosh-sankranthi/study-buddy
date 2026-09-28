"""SOLUTION -- Multi-Chunk Security Sandboxing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import wrap_chunk_as_untrusted

def build_isolated_context_block(chunks: list[dict]) -> str:
    blocks = [
        wrap_chunk_as_untrusted(
            i + 1,
            c["text"],
            c.get("metadata", {}).get("filename", "unknown"),
        )
        for i, c in enumerate(chunks)
    ]
    return "\n\n".join(blocks)

OBSERVATION = "Enclosing retrieved text within syntactic data fences instructs the LLM to treat content as untrusted evidence rather than instructions."

if __name__ == "__main__":
    print(build_isolated_context_block([{"text": "Fact", "metadata": {"filename": "f.md"}}]))
