# Vector Databases: Indexing & Persistence

> **Time:** ~2 min read | **Goal:** Understand why production applications need dedicated vector databases like ChromaDB instead of raw Python lists.

---

## 1. Why Python Lists Fail at Scale

In Phase 3, we compared the query against every document using `for doc in docs` ($O(N)$ brute-force linear scan).
- For 10 documents: fast (~1ms).
- For 100,000 documents: 100,000 dot products per query $\rightarrow$ seconds of lag.
- When the server restarts: all vectors in Python memory vanish.

---

## 2. Approximate Nearest Neighbor (ANN) & HNSW

Dedicated vector databases index vectors using graph-based structures such as **HNSW (Hierarchical Navigable Small World)**:
- Instead of checking all $N$ vectors, HNSW navigates through multi-layered graphs in $O(\log N)$ time.
- Searches millions of vectors in single-digit milliseconds.

---

## 3. ChromaDB Architecture

In Study Buddy, we use **ChromaDB**:
- **Persistent storage:** Stored locally in SQLite and Parquet under `./data/chroma`. Survived across app restarts.
- **Collection space:** Configured with `hnsw:space: "cosine"`.
- **Distance vs. Similarity:**
  - Chroma returns **cosine distance** $D \in [0, 2]$.
  - Identical vectors have distance $0.0$.
  - Cosine similarity $S = 1 - D$.
