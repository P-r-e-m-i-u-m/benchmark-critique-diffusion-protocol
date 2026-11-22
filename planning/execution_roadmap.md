# Execution Roadmap

**Version:** 1.0  
**Prepared:** 13 November 2026  
**Assumed start:** 1 December 2026 (Tuesday)  
**Assumed end:** 29 November 2027 (week 52); 30 November 2027 reserved as a float day  
**Base design:** 900 invited = 135 SWE-bench+ census + 765 EvalPlus-only sample; target 120 eligible; cap 1,200 invited.

> **Update 22 November 2026 — registration route.** The project now targets the
> ICSME 2027 Registered Reports track, run in conjunction with EMSE. Under that
> route the accepted Stage 1 protocol is the registration; C3 can be met by an
> accepted Stage 1 reference instead of an OSF DOI. The OSF-specific wording
> below is retained for the independent route. The gate itself is unchanged: no
> main sample is drawn and no coding starts until a registration reference and a
> committed human coder exist. Gate 0 still fails today because neither exists.

---

## 1. Calendar assumptions

- The researcher can protect **20 h/week** during retrieval, reliability, and analysis (weeks 7–34), and **16 h/week** on average across the year. The 16.0 h/week figure in `planning/feasibility_workload.md` is an **average**, not a uniform weekly load.
- Gate 0 is completed before week 1 of main work. If Gate 0 slips, every date shifts by the same number of weeks; the phase structure does not change.
- No work is scheduled on public holidays; the buffer absorbs them.
- The second coder’s hours are separate from the researcher’s hours.
- The frame is frozen at 2026-11-13. No mid-study citation refresh.

---

## 2. Phase summary

| Phase | Weeks | Dates | Main work | Gate / output |
|---|---:|---|---|---|
| **0. Gate 0** | 1–2 | 2026-12-01 to 12-14 | Second coder commitment; 50-record access pretest; OSF registration; library route; sample draw and seed. | **G0:** C1–C3 met; decision flips to READY TO EXECUTE or remains NEEDS EXTERNAL INPUT. |
| **1. Calibration** | 3–6 | 12-15 to 2027-01-11 | 20-paper calibration (10 EvalPlus, 10 SWE-bench+); coder training; rubric v1.1 test; agreement check. | **G1:** rubric locked; weighted κ ≥0.60 or documented consensus; OSF update. |
| **2. Retrieval/screening/coding** | 7–30 | 01-12 to 06-28 | Four blocks of 225 invited; retrieve, screen, code eligible; weekly access log. | **G2:** ≥120 eligible or 1,200 invited; flow diagram. |
| **3. Reliability/adjudication** | 27–30 | 06-01 to 06-28 | 20% blind double-code (26 papers); adjudicate; compute κ and CIs; lock coding table. | **G3:** 100% coded; reliability report; adjudication log. |
| **4. Analysis** | 31–34 | 06-29 to 07-26 | Primary estimate; pair-specific; weighted; sensitivity; access bounds; figures; reproducibility. | **G4:** analysis memo; every number recomputes. |
| **5. Writing** | 35–42 | 07-27 to 09-19 | Draft; second-coder/co-author review; data statement; LLM disclosure; formatting. | **G5:** manuscript ready; sign-off. |
| **6. Submission** | 43–46 | 09-20 to 10-17 | EMSE submission; arXiv preprint; OSF update; response file. | **G6:** submitted; preprint live. |
| **Buffer** | 47–52 | 10-18 to 11-29 | Desk-reject contingency; review response; DMLR reformat if needed; project close. | Final deposit; decision log closed. |

---

## 3. Load profile (base case)

| Phase | Hours | Weeks | Average h/week | Peak note |
|---|---:|---:|---:|---|
| Gate 0 | ~26 | 2 | 13.0 | Front-loaded; 50-record pretest is the bulk. |
| Calibration | ~28 | 4 | 7.0 | Light; second coder training is scheduled here. |
| Retrieval/screening/coding | 455 | 24 | 19.0 | Peak phase; 37.5 invited/week. |
| Reliability/adjudication | 6.5 (first coder) | 4 | 1.6 | Overlaps weeks 27–30; +1.6 h/week on top of retrieval. |
| Analysis | 80 | 4 | 20.0 | Peak; no other major work in these weeks. |
| Writing | 140 | 8 | 17.5 | Sustained. |
| Submission | 20 | 4 | 5.0 | Light; admin-heavy. |
| Admin (spread) | 40 | 52 | 0.8 | OSF updates, logs, email. |

**Realistic peak:** ~21 h/week in weeks 27–30 (retrieval 19.0 + reliability 1.6) and ~20 h/week in weeks 31–34 (analysis). The annual average is 16.0 h/week, but the first 34 weeks are heavier than the last 18. Do not plan a uniform 16 h/week schedule; protect 20–21 h/week for the retrieval and analysis months.

**If 20 h/week cannot be protected:** use the 9-month reduced design (560 invited, 81 eligible) or extend the 12-month design to 15–18 months. Do not start the 900 design at 12 h/week and hope the buffer absorbs it.

---

## 4. Week-by-week plan

| Week | Dates | Phase | Work | Output / gate |
|---:|---|---|---|---|
| 1 | 2026-12-01 to 12-07 | Gate 0 | Send second-coder invitation and role description; confirm hours (6 h calibration, ≥19.5 h coding, 6 h adjudication); open OSF project; confirm library/ILL route. | C1 draft; OSF project created. |
| 2 | 12-08 to 12-14 | Gate 0 | Run 50-record access pretest with a separate seed; log route/outcome; draw main sample with committed seed; register protocol, rubric, sample script, frame hash; **G0 review**. | **G0:** C1–C3 met or decision stays NEEDS EXTERNAL INPUT. Sample list frozen. |
| 3 | 12-15 to 12-21 | Calibration | Select 20 calibration papers from the first block (10 EvalPlus, 10 SWE-bench+); retrieve them; prepare blinded packets; second-coder training session 1. | Calibration set; training log. |
| 4 | 12-22 to 12-28 | Calibration | First coder codes 20 papers with rubric v1.1; second coder codes independently; record evidence quotes. | Two independent calibration sets. |
| 5 | 12-29 to 2027-01-04 | Calibration | Compare; adjudicate disagreements; compute agreement; identify ambiguous rules; revise rubric only if necessary. | Calibration report v1. |
| 6 | 01-05 to 01-11 | Calibration | Lock rubric; update OSF with any clarification; finalize coding form; **G1 review**. | **G1:** rubric locked; κ or consensus documented. |
| 7 | 01-12 to 01-18 | Retrieval | Block 1 starts (225 invited): retrieve full texts; log access; begin eligibility screening. | Access log week 1; 50–60 records processed. |
| 8 | 01-19 to 01-25 | Retrieval | Block 1: screening; code eligible papers; weekly reconciliation of ambiguous cases. | 100–120 records processed. |
| 9 | 01-26 to 02-01 | Retrieval | Block 1: screening/coding; update flow diagram counts. | 150–170 records. |
| 10 | 02-02 to 02-08 | Retrieval | Block 1: screening/coding; first access-rate check. | 200–225 records; access rate estimate. |
| 11 | 02-09 to 02-15 | Retrieval | Block 1 completion; block 1 quality check (10% audit of first 20 codes). | Block 1 closed; audit log. |
| 12 | 02-16 to 02-22 | Retrieval | Block 2 starts (225 invited): retrieval and screening. | Block 2 at ~25%. |
| 13 | 02-23 to 03-01 | Retrieval | Block 2: screening/coding. | Block 2 at ~50%. |
| 14 | 03-02 to 03-08 | Retrieval | Block 2: screening/coding; interim eligibility-rate estimate. | Block 2 at ~75%; eligibility estimate. |
| 15 | 03-09 to 03-15 | Retrieval | Block 2 completion; reconcile; update flow diagram. | Block 2 closed. |
| 16 | 03-16 to 03-22 | Retrieval | Block 3 starts (225 invited): retrieval and screening. | Block 3 at ~25%. |
| 17 | 03-23 to 03-29 | Retrieval | Block 3: screening/coding. | Block 3 at ~50%. |
| 18 | 03-30 to 04-05 | Retrieval | Block 3: screening/coding; check eligibility projection against 120 target. | Block 3 at ~75%; projection memo. |
| 19 | 04-06 to 04-12 | Retrieval | Block 3 completion; decide whether block 4 needs expansion. | Block 3 closed; expansion decision. |
| 20 | 04-13 to 04-19 | Retrieval | Block 4 starts (225 invited): retrieval and screening. | Block 4 at ~25%. |
| 21 | 04-20 to 04-26 | Retrieval | Block 4: screening/coding. | Block 4 at ~50%. |
| 22 | 04-27 to 05-03 | Retrieval | Block 4: screening/coding; begin reliability sample selection (20% stratified). | Block 4 at ~75%; reliability list drafted. |
| 23 | 05-04 to 05-10 | Retrieval | Block 4: screening/coding; prepare blinded reliability packets. | Block 4 at ~90%; packets ready. |
| 24 | 05-11 to 05-17 | Retrieval | Block 4: complete retrieval; close access log; **interim G2 check** (eligible count). | 900 invited processed; interim eligible count. |
| 25 | 05-18 to 05-24 | Retrieval | Complete any remaining screening/coding; if <120 eligible, start 100-record add-on block (decision point). | Screening complete or add-on started. |
| 26 | 05-25 to 05-31 | Retrieval | Add-on block if needed; otherwise begin reliability double-coding. | Add-on at ~50% or reliability started. |
| 27 | 06-01 to 06-07 | Retrieval + reliability | Add-on completion or reliability coding; second coder codes independently. | Add-on closed or 10 reliability papers coded. |
| 28 | 06-08 to 06-14 | Retrieval + reliability | Reliability coding; adjudication meeting 1; update coding table. | 20 reliability papers; adjudication log. |
| 29 | 06-15 to 06-21 | Reliability | Reliability coding; adjudication meeting 2; compute preliminary agreement. | 26 reliability papers; preliminary κ. |
| 30 | 06-22 to 06-28 | Reliability | Final adjudication; lock coding table; **G2/G3 review**; flow diagram final. | **G2/G3:** eligible count final; reliability report; coding table frozen. |
| 31 | 06-29 to 07-05 | Analysis | Clean data; descriptive tables; frame/sample profile; score distribution. | Analysis dataset v1; descriptives. |
| 32 | 07-06 to 07-12 | Analysis | Primary estimate: pair-specific Wilson CIs; weighted estimate; bootstrap CI. | Primary results table. |
| 33 | 07-13 to 07-19 | Analysis | Sensitivity analyses: partial-as-adoption, self-citation, 2026 exclusion, no-ID exclusion, peer-reviewed only, access bounds. | Sensitivity table. |
| 34 | 07-20 to 07-26 | Analysis | Figures; reproducibility check (recompute every number); analysis memo; **G4 review**. | **G4:** analysis memo; reproducibility log. |
| 35 | 07-27 to 08-02 | Writing | Outline; introduction; research question; contribution claims. | Draft intro. |
| 36 | 08-03 to 08-09 | Writing | Background; prior work; pair definitions; rubric summary. | Draft related work/methods. |
| 37 | 08-10 to 08-16 | Writing | Methods: frame, sampling, eligibility, coding, reliability, analysis. | Draft methods. |
| 38 | 08-17 to 08-23 | Writing | Results: prevalence, typology, contrast, sensitivity. | Draft results. |
| 39 | 08-24 to 08-30 | Writing | Discussion: interpretation, limits, implications for SE evaluation. | Draft discussion. |
| 40 | 08-31 to 09-06 | Writing | Limitations; conclusion; abstract (150–250 words); title. | Complete draft v1. |
| 41 | 09-07 to 09-13 | Writing | Second-coder/co-author review; fact-check every number against analysis memo; references. | Draft v2; review comments. |
| 42 | 09-14 to 09-19 | Writing | Data availability statement; LLM disclosure; formatting; cover letter; **G5 review**. | **G5:** submission-ready manuscript. |
| 43 | 09-20 to 09-26 | Submission | Final proof; supplementary files; OSF/Zenodo deposit; submit to EMSE. | Submission confirmation. |
| 44 | 09-27 to 10-03 | Submission | Post arXiv preprint (cs.SE; cross-list cs.CL/cs.LG if appropriate); update OSF. | Preprint DOI. |
| 45 | 10-04 to 10-10 | Submission | Prepare response file; monitor submission system; check preprint metadata. | Response file v1. |
| 46 | 10-11 to 10-17 | Submission | Confirm submission; archive correspondence; **G6 review**. | **G6:** submitted; preprint live; archive complete. |
| 47 | 10-18 to 10-24 | Buffer | Desk-reject contingency: prepare DMLR reformat if needed; otherwise draft review-response template. | Fallback package or response template. |
| 48 | 10-25 to 10-31 | Buffer | Address early reviewer comments if any; run any requested sensitivity analysis. | Response draft. |
| 49 | 11-01 to 11-07 | Buffer | Final data/code deposit; README; metadata; license checks. | Public deposit v1. |
| 50 | 11-08 to 11-14 | Buffer | Project close: decision log; deviations; lessons learned; archive. | Close-out memo. |
| 51 | 11-15 to 11-21 | Buffer | Contingency: resubmission preparation or additional analysis. | Updated package if needed. |
| 52 | 11-22 to 11-28 | Buffer | Final checks; handover notes; 30 November float. | Project complete. |

---

## 5. Gates

### G0 — Gate 0 (end of week 2, 2026-12-14)

**Required evidence**

1. **C1:** signed email/letter from the human second coder committing to 6 h calibration, at least 19.5 h of blind coding (26 papers at 45 min), and 6 h adjudication.
2. **C2:** 50-record access pretest log with route, outcome, failure reason, and date; access rate ≥70% (or 50–70% with an ILL plan).
3. **C3:** Registration reference containing protocol v1.0, rubric v1.1, sampling script and seed, analysis plan, and frame hash — an OSF DOI, or the accepted Stage 1 protocol under the ICSME/EMSE RR route.

**If met:** decision flips to **READY TO EXECUTE**; start calibration on 2026-12-15.  
**If not met:** decision remains **NEEDS EXTERNAL INPUT**; do not start main coding. See `planning/decision_record.md`.

### G1 — Calibration (end of week 6, 2027-01-11)

- 20 papers coded independently by both coders.
- Weighted κ ≥0.60, or a documented consensus rule for every disagreement.
- Rubric v1.1 locked; any clarification recorded on OSF.
- If weighted κ <0.40: revise rubric and repeat calibration with 10 new papers (adds 2–3 weeks; shifts the schedule).

### G2 — Retrieval/screening (end of week 30, 2027-06-28)

- At least 120 eligible papers, or 1,200 invited with a documented shortfall.
- Flow diagram complete: invited, accessible, screened, eligible, ineligible by reason, uncodable by reason.
- Access log complete; access-bias comparison ready.

### G3 — Reliability (end of week 30, 2027-06-28)

- 26 papers double-coded (20% of 130; 16 if the reduced design is used).
- Adjudication complete; κ with bootstrap CI; PABAK if prevalence <10%.
- Coding table frozen; no changes after this gate without an amendment.

### G4 — Analysis (end of week 34, 2027-07-26)

- Primary estimate and all pre-specified sensitivity analyses complete.
- Every number in the abstract and main tables recomputes from the coding CSV.
- Analysis memo and reproducibility log filed.

### G5 — Writing (end of week 42, 2027-09-19)

- Manuscript complete; abstract 150–250 words.
- Data availability statement and LLM disclosure checked.
- Second coder/co-author sign-off.
- Cover letter explains EMSE fit.

### G6 — Submission (end of week 46, 2027-10-17)

- EMSE submission confirmation.
- arXiv preprint DOI.
- OSF updated with manuscript and analysis code.
- Response file and correspondence archived.

---

## 6. Deliverables by month

| Month | Weeks | Deliverable |
|---|---|---|
| Dec 2026 | 1–4 | Gate 0 package; OSF DOI; sample list; calibration set; training log. |
| Jan 2027 | 5–8 | Locked rubric; calibration report; block 1 retrieval underway. |
| Feb 2027 | 9–12 | Block 1 closed; access-rate estimate; block 2 underway. |
| Mar 2027 | 13–16 | Block 2 closed; eligibility estimate; block 3 underway. |
| Apr 2027 | 17–20 | Block 3 closed; expansion decision; block 4 underway. |
| May 2027 | 21–24 | 900 invited processed; interim eligible count; reliability packets. |
| Jun 2027 | 25–28 | Add-on or reliability coding; adjudication meetings. |
| Jul 2027 | 29–32 | Coding table frozen; reliability report; primary analysis. |
| Aug 2027 | 33–36 | Sensitivity analyses; figures; analysis memo; draft methods/results. |
| Sep 2027 | 37–40 | Complete draft; internal review; submission package. |
| Oct 2027 | 41–44 | Submission; preprint; response file. |
| Nov 2027 | 45–48 | Buffer; fallback package; public deposit; close-out. |

---

## 7. 9-month compressed option

**Use only if the end date is fixed at 2027-08-31.** Design: 560 invited, 448 accessible, 81 eligible, 16 double-coded, ±7.2 pp.

| Phase | Weeks | Dates | Work | Gate |
|---|---:|---|---|---|
| Gate 0 | 1–2 | 2026-12-01 to 12-14 | Same as base; C1–C3. | G0 |
| Calibration | 3–5 | 12-15 to 2027-01-04 | 20 papers; compressed training. | G1 |
| Retrieval | 6–21 | 01-05 to 05-24 | Four blocks of 140 invited; 16 weeks. | G2 |
| Reliability | 19–21 | 05-10 to 05-24 | 16 papers double-coded; adjudication. | G3 |
| Analysis | 22–25 | 05-25 to 06-20 | Primary + sensitivity; 4 weeks. | G4 |
| Writing | 26–32 | 06-21 to 08-01 | 7 weeks; 20 h/week. | G5 |
| Submission | 33–35 | 08-02 to 08-22 | EMSE submission; preprint. | G6 |
| Buffer | 36–39 | 08-23 to 08-29 | Contingency; close-out; 30–31 August float. | Final |

**Load:** retrieval 283 h / 16 weeks = 17.7 h/week; analysis 20 h/week; writing 20 h/week. The average is 16.1 h/week, but the peak is ~22 h/week. This option is feasible only with protected time and a cooperative second coder. It is the fallback, not the recommendation.

---

## 8. Contingency paths

### 8.1 If access is 50–70%

- Add ILL requests in weeks 7–12; prioritize DOI/publisher routes.
- Record the shortfall and compare accessible vs inaccessible records on year, venue, and identifiers.
- If the shortfall is concentrated in one stratum, report stratum-specific access rates and use extreme bounds.
- Do not silently treat access failure as random.

### 8.2 If access is <50%

- Restrict the primary frame to open-access/arXiv records and report the restriction as a design change (OSF amendment).
- Or pause and secure institutional access before continuing. Do not code from abstracts.

### 8.3 If eligibility is <10%

- The 900 design yields ~72 eligible at 80% access; precision ±7.7 pp. That is reportable.
- Add 100-record blocks up to 1,200 only if the added precision is worth the workload. At 10% eligibility, 1,200 yields 96 eligible, ±6.6 pp.
- If the added blocks would push the project past 20 h/week or past the 12-month end date, stop at 900 and report the realized precision. A protocol amendment is not required to stop early; it is required to exceed 1,200.

### 8.4 If the cap (1,200) is triggered

- The cap case is ~1,006 h, or 19.4 h/week over 52 weeks; peak retrieval is ~25 h/week if 300 add-on records are processed in 12 weeks.
- Either protect 25 h/week for the add-on period, or extend the project by 4–8 weeks and use the buffer.
- Record the decision and its effect on precision in the decision log. Do not pretend the 12-month/16 h week plan still holds.

### 8.5 If the second coder drops out

- Before calibration: recruit a replacement; delay G1; do not start main coding.
- After calibration but before reliability: use the fallback single-coder design (80 eligible, no human κ, LLM audit as diagnostic only) and switch venue to DMLR/preprint. Record the deviation.
- After reliability coding: retain the completed double-coded sample; do not claim more reliability than was actually collected.

### 8.6 If EMSE desk-rejects

- Reformat for DMLR within 4 weeks (no fees, no page limit, single-blind).
- Keep the same manuscript and supplement; adjust the cover letter and framing.
- If DMLR also declines, post the preprint and consider Scientometrics/QSS only with a reframed, broader analysis.

### 8.7 If the frame hash changes

- Stop. Rebuild the frame from the frozen source and verify the hash. Do not sample from a changed frame.
- If the source cannot be rebuilt, the study cannot proceed as registered; document and pause.

---

## 9. Weekly operating cadence

- **Monday:** review the week’s target (records to retrieve/screen, papers to code); check access log.
- **Wednesday:** midweek reconciliation of ambiguous cases; update adjudication queue.
- **Friday:** update flow-diagram counts; back up the coding CSV; write a 5-line progress note (records, eligible, issues, next week).
- **End of each block:** 10% audit of the first coder’s codes; update the access/eligibility table; check the projection against 120.
- **End of each phase:** gate review; file the gate memo; update OSF if the protocol changed.

---

## 10. What must be true before week 1

- [ ] C1 second coder committed in writing.
- [ ] C2 access pretest ≥70% (or 50–70% with an ILL plan).
- [ ] C3 registration reference created (OSF DOI or accepted Stage 1).
- [ ] Frame CSV hash verified against `6a0a374b…`.
- [ ] Sampling seed and script committed; sample list frozen.
- [ ] Library/ILL route confirmed.
- [ ] 20 h/week protected for weeks 7–34; calendar blocked.
- [ ] Backup drive and versioning for the coding table; no PDFs in the public workspace.
- [ ] Decision record signed and dated.

If any of the first three is missing, the project is **not** in execution; it remains **NEEDS EXTERNAL INPUT**.
