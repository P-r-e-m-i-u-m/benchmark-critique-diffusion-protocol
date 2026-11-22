# Sampling

## 1. Planned full-study design (not executed)

| Stratum | Frame N | Planned sample | Design weight |
|---|---:|---:|---:|
| SWE-bench+ census (includes 23 both-critique clusters) | 135 | 135 | 1.000 |
| EvalPlus-only | 2,531 | 765 | 3.308 |
| **Total** | **2,666** | **900** | — |

The EvalPlus-only sample is allocated proportionally by publication year (2022
collapsed into 2023, minimum 10 per non-empty stratum where possible), with a
fixed seed committed at registration.

### Planning assumptions

- Full-adoption planning value: p = 0.125 (from the all-pair pilot).
- Access rate: 80%.
- Eligibility among accessible papers: 18%.
- Expected eligible papers: 900 × 0.80 × 0.18 ≈ 130.
- Expected Wilson 95% CI half-width: about 5.7 percentage points (7.7–19.1%).

These are design calculations, not observed values.

### Stop rule

Sample and code in blocks. Start with 900 invited. If fewer than 120 eligible
papers are found, add blocks of 100 EvalPlus-only records up to a hard cap of
1,200 invited. Stop when 120 eligible papers are reached. If the cap is reached
with fewer than 120 eligible, report the realized count and do not extend without
a protocol amendment.

### Status

**Not executed.** No 900-paper sample was drawn, no main coding began, and no
full-scale estimate exists.

The draw is gated on the registration route. Under the ICSME 2027 / EMSE
Registered Report route, the accepted Stage 1 protocol is the registration; an
OSF DOI is not required. Under an independent route, an OSF DOI is required
before the draw. `scripts/sample_frame.py` accepts either route:

```
python scripts/sample_frame.py --design registered \
    --frame data/citation_frame_2666.csv \
    --out data/sample_900.csv --seed <committed-seed> \
    --stage1-acceptance <accepted-stage1-reference>
```

`--allow-unregistered` exists only for a labelled local dry run. It must not be
used for the study sample. The 900-row draw is covered by `tests/test_sampling.py`:
the test draws with a placeholder seed into a temporary directory and checks the
135 + 765 split and the design weight, but commits no sample.

## 2. Pilot design

The pilot is a purposive 29-paper access frame, not a probability sample. It was
selected to exercise different benchmarks and likely adoption levels:

- 29 papers in the access frame,
- 27 accessible full texts (93.1%),
- 12 coded,
- 8 eligible for the all-pair set,
- 6 eligible for the primary pairs,
- 4 ineligible.

The 93.1% access rate applies only to this purposive frame and must not be
generalized to the 2,666-paper frame.

## 3. Feasibility cohort (documented deviation)

A 335-record cohort was drawn to test retrieval beyond the pilot:

| Stratum | N | Design weight |
|---|---:|---:|
| SWE-bench+ census | 135 | 1.000 |
| EvalPlus-only | 200 | 12.655 |
| **Total** | **335** | — |

- Seed: `20261113`.
- Frame SHA-256: `4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0`.
- Manifest: `data/cohort_feasibility.manifest.json`.
- Records coded: **0**.
- Retrieval: halted before completion.

The cohort is not the registered sample and contributes no result to the
manuscript. It is retained so the deviation is auditable.

## 4. Reproduction

`scripts/sample_frame.py` implements the stratified draw. Because the planned
900-paper sample was never executed, running it now produces a new draw and must
not be described as the study's sample. A registered-route run requires either
`--osf-doi` or `--stage1-acceptance`; a run without either is refused. The
335-record cohort can be regenerated from the manifest and seed; it predates the
Stage 1 gate and is labelled as an unregistered feasibility deviation.

The frame hash and the seed are the two values that make the draw auditable. The
seed is committed only when the registration is accepted, and the resulting
manifest records the registration route and reference alongside the frame hash.
