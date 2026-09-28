# Memory: Conversation History Management

> **Time:** ~2 min read | **Goal:** Understand why LLMs are stateless and how conversational memory is maintained in multi-turn applications.

---

## 1. LLMs are Stateless

Every HTTP call to an LLM provider (OpenAI, Anthropic, OpenRouter) is completely independent. The model retains zero memory of previous requests.

When a user chats with Study Buddy:
- **Turn 1:** User: "I am studying for my Biology midterm." → Assistant: "Great! What topic would you like to start with?"
- **Turn 2:** User: "What is its main energy molecule?"

If Turn 2 only sends "What is its main energy molecule?", the LLM has no idea what "its" refers to.

---

## 2. Maintaining Conversational Memory

To provide a seamless conversational experience, the application server maintains a session store:
```
Session 'biology-101'
├── Turn 1: user: "I am studying for my Biology midterm."
├── Turn 1: assistant: "Great! What topic would you like to start with?"
└── Turn 2: user: "What is its main energy molecule?"
```

On Turn 2, the app prefixes the history before sending the prompt to the model.

---

## 3. The Memory Dilemma: Unbounded Growth

If every message is kept forever:
1. Context token usage increases linearly on every turn.
2. Costs escalate rapidly.
3. The prompt eventually hits the model's hard context limit, crashing the app.

Hence, memory management strategies like **sliding window token trimming** and **summarization compaction** are essential.
