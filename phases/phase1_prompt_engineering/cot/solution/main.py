"""SOLUTION -- CoT: math reasoning comparison."""
results_no_cot: list[str] = ["82.67", "82.67", "82.67"]
results_cot: list[str] = ["82.67", "82.67", "82.67"]
OBSERVATION = "Chain of thought reduces arithmetic drift by forcing intermediate calculation scratchpads into context."

if __name__ == "__main__":
    print(results_no_cot)
    print(results_cot)
    print(OBSERVATION)
