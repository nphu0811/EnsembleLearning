# PHASE 6 — Baseline Development Protocol

## What Stage 5.2 established

Feature selection is reasonably stable:
- Filter mean pairwise Jaccard ≈ 0.889
- L1 mean pairwise Jaccard ≈ 0.862
- Extra Trees mean pairwise Jaccard ≈ 0.829

Seven original features were stable across all three selection families:
`ct_srv_dst`, `ct_state_ttl`, `dload`, `dttl`, `proto`, `state`, `sttl`.

RFECV reduced the Stage-1 20-feature candidate space to 13 original features and achieved
development Macro-F1 ≈ 0.922 on its internal wrapper CV. This is wrapper-specific evidence,
not final performance.

## Phase-6 objective

Feature rankings are not enough. We now test whether reduced subsets actually preserve
predictive quality across different baseline model families while reducing cost.

## Baseline models

1. Logistic Regression — linear baseline.
2. Decision Tree — simple nonlinear baseline.
3. Random Forest — strong conventional bagging reference.

Random Forest is technically an ensemble, but it serves here as a standard strong benchmark.
The proposed heterogeneous ensemble comparison begins in Phase 7.

## Candidate subsets

- All 42 original model features
- Stable >=2 selector families: 17
- RFECV-selected: 13
- Stable ∩ RFECV: 12
- Stable across all 3 selector families: 7

## Evaluation

Three-fold Stratified CV on the official training split only.

Within every fold:
- fit OneHotEncoder on fold-train only
- fit StandardScaler for Logistic Regression on fold-train only
- train model
- evaluate on fold-validation

Metrics:
- Accuracy
- Balanced Accuracy
- Precision
- Recall / Detection Rate
- F1
- Macro-F1
- MCC
- ROC-AUC
- PR-AUC
- FPR / FNR
- Training time
- Inference time
- Serialized pipeline size

## Important limitation

The candidate feature sets were themselves discovered from the official training split.
Therefore the Phase-6 CV values are development/model-selection evidence and may be
optimistic. The untouched official test remains the final external holdout and must not be
used until feature set + model family + hyperparameters are frozen.
