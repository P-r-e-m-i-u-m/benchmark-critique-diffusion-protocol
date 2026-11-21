# Checksums and Integrity

## Purpose

The frame, rubric, and pilot table are frozen inputs. Their SHA-256 hashes make
silent edits detectable and let a reader confirm that the manuscript's counts came
from the committed files.

## Covered files

`reproducibility/checksums.sha256` covers:

- `data/citation_frame_2666.csv`
- `data/frame_summary.json`
- `data/cohort_feasibility.csv`
- `data/cohort_feasibility.manifest.json`
- `pilot/pilot_coding_table.csv`
- `pilot/pilot_summary.md`
- `rubric_v1.1.md`
- `PROTOCOL.md`
- `manuscript/abstract.md`
- `manuscript/paper.md`
- `manuscript/references.bib`
- the six Markdown and six CSV tables in `manuscript/tables/`
- the three figure CSV files in `manuscript/figures/`

The generated `analysis/pilot_results.json` is excluded because it contains a
generation timestamp. The analysis's source hash is recorded inside the JSON and
checked by the tests.

## Not covered

The human-coding templates in `reproducibility/human_coding/` are committed, but
they are not frozen research inputs and are not in the manifest. Completed coder
sheets and the `analysis/human_coding/` outputs are working data: they are
gitignored and never checksummed. The agreement report records the SHA-256 of the
two sheets it actually read, so a completed run remains auditable without
publishing the sheets.

## Verify

```powershell
python scripts/verify_checksums.py
```

Expected output: one `OK` line per covered file and a final count, exit code 0.
Any mismatch prints `FAIL` and exits 1.

Hashes are computed over the bytes stored in Git. `.gitattributes` normalizes
text files to LF, so a fresh clone verifies on Windows, macOS, and Linux. A text
file rewritten with CRLF line endings will not match.

## Regenerate

Only regenerate after an intentional, documented change to a frozen input:

```powershell
python scripts/verify_checksums.py --write
```

Regenerating checksums does not make an edit correct. Record the reason in the
commit message and, for a frame change, in `reproducibility/provenance.md`.

## Known hashes

| File | SHA-256 |
|---|---|
| `data/citation_frame_2666.csv` | `4650ce1b67df80bdeb1691b883a36f5bda540efd1dad20da652660f216f705a0` |
| `data/frame_summary.json` (source frame hash field) | `46a58fe017577d9e15c22e6bef198fdff526b511ff7897519b6a0e91542cdd72` |
| `pilot/pilot_coding_table.csv` | Recorded in `analysis/pilot_results.json` and verified by tests. |
