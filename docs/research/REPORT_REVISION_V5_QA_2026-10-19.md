# V5 manuscript build and QA — 2026-10-19

- Source commit used for build: 75f4b2d73ec31671eb14fc86cf68bf03fce031ca
- Build: XeLaTeX and BibTeX via latexmk
- PDF: exports/report_revision_v5_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V5.pdf
- Pages: 50
- SHA-256: 8e8c558e99501b2b8088332a1edbbc7c7331e6f48e5747b070c82749d31f7d4d
- Automated checks: historical plus P21 five-seed RQ/result text present; unresolved citation/reference markers absent; missing glyph and overfull box warnings absent; PDF parsed by pdfinfo and pdftotext.
- Visual page review: pending a separately published V5 page render and examiner inspection; a successful LaTeX build does not by itself demonstrate readability.
- Scope: no model fitting, feature selection, bootstrap, or official TEST access was performed for this manuscript build. P21 outcomes are post-hoc TRAIN-derived internal validation on one shared held-out fold across 5 FIT seeds, not an independent external test.
