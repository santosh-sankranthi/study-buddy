"""EXERCISE -- Output Content Moderation.

The demo moderated user input.
Your twist: implement moderate_assistant_output(answer: str) -> dict
to verify the assistant response does not violate content policies.

Run when done:
    python phases/phase8_safety/moderation/solution/check.py
"""
# TODO(1): Implement moderate_assistant_output(answer: str) -> dict
# Return {"flagged": bool, "status": "APPROVED" | "BLOCKED"}
def moderate_assistant_output(answer: str) -> dict:
    raise NotImplementedError("TODO(1): implement moderate_assistant_output")

if __name__ == "__main__":
    print(moderate_assistant_output("Photosynthesis occurs in chloroplasts."))
