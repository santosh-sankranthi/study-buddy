# PII Scrubbing & Data Privacy Compliance

> **Time:** ~2 min read | **Goal:** Redact sensitive personal data (emails, phones, financial records) before text is forwarded to external APIs or stored in vector databases.

---

## 1. Why Scrub PII?

Under global privacy regulations (GDPR, FERPA, CCPA, HIPAA), personal identifiers must not be leaked:
1. **Third-Party Model Providers:** Forwarding student emails, phone numbers, or grades to commercial LLM APIs can breach student data privacy agreements.
2. **Shared Vector Databases:** If one student uploads course notes containing another student's phone number or home address, semantic search might inadvertently retrieve and display that PII to other students.

---

## 2. Redaction Architecture

Before text enters any embedding or generation pipeline, it passes through the PII sanitizer:

```
Raw Input: "My email is alice@school.edu and my phone is +1-555-123-4567."
                                 │
                                 ▼
                         [Regex Scrubbing]
                                 │
                                 ▼
Clean Text: "My email is [EMAIL_REDACTED] and my phone is [PHONE_US_REDACTED]."
```

Detected PII types are logged for audit compliance (`["EMAIL", "PHONE_US"]`).

---

## 3. Global Formats

In `app/security.py`, `_PII_PATTERNS` supports:
- `EMAIL`: Standard RFC email addresses
- `PHONE_US`: Standard North American phone formats
- `CC`: 15-16 digit credit card sequences
- `PHONE_IN`: Indian phone numbers (`+91 ...`)
- `PHONE_UK`: UK phone numbers (`+44 ...`)
