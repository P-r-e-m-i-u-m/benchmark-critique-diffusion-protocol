# Coding Schema

The authoritative instrument is `rubric_v1.1.md`. This file summarizes the fields
used in `pilot/pilot_coding_table.csv` and the rules that determine eligibility.

## 1. Construct

**Documented adoption:** the extent to which a citing paper's own evaluation of
the criticized benchmark uses the critique's recommended artifact or protocol, as
stated in the paper's text, tables, or captions.

It is not citation frequency, agreement with the critique, general evaluation
quality, independent remediation, or verified execution.

## 2. Primary and secondary pairs

| ID | Critique | Criticized benchmark | Recommended practice | Role |
|---|---|---|---|---|
| P1 | EvalPlus | HumanEval, MBPP | HumanEval+/MBPP+ augmented tests as primary evaluation | Primary |
| P2 | SWE-bench+ | SWE-bench, Lite, Verified | 548-instance SWE-bench+ dataset and/or strengthened-test protocol as primary evaluation | Primary |
| S1 | GSM1k | GSM8K | GSM1k or equivalent contamination-controlled replication | Secondary only |

GSM1k is never pooled into the primary estimate.

## 3. Eligibility (decided before scoring)

- **E1:** reports empirical evaluation results on the criticized benchmark.
- **E2:** cites the critique paper or official artifact.
- **E3:** English full text with enough methods/results detail to code.

A paper evaluating only a derivative benchmark (SWE-bench Pro, CWEval) is
ineligible. A paper evaluating both the original and a derivative is eligible and
the original is coded.

## 4. Ordinal score

| Score | Label | Definition |
|---:|---|---|
| 0 | Citation only | Reference-list entry; no specific finding discussed; benchmark unchanged. Generic contamination/leakage mention is 0. |
| 1 | Acknowledged | Specific finding mentioned, but evaluation unchanged. |
| 2 | Partial adoption | Recommended practice used in a secondary role (appendix, robustness check, subset), not the main result. |
| 3 | Full adoption | Recommended artifact/protocol supports at least one main claim/table/figure, with the critique cited as the basis. |

The binary primary outcome is score 3. Scores 0–2 are non-adoption for the primary
estimate. Partial adoption is reported separately and tested as 2+3 versus 0+1.

## 5. Secondary fields

| Field | Values | Meaning |
|---|---|---|
| `engagement` | 0, 1, 2 | Reference only / brief mention / substantive discussion. |
| `independent_remediation` | true, false | Paper strengthened evaluation without adopting the critique's artifact. |
| `evidence_quote` | string | Verbatim quote ≤60 words or reference entry supporting the score. |
| `notes` | string | Boundary decision and rationale. |
| `benchmark_version` | string (full study) | Version named by the paper. Recorded, not scored. |
| `critique_version` | string (full study) | Version of the critique/artifact. |
| `confidence` | high/medium/low (full study) | Low-confidence cases go to adjudication. |

## 6. Boundary rules

1. Citation is not adoption.
2. Generic contamination talk is not acknowledgment.
3. Acknowledgment requires the critique's specific finding.
4. Independent remediation is not adoption.
5. Full adoption requires use in the main evaluation.
6. Co-primary use counts as full if the augmented result supports a main claim.
7. Derivative-only papers are ineligible.
8. Benchmark version is recorded, not scored.
9. Code inspection can corroborate but not upgrade a score.
10. Self-citation is coded normally and flagged for sensitivity analysis.
11. Unresolved ambiguity uses the conservative lower score and is flagged.

## 7. Reliability

The pilot's agreement statistics are LLM–LLM only:

- eligibility agreement 12/12,
- ordinal agreement 7/8,
- unweighted κ = 0.78,
- linear-weighted κ = 0.86.

These are not human inter-rater reliability. No human second coder participated.
The full study requires human double-coding of at least 20% of eligible papers,
calibration, adjudication, and a 10% audit.

### 7.1 Pilot human double-coding package

The repository now contains the preparation for a human reliability check on the
12 pilot rows:

- `reproducibility/human_coding/README.md`: coder instructions, blinding rules,
  and the field guide;
- `reproducibility/human_coding/coder_A.csv` and `coder_B.csv`: blank sheets with
  the pilot metadata filled and every coding field cleared;
- `scripts/agreement.py`: the agreement calculator.

The sheets keep `paper_key`, `title`, `venue`, `year`, and `critique`. Coders fill
`eligible`, `ineligibility_reason`, `score`, `engagement`,
`independent_remediation`, `adoption_locus`, `evidence_quote`, `notes`,
`confidence`, `adjudicate`, `access_route`, and `coded_at`. The agreement script
requires `paper_key`, `critique`, `eligible`, and `score`; it validates
`ineligibility_reason` when the column is present.

The comparison is strict. A missing or duplicate `paper_key` + `critique` key is
an error; the script does not silently drop rows or intersect the sheets.
Eligibility is compared on every row. Ordinal κ is computed only on rows that
both coders mark eligible. Ineligible rows never receive a score.

The script reports percent agreement, unweighted κ, linear-weighted κ,
quadratic-weighted κ, PABAK, bootstrap percentile intervals, a confusion matrix,
and a CSV of disagreements. Weighted κ uses the 0–3 scale, so a 0-versus-3
disagreement counts more than a 0-versus-1 disagreement.

**Undefined κ.** If expected agreement is 1.0, κ has no denominator. The script
reports `null` and explains why. It does not substitute 1.00. The pilot's 1.00
eligibility value was a documented convention for a no-variance LLM–LLM check,
not an estimate, and it should not be used as a template for human κ.

**What the package does not do.** It cannot verify that the sheets came from two
independent humans, and it cannot make n=12 precise. The pilot human κ remains
unavailable until a second human completes the sheet. Until then, the only
reliability values in this repository are the LLM–LLM values above.

## Worked coding example

See [`coding_example.md`](coding_example.md) for a worked example showing
eligibility decisions, adoption scoring, counterfactual boundary cases, and
common coding misreads.
