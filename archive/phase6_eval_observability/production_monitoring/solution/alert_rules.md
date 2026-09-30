# Production Monitoring Alert Rules

Alert: cost_per_session_usd
Threshold: > $0.10 per session
Why: Free tier and educational budgets have daily caps; runaway agent loops could exhaust quotas.

Alert: latency_p99_ms
Threshold: > 5000 ms
Why: Students abandon tutoring sessions if responses take longer than 5 seconds.

Alert: judge_pass_rate
Threshold: < 0.85
Why: A drop below 85% on the quality judge indicates answer quality is drifting after a prompt or model change.
