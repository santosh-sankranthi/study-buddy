"""SOLUTION -- Deterministic RAG Verification."""
def verify_rag_answer(answer: str) -> dict:
    words = answer.strip().split()
    word_count = len(words)
    has_citation = "[Source:" in answer or "Source:" in answer
    passed = (word_count > 0) and (word_count <= 150) and has_citation
    return {
        "passed": passed,
        "word_count": word_count,
        "has_citation": has_citation,
    }

def evaluate_rag_test_suite() -> dict[str, bool]:
    good = "Chlorophyll absorbs blue and red wavelengths. [Source: photosynthesis.md]"
    bad = "I think it is green light."
    return {
        "good_answer_passed": verify_rag_answer(good)["passed"],
        "bad_answer_failed": not verify_rag_answer(bad)["passed"],
    }

if __name__ == "__main__":
    print(evaluate_rag_test_suite())
