"""DEMO -- The RAG Triad Evaluation Metrics.

Live-code target: score an end-to-end RAG interaction across the three pillars:
Context Relevance, Faithfulness, and Answer Relevance, computing the composite score.

Run:
    python phases/phase9_advanced_capstone/eval_frameworks/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

QUERY = "Where does glycolysis occur and what is its net ATP yield?"
CONTEXT = (
    "Glycolysis takes place in the cytoplasm of eukaryotic and prokaryotic cells. "
    "It converts one glucose molecule into two pyruvate molecules, producing a net yield of 2 ATP and 2 NADH."
)
ANSWER = "Glycolysis occurs in the cytoplasm and produces a net yield of 2 ATP molecules."


def compute_rag_triad(query: str, context: str, answer: str) -> dict[str, float]:
    """Compute RAG Triad metrics (normalized 0.0 to 1.0)."""
    # 1. Context Relevance: Does context contain terms answering the query?
    q_terms = {"glycolysis", "occur", "net", "atp"}
    c_lower = context.lower()
    ctx_rel = round(sum(1 for t in q_terms if t in c_lower) / len(q_terms), 2)

    # 2. Faithfulness: Are answer claims present in context?
    ans_terms = {"cytoplasm", "2 atp"}
    faithfulness = round(sum(1 for t in ans_terms if t in c_lower) / len(ans_terms), 2)

    # 3. Answer Relevance: Does the answer address where and what yield?
    ans_lower = answer.lower()
    ans_rel = round(1.0 if ("cytoplasm" in ans_lower and "2 atp" in ans_lower) else 0.5, 2)

    composite = round((ctx_rel + faithfulness + ans_rel) / 3.0, 2)

    return {
        "context_relevance": ctx_rel,
        "faithfulness": faithfulness,
        "answer_relevance": ans_rel,
        "composite_score": composite,
    }


print("=" * 60)
print("RAG TRIAD EVALUATION DEMO")
print("=" * 60)

metrics = compute_rag_triad(QUERY, CONTEXT, ANSWER)
print(f"Query:  {QUERY}")
print(f"Answer: {ANSWER}\n")
print(f"1. Context Relevance: {metrics['context_relevance']:0.2f}")
print(f"2. Faithfulness:       {metrics['faithfulness']:0.2f}")
print(f"3. Answer Relevance:   {metrics['answer_relevance']:0.2f}")
print("-" * 35)
print(f"Composite Triad Score: {metrics['composite_score']:0.2f} / 1.00")
