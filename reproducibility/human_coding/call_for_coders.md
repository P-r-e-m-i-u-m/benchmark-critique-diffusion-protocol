# Call for an Independent Human Coder

**Status:** Open. One coder needed for the pilot reliability check.  
**Commitment:** 12 papers, about 4–6 hours over two weeks. Unpaid.  
**Location:** Remote; all materials are online.

## What the project is

This project asks whether benchmark critiques change evaluation practice. The
two cases are EvalPlus (HumanEval+/MBPP+) and SWE-bench+ (a filtered 548-instance
dataset and strengthened-test protocol). Citation counts show that a critique was
noticed; they do not show that citing papers changed their own evaluation.

The repository contains a frozen citation frame, a four-level rubric (0 = citation
only, 1 = acknowledged, 2 = partial adoption, 3 = full adoption), a 12-paper pilot,
and a reproducibility package. The immediate gap is the pilot reliability check:
the two existing coding passes were LLM–LLM, not human. A human second coder is
needed before any human κ can be reported.

## What you would do

1. Receive a blinded packet: paper titles, venue, year, the critique under study,
   and direct links to the full texts.
2. Read each paper and decide whether it is eligible for the adoption question.
3. Assign a 0–3 rubric score and paste a short supporting quote (at most 60 words).
4. Return the completed sheet with the time spent and any conflicts.

The packet contains no existing scores, no expected answers, and no pilot summary.
Normal reading, search, and PDF tools are fine. Please do **not** use an LLM to
assign scores; the point is an independent human judgment.

## Independence requirements

You must not:

- have written the manuscript, rubric, or coding instructions;
- have seen the pilot coding table, pilot summary, or the manuscript's results or
  reliability sections;
- have discussed this project's scores with anyone involved.

A conflict of interest — for example, being an author of one of the 12 papers —
does not automatically disqualify you. Declare it and we will decide whether that
paper should be excluded from your packet.

## What you get

- Acknowledgment by name in the repository and the resulting paper, or anonymity,
  whichever you prefer.
- A clear, citable contribution to the reliability evidence.
- No payment. The project currently has no funding; this is stated honestly rather
  than buried.

The full study will later need about 26 papers double-coded. A pilot coder who
wants to continue is welcome, but there is no obligation.

## How to apply

Open an issue in this repository (https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol/issues)
with the subject “Coder application” and tell us:

1. your relevant experience (reading empirical software-engineering or NLP papers
   is enough; you do not need to be a benchmark expert);
2. any conflicts of interest;
3. whether you have seen the pilot codes, pilot summary, or the manuscript's
   results section;
4. roughly how many hours you can give in the next two weeks.

Do not send a CV, identity documents, or other personal data. A GitHub handle and
a short statement are enough.

## What happens after you apply

The author will send the independence questions, then the packet only if you are
eligible and still willing. You can stop at any point before returning the sheet;
if you return it, the completed sheet and your stated preferences are kept as part
of the audit trail. The blank sheet and instructions are public:

- [`README.md`](README.md)
- [`paper_sources.csv`](paper_sources.csv)
- [`../../rubric_v1.1.md`](../../rubric_v1.1.md)
- [`../coding_schema.md`](../coding_schema.md)

The invitation template is in [`recruitment_note.md`](recruitment_note.md).
