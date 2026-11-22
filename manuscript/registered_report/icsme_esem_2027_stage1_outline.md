# Registered Report — Stage 1 Outline

**Title:** Does Benchmark Critique Diffuse into Evaluation Practice? A Registered
Report on Documented Adoption of EvalPlus and SWE-bench+

**Author:** Syed Abdul Aman, Independent Researcher

**Target:** ICSME 2027 Registered Reports (primary). ESEM 2027 Registered Reports
is a format-compatible fallback, but its track details were not verifiable at the
time of writing (the track URL returned 404); this outline follows the verified
ICSME 2027 requirements.

**Format:** IEEE two-column conference, `\documentclass[conference]{IEEEtran}`,
6 pages plus 1 additional page of references, single-blind.

**Status of this file:** Working draft, not the submission PDF. It contains the
section-by-section page budget, drafted prose, table shells, and a pre-submission
checklist. The 6-page budget excludes this header and the appendices.

**Evidence status:** The 12-paper pilot is preliminary feasibility data only. It
does not estimate prevalence, does not establish human reliability, and does not
test the confirmatory hypotheses.

---

## Page budget

| Element | Draft words | Pages |
|---|---:|---:|
| Title, abstract, index terms | 260 | 0.27 |
| 1. Introduction | 400 | 0.40 |
| 2. Preliminary pilot study + Table 1 | 620 | 0.80 |
| 3. Research questions, hypotheses, design + Table 2 | 600 | 0.78 |
| 4. Sampling, frame, and access + Figure 1 | 700 | 0.85 |
| 5. Coding instrument and human reliability + Table 3 | 760 | 0.90 |
| 6. Analysis plan | 510 | 0.55 |
| 7. Threats to validity and ethics | 306 | 0.33 |
| 8. Timeline, feasibility, and deliverables + Table 4 | 430 | 0.45 |
| **Body total** | **4,586** | **5.33** |
| Buffer for typesetting | — | 0.67 |
| **Body limit** | | **6.00** |
| References (page 7 only) | 17 entries | 1.00 |
| **Total** | | **7.00** |

The body must end on page 6. References start on page 7 and may use that page
only. Figures and tables count toward the 6 pages.

---

## Abstract (draft, 250 words)

Benchmark critiques identify concrete defects in widely used evaluations and
usually release a remediation: stronger tests, filtered instances, or a
contamination-controlled dataset. Citation counts show that a critique was
noticed; they do not show that citing papers changed their own evaluation
practice. This Registered Report proposes a confirmatory audit of documented
adoption for two code-generation remediations: EvalPlus, which augments HumanEval
and MBPP with additional tests, and SWE-bench+, which releases a filtered
548-instance SWE-bench dataset and a strengthened-test protocol. The unit of
analysis is a title-level citing work by critique. The primary outcome is full
adoption (rubric score 3) among eligible citing papers. We pre-specify two
confirmatory hypotheses: full adoption is uncommon (<25%), and most eligible
papers are citation-only or acknowledged (scores 0–1). A 12-paper pilot
established feasibility, boundary rules, and planning values, but it is purposive
and cannot estimate prevalence; it is reported only as preliminary data. The full
study will draw 900 papers from a frozen frame of 2,666 title clusters—a census of
the 135 SWE-bench+ clusters plus a random sample of 765 EvalPlus-only
clusters—targeting 120 eligible papers, with a hard cap of 1,200 invited. An
independent human coder will double-code 20% of eligible papers; we will report
Cohen's κ and weighted κ with bootstrap confidence intervals and will not treat
LLM agreement as human reliability. Stage 2 will report pair-specific and weighted
prevalence with Wilson intervals, ten pre-specified sensitivity analyses, and
access-failure bounds. The contribution is a human-validated instrument
measuring whether critique changes practice, not a citation count.

**Index Terms:** benchmark evaluation, benchmark critique, EvalPlus, SWE-bench+,
citation diffusion, meta-research, reproducibility, code generation.

---

## 1. Introduction

Benchmarks are infrastructure for empirical claims about code-generation
systems. When a benchmark is defective, a critique can identify the defect and
release a remediation. EvalPlus augments HumanEval [1] and MBPP [2] with
additional tests and a harness; SWE-bench+ releases a filtered 548-instance
dataset and a strengthened-test protocol for SWE-bench [3], [4], [5]. In both
cases, the scientific value of the critique depends on whether later evaluations
change. A citation count records attention. It does not record whether a citing
paper used the augmented tests or the filtered dataset in its own main results.

The gap is empirical. We lack systematic evidence on *documented adoption* of a
critique's remediation in code-generation evaluations, and we lack a
human-validated instrument for measuring it. The closest prior work studies
documentation and accessibility of non-English NLP benchmarks, not the adoption
of a critique's remediation in code-generation practice, and it is unpublished
replication material rather than a peer-reviewed antecedent [7]. Citation-diffusion
research explains why citation and use can diverge [8], and reproducibility work
documents how leakage and benchmark defects persist [9], but neither supplies a
confirmatory estimate for these two remediations.

The two cases are a useful contrast. EvalPlus is a comparatively drop-in
remediation: a lab can run HumanEval+/MBPP+ and report pass rates. SWE-bench+
requires a different instance set, harness reconciliation, and agent re-runs. If
adoption is low even for a drop-in artifact, the diffusion problem is not merely
tooling cost. If adoption is high for EvalPlus and low for SWE-bench+, the
contrast points to integration cost and benchmark-version inertia. That contrast
is descriptive; this study does not identify a causal effect.

This Registered Report asks: among research papers that cite a benchmark
remediation critique, what proportion document adopting the critique's recommended
benchmark or protocol in their own evaluation of the criticized benchmark? We
answer with a frozen citation frame, a probability sample, a four-level rubric,
human double-coding, and a pre-specified analysis plan. The contribution is four
things: (i) a confirmatory prevalence estimate in a defined frame; (ii) an
instrument with boundary rules that separate citation, acknowledgment, partial
adoption, full adoption, and independent remediation; (iii) human reliability
evidence, not LLM–LLM agreement; and (iv) open materials that make the estimate
auditable. The study does not claim that a citation causes adoption, that
documented use was executed correctly, or that the results generalize to every
benchmark. The 12-paper pilot is reported in Section 2 as feasibility evidence
only.

---

## 2. Preliminary pilot study

### 2.1 Design and flow

The pilot used a purposive 29-paper access frame drawn from papers citing
EvalPlus, SWE-bench+, or GSM1k [6]. Full text was accessible for 27 papers (93.1%).
Twelve papers were coded with rubric v1.0; the remaining accessible papers were
used for access testing or were not needed after category saturation. Eight
papers were eligible for the all-pair set, and six for the two primary pairs.
Ineligible rows received no score. Table 1 reports the flow and the planning
values used in this protocol.

**Table 1. Pilot flow and planning values.** Intervals are Wilson 95% CIs.

| Quantity | Pilot result | Use in this Registered Report |
|---|---|---|
| Purposive access frame | 29 | Not used for inference |
| Full text accessible | 27 (93.1%) | 80% base access; 70% pretest gate |
| Coded | 12 | Excluded from confirmatory sample |
| Eligible, all pairs | 8 | 18% base eligibility |
| Eligible, two primary pairs | 6 | — |
| Full adoption, primary | 1/6 = 16.7% (3.0–56.4) | Not used; n too small |
| Full adoption, all pairs | 1/8 = 12.5% (2.2–47.1) | Planning value p = 0.125 |
| Ordinal agreement | 7/8; κ 0.78 / 0.86 | Rubric debugging only |
| Eligibility agreement | 12/12; κ undefined | Report as null, not 1.00 |

### 2.2 What the pilot observed

Among the six primary-pair papers, one fully adopted the remediation
(`whatswrong`, EvalPlus), three acknowledged it without changing their evaluation,
and two cited it without specific engagement; no paper was coded partial. The
primary-pair estimate was 1/6 = 16.7% (Wilson 95% CI 3.0–56.4). The all-pair
estimate, which adds two GSM1k cases, was 1/8 = 12.5% (2.2–47.1). Three of the six
primary-pair papers independently remediated the benchmark without adopting the
critique's artifact; none of the three SWE-bench+ cases used the 548-instance
dataset. These are descriptions of a purposive set, not estimates of prevalence.

### 2.3 Reliability was LLM–LLM, not human

The pilot's two coding passes were LLM annotations with fresh contexts. They
agreed on eligibility for 12/12 papers; eligibility κ is undefined because there
was no variance, and is reported as `null`, not 1.00. Ordinal agreement was 7/8
with unweighted κ = 0.78 and linear-weighted κ = 0.86. No human second coder
participated. These values are a rubric-debugging signal, not human inter-rater
reliability, and they will not be reused as a reliability estimate in Stage 2.

### 2.4 What the pilot licenses

The pilot licenses four planning choices. First, it supports a conservative
planning value of p = 0.125 for full adoption, taken from the all-pair estimate
because the primary-pair n is too small to prefer 16.7%. Second, it supports a
base-case access rate of 80%, not the pilot's 93.1%, because the pilot frame was
chosen partly for accessibility. Third, it supports a base-case eligibility rate
of 18% and a workload estimate of 20 minutes per eligibility screen and 30
minutes per eligible paper; both are estimates to validate in calibration.
Fourth, it identified the boundary problems that rubric v1.1 resolves: generic
contamination clusters, independent remediation, derivative-only evaluations,
partial versus full adoption, and co-primary use of original and augmented
benchmarks.

### 2.5 What the pilot does not license

The pilot does not estimate prevalence in the 2,666-cluster frame, does not
establish human reliability, does not support the EvalPlus/SWE-bench+ contrast,
and does not estimate time or venue gradients. It also does not show that the
93.1% access rate generalizes. The confirmatory sample therefore excludes the
pilot clusters; if a pilot cluster would be sampled, the next record in the same
stratum replaces it. The pilot is reported as preliminary feasibility data, not
as a test of H1 or H3.

---

## 3. Research questions, hypotheses, and design

### 3.1 Research question and estimand

The primary research question is: among eligible citing papers in the frozen
frame, what proportion document full adoption of the critique's recommended
artifact or protocol in their own evaluation of the criticized benchmark? The
estimand is the proportion with rubric score 3 among eligible citing-work ×
critique rows, reported separately for EvalPlus and SWE-bench+ and pooled with
stratum weights. A paper citing both critiques contributes two rows; a paper
evaluating multiple criticized benchmarks contributes one score per critique,
based on the highest-adoption use that supports a main claim.

### 3.2 Confirmatory hypotheses

**H1 (primary).** Full adoption is uncommon among eligible citing papers:
less than 25%. The 25% threshold is a substantive "rare versus common" boundary
chosen before data collection, not a pilot estimate. H1 is tested with a
one-sided exact binomial test against 0.25. We report the prevalence and its
Wilson 95% CI and reject the null if the upper confidence bound is below 25%, or
if p < .05 in the pre-specified direction. With 130 eligible papers and a true
proportion of 12.5%, the one-sided test has approximately 98% power, and the
upper Wilson bound falls below 25% with approximately 95% probability. These are
planning calculations, not results.

**H3 (secondary confirmatory).** Most eligible papers are citation-only or
acknowledged (scores 0–1), not partial or full adopters. H3 is tested with a
one-sided exact binomial test against 0.50 on the combined 0/1 proportion. With
130 eligible papers and a true 0/1 proportion of 0.65, the test has approximately
97% power; at 0.70, power is above 99%. The pilot's 5/6 primary-pair 0/1
proportion is a planning value only.

### 3.3 Exploratory hypotheses

**H2.** Full adoption is more common for EvalPlus than for SWE-bench+. The test
is Fisher's exact test with a risk difference and Newcombe CI [12]. H2 is
exploratory because the SWE-bench+ stratum is small even under a census; the
study can describe a contrast but cannot confirm one.

**H4.** Adoption is more common at least 12 months after critique release and in
peer-reviewed venues. H4 is descriptive. A logistic regression is fitted only if
there are at least 10 outcome events per estimated parameter; otherwise the study
reports stratified rates and does not fit a multivariable model.

Table 2 summarizes the hypotheses and decision rules. The distribution of scores
0–3, the rate of independent remediation, and the sensitivity analyses are
descriptive or robustness questions, not additional confirmatory tests.

**Table 2. Hypotheses and decision rules.**

| ID | Statement | Role | Test and decision rule |
|---|---|---|---|
| H1 | Full adoption <25% among eligible citing papers | Confirmatory (primary) | One-sided exact binomial vs 0.25; report prevalence + Wilson 95% CI; reject if upper bound <25% or p < .05 in the pre-specified direction |
| H3 | Most eligible papers are 0/1 | Confirmatory (secondary) | One-sided exact binomial vs 0.50 on (0+1)/eligible |
| H2 | EvalPlus adoption > SWE-bench+ adoption | Exploratory | Fisher exact; risk difference with Newcombe CI; no confirmatory claim |
| H4 | Adoption varies by time since critique and peer-review status | Exploratory | Descriptive rates; logistic only if ≥10 events per parameter |

### 3.4 Design

The design is a cross-sectional citation audit with a frozen frame and a
pre-specified sampling plan. The frame was frozen on 13 November 2026; new
citations after that date are out of scope. The study is observational: it
measures the co-occurrence of a citation and a documented evaluation practice.
It does not identify a causal effect of the critique, and it does not verify that
a reported artifact executed correctly. Registered Reports separate the pre-data
design from the post-data analysis [14], and preregistration reduces
unacknowledged researcher degrees of freedom [15].

---

## 4. Sampling, frame, and access

### 4.1 Frame construction

The frame was built from Semantic Scholar Graph API citations to the EvalPlus and
SWE-bench+ papers, retrieved on 13 November 2026 [17]. EvalPlus returned 2,572
citation rows and SWE-bench+ returned 136, for 2,708 raw rows. Identifier
union-find on DOI, arXiv ID, DBLP key, CorpusId, and Semantic Scholar paperId
produced 2,684 records; title normalization removed 18 more, leaving 2,666 title
clusters. Of these, 135 clusters cite SWE-bench+ (112 SWE-only and 23 citing both
critiques) and form the census stratum; 2,531 cite EvalPlus only and form the
sampled stratum. The 24 both-critique clusters contribute two rows, one per
critique.

### 4.2 Frame profile and data quality

The frame contains 2 clusters from 2022, 119 from 2023, 526 from 2024, 838 from
2025, 1,139 from 2026, and 42 with no publication date. Identifier coverage is
2,313 DOI, 2,028 arXiv, 2,129 DBLP, and 42 with none. The largest venue groups are
arXiv.org (974), unknown (331), ACL (110), EMNLP (82), TOSEM (71), NeurIPS (70),
ICLR (69), ASE (39), ICML (33), and ICSE (21). Three flags are reported rather
than silently cleaned: 225 clusters lack a publication date, 231 have a
publication date after 30 September 2026, and 14 clusters have multiple title
variants and require manual review. The identifier-deduplicated 2,684-record
frame is retained as a sensitivity check.

### 4.3 Sampling design

The target is 900 invited papers: a census of the 135 SWE-bench+ clusters plus a
random sample of 765 EvalPlus-only clusters. The EvalPlus-only sample is
allocated proportionally by year, with 2022 collapsed into 2023 and a minimum of
10 per stratum where possible, then drawn by simple random sampling within
stratum. The seed is committed when the Stage 1 protocol is accepted, and the
sampling script is versioned. Pilot clusters are excluded before sampling; the
script recomputes the stratum sizes and adjusts the EvalPlus-only sample so that
the total invited remains 900.

The base case assumes 80% access and 18% eligibility: 900 invited yields about
720 accessible papers and 130 eligible papers. At p = 0.125, the expected Wilson
95% CI is 7.7–19.1%, a half-width of 5.7 percentage points. The target is 120
eligible papers. If 900 invited yields fewer than 120, the study adds blocks of
100 EvalPlus-only records up to a hard cap of 1,200 invited, stopping as soon as
120 eligible papers are reached. The conservative case (70% access, 10%
eligibility) yields about 63 eligible papers and a half-width of 8.3 points; the
study reports that estimate with its wider interval rather than extending beyond
the cap without an amendment.

### 4.4 Access pretest and inclusion

Before main coding, the study draws 50 random frame records and attempts full-text
retrieval through open access, arXiv, author copies, publisher HTML, and any
library access the author can secure. No institutional subscription is assumed.
If at least 70% are retrievable, the design proceeds. If 50–70% are retrievable,
the study adds interlibrary loan and documents the shortfall. If fewer than 50%
are retrievable, the primary frame is restricted to open-access records and the
restriction is reported, or the study pauses.

A paper is eligible only if it reports empirical evaluation results on the
criticized benchmark (E1), contains a bibliographic citation to the critique
(E2), and has an English full text with enough methods/results detail to code
(E3). Ineligible papers receive no 0–3 score. Derivative-only evaluations
(SWE-bench Pro, CWEval, and similar) are ineligible; a paper evaluating both the
original and a derivative is eligible and is coded on the original. GSM1k remains
a secondary contrast and is never pooled into the primary estimate. Figure 1
reports the flow from frame to invited, retrieved, accessible, screened, eligible,
coded, and double-coded papers, with exclusion counts and reasons at each step.

**Figure 1 (placeholder).** Full-study flow diagram, one column: frozen frame
(2,666) → invited (900, plus 100-record blocks to a cap of 1,200) → retrieved →
accessible → screened → eligible (target 120) → coded → human double-coded (20%
of eligible). The diagram is generated from the coding log, not hand-edited.

### 4.5 Frame freeze

The frame is frozen before main coding. A post-freeze citation refresh may be
reported as a sensitivity analysis but cannot change the sampling frame. This
prevents denominator drift and selective inclusion. Any deviation from the
sampling plan is logged with date, reason, and impact.

---

## 5. Coding instrument and human reliability

### 5.1 Construct

*Documented adoption* is the extent to which a citing paper's own evaluation of
the criticized benchmark uses the critique's recommended artifact or protocol, as
stated in the paper's text, tables, or captions. It is not citation frequency,
agreement with the critique, general evaluation quality, independent remediation
that is not the critique's recommended practice, or verified execution of the
artifact. The unit is a title-level citing work by critique.

### 5.2 Rubric v1.1

Rubric v1.1 has four levels. Score 0 (citation only) means the critique appears
in the reference list or a generic cluster, but the body does not discuss its
specific finding or recommendation, and the criticized benchmark is used
unchanged. Score 1 (acknowledged) means the body states the critique's specific
finding, but the evaluation is unchanged. Score 2 (partial adoption) means at
least one recommended practice is applied, but not the core remediated artifact
or protocol for the main results. Score 3 (full adoption) means the core
remediated artifact or protocol supports at least one main table, figure, or
claim, with the critique cited as the basis. Table 3 gives the decision tests.

**Table 3. Rubric v1.1.**

| Score | Label | Decision test |
|---:|---|---|
| 0 | Citation only | Critique in reference list or generic cluster; no specific finding discussed; benchmark unchanged |
| 1 | Acknowledged | Specific finding discussed; evaluation unchanged |
| 2 | Partial adoption | Recommended practice used, but not for a main claim |
| 3 | Full adoption | Recommended artifact/protocol supports at least one main table, figure, or claim |

The binary primary outcome is score 3 versus 0–2. The pre-specified sensitivity
analysis treats 2+3 as adoption versus 0+1. Independent remediation is recorded
in a separate field and is never counted as adoption.

### 5.3 Boundary rules

Six rules decide the difficult cases. Citation alone is not adoption. Generic
contamination or leakage talk is not acknowledgment; the paper must state the
critique's specific finding or its implication for the paper's own evaluation.
Acknowledgment requires specificity. Partial adoption requires a recommended
practice, not any improvement; an independently designed stronger test suite is
coded as 1 (if the finding is discussed) with `independent_remediation=yes`.
Full adoption requires use in the main evaluation; appendix-only or
robustness-only use is 2. Derivative-only evaluations are ineligible. The coding
form also records benchmark version, critique version, author overlap, artifact
check, confidence, access route, and a verbatim evidence quote of at most 60
words. Code inspection can corroborate documented use but cannot upgrade a score
on its own. Unresolved ambiguity is adjudicated; if consensus fails, the
conservative lower score is used and the reason is recorded.

### 5.4 Human reliability

The author codes all papers. An independent human coder, who has not seen the
pilot codes, the pilot summary, or the manuscript's results section, double-codes
20% of eligible papers, stratified by critique and score band: 26 papers at the
base case of 130 eligible, and 16 at the reduced case of 81. Calibration uses 20
fresh papers that are not in the pilot, are excluded from the confirmatory
sample, and are replaced in the sampling frame. The second coder receives a
blinded packet with the first coder's scores
removed and codes independently before seeing them. Adjudication is a discussion,
not an average; if consensus fails, a third coder or the conservative rule
applies.

Reliability is reported as percent agreement and Cohen's κ for eligibility [10],
and as unweighted and linear-weighted κ for the ordinal score [13], with 95%
bootstrap confidence intervals. If prevalence is below 10%, PABAK is reported
alongside κ because κ is unstable under low variance. A weighted κ of at least
0.60 is acceptable for the main analysis; 0.40–0.59 is moderate and requires a
limitation paragraph; below 0.40 triggers retraining and recoding. These
thresholds are pre-specified. The pilot's LLM–LLM values are not reused.

An LLM may be used for pre-screening, flagging, or a second-pass audit, but never
as the human reliability coder. If an LLM is used, the study reports model,
version, prompt, temperature, date, and agreement with the human coder. Paywalled
full texts are not sent to external APIs; abstracts, metadata, or a local model
are used instead.

The second coder is a hard feasibility gate. If no independent coder is secured
before main coding, the study does not proceed to Stage 2 with a human reliability
claim. The fallback is a single-coder study with an LLM audit, reported as a
limitation, not as human reliability. The recruitment note and blinding packet
are prepared; the coder is not yet secured at the time of writing.

---

## 6. Analysis plan

### 6.1 Descriptive analysis

The study reports the frame profile, the realized flow (invited, retrieved,
accessible, screened, eligible, coded, double-coded), the score distribution
overall and by critique, the engagement and independent-remediation rates, the
adoption-locus distribution, and the access-route distribution. All counts are
reported with denominators; ineligible and uncodable papers are never assigned a
score.

### 6.2 Primary estimate

The primary estimate is the proportion of eligible citing-work × critique rows
with score 3. Pair-specific proportions are reported with Wilson 95% CIs [11].
The pooled estimate uses stratum weights: 1 for the SWE-bench+ census and
2,531/765 ≈ 3.308 for the EvalPlus-only sample; both-critique census rows carry
weight 1 for both rows. The analysis script recomputes the weights from the
realized frame after the pilot exclusions. The pooled interval is a stratified bootstrap 95% CI with
10,000 resamples. The unweighted sample proportion is reported as a descriptive
check. A single pooled number is never reported without the pair-specific numbers.

### 6.3 Hypothesis tests

H1 and H3 use one-sided exact binomial tests with the decision rules in Table 2.
The study reports the p-value, the prevalence, and the Wilson CI. There are only
two confirmatory tests, so no alpha adjustment is applied; both are reported and
interpreted conservatively. H2 uses Fisher's exact test and a Newcombe CI for the
risk difference; H4 is descriptive unless the events-per-parameter threshold is
met. A non-significant H2 is not described as evidence of no difference; the CI
and the small SWE-bench+ n are reported.

### 6.4 Sensitivity analyses

Ten analyses are pre-specified: (1) partial adoption counted as adoption (2+3 vs
0+1); (2) self-citations excluded; (3) 2026 and future-dated records excluded;
(4) records with no DOI/arXiv excluded; (5) peer-reviewed venues only; (6) papers
published at least 12 months after critique release; (7) access extreme bounds;
(8) main-results-only versus any-use; (9) the identifier-deduplicated 2,684-row
frame; and (10) the 14 multi-variant clusters dropped. All ten are reported, not
only the favorable ones. The access extreme bounds treat all uncodable papers as
non-adopters (lower bound) or all as adopters (upper bound).

### 6.5 Access bias and missing data

Accessible and inaccessible records are compared on year, venue, identifier
presence, and stratum. If the differences are material, the study reports the
extreme bounds and, only if the model is stable, a propensity-weighted estimate.
Access failure is not treated as random. Uncodable papers are not eligible; they
are reported in the flow diagram and in the bounds. Missing metadata is reported,
not imputed for the primary analysis. A paper whose score remains ambiguous after
adjudication receives the conservative score and a flag.

### 6.6 Reproducibility and deviations

The analysis uses Python 3.11+ and keeps the core estimates in the standard
library (`math`, `statistics`, `random`). Any optional dependency used for an
exploratory regression is pinned and disclosed; it is not part of the primary
analysis. The analysis JSON records the SHA-256 of the coding table. A
reproducibility check recomputes every number in the abstract and main tables
from the coding CSV. The accepted Stage 1 protocol is the registration; no OSF
registration exists. Deviations are logged with date, reason, and impact and are
reported in Stage 2. The reporting follows the transparency recommendations in
[16].

---

## 7. Threats to validity and ethics

**Construct validity.** Documented adoption is not execution. A paper may claim
HumanEval+ but run HumanEval, or use HumanEval+ silently. Evidence quotes,
adoption locus, and an artifact-check subsample mitigate but do not eliminate
this threat. The rubric separates independent remediation from adoption, which
prevents good practice from inflating the estimate.

**Internal validity.** Coder bias and rubric drift are the main threats. Human
double-coding, calibration on fresh papers, adjudication, and a 10% audit are the
mitigations. Selection bias from access failure is addressed by the pretest,
metadata comparison, and extreme bounds. Title clustering and Semantic Scholar
coverage can merge distinct works or miss non-indexed work; the 14 multi-variant
clusters are manually reviewed, and the identifier-deduplicated frame is a
sensitivity check.

**External validity.** The findings may not generalize beyond code-generation
benchmarks, English full texts, or Semantic Scholar-indexed literature. The study
does not claim universal benchmark-critique diffusion. Replication on other pairs
is needed.

**Statistical conclusion validity.** The SWE-bench+ stratum is small, intervals
may be wide, and H2/H4 are exploratory. H1 and H3 are the only confirmatory tests.
The study reports intervals and avoids causal language.

**Ethics and licensing.** No human subjects are involved; the study analyzes
published papers and metadata. The author will confirm local IRB policy and state
the determination. Full texts are stored privately and are not redistributed.
Evidence quotes are at most 60 words per paper, used for research criticism and
verification. The public coding table contains metadata, codes, and short quotes
only. Third-party artifacts retain their licenses: EvalPlus is Apache-2.0,
SWE-bench+ is CC BY 4.0, and SWE-bench is MIT. Paywalled full texts are not sent
to external LLM APIs. LLM assistance, if any, is disclosed with model, version,
prompt, temperature, and date. The second coder is unpaid at the time of writing
and is acknowledged by name or kept anonymous at their choice; if funding becomes
available, an honorarium will be offered. Authorship follows substantive
contribution, not honorary convention.

---

## 8. Timeline, feasibility, and deliverables

ICSME 2027 is scheduled for 7–11 September 2027. The Registered Reports track
requires at most 6 pages plus 1 page of references, IEEE two-column conference
format, single-blind review, and confirmatory studies are eligible for
In-Principal Acceptance. The Stage 1 deadline and submission system were listed
as TBA at the time of writing; the calendar anchor will be fixed when the track
publishes them.

The timeline is expressed relative to Stage 1 acceptance (M0). Calibration and
coder training run in M0–M1. Retrieval, screening, and coding run for 24 weeks in
M1–M7, in four blocks of 225 invited papers, with 100-record blocks added to the
1,200 cap if needed. Reliability and adjudication overlap the last retrieval
block in M6–M7. Analysis runs in M7–M8, Stage 2 writing in M8–M9, and a buffer
covers review response and contingency in M9–M12. Table 4 summarizes the gates.

**Table 4. Timeline and gates.**

| Phase | Relative months | Work | Gate |
|---|---|---|---|
| Calibration | M0–M1 | 20 fresh papers; coder training; reliability; lock rubric | Weighted κ ≥0.60 or documented consensus |
| Retrieval, screening, coding | M1–M7 | 900 invited in four blocks; add 100-record blocks to cap 1,200 | ≥120 eligible or cap reached |
| Reliability | M6–M7 | 20% blind double-code; adjudication | 100% coded; reliability report |
| Analysis | M7–M8 | Primary, pair-specific, sensitivity, bounds | Every number recomputes |
| Stage 2 writing | M8–M9 | Draft, review, deposit | Submitted |
| Buffer | M9–M12 | Review response; contingency | — |

The base-case workload is about 830 hours over 12 months (16 hours per week),
including 31.5 hours from the second coder. The reduced design (560 invited, 81
eligible, ±7.2 points) is about 629 hours over 9 months (16.1 hours per week),
including 22 hours from the second coder. If the ICSME 2027 Stage 2 deadline is
shorter than 9 months after Stage 1 acceptance, the study uses the pre-specified
reduced design or moves to a journal Registered Report with a longer cycle; it
does not compress the 900-paper design below 9 months. This is a feasibility
constraint, not a reason to overstate precision.

The deliverables are the frozen frame and hash, the accepted Stage 1 protocol,
the calibration report, the coding table with evidence quotes, the reliability
report, the analysis scripts and reproducibility log, the Stage 2 manuscript, and
a public deposit. The study currently has no cash budget; software is open
source, the second coder is unpaid at the time of writing, and access relies on
open access, arXiv, author copies, and any library access the author can secure.

---

## References

[1] M. Chen et al., “Evaluating large language models trained on code,”
arXiv:2107.03374, 2021.

[2] J. Austin et al., “Program synthesis with large language models,”
arXiv:2108.07732, 2021.

[3] C. E. Jimenez et al., “SWE-bench: Can language models resolve real-world
GitHub issues?” in *Proc. ICLR*, 2024. arXiv:2310.06770.

[4] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by ChatGPT
really correct? Rigorous evaluation of large language models for code
generation,” in *Proc. NeurIPS*, 2023. arXiv:2305.01210.

[5] R. Aleithan et al., “SWE-Bench+: Enhanced coding benchmark for LLMs,”
arXiv:2410.06992, 2024.

[6] H. Zhang et al., “A careful examination of large language model performance
on grade school arithmetic,” arXiv:2405.00332, 2024.

[7] B. M. Merzah, “Cited but not used: Documented adoption and data
accessibility in 40 non-English NLP benchmarks,” Zenodo, 2026,
doi: 10.5281/zenodo.23634794. Unpublished replication materials.

[8] H. G. Small, “Cited documents as concept symbols,” *Social Studies of
Science*, vol. 8, no. 3, pp. 327–340, 1978.

[9] S. Kapoor and A. Narayanan, “Leakage and the reproducibility crisis in
machine-learning-based science,” *Patterns*, vol. 4, no. 9, p. 100804, 2023.

[10] J. Cohen, “A coefficient of agreement for nominal scales,” *Educational and
Psychological Measurement*, vol. 20, no. 1, pp. 37–46, 1960.

[11] E. B. Wilson, “Probable inference, the law of succession, and statistical
inference,” *Journal of the American Statistical Association*, vol. 22, no. 158,
pp. 209–212, 1927.

[12] R. G. Newcombe, “Interval estimation for the difference between independent
proportions: Comparison of eleven methods,” *Statistics in Medicine*, vol. 17,
no. 8, pp. 873–890, 1998.

[13] J. R. Landis and G. G. Koch, “The measurement of observer agreement for
categorical data,” *Biometrics*, vol. 33, no. 1, pp. 159–174, 1977.

[14] C. D. Chambers and L. Tzavella, “The past, present and future of Registered
Reports,” *Nature Human Behaviour*, vol. 6, pp. 29–42, 2022.

[15] B. A. Nosek, C. R. Ebersole, A. C. DeHaven, and D. T. Mellor, “The
preregistration revolution,” *Proceedings of the National Academy of Sciences*,
vol. 115, no. 11, pp. 2600–2606, 2018.

[16] M. R. Munafò et al., “A manifesto for reproducible science,” *Nature Human
Behaviour*, vol. 1, p. 0021, 2017.

[17] Semantic Scholar, “Graph API,” https://api.semanticscholar.org/, accessed
13 November 2026.

---

## Appendix A. Formatting and submission checklist (not part of the 6 pages)

- Use `\documentclass[conference]{IEEEtran}`, 10 pt, two columns. Do not change
  the template's margins or font sizes to gain space.
- Include the author's real name and “Independent Researcher”; the track is
  single-blind, so no anonymization is required.
- Keep the abstract at or below 250 words; the draft is 250.
- End the body on page 6. Start references on page 7 and keep them there.
- Figures and tables count toward the 6 pages; place Table 1 and Table 3 in a
  single column where possible, Table 2 in two columns or full width, and
  Figure 1 in one column.
- Do not include appendices in the submission. The supplement carries the full
  rubric, frame profile, sampling script, and sensitivity table.
- Add the data-availability and LLM-disclosure statements in the paper, even if
  the supplement repeats them.
- Verify every reference against the publisher or arXiv before submission; the
  list above is a draft, not a verified bibliography.
- Add the corresponding email and, if available, ORCID from the submission
  system. Do not invent either.
- Compile to PDF, embed fonts, and check the page count in the submission system,
  not only in the local PDF viewer.

## Appendix B. Claims audit (not part of the 6 pages)

| Claim | Evidence | Allowed in Stage 1? |
|---|---|---|
| Pilot full adoption 1/6 (16.7%) | Pilot coding table | Yes, as a purposive descriptive result, not prevalence |
| Pilot all-pair adoption 1/8 (12.5%) | Pilot coding table | Yes, as a planning value, not an estimate |
| Pilot access 93.1% | Pilot flow | Yes, as a purposive access result, not a general rate |
| LLM κ 0.78 / 0.86 | Pilot analysis | Yes, labeled LLM–LLM; never human reliability |
| Human κ | None | No; Stage 2 requires the human double-code |
| Causal diffusion | None | No; the design is observational |
| Full-study prevalence | Not executed | No; Stage 2 only |
| Preregistration via OSF | None | No; the accepted Stage 1 protocol is the registration |

## Appendix C. Open items before submission (not part of the 6 pages)

1. **ICSME 2027 RR deadline and submission system.** Listed as TBA. Check the
   track page before submitting; do not invent a date.
2. **ESEM 2027 RR track.** The track URL returned 404. Do not assert ESEM
   requirements; use the verified ICSME requirements. If ESEM is confirmed with
   different limits, revise the page budget.
3. **Human second coder.** Not yet secured. This is a hard gate. The recruitment
   note, blinding packet, and status runner are ready; the coder is not.
4. **OSF registration.** Not created. The accepted Stage 1 protocol is the
   registration; do not claim an OSF DOI.
5. **Timeline fit.** If the Stage 2 deadline is shorter than 9 months after Stage
   1 acceptance, use the reduced design or a journal RR; do not compress the
   900-paper design.
6. **Author contact details.** Add the corresponding email and ORCID from the
   submission system if available; do not fabricate them.
7. **Reference verification.** Check every entry, especially the workshop and
   preprint entries, before submission.
8. **Page count.** Compile early and trim with the cut list below; do not rely on
   the markdown word count.

## Appendix D. Cut list if the body exceeds 6 pages (not part of the 6 pages)

Cut in this order: (1) move the detailed frame profile and venue list to the
supplement, keeping one sentence and Figure 1; (2) shorten Section 2.2 to three
sentences plus Table 1; (3) move the boundary-rule detail to the supplement,
keeping Table 3 and the four rules that decide cases; (4) compress the ten
sensitivity analyses into one paragraph and put the full table in the supplement;
(5) reduce the references to the 12 entries actually cited in the body. Do not
cut the hypotheses, the decision rules, the human-reliability plan, the access
bounds, or the ethics statement.

---

*This outline is a planning document. It is not the Stage 1 submission and does
not report full-study results. The pilot remains a 12-paper feasibility study,
and the human κ remains unmeasured until an independent coder completes the
blinded sheets.*
