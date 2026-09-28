"""EXERCISE -- Grounded Prompt Constraints & Attribution Formatting.

The demo generated prompt messages from raw chunks.
Your twist: verify that build_rag_prompt() strictly includes citation and abstention
constraints, that extract_sources() deduplicates filenames, and implement
format_grounded_answer() to append source metadata to the assistant's reply.

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/grounded_generation/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.rag import build_rag_prompt, extract_sources


# ── TODO(1): Verify prompt constraints ───────────────────────────────────────
def verify_prompt_rules(question: str, chunks: list[dict]) -> tuple[bool, bool]:
    """Return (has_citation_rule, has_abstention_rule)."""
    messages = build_rag_prompt(question, chunks)
    sys_content = messages[0]["content"]
    # TODO(1): check if "[Chunk N — filename.md]" and "don't have enough information" are in sys_content
    has_cite = "[Chunk N — filename.md]" in sys_content
    has_abstain = "don't have enough information in your notes" in sys_content
    return has_cite, has_abstain


# ── TODO(2): Implement format_grounded_answer ────────────────────────────────
def format_grounded_answer(answer: str, sources: list[str]) -> str:
    """Format final user-facing text with a 'Sources: file1, file2' footer."""
    if not sources:
        return answer
    # TODO(2): return f"{answer}\n\nSources: {', '.join(sources)}"
    return f"{answer}\n\nSources: {', '.join(sources)}"


SAMPLE_CHUNKS = [
    {"text": "A", "metadata": {"filename": "bio.md"}},
    {"text": "B", "metadata": {"filename": "bio.md"}},  # duplicate file
    {"text": "C", "metadata": {"filename": "chem.md"}},
]

if __name__ == "__main__":
    sources = extract_sources(SAMPLE_CHUNKS)
    print("Deduplicated sources:", sources)
    cite_rule, abstain_rule = verify_prompt_rules("What is ATP?", SAMPLE_CHUNKS)
    print("Has citation rule:", cite_rule)
    print("Has abstention rule:", abstain_rule)
    formatted = format_grounded_answer("Glycolysis produces 2 ATP [Chunk 1 — bio.md].", sources)
    print("\nFormatted response:\n", formatted)
