"""EXERCISE -- Multimodal Chunk Formulation & Indexing.

The demo built raw multimodal API messages.
Your twist: implement create_multimodal_note_chunk() to format an extracted
diagram caption and image metadata into an indexable chunk dict, ready for ChromaDB.

Fill in every TODO. Run when done:
    python phases/phase9_advanced_capstone/multimodal/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


# ── TODO(1): Implement create_multimodal_note_chunk ──────────────────────────
def create_multimodal_note_chunk(
    image_uri: str,
    caption: str,
    filename: str,
    subject: str,
) -> dict:
    """Format an image diagram and its descriptive caption into a searchable chunk.

    Returns:
        {
            "text": str,
            "metadata": dict,
        }
    """
    # TODO(1): text = f"[DIAGRAM: {caption}]"
    #          metadata = {"filename": filename, "subject": subject, "has_image": True, "image_uri": image_uri}
    return {
        "text": f"[DIAGRAM: {caption}]",
        "metadata": {
            "filename": filename,
            "subject": subject,
            "has_image": True,
            "image_uri": image_uri,
        },
    }


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Converting images into structured descriptive captions allows multimodal content to be "
    "retrieved via standard text embeddings while preserving rich image URI metadata for UI rendering."
)


if __name__ == "__main__":
    uri = "data:image/png;base64,ABCDEF..."
    desc = "Krebs cycle showing conversion of citrate to isocitrate."
    chunk = create_multimodal_note_chunk(uri, desc, "krebs_diagram.png", "biology")
    print("Formatted Multimodal Chunk:")
    print("  Text:", chunk["text"])
    print("  Meta:", chunk["metadata"])
    print("\nObservation:", OBSERVATION)
