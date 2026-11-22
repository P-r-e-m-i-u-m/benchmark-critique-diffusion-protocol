from __future__ import annotations

import csv
import json
import sys

import pytest


def _run(monkeypatch, *argv: str) -> int:
    import sample_frame

    monkeypatch.setattr(sys, "argv", ["sample_frame.py", *argv])
    return sample_frame.main()


def test_largest_remainder_allocates_exactly():
    import sample_frame

    populations = {"2022": 2, "2023": 100, "2024": 50, "unknown": 3}
    allocation = sample_frame.largest_remainder(40, populations)
    assert sum(allocation.values()) == 40
    assert set(allocation) == set(populations)
    assert all(allocation[k] <= populations[k] for k in populations)


def test_registered_design_requires_registration(root, tmp_path, monkeypatch, capsys):
    out = tmp_path / "sample.csv"
    code = _run(
        monkeypatch,
        "--design", "registered",
        "--frame", str(root / "data" / "citation_frame_2666.csv"),
        "--out", str(out),
        "--seed", "20261122",
    )
    assert code == 4
    assert not out.exists()
    assert "registration reference" in capsys.readouterr().err


def test_registered_design_accepts_stage1_reference(root, tmp_path, monkeypatch):
    out = tmp_path / "sample.csv"
    code = _run(
        monkeypatch,
        "--design", "registered",
        "--frame", str(root / "data" / "citation_frame_2666.csv"),
        "--out", str(out),
        "--seed", "20261122",
        "--stage1-acceptance", "TEST-STAGE1-REFERENCE",
    )
    assert code == 0

    with out.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 900
    assert sum(1 for r in rows if r["design_role"] == "swe_bench_plus_census") == 135
    assert sum(1 for r in rows if r["design_role"] == "evalplus_only_sample") == 765

    manifest = json.loads(out.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["registration"]["route"] == "stage1"
    assert manifest["registration"]["reference"] == "TEST-STAGE1-REFERENCE"
    assert manifest["design_weight"]["evalplus_only_sample"] == pytest.approx(2531 / 765)


def test_registered_design_is_deterministic_for_a_fixed_seed(root, tmp_path, monkeypatch):
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"
    base = [
        "--design", "registered",
        "--frame", str(root / "data" / "citation_frame_2666.csv"),
        "--seed", "20261122",
        "--allow-unregistered",
    ]
    assert _run(monkeypatch, *base, "--out", str(first)) == 0
    assert _run(monkeypatch, *base, "--out", str(second)) == 0

    def ids(path):
        with path.open(encoding="utf-8", newline="") as handle:
            return [row["cluster_id"] for row in csv.DictReader(handle)]

    assert ids(first) == ids(second)
