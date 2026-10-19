# P21 RQ5 author resource-pilot acceptance — 2026-10-18

**Decision: PASS_RESOURCE_SMOKE_ONLY, with evidence-packaging finding; NOT a scientific RQ5 result.** Source: author commit [d2af75c](https://github.com/nphu0811/EnsembleLearning/commit/d2af75c4b5888e2a4589db64562f366197b3b8c6), machine-reported `run_report.json` and `worker_result.json`. These are metadata checks, not independent operating-system telemetry reproduction.

## Resource and fit-only results
- PRE execution protocol audit: 30/30 PASS, official TRAIN SHA verified, official TEST not read by validator.
- RQ5 local supervisor: `PASS_RQ5_RESOURCE_SMOKE_ONLY`, exit 0, null stop reason, elapsed **91.25s**, process-tree peak **331747328 B (316.38 MiB)**, RAM available floor **4135841792 B**, 177 resource samples. Startup free RAM 4489478144 B, disk 31593639936 B.
- TRAIN 175341 rows; fixed fold 0 FIT_POOL 140272, validation 35069; **8000 fit-only pilot rows** with 2555 Normal and 5445 Attack. Validation was not fitted/predicted according to the worker report.
- NONE: 8000 training rows, fit 12.906s, `class_weight=None`.
- BALANCED: identical 8000 base rows, fit 12.5s, `class_weight="balanced"`.
- FIT_ONLY_RANDOM_OVERSAMPLE: duplicates FIT minority Normal only to 5445 Normal / 5445 Attack, 10890 fitted rows, fit 18.406s, `class_weight=None`.
- All reported flags: `official_test_opened=false`, `validation_predicted=false`, `scientific_metrics_calculated=false`, `model_artifact_saved=false`. These remain self-reported worker flags consistent with code and source, not independent hardware attestation.
- Previous local synthetic tests: 8 sampler tests PASS; 6 acceptance tests PASS. Their pass alone is not a scientific result.

## Evidence hygiene finding
Commit d2af75c contains **more than three allowlisted JSONs**: `go.signal` and `resources.csv` are tracked as well as the JSON evidence. The latter is low-level hardware time-series metadata and should stay local for future runs. Do **not** destroy current local records, remove physical files from other users' checkouts, rewrite history, or mark package release-clean based only on the aggregate reports. Future packaging should use an explicit allowlist and separate safe release branch/archive. Public Git history already contains these metadata files; .gitignore changes do not retroactively untrack them.

## Next sequence
1. Implement and synthetic-test a 3-fold, one-worker Stacking-Lite resource pilot with no validation predictions or performance metrics, audit source and capacity, and request separate author-host consent. Do not infer Stack resource usage from three RF42 RQ5 arms.
2. Audit the new pilot evidence and safety report before scientific P21 work.
3. The **five-replication × five-arm** TRAIN-derived internal-validation study requires a dedicated safe launcher, reproducibility QA and separate opt-in. The author requested **no arbitrary full-training wall-clock timeout**; keep memory watchdog, cancellation and checkpoints. Scientific outcomes cannot be claimed from pilots.
4. Build a new report V3 only from verified evidence and exact NotebookLM review text/page anchors; retain V2 immutable. The post-hoc study cannot provide a new independent official TEST.
