"""DEMO -- AI Engineering Technique Decision Engine.

Live-code target: evaluate system requirements (knowledge freshness, citation needs,
latency ceilings, style specificity) to deterministically recommend Prompt Engineering,
RAG, or Fine-Tuning.

Run:
    python phases/phase9_advanced_capstone/fine_tuning_concepts/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


def recommend_technique(
    needs_dynamic_knowledge: bool,
    needs_citations: bool,
    strict_style_or_format: bool,
    high_volume_low_latency: bool,
) -> tuple[str, str]:
    """Recommend the optimal architecture based on technical requirements."""
    if needs_dynamic_knowledge or needs_citations:
        return (
            "RAG",
            "Dynamic factual knowledge and source attribution require external retrieval, not baked weights.",
        )
    if strict_style_or_format and high_volume_low_latency:
        return (
            "Fine-Tuning (LoRA)",
            "High throughput and fixed syntax benefit from baking style into weights, cutting prompt token costs.",
        )
    return (
        "Prompt Engineering",
        "Fastest to iterate, zero training costs, optimal for personas and general reasoning.",
    )


SCENARIOS = [
    {
        "name": "Live Student Notes Q&A",
        "dynamic": True,
        "citations": True,
        "style": False,
        "high_vol": False,
    },
    {
        "name": "High-Throughput JSON Flashcard API (10M requests/day)",
        "dynamic": False,
        "citations": False,
        "style": True,
        "high_vol": True,
    },
    {
        "name": "Prototype Socratic Persona",
        "dynamic": False,
        "citations": False,
        "style": True,
        "high_vol": False,
    },
]

print("=" * 60)
print("ARCHITECTURAL DECISION MATRIX DEMO")
print("=" * 60)

for sc in SCENARIOS:
    tech, reason = recommend_technique(
        sc["dynamic"], sc["citations"], sc["style"], sc["high_vol"]
    )
    print(f"\nScenario: {sc['name']}")
    print(f"  -> Recommended: {tech}")
    print(f"  -> Rationale:   {reason}")
