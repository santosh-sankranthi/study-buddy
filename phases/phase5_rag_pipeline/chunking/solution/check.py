"""Self-check -- Chunking exercise.

Run:
    python phases/phase5_rag_pipeline/chunking/solution/check.py
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

print("Checking chunking exercise ...\n")

# Verify paragraph chunks
p_chunks = ex.get_paragraph_chunks()
assert len(p_chunks) == 3, f"Expected 3 paragraph chunks, got {len(p_chunks)}"
assert "Biotic factors" in p_chunks[1]
assert "Abiotic factors" in p_chunks[2]
print("✅  chunk_paragraph cleanly separated the 3 distinct thematic sections")

# Verify fixed chunks
f_chunks = ex.get_fixed_chunks(size=30, overlap=10)
assert len(f_chunks) >= 4, f"Expected >= 4 fixed chunks for ~90 words, got {len(f_chunks)}"
assert all(len(c.split()) <= 30 for c in f_chunks), "No fixed chunk should exceed chunk_size words"
print(f"✅  chunk_fixed created {len(f_chunks)} chunks, all respecting the 30-word limit")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
