# P15 — Full TRAIN reconstruction on 12 GB Windows laptop: three author-reported PASS runs

**QA date:** 17 October 2026. **Evidence source:** user-pushed GitHub commit [`d090c163a3c20f5637a8e500fdb7afc552ddbe9f`](https://github.com/nphu0811/EnsembleLearning/commit/d090c163a3c20f5637a8e500fdb7afc552ddbe9f).

**Decision: THREE_FULL_TRAIN_AUTHOR_EVIDENCE = PASS_SCOPED. P15 artifact acceptance still OPEN; G3 not yet closed.**

## What was actually inspected

Without loading models or executing ML, independently retrieved the four recorded artifacts `run_report.json`, `worker/worker_result.json`, `resources.csv`, `start.json` from each of:

- `results/reproducibility/p15_local_rf17_full_01`
- `results/reproducibility/p15_local_rf42_full_02`
- `results/reproducibility/p15_local_stack_full_01`

The local `*.joblib` binaries remain on the author's Windows laptop; they were **not** uploaded to GitHub or independently deserialized during this QA.

**All 75/75 read-only evidence consistency predicates PASS:** 23 checks for each run, six cross-run checks. Conditions included full mode, matching frozen candidate, worker/supervisor PASS, entire TRAIN 175341, exact ordered feature cardinality, labels[0,1]/threshold0.5, source hashes and environment parity, report+worker/start congruence, exact resource trace sample count and peak/minima, RAM/disk safety, exit0/no stop, model artifact filename/byte count/SHA256 *reported* metadata, valid original/no-release/TEST distinction, monotonic trace and wall-time policy. This is **not** an independent scientific repetition or verified local binary read.

## Reported measured results and checked resource traces

| Metric | RF17 full | RF42 full | Stacking42 full |
|---|---:|---:|---:|
| Result | PASS | PASS | PASS |
| Original official TRAIN rows | 175,341 | 175,341 | 175,341 |
| Feature count | 17 | 42 | 42 |
| Fit seconds | 307.453 | 1,867.234 | 4,759.094 |
| Fit minutes | 5.124 | 31.121 | 79.318 |
| Total resource-log elapsed minutes | 5.251 | 31.288 | 79.477 |
| Max observed process-tree RSS (MiB) | 510.24 | 693.57 | 725.33 |
| Minimum observed available system RAM (GiB) | 5.222 | 5.909 | 5.744 |
| Available RAM at start (GiB) | 5.553 | 6.771 | 6.877 |
| Resource samples | 620 | 3,693 | 9,379 |
| Min observed disk free (GiB) | 28.441 | 28.374 | 28.192 |
| Exit / watchdog stop | 0 / null | 0 / null | 0 / null |
| Run time deadline | 20 minutes | none (opt-in) | none (opt-in) |
| Serialized artifact bytes (reported) | 22,169,429 | 42,207,326 | 42,368,839 |
| Artifact MiB (reported) | 21.142 | 40.252 | 40.406 |

Reported model binary hashes (locally checked at execution by supervisor, **not yet independently recomputed**):
- RF17 `b2751bfc6677a724bcadc85070e5848c0f183c3c81d508b5e4cdae82287c8818`
- RF42 `9509b1561e50488c756ac986595da4efd9f75a8ede6a8fc4c1f04f15ce85ef8d`
- Stacking42 `cb0d9b6c50ca19f83982a7bdf5d952d468cb6de9412234791db03efaee594995`

Both RF42 and Stacking used `--timeout-min 0` only on the *new* full attempts. Their `wall_time_policy` in `start.json` and final report agrees. Peak memory of every run remained below the separately set 2GiB RSS sampled-process cap, and system RAM remained above the 1.5GiB floor. This is observed, **not a machine-guaranteed allocation maximum**, and not a proof other hosts will behave the same.

All three runs used recorded Python 3.11.9, NumPy 2.4.6, pandas 3.0.5, scikit-learn 1.9.0, SciPy 1.17.1, joblib 1.5.3, threadpoolctl 3.6.0, psutil 7.2.2. The original historical environment remains UNKNOWN.

All 4 frozen input SHA-256 fingerprints in all 3 reports and worker outputs agreed with the approved P15 source/train/freeze/subset; the reports did not open official TEST or recompute scientific performance measures.

## Preserved unsuccessful attempt

`results/reproducibility/p15_local_rf42_full_01` stopped at the earlier *20-minute* `TIMEOUT` and is **INCOMPLETE**, not deleted or altered. RSS peak461 MiB and available RAM safely above floor proved that particular observed stop reason was operational timebox, not a memory limit. The successful replacement is a distinct `p15_local_rf42_full_02` run; do **not** silently reinterpret or overwrite the prior failure.

## What still needs to be checked before closing P15/G3

1. **Fresh laptop-side file verification** on all 3 physical `*_RECONSTRUCTED_FULL_TRAIN.joblib` files. Verify SHA256, byte sizes, deserialize the already-trained models from a fresh process, confirm fitted estimators, feature schema/parameters, class-probability behavior on only 16 TRAIN rows, runtime versions, and no TEST reading. No new fitting or new generalization metric.
2. Preserve the resulting limited acceptance report with explicit scope, not the joblib binaries. `tools/p15_verify_full_artifacts.py` is the dedicated verifier; author should run it from local Python 3.11 venv and push `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json` **if PASS**.
3. QA reviewer checks the pushed acceptance report and release provenance independently; P15 may then be marked **DONE_SCOPED_RECONSTRUCTION** (not historical bitwise identity, not new official TEST performance). G3 release/demo and G0–G6 administrative/scientific gates remain separate.

## Local next step once verifier is on GitHub

```powershell
git pull --ff-only origin main
.\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p "test_p15_artifact_acceptance.py" -v
.\.venv-p15-local\Scripts\python.exe tools/p15_verify_full_artifacts.py --out-dir results/reproducibility/p15_local_artifact_qa_01
```

The verifier must **never** load a `.joblib` from any untrusted sender (pickle code execution risk). This tool runs on author-generated local artifacts only. It will store a new JSON result without models/probabilities, does not touch TEST, does not overwrite scientific evidence and does not train. If it fails, leave original models/logs unchanged and inspect the saved reason; do not call it PASS.
