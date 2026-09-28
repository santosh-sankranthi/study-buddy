"""DEMO -- Function Calling (Tool Schemas).

Live-code target: examine standard OpenAI/OpenRouter tool schemas in app/tools.py,
understand the schema structure, and inspect how schemas specify required parameters.
Finally, verify that tools are accessible via GET /tools.

Run:
    python phases/phase1_prompt_engineering/function_calling_concept/demo/main.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOLS

print("=" * 60)
print("REGISTERED TOOL SCHEMAS IN app/tools.py")
print("=" * 60)

for tool in TOOLS:
    fn = tool["function"]
    name = fn["name"]
    desc = fn["description"]
    params = fn["parameters"]
    required = params.get("required", [])
    print(f"\nTool: {name}")
    print(f"  Description: {desc}")
    print(f"  Parameters:  {list(params.get('properties', {}).keys())}")
    print(f"  Required:    {required}")

print("\nFull JSON schema for search_notes:")
search_tool = next(t for t in TOOLS if t["function"]["name"] == "search_notes")
print(json.dumps(search_tool, indent=2))

print("\n" + "=" * 60)
print("Next: in the exercise, you will add calculate_grade to TOOLS.")
print("=" * 60)
