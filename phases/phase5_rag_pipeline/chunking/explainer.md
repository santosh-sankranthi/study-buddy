# Chunking Strategies: Fixed-Size vs. Paragraph vs. Semantic

> **Time:** ~2 min read | **Goal:** Understand how document segmentation trades off contextual completeness against retrieval precision.

---

## 1. Why Chunk at All?

If you embed an entire 50-page biology textbook as a single vector:
1. The vector becomes a vague "average" of everything from cell membranes to human evolution.
2. When a user asks about "glycolysis ATP count", the global document vector has poor cosine similarity to that specific question.
3. Even if retrieved, the whole 50-page text blows past the model's prompt budget.

**Chunking** segments documents into compact, highly focused passages.

---

## 2. Fixed-Size Chunking with Overlap

- **Mechanism:** Slide a window of size $N$ words (or tokens) across the text, advancing by $N - \text{overlap}$ on each step.
- **Why Overlap?** If an important definition is split across chunk 1 and chunk 2, neither chunk has the complete fact. Overlap ensures sentences spanning the seam appear in full in at least one chunk.
- **Trade-off:** Fast and predictable in size, but can split sentences or paragraphs mid-thought.

---

## 3. Paragraph & Semantic Chunking

- **Paragraph Chunking (`\n\n`):** Preserves natural human conceptual boundaries. A paragraph usually focuses on a single coherent idea.
- **Trade-off:** Paragraph lengths can vary widely — some are 1 sentence, others are 1,000 words.

A production RAG system often uses **hybrid chunking**: split by structural headings or paragraphs first, then apply fixed-size splitting with overlap only to paragraphs that exceed the token ceiling.
