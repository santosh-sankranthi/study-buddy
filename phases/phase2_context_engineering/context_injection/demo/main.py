"""DEMO -- Context Sources and Context Reporting.

Live-code target: construct a multi-part prompt (system + injected metadata + history + query),
compute the token breakdown using app.context.context_report, and observe token distribution.

Run:
    python phases/phase2_context_engineering/context_injection/demo/main.py
"""

from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.context import context_report
from app.prompts import TUTOR_SYSTEM_PROMPT

print("=" * 60)
print("CONTEXT BREAKDOWN DEMO")
print("=" * 60)

# 1. Base prompt without dynamic metadata
base_messages = [
    {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
    {"role": "user", "content": "Can you explain cell division?"},
]
rep_base = context_report(base_messages)
print("\nBase Message Tokens:")
for role, cnt in rep_base.items():
    print(f"  {role:10s}: {cnt} tokens")

# 2. Injected metadata (date + student name)
today = datetime.now().strftime("%A, %B %d, %Y")
student_name = "Alice"
injected_system = (
    f"Today is {today}.\n"
    f"The student's name is {student_name}.\n"
    f"{TUTOR_SYSTEM_PROMPT}"
)

injected_messages = [
    {"role": "system", "content": injected_system},
    {"role": "user", "content": "Can you explain cell division?"},
]
rep_injected = context_report(injected_messages)
print("\nInjected Message Tokens:")
for role, cnt in rep_injected.items():
    print(f"  {role:10s}: {cnt} tokens")

delta = rep_injected["system"] - rep_base["system"]
print(f"\nMetadata injection added: +{delta} tokens to 'system' context")
