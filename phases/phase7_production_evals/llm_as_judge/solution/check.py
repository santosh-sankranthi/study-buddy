"""Self-check -- LLM-as-a-Judge exercise.

Run:
    python phases/phase7_production_evals/llm_as_judge/solution/check.py
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

print("Checking LLM-as-a-Judge exercise ...\n")

res = ex.evaluate_flashcard_quality(
    question="What is the function of ribosomes?",
    answer="Protein synthesis by translating mRNA.",
    difficulty="easy",
)

assert "score" in res, "Evaluation result missing 'score' key"
assert isinstance(res["score"], int) and 1 <= res["score"] <= 5, f"Score must be int 1..5, got: {res['score']}"
assert "reason" in res and len(res["reason"].strip()) > 5, "Evaluation result missing descriptive reason"
print(f"✅  evaluate_flashcard_quality returned valid rubric score ({res['score']}/5) with justification")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
