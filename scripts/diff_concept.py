#!/usr/bin/env python3
"""diff_concept.py — Inspect the diff between exercise skeleton and solution.

Usage:
    python scripts/diff_concept.py <concept_name>
    python scripts/diff_concept.py <phase_number_or_prefix> <concept_name>

Examples:
    python scripts/diff_concept.py tokens
    python scripts/diff_concept.py p0 tokens
    python scripts/diff_concept.py p6 react_loop
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = REPO_ROOT / "phases"


def find_concept_dir(query: str, phase_filter: str = None) -> Path:
    query = query.lower().strip()
    candidates = []

    for phase_dir in sorted(PHASES_DIR.iterdir()):
        if not phase_dir.is_dir() or not phase_dir.name.startswith("phase"):
            continue
        if phase_filter:
            pf = phase_filter.lower().strip()
            if not (phase_dir.name.startswith(f"phase{pf}") or phase_dir.name == pf or f"phase_{pf}" in phase_dir.name):
                # allow e.g. "p0" or "0"
                num = pf.replace("p", "").replace("phase", "")
                if not phase_dir.name.startswith(f"phase{num}"):
                    continue

        for concept_dir in sorted(phase_dir.iterdir()):
            if not concept_dir.is_dir():
                continue
            cname = concept_dir.name.lower()
            if query == cname or query in cname:
                candidates.append(concept_dir)

    if not candidates:
        print(f"Error: Concept '{query}' not found" + (f" in phase '{phase_filter}'" if phase_filter else "") + ".")
        sys.exit(1)

    if len(candidates) > 1:
        # Check for exact match
        exact = [c for c in candidates if c.name.lower() == query]
        if len(exact) == 1:
            return exact[0]
        print(f"Multiple matches found for '{query}':")
        for c in candidates:
            rel = c.relative_to(REPO_ROOT)
            print(f"  - {rel}")
        print("Please be more specific or specify the phase.")
        sys.exit(1)

    return candidates[0]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if len(sys.argv) == 2:
        concept_dir = find_concept_dir(sys.argv[1])
    else:
        concept_dir = find_concept_dir(sys.argv[2], phase_filter=sys.argv[1])

    exercise_dir = concept_dir / "exercise"
    solution_dir = concept_dir / "solution"

    if not exercise_dir.exists() or not solution_dir.exists():
        print(f"Error: Missing exercise/ or solution/ directory in {concept_dir.relative_to(REPO_ROOT)}")
        sys.exit(1)

    # Find matching files to diff
    # Usually main.py, or markdown files
    exercise_files = list(exercise_dir.glob("*.py")) + list(exercise_dir.glob("*.md"))
    if not exercise_files:
        print(f"No exercise files found in {exercise_dir.relative_to(REPO_ROOT)}")
        sys.exit(1)

    for ex_file in exercise_files:
        sol_file = solution_dir / ex_file.name
        if not sol_file.exists():
            continue
        print(f"================================================================================")
        print(f"Diff: {ex_file.relative_to(REPO_ROOT)} -> {sol_file.relative_to(REPO_ROOT)}")
        print(f"================================================================================")
        cmd = ["git", "diff", "--no-index", "--color=always", str(ex_file), str(sol_file)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(res.stdout)


if __name__ == "__main__":
    main()
