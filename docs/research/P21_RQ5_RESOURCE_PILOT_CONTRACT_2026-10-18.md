# P21 RQ5 — Class-weight / FIT-only oversampling resource pilot contract (2026-10-18)

**Status: DESIGN_ONLY / NOT AUTHORIZED / NOT EXECUTED.** This document is a design checkpoint, not evidence of a training run, RQ5 metric, or completed research phase.

## Motivation and boundary
P21 RF42 and selector17 resource pilots have scoped author-host acceptance. The next prerequisite to scientific P21 is a matched resource feasibility pilot for RF42 on the same FIT-only source, without scoring held-out internal validation and without opening official TEST. All P9/P15 frozen artifacts and V2 47-page PDF remain immutable. P21 is a **post-hoc, TRAIN-derived** extension; it cannot yield a fresh official TEST or retroactively fix an earlier evaluation.

## Three comparable arms (same source and fixed randomness)
1. **NONE**: RF42 `class_weight=None`, train on sampled FIT rows without oversampling.
2. **BALANCED**: exactly the same RF42 hyperparameters, seed and FIT-row identities; change only `class_weight="balanced"`.
3. **FIT_ONLY_RANDOM_OVERSAMPLE**: exactly the same RF42 hyperparameters/seed; set `class_weight=None` and duplicate **only the minority-class rows from the pilot FIT sample**, uniformly with replacement until both class counts match. Do not oversample before group split. Never include internal-validation indices in the resampling pool.

The original dataset class distribution must be inspected and the minority class derived from the *pilot FIT labels*; never assume Attack is minority. Preserve the exact RF42 builder settings from the frozen protocol, except the single intended arm treatment. Compare fit-only time and process-tree RSS; do **not** infer predictive benefit from timing, fitted tree count, or training accuracy.

## Preconditions / fail-closed invariants
- Reuse existing checksum-verified official TRAIN path and frozen P21 grouped fold-0 split; fail if hashes, source identities, group disjointness, or label mapping disagree.
- Select at most 8,000 pilot rows by fixed seed and only from FIT_POOL; record seed, row count, label counts and an identity digest that cannot expose row IDs. Do not use a historical stable17 feature list: this is **RF42**, original 42 permitted predictors only.
- Block `official TEST` path access entirely; never predict or score internal validation, calculate test/validation accuracy/F1/MCC/FPR/FNR, inspect 47-page V2 to choose arm, or save per-row predictions.
- Supervisor should require an **exact, new, distinct author authorization token** for RQ5, a fresh ignored output directory, >=4 GiB available RAM at startup, >=10 GiB free disk, process tree <=2 GiB RSS, >=1.5 GiB host available-RAM floor, <=1 CPU, telemetry about every 0.5 seconds, and <=20 minutes total. Abort on violation, preserve bounded evidence; do not automatically advance to full experiment.
- Avoid oversampling blow-up: cap final resampled rows conservatively (e.g., <=16,000 for 8k base) and verify original FIT-only source membership. Block unexpected dtypes or classes.
- Use a fresh worker subprocess under existing P21 guard/supervisor approach rather than fitting inside a validator/CI workflow. An unsuccessful pilot is an honest feasibility result, never a reason to relax split or leak to validation.

## Acceptance matrix before author-host execution
**Static:** original protocol/dataset hash, arm-config delta check, exact predictor allowlist, output allowlist, TEST exclusion, FIT/internal-validation nonintersection, new authorization token, resource envelope, immutable-file inventory.

**Synthetic ML:** build grouped synthetic examples with both possible minority class orientations; show that all three arms begin from identical FIT identities, BALANCED only adjusts weights, oversampling duplicates only FIT-minority indices, balanced post-resampling class counts, no validation usage, no saved predictions. Include failing fixtures for forbidden leakage or unexpected source/hash.

**Report metadata:** aggregate only: arm name, fit-only source/hash and split identifiers, class counts before/after resampling, elapsed seconds, peak process-tree RSS, min host available RAM, exit code, stop reason, boolean `official_test_opened=false`, `validation_predicted=false`, `scientific_metrics_calculated=false`. No feature rows, selected names, serialized estimators, prediction CSV, raw data, trace dumps, or OS-specific confidential paths committed.

## Order of work and hard gates
1. Implement core + supervisor/worker with separate opt-in and mandatory safety assertions. **Do not execute on author data.**
2. Test on synthetic fixtures and run CI checks; inspect safety review.
3. Author explicitly authorizes a bounded laptop pilot using a new output folder, then provides only allowlisted metadata.
4. Verify resource-only report independently. If accepted, separately design/validate 3-fold Stacking-Lite resource pilot.
5. Only after resource evidence and a **new distinct authorization** may the full P21 5-seed/5-arm scientific comparison start on TRAIN-derived internal validation. Its reported scientific findings must be labeled post-hoc.

## Current scope acknowledgment
The existing P21 selector17 pilot passed its bounded report checks (see `docs/research/P21_SELECTOR17_AUTHOR_PILOT_ACCEPTANCE_2026-10-18.md`). This RQ5 design document **does not** mark any RQ5 implementation, author-host pilot, or P21 final evidence as complete.
