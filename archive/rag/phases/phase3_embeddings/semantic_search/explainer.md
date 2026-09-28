# Semantic Search vs. Keyword Matching

> **Time:** ~2 min read | **Goal:** Understand why vector search succeeds where keyword search fails, and implement a pure vector-based search engine.

---

## 1. The Limitation of Keyword Search

Traditional search (lexical matching, inverted index, BM25) looks for literal character or word overlap:
- Query: *"how do plants make food?"*
- Document: *"Photosynthesis converts radiant solar energy into chemical sugars."*

A keyword search engine finds **0 matching words** (except perhaps "into"). It completely misses the document.

---

## 2. Semantic Search Mechanics

With semantic search:
1. **Offline / Index time:** Each candidate text chunk is converted to an embedding vector $\mathbf{v}_{\text{doc}}$.
2. **Query time:** The user's query is converted into an embedding vector $\mathbf{v}_{\text{query}}$ using the *same* model.
3. **Similarity computation:** Cosine similarity is computed between $\mathbf{v}_{\text{query}}$ and each $\mathbf{v}_{\text{doc}}$.
4. **Ranking:** Documents are sorted descending by score; the top $k$ items are returned.

Because the embedding model was trained on billions of sentences, it knows that "plants make food" is semantically synonymous with "photosynthesis produces sugars".

---

## 3. The Core Search Loop

In Python (`app/search.py`):
```python
query_vec = embed(query)
doc_vecs  = embed_batch(docs)
scores    = [cosine_similarity(query_vec, d_vec) for d_vec in doc_vecs]
ranked    = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
return ranked[:k]
```
