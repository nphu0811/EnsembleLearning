# P15 — RF-17 pilot: independent GitHub artifact review (2026-10-16)

**Review scope:** User-pushed read-only artifacts; no model fit/predict performed by reviewer. **P15/G3 remains PARTIAL.**

## Source and scope
- Tracked pilot `results/reproducibility/p15_local_rf17_pilot_01/run_report.json`, `worker/worker_result.json`, `resources.csv`, `start.json` at GitHub `main` head `ab88db808dc19fb913fe35a5823f72da14360177` (this review's input).
- Run's source `git_head`: `7596bded6cff1b7f7e71e5ed44ee9a68c3d27226`. Later Git commits do **not** mean the original model sources/configs changed.
- Input SHA-256 values reported in run/worker match project frozen P15 plan for TRAIN, P9 builder, freeze and feature subset; 17 ordered features and decision threshold 0.5 preserved.

## Cross-checked run findings

| Field | Value |
|---|---|
| Candidate / mode | `random_forest_17` / `pilot` |
| Outcome | `PASS`; worker checks PASS; exit code 0 |
| TRAIN rows in pilot | 10,000 (TRAIN-derived stratified subset, no official TEST) |
| Start available system RAM | 7,474,434,048 bytes = 6.960 GiB |
| Lowest sampled system available RAM | 7,161,253,888 bytes = 6.670 GiB |
| Max sampled process-tree RSS | 370,864,128 bytes = 353.68 MiB |
| Process-tree RSS policy | max 2 GiB |
| Resource observations | 24 at ~0.5-s interval |
| Worker fit time | 5.125 seconds |
| Termination | `stop_reason=null`; `exit_code=0` |
| Python | 3.11.9; observed scikit-learn 1.9.0 (historical environment UNKNOWN) |
| CPU setting | affinity cores [0,1] |
| Frozen decision | class [0,1], threshold 0.5 |

The **pilot's measured max RSS is below 75% of the 2-GiB process-tree ceiling**, a required (but insufficient) next-stage headroom condition. The reported minimum sampled available system RAM is above 1.5 GiB. None of these figures bounds full-TRAIN peak memory: the full fit may build trees with different sizes, incur extra allocations or exceed the configured budget.

No serialized **full-TRAIN** RF-17/RF-42/Stacking artifacts are present in this audited run. Pilot roundtrip does **not** constitute a held-out TEST evaluation. The run report has `release_certified=false`, and the canonical 9-GiB preflight gate remained false under the alternative monitored admission policy.

## Repository hygiene finding requiring author action

Commit `ab88db8` tracked approximately 7,401 tree objects under `.venv-p15-local/` (about 97,727,898 bytes of tracked blobs). These files are installed environment dependencies, not scientific source/evidence. The `.gitignore` on subsequent main now includes `.venv-p15-local/`, **but adding an ignore pattern does not untrack existing files**.

**DO NOT remotely delete tracked virtualenv files without preparing the laptop**: pulling a deletion commit can remove the author's tracked local venv files. To safely untrack, the author should run `git rm -r --cached -- .venv-p15-local` on the laptop, verify files still exist on disk, commit the staged index-only removal and push. See `docs/research/P15_GIT_VENV_SAFE_CLEANUP_2026-10-16.md`. This does not purge earlier public Git history; no history rewrite was performed or authorized.

## Recommended next step

1. On the laptop, confirm RAM >=4 GiB free and that the previous RF-17 pilot has fully stopped; preserve work and avoid heavy concurrent apps.
2. Run **RF-42 pilot** with a new directory, then **Stacking-42 pilot** sequentially. Capture each `run_report.json`, RSS and stderr. Do not infer either candidate will match RF-17's memory profile.
3. Only after **each candidate's own** pilot PASS and <75% peak RSS, consider that candidate's one-time full 175,341 TRAIN fitting under the same bounded supervisor. Pre-run science/source hashes and available RAM must be checked again.
4. Keep raw TEST untouched, no retune, no frozen-result overwrite; report aborts/partial results honestly.

**Status:** `RF17_PILOT_DONE_SCOPED`; `RF17_FULL=NOT_RUN`, `RF42_PILOT=NOT_RUN`, `STACK_PILOT=NOT_RUN`, `G3/P15=PARTIAL`.
