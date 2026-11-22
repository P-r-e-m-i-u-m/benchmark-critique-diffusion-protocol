# Does Benchmark Critique Diffuse into Evaluation Practice?

**A pilot-based study of EvalPlus and SWE-bench+ adoption in code-generation evaluation**

**Research website:** [p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol](https://p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol/)

**Paper (PDF):** [manuscript/paper.pdf](manuscript/paper.pdf) · **Typeset source:** [manuscript/paper.tex](manuscript/paper.tex) · **Markdown:** [manuscript/paper.md](manuscript/paper.md)

**DOI:** [10.5281/zenodo.24245000](https://doi.org/10.5281/zenodo.24245000) · **Zenodo record:** [zenodo.org/records/24245000](https://zenodo.org/records/24245000)

**Errata:** [`ERRATA.md`](ERRATA.md) records the correction of the pre-deposit “no DOI” wording; the deposited PDF is unchanged.

**Seeking an independent coder:** the pilot reliability check needs one human coder for 12 papers, about 4–6 hours, unpaid. See the [public call](reproducibility/human_coding/call_for_coders.md) or the [pinned issue](https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol/issues/14).

**Citation metadata:** The root `CITATION.cff` powers GitHub's "Cite this repository" panel. Keep it consistent with [`docs/cite.bib`](docs/cite.bib) and the Zenodo record when citation metadata changes.

<p align="center">
  <img alt="Status: pilot-study preprint" src="https://img.shields.io/badge/status-pilot%20preprint-b7791f?style=flat-square">
  <img alt="Python 3.11 or newer" src="https://img.shields.io/badge/python-3.11%2B-17324d?style=flat-square">
  <img alt="Tests passing" src="https://img.shields.io/badge/tests-passing-0f766e?style=flat-square">
  <img alt="Code license: MIT" src="https://img.shields.io/badge/code%20license-MIT-2f855a?style=flat-square">
  <img alt="Data license: CC BY 4.0" src="https://img.shields.io/badge/data%20license-CC%20BY%204.0-2c7a7b?style=flat-square">
</p>

> **Research status.** This repository hosts a **pilot-study preprint**, not a
> completed full-scale study. The pilot is purposive and small: six primary-pair
> and eight all-pair eligible papers. Agreement statistics are **LLM–LLM**, not
> human inter-rater reliability. The project does **not** estimate population
> prevalence, does **not** establish causal diffusion, and has **not** been peer
> reviewed. Read the [typeset paper](manuscript/paper.pdf), the
> [Markdown manuscript](manuscript/paper.md), or the
> [limitations checklist](manuscript/limitations_checklist.md).

**Contents:** [Paper (PDF)](#paper-pdf) · [Overview](#overview) · [Research questions](#research-questions) ·
[Methodology](#methodology) · [Pilot findings](#pilot-findings) ·
[Figures](#figures) · [Reproducibility](#reproducibility) ·
[Limitations and status](#limitations-and-status) · [Citation](#citation) ·
[Repository map](#repository-map) · [Licenses](#licenses)

| Citation frame | Pilot flow | Primary result | Agreement |
|:---:|:---:|:---:|:---:|
| **2,666**<br>title clusters | **29 → 27 → 12 → 8 → 6**<br>purposive pilot | **1/6**<br>full adoption (16.7%; 95% CI 3.0–56.4%) | **κ = 0.86**<br>linear weighted, LLM–LLM only |

*These are descriptive pilot quantities, not estimates of prevalence in the
2,666-cluster frame.*

---

## Paper (PDF)

The typeset paper is a 20-page A4 preprint with academic typography, eight
tables, three figures, and a full reference list:

- [**Download the PDF**](manuscript/paper.pdf)
- [LaTeX source](manuscript/paper.tex)
- [Markdown manuscript](manuscript/paper.md)

The PDF and Markdown manuscript report the same pilot. Neither is a peer-reviewed
publication, and neither estimates prevalence in the 2,666-cluster frame.

## Overview

Benchmark critiques such as EvalPlus and SWE-bench+ identify concrete defects in
widely used code-generation benchmarks and release remediations. Citation counts
record attention; they do not show whether citing papers change their own
evaluation practice. This project asks how often citing papers **document using
the critique's recommended artifact or protocol** in their primary evaluation of
the criticized benchmark.

The repository provides the measurement infrastructure for that question: a
frozen citation frame, a four-level coding rubric, a coded pilot, generated
tables and figures, and a reproducibility package. The pilot shows that citation,
acknowledgment, and full adoption can be distinguished in practice; no pilot
paper received a partial-adoption score. It also yields preliminary planning
estimates for access and coding effort. It does not estimate how common adoption
is across the frame; that question belongs to the full-scale study, which has
been designed but not executed.

## Research questions

> **Primary question.** Among research papers that cite a benchmark-remediation
> critique, what proportion document adopting the critique's recommended
> benchmark or protocol in their own evaluation of the criticized benchmark?

| ID | Secondary question | Role |
|---|---|---|
| SQ1 | How is engagement distributed across citation only, acknowledgment, partial adoption, and full adoption? | Descriptive |
| SQ2 | Does documented adoption differ between EvalPlus and SWE-bench+? | Exploratory; underpowered |
| SQ3 | Is adoption more common at least 12 months after the critique, in peer-reviewed venues, or in papers with author overlap? | Exploratory |
| SQ4 | How often do papers remediate independently without adopting the critique's artifact? | Descriptive |
| SQ5 | How sensitive are estimates to access failure, self-citation, benchmark version, and the treatment of partial adoption? | Robustness |

The primary outcome is **documented full adoption** (rubric score 3) among
**eligible citing papers**. "Documented" means the paper's text, tables, or
captions state that the recommended artifact or protocol was used. It does not
mean the artifact was verified to execute correctly.

## Methodology

### Citation frame

The frame is a Semantic Scholar citation snapshot retrieved on 13 November 2026
for EvalPlus (arXiv:2305.01210) and SWE-bench+ (arXiv:2410.06992). Retrieval
returned 2,572 EvalPlus citation rows and 136 SWE-bench+ rows, for 2,708 raw
rows. Identifier deduplication produced 2,684 records; title clustering produced
**2,666 analysis clusters**. The 135-cluster SWE-bench+ stratum is a census
(including 23 clusters that cite both critiques); the remaining 2,531 EvalPlus-only
clusters form the planned sample stratum. The frame is frozen, and its SHA-256
hashes are recorded in [`data/frame_summary.json`](data/frame_summary.json).

### Coding instrument

[Rubric v1.1](rubric_v1.1.md) defines four levels of documented adoption:

| Score | Label | Meaning |
|---:|---|---|
| 0 | Citation only | Reference-list entry; no specific finding discussed; benchmark unchanged. |
| 1 | Acknowledged | Specific finding discussed; evaluation unchanged. |
| 2 | Partial adoption | Remediation used in a secondary role, not for the main result. |
| 3 | Full adoption | Remediation supports a main claim, table, or figure. |

The unit of analysis is one title-level citing work × one critique. A paper is
eligible only if it evaluates the criticized benchmark. Independent remediation
is coded separately so that building a different fix is not mistaken for adopting
the critique's artifact.

### Benchmark pairs

| Pair | Critique | Criticized benchmark | Recommended remediation | Role |
|---|---|---|---|---|
| P1 | EvalPlus (Liu et al., 2023) | HumanEval; MBPP | HumanEval+ / MBPP+ augmented tests as the primary evaluation | Primary |
| P2 | SWE-bench+ (Aleithan et al., 2024) | SWE-bench; SWE-bench Lite; SWE-bench Verified | 548-instance curated dataset and/or strengthened-test protocol | Primary |
| S1 | GSM1k (Zhang et al., 2024) | GSM8K | GSM1k or an equivalent contamination-controlled replication | Secondary contrast only |

### Pilot design

The pilot is purposive, not a probability sample. It assembled 29 papers likely
to cover different benchmarks and adoption levels; 27 full texts were accessible
(93.1%), and 12 papers were coded with rubric v1.0. A second independent LLM pass
re-coded the pilot with fresh context; ordinal agreement was assessed on the eight
eligible papers, and one disagreement (`promptcot`) was adjudicated. Six papers
were eligible for the two primary pairs. No human second coder participated. The
93.1% access rate applies only to this 29-paper frame.

## Pilot findings

The pilot's purpose is measurement feasibility, not prevalence estimation.

**Flow.** 29 purposively selected papers → 27 full texts accessible → 12 coded →
8 eligible for all pairs → 6 eligible for the two primary pairs.

### Adoption scores

| Score | Label | Primary pairs (n = 6) | All pairs (n = 8) |
|---:|---|---:|---:|
| 0 | Citation only | 2 (33.3%) | 3 (37.5%) |
| 1 | Acknowledged | 3 (50.0%) | 4 (50.0%) |
| 2 | Partial adoption | 0 (0.0%) | 0 (0.0%) |
| 3 | Full adoption | 1 (16.7%) | 1 (12.5%) |

### Primary results

- **Primary pairs:** 1/6 papers fully adopted the remediation (**16.7%; Wilson
  95% CI 3.0–56.4%**). Three acknowledged the critique, two were citation-only,
  and none partially adopted.
- **All pairs:** adding the two GSM1k secondary rows gives 1/8 full adoption
  (**12.5%; Wilson 95% CI 2.2–47.1%**).
- **Independent remediation:** 3/6 primary-pair papers and 4/8 all-pair papers
  built their own remediation without adopting the critique's artifact.
- **SWE-bench+:** none of the three cases adopted the 548-instance dataset; all
  three pursued independent remediation.
- **Reliability:** ordinal agreement 7/8, unweighted κ = 0.78, linear-weighted
  κ = 0.86. Both passes were LLM annotations. These values are **not human
  inter-rater reliability**.

The counts show that citation, acknowledgment, and adoption are distinguishable.
The confidence intervals are wide because n = 6 and n = 8. Neither result is a
prevalence estimate.

## Figures

All figures are generated from the frozen pilot data by
[`scripts/make_figures.py`](scripts/make_figures.py). SVG and source CSV files
are in [`manuscript/figures/`](manuscript/figures/).

**Figure 1. The frozen citation frame.** 2,666 title clusters by publication
year. The 2026 bar is incomplete and includes 231 future-dated records; 42
clusters have no publication year. [SVG](manuscript/figures/fig1_frame_years.svg)
· [CSV](manuscript/figures/fig1_frame_years.csv)

![Figure 1: frozen citation frame by publication year](manuscript/figures/fig1_frame_years.svg)

**Figure 2. Pilot flow.** From 29 purposively selected papers to six
primary-pair eligible papers. [SVG](manuscript/figures/fig2_pilot_flow.svg) ·
[CSV](manuscript/figures/fig2_pilot_flow.csv)

![Figure 2: pilot flow](manuscript/figures/fig2_pilot_flow.svg)

**Figure 3. Adoption scores.** Documented engagement with the critique, scored
from 0 to 3, for primary pairs and all pairs. [SVG](manuscript/figures/fig3_pilot_scores.svg)
· [CSV](manuscript/figures/fig3_pilot_scores.csv)

![Figure 3: adoption-score distribution](manuscript/figures/fig3_pilot_scores.svg)

## Reproducibility

All commands run from the repository root and require no network access. The
analysis path uses Python 3.11+ and the standard library; pytest is required only
for the test suite.

```shell
python -m pytest tests -q           # 119 passed
python scripts/verify_checksums.py  # 27/27 files verified
python scripts/analyze_pilot.py     # regenerates the pilot analysis
```

The checksum manifest covers the frame, pilot table, manuscript, rubric,
protocol, tables, and figure source data. Checksums are recorded over
LF-normalized bytes (enforced by `.gitattributes`), so verification is stable
across Windows, macOS, and Linux. Tables and figures are regenerated by script;
the SVG files are not hand-edited.

### Optional link and DOI checks

The network-dependent link checker is opt-in and is not part of the
default test suite. Run it from the repository root:

```bash
python scripts/check_links.py
```

To set a longer timeout and return a nonzero exit code when any link
is broken:

```bash
python scripts/check_links.py --timeout 20 --fail-on-broken
```

The checker reads URLs and DOIs from `README.md`, `docs/index.html`,
and `verification/references.md`. It generates
`verification/link_report.json` and `verification/link_report.md`.

Known automated-access restrictions are documented in
`verification/link_allowlist.json`. Blocked responses are reported
separately from broken links. If Zenodo blocks direct automated access,
the required Zenodo DOI and record are independently verified through
DataCite.

### Human double-coding packet

The human double-coding package is prepared but not executed. The blinded sheets,
a verified link list for all 12 papers, and instructions are in
[`reproducibility/human_coding/`](reproducibility/human_coding/).
[`scripts/human_coding_status.py`](scripts/human_coding_status.py) checks that both
completed sheets exist and share the same keys; add `--run` to compute agreement in
the same step. No human has filled the sheets, so the pilot's κ values above remain
**LLM–LLM**. Completed sheets and generated agreement outputs are gitignored working
data, not part of the checksum manifest.

| Document | Purpose |
|---|---|
| [`reproducibility/reproduction.md`](reproducibility/reproduction.md) | Full run order and expected values. |
| [`reproducibility/checksums.md`](reproducibility/checksums.md) | Integrity model and verification procedure. |
| [`reproducibility/environment.md`](reproducibility/environment.md) | Tested versions and dependency policy. |
| [`reproducibility/data_dictionary.md`](reproducibility/data_dictionary.md) | Every column in the frozen data and analysis outputs. |
| [`reproducibility/human_coding/`](reproducibility/human_coding/) | Blinded human-coding instructions, blank coder sheets, and paper links. |
| [`manuscript/reproducibility_statement.md`](manuscript/reproducibility_statement.md) | Manuscript-level data and code availability statement. |

## Limitations and status

### What the pilot supports

- The four-level rubric can be applied consistently enough to distinguish
  citation, acknowledgment, and full adoption in a small purposive sample.
- Full-text access and coding effort can be estimated for planning purposes.
- The measure separates adoption of the critique's artifact from independent
  remediation.

### What it does not establish

| Limitation | Consequence |
|---|---|
| Purposive 29-paper pilot; 6 primary-pair and 8 all-pair eligible papers | No population prevalence estimate. |
| No human second coder | κ values are LLM–LLM only, not human reliability. The blinded packet and agreement script are ready; recruiting an independent coder is the blocker. |
| Exact LLM model, prompt, temperature, and raw outputs not preserved | The LLM coding pass is not exactly reproducible; the rubric and coded table are. |
| Full-scale 900-paper study not executed | No confirmatory hypothesis tests or full-frame estimates. |
| 335-record feasibility cohort drawn but not coded | Documents a deviation from the planned design; contributes no result. |
| 93.1% access rate comes from a purposive frame | The frame-wide access rate is unknown. |
| Only documented adoption is measured | Execution of the recommended artifact is not verified. |
| No registration or peer review | The paper is a pilot-study preprint, not a peer-reviewed publication. The Zenodo DOI identifies the deposited preprint; it is not a registration DOI. |

### Component status

| Component | Status |
|---|---|
| Citation frame | Frozen and verified. |
| Coding rubric | Frozen at v1.1. |
| Pilot data and analysis | Complete for 12 coded papers. |
| Typeset paper | Complete as a 20-page pilot-study preprint; not peer reviewed. |
| Preprint DOI | Zenodo, [10.5281/zenodo.24245000](https://doi.org/10.5281/zenodo.24245000). |
| Full-scale data collection | Not executed. |
| Human-coding package | Instructions, two blank sheets, agreement script, and tests complete. No completed human sheets. |
| Human reliability | Not available. The pilot κ remains LLM–LLM until two independent humans complete the sheets. |
| OSF registration | Not created; the Zenodo DOI covers the preprint and materials, not a preregistration. |
| Submission | Not ready; see [`manuscript/submission/submission_checklist.md`](manuscript/submission/submission_checklist.md). |

The next scientific step is the full study: a probability sample from the frozen
frame, a 50-record access pretest, human double-coding of at least 20% of eligible
papers, the pre-specified sensitivity analyses, and registration before main
coding. The immediate human-reliability step is narrower: recruit one independent
coder, have both coders complete the blinded sheets in
[`reproducibility/human_coding/`](reproducibility/human_coding/), and run
`scripts/agreement.py`. That gives a pilot human κ; it does not replace the full
study's double-coding plan. No further citation-frame retrieval was performed for
this repository.

## Data availability

**Included:** the frozen 2,666-cluster frame and its summary and hashes, the
12-row pilot coding table with short evidence quotes, analysis scripts, generated
tables and figures, the test suite, the blank human-coding templates, instructions,
and verified paper links, and the 335-record feasibility cohort with its manifest.
The cohort was drawn but **not coded** and contributes no result.

**Not included:** publisher PDFs and full-text copies; completed human coder
sheets and generated agreement outputs (none exist; working data are gitignored);
third-party abstracts (`data/cohort_arxiv_metadata.csv`); LLM prompts and raw
model outputs; credentials, API keys, and local temporary files. Full texts are
not redistributed. The citation-frame metadata is not relicensed and remains
subject to Semantic Scholar's terms. See
[`reproducibility/licensing.md`](reproducibility/licensing.md).

## Citation

If you use this material, cite the preprint and preserve its pilot status:

> Aman, S. A. (2026). *Does Benchmark Critique Diffuse into Evaluation Practice?
> A Pilot-Based Study of EvalPlus and SWE-bench+ Adoption* [Pilot-study
> preprint]. Zenodo. https://doi.org/10.5281/zenodo.24245000

```bibtex
@misc{aman2026benchmarkcritique,
  author       = {Aman, Syed Abdul},
  title        = {Does Benchmark Critique Diffuse into Evaluation Practice?
                  A Pilot-Based Study of EvalPlus and SWE-bench+ Adoption},
  year         = {2026},
  month        = nov,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.24245000},
  howpublished = {\url{https://p-r-e-m-i-u-m.github.io/benchmark-critique-diffusion-protocol/}},
  url          = {https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol},
  note         = {Pilot-study preprint; not peer reviewed}
}
```

Section 10.6 of the paper predates the deposit: its statement that no DOI has
been obtained refers to the planned OSF registration, not to this Zenodo DOI.
The frozen manuscript and deposited PDF are unchanged; see [`ERRATA.md`](ERRATA.md)
for the full correction and the affected locations.

## Repository map

| Path | Contents |
|---|---|
| [`manuscript/paper.pdf`](manuscript/paper.pdf) | Typeset 20-page pilot-study preprint. |
| [`manuscript/paper.tex`](manuscript/paper.tex) | LaTeX source for the typeset paper. |
| [`manuscript/paper.md`](manuscript/paper.md) | Markdown manuscript, consistent with the PDF. |
| [`manuscript/abstract.md`](manuscript/abstract.md) | Abstract and keywords. |
| [`manuscript/references.bib`](manuscript/references.bib) | BibTeX entries for cited work. |
| [`manuscript/tables/`](manuscript/tables/) | Six generated tables in Markdown and CSV. |
| [`manuscript/figures/`](manuscript/figures/) | Three generated SVG figures and source CSVs. |
| [`manuscript/submission/`](manuscript/submission/) | Venue comparison, cover-letter draft, checklist, and reviewer expertise. |
| [`manuscript/registered_report/`](manuscript/registered_report/) | Stage 1 outline for ICSME/EMSE 2027 and the registration plan. |
| [`docs/`](docs/) | Static research website, published with GitHub Pages from `main` `/docs`. |
| [`PROTOCOL.md`](PROTOCOL.md) | Research protocol and planned full-scale design. |
| [`rubric_v1.1.md`](rubric_v1.1.md) | Frozen coding instrument and boundary rules. |
| [`pilot/pilot_coding_table.csv`](pilot/pilot_coding_table.csv) | Authoritative 12-row pilot coding table. |
| [`pilot/pilot_summary.md`](pilot/pilot_summary.md) | Pilot flow, results, reliability, and caveats. |
| [`reproducibility/human_coding/`](reproducibility/human_coding/) | Blinded instructions, blank coder sheets, and the public coder call. |
| [`data/citation_frame_2666.csv`](data/citation_frame_2666.csv) | Frozen 2,666-cluster citation frame. |
| [`data/frame_summary.json`](data/frame_summary.json) | Frame counts, coverage, and SHA-256 hashes. |
| [`reproducibility/`](reproducibility/) | Data dictionary, provenance, sampling, environment, licensing, checksums, and reproduction. |
| [`scripts/`](scripts/) | Frame construction, sampling, pilot analysis, table and figure generation, and checksum verification. |
| [`tests/`](tests/) | Integrity and consistency tests for the frame, pilot, tables, figures, manuscript, and research website. |
| [`verification/`](verification/) | Source verification and journal-requirement records. |
| [`planning/`](planning/) | Feasibility, roadmap, risks, decision record, and Stage 2 readiness. |
| [`RESEARCH_PORTFOLIO.md`](RESEARCH_PORTFOLIO.md) | One-page research portfolio summary. |

## Licenses

- **Code:** [MIT](LICENSE)
- **Original documentation, rubric, manuscript, and derived data:** [CC BY 4.0](LICENSE-DATA)
- **Citation-frame metadata:** not relicensed; see
  [`reproducibility/licensing.md`](reproducibility/licensing.md).

Third-party benchmarks and papers retain their own licenses. No full texts are
redistributed.

---

**Author:** Syed Abdul Aman (Independent Researcher)  
**Maintainer:** [P-r-e-m-i-u-m](https://github.com/P-r-e-m-i-u-m)
