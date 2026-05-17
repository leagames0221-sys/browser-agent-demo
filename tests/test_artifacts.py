"""Schema integrity checks for committed baseline-run evidence.

The five baseline_*.json files under artifacts/ are honest-failure records
documenting each of the 5 progressive defense layers (v1 rogue navigation,
v2 fabrication, v3 attractor return, v4 plan ignored, v5 frontier
token-cap). The portfolio thesis depends on these records remaining
parseable and carrying the minimum identifying fields. These checks
enforce that invariant.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REQUIRED_KEYS = {"task" if False else "model"}  # 'model' is the universal field


def _artifact_files(repo_root: Path) -> list[Path]:
    artifacts = repo_root / "artifacts"
    return sorted(p for p in artifacts.glob("baseline*.json") if p.is_file())


def test_artifacts_dir_populated(repo_root: Path) -> None:
    files = _artifact_files(repo_root)
    assert files, "artifacts/ must contain baseline*.json evidence"


@pytest.mark.parametrize(
    "artifact_path",
    _artifact_files(Path(__file__).resolve().parent.parent),
    ids=lambda p: p.name,
)
def test_artifact_is_valid_json(artifact_path: Path) -> None:
    with artifact_path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"{artifact_path.name}: top-level must be object"


@pytest.mark.parametrize(
    "artifact_path",
    _artifact_files(Path(__file__).resolve().parent.parent),
    ids=lambda p: p.name,
)
def test_artifact_has_model_field(artifact_path: Path) -> None:
    with artifact_path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert "model" in data, f"{artifact_path.name}: missing 'model' field"


@pytest.mark.parametrize(
    "artifact_path",
    _artifact_files(Path(__file__).resolve().parent.parent),
    ids=lambda p: p.name,
)
def test_artifact_run_terminated(artifact_path: Path) -> None:
    """Each baseline run must record an outcome — either is_done flag, a
    final_result string, or both. Open-ended runs would invalidate the
    honest-failure narrative."""
    with artifact_path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert "is_done" in data or "final_result" in data, (
        f"{artifact_path.name}: must record run outcome (is_done or final_result)"
    )
