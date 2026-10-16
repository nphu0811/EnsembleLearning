# P18 — Reference integrity QA for the compiled P17 report (2026-10-16)

**Scope/status:** `DONE_SCOPED_REPORT_BIBLIOGRAPHY`; canonical **P18 remains PARTIAL**. This is a technical citation-to-bibliography audit, not a systematic literature review, full-text verification, or resolution of all legacy references.

## Checked sources and artifact
- Current sources at GitHub commit `97f6ab66386c98d930fedd27222946a661725323`:
  - `report/references_verified.bib` and `literature/refs_verified_subset.bib` (11 legacy metadata-verified records)
  - `report/references_dataset_checked.bib` and `literature/verification_2026_10_16/dataset_references.bib` (U01 original UNSW-NB15 citation)
  - `report/main.tex` and 5 report chapter files
- Actual XeLaTeX/BibTeX GitHub Actions run **38901027329** on source commit `cb556fc8d5b587708e747afce0d3024a482833c1`, artifact `12046305669`; `main.blg`, `main.bbl` and 22-page `main.pdf` inspected.

## Independent checks performed

| Test | Result |
|---|---|
| Distinct BibTeX entries | 12/12 (11 legacy + U01) |
| Duplicate keys | 0 |
| Distinct DOI values | 12/12 |
| Citation keys actually appearing in source `\\cite{}` | 12 |
| Undefined cited keys by parsing source | 0 |
| Entries in BibTeX that were not cited | 0 |
| BibTeX `\\bibitem{}` entries actually emitted in `main.bbl` | 12 |
| Final `main.blg` BibTeX `Warning--` messages | 0 |
| Final LaTeX `Citation ... undefined` warnings | 0 |
| Legacy subset copied from originally verified subset | Exact trailing body match, 11/11 |
| U01 record copied from institutional-reference source | Exact record match |
| L03 conflict citation added accidentally | NO: L03 excluded |

The installed `plain.bst` rendered the reference list in the real PDF (pages 21–22); glyphs/text could be extracted. The twelve-entry reference list was **not** expanded beyond metadata actually checked.

## Scientific and release boundary

- L03 `10.1109/CNS56114.2022.9947235` is still excluded because its page field is disputed: 254–262 in Crossref/author project, 254–263 across several institutional records; publisher version-of-record page needs manual inspection before certifying.
- U03 official final issue/year corroborated separately (2019, 5(4), 481–494), but not cited in this report; do not claim all dataset-bibliography items were independently VOR-inspected.
- The 11 legacy references are metadata-verified *at varying reading depths*, not 11 full-text method validations. No assertion of exhaustive literature screening, scientifically established novelty or repeated-model generalization is derived from correct BibTeX syntax.
- Canonical P01 and P18 are PARTIAL. Missing institutional form/author details and release G0–G6 remain independent.

**Next P18 acceptance gate:** review each claim→source reading scope, clear L03 only with VOR evidence if that source becomes necessary, finalize institutional citation style and compile/browse the actual submitted PDF, not just the working report.
