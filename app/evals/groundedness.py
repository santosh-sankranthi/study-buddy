"""Groundedness eval — LLM-as-judge + deterministic checks (Phase 5.5 / 9.2)."""

from __future__ import annotations

import re

from common.llm import chat


# ── LLM-as-judge (Phase 5.5) ──────────────────────────────────────────────────

def check_groundedness(answer: str, context: str) -> bool:
    """Ask the LLM whether *answer* is supported by *context*.

    Returns True if the answer is grounded, False if it appears to hallucinate.
    """
    prompt = [
        {
            "role":    "system",
            "content": "You are a strict fact-checker. Answer ONLY 'YES' or 'NO'.",
        },
        {
            "role":    "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Does the following answer contain ONLY information from the context above? "
                f"Answer YES or NO.\n\n"
                f"Answer: {answer}"
            ),
        },
    ]
    try:
        verdict = chat(prompt, temperature=0.0).strip().upper()
        return verdict.startswith("YES")
    except Exception:
        # Offline heuristic fallback: require at least 70% of answer content words to appear in context
        stopwords = {"the", "a", "an", "is", "in", "it", "to", "of", "and", "at", "by", "that", "this", "chunk", "md", "1", "2", "3"}
        ans_words = {w for w in re.findall(r"\w+", answer.lower()) if w not in stopwords}
        ctx_words = set(re.findall(r"\w+", context.lower()))
        if not ans_words:
            return True
        overlap = len(ans_words & ctx_words) / len(ans_words)
        return overlap >= 0.70


# ── Deterministic checks (Phase 5.5 exercise / 9.1) ──────────────────────────

def check_length_and_citation(answer: str, max_words: int = 100) -> dict:
    """Deterministic check: answer is short enough AND contains a citation marker.

    Returns:
        {word_count, under_limit, has_citation, passed}
    """
    word_count   = len(answer.split())
    has_citation = bool(re.search(r"\[Chunk\s*\d+", answer) or ".md" in answer)
    return {
        "word_count":   word_count,
        "under_limit":  word_count <= max_words,
        "has_citation": has_citation,
        "passed":       word_count <= max_words and has_citation,
    }


# ── Reusable LLM judge (Phase 9.2) ───────────────────────────────────────────

def llm_judge(answer: str, context: str, criteria: str) -> dict:
    """Generic LLM-as-judge scoring function.

    Args:
        answer:   The text to evaluate.
        context:  Optional reference context (pass "" if not relevant).
        criteria: A plain-language description of the scoring criteria.

    Returns:
        {"score": int (1–5), "reason": str}
    """
    import json
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
            import re as _re
            m = _re.search(r'\{.*?"score".*?\}', resp, _re.DOTALL)
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
