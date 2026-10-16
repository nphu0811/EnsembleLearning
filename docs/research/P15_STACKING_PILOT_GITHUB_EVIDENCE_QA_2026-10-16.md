# P15 — Stacking-42 10k TRAIN pilot: independent GitHub evidence QA

**Reviewed:** 2026-10-16. **Status:** DONE_SCOPED_PILOT; G3/P15 still PARTIAL, no full-TRAIN model reconstructed.
**Scope:** Read-only examination and arithmetic consistency checks on **author-pushed artifacts**, not fresh fitting or TEST validation.

## Evidence and baseline

- Author push (evidence input): `b4707dc9f3fab6750007f08b4df2d8475233bbd7` (`supervisor`).
- `results/reproducibility/p15_local_stack_pilot_01/run_report.json`
- `results/reproducibility/p15_local_stack_pilot_01/worker/worker_result.json`
- `results/reproducibility/p15_local_stack_pilot_01/resources.csv`
- `results/reproducibility/p15_local_stack_pilot_01/start.json`
- The run was made from local Git HEAD `de40b9437c3ff18ec24a19327ba99286731dd201`, which differs from subsequent documentation commits; tracked frozen science input SHA-256 values agree with the earlier RF17/RF42 pilots and original P15 expected hashes.
- Crosschecked **21/21 independent consistency predicates PASS** over three pilot reports and Stacking worker/resource log, including SHA field agreement, matching package versions (key-order invariant), 170 CSV rows and exact reported resource extrema, no stop reason, class/threshold/feature contract, safety budget, and scope label. This is NOT a fresh ML experiment or proof that a full fit will fit inside 2 GiB RSS.

## Observed figures

| Field | Observed |
|---|---:|
| Mode/candidate | `pilot` / `stacking_42` |
| Report and worker | `PASS` / `passed=true` |
| Rows / features | 10,000 official TRAIN-derived rows / ordered 42 unique predictors |
| Class/threshold | [0,1] / 0.5 |
| Local Python | 3.11.9; scikit-learn 1.9.0, psutil 7.2.2 |
| CPU affinity | [0,1] |
| Supervisor RAM available at start | 6,140,862,464 bytes = **5.719 GiB** |
| Lowest sampled system RAM available | 5,776,723,968 bytes = **5.380 GiB** |
| Peak sampled process-tree RSS | 368,455,680 bytes = **351.39 MiB** |
| RSS ceiling | 2,147,483,648 bytes = **2 GiB**, peak uses ~17.16% |
| Worker fit time | **80.968 s** |
| Resource samples | **170** samples at approximately 0.5-s intervals |
| Exit/abort | exit code 0, `stop_reason=null` |
| Evaluation scope | TRAIN-derived 16-row roundtrip only, **no official TEST** |
| Release flag | `release_certified=false` |

## All pilot comparison

| Candidate | 10k sample status | Max sampled process-tree RSS | Fit time |
|---|---|---:|---:|
| `random_forest_17` | PASS | 353.68 MiB | 5.125s |
| `random_forest_42` | PASS | 365.91 MiB | 22.547s |
| `stacking_42` | PASS | 351.39 MiB | 80.968s |

Three 10k pilot outputs are now available with matched source anchors. Each passes the default 75%-of-cap headroom filter and the originally configured alternate local admission policy.

## Next step: supervised FULL TRAIN, one candidate at a time

**Provisional permission to ATTEMPT** RF17 full on the same laptop, not certification or a guarantee: fresh >=4 GiB system available RAM, >=10 GiB disk, no applications requiring unsaved data, matching pilot/executable/input hash, no concurrent ML job, new output directory, 2 GiB process-tree RSS cap and 1.5 GiB remaining system RAM floor. Preserve the canonical 9 GiB gate's separate `FAIL` record; this alternative admission is a local engineering risk-management policy and must never be misreported as meeting the 9 GiB gate.

The supervisor validates pilot-report provenance and config; the worker uses original frozen builders but never executes historical P9 `main()`, never reads official TEST and does not modify historical metrics. Full reconstruction, if successful, is specifically labeled `RECONSTRUCTED_FULL_TRAIN` rather than `ORIGINAL`.

**RF17 first** (new out-dir, do not re-use):
```powershell
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate random_forest_17 --pilot-report results/reproducibility/p15_local_rf17_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_rf17_full_01
```

Wait for report `result=PASS`, a `worker_result.json` with `train_rows=175341`, `mode=full`, SHA and artifact metadata, and an actual `*_RECONSTRUCTED_FULL_TRAIN.joblib` on local disk. Also inspect `resources.csv`, `worker.stderr.log` if any abort. **Do not push serialized .joblib model/raw CSV**. Send the report/logs to review before RF42 full or Stacking full. If `INCOMPLETE`, `TIMEOUT`, memory stop or audit fails, do not simply raise resource limits or change frozen estimators.

Remaining gated evidence: independent local full artifact load/roundtrip in a new process, all three completed full fits, consistent environment provenance/hashes, and separate release/inference approval. No post-hoc TEST metrics or revised P17 report. 
