# Stage 2 Readiness

**Updated:** 22 November 2026  
**Status:** Not ready to execute. No confirmatory data exist.

This note separates what is actually ready from what is still missing. It exists
to prevent a planning document from being mistaken for an executed study.

## 1. What is ready

| Component | State | Evidence |
|---|---|---|
| Citation frame | Frozen, 2,666 title clusters | `data/citation_frame_2666.csv`; SHA-256 `4650ce1b…` |
| Sampling design | Implemented and tested | `scripts/sample_frame.py`; `tests/test_sampling.py` |
| Sampling gate | Requires a registration reference or a labelled dry run | `--osf-doi`, `--stage1-acceptance`, or `--allow-unregistered` |
| Coding rubric | v1.1, with boundary rules | `rubric_v1.1.md`; `reproducibility/coding_schema.md` |
| Pilot | 12 coded papers, 6 primary-pair eligible | `pilot/pilot_coding_table.csv`; `analysis/pilot_results.json` |
| Analysis template | Primary estimate, Wilson intervals, sensitivity shells | `scripts/analysis_template.py` |
| Human-coding packet | Instructions, blank sheets, agreement script, public call | `reproducibility/human_coding/` |
| Stage 1 outline | 6+1 page draft with hypotheses and decision rules | `manuscript/registered_report/icsme_esem_2027_stage1_outline.md` |
| Registration plan | Sequence and package defined | `manuscript/registered_report/registration_plan.md` |

The 900-row draw was exercised in tests with a placeholder seed in a temporary
directory. The test checks the 135 SWE-bench+ census plus 765 EvalPlus-only
sample, and the 3.308 design weight. **No study sample was committed.** A test
draw is not the registered sample.

## 2. What is missing

| Missing input | Why it blocks Stage 2 | Who can supply it |
|---|---|---|
| Accepted Stage 1 protocol | The registration reference and the locked design | ICSME 2027 / EMSE review |
| Independent human coder | Human κ and the reliability gate | A human volunteer |
| 50-record access pretest | Confirms the frame is retrievable at ≥70% | The author, before main coding |
| Committed sampling seed | Makes the draw auditable | The author, at acceptance |
| 900-paper retrieval and coding | Produces the confirmatory data | The author, over months |
| Stage 2 analysis and writing | Produces the estimate | The author, after coding |

## 3. Why the confirmatory study is not run here

The protocol's primary coder is the human author, and the reliability claim
requires a second human. This repository explicitly refuses to treat LLM–LLM
agreement as human reliability. Running the 900-paper study with an AI coder
would produce exactly the data the design says are not acceptable, and would
misrepresent the study as human-coded.

The execution also requires retrieving hundreds of full texts, including
paywalled papers, over roughly 24 weeks. That is a research programme, not a
repository task. The correct next step is not to simulate it; it is to secure the
coder and submit Stage 1.

## 4. Order of operations

1. Submit Stage 1 to ICSME 2027 RR when the deadline and EasyChair link appear.
2. On acceptance, tag the protocol, commit the seed, and draw the 900-paper
   sample with `--stage1-acceptance`.
3. Recruit and train the independent coder; run calibration on 20 fresh papers.
4. Run the 50-record access pretest and confirm the retrieval route.
5. Retrieve, screen, and code in four blocks; double-code 20% of eligible papers.
6. Run the pre-specified analysis and submit Stage 2 to EMSE.

Steps 2–6 must not start before step 1. The current status is **not ready to
execute**, and the decision record remains **NEEDS EXTERNAL INPUT**.
