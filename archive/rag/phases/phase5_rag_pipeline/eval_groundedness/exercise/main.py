"""EXERCISE -- Deterministic RAG Verification.

The demo used an LLM judge.
Your twist: implement verify_rag_answer() and evaluate_rag_test_suite()
performing deterministic checks on length and citation presence.

Run when done:
    python phases/phase5_rag_pipeline/eval_groundedness/solution/check.py
"""
# TODO(1): Implement verify_rag_answer(answer: str) -> dict
def verify_rag_answer(answer: str) -> dict:
    raise NotImplementedError("TODO(1): implement verify_rag_answer")

# TODO(2): Implement evaluate_rag_test_suite() -> dict[str, bool]
def evaluate_rag_test_suite() -> dict[str, bool]:
    raise NotImplementedError("TODO(2): implement evaluate_rag_test_suite")

if __name__ == "__main__":
    print(evaluate_rag_test_suite())
