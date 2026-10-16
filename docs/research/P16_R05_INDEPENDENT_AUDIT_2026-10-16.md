# P16 r05 — independent read-only QA (GitHub handoff)

**Date:** 2026-10-16 (UTC date); **reviewed commit:** `13cafe08cfb013bd4e765829f3ebf4add6bcd167` (branch `main` at review).  
**Scope:** P16 r05 official-performance, historical-cost, paired-effect **source tables** and FP/FN **PNG visual preview**.  
**Disposition:** **PASS_SCOPED_NUMERIC_AND_PREVIEW; P16 REMAINS IN PROGRESS.**

## Evidence and verification method

All inputs were **read directly from the GitHub repository at the reviewed commit** using the GitHub file API. A separate in-session JavaScript check parsed the CSVs and evaluated **141 assertions**, with **0 mismatches**. This was independent of the r05 generator's own `validation.json` result (which reports 25/25). It did **not** execute project Python code, read raw UNSW data, refit models, re-evaluate saved predictions, rerun bootstrap, or change any frozen artifact.

Historical inputs:
- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`
- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`

New P16 outputs crosschecked:
- `results/tables/p16_r05_frozen_summary/official_performance.csv`
- `results/tables/p16_r05_frozen_summary/historical_cost.csv`
- `results/tables/p16_r05_frozen_summary/stack_minus_rf42.csv`
- `results/tables/p16_r05_frozen_summary/official_performance.tex`
- `results/tables/p16_r05_frozen_summary/TABLES_AND_CAPTIONS.md`
- `results/figures/p16_r05_error_tradeoff/source_data.csv`
- `results/figures/p16_r05_error_tradeoff/CAPTION.md`
- `results/figures/p16_r05_error_tradeoff/error_tradeoff.png`

The independent checks included: unique candidate mapping; exact preservation of all displayed CSV tokens; confusion totals and class supports; FPR/FNR from confusion counts; Macro-F1 and MCC recomputed from confusion counts; per-model cost row equality; all four paired-effect rows and CI fields; whether CI spans zero; signed FP/FN plot deltas and correct class denominators. Numeric tolerance for derived rates/metrics: `1e-11`; source table tokens were compared exactly as strings.

## Observations

| Model, official TEST (n=82,332) | Macro-F1 | MCC | FP | FN |
|---|---:|---:|---:|---:|
| RF-42 | 0.863343 | 0.750910 | 10,003 | 734 |
| Stacking-42 | 0.863840 | 0.750497 | 9,861 | 852 |
| RF-17 | 0.860673 | 0.746881 | 10,224 | 708 |

`Stacking-42 minus RF-42`: **FP = −142**, **FN = +118**. These are observed counts on the same fixed official holdout, not means across training runs. For paired bootstrap, `ΔMacro-F1 = +0.000496689894` and 95% CI `[-0.000311804213, 0.001308950325]`; `ΔMCC = −0.000413036259` and CI `[-0.001937876021, 0.001139570406]`. Both intervals include zero; there is no demonstrated overall superiority, nor a statistical equivalence result. The `FPR` rate effect is negative; the `FNR` rate effect is positive, as reported in the stored paired table.

**PNG visual preview:** `error_tradeoff.png` was opened as an image from the GitHub file and inspected at the preview scale. It clearly shows a zero reference line, a negative false-positive bar labeled `−142`, a positive false-negative bar labeled `+118`, and an x-axis identifying the direction `Stacking-42 minus RF-42`. No apparent clipping or label collision was observed in the preview. This is **not** a PDF glyph/font audit, print-scale QA, full visual accessibility review, or LaTeX integration/render verification.

**LaTeX source:** `official_performance.tex` contains a syntactically plausible `tabular` with the expected seven columns and three model rows; it explicitly says `NOT COMPILED OR VISUALLY VERIFIED`. No TeX compilation was performed here. Keep that limitation.

## Risks and next gates

1. **P16 still PARTIAL.** Other figures, source/caption mapping, final journal/report layout, print-size readability and rendered LaTeX/PDF inspection remain to be completed.
2. All scientific claims continue to inherit original-study limitations: selected features from full official TRAIN before development CV, non-fully-nested meta selection, train/test feature-vector overlap, lack of external/temporal validation, original training environment UNKNOWN.
3. RF-17 differs from RF-42 in estimator hyperparameters as well as feature count; runtime/predictive comparison is a *pipeline-level trade-off*, not isolated causal feature-count ablation.
4. Timing and model size are historical estimates reported by the original run; the last field name `serialized_model_size_mb` uses byte/(1024²), i.e. MiB in the new caption. There is no extant reconstructed full model verified by this check.
5. No review of `error_tradeoff.pdf` text embedding or SVG import/export was performed. The PNG image inspection does not establish journal-ready figure acceptance.
6. This audit checks **internal cross-file consistency**, not external dataset authenticity, independent training reproducibility or absence of leakage.

## Research Task Board entry (proposed; do not overwrite history)

| ID | Task | Status | Evidence |
|---|---|---|---|
| P16-R05-TABLE-QA-INDEPENDENT | Independent source/cross-metric audit of r05 tables | **DONE_SCOPED** | This file: 141/141 assertions, 0 mismatches, reviewed commit above |
| P16-R05-FIGURE-PREVIEW | PNG preview and numeric labels | **DONE_SCOPED_PREVIEW** | This file: visual preview + `source_data.csv` agreement |
| P16-FINAL-VISUAL | PDF/SVG glyph/readability + rendered manuscript QA | **TODO** | NOT_EXECUTED |
| P16 full phase | Figures & tables complete | **PARTIAL** | No full visual/manuscript acceptance yet |

**Handoff:** Preserve all frozen source CSVs and generated r05 files. Next bounded step: perform the unverified PDF/SVG/rendered-source checks (or work on an independently unblocked P17 manuscript section), create separate evidence and run actual checks before upgrading P16 status. Do not rerun RF/Stacking or use official TEST for new tuning.

**Repository safety:** This read-only audit generated one new documentation artifact on a review branch, with no changes to `main`, original data, source training code, model configs, results or canonical roadmap.
