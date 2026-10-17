# P21 — Feature Selection Pilot for RQ2 (18/10/2026)

**Status: IMPLEMENTED; SYNTHETIC QA PASS; NOT YET EXECUTED ON AUTHOR LAPTOP.**

The P21 extension is post-hoc relative to the previously evaluated official TEST. All historical P9/P15 artifacts and 47-page V2 PDF remain immutable. This is a resource/security pilot, not a new scientific RQ2 outcome.

## Methods and controls

The new pilot uses three prior feature-ranking approaches on a strictly FIT-only sample: MI filter (Spearman redundancy cutoff 0.95), L1 logistic regression (liblinear, C=0.1), and ExtraTrees (200 trees, leaf2, one CPU). It runs each method with the five predeclared selection seeds 11, 23, 42, 71, 101, aggregates top20 frequencies, then ranks original predictors by the number of methods satisfying >=3/5, mean frequency, and feature name for ties, taking exactly 17.

For a default 8,000-row resource pilot, each selection seed uses 4,667 rows (scaled from the full-study 35k/60k ratio). The final 60k scientific per-replication subset selection MUST be refitted from scratch later; neither the historical TRAIN-wide stable17 nor any 8k pilot-selected feature names may substitute for it. No pilot feature names, model binaries or per-row predictions are committed.

Worker tools/p21_selector_pilot_worker.py reads only checksum-verified official TRAIN and uses the locked StratifiedGroupKFold split from P21 (exact-vector grouped, fold0). It samples only from FIT_POOL, preserves original indices, rejects all validation/fit index intersection and any identity/label predictor. The worker never fits on validation, never predicts validation, never computes F1/MCC/accuracy, and never opens official TEST.

Supervisor tools/p21_selector_pilot_supervisor.py requires a separate explicit authorization token and a fresh output directory, with ≥4GiB available RAM at startup, 2GiB process-tree RSS cap, 1.5GiB available RAM floor, ≥10GiB free disk, one CPU and a 20-minute ceiling. It records limited resource and selector-safety metadata. All transient local logs and models are ignored by Git.

## Synthetic-only GitHub QA

GitHub Actions run: https://github.com/nphu0811/EnsembleLearning/actions/runs/39065559976 — SUCCESS.

- 14 protocol tests + 7 RF42/pilot-guard tests + 5 RF42 record-acceptance tests + 4 selector-safety tests = **30/30 stdlib tests**.
- 3 synthetic grouped-split tests + 4 synthetic selector tests (including running MI/L1/ET for all five seeds on fabricated rows) = **7/7 synthetic ML tests**.
- **29/29 static source/protocol checks** PASS.
- No raw TRAIN/TEST used by CI; synthetic ML tests do fit selectors to fabricated rows only.

## Optional, author-initiated Windows command

Open PowerShell inside C:\Users\admin\Documents\ChatGPT\NCKH. After freeing memory, issue separately:

    git pull --ff-only origin main

    .\.venv-p15-local\Scripts\python.exe -X utf8 tools/p21_selector_pilot_supervisor.py --authorize I_AUTHORIZE_TRAIN_ONLY_P21_SELECTOR17_PILOT --pilot-rows 8000 --timeout-min 20 --out-dir results/controlled_extensions/p21_train_only_pilot_selector17_01

The target directory must be NEW. If _01 exists, use _02 without deleting old evidence. If RAM/disk is insufficient, the supervisor must fail closed rather than forcing a fit.

Expected report on success: run_report.json status PASS_SELECTOR_RESOURCE_SMOKE_ONLY; worker/worker_result.json passed true, selector_fit_calls=15, selected_feature_count=17, no_validation_rows_used=true, validation_predicted=false, official_test_opened=false and scientific_metrics_calculated=false. A failure or timeout is an honest resource finding, not a science failure; preserve evidence and do not change protocol in response to score.

If sharing a run, commit only start.json, run_report.json and worker/worker_result.json. Do not upload resources.csv, worker logs, raw rows/data, chosen pilot feature list, or model artifacts.

## Unresolved next gates

Passing selector pilot only allows progression to independently supervised class-weighting, random oversampling and Stacking-Lite resource pilots. Five-seed scientific comparisons on 60k FIT subsets require separate resource review and explicit author authorization. None of these gates retroactively create an independent TEST or establish ensemble superiority.
