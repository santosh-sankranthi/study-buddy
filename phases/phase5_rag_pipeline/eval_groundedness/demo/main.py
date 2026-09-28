"""DEMO -- Groundedness Evaluation.

Live-code target: evaluate candidate RAG answers using check_length_and_citation()
and check_groundedness() from app.evals.groundedness, identifying hallucinations.

Run:
    python phases/phase5_rag_pipeline/eval_groundedness/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.evals.groundedness import check_groundedness, check_length_and_citation

CONTEXT = (
    "Mitochondria are double-membraned organelles found in most eukaryotic cells. "
    "They generate most of the cell's supply of adenosine triphosphate (ATP), "
    "used as a source of chemical energy."
)

ANS_GROUNDED = (
    "Mitochondria generate adenosine triphosphate (ATP) for eukaryotic cells [Chunk 1 — bio.md]."
)

ANS_HALLUCINATED = (
    "Mitochondria produce ATP and also conduct photosynthesis using chlorophyll pigments [Chunk 1 — bio.md]."
)

print("=" * 60)
print("GROUNDEDNESS EVALUATION DEMO")
print("=" * 60)

# 1. Deterministic checks
print("\n--- Tier 1: Deterministic Check ---")
det_result = check_length_and_citation(ANS_GROUNDED, max_words=30)
print(f"Word count:   {det_result['word_count']}")
print(f"Has citation: {det_result['has_citation']}")
print(f"Passed:       {det_result['passed']}")

# 2. LLM Judge on grounded answer
print("\n--- Tier 2: Grounded Answer Eval ---")
is_grounded = check_groundedness(ANS_GROUNDED, CONTEXT)
print(f"Answer:   {ANS_GROUNDED}")
print(f"Grounded: {is_grounded} (Expected: True)")

# 3. LLM Judge on hallucinated answer
print("\n--- Tier 2: Hallucinated Answer Eval ---")
is_hallucinated = check_groundedness(ANS_HALLUCINATED, CONTEXT)
print(f"Answer:   {ANS_HALLUCINATED}")
print(f"Grounded: {is_hallucinated} (Expected: False — chlorophyll is not in context!)")
