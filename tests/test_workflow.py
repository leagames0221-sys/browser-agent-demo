"""Drift-check workflow integrity — the workflow backs every README claim.
If it is malformed or missing the gates, the rest of the discipline
collapses silently.
"""
from __future__ import annotations

from pathlib import Path

WORKFLOW_REL = Path(".github/workflows/drift-check.yml")

REQUIRED_STEP_MARKERS = (
    "Verify LICENSE is MIT",
    "Verify Memory Bank has 5 Cline-pattern files",
    "Verify drift-check workflow self-reference",
    "Verify pyproject.toml exists",
)


def test_workflow_file_exists(repo_root: Path) -> None:
    assert (repo_root / WORKFLOW_REL).is_file()


def test_workflow_has_required_top_level_keys(repo_root: Path) -> None:
    body = (repo_root / WORKFLOW_REL).read_text(encoding="utf-8")
    for key in ("name:", "on:", "jobs:", "runs-on:"):
        assert key in body, f"drift-check.yml missing top-level key {key!r}"


def test_workflow_declares_required_gates(repo_root: Path) -> None:
    body = (repo_root / WORKFLOW_REL).read_text(encoding="utf-8")
    for marker in REQUIRED_STEP_MARKERS:
        assert marker in body, f"drift-check.yml missing gate: {marker!r}"
