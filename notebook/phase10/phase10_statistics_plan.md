# PHASE 10 — Statistical + Final Error Analysis

## Objective

Analyze only the frozen Phase-9 predictions. No model is trained, tuned, or altered.

## Inputs

`results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`

`results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`

## Analyses

### 1. Point metrics

Recompute binary confusion-count metrics for:
- official test,
- novel-vector test.

Metrics include:
- Macro-F1,
- MCC,
- FPR,
- FNR,
- Accuracy,
- Balanced Accuracy,
- Precision,
- Detection Rate / Recall.

### 2. Bootstrap confidence intervals

Use 10,000 stratified paired bootstrap replicates with a fixed seed.

The bootstrap is implemented efficiently through the joint prediction-pattern
distribution of the three frozen models, separately within Normal and Attack strata.

For each pipeline and evaluation view, estimate 95% percentile CIs for:
- Macro-F1,
- MCC,
- FPR,
- FNR.

These intervals quantify uncertainty conditional on the benchmark rows. They do not
establish independence of individual network flows.

### 3. Paired bootstrap differences

For each model pair, estimate:
- delta Macro-F1,
- delta MCC,
- delta FPR,
- delta FNR,

where delta is always `model_a - model_b`.

The output includes the 95% percentile interval and whether the interval excludes zero.
This is used primarily as effect-size uncertainty, not as a separate multiple-testing
hypothesis-testing framework.

### 4. Exact McNemar tests

Perform exact two-sided McNemar tests for the three frozen model pairs on paired
correctness.

McNemar answers whether two classifiers have different overall paired error rates. It
does NOT test Macro-F1 or MCC.

Within each evaluation view, the three McNemar p-values receive Holm family-wise error
correction at alpha = 0.05.

### 5. Per-attack miss-rate uncertainty

For each attack family and frozen pipeline:
- attack sample count,
- false negatives,
- miss rate,
- Wilson 95% interval.

This is especially important for rare categories, where raw percentages can be unstable.

### 6. Novel-vector degradation

Report descriptive changes from official test to novel-vector test for:
- Macro-F1,
- MCC,
- FPR,
- FNR.

Because the novel-vector set is a subset of the official test, these are descriptive
sensitivity comparisons rather than independent-sample tests.

### 7. Performance-cost trade-off

Merge official-test predictive metrics with Phase-9:
- training time,
- inference time,
- inference ms/sample,
- serialized model size.

## Outputs

`results/final_analysis/unsw_nb15/phase10_statistics/`

- `phase10_summary.txt`
- `experiment_metadata.json`
- `tables/recomputed_point_metrics.csv`
- `tables/bootstrap_metric_ci.csv`
- `tables/paired_bootstrap_differences.csv`
- `tables/mcnemar_holm.csv`
- `tables/attack_family_miss_rate_ci.csv`
- `tables/official_vs_novel_degradation.csv`
- `tables/performance_cost_tradeoff.csv`

## Post-test rule

Phase 10 findings are analysis only. No model, feature set, threshold, or hyperparameter
may be changed because of these results.
