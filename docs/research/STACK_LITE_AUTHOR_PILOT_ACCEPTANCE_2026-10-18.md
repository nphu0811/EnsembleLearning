# P21 Stacking-Lite resource pilot author acceptance (18 October 2026)

**Evidence source:** Author commit [c075191](https://github.com/nphu0811/EnsembleLearning/commit/c075191); `results/controlled_extensions/p21_train_only_pilot_stacklite_01/run_report.json` and its `worker/worker_result.json`. Verified against actual committed metadata, not re-executed on our machine.

**Decision:** `PASS_STACK_LITE_RESOURCE_SMOKE_ONLY` for strictly TRAIN-FIT-only Stacking feasibility. **NOT RQ1 scientific validation, no official TEST and no reproduced holdout estimate.**

- Official TRAIN SHA-256: `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`. Protocol SHA-256 `3a4c21cd069432c36cb8cfcdb863dbd4898845cd095fb4111be34b8d0c455c86`.
- 175341 rows source; group-disjoint internal split: 140272 FIT pool + 35069 internal validation; 8000 rows sampled only from FIT for pilot (2555 Normal, 5445 Attack).
- 42 input features; LR/DT/RF Stacking with 3-fold inner CV. Worker-reported fit time **38.937 s**; wall time **90.812 s** (separate worker setup/split overhead). Process-tree peak **352333824 bytes = 336.0 MiB**; minimum system available RAM **5395247104 bytes**. `exit_code=0`, `stop_reason=null`.
- Worker-reported `official_test_opened=false`, `validation_predicted=false`, `scientific_metrics_calculated=false`, `model_artifact_saved=false`; evidence flags are consistent with source scope, not independently instrumented host attestation.
- `go.signal`, `heartbeat`, `resources.csv` were included by author's `git add .` in c075191. Keep the historical evidence; new `.gitignore` prevents **untracked future** runtime files from being staged, but does not remove these already-tracked artifacts. Prefer selected safe JSONs for research release; do not rewrite history.

**Next gate:** A **new** five-arm full P21 study per preselected replication seed (1103/2207/3301/4409/5501), tested and supervised separately, with 60000 FIT rows per seed. This is a *post-hoc reused-TRAIN internal-validation* extension, not a prospective independent confirmation or replacement for frozen P9/P15. Full runs use no arbitrary wall clock time limit but fail closed on resource budget.

**Potential methodological adjustment:** pilot stacking used `StratifiedKFold` without exact-vector grouping. For full scientific runs, a pre-run amendment mandates `StratifiedGroupKFold` for inner stacking folds, as independently documented. Therefore the pilot validates approximate resource feasibility rather than guaranteeing full-run fit time or identical CV behavior.
