# PHASE 5.2 — Stability + Wrapper Plan

## Why Stage 1 is not enough

Stage 1 produced a useful consensus, but it used one fixed sample and one random seed.
A feature ranking that changes dramatically when the sample changes is not a strong
research result.

Therefore Stage 5.2 asks two questions:

1. **Stability:** do the same features keep appearing when we repeat the selectors?
2. **Wrapper evidence:** does a model-driven recursive elimination procedure retain a
   similar subset when judged by cross-validated Macro-F1?

## Stability protocol

- Official training split only.
- Seeds: 11, 23, 42, 71, 101.
- 60,000 stratified training rows per run.
- Repeat:
  - Mutual Information + redundancy pruning
  - L1 Logistic Regression
  - Extra Trees
- Each method selects Top-20.
- Feature is stable for a method if it appears in >= 3/5 runs.
- Pairwise Jaccard similarity summarizes how reproducible each selector is.

## Wrapper protocol

- Input space: Stage-1 consensus features only.
- Sample: 50,000 stratified training rows.
- Preprocessing:
  - numeric -> StandardScaler
  - categorical -> OneHotEncoder(handle_unknown='ignore')
- Estimator: Logistic Regression (L2).
- RFECV:
  - 3-fold Stratified CV
  - scoring = Macro-F1
  - step = 10% of remaining transformed features
  - test set is never loaded

## Important interpretation

RFECV is estimator-dependent. Its output is evidence from one wrapper perspective, not an
oracle. One-hot dummy levels are mapped back to the original feature names.

## Decision after Phase 5.2

Do NOT pick the final feature set solely from rankings. Phase 6 must compare:

- All 42 original features
- Stage-1 consensus
- Stable consensus
- RFECV subset
- Stable + RFECV intersection

using the same baseline models and validation protocol.

The final selection is based on predictive performance AND computational cost.
