# Vector Representations & Cosine Similarity

> **Time:** ~2 min read | **Goal:** Understand high-dimensional text vectors and compute cosine similarity from first principles without external math libraries.

---

## 1. Words as Geometric Coordinates

Computers cannot understand the conceptual meaning of words. They can only calculate with numbers.

An **embedding** maps a piece of text to a list of floating-point numbers (a vector) in an $N$-dimensional space (e.g., $N=1536$).
- Texts with similar meanings are mapped to vectors that point in nearly the same direction.
- Unrelated texts point in different, nearly orthogonal directions.

---

## 2. Cosine Similarity Formula

To measure how close two vectors $\mathbf{A}$ and $\mathbf{B}$ are, we compute the cosine of the angle between them:

$$\text{cosine\_similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$

### Intuition:
- **$+1.0$**: Vectors point in identical directions (identical meaning).
- **$0.0$**: Vectors are perpendicular / orthogonal (completely unrelated).
- **$-1.0$**: Vectors point in diametrically opposite directions.

---

## 3. Why Cosine Similarity Over Euclidean Distance?

Euclidean distance measures the physical length of the difference between points, which is sensitive to document length (a longer text with repeated terms produces larger magnitudes).

Cosine similarity normalizes vector lengths to unit length, measuring purely the **direction** (the topical focus), making it invariant to document length.
