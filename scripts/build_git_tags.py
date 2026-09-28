"""Rebuild the curriculum's git tags as *real*, diffable commits.

The workshop teaches by `git diff` between tags, so every tag must point at a
commit whose tree actually differs. This script constructs those trees with git
plumbing (no working-tree changes, no branch history pollution) and force-moves
the tags onto them.

Two tag families are produced:

* **Version tags** ``v0``..``v8`` — same tree as the base commit, but
  ``app/main.py`` replaced by that milestone from ``app/versions/vN/main.py``.
  ``git checkout v4`` therefore gives a working RAG app.

* **Concept tags** ``p<phase>-<concept>-<beat>`` — a *progressive* tree: every
  concept up to the current one is present, all later concepts are removed. For
  the current concept, ``exercise`` hides ``demo/`` and ``solution/``, ``demo``
  hides only ``solution/``, and ``solution`` hides nothing. That makes

      git diff p5-retrieval-exercise p5-retrieval-solution

  show exactly the answer the instructor revealed.

Usage::

    python scripts/build_git_tags.py            # rebuild from HEAD
    python scripts/build_git_tags.py --base v8  # rebuild from another ref
    python scripts/build_git_tags.py --dry-run  # print what would be tagged
"""

from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES_DIR = REPO_ROOT / "phases"
VERSIONS_DIR = REPO_ROOT / "app" / "versions"

BEATS = ("exercise", "demo", "solution")

# Canonical teaching order. Any concept directory not listed is appended at the
# end of its phase (so the extra generated concepts still get coherent tags).
CONCEPT_ORDER: dict[int, list[str]] = {
    0: ["tokens", "context_window", "training_vs_inference", "sampling"],
    1: ["system_prompts", "few_shot_zero_shot", "cot", "structured_output",
        "function_calling_concept", "react_concept"],
    2: ["context_sources", "memory", "context_compaction", "long_context",
        "context_security", "mcp_concept"],
    3: ["vector_representations", "embedding_models", "semantic_search"],
    4: ["indexing", "similarity_search"],
    5: ["chunking", "embedding", "indexing", "retrieval", "grounded_generation",
        "eval_groundedness"],
    6: ["tools", "function_calling_live", "react_loop", "agent_loops",
        "agent_safety", "multi_agent"],
    7: ["servers", "tools_resources", "clients", "hosts"],
    8: ["prompt_injection", "rag_isolation", "privacy", "bias", "moderation",
        "adversarial_testing"],
    9: ["deterministic_evals", "model_based_evals", "human_evals",
        "metrics_regression", "tracing", "production_monitoring"],
}

# Phase -> app milestone used by that phase's concept tags.
PHASE_VERSION = {0: "v0", 1: "v1", 2: "v2", 3: "v3", 4: "v3",
                 5: "v4", 6: "v5", 7: "v6", 8: "v7", 9: "v8"}


def git(*args: str, index: str | None = None, check: bool = True) -> str:
    env = os.environ.copy()
    if index is not None:
        env["GIT_INDEX_FILE"] = index
    result = subprocess.run(
        ["git", *args], cwd=REPO_ROOT, env=env,
        capture_output=True, text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout.strip()


def phase_number(phase_dir: Path) -> int | None:
    name = phase_dir.name
    if not name.startswith("phase"):
        return None
    digits = ""
    for ch in name[5:]:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else None


def ordered_concepts() -> list[tuple[int, Path]]:
    """[(phase_number, concept_dir)] in canonical teaching order."""
    result: list[tuple[int, Path]] = []
    for phase_dir in sorted(PHASES_DIR.iterdir()):
        if not phase_dir.is_dir():
            continue
        num = phase_number(phase_dir)
        if num is None:
            continue
        present = [c for c in phase_dir.iterdir() if c.is_dir() and not c.name.startswith("__")]
        by_name = {c.name: c for c in present}
        ordered = [by_name[n] for n in CONCEPT_ORDER.get(num, []) if n in by_name]
        for name in sorted(by_name):
            if name not in CONCEPT_ORDER.get(num, []):
                ordered.append(by_name[name])
        result.extend((num, c) for c in ordered)
    return result


def beats_for(concept_dir: Path) -> list[str]:
    """Beats that actually contain files (ignore stray empty directories)."""
    return [
        b for b in BEATS
        if (concept_dir / b).is_dir()
        and any(p.is_file() for p in (concept_dir / b).rglob("*"))
    ]


def build_tree(index: str, base: str, version: str | None,
               remove: list[Path]) -> str:
    git("read-tree", base, index=index)
    if version is not None:
        blob = git("hash-object", "-w", str(VERSIONS_DIR / version / "main.py"))
        git("update-index", "--cacheinfo", f"100644,{blob},app/main.py", index=index)
    if remove:
        rels = [str(p.relative_to(REPO_ROOT)) for p in remove]
        git("rm", "-r", "--cached", "--quiet", "--ignore-unmatch", *rels, index=index)
    return git("write-tree", index=index)


def make_commit(tree: str, base: str, message: str) -> str:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Study Buddy Curriculum")
    env.setdefault("GIT_AUTHOR_EMAIL", "curriculum@study-buddy.local")
    env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
    env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
    result = subprocess.run(
        ["git", "commit-tree", tree, "-p", base, "-m", message],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"commit-tree failed:\n{result.stderr}")
    return result.stdout.strip()


def tag(name: str, commit: str, message: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  would tag {name} -> {commit[:10]}")
        return
    git("tag", "-f", "-a", name, commit, "-m", message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD", help="base ref to build trees from")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    base = git("rev-parse", args.base)

    with tempfile.TemporaryDirectory() as tmp:
        index = str(Path(tmp) / "index")

        # ── Version tags ─────────────────────────────────────────────────────
        print("Version tags:")
        for level in range(0, 9):
            version = f"v{level}"
            tree = build_tree(index, base, version, remove=[])
            commit = make_commit(tree, base, f"{version}: app/main.py milestone")
            tag(version, commit, f"Study Buddy {version}", args.dry_run)

        # ── Concept tags (progressive) ───────────────────────────────────────
        concepts = ordered_concepts()
        print(f"Concept tags ({len(concepts)} concepts):")
        for i, (phase, concept_dir) in enumerate(concepts):
            beats = beats_for(concept_dir)
            if not beats:
                continue
            version = PHASE_VERSION[phase]

            # Later concepts do not exist yet in this tag's tree.
            later = [c for (_, c) in concepts[i + 1:]]
            rel = concept_dir.relative_to(REPO_ROOT)

            for beat in beats:
                remove = list(later)
                if beat == "exercise":
                    remove += [concept_dir / "demo", concept_dir / "solution"]
                elif beat == "demo":
                    remove += [concept_dir / "solution"]
                # beat == "solution": keep everything in this concept

                name = f"p{phase}-{concept_dir.name}-{beat}"
                tree = build_tree(index, base, version, remove=remove)
                commit = make_commit(
                    tree, base,
                    f"{name}: {concept_dir.name} ({beat}) at app milestone {version}",
                )
                tag(name, commit, f"{name}", args.dry_run)

    print("Done." + (" (dry run — no tags changed)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
