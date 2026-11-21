#!/usr/bin/env python3
"""Compute human inter-rater agreement for the pilot double-coding.

The script reads two completed coder sheets and writes a JSON report, a
Markdown summary, and a CSV of disagreements. It is deliberately strict: the
two sheets must cover exactly the same ``paper_key`` + ``critique`` keys, and
duplicate keys are an error. A missing row is a protocol failure, not something
to paper over with an inner join.

This computes agreement between whatever sheets you give it. It cannot verify
that the sheets were completed by two independent humans. Do not describe the
output as human reliability until that is true.

Usage
-----
    python scripts/agreement.py \
        --coder-a reproducibility/human_coding/coder_A_completed.csv \
        --coder-b reproducibility/human_coding/coder_B_completed.csv

Outputs
-------
analysis/human_coding/agreement_report.json
analysis/human_coding/agreement_report.md
analysis/human_coding/agreement_disagreements.csv

Exit codes
----------
0  agreement computed
2  malformed input, duplicate key, or key-set mismatch
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "analysis" / "human_coding"
DEFAULT_SEED = 20261113

REQUIRED_COLUMNS = ("paper_key", "critique", "eligible", "score")
ALLOWED_CRITIQUES = ("evalplus", "swebenchplus", "gsm1k")
ALLOWED_REASONS = ("NO_EVAL", "NO_CITATION", "ACCESS", "LANGUAGE", "DUPLICATE")
TRUE_VALUES = {"true", "yes", "1"}
FALSE_VALUES = {"false", "no", "0"}
SCORE_LABELS = (0, 1, 2, 3)
ELIGIBILITY_LABELS = (0, 1)

DISAGREEMENT_FIELDS = [
    "paper_key",
    "critique",
    "disagreement_type",
    "a_eligible",
    "b_eligible",
    "a_score",
    "b_score",
    "score_gap",
    "a_ineligibility_reason",
    "b_ineligibility_reason",
    "a_engagement",
    "b_engagement",
    "a_confidence",
    "b_confidence",
    "a_evidence_quote",
    "b_evidence_quote",
    "a_notes",
    "b_notes",
]


class AgreementError(ValueError):
    """Raised when a coder sheet cannot be compared safely."""


@dataclass(frozen=True)
class Coding:
    paper_key: str
    critique: str
    eligible: bool
    score: int | None
    ineligibility_reason: str | None
    row: dict[str, str]


@dataclass(frozen=True)
class KappaResult:
    n: int
    agreement: float | None
    observed: float | None
    expected: float | None
    kappa: float | None
    note: str | None


@dataclass(frozen=True)
class Comparison:
    keys: list[tuple[str, str]]
    eligibility_pairs: list[tuple[int, int]]
    ordinal_pairs: list[tuple[int, int]]
    disagreements: list[dict[str, Any]]


def _key_label(key: tuple[str, str]) -> str:
    return f"{key[0]}/{key[1]}"


def parse_bool(raw: str | None, field: str, where: str) -> bool:
    value = str(raw or "").strip().lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    if value == "":
        raise AgreementError(f"{where}: {field} is blank; use true or false")
    raise AgreementError(
        f"{where}: {field} must be true or false, got {raw!r}"
    )


def parse_score(raw: str | None, eligible: bool, where: str) -> int | None:
    value = str(raw or "").strip()
    if not eligible:
        if value != "":
            raise AgreementError(
                f"{where}: ineligible rows must leave score blank, got {raw!r}"
            )
        return None
    if value not in {"0", "1", "2", "3"}:
        raise AgreementError(
            f"{where}: eligible rows need an integer score from 0 to 3, got {raw!r}"
        )
    return int(value)


def read_sheet(path: Path) -> dict[tuple[str, str], Coding]:
    """Read one coder sheet and validate the fields the comparison needs."""
    path = Path(path)
    if not path.is_file():
        raise AgreementError(f"coder sheet not found: {path}")

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            raw_header = next(reader)
        except StopIteration:
            raise AgreementError(f"{path}: file is empty") from None
        header = [str(name).strip() for name in raw_header]
        if any(not name for name in header):
            raise AgreementError(f"{path}: header contains an empty column name")
        duplicates = [name for name, count in Counter(header).items() if count > 1]
        if duplicates:
            raise AgreementError(
                f"{path}: duplicate column name(s): {', '.join(sorted(duplicates))}"
            )
        missing = [name for name in REQUIRED_COLUMNS if name not in header]
        if missing:
            raise AgreementError(
                f"{path}: missing required column(s): {', '.join(missing)}"
            )

        records: dict[tuple[str, str], Coding] = {}
        seen_at: dict[tuple[str, str], int] = {}
        for line_no, values in enumerate(reader, start=2):
            if len(values) != len(header):
                raise AgreementError(
                    f"{path}:{line_no}: expected {len(header)} columns, got {len(values)}"
                )
            if all(not str(value).strip() for value in values):
                continue
            row = dict(zip(header, values))
            paper_key = row["paper_key"].strip()
            critique = row["critique"].strip().lower()
            where = f"{path.name}:{line_no}"
            if not paper_key:
                raise AgreementError(f"{where}: paper_key is blank")
            if critique not in ALLOWED_CRITIQUES:
                raise AgreementError(
                    f"{where}: critique must be one of {', '.join(ALLOWED_CRITIQUES)}; "
                    f"got {row['critique']!r}"
                )
            eligible = parse_bool(row["eligible"], "eligible", where)
            score = parse_score(row["score"], eligible, where)

            reason: str | None = None
            if "ineligibility_reason" in header:
                reason_value = row.get("ineligibility_reason", "").strip().upper()
                if eligible:
                    if reason_value:
                        raise AgreementError(
                            f"{where}: eligible rows must leave ineligibility_reason "
                            f"blank, got {row['ineligibility_reason']!r}"
                        )
                else:
                    if not reason_value:
                        raise AgreementError(
                            f"{where}: ineligible rows need an ineligibility_reason "
                            f"({', '.join(ALLOWED_REASONS)})"
                        )
                    if reason_value not in ALLOWED_REASONS:
                        raise AgreementError(
                            f"{where}: ineligibility_reason must be one of "
                            f"{', '.join(ALLOWED_REASONS)}; got {row['ineligibility_reason']!r}"
                        )
                    reason = reason_value

            key = (paper_key, critique)
            if key in records:
                raise AgreementError(
                    f"{path}: duplicate key {_key_label(key)} at lines "
                    f"{seen_at[key]} and {line_no}"
                )
            seen_at[key] = line_no
            records[key] = Coding(
                paper_key=paper_key,
                critique=critique,
                eligible=eligible,
                score=score,
                ineligibility_reason=reason,
                row=row,
            )

    if not records:
        raise AgreementError(f"{path}: no data rows")
    return records


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _disagreement_row(
    a: Coding,
    b: Coding,
    disagreement_type: str,
) -> dict[str, Any]:
    score_a = a.score
    score_b = b.score
    gap = abs(score_a - score_b) if score_a is not None and score_b is not None else None
    return {
        "paper_key": a.paper_key,
        "critique": a.critique,
        "disagreement_type": disagreement_type,
        "a_eligible": _bool_text(a.eligible),
        "b_eligible": _bool_text(b.eligible),
        "a_score": score_a,
        "b_score": score_b,
        "score_gap": gap,
        "a_ineligibility_reason": a.ineligibility_reason,
        "b_ineligibility_reason": b.ineligibility_reason,
        "a_engagement": _blank(a.row.get("engagement")),
        "b_engagement": _blank(b.row.get("engagement")),
        "a_confidence": _blank(a.row.get("confidence")),
        "b_confidence": _blank(b.row.get("confidence")),
        "a_evidence_quote": _blank(a.row.get("evidence_quote")),
        "b_evidence_quote": _blank(b.row.get("evidence_quote")),
        "a_notes": _blank(a.row.get("notes")),
        "b_notes": _blank(b.row.get("notes")),
    }


def _blank(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def compare_sheets(
    a: dict[tuple[str, str], Coding],
    b: dict[tuple[str, str], Coding],
) -> Comparison:
    keys_a = set(a)
    keys_b = set(b)
    missing_from_b = sorted(keys_a - keys_b)
    missing_from_a = sorted(keys_b - keys_a)
    if missing_from_a or missing_from_b:
        parts: list[str] = []
        if missing_from_b:
            parts.append(
                "missing from coder B: "
                + ", ".join(_key_label(key) for key in missing_from_b)
            )
        if missing_from_a:
            parts.append(
                "missing from coder A: "
                + ", ".join(_key_label(key) for key in missing_from_a)
            )
        raise AgreementError(
            "coder sheets do not cover the same paper_key + critique keys; "
            + "; ".join(parts)
        )

    keys = sorted(keys_a)
    eligibility_pairs: list[tuple[int, int]] = []
    ordinal_pairs: list[tuple[int, int]] = []
    disagreements: list[dict[str, Any]] = []

    for key in keys:
        ca = a[key]
        cb = b[key]
        eligibility_pairs.append((int(ca.eligible), int(cb.eligible)))

        if ca.eligible and cb.eligible:
            assert ca.score is not None and cb.score is not None
            ordinal_pairs.append((ca.score, cb.score))
            if ca.score != cb.score:
                disagreements.append(_disagreement_row(ca, cb, "score"))
        elif ca.eligible != cb.eligible:
            disagreements.append(_disagreement_row(ca, cb, "eligibility"))
        else:
            if (
                ca.ineligibility_reason is not None
                and cb.ineligibility_reason is not None
                and ca.ineligibility_reason != cb.ineligibility_reason
            ):
                disagreements.append(
                    _disagreement_row(ca, cb, "ineligibility_reason")
                )

    return Comparison(
        keys=keys,
        eligibility_pairs=eligibility_pairs,
        ordinal_pairs=ordinal_pairs,
        disagreements=disagreements,
    )


def confusion_matrix(
    pairs: Sequence[tuple[int, int]],
    labels: Sequence[int],
) -> list[list[int]]:
    index = {label: position for position, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for left, right in pairs:
        matrix[index[left]][index[right]] += 1
    return matrix


def cohens_kappa(
    pairs: Sequence[tuple[int, int]],
    labels: Sequence[int],
    weighting: str = "none",
) -> KappaResult:
    """Cohen's kappa with unweighted, linear, or quadratic weights."""
    n = len(pairs)
    if n == 0:
        return KappaResult(0, None, None, None, None, "no pairs to compare")

    k = len(labels)
    if k < 2:
        raise ValueError("kappa needs at least two categories")
    matrix = confusion_matrix(pairs, labels)
    row_totals = [sum(row) for row in matrix]
    col_totals = [sum(matrix[i][j] for i in range(k)) for j in range(k)]

    if weighting == "none":
        weights = [
            [1.0 if i == j else 0.0 for j in range(k)] for i in range(k)
        ]
    elif weighting == "linear":
        weights = [
            [1.0 - abs(i - j) / (k - 1) for j in range(k)] for i in range(k)
        ]
    elif weighting == "quadratic":
        weights = [
            [1.0 - ((i - j) / (k - 1)) ** 2 for j in range(k)]
            for i in range(k)
        ]
    else:
        raise ValueError(f"unknown weighting: {weighting!r}")

    agreement = sum(matrix[i][i] for i in range(k)) / n
    observed = (
        sum(weights[i][j] * matrix[i][j] for i in range(k) for j in range(k))
        / n
    )
    expected = (
        sum(
            weights[i][j] * row_totals[i] * col_totals[j]
            for i in range(k)
            for j in range(k)
        )
        / (n * n)
    )

    if math.isclose(expected, 1.0, abs_tol=1e-12):
        return KappaResult(
            n=n,
            agreement=agreement,
            observed=observed,
            expected=expected,
            kappa=None,
            note=(
                "undefined because expected agreement is 1.0; there is no "
                "variance for kappa to correct for"
            ),
        )

    return KappaResult(
        n=n,
        agreement=agreement,
        observed=observed,
        expected=expected,
        kappa=(observed - expected) / (1.0 - expected),
        note=None,
    )


def pabak(result: KappaResult) -> float | None:
    if result.agreement is None:
        return None
    return 2.0 * result.agreement - 1.0


def bootstrap_ci(
    pairs: Sequence[tuple[int, int]],
    labels: Sequence[int],
    weighting: str = "none",
    resamples: int = 2000,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Percentile bootstrap interval for kappa.

    Degenerate resamples have an undefined kappa and are skipped. If too few
    valid resamples remain, the interval is reported as unavailable rather than
    silently computed from a handful of values.
    """
    n = len(pairs)
    if n == 0 or resamples <= 0:
        return {
            "resamples": max(resamples, 0),
            "valid_resamples": 0,
            "low": None,
            "high": None,
            "note": "bootstrap disabled or no pairs",
        }

    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(resamples):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        result = cohens_kappa(sample, labels, weighting)
        if result.kappa is not None:
            values.append(result.kappa)

    minimum = max(50, resamples // 2)
    if len(values) < minimum:
        return {
            "resamples": resamples,
            "valid_resamples": len(values),
            "low": None,
            "high": None,
            "note": (
                "too many resamples had an undefined kappa; interval not "
                "reported"
            ),
        }

    values.sort()
    low_index = int(0.025 * (len(values) - 1))
    high_index = int(0.975 * (len(values) - 1))
    return {
        "resamples": resamples,
        "valid_resamples": len(values),
        "low": values[low_index],
        "high": values[high_index],
        "note": None,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _display_path(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(Path(path).resolve())


def _coder_ids(sheet: dict[tuple[str, str], Coding]) -> list[str]:
    values = {
        str(coding.row.get("coder_id") or "").strip()
        for coding in sheet.values()
    }
    return sorted(value for value in values if value)


def _identity_checks(
    a_path: Path,
    b_path: Path,
    a: dict[tuple[str, str], Coding],
    b: dict[tuple[str, str], Coding],
) -> dict[str, Any]:
    same_hash = _sha256(a_path) == _sha256(b_path)
    ids_a = _coder_ids(a)
    ids_b = _coder_ids(b)
    warnings: list[str] = []
    if same_hash:
        warnings.append(
            "The two input files are byte-identical. Confirm the coders worked "
            "independently and did not copy one another."
        )
    overlap = sorted(set(ids_a) & set(ids_b))
    if overlap:
        warnings.append(
            "Both sheets report the same coder_id value(s): "
            + ", ".join(overlap)
            + ". Confirm they were completed by different people."
        )
    return {
        "a_sha256": _sha256(a_path),
        "b_sha256": _sha256(b_path),
        "same_file_hash": same_hash,
        "coder_ids_a": ids_a,
        "coder_ids_b": ids_b,
        "warning": " ".join(warnings) if warnings else None,
    }


def _stats(
    pairs: Sequence[tuple[int, int]],
    labels: Sequence[int],
    label_names: Sequence[str],
    weightings: Sequence[str],
    bootstrap: int,
    seed: int,
) -> dict[str, Any]:
    if not pairs:
        return {
            "n": 0,
            "agreement_count": 0,
            "agreement": None,
            "kappa": None,
            "kappa_note": "no pairs to compare",
            "pabak": None,
            "confusion_matrix": {
                "labels": list(label_names),
                "rows": confusion_matrix(pairs, labels),
            },
            "weighted": {},
            "bootstrap_95_ci": {},
        }

    unweighted = cohens_kappa(pairs, labels, "none")
    agreement_count = sum(1 for left, right in pairs if left == right)
    weighted: dict[str, Any] = {}
    intervals: dict[str, Any] = {}
    for weighting in weightings:
        result = cohens_kappa(pairs, labels, weighting)
        weighted[weighting] = {
            "observed": result.observed,
            "expected": result.expected,
            "kappa": result.kappa,
            "note": result.note,
        }
        intervals[weighting] = bootstrap_ci(
            pairs, labels, weighting, resamples=bootstrap, seed=seed
        )

    return {
        "n": unweighted.n,
        "agreement_count": agreement_count,
        "agreement": unweighted.agreement,
        "kappa": unweighted.kappa,
        "kappa_note": unweighted.note,
        "pabak": pabak(unweighted),
        "confusion_matrix": {
            "labels": list(label_names),
            "rows": confusion_matrix(pairs, labels),
        },
        "weighted": weighted,
        "bootstrap_95_ci": intervals,
    }


def build_report(
    a_path: Path,
    b_path: Path,
    a: dict[tuple[str, str], Coding],
    b: dict[tuple[str, str], Coding],
    label_a: str = "A",
    label_b: str = "B",
    bootstrap: int = 2000,
    seed: int = DEFAULT_SEED,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    comparison = compare_sheets(a, b)
    eligibility = _stats(
        comparison.eligibility_pairs,
        ELIGIBILITY_LABELS,
        ("ineligible", "eligible"),
        ("none",),
        bootstrap,
        seed,
    )
    ordinal = _stats(
        comparison.ordinal_pairs,
        SCORE_LABELS,
        ("0", "1", "2", "3"),
        ("none", "linear", "quadratic"),
        bootstrap,
        seed,
    )
    ordinal["score_distribution_a"] = {
        str(label): sum(1 for left, _ in comparison.ordinal_pairs if left == label)
        for label in SCORE_LABELS
    }
    ordinal["score_distribution_b"] = {
        str(label): sum(1 for _, right in comparison.ordinal_pairs if right == label)
        for label in SCORE_LABELS
    }

    by_type = Counter(row["disagreement_type"] for row in comparison.disagreements)
    identity = _identity_checks(a_path, b_path, a, b)

    report: dict[str, Any] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": (
            "Agreement between the supplied coder sheets for the 12-paper "
            "pilot. Not a prevalence estimate."
        ),
        "inputs": {
            "coder_a": {
                "label": label_a,
                "path": _display_path(a_path),
                "sha256": identity["a_sha256"],
                "rows": len(a),
            },
            "coder_b": {
                "label": label_b,
                "path": _display_path(b_path),
                "sha256": identity["b_sha256"],
                "rows": len(b),
            },
        },
        "key_count": len(comparison.keys),
        "eligibility": eligibility,
        "ordinal": ordinal,
        "disagreement_count": len(comparison.disagreements),
        "disagreements_by_type": dict(sorted(by_type.items())),
        "disagreements": comparison.disagreements,
        "identity_checks": identity,
        "caveats": [
            "The script cannot verify that the sheets were completed by two "
            "independent humans. Confirm that before reporting the values.",
            "The pilot has 12 rows. Any kappa estimated from it is unstable; "
            "report the interval and do not treat it as an instrument property.",
            "A null kappa means expected agreement was 1.0, so kappa is "
            "undefined. Do not substitute 1.00.",
            "These values are not the pilot's LLM-LLM agreement values and "
            "must not be reported as such.",
        ],
    }
    return report, comparison.disagreements


def _format_float(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "undefined"
    return f"{value:.{digits}f}"


def _format_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def _format_ci(interval: dict[str, Any] | None) -> str:
    if not interval:
        return "unavailable"
    low = interval.get("low")
    high = interval.get("high")
    if low is None or high is None:
        return "unavailable"
    return f"{low:.3f}–{high:.3f}"


def _md_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _matrix_lines(matrix: dict[str, Any], row_title: str = "A \\ B") -> list[str]:
    labels = matrix["labels"]
    rows = matrix["rows"]
    column_widths = [len(str(label)) for label in labels]
    for row in rows:
        column_widths = [
            max(width, len(str(value)))
            for width, value in zip(column_widths, row)
        ]
    row_header_width = max(
        [len(row_title)] + [len(str(label)) for label in labels]
    )
    header = f"{row_title:>{row_header_width}}"
    for width, label in zip(column_widths, labels):
        header += f"  {str(label):>{width}}"
    lines = [header]
    for row_label, row in zip(labels, rows):
        line = f"{str(row_label):>{row_header_width}}"
        for width, value in zip(column_widths, row):
            line += f"  {str(value):>{width}}"
        lines.append(line)
    return lines


def format_report_markdown(report: dict[str, Any]) -> str:
    eligibility = report["eligibility"]
    ordinal = report["ordinal"]
    inputs = report["inputs"]
    lines: list[str] = [
        "# Human Coding Agreement\n\n",
        f"Generated {report['generated_utc']}.\n\n",
        f"**Status:** {report['status']}\n\n",
        "## Inputs\n\n",
        "| Coder | File | SHA-256 | Rows |\n",
        "|---|---|---|---:|\n",
        f"| {_md_cell(inputs['coder_a']['label'])} | `{_md_cell(inputs['coder_a']['path'])}` | "
        f"`{inputs['coder_a']['sha256'][:16]}…` | {inputs['coder_a']['rows']} |\n",
        f"| {_md_cell(inputs['coder_b']['label'])} | `{_md_cell(inputs['coder_b']['path'])}` | "
        f"`{inputs['coder_b']['sha256'][:16]}…` | {inputs['coder_b']['rows']} |\n",
        f"\nCompared keys: **{report['key_count']}**.\n",
    ]

    warning = report["identity_checks"].get("warning")
    if warning:
        lines.append(f"\n> **Identity check:** {warning}\n")

    lines += [
        "\n## Eligibility (all rows)\n\n",
        "| Quantity | Value |\n",
        "|---|---:|\n",
        f"| Rows | {eligibility['n']} |\n",
        f"| Agreement | {eligibility['agreement_count']}/{eligibility['n']} "
        f"({_format_pct(eligibility['agreement'])}) |\n",
        f"| Cohen's κ (unweighted) | {_format_float(eligibility['kappa'])} |\n",
        f"| Bootstrap 95% CI | "
        f"{_format_ci(eligibility['bootstrap_95_ci'].get('none'))} |\n",
        f"| PABAK | {_format_float(eligibility['pabak'])} |\n",
    ]
    if eligibility.get("kappa_note"):
        lines.append(f"\n*κ note:* {eligibility['kappa_note']}.\n")

    lines += [
        "\nConfusion matrix (rows = coder A, columns = coder B):\n\n",
        "```text\n",
        "\n".join(_matrix_lines(eligibility["confusion_matrix"])),
        "\n```\n",
    ]

    lines += [
        "\n## Ordinal adoption score\n\n",
        "Only rows that both coders marked eligible are included.\n\n",
        "| Quantity | Value |\n",
        "|---|---:|\n",
        f"| Rows | {ordinal['n']} |\n",
        f"| Agreement | {ordinal['agreement_count']}/{ordinal['n']} "
        f"({_format_pct(ordinal['agreement'])}) |\n",
        f"| Cohen's κ (unweighted) | {_format_float(ordinal['kappa'])} |\n",
        f"| Unweighted κ 95% CI | "
        f"{_format_ci(ordinal['bootstrap_95_ci'].get('none'))} |\n",
        f"| Linear-weighted κ | {_format_float(ordinal['weighted'].get('linear', {}).get('kappa'))} |\n",
        f"| Linear κ 95% CI | "
        f"{_format_ci(ordinal['bootstrap_95_ci'].get('linear'))} |\n",
        f"| Quadratic-weighted κ | {_format_float(ordinal['weighted'].get('quadratic', {}).get('kappa'))} |\n",
        f"| Quadratic κ 95% CI | "
        f"{_format_ci(ordinal['bootstrap_95_ci'].get('quadratic'))} |\n",
        f"| PABAK | {_format_float(ordinal['pabak'])} |\n",
    ]
    if ordinal.get("kappa_note"):
        lines.append(f"\n*κ note:* {ordinal['kappa_note']}.\n")

    lines += [
        "\nConfusion matrix (rows = coder A, columns = coder B):\n\n",
        "```text\n",
        "\n".join(_matrix_lines(ordinal["confusion_matrix"])),
        "\n```\n",
    ]

    if ordinal["n"] == 0:
        lines.append(
            "\nNo rows were marked eligible by both coders, so the ordinal "
            "statistics are not defined.\n"
        )

    lines += [
        "\n## Disagreements\n\n",
        f"Total: **{report['disagreement_count']}**.\n\n",
    ]
    if report["disagreements"]:
        lines += [
            "| Paper | Critique | Type | A | B | Gap |\n",
            "|---|---|---|---|---|---:|\n",
        ]
        for row in report["disagreements"]:
            if row["disagreement_type"] == "eligibility":
                left = f"eligible={row['a_eligible']}"
                right = f"eligible={row['b_eligible']}"
                gap = ""
            elif row["disagreement_type"] == "score":
                left = f"score={row['a_score']}"
                right = f"score={row['b_score']}"
                gap = str(row["score_gap"])
            else:
                left = str(row["a_ineligibility_reason"] or "")
                right = str(row["b_ineligibility_reason"] or "")
                gap = ""
            lines.append(
                f"| `{_md_cell(row['paper_key'])}` | `{_md_cell(row['critique'])}` | "
                f"{_md_cell(row['disagreement_type'])} | {_md_cell(left)} | "
                f"{_md_cell(right)} | {gap} |\n"
            )
        lines.append("\n### Detail\n\n")
        for row in report["disagreements"]:
            lines.append(
                f"#### `{_md_cell(row['paper_key'])}` / `{_md_cell(row['critique'])}`\n\n"
            )
            score_a = "" if row["a_score"] is None else row["a_score"]
            score_b = "" if row["b_score"] is None else row["b_score"]
            lines.append(
                f"- Type: `{row['disagreement_type']}`\n"
                f"- Coder A: eligible={row['a_eligible']}, score={score_a}\n"
                f"- Coder B: eligible={row['b_eligible']}, score={score_b}\n"
            )
            if row.get("a_evidence_quote") or row.get("b_evidence_quote"):
                lines.append(
                    f"- A quote: {_md_cell(row.get('a_evidence_quote'))}\n"
                    f"- B quote: {_md_cell(row.get('b_evidence_quote'))}\n"
                )
            if row.get("a_notes") or row.get("b_notes"):
                lines.append(
                    f"- A notes: {_md_cell(row.get('a_notes'))}\n"
                    f"- B notes: {_md_cell(row.get('b_notes'))}\n"
                )
            lines.append("\n")
    else:
        lines.append(
            "No disagreements. With 12 rows, that is a useful signal but not "
            "evidence that the instrument is reliable; check the confusion "
            "matrix and the score distribution before saying anything stronger.\n"
        )

    lines += [
        "\n## How to read this\n\n",
        "- κ is agreement beyond chance. It is not a measure of whether the "
        "scores are correct.\n",
        "- Weighted κ treats a 0-versus-3 disagreement as worse than a "
        "0-versus-1 disagreement. The unweighted value treats every "
        "disagreement the same.\n",
        "- `undefined` means expected agreement was 1.0, so κ has no "
        "denominator. Report the raw agreement and say that κ is undefined. "
        "Do not replace it with 1.00.\n",
        "- The bootstrap intervals are percentile intervals from the rows in "
        "these two sheets. With 12 rows they will be wide, and that is the "
        "honest answer.\n",
        "- The script cannot verify independence, blinding, or human "
        "authorship. Those are process claims the author has to document.\n",
    ]
    return "".join(lines)


def write_outputs(
    report: dict[str, Any],
    disagreements: list[dict[str, Any]],
    out_dir: Path,
) -> tuple[Path, Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "agreement_report.json"
    md_path = out_dir / "agreement_report.md"
    csv_path = out_dir / "agreement_disagreements.csv"

    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    md_path.write_text(
        format_report_markdown(report),
        encoding="utf-8",
        newline="\n",
    )

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=DISAGREEMENT_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in disagreements:
            writer.writerow(
                {
                    field: ("" if row.get(field) is None else row.get(field, ""))
                    for field in DISAGREEMENT_FIELDS
                }
            )

    return json_path, md_path, csv_path


def _print_confusion(matrix: dict[str, Any]) -> None:
    for line in _matrix_lines(matrix):
        print(f"  {line}")


def print_summary(report: dict[str, Any]) -> None:
    eligibility = report["eligibility"]
    ordinal = report["ordinal"]
    print("Human coding agreement")
    print("======================")
    print(
        f"Coder A: {report['inputs']['coder_a']['label']} "
        f"({report['inputs']['coder_a']['rows']} rows)"
    )
    print(
        f"Coder B: {report['inputs']['coder_b']['label']} "
        f"({report['inputs']['coder_b']['rows']} rows)"
    )
    print(f"Compared keys: {report['key_count']}")
    if report["identity_checks"].get("warning"):
        print(f"\nWARNING: {report['identity_checks']['warning']}")

    print("\nEligibility (all rows)")
    print(
        f"  Agreement: {eligibility['agreement_count']}/{eligibility['n']} "
        f"({_format_pct(eligibility['agreement'])})"
    )
    print(f"  Cohen's kappa: {_format_float(eligibility['kappa'])}")
    print(f"  PABAK: {_format_float(eligibility['pabak'])}")
    if eligibility.get("kappa_note"):
        print(f"  Note: {eligibility['kappa_note']}")
    print("  Confusion matrix (A rows, B columns):")
    _print_confusion(eligibility["confusion_matrix"])

    print("\nOrdinal adoption score (rows both coders marked eligible)")
    print(f"  n: {ordinal['n']}")
    print(
        f"  Agreement: {ordinal['agreement_count']}/{ordinal['n']} "
        f"({_format_pct(ordinal['agreement'])})"
    )
    print(f"  Unweighted kappa: {_format_float(ordinal['kappa'])}")
    for weighting in ("linear", "quadratic"):
        print(
            f"  {weighting.capitalize()}-weighted kappa: "
            f"{_format_float(ordinal['weighted'].get(weighting, {}).get('kappa'))}"
        )
    print(f"  PABAK: {_format_float(ordinal['pabak'])}")
    if ordinal.get("kappa_note"):
        print(f"  Note: {ordinal['kappa_note']}")
    print("  Confusion matrix (A rows, B columns):")
    _print_confusion(ordinal["confusion_matrix"])

    print(f"\nDisagreements: {report['disagreement_count']}")
    for row in report["disagreements"]:
        if row["disagreement_type"] == "score":
            detail = f"score A={row['a_score']}, B={row['b_score']}"
        elif row["disagreement_type"] == "eligibility":
            detail = f"eligible A={row['a_eligible']}, B={row['b_eligible']}"
        else:
            detail = (
                f"reason A={row['a_ineligibility_reason']}, "
                f"B={row['b_ineligibility_reason']}"
            )
        print(f"  - {row['paper_key']}/{row['critique']}: {detail}")

    print(
        "\nReminder: this is only human reliability if both sheets were "
        "completed independently by humans. The pilot n is 12; do not report "
        "these values as a stable instrument property or as prevalence."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute human agreement between two completed pilot coder sheets. "
            "Keys are paper_key + critique; missing or duplicate keys are errors."
        )
    )
    parser.add_argument("--coder-a", required=True, type=Path, help="completed coder A CSV")
    parser.add_argument("--coder-b", required=True, type=Path, help="completed coder B CSV")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"output directory (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument("--label-a", default="A", help="display label for coder A")
    parser.add_argument("--label-b", default="B", help="display label for coder B")
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=2000,
        help="bootstrap resamples for kappa CIs; 0 disables (default: 2000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"bootstrap RNG seed (default: {DEFAULT_SEED})",
    )
    args = parser.parse_args(argv)

    try:
        coder_a = read_sheet(args.coder_a)
        coder_b = read_sheet(args.coder_b)
        report, disagreements = build_report(
            args.coder_a,
            args.coder_b,
            coder_a,
            coder_b,
            label_a=args.label_a,
            label_b=args.label_b,
            bootstrap=max(args.bootstrap, 0),
            seed=args.seed,
        )
    except AgreementError as exc:
        print(f"agreement: error: {exc}", file=sys.stderr)
        return 2

    json_path, md_path, csv_path = write_outputs(report, disagreements, args.out_dir)
    print_summary(report)
    print(f"\nWrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
