# P21 protocol static QA closure — DESIGN ONLY (18/10/2026)

**Status:** `P21_DESIGN_QA_PASS / P21_TRAINING_NOT_AUTHORIZED / NO_EXPERIMENT_STARTED`. This protocol is a **controlled post-hoc extension** outside historical roadmap P00–P20, **not** a rewrite of frozen research questions or official TEST.

## Evidence and actual tests

- Protocol `docs/research/P21_TRAIN_ONLY_CONTROLLED_EXTENSION_PROTOCOL_2026-10-18.md`, immutable machine-readable contract `config/p21_train_only_protocol_2026_10_18.json`.
- Executable **static-only**, stdlib validator `tools/p21_protocol_validator.py` and `tests/test_p21_train_only_protocol.py`: check source input lineage, split/group policy, training-only refitted stable-top17 features, matched RF42/RF17 hyperparameters, three weight/oversample arms, five fixed replication seeds, resource watchdog budget, no official TEST, safety and no frozen artifact overwrite.
- [GitHub Actions run 39060348600](https://github.com/nphu0811/EnsembleLearning/actions/runs/39060348600) **SUCCESS: 10/10 regression tests, 29/29 protocol/static source checks**, 0 failure. CI never installed sklearn/pandas, loaded raw dataset or model, trained/predicted, or read official TEST.
- File hash reconciliation: `src/models/run_unsw_phase9_final_holdout.py` Git SHA256 equals frozen P15 `3e7d1369...80ae480`. Git contains LF:
  - `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`: Git LF `7e9b99b39c455379871af93e447c80e375232ad66d9aae4075c105059dd1f6e7`; byte-converted CRLF SHA256 `cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6`, identical with author Windows P15 record.
  - `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`: Git LF `1066e0791b13f681f72426636ca0713bb6c3316aacebf09d2f9b3b34121125e1`; CRLF SHA256 `5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be`, identical with P15.
  - Hash conversion is **read-only**, and both original strings from local P15 provenance remain intact. Early static workflow runs failed due unhandled LF/CRLF difference; those failure logs are preserved, not reclassified as PASS.

## Design in one view

- One internal TRAIN-only group-disjoint stratified 5-fold split (fold0 validation ~20%, 80% fit pool), exact-vector grouping; no claim of host/session/time split or independent external data.
- Five seeds [1103,2207,3301,4409,5501], each selects stratified 60000 rows from fit pool, fixed single validation view. `stable_top17` **refitted within that replicate's fit subset**, using 5×35k training-only samples for MI/L1/ExtraTrees; original full-TRAIN stable17 cannot be used as independent internal-val FS.
- Five model arms per seed: `RF42_NONE` shared by RQ1/RQ2/RQ5, `RF17_NONE` matched to RF42 hyperparameters except train-refitted features, `RF42_BALANCED`, `RF42_OVERSAMPLE` training-only duplicate minority, `STACK42_NONE` same RF150 anchor with LR/DT/meta. **20 RF fits + 5 Stacking fits** if all 5 seeds run, plus 5 selectors.
- The five repeated results are **exploratory training-subset+RNG robustness under a common held-out subset**, not iid repeated-training significance, no deterministic superiority claims. New RF150/leaf2 and Stack-Lite are not original frozen candidates; internal-val class distribution differs from official TEST and must not be pooled with P9 holdout metrics.
- Config sets `training_authorized=false`, `first_experiment_executed=false`; no P21 runner has been released yet. Before executing, author must authorize **pilot separately** after a user-local resource/read-TRAIN SHA preflight. Pilot only validates compute feasibility and leakage safety, not outcome selection.

## Next acceptance gate

1. Author pulls `main` and can run **read-only** `python -X utf8 tools/p21_protocol_validator.py --verify-local-train-sha`. It reads official TRAIN as opaque bytes **only to compare SHA**; no raw TEST, no model or sample creation. If no local TRAIN, the command fails visibly without fabricating success.
2. Build a separate P21 pilot worker/supervisor (new paths only); unit tests on synthetic rows prove no leakage and FIFO execution safety; no reused P9/Stage2 `main()`.
3. Check RAM gate >=4GiB free, watchdog process tree 2GiB cap, system floor 1.5GiB, disk >=10GiB, pilot fit subset<=20k. Then author explicitly approves pilot run. Use pilot resource logs to accept / block 60000-row scientific extension **without inspecting metrics**.
4. Only complete 5 paired seed runs after feasibility authorization; keep missing arms as INCOMPLETE, preserve any negative results. Do not produce PDF V3 until source/metric QA and author decides.

**Unchanged**: P15 full TRAIN reconstruction, 47-page PDF V2 sha `5300f9de92a7fc3834294b015382acfff80c9f0384ef9d6a32419e2bf72b52f3`, official TEST and historical paper metrics, P20 original reviewer reports. P18/P19/licensing and G0–G6 remain separate.
