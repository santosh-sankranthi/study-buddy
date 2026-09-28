# Output Moderation & Harm Prevention

> **Time:** ~2 min read | **Goal:** Safeguard student users by screening model generations for policy violations before delivery.

---

## 1. Why Moderate Model Outputs?

Even with input sanitization and strict system prompts:
- Jailbreak attacks can succeed in coercing unsafe outputs.
- Complex user queries might prompt the model to generate self-harm, hate speech, or dangerous instructions (e.g. explosive synthesis).
- Hallucinations can inadvertently generate toxic or defamatory text.

Output moderation acts as the **final defensive firewall** between the model and the user.

---

## 2. Moderation Workflow

```
Model Generates Answer
         │
         ▼
[app.security.moderate()]
         │
         ├─ Flagged == False ──► Return answer to user
         │
         └─ Flagged == True  ──► 1. Suppress toxic answer
                                 2. Return safe generic refusal
                                 3. Log incident for administrator review
```

---

## 3. Safe Degradation

When an output is flagged, the user receives an informative, non-accusatory refusal:
*"I am unable to display this response as it violates educational safety policies. Please feel free to ask another academic question."*
This prevents legal liability, ensures school safety compliance, and preserves student trust.
