# P15 — RF-17 full-TRAIN reconstruction, author-pushed execution evidence QA

**Reviewed 2026-10-16.** Decision: **RF17_FULL_TRAIN = PASS_SCOPED_AUTHOR_EVIDENCE**; **P15/G3 remains PARTIAL** (RF42 and Stacking full still NOT_RUN, separate artifact acceptance pending).

## Evidence

- GitHub author commit: [`78e91117c888d9e1651a20211d364aae47887cf6`](https://github.com/nphu0811/EnsembleLearning/commit/78e91117c888d9e1651a20211d364aae47887cf6) (pushed logs, no serialized final model).
- Inputs retrieved READ ONLY: `results/reproducibility/p15_local_rf17_full_01/run_report.json`, `worker/worker_result.json`, `resources.csv`, and `start.json`.
- Matching prior RF17 pilot: `results/reproducibility/p15_local_rf17_pilot_01/run_report.json`.
- A **20/20 field-and-resource-trace consistency audit PASS** with no mismatch: valid mode/candidate, supervisor+worker PASS, exit0/no abort, rows, ordered17 features, labels/threshold, source+environment and pilot agreement, worker report echoed by supervisor, 620 trace samples, extrema, monitoring floors/budget, claimed artifact metadata, run duration and release scope. This is a log audit only; **the local binary .joblib was not transferred to GitHub or independently loaded**.

## Measured execution and saved-artifact claim

| Field | User-run report / checked trace |
|---|---:|
| Candidate | `random_forest_17` |
| Mode | `full` |
| TRAIN rows | **175,341** (all official TRAIN), 17 frozen features |
| Classes / decision threshold | [0,1] / **0.5** |
| Worker fit time | **307.453 seconds** |
| Last resource-log timestamp | **315.03 seconds** |
| Resource samples | **620** (approximately 0.5s apart) |
| RAM available before start | **5.553 GiB** |
| Minimum sampled system available RAM | **5.222 GiB** |
| Peak sampled process-tree RSS | **535,023,616 bytes = 510.24 MiB** |
| Process-tree RSS limit | **2 GiB** |
| Watchdog | `exit_code=0`, `stop_reason=null` |
| Worker model-file claim | `random_forest_17_RECONSTRUCTED_FULL_TRAIN.joblib` |
| Serialized artifact size (claimed) | **22,169,429 bytes = 21.14 MiB** |
| Serialized artifact SHA-256 (claimed) | `b2751bfc6677a724bcadc85070e5848c0f183c3c81d508b5e4cdae82287c8818` |
| Release certification | **false** |
| Official TEST | **Not opened** |

All four scientific input SHA-256 values match previously locked original TRAIN, source P9 builder, freeze candidates and stable feature subset. Reports record Python3.11.9, scikit-learn1.9.0, two logical-core affinity and watchdog. The former canonical 9-GiB RAM gate is *still* false; the separately documented supervised 12-GB-host alternative admission gate was true for this run.

The worker claims TRAIN-only probability/label/software roundtrip and serialized file SHA-256 verification; the supervisor code checks the model-file hash during author execution before recording PASS. **This independent GitHub audit cannot directly read or recompute the local .joblib SHA, independently deserialize the artifact, or certify original historical model equivalence.** Do not use reconstructed probabilities as if they were earlier official TEST predictions.

## Interpretive boundary

- RF17 full software/model-artifact reconstruction is **supported by author-pushed source, metadata and log evidence**. It does NOT prove historical original-environment reproducibility (original environment UNKNOWN), and does not compare generalized performance.
- **P15 still PARTIAL, G3 open:** only one of three required frozen candidates has a reported full reconstruction. RF42 and Stacking still need full-TRAIN runs and independent artifact acceptance/reproducibility documentation before P15 can be closed.
- **Do not rewrite the approved five-chapter PDF, raw TRAIN, TEST, P9 historical script, frozen metrics or candidate thresholds.** Do not upload binary joblib or raw UNSW data to the public repository.

## Next exact candidate: RF-42 full (when RAM >=4GiB free)

From repository root in Windows PowerShell, after `git pull --ff-only origin main`, save work/close heavy applications, confirm free RAM and no other training process. Run **only**:

```powershell
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate random_forest_42 --pilot-report results/reproducibility/p15_local_rf42_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_rf42_full_01
```

The output directory must not exist. Watchdog uses process-tree 2 GiB cap, 1.5 GiB free system RAM floor, >=10 GiB disk, 20 min timeout, one fit at a time. **RF42 full RAM/runtime is not guaranteed by the 10k pilot or RF17 full.** If the runner fails or aborts, preserve logs, do not bypass guard/increase estimator search, and request a resource review.

Afterward author can push **only run_report.json, worker/worker_result.json and resources.csv**; leave `*_RECONSTRUCTED_FULL_TRAIN.joblib` on the laptop. No need to repeat RF17 full.
