# Phase 4 Instructor Guide: Vector Databases (ChromaDB)

## Learning Objectives
1. Understand why vector databases are necessary (persistent indexing, HNSW indexing, metadata filtering).
2. Ingest notes and compute document IDs in an embedded ChromaDB collection.
3. Perform similarity queries with strict metadata filters.

## Timing & Pacing (Total: 35 min)
- **4.1 Indexing (15 min)**: Initialize ChromaDB client; index sample notes.
- **4.2 Similarity Search (20 min)**: Query top-k with `where={"subject": "physics"}` filters.

## Common Stumbling Blocks
- Remind students that distance in Chroma with cosine space is $1 - 	ext{similarity}$. Identical vectors have distance 0.
