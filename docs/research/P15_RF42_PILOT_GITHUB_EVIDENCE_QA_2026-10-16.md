# P15 — RF-42 local pilot: independent GitHub evidence QA (2026-10-16)

**Decision: DONE_SCOPED_PILOT; FULL TRAIN NOT RUN; P15/G3 remains PARTIAL.**
This is a source/log audit of user-pushed files, **not** an independent ML execution or a statement of generalization quality.

## Verified source

- GitHub main as of user's report commit [`b0b9c856165f7360c43cd40c3d8ab717ba909748`](https://github.com/nphu0811/EnsembleLearning/commit/b0b9c856165f7360c43cd40c3d8ab717ba909748).
- Input files (read-only): `results/reproducibility/p15_local_rf42_pilot_01/{run_report.json,resources.csv,worker/worker_result.json,start.json}`.
- Source-in-run git head `2a20b7f3aaf192472a0d67be95019e5f48ff4412`; hash of TRAIN, P9 builder, frozen manifest, stable 17 subset match both worker and supervisor and known P15 preflight anchors. Threshold 0.5, binary classes [0,1], 42 unique ordered predictors; Python3.11.9; package names/versions match (JSON field ordering differs only).
- Read-only crosscheck: **19/19 logical conditions pass** after dictionary comparisons by keys (not comparing serialized JSON property ordering). Conditions include outcomes, mode/schema, input/package matches, samples/peaks/floors, 75% headroom, exit code, unchanged scientific provenance and explicit no-full-run boundary.

## Recorded resource profile

| Variable | RF-42 pilot observed |
|---|---:|
| Training sample | 10,000 rows sampled from official TRAIN |
| Worker fit time | 22.547 s |
| Supervisor samples | 55 (last sample 27.52 s) |
| Available RAM at admission | 6,057,549,824 bytes = **5.642 GiB** |
| Minimum available RAM during sampling | 5,708,353,536 bytes = **5.316 GiB** |
| Maximum process-tree sampled RSS | 383,684,608 bytes = **365.91 MiB** |
| Watchdog RSS cap | 2,147,483,648 bytes = **2 GiB** |
| Peak / cap | **17.87%**, below 75% threshold |
| Exit and safety | exit code 0, no stop reason, worker PASS, `release_certified=false` |
| Estimated disk at start | 30,563,332,096 bytes = 28.46 GiB |
| CPU affinity | logical cores [0,1] |

The earlier RF-17 pilot reported 370,864,128 B (353.68 MiB) peak and 5.125 s fit. **No reliable extrapolation to 175,341 full-TRAIN memory/time** is possible from these samples. RF-42 historical full training duration is environment-specific.

## Repository hygiene verified

- The commit cleaning Git tracking followed earlier advice: GitHub `main` recursive tree now contains **0 paths** under `.venv-p15-local/`, compared with ~7,401 tree entries previously tracked.
- `.gitignore` retains `.venv-p15-local/`. This is an index/tree check only; it cannot confirm physical local environment remains intact, although the RF-42 pilot log proves the Python interpreter was present at its start.
- No history rewrite/force push was used by this QA, and previously committed virtualenv blobs may remain in older Git objects.
- The source logs are currently tracked; **do not commit serialized full-model `.joblib`** or raw datasets.

## Remaining gates

**RF-17 PILOT = PASS, RF-42 PILOT = PASS; Stacking-42 PILOT = NOT_RUN.** Next execute one isolated `stacking_42` pilot under the same 2-GiB watchdog cap and >=4-GiB fresh system available RAM gate. It must have independent `run_report.json` and resources.csv before beginning any full training.

Only when that passes, evaluate sequential full reconstruction of each frozen candidate one at a time; full passes require original TRAIN all 175,341 rows, hash/source/schema/probability/joblib roundtrip checks and watchdog evidence. None has yet happened. **The historical 9-GiB preflight policy remains NOT_PASSED; the local 4-GiB pilot alternative is a separate measured-resource policy, not an override of source gates.** Full results do not reopen official TEST or alter frozen research metrics. The five-chapter PDF remains unchanged.

## Exact next command after latest main is pulled (only if RAM >=4 GiB)

```powershell
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate stacking_42 --out-dir results/reproducibility/p15_local_stack_pilot_01
```

The `--out-dir` must be new/not already existing. Stop if any watchdog/resource gate fails; do not run two models in parallel.
