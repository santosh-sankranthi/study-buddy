# Phase 3 Instructor Guide: Embeddings & Vector Semantics

## Learning Objectives
1. Understand high-dimensional vector representations of text.
2. Implement and verify cosine similarity mathematically without libraries.
3. Transition from hardcoded toy vectors to real embedding models.
4. Execute semantic search by ranking text by vector similarity.

## Timing & Pacing (Total: 45 min)
- **3.1 Vector Representations (15 min)**: Hand-rolled dot product and norms; invariant testing.
- **3.2 Embedding Models (15 min)**: Live API call via `embed()`; students implement `embed_batch()`.
- **3.3 Semantic Search (15 min)**: Ranking candidate sentences against user queries.

## Key Teaching Point
- Contrast keyword search with vector search: "Photosynthesis" and "Plants absorb sunlight" share almost no words, yet their cosine similarity is > 0.85.
