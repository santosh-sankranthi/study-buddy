"""EXERCISE -- Citations and Grounded RAG Prompts.

The demo built an augmented RAG prompt.
Your twist: ensure every retrieved context chunk explicitly includes its source filename
and instruct the model to cite the filename in its response.

Run when done:
    python phases/phase5_rag_pipeline/grounded_generation/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str
# Each chunk has chunk['text'] and chunk['metadata']['filename'].
# Format each chunk as:
#   [Source: <filename>]
#   <text>
#   [End Source]
# Followed by instructions: "Answer using only the sources above. Cite the source filename."

def build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str:
    raise NotImplementedError("TODO(1): implement build_rag_prompt_with_sources")


if __name__ == "__main__":
    sample_chunks = [
        {"text": "Chlorophyll absorbs blue and red light.", "metadata": {"filename": "photosynthesis.md"}},
    ]
    prompt = build_rag_prompt_with_sources("What light does chlorophyll absorb?", sample_chunks)
    print("Generated RAG Prompt:
", prompt)
