"""Generate the sequential paste guide for the live workshop.

For each app upgrade (v0->v1, v1->v2, ...) this emits:

* the exact `git diff` of `app/main.py` (so you paste exactly what ships),
* a `.patch` you can `git apply` if a live paste goes wrong,
* the list of concepts to explain at that step,
* the `git checkout vN` to run in the read-only showcase clone.

Output: ``workshop/PASTE_GUIDE.md`` and ``workshop/patches/stepN.patch``.

Run:  python scripts/build_workshop_guide.py
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDE_DIR = REPO_ROOT / "workshop"
PATCH_DIR = GUIDE_DIR / "patches"

# Each step is one app upgrade. `core` marks the 2.5-hour workshop path.
STEPS = [
    dict(n=1, frm="v0", to="v1", phase="Phase 1 — Prompt Engineering", core=True,
         concepts=[
             ("System prompts", "`build_system()` prepends a persona; the model stops sounding random.", "ask()"),
             ("Chain of thought", "Optional 'think step by step' + `<thinking>` / `<answer>` splitting.", "ask()"),
             ("Few-shot", "Two worked examples fix the format of `/quiz-item`.", "QUIZ_EXAMPLES + /quiz-item"),
             ("Structured output", "Pydantic validates the model's JSON in `/flashcards` and `/study-plan`.", "/flashcards, /study-plan"),
             ("Tool schemas", "`/tools` publishes the JSON tool contracts — no execution yet.", "/tools, /modes"),
         ]),
    dict(n=2, frm="v1", to="v2", phase="Phase 2 — Context Engineering", core=True,
         concepts=[
             ("Context sources", "`context_report()` shows where every token goes.", "ask() + /context-report"),
             ("Memory", "Session history is reloaded each turn so it remembers.", "ask() + /session/{id}"),
             ("Context compaction", "Long history is summarised instead of overflowing.", "ask()"),
             ("Compaction on demand", "Type `/compact` in the chat to summarise the session and watch the token count drop.", "POST /session/{id}/compact"),
             ("Long context", "Measure latency/cost as the document grows.", "/measure-long-context"),
             ("Context security", "Obvious injection is stripped before it reaches the model.", "sanitize (Phase 2 light pass)"),
         ]),
    dict(n=3, frm="v2", to="v3", phase="Phase 3 — Agents & Tools", core=True,
         concepts=[
             ("Tools + function calling", "Real functions in `TOOL_REGISTRY` are executed.", "/agent/ask"),
             ("ReAct loop", "Think → act → observe, with a visible trace.", "/agent/ask"),
             ("Agent loops", "Stop conditions: step cap + repeat detection.", "app/agent.py"),
             ("Multi-agent", "Planner → executor → critic.", "/agent/plan-and-execute"),
         ]),
    dict(n=4, frm="v3", to="v4", phase="Phase 4 — MCP", core=False,
         concepts=[
             ("Servers / tools / resources", "Tools and the notes corpus exposed over MCP.", "mcp_server/server.py"),
             ("Clients", "Study Buddy discovers tools via `/mcp/tools`.", "/mcp/tools"),
         ]),
    dict(n=5, frm="v4", to="v5", phase="Phase 5 — AI Safety", core=False,
         concepts=[
             ("Prompt injection", "Obvious injections are stripped before the model sees them.", "ask()"),
             ("Privacy", "Emails / phones / cards are redacted before sending.", "ask()"),
             ("Moderation", "Input and output are checked by `moderate()`.", "ask()"),
         ]),
    dict(n=6, frm="v5", to="v6", phase="Phase 6 — Evaluation & Observability", core=False,
         concepts=[
             ("Regression report", "A built-in eval set scored against the running app.", "/eval/regression-report"),
         ]),
]


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout


def main() -> None:
    GUIDE_DIR.mkdir(exist_ok=True)
    PATCH_DIR.mkdir(exist_ok=True)

    out: list[str] = []
    out.append("# Study Buddy — Live Workshop Paste Guide\n")
    out.append(
        "Two clones of this repo: **Clone A (typing)** and **Clone B (showcase)**.\n\n"
        "- Clone A: `git switch -c live v0` — this is where you paste, step by step. Never switch it.\n"
        "- Clone B: read-only; run `git checkout vN` here to show the finished result of each step.\n"
        "- Both: `pip install -r requirements.txt` once, and copy `.env` with your key.\n"
        "- Before each run: `python scripts/workshop_reset.py` to clear session state.\n\n"
        "Each step below shows the **exact diff** of `app/main.py`. Type the `+` lines into "
        "Clone A. If a live paste goes wrong, run the matching `workshop/patches/stepN.patch` "
        "with `git apply`. Concepts are numbered so you can explain as you paste.\n"
    )

    for step in STEPS:
        frm, to, n = step["frm"], step["to"], step["n"]
        diff = git("diff", "--no-color", frm, to, "--", "app/main.py")
        patch_path = PATCH_DIR / f"step{n}.patch"
        patch_path.write_text(git("diff", frm, to, "--", "app/main.py"), encoding="utf-8")

        tag = "  ⭐ CORE (2.5h path)" if step["core"] else "  (extension)"
        out.append(f"\n---\n\n## Step {n} — {step['phase']}{tag}\n")
        out.append(f"**Clone A:** paste the changes below into `app/main.py`.\n")
        out.append(f"**Clone B:** `git checkout {to}`\n")
        out.append(f"**Fallback:** `git apply workshop/patches/step{n}.patch`\n")
        out.append("\n### Concepts to explain while you paste\n")
        for i, (name, why, where) in enumerate(step["concepts"], 1):
            out.append(f"{i}. **{name}** (`{where}`) — {why}\n")
        out.append(f"\n### The exact change (`app/main.py`)\n")
        out.append("```diff\n" + diff.rstrip("\n") + "\n```\n")

    out.append(
        "\n---\n\n## Show the product was built sequentially\n\n"
        "```bash\n"
        "git diff v0 v3 -- app/main.py     # what the first three steps added, together\n"
        "git log --oneline v0..v3          # (tags are snapshots, not a linear log)\n"
        "```\n\n"
        "At the end: `git checkout v6` in Clone B to preview everything beyond the core "
        "(MCP, safety, evals).\n"
    )

    guide = GUIDE_DIR / "PASTE_GUIDE.md"
    guide.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {guide.relative_to(REPO_ROOT)}")
    print(f"wrote {len(STEPS)} patches to {PATCH_DIR.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
