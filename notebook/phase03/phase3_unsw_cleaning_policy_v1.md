# PHASE 3 — UNSW-NB15 Data Cleaning & Leakage Policy v1.0

## Scope
Binary NIDS task: Normal (0) vs Attack (1).

## Evidence from audit

- Train: 175,341 rows.
- Test: 82,332 rows.
- 45 total columns.
- No missing values detected.
- No +/- infinity detected.
- No exact full-row duplicates when `id` is included.
- Feature-vector duplicates are common when comparing the 42 modeling features.
- 1,302 unique feature vectors occur in both predefined train and test.
- These overlaps involve 10,279 train rows and 8,541 test rows (10.374% of test).
- 279 cross-split overlapping vectors have different binary label sets.
- Within train, 229 duplicate-vector groups contain both binary labels.
- Within test, 6 duplicate-vector groups contain both binary labels.

## Interpretation

Identical observed feature vectors do not always map to the same target label.
Therefore duplicated vectors cannot be treated automatically as erroneous duplicate records.
They may represent repeated traffic, feature collisions, coarse/aggregated flow
representations, or labeling inconsistencies.

The project will not silently relabel or blindly remove these records.

## Primary benchmark track — Official Split

Preserve the official UNSW-NB15 training and testing rows.

Model input:
- DROP from X: `id`
- DROP from binary X: `attack_cat`
- TARGET y: `label`

Keep `attack_cat` separately as metadata for class-specific error analysis.

Do not:
- merge train + test and randomly resplit for the primary benchmark
- fit encoders/scalers/feature selection/resampling on test
- remove duplicate vectors simply because they are duplicated
- resolve contradictory labels by majority vote

Categorical inputs:
- `proto`
- `service`
- `state`

Encoding must be fitted on training data only and must tolerate categories unseen in train.

## Leakage/repetition sensitivity track — Novel-Vector Test

Create a second evaluation view:

`test_unseen_vectors`

Definition:
Remove from the official test evaluation view every test row whose 42-feature vector
already occurs in the official training set.

Current audit indicates:
- official test rows: 82,332
- overlapping test rows: 8,541
- novel-vector test rows expected: 73,791

The model is still trained on the original official training set.

Compare:
1. Official test performance
2. Novel-vector test performance

Interpretation:
If performance drops substantially on the novel-vector test, repeated feature patterns
between train and test contributed materially to the official benchmark score.

This is a sensitivity analysis, not a replacement for the official benchmark.

## Duplicate-removal ablation — Deferred

Do not deduplicate training data yet.

Later, if time permits, an ablation can compare:
- original training distribution
- exact-labeled deduplicated training
- possibly group-aware alternatives

This must be reported as an experimental factor because deduplication changes the
empirical traffic distribution.

## Cleaning actions currently approved

| Action | Decision |
|---|---|
| Modify files in `data/raw` | NEVER |
| Missing-value imputation | NOT NEEDED from current audit |
| Infinity cleanup | NOT NEEDED from current audit |
| Remove `id` from model X | YES |
| Use `label` as target | YES |
| Use `attack_cat` as binary input | NO |
| Retain `attack_cat` for error analysis | YES |
| Blind `drop_duplicates()` | NO |
| Relabel contradictory vectors | NO |
| Fit preprocessing on full dataset | NO |
| Encode categorical features | YES, fit on train only |
| Scale numeric features | MODEL-DEPENDENT, fit on train only |
| SMOTE/resampling now | NO |
| Feature selection now | NO — Phase 5 |

## Scientific rationale

The primary track preserves comparability with the published/predefined benchmark.
The novel-vector track explicitly measures sensitivity to repeated feature patterns
without rewriting the original dataset or pretending all duplicates are invalid.

This two-track design supports the project's research question about trustworthy
ensemble evaluation while preserving reproducibility.
