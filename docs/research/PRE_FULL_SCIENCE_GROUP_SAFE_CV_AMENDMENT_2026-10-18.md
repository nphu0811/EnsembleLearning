# P21 PRE-FULL-SCIENCE amendment — GROUP-SAFE stacking inner OOF

**Amendment ID:** `P21_PRE_FULL_SCIENCE_INNER_GROUP_SPLIT_2026-10-18`. Date 18 October 2026. **Status: documented before any full P21 scientific internal-validation run.** Applies ONLY to future P21 science run, not historical P9/P15 or four resource pilots.

## Precisely one protocol improvement

The earlier `P21_TRAIN_ONLY_CONTROLLED_EXTENSION_V1` specified Stacking-Lite inner `StratifiedKFold(n_splits=3, shuffle=True, random_state=137)`. Exact duplicate 42-predictor vectors may be present on both inner FIT and OOF validation folds if those rows are split independently, leading to optimistic meta-features. The author already acknowledged exact-vector dependence in the outer split. The full P21 worker therefore constructs all three **StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=137)** inner folds using the same canonical 42 original-predictor vector hashes **from that seed's 60000 FIT subset only**.

- A group never straddles inner train and inner validation. The three OOF validation arrays partition the FIT subset exactly. All inner folds must contain both classes, or fail closed before model fit.
- Group fingerprints exclude label, `id`, `attack_cat`; hash collisions between differing rows are rejected. The grouping itself is unsupervised and never accesses outer validation labels or rows.
- Fold count, seed, base LR/DT/RF, meta LR, thresholds, fit subset sizes, all five arms and other fixed hyperparameters remain unchanged.
- RQ1 comparison remains paired against the same `RF42_LITE` A0, but **results of the modified grouped OOF stacking cannot be treated as the identical configuration to the older stratified-only pilot or frozen P9 Stacking**.
- Grouping exact vectors does not address correlated sessions, hosts or chronology without trustworthy metadata. Also, 5 random FIT subsamples share the same outer internal validation; infer descriptive seed-level stability only.
- This is a **safety-motivated prospective amendment within P21**, not an original-study preregistration; do not hide it or compare it as a wholly independent new test.
- If the group folds are infeasible, stop and publish the blocker. Do not silently fall back to ungrouped `StratifiedKFold` after seeing metrics.

## Full-run execution policy

Five fixed replication seeds: `1103, 2207, 3301, 4409, 5501`. Each requires a separate exact author-initiated supervised invocation and a new immutable result directory. All five predeclared arms run in fixed order; metrics are computed only on P21's internal held-out fold. **No official TEST use**.

Full science has **NO wall-time timeout**; a separate watchdog enforces process-tree RSS cap 2 GiB, host RAM floor 1.5 GiB, startup RAM >=4 GiB, available disk >=10 GiB, single logical CPU, and heartbeats. Failed attempts remain evidence but do not count as completed seed. The top-level immutable config still reads `training_authorized=false` because historical P21 was design-stage; per-invocation authorization is via exact `--authorize` token, without changing canonical frozen source or any past result.

## Publication gates

Only five successfully completed, independently metadata-verified seed reports permit an aggregated RQ1/RQ2/RQ5 table. Absent 5/5, mark partial and do not present full RQ conclusions. Final PDF V3 may cite this new TRAIN-derived internal-validation extension but must separate it from P9 official TEST and disclose this protocol amendment. Retain original V2, original numerical P9 anchors and bibliography provenance.
