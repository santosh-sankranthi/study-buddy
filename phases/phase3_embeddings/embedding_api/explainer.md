# Embedding Models & Batch API Integration

> **Time:** ~2 min read | **Goal:** Understand commercial embedding APIs, vector dimensionality, and the performance benefits of batching.

---

## 1. How Real Embedding Models Work

While toy models use 2 or 3 dimensions, production embedding models (e.g. OpenAI's `text-embedding-3-small`, Cohere, or local BGE models) project sentences into **1536** or **3072** continuous dimensions.

Each dimension captures subtle semantic facets:
- Polarity (positive / negative)
- Domain (scientific / legal / informal)
- Syntactic role
- Entity relations

---

## 2. Incompatible Embedding Spaces

> [!WARNING]
> You **cannot** compare a vector from Model A with a vector from Model B, or vectors of different dimensions.
> The coordinates have meaning only within the internal geometry learned by that specific model during training.

If you ever upgrade or switch your embedding model:
- You must **re-embed your entire database**.

---

## 3. The Power of Batching

Embedding 100 paragraphs individually requires 100 separate HTTP requests:
- 100 round-trips $\times$ ~150ms = **15 seconds**
- Multiple connection handshakes
- High risk of hitting API rate limits

Embedding 100 paragraphs in a **single batch request** (`embed_batch()`):
- 1 round-trip = **~400ms**
- Drastically reduced network overhead and lower latency
