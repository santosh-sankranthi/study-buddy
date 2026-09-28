# Retrieval with Confidence Thresholds

> **Time:** ~2 min read | **Goal:** Prevent hallucinations by establishing minimum similarity cutoffs before context reaches the generator.

---

## 1. The "Forced Retrieval" Failure Mode

Standard vector queries always return the top $k$ items, no matter how bad they are:
- User asks: *"Who was Napoleon Bonaparte?"*
- Database contains: *Only Biology notes*.
- Nearest neighbor search returns: *Cellular Respiration* (similarity: 0.18).

If you feed this 0.18 chunk to the LLM and tell it "Answer using only the provided notes", the model either gets confused or hallucinates a connection between Napoleon and mitochondria!

---

## 2. Setting a Minimum Similarity Threshold

Instead of blindly accepting the top $k$ results, we set a **confidence threshold**:

$$\text{similarity} = 1.0 - \text{distance} \ge \text{min\_similarity}$$

- If at least one chunk exceeds `min_similarity` (e.g., $\ge 0.30$), return the passing chunks.
- If **no chunk** passes the threshold, return `None` (or empty list).

---

## 3. Fallback Handling

When `retrieve()` returns `None`, the application intercepts the flow before making an LLM call:
- *"I don't have notes on that topic. Would you like me to answer using general knowledge?"*
- Or returns: *"No relevant course notes found for this question."*

This saves an unnecessary generation API call and completely prevents off-topic hallucinations.
