# P15-04 — Split, Seeds & Leakage Safeguards (read-only)

Status: **STATIC_PROTOCOL_EVIDENCE_MATCH_WITH_CAVEATS**

This is static source/metadata verification, not an executed training replay.

## Checks

| Check | Status | Evidence |
|---|---|---|
| `feature_subset_17` | PASS | stable_2plus_methods count=17 |
| `phase8_official_test_not_loaded` | PASS | Phase 8 metadata official_test_loaded=False |
| `phase9_official_test_evaluated` | PASS | Phase 9 metadata official_test_opened=True |
| `official_split_sizes` | PASS | train=175341; test=82332 |
| `three_frozen_models` | PASS | models=['random_forest_17', 'random_forest_42', 'stacking_42'] |
| `manifest_unchanged_in_phase9` | PASS | Phase 8 freeze_candidates JSON compared with Phase 9 experiment_metadata frozen_candidates |
| `frozen_thresholds_0_5` | PASS | All three final-model thresholds must equal 0.5 |
| `dataset_label` | PASS | Both saved metadata records identify UNSW-NB15 |
| `source_matches_historical_audit` | PASS | Seven critical script SHA-256 digests compared with audit snapshot; exact line evidence requires MATCH |

## Audited source evidence (only if all hashes match)

- `src/models/run_unsw_phase9_final_holdout.py:72-73` — RANDOM_STATE=42; STACKING_INNER_RANDOM_STATE=137
- `src/models/run_unsw_phase9_final_holdout.py:222-232` — Drops id, label, attack_cat from model features
- `src/models/run_unsw_phase9_final_holdout.py:270-325,332-403` — Unknown categories ignored; preprocessing occurs inside sklearn Pipeline
- `src/models/run_unsw_phase9_final_holdout.py:466-509` — StratifiedKFold inner CV; StackingClassifier predict_proba; passthrough=False
- `src/models/run_unsw_phase9_final_holdout.py:932-943,991-1073` — Loads official train/test, frozen manifest; fits frozen models only on train
- `src/models/run_unsw_phase8_controlled_tuning.py:462-483,603-610,638-662` — Training-only GridSearchCV, base OOF predictions via cross_val_predict, meta-model tuning
- `src/models/run_unsw_ensemble_phase7_2.py:428-449,675-725,1113-1127` — Outer StratifiedKFold and nested internal StackingClassifier CV
- `src/features/select_unsw_features_stage2.py:793-804,901-913` — Stage2 features selected using full official TRAIN before development CV
- `src/features/select_unsw_features_stage2.py:53-62` — Stability seeds 11,23,42,71,101

## Caveats / research limitations

- Historical original-training Python and package versions UNKNOWN; current reference venv is not proof of original environment.
- Feature selection is done on the entire official TRAIN before development CV; development scores can be optimistic (selection outside CV folds).
- Stratified shuffled CV is not a time/session-group split. Original official train/test may have feature-vector overlap; do not claim independent temporal validation.
- Static source checks plus metadata do NOT prove the original scripts executed exactly as currently stored, or that every data-leakage mode was excluded.
- Meta learner tuning reuses saved base OOF features from the full training set; do not call this a completely nested unbiased CV estimate.

Do not use official TEST to adjust features, threshold or model configuration.
