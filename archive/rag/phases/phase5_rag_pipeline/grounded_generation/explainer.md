# Grounded Generation & Citation Attribution

> **Time:** ~2 min read | **Goal:** Construct prompts that constrain the model to cite retrieved notes and explicitly abstain when evidence is missing.

---

## 1. Grounding Constraints

Even when provided with retrieved context, LLMs have a tendency to:
1. Interpolate facts from their pre-training data that contradict the student's specific course syllabus.
2. Fabricate plausible-sounding explanations when the text doesn't contain the answer.
3. Fail to attribute which note supplied which fact.

To guarantee trustworthy answers, we construct a **grounded system prompt**.

---

## 2. Anatomy of a Grounded Prompt (`app/rag.py`)

A grounded RAG prompt must contain four strict instructions:
1. **Source of Truth:** "Answer ONLY using the context blocks provided below."
2. **Citation Requirement:** "After every factual claim, cite the source as `[Chunk N — filename.md]`."
3. **Abstention Instruction:** "If the context does NOT contain enough information, say exactly: *'I don't have enough information in your notes to answer this.'*"
4. **Untrusted Data Isolation:** Wrapping chunks with security boundaries to neutralize indirect prompt injections.

---

## 3. Extracting Structured Citations

Alongside the generated response string, the application extracts the unique set of cited filenames (`extract_sources(chunks)`). The frontend renders these as clickable citation chips below the tutor's response.
