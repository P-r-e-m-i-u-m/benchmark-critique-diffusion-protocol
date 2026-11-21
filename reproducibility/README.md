# Reproducibility Package

This directory documents what can and cannot be reproduced from the public
repository for *Does Benchmark Critique Diffuse into Evaluation Practice?*

**Project status:** pilot-based draft. The full-scale study was designed but not
executed. No population prevalence estimate exists.

## Contents

| File | Purpose |
|---|---|
| `README.md` | Entry point and command index. |
| `data_dictionary.md` | Every column in the frozen frame, pilot table, and analysis outputs. |
| `provenance.md` | Where each dataset came from, retrieval dates, and what was excluded. |
| `frame_construction.md` | Raw citation rows to 2,666 title clusters, including hashes. |
| `sampling.md` | Planned 900-paper design and the documented 335-record feasibility deviation. |
| `coding_schema.md` | Rubric v1.1 fields, eligibility rules, and score definitions. |
| `human_coding/` | Blinded instructions and blank coder sheets for the pilot human reliability check. |
| `environment.md` | Software versions and dependency policy. |
| `licensing.md` | What is shareable, what is not, and why. |
| `checksums.md` | How integrity is verified and which inputs are covered. |
| `reproduction.md` | Step-by-step commands and expected outputs. |

## Quick verification

From the repository root:

```powershell
python -m pytest tests -q
python scripts/verify_checksums.py
python scripts/analyze_pilot.py
```

`analyze_pilot.py` rewrites `analysis/pilot_results.json` with a new timestamp.
Run checksum verification before regenerating outputs if you want to compare
against the committed checksums.

The human-coding packet is prepared but not executed. No human has completed the
sheets, so the pilot κ remains LLM–LLM. The agreement command is documented in
`human_coding/README.md` and in `reproduction.md` §4.

## What is reproducible

- Frame counts, strata, year distribution, and SHA-256 hashes.
- Pilot flow, score distributions, Wilson intervals, and exact-binomial diagnostics.
- All manuscript tables and figures from the frozen CSVs.
- Rubric application on the 12 published pilot rows.

## What is not reproducible from this repository

- The full texts of coded papers (not redistributed).
- The original LLM prompts, model identifier, temperature, and raw outputs
  (not preserved during the pilot).
- Human inter-rater reliability. The packet is ready, but no human second coder
  has completed it. The pilot κ values are LLM–LLM.
- Full-scale prevalence estimates (not collected).
- The partial feasibility-cohort retrieval (halted; no coding performed).
