# Evaluation Frameworks & The RAG Triad

> **Time:** ~2 min read | **Goal:** Master the industry-standard evaluation triad (Context Relevance, Groundedness, Answer Relevance) used by Ragas and DeepEval.

---

## 1. Beyond Ad-Hoc Testing

While custom unit tests verify basic edge cases, production evaluation frameworks (such as **Ragas** and **DeepEval**) formalize evaluation into three orthogonal metrics known as **The RAG Triad**:

```
                  ┌──────────────────────┐
                  │      User Query      │
                  └──────────┬───────────┘
                             │
            ▲                │                ▲
            │ (3)            │                │ (1)
    Answer Relevance         │        Context Relevance
            │                │                │
            ▼                ▼                ▼
┌──────────────────────┐           ┌──────────────────────┐
│   Generated Answer   │◄──────────┤   Retrieved Context  │
└──────────────────────┘    (2)    └──────────────────────┘
                        Faithfulness /
                         Groundedness
```

---

## 2. The Three Pillars of the Triad

### 1. Context Relevance
- **Question:** *Did retrieval find relevant context, or did it bring back noise?*
- **Formula:** $\frac{\text{Relevant sentences in retrieved chunks}}{\text{Total sentences in retrieved chunks}}$

### 2. Groundedness (Faithfulness)
- **Question:** *Is every statement in the answer supported by the retrieved context?*
- **Formula:** $\frac{\text{Answer claims verified by context}}{\text{Total claims made in answer}}$

### 3. Answer Relevance
- **Question:** *Does the answer actually answer the user's specific question?*
- **Formula:** Measures semantic alignment between the user's question and the generated answer, regardless of whether it's grounded.

---

## 3. The Triad Composite Score

$$\text{Composite RAG Score} = \frac{\text{Context Relevance} + \text{Groundedness} + \text{Answer Relevance}}{3}$$

By tracking this composite metric across prompt iterations, chunking adjustments, and embedding model upgrades, you scientifically validate pipeline improvements.
