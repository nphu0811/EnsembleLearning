# PHASE 4 — EDA Plan

## Scientific questions

1. Is the binary task strongly imbalanced?
2. Which attack categories are rare enough to make aggregate accuracy misleading?
3. Which numeric features show the strongest descriptive Normal-vs-Attack separation?
4. Which numeric features are strongly correlated and therefore candidates for later redundancy analysis?
5. Do categorical inputs contain train/test category mismatch that preprocessing must tolerate?

## Figures kept

- Fig 01 — Binary class distribution: establishes binary imbalance context.
- Fig 02 — Attack-category distribution on log scale: exposes minority attack classes.
- Fig 03 — TRAIN-only standardized Normal–Attack separation: identifies descriptive signals without claiming feature selection.
- Fig 04 — TRAIN-only Spearman correlation heatmap for target-associated numeric features: visualizes redundancy structure.

## What is deliberately not done

- No dozens of per-feature histograms.
- No test-driven feature ranking.
- No feature deletion.
- No SMOTE/resampling.
- No model fitting.
- No claim that a high-correlation feature pair must be removed.
- No publication-level figure QA yet; that is reserved for Phase 16.
