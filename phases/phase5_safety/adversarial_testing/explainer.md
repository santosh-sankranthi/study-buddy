# 5.5 — Adversarial Red-Teaming

## What was broken before
Standard unit tests check the "happy path" (correct queries, friendly questions). Attackers specifically target the boundaries — attempting to make agents enter infinite loops, call unauthorized tools, or disclose system prompts.

## How it works
Adversarial testing crafts inputs designed to induce system failure. Automated regression tests verify that your defenses (sanitizers, step caps, tool authorization checks) catch these exploits reliably.
