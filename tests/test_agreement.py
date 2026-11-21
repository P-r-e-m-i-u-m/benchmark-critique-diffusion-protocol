from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

import agreement
import human_coding_status


MINIMAL_FIELDS = ("paper_key", "critique", "eligible", "score")
FULL_FIELDS = (
    "paper_key",
    "critique",
    "eligible",
    "score",
    "ineligibility_reason",
)


def write_sheet(
    path: Path,
    rows: list[dict[str, str]],
    fieldnames: tuple[str, ...] = MINIMAL_FIELDS,
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return path


def eligibility_pair(tmp_path: Path) -> tuple[Path, Path]:
    # Coder A calls p01-p06 eligible; coder B calls p01-p04 eligible.
    # Both give every eligible row a score of 1.
    a_rows = [
        {
            "paper_key": f"p{index:02d}",
            "critique": "evalplus",
            "eligible": "true" if index <= 6 else "false",
            "score": "1" if index <= 6 else "",
        }
        for index in range(1, 11)
    ]
    b_rows = [
        {
            "paper_key": f"p{index:02d}",
            "critique": "evalplus",
            "eligible": "true" if index <= 4 else "false",
            "score": "1" if index <= 4 else "",
        }
        for index in range(1, 11)
    ]
    return (
        write_sheet(tmp_path / "coder_a.csv", a_rows),
        write_sheet(tmp_path / "coder_b.csv", b_rows),
    )


def ordinal_pair(tmp_path: Path) -> tuple[Path, Path]:
    # Eight rows, all eligible. Marginals are uniform for both coders.
    a_scores = [0, 1, 2, 3, 0, 1, 2, 3]
    b_scores = [0, 1, 2, 3, 1, 2, 3, 0]
    a_rows = [
        {
            "paper_key": f"q{index + 1:02d}",
            "critique": "swebenchplus",
            "eligible": "true",
            "score": str(score),
        }
        for index, score in enumerate(a_scores)
    ]
    b_rows = [
        {
            "paper_key": f"q{index + 1:02d}",
            "critique": "swebenchplus",
            "eligible": "true",
            "score": str(score),
        }
        for index, score in enumerate(b_scores)
    ]
    return (
        write_sheet(tmp_path / "coder_a.csv", a_rows),
        write_sheet(tmp_path / "coder_b.csv", b_rows),
    )


def test_eligibility_kappa_is_hand_computed(tmp_path):
    a_path, b_path = eligibility_pair(tmp_path)
    comparison = agreement.compare_sheets(
        agreement.read_sheet(a_path),
        agreement.read_sheet(b_path),
    )
    result = agreement.cohens_kappa(
        comparison.eligibility_pairs,
        agreement.ELIGIBILITY_LABELS,
        "none",
    )

    assert result.n == 10
    assert result.agreement == pytest.approx(0.8)
    assert result.expected == pytest.approx(0.48)
    assert result.kappa == pytest.approx(0.6153846153846154)
    assert agreement.pabak(result) == pytest.approx(0.6)
    assert agreement.confusion_matrix(
        comparison.eligibility_pairs,
        agreement.ELIGIBILITY_LABELS,
    ) == [[4, 0], [2, 4]]
    assert len(comparison.disagreements) == 2
    assert {
        row["disagreement_type"] for row in comparison.disagreements
    } == {"eligibility"}


def test_ordinal_kappas_are_hand_computed(tmp_path):
    a_path, b_path = ordinal_pair(tmp_path)
    comparison = agreement.compare_sheets(
        agreement.read_sheet(a_path),
        agreement.read_sheet(b_path),
    )
    pairs = comparison.ordinal_pairs

    unweighted = agreement.cohens_kappa(pairs, agreement.SCORE_LABELS, "none")
    linear = agreement.cohens_kappa(pairs, agreement.SCORE_LABELS, "linear")
    quadratic = agreement.cohens_kappa(
        pairs, agreement.SCORE_LABELS, "quadratic"
    )

    assert unweighted.n == 8
    assert unweighted.agreement == pytest.approx(0.5)
    assert unweighted.expected == pytest.approx(0.25)
    assert unweighted.kappa == pytest.approx(1 / 3)
    assert linear.kappa == pytest.approx(0.4)
    assert quadratic.kappa == pytest.approx(0.4)
    assert agreement.pabak(unweighted) == pytest.approx(0.0)
    assert agreement.confusion_matrix(pairs, agreement.SCORE_LABELS) == [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]
    assert len(comparison.disagreements) == 4
    assert {row["score_gap"] for row in comparison.disagreements} == {1, 3}


def test_all_agree_with_variance_gives_kappa_one(tmp_path):
    scores = [0, 0, 1, 1, 2, 2]
    rows = [
        {
            "paper_key": f"r{index + 1:02d}",
            "critique": "evalplus",
            "eligible": "true",
            "score": str(score),
        }
        for index, score in enumerate(scores)
    ]
    a_path = write_sheet(tmp_path / "coder_a.csv", rows)
    b_path = write_sheet(tmp_path / "coder_b.csv", rows)
    comparison = agreement.compare_sheets(
        agreement.read_sheet(a_path),
        agreement.read_sheet(b_path),
    )
    result = agreement.cohens_kappa(
        comparison.ordinal_pairs,
        agreement.SCORE_LABELS,
        "none",
    )

    assert result.agreement == 1.0
    assert result.expected == pytest.approx(1 / 3)
    assert result.kappa == pytest.approx(1.0)


def test_all_agree_same_category_is_undefined_not_one():
    pairs = [(1, 1)] * 5
    result = agreement.cohens_kappa(pairs, agreement.SCORE_LABELS, "none")

    assert result.agreement == 1.0
    assert result.expected == 1.0
    assert result.kappa is None
    assert result.note is not None
    assert "undefined" in result.note


def test_bootstrap_interval_is_ordered_when_defined():
    pairs = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (1, 2), (2, 3), (3, 0)]
    interval = agreement.bootstrap_ci(
        pairs,
        agreement.SCORE_LABELS,
        "linear",
        resamples=200,
        seed=7,
    )

    assert interval["valid_resamples"] > 0
    assert interval["low"] is not None
    assert interval["high"] is not None
    assert interval["low"] <= interval["high"]


def test_bootstrap_interval_is_unavailable_for_degenerate_data():
    interval = agreement.bootstrap_ci(
        [(1, 1)] * 5,
        agreement.SCORE_LABELS,
        "none",
        resamples=50,
        seed=1,
    )

    assert interval["valid_resamples"] == 0
    assert interval["low"] is None
    assert interval["high"] is None
    assert "undefined" in interval["note"]


def test_missing_key_fails_loudly(tmp_path):
    a_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p02", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    b_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    a = agreement.read_sheet(write_sheet(tmp_path / "a.csv", a_rows))
    b = agreement.read_sheet(write_sheet(tmp_path / "b.csv", b_rows))

    with pytest.raises(agreement.AgreementError, match="missing from coder B"):
        agreement.compare_sheets(a, b)


def test_missing_key_in_coder_a_fails_loudly(tmp_path):
    a_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    b_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p02", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    a = agreement.read_sheet(write_sheet(tmp_path / "a.csv", a_rows))
    b = agreement.read_sheet(write_sheet(tmp_path / "b.csv", b_rows))

    with pytest.raises(agreement.AgreementError, match="missing from coder A"):
        agreement.compare_sheets(a, b)


def test_duplicate_key_fails_loudly(tmp_path):
    rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    path = write_sheet(tmp_path / "a.csv", rows)

    with pytest.raises(agreement.AgreementError, match="duplicate key p01/evalplus"):
        agreement.read_sheet(path)


def test_same_paper_with_two_critiques_is_allowed(tmp_path):
    rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p01", "critique": "swebenchplus", "eligible": "true", "score": "1"},
    ]
    a = agreement.read_sheet(write_sheet(tmp_path / "a.csv", rows))
    b = agreement.read_sheet(write_sheet(tmp_path / "b.csv", rows))

    comparison = agreement.compare_sheets(a, b)
    assert comparison.keys == [("p01", "evalplus"), ("p01", "swebenchplus")]
    assert comparison.eligibility_pairs == [(1, 1), (1, 1)]


@pytest.mark.parametrize(
    "row, message",
    [
        (
            {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "4"},
            "integer score from 0 to 3",
        ),
        (
            {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": ""},
            "integer score from 0 to 3",
        ),
        (
            {"paper_key": "p01", "critique": "evalplus", "eligible": "false", "score": "0"},
            "must leave score blank",
        ),
        (
            {"paper_key": "p01", "critique": "other", "eligible": "true", "score": "1"},
            "critique must be one of",
        ),
        (
            {"paper_key": "", "critique": "evalplus", "eligible": "true", "score": "1"},
            "paper_key is blank",
        ),
        (
            {"paper_key": "p01", "critique": "evalplus", "eligible": "maybe", "score": "1"},
            "must be true or false",
        ),
    ],
)
def test_invalid_minimal_rows_are_rejected(tmp_path, row, message):
    path = write_sheet(tmp_path / "a.csv", [row])
    with pytest.raises(agreement.AgreementError, match=message):
        agreement.read_sheet(path)


def test_ineligible_row_needs_a_reason_when_the_column_exists(tmp_path):
    row = {
        "paper_key": "p01",
        "critique": "evalplus",
        "eligible": "false",
        "score": "",
        "ineligibility_reason": "",
    }
    path = write_sheet(tmp_path / "a.csv", [row], FULL_FIELDS)
    with pytest.raises(agreement.AgreementError, match="need an ineligibility_reason"):
        agreement.read_sheet(path)


def test_eligible_row_must_not_have_an_ineligibility_reason(tmp_path):
    row = {
        "paper_key": "p01",
        "critique": "evalplus",
        "eligible": "true",
        "score": "1",
        "ineligibility_reason": "NO_EVAL",
    }
    path = write_sheet(tmp_path / "a.csv", [row], FULL_FIELDS)
    with pytest.raises(
        agreement.AgreementError,
        match="must leave ineligibility_reason blank",
    ):
        agreement.read_sheet(path)


def test_ineligibility_reason_disagreement_is_reported(tmp_path):
    a_rows = [
        {
            "paper_key": "p01",
            "critique": "evalplus",
            "eligible": "false",
            "score": "",
            "ineligibility_reason": "NO_EVAL",
        }
    ]
    b_rows = [
        {
            "paper_key": "p01",
            "critique": "evalplus",
            "eligible": "false",
            "score": "",
            "ineligibility_reason": "ACCESS",
        }
    ]
    a = agreement.read_sheet(
        write_sheet(tmp_path / "a.csv", a_rows, FULL_FIELDS)
    )
    b = agreement.read_sheet(
        write_sheet(tmp_path / "b.csv", b_rows, FULL_FIELDS)
    )
    comparison = agreement.compare_sheets(a, b)

    assert comparison.eligibility_pairs == [(0, 0)]
    assert len(comparison.disagreements) == 1
    assert comparison.disagreements[0]["disagreement_type"] == "ineligibility_reason"


def test_all_ineligible_reports_zero_ordinal(tmp_path):
    rows = [
        {
            "paper_key": f"r{index:02d}",
            "critique": "evalplus",
            "eligible": "false",
            "score": "",
        }
        for index in range(1, 5)
    ]
    a_path = write_sheet(tmp_path / "a.csv", rows)
    b_path = write_sheet(tmp_path / "b.csv", rows)
    report, disagreements = agreement.build_report(
        a_path,
        b_path,
        agreement.read_sheet(a_path),
        agreement.read_sheet(b_path),
        bootstrap=0,
    )

    assert report["eligibility"]["agreement"] == 1.0
    assert report["eligibility"]["kappa"] is None
    assert report["ordinal"]["n"] == 0
    assert report["ordinal"]["kappa"] is None
    assert report["ordinal"]["confusion_matrix"]["rows"] == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert disagreements == []


def test_identical_files_trigger_identity_warning(tmp_path):
    rows = [
        {
            "paper_key": f"p{index:02d}",
            "critique": "evalplus",
            "eligible": "true",
            "score": str(index % 4),
        }
        for index in range(1, 9)
    ]
    a_path = write_sheet(tmp_path / "a.csv", rows)
    b_path = write_sheet(tmp_path / "b.csv", rows)
    report, _ = agreement.build_report(
        a_path,
        b_path,
        agreement.read_sheet(a_path),
        agreement.read_sheet(b_path),
        bootstrap=0,
    )

    assert report["identity_checks"]["same_file_hash"] is True
    assert "byte-identical" in report["identity_checks"]["warning"]


def test_cli_writes_json_markdown_and_disagreement_csv(tmp_path, capsys):
    a_path, b_path = eligibility_pair(tmp_path)
    out_dir = tmp_path / "out"
    exit_code = agreement.main(
        [
            "--coder-a",
            str(a_path),
            "--coder-b",
            str(b_path),
            "--out-dir",
            str(out_dir),
            "--bootstrap",
            "0",
        ]
    )

    assert exit_code == 0
    report = json.loads(
        (out_dir / "agreement_report.json").read_text(encoding="utf-8")
    )
    assert report["key_count"] == 10
    assert report["eligibility"]["kappa"] == pytest.approx(0.6153846153846154)
    assert report["eligibility"]["confusion_matrix"]["rows"] == [[4, 0], [2, 4]]
    assert report["ordinal"]["n"] == 4
    assert report["ordinal"]["kappa"] is None
    assert report["disagreement_count"] == 2

    with (out_dir / "agreement_disagreements.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert {row["disagreement_type"] for row in rows} == {"eligibility"}

    markdown = (out_dir / "agreement_report.md").read_text(encoding="utf-8")
    assert "Confusion matrix" in markdown
    assert "Eligibility" in markdown

    captured = capsys.readouterr()
    assert "Eligibility" in captured.out
    assert "Cohen's kappa" in captured.out
    assert "Reminder" in captured.out


def test_cli_missing_key_returns_two_and_writes_nothing(tmp_path, capsys):
    a_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p02", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    b_rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    a_path = write_sheet(tmp_path / "a.csv", a_rows)
    b_path = write_sheet(tmp_path / "b.csv", b_rows)
    out_dir = tmp_path / "out"

    exit_code = agreement.main(
        [
            "--coder-a",
            str(a_path),
            "--coder-b",
            str(b_path),
            "--out-dir",
            str(out_dir),
        ]
    )

    assert exit_code == 2
    captured = capsys.readouterr()
    assert "missing from coder B" in captured.err
    assert not (out_dir / "agreement_report.json").exists()


def test_cli_duplicate_key_returns_two(tmp_path, capsys):
    rows = [
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
        {"paper_key": "p01", "critique": "evalplus", "eligible": "true", "score": "1"},
    ]
    a_path = write_sheet(tmp_path / "a.csv", rows)
    b_path = write_sheet(tmp_path / "b.csv", rows)

    exit_code = agreement.main(
        [
            "--coder-a",
            str(a_path),
            "--coder-b",
            str(b_path),
            "--out-dir",
            str(tmp_path / "out"),
        ]
    )

    assert exit_code == 2
    assert "duplicate key" in capsys.readouterr().err


def test_blank_templates_are_blank_and_match_pilot_metadata(root):
    with (root / "pilot" / "pilot_coding_table.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        pilot = list(csv.DictReader(handle))

    for coder in ("A", "B"):
        path = root / "reproducibility" / "human_coding" / f"coder_{coder}.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 12
        assert len(rows) == len(pilot)
        for template, source in zip(rows, pilot):
            for field in ("paper_key", "title", "venue", "year", "critique"):
                assert template[field] == source[field]
            for field in (
                "eligible",
                "ineligibility_reason",
                "score",
                "engagement",
                "independent_remediation",
                "adoption_locus",
                "evidence_quote",
                "notes",
                "confidence",
                "adjudicate",
                "access_route",
                "coded_at",
            ):
                assert template[field] == ""
            assert template["coder_id"] == coder


def test_blank_templates_differ_only_in_coder_id(root):
    def read(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    a_rows = read(root / "reproducibility" / "human_coding" / "coder_A.csv")
    b_rows = read(root / "reproducibility" / "human_coding" / "coder_B.csv")
    assert len(a_rows) == len(b_rows)
    for left, right in zip(a_rows, b_rows):
        for field in left:
            if field == "coder_id":
                continue
            assert left[field] == right[field]


def test_blank_template_is_not_a_completed_sheet(root):
    path = root / "reproducibility" / "human_coding" / "coder_A.csv"
    with pytest.raises(agreement.AgreementError, match="eligible is blank"):
        agreement.read_sheet(path)


def test_human_coding_readme_keeps_the_blinding_rules(root):
    text = (
        root / "reproducibility" / "human_coding" / "README.md"
    ).read_text(encoding="utf-8")

    assert "No human coder has completed" in text
    assert "LLM–LLM" in text
    assert "Do not read" in text
    assert "Do not use an LLM to assign scores" in text
    assert "coder_A_completed.csv" in text
    assert "coder_B_completed.csv" in text


def test_status_reports_missing_completed_sheets(tmp_path, capsys):
    exit_code = human_coding_status.main(
        [
            "--coder-a",
            str(tmp_path / "coder_A_completed.csv"),
            "--coder-b",
            str(tmp_path / "coder_B_completed.csv"),
        ]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not ready" in captured.out
    assert "coder_A_completed.csv" in captured.out
    assert "Do not create these files" in captured.out


def test_status_rejects_an_invalid_sheet(tmp_path, capsys):
    rows = [
        {
            "paper_key": "p01",
            "critique": "evalplus",
            "eligible": "",
            "score": "",
        }
    ]
    a_path = write_sheet(tmp_path / "a.csv", rows)
    b_path = write_sheet(tmp_path / "b.csv", rows)

    exit_code = human_coding_status.main(
        ["--coder-a", str(a_path), "--coder-b", str(b_path)]
    )

    assert exit_code == 2
    assert "invalid" in capsys.readouterr().err


def test_status_ready_then_run_writes_agreement(tmp_path, capsys):
    a_path, b_path = eligibility_pair(tmp_path)
    out_dir = tmp_path / "out"

    ready_code = human_coding_status.main(
        ["--coder-a", str(a_path), "--coder-b", str(b_path)]
    )
    assert ready_code == 0
    ready_output = capsys.readouterr().out
    assert "ready" in ready_output
    assert "rows both marked eligible" in ready_output
    assert "python scripts/human_coding_status.py --run" in ready_output

    run_code = human_coding_status.main(
        [
            "--coder-a",
            str(a_path),
            "--coder-b",
            str(b_path),
            "--out-dir",
            str(out_dir),
            "--run",
        ]
    )
    assert run_code == 0
    assert (out_dir / "agreement_report.json").is_file()
    assert (out_dir / "agreement_report.md").is_file()
    assert (out_dir / "agreement_disagreements.csv").is_file()


def test_paper_sources_cover_the_pilot_without_coding_fields(root):
    with (root / "pilot" / "pilot_coding_table.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        pilot = list(csv.DictReader(handle))
    with (
        root / "reproducibility" / "human_coding" / "paper_sources.csv"
    ).open(encoding="utf-8-sig", newline="") as handle:
        sources = list(csv.DictReader(handle))

    assert len(sources) == len(pilot)
    assert [row["paper_key"] for row in sources] == [
        row["paper_key"] for row in pilot
    ]
    for source in sources:
        assert source["open_access_url"].startswith("https://")
        for hidden in ("eligible", "score", "notes", "evidence_quote"):
            assert hidden not in source

