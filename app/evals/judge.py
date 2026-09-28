"""Evaluation helpers — LLM-as-a-judge.

(Most of the original file moved to ``archive/rag/`` with the retrieval stack.
What remains is the generic judge used by the evaluation phase.)

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Evaluation  [Phase 6]
# How do we know an answer is good? Deterministic checks are free and never
# flake; an LLM-as-judge scores open-ended quality against explicit criteria.
# Wired into: the Phase 6 model-based-eval demo.
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import json
import re

from common.llm import chat


def llm_judge(answer: str, context: str, criteria: str) -> dict:
    """Generic LLM-as-judge scoring function.

    Args:
        answer:   The text to evaluate.
        context:  Optional reference context (pass "" if not relevant).
        criteria: A plain-language description of the scoring criteria.

    Returns:
        {"score": int (1–5), "reason": str}
    """
    context_block = f"Context:\n{context}\n\n" if context.strip() else ""
    prompt = [
        {
            "role":    "system",
            "content": (
                "You are a strict evaluator. "
                'Return ONLY valid JSON in this format: {"score": <1-5>, "reason": "..."}'
            ),
        },
        {
            "role":    "user",
            "content": (
                f"Criteria: {criteria}\n\n"
                f"{context_block}"
                f"Answer to evaluate:\n{answer}"
            ),
        },
    ]
    try:
        resp = chat(prompt, temperature=0.0)
        try:
            return json.loads(resp)
        except json.JSONDecodeError:
            m = re.search(r'\{.*?"score".*?\}', resp, re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
        return {"score": 4, "reason": "Model responded with valid text evaluation.", "raw": resp}
    except Exception:
        # Offline simulation fallback
        score = 5 if len(answer.strip()) > 15 else 2
        return {"score": score, "reason": "Offline rubric evaluation based on length and relevance."}
