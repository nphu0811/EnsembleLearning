# PHASE 7.2 — Voting / Stacking Development Protocol

## Objective

Test whether the complementary errors found in Phase 7.1 translate into a real
performance benefit when the models are combined.

## Configurations

### References
- Random Forest: bagging reference and strongest development baseline so far.
- AdaBoost: boosting reference.

### Heterogeneous ensembles
- Hard Voting: Logistic Regression + Decision Tree + Random Forest.
- Soft Voting: Logistic Regression + Decision Tree + Random Forest.
- Stacking:
  - base learners: Logistic Regression, Decision Tree, Random Forest
  - meta learner: Logistic Regression

## Feature tracks

- All 42 model features: performance-oriented.
- 17 stable features: efficiency-oriented.

## Leakage-safe nested structure

The outer 3-fold Stratified CV estimates development performance.

For Voting:
- base models fit only on the outer-training fold,
- outer-validation is used only for evaluation.

For Stacking:
- inside each outer-training fold, an inner 3-fold CV generates out-of-fold
  base predictions,
- the meta learner is fitted on those inner OOF predictions,
- base learners are refit on the whole outer-training fold,
- only then is the outer-validation fold predicted.

Thus the outer-validation fold never trains the meta learner.

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

Cost:
- training time
- inference time per sample
- serialized model size

## Fair comparison rule

All configurations use exactly the same outer folds within both feature tracks.

A dedicated `comparison_vs_random_forest.csv` reports metric and cost deltas relative
to the Random Forest reference; this does not declare a winner.

## Interpretation

This is development evidence only. The official UNSW-NB15 test split remains locked.

After this phase, freeze only a small number of pipelines before final holdout testing.
