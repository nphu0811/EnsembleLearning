# V6 manuscript build and QA — 2026-10-19

- Source commit used for build: a0684a42db240dc2f7b3f1f41edc4624c8fb734f
- Build: XeLaTeX and BibTeX via latexmk
- PDF: exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf
- Pages: 50
- SHA-256: 40b35c9a5c7f228ee91bbba94cfb0ccd701d52dd707a6f5b184171412ce6afc3
- Automated checks: historical plus P21 five-seed RQ/result text present; unresolved citation/reference markers absent; missing glyph and overfull box warnings absent; PDF parsed by pdfinfo and pdftotext.
- Visual page review: pending a separately published V6 page render and examiner inspection; a successful LaTeX build does not by itself demonstrate readability.
- Scope: no model fitting, feature selection, bootstrap, or official TEST access was performed for this manuscript build. P21 outcomes are post-hoc TRAIN-derived internal validation on one shared held-out fold across 5 FIT seeds, not an independent external test.
