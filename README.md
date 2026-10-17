# Ensemble Learning for Network Intrusion Detection

Evidence-based binary Normal/Attack research on the official UNSW-NB15 split.
This repository preserves frozen historical results and separately documented
full-TRAIN reconstructed models. It is **not ready for final submission**.

Read [current handoff](.research_memory/HANDOFF.md),
[roadmap](docs/ROADMAP_CURRENT.md) and
[release blockers](release/RELEASE_BLOCKERS.md) before running research commands.
`README_FIRST.md` describes the agent instruction pack, not research completion.

## Current evidence

- Official TRAIN has 175,341 rows; official TEST has 82,332 rows. Normal=0,
  Attack=1. Final frozen candidates RF42, Stacking42 and RF17 use threshold 0.5.
- [P15 closure](docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md)
  documents three reconstructed full-TRAIN artifacts and 69/69 author-host checks.
  These are not original historical artifacts. Original training environment and
  binary identity remain UNKNOWN. Model binaries stay local and are not needed
  for the read-only audits below. Do not rerun training to refresh status.
- [P16 audit](docs/research/P16_COMPREHENSIVE_QA_2026-10-17.md) records saved-summary
  checks, the approved five-chapter 37-page PDF and six standalone alternatives.
  The approved PDF remains unchanged; print and snapshot-age findings stay open.
- [P18 audit](docs/research/P18_CURRENT_REPORT_READING_BOUNDARIES_2026-10-17.md)
  distinguishes verified metadata from actual reading. Full literature validation
  and research novelty are not established by DOI existence.

Stacking42 has 142 fewer false positives and 118 more false negatives than RF42.
Its Macro-F1/MCC paired intervals contain zero. This does not establish either
overall superiority or equivalence. Feature selection before development CV,
non-fully-nested meta selection, overlapping feature vectors, conditional row
bootstrap and absent temporal/external validation limit generalization claims.
RF17 changes both features and hyperparameters, so it is a pipeline trade-off.

## Reproduce the read-only QA

Use Python 3.11 and a new output directory each time. See
[QA environment](reproducibility/requirements-p16-qa-py311-NOT-TRAINING.txt).
These scripts do not need raw TRAIN/TEST, serialized models or prediction CSVs.

```powershell
python -X utf8 tools/p16_frozen_results_audit.py --out-dir results/reproducibility/UNIQUE_P16_AUDIT
python -X utf8 tools/p18_current_report_citation_audit.py --out-dir literature/UNIQUE_REPORT_AUDIT
```

For PDF QA, supply the author-approved local PDF with SHA-256
`8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`.
Install Poppler and ensure `pdftoppm` is on PATH. The PDF is not committed here;
its path and unchanged hash are documented in the QA evidence. Do not replace
the report with a similarly named older draft.

```powershell
python -X utf8 tools/p16_report_pdf_audit.py --pdf C:/path/to/approved-report.pdf --out-dir results/reproducibility/UNIQUE_PDF_AUDIT
```

For figure generation and preflight, an installed `nature-figure` skill provides
the alignment/text/collision audit scripts. Pass its actual `scripts` location to
`--skill-scripts`; the exact commands are in the P16 audit. That external skill is
not vendored or presumed installed on another machine. Existing result source
CSVs are copied byte-for-byte beside each new figure; PDF/SVG are authoritative
vector assets and PNGs are previews. No automated overwrite is allowed.

## Training, availability and release

Frozen builders are in `src/models/run_unsw_phase9_final_holdout.py`; the historical
entry point can evaluate TEST and must not be casually rerun. The P15 supervisor
imports only frozen constructors and was used under its documented TRAIN-only
contract. Follow the [reconstruction closure](docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md)
and existing runbook for provenance, not as a request to launch another fit.
Do not assign the historical TEST metrics to newly reconstructed binaries.

Raw UNSW data, virtual environments, credentials and reconstructed model binaries
must stay out of new commits/packages. Public dataset availability does not grant
unspecified redistribution rights. No project code LICENSE has been established;
this README does not grant a license to code, data, templates or third-party papers.
The release review also flags three pre-existing tracked `SMOKE_ONLY.joblib`
artifacts. They are historical software-smoke evidence, not approved release
models. Their tracked presence remains an open release hygiene finding.
The repository URL is `https://github.com/nphu0811/EnsembleLearning`; there is no
confirmed archival DOI or final release tag. See
[availability review](docs/research/P19_RELEASE_READINESS_2026-10-17.md).

No FINAL_NCKH.zip, external panel endorsement, production IDS or live demo readiness
is claimed. Administrative acceptance/signatures, proposal DOCX/PDF, defense slides
and remaining scientific/release checks are distinct gates.
