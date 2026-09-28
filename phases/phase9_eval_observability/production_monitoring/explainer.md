# 9.6 — Production Monitoring & Alerting

## What was broken before
Passing evals at deployment does not guarantee safety or uptime in production. Upstream LLM providers degrade, rate limits trigger, and anomalous user prompts can cause cost or latency blowouts.

## How it works
Define production SLIs (Service Level Indicators) and alert thresholds covering:
1. Cost per session (budget overrun defense)
2. p99 latency (user drop-off defense)
3. Groundedness / hallucination rate (accuracy defense)
