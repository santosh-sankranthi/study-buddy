# Metadata Filtering: Pre-filtering vs. Post-filtering

> **Time:** ~2 min read | **Goal:** Understand why pure vector search is not enough, and how metadata filtering narrows the search space deterministically.

---

## 1. Why Pure Vector Search Fails Business Logic

Suppose a student asks:
*"What are the laws of conservation?"*

This concept exists in:
- Physics (Conservation of Energy, Momentum)
- Chemistry (Conservation of Mass)
- Biology (Nutrient Cycling)

If the student is currently studying for their **Physics** midterm, returning Biology notes is confusing and unhelpful. An embedding vector alone cannot enforce business constraints like:
- `subject == "physics"`
- `user_id == current_user`
- `created_at >= 2026-01-01`
- `visibility == "public"`

---

## 2. Pre-Filtering vs. Post-Filtering

### Post-Filtering (Naive):
1. Query the vector index for the top $k=10$ nearest neighbors.
2. In Python, filter out results where `metadata.subject != "physics"`.

**The Failure Mode:** If all 10 top results happened to be Chemistry, post-filtering leaves you with **0 results**, even if valid Physics notes existed further down in the database!

### Pre-Filtering (ChromaDB / Production Vector DBs):
1. The vector index uses the metadata index to restrict candidate vectors *before* or *during* graph traversal.
2. It guarantees returning $k$ documents that satisfy both semantic similarity **and** metadata predicates.

---

## 3. Metadata Filtering in ChromaDB

```python
results = collection.query(
    query_embeddings=[embed(query)],
    n_results=k,
    where={"subject": "physics"},  # HNSW pre-filter
)
```
