# P15 — RF-42 full TIMEOUT: bounded-resource recovery with no wall-clock deadline

**Date:** 2026-10-17 (Vietnam local). **Scientific status:** RF17 full author-evidence PASS; RF42 full first attempt INCOMPLETE; Stacking full NOT_RUN; P15/G3 PARTIAL.

## Frozen evidence — previous RF42 full attempt

- Author GitHub commit `5c02bf5a38619fe457537beb79df59a3d78726dc`.
- Original immutable attempt: `results/reproducibility/p15_local_rf42_full_01/`.
- `run_report.json`: `mode=full`, `candidate=random_forest_42`, `result=INCOMPLETE`, `stop_reason=TIMEOUT`, `exit_code=15`, `worker_checks.passed=false`.
- Watched `resources.csv`: **2,358 samples**, last at **1,200.12 seconds**, maximum tree RSS **483,598,336 bytes = 461.20 MiB**, minimum available system RAM **5,823,201,280 bytes = 5.424 GiB**, min disk free **30,537,601,024 bytes (~28.44 GiB)**. Start available RAM **6,328,860,672 bytes = 5.894 GiB**. Default 2 GiB process RSS cap never reached, and the 1.5 GiB remaining-system-RAM floor was not violated.
- This was **not** a memory failure and did **not** produce a confirmed full model. No `worker_result.json` or `.joblib` was pushed for the timed-out run. Local stderr/stdout are ignored by Git; without them the exact fit progress at kill time is unknown.
- No reason to lower number of trees, change the 42 features, tune threshold/folds, reread official TEST, or overwrite frozen scientific metrics.

## Explicit author request to change operational deadline

The author requests the **remaining two full jobs** execute for as long as necessary, because they can free approximately 8–9 GiB system RAM by closing other apps. This request supersedes **only the 20-minute wall-clock limit for these new full attempts**, not the prior evidence nor the original R05 planning assumptions. The original conservative 9-GiB free RAM gate is a separate historical admission threshold and remains documented as FAIL in prior runs.

Implementation on `main`:
- `tools/p15_local_supervisor.py`: `--timeout-min 0` valid **only** with `--mode full`; a sentinel disables the **wall-time cutoff only**. A positive timeout remains bounded to 5–20 min; pilots cannot opt out. The `wall_time_policy` record is emitted into `start.json` and `run_report.json`.
- **Watchdog remains continuously active at ~0.5 second samples**: max process-tree RSS **2 GiB** unless explicitly configured otherwise (do NOT raise), min remaining system RAM **1.5 GiB**, disk free min **10 GiB**, mandatory initial free RAM **>=4 GiB** for the alternative policy (no assumption about 8–9 GiB until fresh measurement), checksums/gates/heartbeat, and a kill of subprocess family on abort/interruption. The kernel is still not enforcing a hard memory allocation cap.
- `tools/p15_run_remaining_full_windows.ps1`: **sequential only**, new RF42 `p15_local_rf42_full_02` then new Stacking `p15_local_stack_full_01`; never start the second unless first exits 0 **and** its `run_report.json` confirms supervisor/worker PASS with 175,341 rows, full mode, correct candidate and no deadline. Each model must pass its own matching pilot provenance check.
- No automatic retries, no background detached jobs, no changes to original P9 source, frozen manifest/feature selection, official TEST, raw data, or approved PDF. The prior timed-out directory is preserved and must never be reused.

## How to launch (Windows PowerShell at NCKH root)

First pull `main` and ensure tracked tree clean, save all work, keep laptop plugged into AC power with adequate ventilation, disable **automatic sleep while plugged in** (display may switch off). Close heavyweight apps and stop any running training processes. Do not disable Windows security, pagefile, or system monitoring. Confirm RAM and disk. The local supervised admission gate will refuse if RAM available <4 GiB or disk <10 GiB.

```powershell
git pull --ff-only origin main
.\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p 'test_p15_local_supervisor.py' -v
.\.venv-p15-local\Scripts\python.exe -c "import psutil; print('Available RAM (GiB):', round(psutil.virtual_memory().available/1024**3,2))"
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\p15_run_remaining_full_windows.ps1
```

`-ExecutionPolicy Bypass` above affects the **spawned PowerShell process only**, so that this reviewed local script can run even under the common Restricted execution policy; it does not change your persistent computer policy. Review this repo script before invoking. If corporate/org execution policy prevents it, obey the restriction and use the two commands below separately; do not try to bypass mandatory administrative policy.

Equivalent explicit sequential steps, each command after confirming previous PASS and fresh available RAM (new output dirs must not exist):

```powershell
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate random_forest_42 --pilot-report results/reproducibility/p15_local_rf42_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_rf42_full_02 --timeout-min 0
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate stacking_42 --pilot-report results/reproducibility/p15_local_stack_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_stack_full_01 --timeout-min 0
```

**No time deadline means a hung worker could run indefinitely even at safe RSS.** The watchdog monitors resource safety, **not CPU progress or completion**. If stalled for hours with no meaningful CPU activity, manually interrupt with **Ctrl+C** and preserve incomplete logs. A long run may also be suspended/interrupted by OS sleep, power loss, restart or Windows Update. Reusing or renaming a partial model as final is prohibited.

## Acceptance

Each full report must have `result=PASS`, `mode=full`, `train_rows=175341`, frozen source SHA256, schema/threshold/classes, valid local .joblib artifact SHA256 and package/runtime provenance, `exit_code=0`, `stop_reason=null`; if no-deadline mode then `wall_time_policy.enabled=false`. Supervisor verifies the actual local file SHA before recording PASS. **Remote documentation review cannot independently inspect laptop-only .joblib.**

Push just the fresh `run_report.json`, `worker/worker_result.json`, `resources.csv` (optionally `start.json`) to GitHub. Do **not** push the binary .joblib, raw datasets or virtual environment. The final P15 reproducibility gate still requires independent artifact inspection and provenance review; even two full PASS logs do not imply historical bitwise identity or fresh TEST performance. Preserve RF42 TIMEOUT attempt as an auditable negative/operational observation.
