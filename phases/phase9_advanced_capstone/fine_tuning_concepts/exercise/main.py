"""EXERCISE -- Selecting the Optimal Architecture.

The demo evaluated basic scenarios against Prompting vs. RAG vs. Fine-Tuning.
Your twist: implement classify_engineering_problem() to correctly route 4 distinct
production scenarios, verifying that each recommendation matches real-world trade-offs.

Fill in every TODO. Run when done:
    python phases/phase9_advanced_capstone/fine_tuning_concepts/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


# ── TODO(1): Implement classify_engineering_problem ──────────────────────────
def classify_engineering_problem(scenario_features: dict) -> str:
    """Return 'RAG', 'Fine-Tuning', or 'Prompt Engineering'.

    Features:
      - 'frequent_updates': bool (documents change daily/weekly)
      - 'strict_citations': bool (must cite specific pages or chunk IDs)
      - 'specialized_syntax': bool (special domain grammar, e.g. SQL dialect)
      - 'volume_over_1m_daily': bool (extreme high volume where prompt cost matters)
    """
    # TODO(1):
    #   If frequent_updates or strict_citations -> return 'RAG'
    #   If specialized_syntax and volume_over_1m_daily -> return 'Fine-Tuning'
    #   Else -> return 'Prompt Engineering'
    if scenario_features.get("frequent_updates") or scenario_features.get("strict_citations"):
        return "RAG"
    if scenario_features.get("specialized_syntax") and scenario_features.get("volume_over_1m_daily"):
        return "Fine-Tuning"
    return "Prompt Engineering"


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Fine-tuning changes behavior, style, and syntax, whereas RAG supplies verifiable, "
    "dynamic facts. Selecting the wrong tool leads to either hallucination (fine-tuning for facts) "
    "or massive cost bloat (prompt-stuffing static style)."
)


if __name__ == "__main__":
    test_scenarios = [
        {"name": "Legal Contract Analysis", "frequent_updates": True, "strict_citations": True},
        {"name": "Internal SQL Dialect Parser", "specialized_syntax": True, "volume_over_1m_daily": True},
        {"name": "Customer Support Tone Experiment", "frequent_updates": False, "strict_citations": False},
    ]
    for s in test_scenarios:
        rec = classify_engineering_problem(s)
        print(f"{s['name']}: -> {rec}")
    print("\nObservation:", OBSERVATION)
