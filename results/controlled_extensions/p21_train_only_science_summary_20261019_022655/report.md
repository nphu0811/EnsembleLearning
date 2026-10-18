# P21 — Descriptive TRAIN-derived 5-seed internal-validation results

> POST-HOC reused official TRAIN (not official TEST). All 5 seeds share
> one grouped internal-validation partition. Not independent experiments
> or a prospective test of superiority. No p-values or external claims.

## Per-arm summaries (mean ± sample SD across five FIT replications)

| Arm | Macro-F1 | MCC | FPR | FNR | Mean fit time (s) |
|---|---:|---:|---:|---:|---:|
| A0_RF42_NONE | 0.945220 ± 0.000399 | 0.890971 ± 0.000858 | 0.096196 ± 0.002027 | 0.023989 ± 0.001305 | 241.119 |
| A1_RF17_NONE | 0.936751 ± 0.001291 | 0.874032 ± 0.002462 | 0.107589 ± 0.004369 | 0.029327 ± 0.000758 | 84.600 |
| A2_RF42_BALANCED | 0.943877 ± 0.000275 | 0.887909 ± 0.000563 | 0.064554 ± 0.002145 | 0.041870 ± 0.001021 | 230.247 |
| A3_RF42_OVERSAMPLE | 0.944886 ± 0.000742 | 0.889776 ± 0.001480 | 0.074107 ± 0.001735 | 0.035670 ± 0.001098 | 355.197 |
| A4_STACK42_NONE | 0.944731 ± 0.000340 | 0.889864 ± 0.000738 | 0.094071 ± 0.001530 | 0.025715 ± 0.001103 | 652.913 |

## Paired contrasts (first arm minus baseline)

| Contrast | Δ Macro-F1 | Δ FNR | Δ FPR | Δ MCC |
|---|---:|---:|---:|---:|
| RQ1_STACK42_MINUS_RF42 | -0.000488 ± 0.000437 | 0.001726 ± 0.000282 | -0.002125 ± 0.000956 | -0.001107 ± 0.000861 |
| RQ2_RF17_MINUS_RF42 | -0.008468 ± 0.001594 | 0.005337 ± 0.001320 | 0.011393 ± 0.003330 | -0.016939 ± 0.003163 |
| RQ5_BALANCED_MINUS_NONE | -0.001343 ± 0.000438 | 0.017881 ± 0.000670 | -0.031643 ± 0.001315 | -0.003062 ± 0.000967 |
| RQ5_OVERSAMPLE_MINUS_NONE | -0.000334 ± 0.000730 | 0.011680 ± 0.000694 | -0.022089 ± 0.001063 | -0.001195 ± 0.001485 |

## Mandatory interpretation

- RQ1: comparison of lighter **group-safe** Stacking-Lite vs RF42-Lite.
- RQ2: RF17 FIT-selected vs matched RF42, all RF parameters identical.
- RQ5: weighting and oversampling are distinct interventions; note Normal
  was the FIT minority, so no presumption that Attack recall improves.
- Five seeds vary FIT subsamples and estimator seeds but use ONE shared
  TRAIN-derived internal validation; no new independent external sample.
- Selected17 features were re-learned per FIT seed (never reused from P9).
- New group-safe inner CV is a disclosed P21 pre-full amendment.
- Do not rewrite the historical official TEST P9/P15 results.
