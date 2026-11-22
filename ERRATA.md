# Errata — Pilot-Study Preprint v1.0

**Errata version:** 1.0-errata-1  
**Date:** 22 November 2026  
**Author:** Syed Abdul Aman (Independent Researcher)  
**Applies to:** Zenodo record 24245000, version 1.0, published 15 November 2026  
**DOI:** [10.5281/zenodo.24245000](https://doi.org/10.5281/zenodo.24245000)  
**Status:** Correction of record. The deposited PDF and `manuscript/paper.md` are unchanged.

## 1. Summary

The v1.0 manuscript was frozen on 13 November 2026, two days before the
Zenodo deposit. Three passages say, without qualification, that no DOI has been
obtained. Those statements were accurate when written: no DOI existed on
13 November. They became misleading on 15 November, when the deposit itself
assigned a DOI. Read literally in the deposited record, they contradict the
record.

The statements are correct only in the narrower sense that **no OSF
registration and no OSF DOI exist**. A Zenodo DOI does exist:

> **10.5281/zenodo.24245000** (version DOI)  
> **10.5281/zenodo.24244999** (concept DOI)

The Zenodo record notes already state this distinction. This errata makes the
correction explicit in the repository, where the same unqualified wording
appears in the unchecksummed reproducibility statement.

## 2. What is correct

- No OSF registration was created.
- No OSF DOI exists.
- The study is not preregistered.
- A Zenodo DOI exists for the pilot-study preprint:
  `10.5281/zenodo.24245000`.
- The Zenodo DOI identifies the deposited preprint and its materials. It is
  **not** a registration DOI and does **not** make the study preregistered.
- The deposited PDF is unchanged: 229,726 bytes, SHA-256
  `76923A889BFAB711837B8E3C40ABCDDB8F5EFB5CEDEF7919D45367D045F2C6B6`.

## 3. Affected locations

| Location | Text as written | Correct reading | Action |
|---|---|---|---|
| `manuscript/paper.md` §9.6, item 10 (line 416) | “There is no OSF registration or DOI …” | “There is no OSF registration or OSF DOI. The Zenodo DOI identifies the deposited preprint, not a preregistration.” | Not edited; this errata is the correction. |
| `manuscript/paper.md` §10.5 (line 443) | “… not registered and no OSF DOI is available.” | Accurate as written: it names the OSF DOI specifically. | No correction. |
| `manuscript/paper.md` §10.6 (line 447) | “No DOI has been obtained.” | “No OSF DOI has been obtained. The Zenodo DOI was assigned at deposit.” | Not edited; this errata is the correction. |
| `manuscript/reproducibility_statement.md` §“Registration and status” (lines 70–71) | “… not registered, and no DOI was obtained.” | Same correction as §10.6. | Corrected in the repository on 22 November 2026; see §4. |
| `README.md`, DOI note | Explains that §10.6 refers to the planned OSF registration, not the Zenodo DOI. | Accurate; now links here. | Updated with a link to this errata. |

## 4. Repository correction

`manuscript/reproducibility_statement.md` is not covered by
`reproducibility/checksums.sha256`, so it can be corrected without changing the
frozen deposit. Its “Registration and status” paragraph now reads:

> The protocol was prepared for OSF registration but was **not registered**,
> and no OSF DOI was obtained. The study is therefore not preregistered. A
> Zenodo DOI was assigned to this pilot-study preprint at deposit:
> 10.5281/zenodo.24245000. That DOI identifies the deposited preprint and its
> materials; it is not a registration DOI and does not make the study
> preregistered. See `ERRATA.md` for the correction of the unqualified “no DOI”
> wording in the frozen manuscript.

## 5. Why the PDF and `paper.md` are not edited

`manuscript/paper.md` is covered by `reproducibility/checksums.sha256`
(SHA-256 `efece060db34b9d6ec900824eff96130077c8be0a6f3748959a4aeb1f8b73108`).
The PDF is the identity of the Zenodo v1.0 deposit. Editing either would break
the checksum manifest and the deposit’s integrity, and would create a second,
silently different “v1.0.”

The correct fix is a dated correction note that states the error, plus a fix in
the unchecksummed reproducibility statement. A future manuscript version, if
any, will carry corrected wording and a new version number.

## 6. What this errata does not do

- It does not change the pilot’s results, reliability values, or limitations.
- It does not add a human coder or a human κ.
- It does not make the study preregistered.
- It does not convert the preprint into a peer-reviewed publication.
- It does not change the deposited PDF, the checksum manifest, or the Zenodo
  record.

## 7. Version history

| Date | Version | Change |
|---|---|---|
| 2026-11-15 | 1.0 | Zenodo deposit. Manuscript frozen 2026-11-13. |
| 2026-11-22 | 1.0-errata-1 | This note; reproducibility statement corrected; README link added. |

## 8. Contact

Syed Abdul Aman, Independent Researcher  
Repository: https://github.com/P-r-e-m-i-u-m/benchmark-critique-diffusion-protocol
