"""SOLUTION -- International Phone PII Scrubbing."""
import re

PATTERNS = {
    "PHONE_IN": r"\+91[\s\-]?\d{10}",
    "PHONE_UK": r"\+44[\s\-]?\d{10}",
}

def scrub_international_phone(text: str) -> tuple[str, list[str]]:
    detected = []
    for label, pat in PATTERNS.items():
        if re.search(pat, text):
            detected.append(label)
            text = re.sub(pat, f"[{label}_REDACTED]", text)
    return text, detected

if __name__ == "__main__":
    print(scrub_international_phone("Reach me at +91 9876543210 please."))
