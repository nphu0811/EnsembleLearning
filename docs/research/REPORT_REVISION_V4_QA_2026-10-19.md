# V4 manuscript build and QA — 2026-10-19

- Source commit used for build: f7926e07ea2c5f04a8f9f85336713f97652b24d6
- Build: XeLaTeX and BibTeX via latexmk
- PDF: exports/report_revision_v4_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V4.pdf
- Pages: 56
- SHA-256: 7e8784d7b415eef5b94003440c8446e46c05b399f91ebde57917d0e2581eea98
- Automated checks: historical plus P21 five-seed RQ/result text present; unresolved citation/reference markers absent; missing glyph and overfull box warnings absent; PDF parsed by pdfinfo and pdftotext.
- Visual page review: pending a separately published V4 page render and examiner inspection; a successful LaTeX build does not by itself demonstrate readability.
- Scope: no model fitting, feature selection, bootstrap, or official TEST access was performed for this manuscript build. P21 outcomes are post-hoc TRAIN-derived internal validation on one shared held-out fold across 5 FIT seeds, not an independent external test.
