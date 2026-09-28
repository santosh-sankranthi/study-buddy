"""EXERCISE -- Registering a Tool Schema.

The demo inspected the tool schemas in app/tools.py.
Your twist: verify and inspect the calculate_grade tool schema in app/tools.py,
ensuring it defines scores and weights arrays and marks them as required.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/function_calling_concept/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOLS


def find_tool(name: str) -> dict | None:
    """Find a tool by name in the TOOLS list."""
    for tool in TOOLS:
        if tool.get("function", {}).get("name") == name:
            return tool
    return None


# ── TODO(1): Locate the calculate_grade schema ───────────────────────────────
def get_calculate_grade_schema() -> dict:
    """Return the calculate_grade tool schema dict from TOOLS."""
    tool = find_tool("calculate_grade")
    assert tool is not None, "calculate_grade not found in TOOLS!"
    return tool


# ── TODO(2): Inspect required properties of calculate_grade ─────────────────
def get_required_fields() -> list[str]:
    """Return the list of required field names for calculate_grade."""
    tool = get_calculate_grade_schema()
    params = tool["function"]["parameters"]
    return params.get("required", [])


# ── TODO(3): Check property types ───────────────────────────────────────────
def check_property_types() -> dict[str, str]:
    """Return a mapping of property name -> type (e.g. {'scores': 'array', 'weights': 'array'})."""
    tool = get_calculate_grade_schema()
    props = tool["function"]["parameters"]["properties"]
    return {k: v.get("type", "") for k, v in props.items()}


if __name__ == "__main__":
    tool = get_calculate_grade_schema()
    print("Found calculate_grade schema:")
    print("  Description:", tool["function"]["description"])
    req = get_required_fields()
    print("  Required:", req)
    types = check_property_types()
    print("  Properties:", types)
