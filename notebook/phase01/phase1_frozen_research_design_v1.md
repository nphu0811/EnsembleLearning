# Phase 1 — Frozen Research Design v1.0

## Research problem

The project will not ask merely which classifier achieves the highest benchmark accuracy. It will investigate whether ensemble learning provides a **credible, reproducible and practically useful** advantage over individual ML learners for network intrusion detection when feature selection, class imbalance, data leakage risk, minority-attack performance and computational cost are controlled.

## Frozen primary RQs

### RQ1 — Ensemble effectiveness
Under the same leakage-aware experimental protocol, does ensemble learning provide a stable improvement over matched individual machine-learning models in NIDS?

### RQ2 — Feature selection trade-off
How do feature-selection strategies affect predictive performance, minority-class detection and computational cost of individual and ensemble models?

### RQ3 — Error complementarity
To what extent is ensemble improvement associated with complementary error patterns among base learners, rather than simply combining the individually strongest models?

### RQ4 — Evaluation robustness
How sensitive are model rankings and reported performance to the data-splitting protocol (e.g. conventional stratified random split versus a defensible temporal/day/scenario-aware split when supported by the selected dataset)?

## Secondary RQ

### RQ5 — Class imbalance
How do selected imbalance-handling strategies affect minority-class recall, Macro-F1, false negatives and ensemble behavior when applied only within training folds?

RQ5 is secondary to avoid excessive project scope.

## Candidate contribution (not a novelty claim yet)

1. A leakage-aware and reproducible comparison protocol for NIDS ensembles.
2. Feature selection treated as an experimental factor with performance–cost analysis.
3. Base learner selection supported by error-complementarity analysis rather than only individual accuracy.
4. Minority-class and false-alarm analysis in addition to aggregate metrics.
5. Statistical and ablation evidence explaining where any ensemble gain comes from.

## Claims explicitly not made

- The project does not claim to invent Ensemble Learning.
- It does not claim that stacking/voting is novel.
- It does not claim that feature selection + ensemble is novel.
- It does not claim the final ensemble will outperform all baselines.
- It does not claim CIC-IDS2017 or any other dataset is already selected.
