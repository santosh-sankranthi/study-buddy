# Long Context: Latency, Cost, and "Lost in the Middle"

> **Time:** ~2 min read | **Goal:** Understand why stuffing 100k+ tokens into a prompt is rarely the right engineering answer.

---

## 1. The Long Context Temptation

Modern frontier models boast context windows of 128k, 1M, or even 2M tokens. It is tempting to think:
*"Why bother curating or summarising? Let's just dump the entire 500-page textbook into every prompt!"*

---

## 2. The Three Realities of Giant Contexts

### Reality 1: Linear Cost Scaling
Every single token in the context window is billed on every single call.
If you send 100k tokens per question:
- 1 question = 100,000 tokens
- 10 turns = 1,000,000 tokens
At $2.50 / million tokens, an innocent 10-turn study session costs $2.50. With 10,000 students, that's $25,000 / day.

### Reality 2: Quadratic Attention & Latency
Processing large contexts takes time. Time to first token (TTFT) climbs from ~300ms for short prompts to 5–15 seconds for 100k+ tokens. Real users do not want to wait 10 seconds for a conversational tutor.

### Reality 3: "Lost in the Middle"
Research (Liu et al., 2023) demonstrates that LLMs attend strongly to the very beginning and very end of long contexts, while recall dips significantly for facts buried in the middle 60%.

---

## 3. The Engineering Takeaway

Long context is valuable for complex batch analysis (e.g. analyzing a codebase or reading a complete legal contract once). But for interactive, low-latency, cost-effective applications, **curating a small, relevant context** wins every time.
