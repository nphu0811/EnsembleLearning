# PHASE 11 — Final Results & Figures

## Objective

Convert the locked Phase-9/10 evidence into publication-ready result tables, figures,
captions, and a Results-ready synthesis.

No model is trained or modified in this phase.

## Inputs

Phase-10 statistical tables only.

## Figure QA principles

- One figure = one main message.
- No figure is used to claim model superiority when the paired uncertainty does not
  support that claim.
- Confidence intervals are shown where uncertainty is central to interpretation.
- Computational cost is shown separately from predictive performance.
- Attack-family plots avoid visually emphasizing very rare categories; all categories
  remain available in the companion table.

## Figures

1. Official-test Macro-F1 with 95% bootstrap CI.
2. Official-test MCC with 95% bootstrap CI.
3. FPR/FNR trade-off.
4. Macro-F1 versus training time.
5. Official-test versus novel-vector Macro-F1.
6. Attack-family miss rates with Wilson 95% CI for families with n >= 300.

Each figure is saved as:
- PNG at 300 dpi,
- PDF vector.

## Result tables

1. Final performance with uncertainty.
2. Pairwise effect sizes + McNemar/Holm.
3. Performance-cost trade-off.
4. Attack-family miss rates + Wilson intervals.

## Completion criteria

Phase 11 is complete when:
- all six figures render,
- all four tables are exported,
- captions are written,
- Results-ready prose is generated,
- no post-test model changes occur.
