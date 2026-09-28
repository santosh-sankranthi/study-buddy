# Phase 8 Instructor Guide: AI Safety, Security & Red-Teaming

## Learning Objectives
1. Demonstrate indirect prompt injection via poisoned RAG notes.
2. Neutralize injection using untrusted context fencing (`[RETRIEVED CONTEXT]`).
3. Scrub sensitive PII (emails, phone numbers, credit cards) before inference.
4. Apply two-way content moderation (input and output).
5. Conduct adversarial red-teaming against agent loops and tool dispatchers.

## Timing & Pacing (Total: 50 min)
- **8.1 Prompt Injection (15 min)**: Demonstrate RAG hijack with `injected.md`; apply data fences.
- **8.2 Privacy / PII (10 min)**: Regex scrubbing of international phone numbers and emails.
- **8.3 Bias (8 min)**: Individual observation of demographic framing differences.
- **8.4 Moderation (7 min)**: Two-way input/output moderation checking.
- **8.5 Adversarial Testing (10 min)**: Write tests verifying defense against infinite loops & unauthorized tools.
