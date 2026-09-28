"""Pytest harness for the curriculum self-checks.

Every concept ships a ``solution/check.py`` that students run directly:

    python phases/<phase>/<concept>/solution/check.py
    python phases/<phase>/<concept>/solution/check.py --solution

Those scripts are ordinary programs (they call ``main()`` and use argparse at
module import), not pytest test functions, so pytest cannot collect them by
default. This conftest teaches pytest to run each ``check.py`` as a single test,
and splits them into two groups:

* **offline** checks (pure logic: token counts, cosine math, chunkers, file
  parsing) run on a plain ``pytest`` -- fast and free.
* **llm** checks (they call OpenRouter / embeddings / the agent) are skipped
  unless you pass ``--run-llm-checks`` or select them explicitly with
  ``-m llm``. This keeps ``pytest`` from burning the free-tier quota by default.

Run everything, including the live-LLM checks::

    pytest --run-llm-checks
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# Substrings that mark a check as hitting the network / an LLM. Chosen to match
# the imported helper names used across the curriculum.
_LLM_HINTS = (
    "chat(",
    "OpenAI",
    "embed(",
    "embed_batch",
    "semantic_search",
    "retrieve(",
    "index_document",
    "agent_loop",
    "plan_and_execute",
    "moderate(",
    "check_groundedness",
    "llm_judge",
    "list_mcp_tools",
    "call_mcp_tool",
    "moderation",
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-llm-checks",
        action="store_true",
        default=False,
        help="also run self-checks that make live LLM / embedding calls",
    )
    parser.addoption(
        "--check-exercises",
        action="store_true",
        default=False,
        help="check the student exercise skeletons instead of the reference solutions",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "llm: self-check makes a live LLM/embedding call")


def _source_for(target: Path) -> str:
    """Text used to decide whether a check is an LLM check.

    Looks at the check itself plus the exercise/solution ``main.py`` it imports.
    """
    chunks = []
    for path in (target, target.parent.parent / "exercise" / "main.py",
                 target.parent.parent / "solution" / "main.py"):
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except OSError:
            pass
    return "\n".join(chunks)


def _is_llm(target: Path) -> bool:
    text = _source_for(target)
    return any(hint in text for hint in _LLM_HINTS)


def pytest_collect_file(file_path: Path, parent: pytest.Collector):
    if file_path.name == "check.py":
        return SelfCheckFile.from_parent(parent, path=file_path)
    return None


class SelfCheckFile(pytest.File):
    def collect(self):
        target = Path(str(self.path))
        item = SelfCheckItem.from_parent(self, name="selfcheck", target=target)
        if _is_llm(target):
            item.add_marker(pytest.mark.llm)
        yield item


class SelfCheckItem(pytest.Item):
    def __init__(self, *, target: Path, **kwargs):
        super().__init__(**kwargs)
        self.target = target

    def runtest(self) -> None:
        if self.get_closest_marker("llm") and not self.config.getoption("run_llm_checks"):
            pytest.skip("live LLM check (rerun with --run-llm-checks)")

        source = self.target.read_text(encoding="utf-8")
        exercises = self.config.getoption("check_exercises")
        argv = [str(self.target)]
        # Most checks accept --solution. By default pytest verifies the reference
        # answer (skeletons are meant to fail until a student fills them in).
        if "--solution" in source and not exercises:
            argv.append("--solution")

        module_name = f"selfcheck_{self.target.parent.parent.parent.name}_{self.target.parent.parent.name}"
        spec = importlib.util.spec_from_file_location(module_name, self.target)
        assert spec and spec.loader, f"could not import {self.target}"
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        # The checks use argparse; give it a clean argv so pytest's own args
        # are never parsed as check flags.
        saved_argv = sys.argv
        sys.argv = argv
        try:
            spec.loader.exec_module(module)  # module-level checks run here
            if hasattr(module, "main"):
                result = module.main()          # checks that wrap in main()
                assert result in (0, None), f"{self.target} returned {result!r}"
        finally:
            sys.argv = saved_argv

    def repr_failure(self, excinfo, style=None):
        return f"self-check failed: {self.target}\n{excinfo.getrepr(style=style)}"

    def reportinfo(self):
        return self.path, 0, f"self-check: {self.target}"
