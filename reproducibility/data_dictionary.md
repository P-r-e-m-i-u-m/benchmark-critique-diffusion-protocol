# Data Dictionary

## 1. `data/citation_frame_2666.csv`

One row per title-level citing work. Frozen on 13 November 2026.

| Column | Type | Description |
|---|---|---|
| `cluster_id` | string | Stable cluster identifier (`C0001`–`C2666`). |
| `stratum` | string | `SWE_bench_plus_census` (135 rows) or `EvalPlus_only_sample` (2,531 rows). |
| `title` | string | Representative title for the title cluster. |
| `year` | integer or empty | Publication year from the representative record. |
| `publicationDate` | string or empty | ISO date from Semantic Scholar, when present. |
| `venue` | string or empty | Venue name from the representative record. |
| `doi` | string or empty | Lowercased DOI, when present. |
| `arxiv` | string or empty | arXiv identifier, when present. |
| `dblp` | string or empty | DBLP key, when present. |
| `corpusId` | string or empty | Semantic Scholar CorpusId. |
| `paperId` | string | Semantic Scholar paperId for the representative record. |
| `cites` | string | Source label(s): `evalplus`, `swebenchplus`, or both joined by `+`. |
| `n_title_variants` | integer | Number of identifier-deduplicated records merged into this title cluster. |

Rows sum to 2,666. Strata sum to 2,666. The `cites` split is 2,531
EvalPlus-only, 112 SWE-bench+-only, and 23 both. The 23 both-critique clusters
are assigned to the SWE-bench+ census stratum.

## 2. `data/frame_summary.json`

Machine-readable summary of the frame build: raw row counts, identifier-deduplicated
count, title clusters, strata, year counts, identifier coverage, anomaly counts,
and SHA-256 hashes.

## 3. `pilot/pilot_coding_table.csv`

One row per coded pilot paper (12 rows).

| Column | Type | Description |
|---|---|---|
| `paper_key` | string | Short anonymized project key used in the manuscript. |
| `title` | string | Published title. |
| `venue` | string or empty | Venue as recorded during coding. |
| `year` | integer or `unknown` | Publication year as recorded. |
| `critique` | string | `evalplus`, `swebenchplus`, or `gsm1k`. |
| `eligible` | boolean | `true` or `false` after applying E1–E3. |
| `ineligibility_reason` | string or empty | `NO_EVAL` for the four ineligible rows. |
| `score` | integer 0–3 or empty | Adoption score; empty for ineligible rows. |
| `engagement` | integer 0–2 | 0 = reference only, 1 = brief mention, 2 = substantive discussion. |
| `independent_remediation` | boolean | Whether the paper remediated evaluation without adopting the critique's artifact. |
| `evidence_quote` | string | Short verbatim quote (≤60 words) or reference entry supporting the code. |
| `notes` | string | Boundary decision and coding rationale. |

The four ineligible rows have a blank `score` in the CSV. They are **not**
adoption outcomes and are excluded from every denominator.

## 4. `analysis/pilot_results.json`

Generated from the coding table by `scripts/analyze_pilot.py`.

| Field | Description |
|---|---|
| `source.pilot_coding_table_sha256` | SHA-256 of the coding table used. |
| `flow` | Purposive frame 29, accessible 27, coded 12, eligible all-pair 8, eligible primary 6, ineligible 4. |
| `primary_pair` | Distribution, full-adoption proportion, Wilson 95% CI, acknowledgment, independent remediation, engagement, exact-binomial diagnostics. |
| `all_pair` | Same quantities including the two GSM1k secondary rows. |
| `by_critique` | `evalplus`, `swebenchplus`, `gsm1k` descriptive splits. |
| `by_year` | Descriptive splits for 2025 and unknown year. |
| `reliability` | LLM–LLM agreement only; explicitly not human reliability. |
| `interpretation_rules` | Hard rules that forbid prevalence and causal claims. |

## 5. `manuscript/figures/*.csv`

Source data for the three SVG figures. `fig1_frame_years.csv` uses frame counts;
`fig2_pilot_flow.csv` and `fig3_pilot_scores.csv` use pilot results.

## 6. `manuscript/tables/*.csv`

Machine-readable versions of the six manuscript tables. The Markdown versions are
generated from the same inputs by `scripts/make_manuscript_tables.py`.

## 7. `data/cohort_feasibility.csv`

The 335-record feasibility draw (135 SWE-bench+ census + 200 EvalPlus-only, seed
`20261113`). It is a documented deviation from the 900-paper design. It was drawn
but **not coded**, and no results from it appear in the manuscript. It is included
so the deviation is auditable.

## 8. `reproducibility/human_coding/coder_A.csv` and `coder_B.csv`

Blank double-coding templates for the 12 pilot rows. The first five columns are
copied from `pilot/pilot_coding_table.csv`; every coding field is empty so the
sheet cannot be mistaken for completed data.

| Column | Type | Description |
|---|---|---|
| `paper_key` | string | Pilot key; part of the agreement key. |
| `title` | string | Published title. |
| `venue` | string or empty | Venue as recorded in the pilot. |
| `year` | integer or `unknown` | Publication year as recorded. |
| `critique` | string | `evalplus`, `swebenchplus`, or `gsm1k`; second part of the agreement key. |
| `eligible` | boolean | Filled by the coder: `true` or `false`. |
| `ineligibility_reason` | string or empty | `NO_EVAL`, `NO_CITATION`, `ACCESS`, `LANGUAGE`, or `DUPLICATE`; blank when eligible. |
| `score` | integer 0–3 or empty | Adoption score; blank when ineligible. |
| `engagement` | integer 0–2 or empty | 0 = reference only, 1 = brief mention, 2 = substantive discussion. |
| `independent_remediation` | boolean or empty | Whether the paper strengthened evaluation without adopting the critique's artifact or protocol. |
| `adoption_locus` | string or empty | `main_results`, `secondary_results`, `appendix`, `future_work`, `related_work`, or `none`. |
| `evidence_quote` | string or empty | Verbatim quote (≤60 words) supporting the code. |
| `notes` | string or empty | Section/table/page, boundary decision, and adjudication context. |
| `confidence` | string or empty | `high`, `medium`, or `low`. |
| `adjudicate` | string or empty | `yes` or `no`. |
| `access_route` | string or empty | `publisher`, `arxiv`, `author_copy`, `repository`, `ill`, or `html`. |
| `coder_id` | string | Pre-filled as `A` or `B`; not a person identifier. |
| `coded_at` | date or empty | ISO date the sheet was completed. |

Completed sheets are saved as `coder_A_completed.csv` and
`coder_B_completed.csv` and are gitignored. They are not in the checksum manifest.

## 9. `analysis/human_coding/agreement_report.json`

Generated by `scripts/agreement.py` from two completed sheets. Keys must match
exactly; a missing or duplicated `paper_key` + `critique` aborts with exit code 2.

| Field | Description |
|---|---|
| `inputs` | Each sheet's path, SHA-256, row count, and display label. |
| `key_count` | Number of compared keys. |
| `eligibility` | Agreement, unweighted κ, PABAK, bootstrap interval, and 2×2 confusion matrix over all rows. |
| `ordinal` | Same statistics plus linear- and quadratic-weighted κ over rows both coders marked eligible, plus each coder's score distribution. |
| `disagreements` | Per-row eligibility, score, or reason disagreements with both coders' notes and quotes. |
| `identity_checks` | File hashes, observed `coder_id` values, and warnings for byte-identical sheets or overlapping IDs. These are process warnings, not proof of independence. |
| `caveats` | Fixed statements about independence, sample size, and undefined κ. |

A `kappa` value of `null` means expected agreement was 1.0, so κ is undefined;
`kappa_note` explains this. The script never substitutes 1.00.

`agreement_report.md` is a human-readable rendering of the same report.
`agreement_disagreements.csv` has one row per disagreement with fields
`paper_key`, `critique`, `disagreement_type`, both coders' eligibility, score,
reason, engagement, confidence, evidence quote, and notes, plus `score_gap` for
score disagreements.

