# Submission Checklist

**Current verdict: NOT READY TO SUBMIT.** The manuscript is a pilot-based draft.
The table distinguishes what exists from what is missing.

## 1. Scientific prerequisites

| Item | Status | Evidence / action |
|---|---|---|
| Frozen citation frame | **Complete** | `data/citation_frame_2666.csv`; SHA-256 verified. |
| Coding rubric | **Complete** (v1.1) | `rubric_v1.1.md`. |
| Pilot data | **Complete** (12 rows) | `pilot/pilot_coding_table.csv`. |
| Pilot analysis | **Complete** | `analysis/pilot_results.json`; tests. |
| Full-scale 900-paper sample | **Not executed** | `reproducibility/sampling.md`. |
| Human-coding packet | **Complete** | `reproducibility/human_coding/`: instructions, two blinded blank sheets, agreement script, tests. |
| Human second coder | **Not recruited** | The packet is ready; recruitment is the blocker. |
| Human reliability statistics | **Not available** | Must not substitute LLM–LLM κ. Run `scripts/agreement.py` after both sheets are returned. |
| Pre-specified sensitivity analyses | **Planned, not run** | Paper §14.5; no full data. |
| OSF registration | **Not created** | Paper §10.6. |
| DOI | **Obtained** | Zenodo: `10.5281/zenodo.24245000` (preprint and materials). |

## 2. Manuscript package

| Item | Status | Notes |
|---|---|---|
| Main manuscript | **Pilot draft complete** | `manuscript/paper.md`. |
| Abstract 150–250 words | **Complete** | `manuscript/abstract.md`; recheck count after edits. |
| Keywords | **Complete** | Six keywords. |
| References | **Complete for pilot** | `manuscript/references.bib`; spot-check before submission. |
| Tables | **Complete** (6) | Markdown + CSV; generated. |
| Figures | **Complete** (3) | SVG + source CSV; generated. |
| Reproducibility statement | **Complete** | `manuscript/reproducibility_statement.md`. |
| Limitations checklist | **Complete** | `manuscript/limitations_checklist.md`. |
| Data availability statement | **Complete** | Paper §20.3. |
| Code availability statement | **Complete** | Paper §20; repository. |
| LLM-use disclosure | **Complete with caveat** | Model metadata not preserved. |
| Ethics/IRB determination | **Not documented** | Confirm local policy. |
| Author affiliation/contact | **Partial** | Independent researcher; public contact to confirm. |
| Cover letter | **Draft only** | Do not send. |
| Suggested reviewers | **Not prepared** | Expertise categories only. |

## 3. Venue-specific checks

| Check | EMSE | DMLR | Scientometrics | QSS |
|---|---|---|---|---|
| Current review model verified | Yes (single-blind) | Yes (single-blind) | Yes (single-blind) | **No (403)** |
| Abstract limit | 150–250 | Not specified | 150–250 | Unknown |
| Data statement requirement | Required | Expected | Supported/required | Unknown |
| Fee/APC verified | Hybrid; Open Choice amount not stated | No fees | Hybrid | **Unresolved** |
| Live-page re-verification at submission | Pending | Pending | Pending | Pending |

## 4. Repository checks

| Item | Status |
|---|---|
| Tests pass | **Yes** (see final test report) |
| Checksums pass | **Yes** (see `reproducibility/checksums.sha256`) |
| No PDFs or full texts committed | **Yes** |
| No credentials or API keys | **Yes** |
| Third-party abstract CSV excluded | **Yes** (`data/cohort_arxiv_metadata.csv`) |
| Licenses present | **Yes** (`LICENSE`, `LICENSE-DATA`) |
| README status warning | **Yes** |
| Manuscript status warning | **Yes** |
| Human-coding templates tracked, completed sheets ignored | **Yes** |
| No fabricated full-scale results | **Yes** |

## 5. Hard blockers

1. No human second coder has been recruited, so there are no human reliability
   statistics. The packet and agreement script exist; the missing input is a
   person, not code.
2. No full-scale sample, coding, or prevalence estimate.
3. No registration; the Zenodo DOI covers the preprint but is not a preregistration.
4. The manuscript is not peer reviewed.

## 6. Acceptable alternative

If the author does not want to run the full study, the honest alternative is a
short **pilot/methods paper** that presents the rubric, frame, and pilot as
instrument-development work, explicitly without a prevalence estimate. That paper
would still need a human second coder for the reliability claim, or it must omit
reliability and be framed as a feasibility study. The current manuscript is closer
to that alternative but still labels itself a full-study draft; it must be
shortened and reframed before any submission.
