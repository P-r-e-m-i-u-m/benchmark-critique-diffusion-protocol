# Registration Plan

**Status:** No registration exists yet. No Stage 1 report has been submitted.  
**Chosen route:** ICSME 2027 Registered Reports, run in conjunction with
*Empirical Software Engineering* (EMSE).  
**Updated:** 22 November 2026.

## 1. What counts as the registration

Under the ICSME 2027 / EMSE Registered Report route, **the accepted Stage 1
protocol is the registration**. The track reviews the design before data
collection, and Stage 2 is submitted to EMSE. A separate OSF registration is not
required for this route.

This is a deliberate choice, not an omission:

- The pilot has already been executed. Registering it on OSF now would be a
  retrospective registration, which is weaker than a prospective one and easy to
  misread as evidence that the pilot was preregistered.
- The full study has not started. Its prospective registration is the Stage 1
  protocol accepted by the track, before the 900-paper sample is drawn.
- The pilot manuscript already says no OSF registration exists. That statement is
  accurate and remains accurate.

The Zenodo DOI `10.5281/zenodo.24245000` identifies the pilot preprint and its
materials. It is not a registration DOI and does not make the study preregistered.

## 2. What will be frozen at Stage 1 acceptance

The accepted protocol package will contain, at minimum:

1. The Stage 1 report (6 pages plus 1 reference page) and its source.
2. The full protocol with hypotheses H1–H4, estimand, and decision rules.
3. Rubric v1.1 and the coding schema, including boundary rules.
4. The frozen citation frame `data/citation_frame_2666.csv` and its SHA-256
   (`4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0`).
5. The sampling script and the committed seed, with the realized sample manifest.
6. The analysis plan, including the ten pre-specified sensitivity analyses and
   the access-failure bounds.
7. The human-coding packet: instructions, blank sheets, independence questions,
   agreement script, and the reliability thresholds.
8. The deviation log and the data-availability statement.

The repository tag for the accepted package will be created at acceptance. The
Stage 1 report itself is not deposited before review.

## 3. Sequence

| Step | Action | Gate |
|---|---|---|
| 1 | Submit Stage 1 to ICSME 2027 RR via EasyChair. | Deadline and link TBA; do not invent them. |
| 2 | Respond to reviews; revise the protocol if requested. | Decision: IPA, Continuity Acceptance, or rejection. |
| 3 | On IPA, tag the accepted protocol and commit the sampling seed. | Tag + manifest hash recorded. |
| 4 | Draw the 900-paper sample with `--stage1-acceptance`. | 135 census + 765 sampled; manifest written. |
| 5 | Run calibration and secure the human coder before main coding. | Weighted κ ≥0.60 or documented consensus; coder committed. |
| 6 | Execute Stage 2 and submit to EMSE. | Protocol adhered to; deviations documented. |

Steps 3–4 are deliberately after acceptance. Drawing the sample earlier would
freeze a denominator that reviewers have not seen and could turn a requested
design change into a deviation.

## 4. If the Registered Report route is not taken

If the author runs the study outside the RR track, the fallback is an OSF
preregistration **before main coding**, containing the same package listed in
Section 2. The registration must disclose that the 12-paper pilot was already
executed and that its codes are LLM–LLM, not human. The pilot cannot be made
prospective by registering it late.

If neither route is completed, the study remains unregistered. That is the
current state and must be reported as such.

## 5. What is still missing

- No Stage 1 submission; the deadline and EasyChair link are TBA.
- No accepted protocol, so no registration reference exists.
- No independent human coder, so the reliability gate is not met.
- No 900-paper sample, coding, or Stage 2 results.

The registration plan does not create any of these. It fixes the order in which
they must happen so that the study does not start before its design is locked.
