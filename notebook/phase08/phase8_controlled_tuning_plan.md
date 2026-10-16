# PHASE 8 — Controlled Tuning Protocol

## Objective

Tune only a small number of predeclared candidates before final holdout testing.

The official UNSW-NB15 test split remains locked.

## Candidates

1. Random Forest — all 42 model features.
2. Stacking — all 42 model features.
3. Random Forest — 17 stable features.

Stacking uses:
- Logistic Regression base learner
- Decision Tree base learner
- tuned Random Forest base learner
- Logistic Regression meta learner

## Random Forest tuning

Same compact grid for both 42-feature and 17-feature tracks:

- n_estimators: 150, 300
- min_samples_leaf: 1, 2, 4
- max_features: sqrt, 0.5

Total: 12 candidates per feature track.

Selection:
- 3-fold Stratified CV
- primary refit metric: Macro-F1
- secondary metrics retained: MCC, balanced accuracy, attack recall

## Stacking meta tuning

After RF-42 is tuned, TRAIN-only 3-fold OOF attack probabilities are generated for:

- Logistic Regression
- Decision Tree
- tuned Random Forest

The Logistic Regression meta learner is then tuned on these OOF features.

Grid:

- C: 0.1, 0.5, 1.0, 2.0, 10.0
- class_weight: None, balanced

Primary selection metric: Macro-F1.

This is model-selection evidence only, not an unbiased final performance estimate.

## Threshold diagnostic

A probability-threshold sweep from 0.30 to 0.70 is generated for the tuned meta learner.

This is diagnostic only.

No threshold is automatically selected, and the freeze candidates remain at threshold 0.5
until an explicit scientific decision is made.

## Freeze candidates

The script writes exactly:

- random_forest_42
- stacking_42
- random_forest_17

No candidate may be added after inspecting the official test.

## Outputs

results/tuning/unsw_nb15/phase8_controlled/

- phase8_summary.txt
- experiment_metadata.json
- freeze_candidates.json
- tables/rf42_grid_results.csv
- tables/rf17_grid_results.csv
- tables/stacking42_base_oof_probabilities.csv
- tables/stacking42_meta_grid_results.csv
- tables/stacking42_threshold_sensitivity.csv

## Completion criterion

Phase 8 is complete when:
- both RF grids finish,
- meta tuning finishes,
- threshold diagnostics are saved,
- freeze candidates are written,
- official TEST has not been loaded.
