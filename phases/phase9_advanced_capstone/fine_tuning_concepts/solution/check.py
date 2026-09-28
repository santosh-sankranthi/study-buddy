"""Self-check -- Fine-Tuning Concepts exercise.

Run:
    python phases/phase9_advanced_capstone/fine_tuning_concepts/solution/check.py
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

print("Checking fine-tuning concepts exercise ...\n")

# Test 1: RAG scenario
s1 = {"frequent_updates": True, "strict_citations": True}
assert ex.classify_engineering_problem(s1) == "RAG"
print("✅  Dynamic documents with citations correctly routed to RAG")

# Test 2: Fine-Tuning scenario
s2 = {"specialized_syntax": True, "volume_over_1m_daily": True}
assert ex.classify_engineering_problem(s2) == "Fine-Tuning"
print("✅  High-volume specialized syntax correctly routed to Fine-Tuning")

# Test 3: Prompt Engineering scenario
s3 = {"frequent_updates": False, "strict_citations": False, "volume_over_1m_daily": False}
assert ex.classify_engineering_problem(s3) == "Prompt Engineering"
print("✅  Prototyping persona correctly routed to Prompt Engineering")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
