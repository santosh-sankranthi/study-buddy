"""DEMO -- Wiring Tool Registry for Execution.

The instructor demonstrates registering real Python functions into TOOL_REGISTRY.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOL_REGISTRY, get_exam_schedule, search_notes

print("Registered tools in TOOL_REGISTRY:")
for name, fn in TOOL_REGISTRY.items():
    print(f"  • {name}: {fn.__doc__.strip().splitlines()[0] if fn.__doc__ else 'callable'}")

# Test invoking directly through the registry
print("
Testing get_exam_schedule directly:")
print("  Result:", TOOL_REGISTRY["get_exam_schedule"](subject="biology"))
