# P21 RF42 resource-only pilot — implementation and acceptance gates

**Status 18/10/2026:** `IMPLEMENTED_AND_SYNTHETIC_QA_PASS; AUTHOR_RUN_NOT_STARTED`. The user completed exact P21 laptop protocol preflight: **30/30 PASS** including `explicit_train_sha256`, with `official_test_read=false`, `training_performed=false`. There is still **no P21 model training or new scientific score**.

## New launcher and pilot

- `tools/p21_pilot_guards.py`: stdlib-only safety rules (fresh sandboxed output, only official TRAIN dataset reads under project data, resource gate).
- `tools/p21_pilot_worker.py`: standalone execution *denied* except via watched parent. Rechecks official TRAIN SHA, group-disjoint internal validation using 42-predictor vector hashes with collision check and locked `StratifiedGroupKFold` fold0, validates group/row disjointness and 18–22%/2pp class balance. Takes 8k default (up to 20k) **only from internal fit pool**; fits a single `A0_RF42_NONE` RF150/leaf2/maxfeatures.5/threshold.5 pipeline, CPU/thread limited. Runs only 16 TRAIN-sample probability schema sanity checks; **never predicts on validation or computes any performance metric**. No serialized model produced.
- `tools/p21_pilot_supervisor.py`: requires exact explicit author consent flag `--authorize I_AUTHORIZE_TRAIN_ONLY_P21_RF42_PILOT`, `--out-dir` new `results/controlled_extensions/p21_train_only_pilot_rf42_*`, 1 worker/one CPU, 2GiB peak process-tree RSS, >=4GiB starting available RAM, >=1.5GiB available at all times, >=10GiB free disk, 5–20 min hard deadline, 0.5s sampling and fail-closed worker kill. `--timeout-min 0` refused. Revalidates official TRAIN SHA + P21 frozen-source protocol (30/30) before launching; worker requires go.signal/heartbeat. Records START/RUN reports and worker PASS evidence with no raw prediction vectors, raw data rows, TEST labels, metrics or binaries.
- `tests/test_p21_pilot_guards.py`: seven fixture-only tests for safe output/worker boundary, refused TEST/non-TRAIN data access, resource budget, timeouts and forged worker report rejection; existing 14 P21 protocol tests.
- CI `https://github.com/nphu0811/EnsembleLearning/actions/runs/39061590713` PASS: **14/14 protocol tests + 7/7 pilot tests + 29/29 static source checks**, no raw data, ML packages, model fitting, validation scoring or TEST access.
- `results/controlled_extensions/.gitkeep` tracks intended separate output root; `.gitignore` excludes temporary pilot signals, logs, sampled memory telemetry and any future `.joblib` files.

## Exact author-host invocation — OPTIONAL, explicit opt-in to the resource smoke only

First close memory-intensive apps and confirm sufficient free RAM/disk. From the NCKH workspace PowerShell:

```powershell
git pull --ff-only origin main
.\.venv-p15-local\Scripts\python.exe -X utf8 tools/p21_pilot_supervisor.py --authorize I_AUTHORIZE_TRAIN_ONLY_P21_RF42_PILOT --pilot-rows 8000 --timeout-min 20 --out-dir results/controlled_extensions/p21_train_only_pilot_rf42_01
```

If file/dir `_01` exists, never overwrite it: choose `_02` and preserve `_01` including failures. If free RAM <4GiB or disk<10GiB, result must be `NO_GO_RESOURCE_GATE` with no worker. If group split 18–22%/2pp criterion fails, worker exits NONZERO with recorded reason; do not change split seed/scheme based on score or silently relax protocol. Logs `worker.stderr.log` available locally and ignored by Git. **Expected accepted pilot**: `run_report.json.status=PASS_RESOURCE_SMOKE_ONLY`, `worker/worker_result.json.passed=true`, peak sampled RSS <2GiB, no timeout, and validation-evaluation flags all false.

Push **only compact non-record-level** `run_report.json` and `worker/worker_result.json` if author wishes external review. Never upload raw TRAIN/TEST, worker logs, model binaries, local row IDs or per-record predictions. Keep failed telemetry locally.

## Important limits and further P21 plan

This pilot measures **only RF42 anchor's environment/splitting/fit feasibility** and **cannot** authorize 25 model fits or establish RQ1/RQ2/RQ5 results. The full P21 stage still needs: (1) selector stability/top17 fit-only pilot across five seed/method subsets with 17-feature deterministic ranking, (2) balanced/oversampled RF42 pilot, (3) Stack-Lite inner 3-fold pilot, (4) stronger **synthetic ML split/fit-only** tests executed in a controlled ML environment, (5) capacity review and **separate explicit author authorization** before scientific five-seed matrix.

The P21 design contract remains `training_authorized=false` and `first_experiment_executed=false`. The CLI consent authorizes only the bounded component resource pilot; it does not change science or PDF V2. The historical 37-page PDF and revised 47-page PDF remain untouched. P20 final, P18 and P19 gates remain open.
