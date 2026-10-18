# V3 manuscript build and QA — 2026-10-19

- Source commit used for build: 16cd595dbba9838ee7bbb5a5b69dc0ea77f48131
- Build: XeLaTeX and BibTeX via latexmk
- PDF: exports/report_revision_v3_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V3.pdf
- Pages: 56
- SHA-256: 6fc7ea9e11cd892ea0f2cc9dccf12dee920620508c1c6a58b7649487804e0e8a
- Automated checks: historical plus P21 five-seed RQ/result text present; unresolved citation/reference markers absent; missing glyph and overfull box warnings absent; PDF parsed by pdfinfo and pdftotext.
- Visual page review: pending author-host render and inspection recorded with the build artifact.
- Scope: no model fitting, feature selection, bootstrap, or official TEST access was performed for this manuscript build. P21 outcomes are post-hoc TRAIN-derived internal validation on one shared held-out fold across 5 FIT seeds, not an independent external test.
