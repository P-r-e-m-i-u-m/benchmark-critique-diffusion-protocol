# Reproducibility Statement

**Manuscript:** *Does Benchmark Critique Diffuse into Evaluation Practice? A
Pilot-Based Study of EvalPlus and SWE-bench+ Adoption*  
**Version:** Pilot-based draft v0.1, 13 November 2026  
**Repository:** https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol

## Data availability

The frozen 2,666-cluster citation frame, its summary and hashes, the 12-row pilot
coding table, the analysis scripts, the coding rubric, the generated tables and
figures, and the test suite are available in the public repository. The 335-record
feasibility cohort and its manifest are included to document a deviation from the
planned 900-paper design; the cohort was not coded and contributes no result.

Full texts and publisher PDFs are **not** redistributed. The coding table contains
metadata, codes, boundary notes, and short evidence quotes (target ≤60 words per
paper) for research criticism and verification. Third-party benchmark artifacts
retain their own licenses. Semantic Scholar metadata is provided for research use
subject to Semantic Scholar's terms and is not relicensed by this project.

## Code availability

All analysis code is in `scripts/`. The public verification path uses Python
3.11+ and the standard library; pytest is required for the test suite. No network
access is required to verify the frame, reproduce the pilot counts and intervals,
or regenerate the tables and figures.

Key commands:

```powershell
python scripts/verify_checksums.py
python -m pytest tests -q
python scripts/analyze_pilot.py
python scripts/make_manuscript_tables.py
python scripts/make_figures.py
```

## What is reproducible

- Frame counts, strata, year distribution, identifier coverage, and SHA-256 hashes.
- Pilot flow (29 → 27 → 12 → 8 → 6) and the 12-row score distribution.
- Wilson 95% intervals and exact-binomial diagnostics.
- The six manuscript tables and three SVG figures from the committed CSVs.
- The rubric's application to the published pilot rows.

## What is not reproducible from the repository

- The original full texts (not redistributed).
- The original LLM prompts, exact model identifier, temperature, and raw outputs
  (not preserved).
- Human inter-rater reliability (no human second coder).
- Full-scale prevalence estimates (not collected).
- The partial feasibility-cohort retrieval (halted; no coding performed).

## LLM-use disclosure

The pilot coding and the second coding pass were LLM-assisted. The exact model
identifier, prompt, temperature, and date were not preserved. The second pass used
a fresh context but is not statistically independent in the human sense. The
reported agreement statistics (eligibility 12/12; ordinal 7/8; unweighted κ = 0.78;
linear-weighted κ = 0.86) are **LLM–LLM agreement**, not human inter-rater
reliability. No human second coder participated.

The full study must log model, version, prompt, temperature, date, and the scope of
LLM assistance, and must human double-code at least 20% of eligible papers.

## Registration and status

The protocol was prepared for OSF registration but was **not registered**, and no
OSF DOI was obtained. The study is therefore not preregistered. A Zenodo DOI was
assigned to this pilot-study preprint at deposit: 10.5281/zenodo.24245000. That
DOI identifies the deposited preprint and its materials; it is not a registration
DOI and does not make the study preregistered. See `ERRATA.md` for the correction
of the unqualified “no DOI” wording in the frozen manuscript. This is a
pilot-based draft, not a completed full-scale study or a peer-reviewed paper.

## Integrity

`reproducibility/checksums.sha256` covers the frozen frame, pilot table, rubric,
protocol, manuscript, tables, and figure source data. `scripts/verify_checksums.py`
verifies them. The analysis JSON records the SHA-256 of the pilot table used.

## Contact

Syed Abdul Aman (Independent Researcher)  
Repository: https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol
