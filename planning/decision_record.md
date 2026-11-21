# Decision Record

**Decision ID:** DR-2026-11-13-01  
**Date:** 13 November 2026  
**Status:** **NEEDS EXTERNAL INPUT**  
**Decision owner:** Syed Abdul Aman (independent researcher)  
**Review date:** 14 December 2026  
**Related files:** `PROTOCOL.md`, `rubric_v1.1.md`, `planning/feasibility_workload.md`, `planning/execution_roadmap.md`, `planning/risk_register.md`, `verification/source_verification_log.md`

---

## 1. Decision

The status is **NEEDS EXTERNAL INPUT**: the study is neither **READY TO EXECUTE** nor **NOT FEASIBLE**.

The scientific design is specified, the frame is built and frozen, the rubric is at v1.1, and the pilot shows the coding task is tractable. What is missing is external: a human second coder, evidence that the general frame is accessible, and a registration DOI. None of these can be manufactured by more analysis. The decision therefore turns on three conditions with a hard review date of **2026-12-14**.

**What this decision authorizes**

- Completing the Gate 0 checklist.
- Sending the second-coder invitation and negotiating hours.
- Running the 50-record access pretest with a separate seed.
- Creating the OSF registration and depositing the protocol, rubric, frame, and scripts.
- Preparing calibration packets and the coding form.

**What this decision does not authorize**

- Drawing or coding the main sample.
- Full-scale retrieval or screening.
- Writing the paper as if results existed.
- Claiming human reliability, adoption prevalence, or a validated rubric.
- Creating another repository or modifying existing projects.

---

## 2. Context

The research question is whether benchmark critique diffuses into evaluation practice, narrowed to two critique–benchmark pairs:

- **P1:** EvalPlus (HumanEval+/MBPP+) as a drop-in test augmentation for HumanEval and MBPP.
- **P2:** SWE-bench+ as a filtered 548-instance dataset and strengthened-test protocol for SWE-bench.

GSM1k is retained as a secondary task-fit contrast only. It is excluded from the primary denominator because it is a parallel contamination-controlled benchmark, not a drop-in replacement for GSM8K, and because including it would change the estimand from “adoption of a remediated artifact” to “adoption of a substitute benchmark.”

The primary outcome is **documented protocol adoption**, scored 0–3:

| Score | Label | Meaning |
|---:|---|---|
| 0 | Citation only | The critique appears in the reference list or a generic citation cluster, with no engagement. |
| 1 | Acknowledged | The paper notes the critique or its finding but does not change its evaluation. |
| 2 | Partial | The paper uses part of the remediated artifact/protocol, or uses it for a secondary analysis, or adopts it with material deviations. |
| 3 | Full | The remediated artifact/protocol is used for the paper’s primary evaluation of the criticized benchmark, with at least one reported result and the critique cited as the basis. |

Binary adoption = score 3. The pilot produced 1/6 primary-pair full adoption (16.7%, Wilson 95% CI 3.0–56.4%) and 1/8 all-pair (12.5%, 2.2–47.1%). The planning value is 12.5%, chosen conservatively; it is not a prediction.

---

## 3. Options considered

| Option | Description | Why not chosen |
|---|---|---|
| **A. Execute now, solo** | Start the 900-invited design immediately with no human coder; use the LLM pilot as a rubric check. | The registered protocol requires human reliability. Starting now would either produce an unregistered study or force a post hoc fallback. It also assumes access that has not been tested. |
| **B. Narrow and gate (chosen)** | Freeze the two-pair design; require C1–C3 by 2026-12-14; execute only if met; otherwise use the documented fallback or stop. | The design is feasible at 16 h/week average, the frame is built, and the pilot is encouraging. The gates are external, not scientific. |
| **C. Abandon** | Treat the study as not feasible. | The evidence does not support this. The frame, rubric, and pilot are in place; the workload is part-time, not full-time; the main risks have mitigations. Abandoning would discard a tractable study. |
| **D. Expand** | Add GSM1k to the primary denominator, add more benchmarks, or run a census. | Expansion raises workload and weakens the focused estimand. GSM1k is a different kind of benchmark; more pairs would require a new frame and a new rubric. This is a different study, not a stronger version of this one. |

**Chosen: B.** The decision is deliberately conditional. It does not pretend the external inputs exist, and it does not pretend the study is impossible.

---

## 4. Evidence base

| Evidence | Status | Source |
|---|---|---|
| Analysis frame: 2,666 title clusters (2,531 EvalPlus-only + 135 SWE-bench+ census) | Verified | `data/citation_frame_2666.csv`, `data/frame_summary.json` |
| Frame SHA-256: `6a0a374b…` | Verified | `data/frame_summary.json` |
| Pilot: 29 papers, 27 accessible (93.1%), 12 coded, 8 eligible all-pair, 6 primary-pair | Verified (internal) | `pilot/pilot_summary.md` |
| Pilot primary-pair adoption: 1/6 = 16.7% (3.0–56.4%) | Verified (recomputed) | Wilson interval |
| Pilot all-pair adoption: 1/8 = 12.5% (2.2–47.1%) | Verified (recomputed) | Wilson interval |
| Pilot reliability: 12/12 eligibility; 7/8 ordinal; κ 0.78 unweighted / 0.86 linear | **LLM–LLM only** | `pilot/pilot_summary.md` |
| Base design: 900 invited, 130 eligible, ±5.7 pp, 829.7 h, 16.0 h/week | Verified (recomputed) | `planning/feasibility_workload.md` |
| 24-week retrieval phase, peak ~21 h/week | Verified (arithmetic) | `planning/execution_roadmap.md` |
| No human second coder | **Unresolved** | Blinded packet and agreement script prepared; no commitment record |
| General-frame access rate | **Unknown** | Only the purposive 93.1% pilot |
| OSF registration | **Not created** | No OSF DOI; Zenodo DOI 10.5281/zenodo.24245000 covers the preprint and materials. |
| EvalPlus bibliographic record | Verified | NeurIPS 2023, DOI 10.52202/075280-0943, pp. 21558–21572 |
| SWE-bench+ dataset | Verified | Zenodo 13879453, 548 instances, CC BY 4.0 |
| SWE-bench+ peer-review status | **No record located; not exhaustive** | Describe as arXiv preprint |

The evidence supports a feasible design. It does not support execution without the three external conditions.

---

## 5. Conditions for flipping to READY TO EXECUTE

All three conditions must be met by **2026-12-14**. Partial completion leaves the decision at **NEEDS EXTERNAL INPUT**.

### C1 — Human second coder

**Requirement.** One human coder commits in writing to:

- 6 h calibration (weeks 3–6).
- Blind coding of 20% of eligible papers: at least 26 papers at the base design (45 min each = 19.5 h), or 16 papers at the reduced design (12 h).
- 6 h adjudication.
- A total of at least **31.5 h** at the base design, or **22 h** at the reduced design.

**Evidence required.** A signed email or letter naming the person, the hours, and the dates; a calendar block for calibration and the reliability window; a statement of any conflicts of interest.

**Verification.** The researcher confirms the commitment is specific (hours and dates), not a general expression of interest. A verbal “happy to help” does not satisfy C1.

**If not met.** The study remains **NEEDS EXTERNAL INPUT**. The fallback in §7 is available but is a different, weaker study and must not be described as the registered protocol.

### C2 — Access pretest

**Requirement.** A 50-record access pretest drawn with a **separate seed** from the main sample. The pretest must show **≥70% full-text access** through a documented route (publisher, arXiv, institutional subscription, ILL), or 50–70% with a confirmed ILL plan and turnaround.

**Evidence required.** A log with record ID, route, outcome (success/failure), failure reason, and date for all 50 records. A summary access rate with a Wilson 95% CI.

**Verification.** The pretest records are from the frozen frame, not from the pilot’s purposive set. The seed and script are recorded. Failures are not silently dropped.

**If not met.** At <50%, pause and secure access or register an open-access restriction. At 50–70% without an ILL plan, the study remains **NEEDS EXTERNAL INPUT**.

### C3 — OSF registration

**Requirement.** A public OSF registration with a DOI containing:

- Protocol v1.0 (`PROTOCOL.md`).
- Rubric v1.1 (`rubric_v1.1.md`).
- Sampling script (`scripts/sample_frame.py`) and the committed seed.
- Analysis plan (the pre-specified primary estimate, sensitivity analyses, and reliability plan).
- Frame hash `6a0a374b…` and the retrieval date 2026-11-13.
- The decision rule for the cap and the fallback.

**Evidence required.** The registration DOI and a dated snapshot of the registration.

**Verification.** The DOI resolves; the deposited files match the workspace versions by hash.

**If not met.** The study can still be executed as an unregistered study, but it is not the protocol described here. The decision remains **NEEDS EXTERNAL INPUT** until the researcher either registers or explicitly downgrades the claim.

---

## 6. Flip path

| Date | Check | If met | If not met |
|---|---|---|---|
| 2026-12-07 | C1 draft commitment; C2 pretest half done; OSF project created | Continue Gate 0 | Escalate: contact backup coder; extend pretest |
| **2026-12-14** | **C1, C2, C3 all verified** | **READY TO EXECUTE**; start calibration 2026-12-15 | **NEEDS EXTERNAL INPUT**; do not start main coding |
| 2026-12-21 | Fallback decision if not flipped | Choose fallback (§7) or pause | Pause; archive Gate 0 record |
| 2027-01-11 | G1 calibration | Proceed to retrieval | Revise rubric and repeat calibration |

**All three, not two.** A second coder without access evidence produces an unrepresentative sample. Access without a coder produces no human reliability. A registration without either registers a study that cannot run. The conditions are conjunctive because the design requires all three.

---

## 7. Fallback if C1 fails

**Status:** available, but **not the registered protocol**. It is a weaker study and must be labeled as such.

| Element | Registered design | Fallback |
|---|---|---|
| Coders | One researcher + one human second coder | One researcher only |
| Reliability | 20% blind double-code; human κ | No human κ; LLM audit as diagnostic only |
| Eligible target | 130 (base) | ~80 |
| Precision at 12.5% | ±5.7 pp | ~±7.3 pp |
| Venue | EMSE primary; DMLR alternative | DMLR or preprint |
| Claim | Documented adoption with human reliability | Documented adoption, single-coder, reliability unestablished |

**What the fallback may claim:** a transparent single-coder audit with a frozen frame, explicit rubric, evidence quotes, and a reproducibility package.

**What the fallback may not claim:** human inter-rater reliability, a validated rubric, or equivalence to the registered design.

**Registration:** if the fallback is chosen, register it as a **new** protocol version with a new DOI. Do not silently amend the original registration.

---

## 8. Capacity confirmation

The decision assumes the researcher can protect:

- **20–21 h/week** during weeks 7–34 (retrieval, reliability, analysis).
- **16.0 h/week average** across 52 weeks.
- **19.4 h/week average, peaks ~25 h/week** if the 1,200 cap is triggered.

**Confirmation required before G0:** a calendar block for weeks 7–34 and an explicit statement of the weekly hours available. If only 12 h/week are available, the 900 design is not feasible; choose the 9-month reduced design (560/81) or extend the calendar.

**This is a real constraint, not a formality.** The 24-week retrieval phase exists because a 16-week phase would require ~28 h/week. The cap case is not workload-neutral. A plan that assumes 16 h/week and delivers 8 h/week will fail at week 20, not at week 50.

---

## 9. Decision log

| # | Date | Decision | Evidence | Status |
|---:|---|---|---|---|
| 1 | 2026-11-13 | Narrow to EvalPlus + SWE-bench+; GSM1k secondary only | Pilot; frame; rubric v1.1 | Closed |
| 2 | 2026-11-13 | Use 2,666 title clusters as the analysis frame | CSV + hash | Closed |
| 3 | 2026-11-13 | Planning value p = 0.125; binary adoption = score 3 | Pilot 1/8; conservative choice | Closed |
| 4 | 2026-11-13 | Base design 900 invited / 130 eligible / ±5.7 pp | Scenario table | Closed |
| 5 | 2026-11-13 | 24-week retrieval phase; 12-month plan | Workload recalculation | Closed |
| 6 | 2026-11-13 | EMSE primary; DMLR alternative; QSS deferred | Journal verification | Closed |
| 7 | 2026-11-13 | **NEEDS EXTERNAL INPUT**; C1–C3 by 2026-12-14 | This record | **Open** |
| 8 | 2026-11-21 | Prepare blinded human-coding packet; strict `paper_key` + `critique` agreement script; report undefined κ as `null` | `reproducibility/human_coding/`; `scripts/agreement.py`; `tests/test_agreement.py` | Closed |

---

## 10. Sign-off

**Researcher:** Syed Abdul Aman  
**Date:** 13 November 2026  
**Signature:** ______________________

**Reviewer / supervisor (if any):** ______________________  
**Date:** ______________________

**Next review:** 14 December 2026, at Gate 0. The decision is not reopened before then unless C1, C2, or C3 is resolved early; resolving one condition does not flip the decision until all three are met.

---

## 11. One-paragraph summary

The study is designed, frozen, and feasible at part-time effort, but it cannot start as registered because it lacks a human second coder, general-frame access evidence, and a registration DOI. Those are external inputs, not analysis tasks. The decision is **NEEDS EXTERNAL INPUT** with a hard review on **2026-12-14**: if C1 (signed second coder), C2 (50-record access pretest ≥70%), and C3 (OSF DOI) are all met, the study flips to **READY TO EXECUTE** and calibration starts on 2026-12-15. If C1 fails, the documented fallback is a single-coder, ~80-eligible study with no human κ, submitted to DMLR or as a preprint; it is weaker and must be registered as a new protocol, not presented as the registered design.
