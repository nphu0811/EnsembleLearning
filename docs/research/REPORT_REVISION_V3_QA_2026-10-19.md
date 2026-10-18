# V3 manuscript build and QA — 2026-10-19

- Source commit used for build: cfe7c61091fd839120764724cb4d71a1d76dfe0a
- Build: XeLaTeX and BibTeX via latexmk
- PDF: exports/report_revision_v3_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V3.pdf
- Pages: 55
- SHA-256: 1377ce0a5356e5ad9bfa51f02e28d44f1154a241aa569dec6ac1ae233f52c4fb
- Automated checks: historical plus P21 five-seed RQ/result text present; unresolved citation/reference markers absent; missing glyph and overfull box warnings absent; PDF parsed by pdfinfo and pdftotext.
- Visual page review: pending author-host render and inspection recorded with the build artifact.
- Scope: no model fitting, feature selection, bootstrap, or official TEST access was performed for this manuscript build. P21 outcomes are post-hoc TRAIN-derived internal validation on one shared held-out fold across 5 FIT seeds, not an independent external test.
