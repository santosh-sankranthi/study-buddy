"""Self-check -- Grounded Generation exercise.

Run:
    python phases/phase5_rag_pipeline/grounded_generation/solution/check.py
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

print("Checking grounded generation exercise ...\n")

from app.rag import extract_sources

# Test source deduplication
sources = extract_sources(ex.SAMPLE_CHUNKS)
assert len(sources) == 2, f"Expected 2 deduplicated sources, got {len(sources)}"
assert sources == ["bio.md", "chem.md"]
print("✅  extract_sources successfully deduplicated repeated filenames")

# Test prompt constraints
has_cite, has_abstain = ex.verify_prompt_rules("What is ATP?", ex.SAMPLE_CHUNKS)
assert has_cite is True, "System prompt missing citation instruction"
assert has_abstain is True, "System prompt missing abstention instruction"
print("✅  Prompt contains both citation and abstention rules")

# Test answer formatting
ans = ex.format_grounded_answer("Glycolysis produces 2 ATP.", sources)
assert "Sources: bio.md, chem.md" in ans
print("✅  format_grounded_answer correctly appends formatted sources footer")

print("\n✅  All checks passed!")
