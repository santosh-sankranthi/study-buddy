"""Self-check -- Indexing Pipeline exercise.

Run:
    python phases/phase5_rag_pipeline/indexing/solution/check.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

spec = importlib.util.spec_from_file_location(
    "ex", Path(__file__).resolve().parents[1] / "exercise" / "main.py"
)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

print("Checking indexing pipeline exercise ...\n")

from app.vector_store import count, search

c_start = count()
note_text = (
    "Quantum mechanics is the study of matter and radiation at an atomic and subatomic level. "
    "Wave-particle duality posits that light exhibits behaviors of both waves and particles. "
    "The Heisenberg uncertainty principle states that position and momentum cannot be simultaneously measured with precision."
)
ids = ex.index_note_file(note_text, "quantum.md", "physics", chunk_size=20, overlap=5)

assert len(ids) >= 2, f"Expected at least 2 chunks, got {len(ids)}"
assert count() == c_start + len(ids), "Chroma collection count should match added chunks"
print(f"✅  index_note_file created and indexed {len(ids)} chunks")

# Verify chunk metadata via search
res = search("uncertainty principle", k=1, subject="physics")
assert len(res) > 0
top = res[0]
assert top["metadata"].get("filename") == "quantum.md"
assert top["metadata"].get("subject") == "physics"
assert "chunk_index" in top["metadata"]
print(f"✅  Retrieved chunk has correct metadata: {top['metadata']}")

print("\n✅  All checks passed!")
