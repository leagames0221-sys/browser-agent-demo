"""Example runners must parse cleanly. Import-time execution requires
Ollama + Chrome profile + browser-use, so we stop at AST-level parse — the
cheapest gate that catches typos, syntax errors, and broken edits.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def _example_files() -> list[Path]:
    if not EXAMPLES_DIR.is_dir():
        return []
    return sorted(p for p in EXAMPLES_DIR.glob("baseline*.py") if p.is_file())


def test_examples_dir_populated() -> None:
    assert _example_files(), "examples/ must contain at least one baseline runner"


@pytest.mark.parametrize("example_path", _example_files(), ids=lambda p: p.name)
def test_example_parses_cleanly(example_path: Path) -> None:
    source = example_path.read_text(encoding="utf-8")
    ast.parse(source, filename=str(example_path))
