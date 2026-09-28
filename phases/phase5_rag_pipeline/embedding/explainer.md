# 5.2 — Embedding in RAG (Plumbing Reuse)

## What was broken before
In Phase 3 and 4, we built vector embeddings and stored them in ChromaDB. In RAG, we don't reinvent embedding: we reuse that exact vector pipeline to turn student queries into query vectors that match indexed chunk vectors.

## How it works
When the user asks a question, we call `embed(question)` (or batch embed). The resulting vector is compared against chunk embeddings in ChromaDB using cosine distance. Consistent embedding dimensions and model selection are critical — never mix different embedding models within the same vector store.
