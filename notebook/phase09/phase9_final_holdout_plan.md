# PHASE 9 — Final Holdout Evaluation Protocol

## Objective

Evaluate only the Phase-8 frozen pipelines on the untouched official UNSW-NB15 test split.

This is the first phase in the study allowed to load the official test set.

## Frozen candidates

1. `random_forest_42`
2. `stacking_42`
3. `random_forest_17`

All hyperparameters and decision thresholds are read from:

`results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`

The script rejects any manifest containing missing or extra candidates.

## Rules

After the test is opened:

- no hyperparameter tuning,
- no feature reselection,
- no threshold tuning,
- no adding/removing models because of test results.

Threshold is fixed at 0.5.

## Training

Each frozen pipeline is fit once using the entire official training split.

## Evaluation views

### Official test
All 82,332 official test samples.

### Novel-vector test
Test samples whose complete 42-feature vector did not occur in the official training split.

The previously generated interim novel-vector view is used when available. If it is missing,
the membership mask is reconstructed from the feature vectors only.

## Metrics

Predictive:
- Accuracy
- Balanced Accuracy
- Precision
- Detection Rate / Recall
- F1
- Macro-F1
- MCC
- ROC-AUC
- PR-AUC
- FPR
- FNR
- confusion-matrix counts

Cost:
- full-training time
- official-test inference time
- inference milliseconds/sample
- serialized model size

Error analysis:
- per-attack-category false negatives / miss rate
- paired error counts for every frozen model pair

The prediction table is retained so later statistical tests can use paired sample-level outputs.

## Outputs

`results/final_evaluation/unsw_nb15/phase9_holdout/`

- `phase9_summary.txt`
- `experiment_metadata.json`
- `tables/final_metrics.csv`
- `tables/cost_metrics.csv`
- `tables/attack_category_miss_profile.csv`
- `tables/pairwise_error_counts.csv`
- `tables/official_test_predictions.csv`

## Completion criterion

Phase 9 is complete when all three frozen pipelines have been fitted on full TRAIN and
evaluated on both views without any post-test model changes.
