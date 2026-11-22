# Human Double-Coding Packet

**Status:** templates only. No human coder has completed these sheets yet. The
pilot's κ values remain **LLM–LLM** and are not human inter-rater reliability.
A public recruitment call is pinned as repository issue #14 and written up in
[`call_for_coders.md`](call_for_coders.md).

This folder is the packet for a human reliability check on the 12-paper pilot. It
is not a new prevalence study. The question is narrow: can two humans apply rubric
v1.1 to the same rows independently and get close enough that the instrument is
usable? If they cannot, the rubric or the training needs work before the full
study. A good κ here would be a reason to proceed with calibration, not a result
to put in the manuscript.

## What is in the packet

| File | What it is |
|---|---|
| `coder_A.csv` | Blank sheet for the first coder. Metadata is filled; coding fields are empty. |
| `coder_B.csv` | Blank sheet for the second coder. Same metadata, different `coder_id`. |
| `paper_sources.csv` | Direct open-access and publisher links for the 12 papers. Metadata only, no codes. |
| `recruitment_note.md` | Ready-to-send invitation and the questions to ask before and after coding. |
| `call_for_coders.md` | Public-facing call with independence requirements and how to apply. |
| `../../rubric_v1.1.md` | The coding instrument. Read this first. |
| `../../reproducibility/coding_schema.md` | Field definitions, eligibility rules, and the score scale. |
| `../../scripts/agreement.py` | Computes agreement after both sheets are done. |
| `../../pilot/pilot_coding_table.csv` | **Do not open until both sheets are returned.** It contains the original pilot codes and will bias you. |

## Who should code

Two humans.

- **Coder A** can be the author. The author's original pilot pass was LLM-assisted,
  so a fresh human pass is still useful.
- **Coder B** must be independent: not the author, not someone who wrote the
  rubric, and not someone who has already seen the pilot codes or the manuscript's
  reliability discussion.

Some familiarity with code-generation benchmarks helps, but the rubric is the
instrument. You do not need to know EvalPlus or SWE-bench+ from memory; you need to
be able to read a paper's methods and results and apply the decision tests.

If you have a conflict — for example, you are an author of one of the 12 papers —
write it in `notes` and keep coding. Do not silently skip the row.

**Do not use an LLM to assign scores.** You can use search, Ctrl+F, a PDF reader,
and a reference manager. If you use a tool to extract or summarize text, say so in
`notes`. The judgment has to be yours.

## Blinding

Code from the paper, not from the existing table.

- Do not read `pilot/pilot_coding_table.csv`, `pilot/pilot_summary.md`, the
  manuscript's results section, or the other coder's sheet until both sheets are
  returned.
- Do not discuss scores with the other coder before you both submit. If you do,
  tell the author before the agreement is computed.
- There is no target score to match. The existing pilot codes are LLM output, not
  human gold. Trying to reproduce them would defeat the point.

## What you need

- The 12 papers. The sheet gives title, venue, year, and critique. Retrieve the
  full text from the publisher, arXiv, an author copy, or institutional access.
  `paper_sources.csv` has an open-access link and, where available, a publisher
  DOI for each row. If a link is dead, search the exact title.
- Roughly 4–6 hours. Budget about 20 minutes for an eligibility screen and 30
  minutes for an eligible paper. The pilot did not time this precisely, so treat
  the estimate as a planning number, not a quota.
- A PDF reader and a way to copy short verbatim quotes.

Do not code from the abstract. If the full text is unavailable, code
`eligible=false`, `ineligibility_reason=ACCESS`, and leave `score` blank.

## Workflow

1. Read `rubric_v1.1.md` §1–§5, then `reproducibility/coding_schema.md` §3–§6.
   Keep both open while you code.
2. For each row, decide eligibility before you think about the score.
   - **E1:** Does the paper report empirical results on the criticized benchmark
     (HumanEval, MBPP, SWE-bench, SWE-bench Lite, or SWE-bench Verified)?
   - **E2:** Does it cite the critique paper or the official artifact?
   - **E3:** Is there an English full text with enough methods/results detail?
3. If any condition fails, fill `eligible=false`, give one reason from the list
   below, and leave `score` blank. Ineligibility is **not** a score of 0.
4. If all three hold, read the citation context (±2 paragraphs), the methods, the
   main results tables, and the captions. Assign 0–3.
5. Fill the secondary fields. The score without an evidence quote is not ready.
6. Save the file under a new name. Do not overwrite the blank template.

## Field guide

Fill only the columns after `critique`. The first five columns are metadata; leave
them alone.

| Column | What to put |
|---|---|
| `eligible` | `true` or `false`. |
| `ineligibility_reason` | `NO_EVAL`, `NO_CITATION`, `ACCESS`, `LANGUAGE`, or `DUPLICATE`. Blank if eligible. |
| `score` | `0`, `1`, `2`, or `3` if eligible. Blank if ineligible. |
| `engagement` | `0` = reference only, `1` = brief mention, `2` = substantive discussion. |
| `independent_remediation` | `true` if the paper strengthened evaluation without adopting the critique's artifact or protocol; otherwise `false`. |
| `adoption_locus` | `main_results`, `secondary_results`, `appendix`, `future_work`, `related_work`, or `none`. |
| `evidence_quote` | A verbatim quote of 60 words or fewer. No paraphrase. |
| `notes` | Section/table/page for the quote, the boundary decision, and anything an adjudicator needs. |
| `confidence` | `high`, `medium`, or `low`. |
| `adjudicate` | `yes` if the case is genuinely ambiguous or you marked `confidence=low`; otherwise `no`. |
| `access_route` | `publisher`, `arxiv`, `author_copy`, `repository`, `ill`, or `html`. |
| `coder_id` | Pre-filled as `A` or `B`. Do not change it. |
| `coded_at` | ISO date, e.g. `2026-11-21`. |

## Score reminders

| Score | Use it when |
|---:|---|
| **0** | The critique is only in the reference list, or it appears in a generic contamination/leakage cluster without its specific finding. The benchmark is unchanged. |
| **1** | The paper states the critique's specific finding, but its evaluation of the criticized benchmark is unchanged. |
| **2** | The recommended practice is present, but only in an appendix, robustness check, subset, or secondary analysis. The main results still use the original benchmark. |
| **3** | The recommended artifact or protocol supports at least one main table, figure, or claim, and the critique is cited as the basis. |

The boundary rules matter more than the labels:

- Citation is not adoption.
- Generic contamination talk is not acknowledgment.
- Acknowledgment requires the critique's specific finding.
- Independent remediation is not adoption. Set `independent_remediation=true` and
  score 0 or 1 depending on engagement.
- Derivative-only papers (SWE-bench Pro, CWEval, etc.) are ineligible, not 0.
- Using HumanEval+ problems without the augmented tests is not full adoption.
- If the paper reports both original and augmented results, the augmented result
  must support a main claim for a 3.
- Unresolved ambiguity gets the conservative lower score, `confidence=low`, and
  `adjudicate=yes`. Do not average or split the difference.

## Evidence standard

The quote has to let an independent auditor see why you assigned the score.

- **0:** quote the reference entry or the generic citation context.
- **1:** quote the sentence that states the critique's specific finding, and put
  the methods sentence or table showing the original benchmark in `notes`.
- **2:** quote the methods/table showing the recommended practice, and note the
  main table that shows the original benchmark as primary.
- **3:** quote the main table caption or methods sentence naming the recommended
  artifact/protocol and the critique, plus at least one reported result.

If you cannot find a quote that supports the score, the score is not ready. Mark
`confidence=low`, `adjudicate=yes`, and explain what is missing in `notes`.

## What not to do

- Do not score an ineligible paper as 0.
- Do not infer a score from the abstract, citation count, venue, or author
  reputation.
- Do not average across benchmarks. Use the highest-adoption main use.
- Do not edit the metadata, add rows, remove rows, or rename columns.
- Do not overwrite `coder_A.csv` or `coder_B.csv`. Save your completed file as
  `coder_A_completed.csv` or `coder_B_completed.csv`.
- Do not read the other coder's sheet before you finish.

## Returning the sheet

Save the completed file in this folder (or send it to the person who gave you the
packet) as:

- `coder_A_completed.csv`
- `coder_B_completed.csv`

Keep it UTF-8, comma-separated, and with the same columns. Then send a short note
with:

- your coder ID and the date you finished;
- roughly how long it took;
- any conflicts of interest;
- any tool use beyond search/reading (including LLM use);
- anything about the rubric that was confusing.

Completed sheets are gitignored. They are working data for the reliability check,
not public repository content. If you want to be acknowledged, tell the author
separately; the CSV only needs a coder ID.

## What happens next

The author runs:

```powershell
python scripts/human_coding_status.py --run
```

The status wrapper checks that both completed sheets exist and share exactly the
same keys before it computes anything. It then calls `scripts/agreement.py`,
which writes a JSON report, a Markdown summary, and a disagreement CSV under
`analysis/human_coding/`. It reports:

- eligibility agreement and κ on all 12 rows;
- ordinal agreement and unweighted, linear-weighted, and quadratic-weighted κ on
  the rows both coders marked eligible;
- a confusion matrix for each;
- every disagreement, with both coders' scores and notes.

Disagreements go to adjudication. Discuss the evidence, not the labels. If you
cannot resolve one, use a third coder or the conservative lower score and record
the rationale. Do not edit the original sheets after the fact; keep the
adjudication separate.

A few things the script will not do for you:

- It will not turn a small sample into a precise estimate. Twelve rows is tiny.
  Report the κ with a confidence interval and a plain warning.
- It will not decide whether the coders were independent. That is a process
  question; the author has to confirm it.
- It will not treat an undefined κ as 1.00. If both coders use only one category,
  expected agreement is 1.0 and κ is undefined. The script reports `null` and
  says why. The pilot's 1.00 eligibility value was a documented convention, not
  an estimate.

## Before you return the sheet

- [ ] All 12 rows have `eligible` filled.
- [ ] Every ineligible row has a reason and a blank `score`.
- [ ] Every eligible row has a score from 0 to 3.
- [ ] Every score has an evidence quote and notes with the location.
- [ ] `coder_id` is unchanged and `coded_at` is filled.
- [ ] I did not read the pilot coding table, the pilot summary, the manuscript
      results, or the other coder's sheet.
- [ ] I did not use an LLM to assign scores.
- [ ] I saved the file as `coder_*_completed.csv`, not over the template.
