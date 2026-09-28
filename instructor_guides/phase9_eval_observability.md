# Phase 9 Instructor Guide: Evaluation & Observability

## Learning Objectives
1. Build deterministic test suites for schema validation and response boundaries.
2. Implement model-based evaluation using LLM-as-a-judge with structured criteria.
3. Calibrate human evaluation rubrics across pedagogical dimensions.
4. Track regression test pass-rate deltas across prompt modifications.
5. Trace per-request latency, token consumption, and dollar costs.
6. Formulate operational production alerts for cost, latency, and groundedness.

## Timing & Pacing (Total: 55 min)
- **9.1 Deterministic Evals (10 min)**: Pytest checks on schema and topics.
- **9.2 Model-Based Evals (12 min)**: LLM judge scoring tone on a 1-5 scale.
- **9.3 Human Evals (10 min)**: Group rubric calibration across 5 samples.
- **9.4 Metrics & Regression (10 min)**: Run 10-item eval suite before/after prompt change.
- **9.5 Tracing & Cost (8 min)**: Analyze span breakdowns from trace reports.
- **9.6 Production Monitoring (5 min)**: Operational alert definitions.
