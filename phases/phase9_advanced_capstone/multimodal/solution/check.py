"""Self-check -- Multimodal exercise.

Run:
    python phases/phase9_advanced_capstone/multimodal/solution/check.py
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

print("Checking multimodal exercise ...\n")

chunk = ex.create_multimodal_note_chunk(
    image_uri="data:image/png;base64,mock",
    caption="Chloroplast thylakoid membrane",
    filename="chloroplast.png",
    subject="biology",
)

assert "text" in chunk and "[DIAGRAM: Chloroplast thylakoid membrane]" in chunk["text"]
meta = chunk.get("metadata", {})
assert meta.get("has_image") is True
assert meta.get("filename") == "chloroplast.png"
assert meta.get("subject") == "biology"
assert meta.get("image_uri") == "data:image/png;base64,mock"
print("✅  create_multimodal_note_chunk produced valid schema with caption and image metadata")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
