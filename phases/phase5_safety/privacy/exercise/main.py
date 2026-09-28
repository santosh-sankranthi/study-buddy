"""EXERCISE -- International Phone PII Scrubbing.

The demo scrubbed US phone numbers and emails.
Your twist: implement scrub_international_phone(text: str) -> tuple[str, list[str]]
to detect and scrub Indian (+91) and UK (+44) mobile phone numbers.

Run when done:
    python phases/phase5_safety/privacy/solution/check.py
"""
# TODO(1): Implement scrub_international_phone(text: str) -> tuple[str, list[str]]
def scrub_international_phone(text: str) -> tuple[str, list[str]]:
    raise NotImplementedError("TODO(1): implement scrub_international_phone")

if __name__ == "__main__":
    print(scrub_international_phone("Reach me at +91 9876543210 please."))
