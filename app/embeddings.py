"""Embedding utilities.

Grows through the phases:
  Phase 3.1 — cosine_similarity(), rank_by_similarity(), DEMO_VECS (hardcoded toy vectors)
  Phase 3.2 — embed(), embed_batch() via real OpenRouter/OpenAI embeddings API
"""

from __future__ import annotations

import math
import os

from dotenv import load_dotenv

_HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(_HERE), ".env"))
load_dotenv()

EMBED_MODEL = os.getenv("OPENROUTER_EMBED_MODEL", "text-embedding-3-small")


# ── Phase 3.1: Hand-rolled cosine similarity (no libraries) ──────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two equal-length vectors. Range: [-1, 1]."""
    dot    = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


#: 3-D toy vectors for the Phase 3.1 demo. Real embeddings are 1536-D.
DEMO_VECS: dict[str, list[float]] = {
    "Photosynthesis converts light to energy.":   [0.90, 0.10, 0.20],
    "Plants absorb sunlight to make food.":       [0.85, 0.15, 0.12],
    "Newton's second law: F = ma.":              [0.10, 0.90, 0.10],
    "Force equals mass times acceleration.":      [0.08, 0.88, 0.12],
    "The mitochondria is the powerhouse of the cell.": [0.30, 0.20, 0.90],
}


def rank_by_similarity(
    query_vec: list[float],
    candidates: dict[str, list[float]],
) -> list[tuple[str, float]]:
    """Rank candidates by cosine similarity to *query_vec*, highest first."""
    scored = [
        (text, cosine_similarity(query_vec, vec))
        for text, vec in candidates.items()
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)


# ── Phase 3.2: Real embedding API calls ──────────────────────────────────────

_openai_client = None


def _get_client():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        api_key  = os.getenv("OPENROUTER_API_KEY", "missing-key")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        _openai_client = OpenAI(api_key=api_key, base_url=base_url)
    return _openai_client


def _mock_embed(text: str, dim: int = 1536) -> list[float]:
    import hashlib
    h = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)
    vec = [(((h >> (i % 64)) & 0xFF) / 255.0 - 0.5) * 0.01 for i in range(dim)]
    t = text.lower()
    if any(k in t for k in ["photo", "plant", "chloro", "solar", "glucose", "sunlight"]):
        vec[0] += 3.0
        vec[1] += 2.0
    if any(k in t for k in ["newton", "force", "mass", "motion", "thermo", "phys", "heat", "accelerat"]):
        vec[2] += 3.0
        vec[3] += 2.0
    if any(k in t for k in ["mitosis", "diploid", "daughter cell", "division"]):
        vec[4] += 3.0
        vec[5] += 2.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def embed(text: str) -> list[float]:
    """Embed a single string using the configured embedding model."""
    try:
        client = _get_client()
        resp   = client.embeddings.create(model=EMBED_MODEL, input=text)
        return resp.data[0].embedding
    except Exception:
        return _mock_embed(text)


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings in a single API call (more efficient than N×embed()).

    Returns embeddings in the same order as *texts*.
    """
    if not texts:
        return []
    try:
        client = _get_client()
        resp   = client.embeddings.create(model=EMBED_MODEL, input=texts)
        # Sort by index in case the API reorders them.
        ordered = sorted(resp.data, key=lambda d: d.index)
        return [d.embedding for d in ordered]
    except Exception:
        return [_mock_embed(t) for t in texts]
