"""RAG prompt construction (Phase 5.4).

Builds the augmented prompt that instructs the model to answer ONLY from
retrieved context and to cite its sources.
"""

from __future__ import annotations

from app.security import wrap_chunk_as_untrusted


def build_rag_prompt(question: str, chunks: list[dict]) -> list[dict]:
    """Construct a grounded-generation message list.

    The system prompt instructs the model to:
      - Answer ONLY from the supplied context.
      - Cite every claim as [Chunk N — filename.md].
      - Say "I don't have enough information in your notes" if the context
        doesn't cover the question.

    Args:
        question: The student's question.
        chunks:   Retrieved chunks from vector_store.retrieve().
                  Each dict must have keys "text" and "metadata"
                  (metadata["filename"] is used for citation).

    Returns:
        A messages list ready to pass to common.llm.chat().
    """
    context_blocks = "\n\n".join(
        wrap_chunk_as_untrusted(
            i + 1,
            chunk["text"],
            chunk.get("metadata", {}).get("filename", "unknown"),
        )
        for i, chunk in enumerate(chunks)
    )

    system = (
        "You are Study Buddy, a grounded tutor. You MUST follow these rules:\n"
        "1. Answer ONLY using the context blocks provided below.\n"
        "2. After every factual claim, cite the source as [Chunk N — filename.md].\n"
        "3. If the context does NOT contain enough information to answer, say exactly:\n"
        "   \"I don't have enough information in your notes to answer this.\"\n"
        "4. Do NOT add information from your training data. Notes are the only source of truth.\n"
        "5. Keep your answer under 150 words."
    )

    return [
        {"role": "system", "content": system},
        {
            "role":    "user",
            "content": f"Context:\n\n{context_blocks}\n\nQuestion: {question}",
        },
    ]


def extract_sources(chunks: list[dict]) -> list[str]:
    """Return a list of unique source filenames from retrieved chunks."""
    seen   = set()
    result = []
    for chunk in chunks:
        fname = chunk.get("metadata", {}).get("filename", "unknown")
        if fname not in seen:
            seen.add(fname)
            result.append(fname)
    return result
