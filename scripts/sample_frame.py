#!/usr/bin/env python3
"""Draw a stratified sample from the frozen citation frame.

Designs
-------
``registered`` (the protocol's main design)
    135 SWE-bench+ census + 765 EvalPlus-only = 900 invited.

``feasibility`` (bounded open-access/arXiv cohort used for the manuscript)
    135 SWE-bench+ census + 200 EvalPlus-only = 335 invited.

Both designs take the SWE-bench+ stratum as a census and sample the
EvalPlus-only stratum with proportional allocation by publication year
(largest-remainder rounding, minimum 1 per non-empty stratum).

Safety
------
* The frame SHA-256 is checked before sampling. A mismatch aborts.
* The output file is never overwritten unless --force is given.
* The ``registered`` design requires a registration reference: an OSF DOI
  (``--osf-doi``) or an accepted Stage 1 protocol under the ICSME/EMSE
  Registered Report route (``--stage1-acceptance``). ``--allow-unregistered``
  is only for local dry runs and labels the output as unregistered.
* The feasibility design records that it is a deviation from the registered
  sample.

Usage
-----
    python scripts/sample_frame.py --design feasibility \
        --frame data/citation_frame_2666.csv \
        --out data/cohort_feasibility.csv --seed 20261113

    python scripts/sample_frame.py --design registered \
        --frame data/citation_frame_2666.csv \
        --out data/sample_900.csv --seed 20261113 \
        --stage1-acceptance <reference>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FRAME_SHA256 = "4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0"

DESIGNS = {
    "registered": {"swe_census": 135, "evalplus_sample": 765},
    "feasibility": {"swe_census": 135, "evalplus_sample": 200},
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def largest_remainder(total: int, populations: dict[str, int]) -> dict[str, int]:
    """Allocate ``total`` across strata proportionally, minimum 1 where possible."""
    if total >= sum(populations.values()):
        return dict(populations)

    keys = sorted(populations)
    grand_total = sum(populations.values())
    quotas = {k: total * populations[k] / grand_total for k in keys}
    allocation = {k: int(quotas[k]) for k in keys}

    # Guarantee at least one draw from every non-empty stratum when total allows.
    for key in keys:
        if populations[key] > 0 and allocation[key] == 0 and total >= len(keys):
            allocation[key] = 1

    remainder = total - sum(allocation.values())
    ranked = sorted(keys, key=lambda k: (quotas[k] - int(quotas[k])), reverse=True)
    index = 0
    while remainder > 0:
        key = ranked[index % len(ranked)]
        if allocation[key] < populations[key]:
            allocation[key] += 1
            remainder -= 1
        index += 1
        if index > 10000:
            raise RuntimeError("Allocation failed to converge")
    return allocation


def read_frame(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def draw(rows: list[dict[str, str]], stratum: str, n: int, rng: random.Random) -> list[dict[str, str]]:
    pool = sorted((r for r in rows if r["stratum"] == stratum), key=lambda r: r["cluster_id"])
    if n >= len(pool):
        return pool
    by_year: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in pool:
        by_year[record.get("year") or "unknown"].append(record)
    allocation = largest_remainder(n, {k: len(v) for k, v in by_year.items()})

    chosen: list[dict[str, str]] = []
    for year in sorted(by_year):
        take = allocation.get(year, 0)
        if take <= 0:
            continue
        chosen.extend(rng.sample(by_year[year], take))
    if len(chosen) != n:
        raise RuntimeError(f"Allocation produced {len(chosen)} rows, expected {n}")
    return sorted(chosen, key=lambda r: r["cluster_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", choices=sorted(DESIGNS), required=True)
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--expected-sha256", default=FRAME_SHA256)
    parser.add_argument("--osf-doi", default=None)
    parser.add_argument(
        "--stage1-acceptance",
        default=None,
        help="Reference for an accepted Stage 1 protocol (ICSME/EMSE RR route).",
    )
    parser.add_argument("--allow-unregistered", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.out.exists() and not args.force:
        print(f"Refusing to overwrite {args.out} (use --force).", file=sys.stderr)
        return 2

    actual_hash = sha256_file(args.frame)
    if actual_hash != args.expected_sha256:
        print(
            "FRAME HASH MISMATCH — refusing to sample.\n"
            f"  expected: {args.expected_sha256}\n"
            f"  actual:   {actual_hash}",
            file=sys.stderr,
        )
        return 3

    registration_reference = args.osf_doi or args.stage1_acceptance
    if args.design == "registered" and not registration_reference and not args.allow_unregistered:
        print(
            "The registered design requires a registration reference: an OSF DOI "
            "(--osf-doi) or an accepted Stage 1 protocol (--stage1-acceptance). "
            "Use --allow-unregistered only for a local dry run.",
            file=sys.stderr,
        )
        return 4

    rows = read_frame(args.frame)
    counts = defaultdict(int)
    for record in rows:
        counts[record["stratum"]] += 1
    if counts.get("SWE_bench_plus_census") != 135:
        print(f"Unexpected SWE-bench+ census size: {counts.get('SWE_bench_plus_census')}", file=sys.stderr)
        return 5

    design = DESIGNS[args.design]
    rng = random.Random(args.seed)

    swe = draw(rows, "SWE_bench_plus_census", design["swe_census"], rng)
    evalplus = draw(rows, "EvalPlus_only_sample", design["evalplus_sample"], rng)

    total_evalplus_population = counts["EvalPlus_only_sample"]
    evalplus_weight = total_evalplus_population / design["evalplus_sample"]

    output_rows: list[dict[str, Any]] = []
    for role, records, weight, probability in (
        ("swe_bench_plus_census", swe, 1.0, 1.0),
        ("evalplus_only_sample", evalplus, evalplus_weight, design["evalplus_sample"] / total_evalplus_population),
    ):
        for record in records:
            output_rows.append({
                **record,
                "design_role": role,
                "inclusion_probability": f"{probability:.10f}",
                "design_weight": f"{weight:.10f}",
                "sample_seed": args.seed,
                "osf_doi": args.osf_doi or "",
                "sampled_utc": datetime.now(timezone.utc).isoformat(),
            })

    output_rows.sort(key=lambda r: (r["design_role"], r["cluster_id"]))
    fields = list(rows[0].keys()) + [
        "design_role", "inclusion_probability", "design_weight",
        "sample_seed", "osf_doi", "sampled_utc",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    manifest = {
        "design": args.design,
        "design_note": (
            "Registered main design: 135 SWE-bench+ census + 765 EvalPlus-only."
            if args.design == "registered"
            else "Feasibility deviation: 135 SWE-bench+ census + 200 EvalPlus-only; not the registered 900-paper sample."
        ),
        "frame": str(args.frame),
        "frame_sha256": actual_hash,
        "seed": args.seed,
        "osf_doi": args.osf_doi,
        "registration": {
            "route": (
                "osf" if args.osf_doi
                else "stage1" if args.stage1_acceptance
                else "unregistered"
            ),
            "reference": registration_reference,
        },
        "sampled_utc": datetime.now(timezone.utc).isoformat(),
        "population": dict(counts),
        "sample": {
            "swe_bench_plus_census": len(swe),
            "evalplus_only_sample": len(evalplus),
            "total": len(output_rows),
        },
        "design_weight": {
            "swe_bench_plus_census": 1.0,
            "evalplus_only_sample": evalplus_weight,
        },
    }
    manifest_path = args.out.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Wrote {args.out} and {manifest_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
