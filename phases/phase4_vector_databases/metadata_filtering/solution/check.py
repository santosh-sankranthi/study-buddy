"""Self-check -- Metadata Filtering exercise.

Run:
    python phases/phase4_vector_databases/metadata_filtering/solution/check.py
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

print("Checking metadata filtering exercise ...\n")

ex.seed_chemistry_notes()
results = ex.search_subject_only("chemical reaction and bonding", "chemistry", k=2)

assert len(results) > 0, "Expected at least 1 result for chemistry query"
for r in results:
    subj = r["metadata"].get("subject")
    assert subj == "chemistry", f"Expected metadata subject 'chemistry', got '{subj}'"
print("✅  100% of returned items have metadata['subject'] == 'chemistry'")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
