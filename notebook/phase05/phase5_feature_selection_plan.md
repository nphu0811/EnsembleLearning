# PHASE 5.1 — Feature Selection Plan

## Why this stage exists

Running RFECV blindly on all one-hot-expanded UNSW-NB15 features is expensive and can
make the study harder to reproduce. Stage 5.1 first creates a defensible candidate space
using three different views of feature relevance.

## Methods

### Filter
Mutual Information measures statistical dependence between each original feature and the
binary target. Numeric redundancy is then reduced with a Spearman threshold of |rho| >= 0.95.

### Embedded — L1 Logistic Regression
A linear sparse model is fitted after train-only scaling and one-hot encoding. Absolute
coefficients are aggregated back to the original feature level.

### Embedded — Extra Trees
A non-linear tree ensemble estimates importance after train-only one-hot encoding.
Importances of one-hot levels are aggregated back to the original feature level.

### Consensus
A feature receives one vote when it appears in the Top-20 of a method.
Features selected by at least 2/3 methods form the main consensus candidate set.

## Important limitation

Stage 5.1 does NOT prove that selected features improve predictive performance.
The same training data generates the rankings; therefore performance claims must wait for
later CV/validation where selection/evaluation are separated properly.

## Wrapper method

RFECV is intentionally moved to Phase 5.2. It will operate on a reduced candidate space
and a fixed train-only sample/fold design to keep runtime feasible and reproducible.

## Outputs

- Method-specific rankings
- Consensus ranking
- Candidate feature subsets
- Reproducibility metadata

No official test data is used.
