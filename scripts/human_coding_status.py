#!/usr/bin/env python3
"""Check whether the completed human-coding sheets are ready, then optionally run.

This is a convenience wrapper around ``agreement.py``. It answers one question:
are both completed sheets present and valid? If they are, ``--run`` computes the
agreement in the same step.

It never fills, edits, or infers a sheet. A missing or malformed sheet is a
failure, not something to paper over.

Usage
-----
    python scripts/human_coding_status.py
    python scripts/human_coding_status.py --run

Exit codes
----------
0  both sheets are ready (and, with --run, agreement was written)
1  one or both completed sheets are missing
2  a sheet is present but invalid, or the two sheets do not share the same keys
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import agreement

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "reproducibility" / "human_coding"
DEFAULT_A = PACKET / "coder_A_completed.csv"
DEFAULT_B = PACKET / "coder_B_completed.csv"
DEFAULT_OUT = ROOT / "analysis" / "human_coding"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check for the two completed human-coding sheets. With --run, "
            "compute agreement if both are valid."
        )
    )
    parser.add_argument("--coder-a", type=Path, default=DEFAULT_A)
    parser.add_argument("--coder-b", type=Path, default=DEFAULT_B)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--run",
        action="store_true",
        help="run scripts/agreement.py after the checks pass",
    )
    args = parser.parse_args(argv)

    missing = [path for path in (args.coder_a, args.coder_b) if not path.is_file()]
    if missing:
        print("Human coding status: not ready")
        for path in missing:
            print(f"  missing: {path}")
        print(
            "\nBoth coders must return coder_A_completed.csv and "
            "coder_B_completed.csv before agreement can be computed."
        )
        print("Do not create these files by copying or editing the blank templates.")
        return 1

    try:
        a = agreement.read_sheet(args.coder_a)
        b = agreement.read_sheet(args.coder_b)
        comparison = agreement.compare_sheets(a, b)
    except agreement.AgreementError as exc:
        print(f"Human coding status: invalid\n  {exc}", file=sys.stderr)
        return 2

    eligible_a = sum(1 for coding in a.values() if coding.eligible)
    eligible_b = sum(1 for coding in b.values() if coding.eligible)
    print("Human coding status: ready")
    print(f"  coder A: {len(a)} rows, {eligible_a} eligible")
    print(f"  coder B: {len(b)} rows, {eligible_b} eligible")
    print(f"  common keys: {len(comparison.keys)}")
    print(f"  rows both marked eligible: {len(comparison.ordinal_pairs)}")
    print(f"  disagreements: {len(comparison.disagreements)}")

    if not args.run:
        print("\nNext: python scripts/human_coding_status.py --run")
        return 0

    print()
    return agreement.main(
        [
            "--coder-a",
            str(args.coder_a),
            "--coder-b",
            str(args.coder_b),
            "--out-dir",
            str(args.out_dir),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
