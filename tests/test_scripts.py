from __future__ import annotations

import py_compile
from pathlib import Path


def test_all_scripts_compile(root):
    scripts = sorted((root / "scripts").glob("*.py"))
    assert len(scripts) >= 8
    for script in scripts:
        py_compile.compile(str(script), doraise=True)


def test_required_scripts_exist(root):
    expected = {
        "fetch_citations.py",
        "build_frame.py",
        "sample_frame.py",
        "analysis_template.py",
        "fetch_cohort.py",
        "analyze_pilot.py",
        "agreement.py",
        "make_manuscript_tables.py",
        "make_figures.py",
        "verify_checksums.py",
    }
    actual = {path.name for path in (root / "scripts").glob("*.py")}
    assert expected.issubset(actual)


def test_verify_checksums_api(root):
    import verify_checksums

    checksums = verify_checksums.build_checksums(root)
    assert "data/citation_frame_2666.csv" in checksums
    assert "pilot/pilot_coding_table.csv" in checksums
    assert len(checksums) == len(verify_checksums.COVERED_FILES)


def test_pilot_analysis_does_not_require_network(root):
    source = (root / "scripts" / "analyze_pilot.py").read_text(encoding="utf-8")
    for forbidden in ("requests", "urllib.request", "httpx", "semanticscholar"):
        assert forbidden not in source


def test_figures_are_dependency_free_svg(root):
    for name in ("fig1_frame_years.svg", "fig2_pilot_flow.svg", "fig3_pilot_scores.svg"):
        text = (root / "manuscript" / "figures" / name).read_text(encoding="utf-8")
        assert "<svg" in text
        assert "</svg>" in text
        assert "matplotlib" not in text.lower()


def test_environment_documents_python_version(root):
    text = (root / "reproducibility" / "environment.md").read_text(encoding="utf-8")
    assert "Python" in text
    assert "3.11+" in text
    assert "matplotlib" in text.lower()
