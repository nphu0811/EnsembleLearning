# NCKH revision V2 — final PDF layout fix verification (2026-10-17)

**Result: VERIFIED_BUILD_AND_PDF_QA_PASS, ready for author review, not institutional acceptance.**

## Evidence and code provenance

- The user asked to repair V2 directly on `main`, preserving the 37-page source and all frozen experiment results.
- Source corrections committed:
  - `report/main_revision_v2_2026_10_17.tex`: widened LOF/LOT numeric labels from 4em to 6em; configured siunitx `group-digits=integer` to keep six-decimal metrics visually continuous.
  - `report/chapters/results_discussion_revision_v2_2026_10_17.tex`: rewrote journal/log-like narration in Chapter 4 and cost caption; shortened/wrapped numerical column headings, refined table spacing and made cost header legible.
  - `.github/workflows/build-nckh-revision-v2-pdf.yml`: normalized both extracted PDF text and required literal strings before comparison, rather than stripping whitespace only from the extracted text.
- Final source commit: `964216c720bac26d6aea838ad03931238ebbece6`.
- Successful CI build `https://github.com/nphu0811/EnsembleLearning/actions/runs/38999397120` (XeLaTeX/BibTeX, PDF text QA, no missing glyphs or unbound citations, no overfull hbox/vbox). Bot committed the resulting PDF and mechanical QA at `a797f2f4917713313fed3c3e08b705de4122bbe9`.
- Final file: `exports/report_revision_v2_2026_10_17/Bao_cao_NCKH_EnsembleLearning_REVISION_V2.pdf` (GitHub tracked), **47 A4 pages**, SHA256 **`5300f9de92a7fc3834294b015382acfff80c9f0384ef9d6a32419e2bf72b52f3`**, 379512 bytes. Downloaded and verified independently from the exact successful workflow artifact.
- Original frozen 37-page PDF remained unchanged: SHA256 **`8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`**.

## Independent PDF inspection

- Rendered and visually inspected updated cost table at physical page 34: the numerical columns no longer overlap; two-line headers fit the page; decimals read `0.008679`, `0.012445`, `0.003562`, without fractional digit grouping.
- Rendered and inspected RQ4 novel-vector comparison table on physical page 39: columns are evenly spaced across text width and retain frozen metrics; RQ1–RQ5 all still present in PDF text.
- Rendered the rotated attack-family table on physical page 35: it fits on one A4 landscape page, numeric cells readable, no cropping.
- PyMuPDF analyzed extracted text rectangles across **all 47 pages**; **0 out-of-page blocks after applying rotation transforms** (unrotated-coordinate false positives on the landscape page were normalized).
- Final XeLaTeX log: **0 overfull hbox/vbox**, 0 unresolved citation/reference/missing glyph markers.
- The visual comparison is a print-layout QA, not a new independent scientific review or certification of all author research claims.

## Remaining boundaries

P20 final review, author signoff, administrative submission gates, original training-environment identity, rights/licensing and any pre-existing low-resolution source heatmap/figure issues remain separate. PDF editing introduced no model training, TEST retuning, raw data reads, bootstrap recomputation or modified frozen metrics. Only one PDF should be submitted as requested; no standalone appendix is needed for RQ answers.
