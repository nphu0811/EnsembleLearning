# P16 — Independent forest-plot source and visual preview QA

**Date:** 2026-10-16  
**GitHub source snapshot:** `13cafe08cfb013bd4e765829f3ebf4add6bcd167`  
**Task:** P16-FOREST-INDEPENDENT-SOURCE-SVG-PREVIEW-QA  
**Status:** **DONE_SCOPED**; **canonical P16 remains IN_PROGRESS**.

## Goal

Independent check of the already-produced four-metric paired-effect forest plot; preserve all frozen experiment outputs. No rerun of bootstrap, model fit or held-out prediction.

**Original evidence:** `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`.

**Existing figure artifacts:** `results/figures/p16_paired_effects_2026_10_16/` — `source_data.csv`, `paired_effects.svg`, `paired_effects.png`, `paired_effects.pdf`, `metadata.json`, `CAPTION_QA.md`, and historical text/collision reports.

## Checks actually performed in this ChatGPT takeover

All sources were retrieved from GitHub at the cited snapshot. Independent JavaScript assertions: **79/79 PASS, 0 mismatches**.

- Original paired-bootstrap source has 24 rows; figure data selects exactly four official-test `stacking_42−random_forest_42` rows.
- Every field/token in each of those four rows matches the original CSV exactly.
- Each saved estimate lies inside its saved CI and has level 0.95 with 10,000 bootstrap replicates.
- Saved `ci_excludes_zero` is mathematically consistent with lower/upper bounds.
- SVG frame measures `518.740157 × 283.464567 pt` = **183 × 100 mm** within 0.03 mm rounding.
- SVG contains the proper metric labels (Macro-F1, MCC, False positive rate, False negative rate), difference×100 label, benchmark-sampling footer, single axes group, editable text tags and no embedded `<image>`.
- The GitHub PNG was retrieved as an image and visually inspected: no apparent clipping/collisions at preview scale; FPR CI entirely left of zero, FNR CI entirely right of zero, Macro-F1 and MCC intervals span zero. Labels and uncertainty bars were legible.

Expected plot values (all multiplied by 100 for the figure):

| Metric | Center | Lower 95% | Upper 95% |
|---|---:|---:|---:|
| Macro-F1 | +0.049669 | -0.031180 | +0.130895 |
| MCC | -0.041304 | -0.193788 | +0.113957 |
| FPR | -0.383784 | -0.524324 | -0.243243 |
| FNR | +0.260302 | +0.185300 | +0.337510 |

Numbers represent **points on the displayed delta×100 axis**, not relative-percent improvements. FPR/FNR can be described as percentage points. The 95% intervals are from stored paired row bootstrap; they are not repeated independent model trainings.

## Relation to prior Codex QA

Historical artifact `paired_effects.text-audit.json` reports minimum text size 8 pt, 25 runs, zero under 5 pt. Historical `paired_effects.collision-audit.json` reports PASS, zero warnings/failures. `CAPTION_QA.md` says the figure had previously been visually inspected. These are *saved Codex reports*, **not independently rerun PDF glyph/collision tests in this takeover**. The independent audit only verified their saved presence/content and separately inspected the PNG and SVG.

The source preflight historically warned about an incorrectly parsed width from the expression `183/25.4`; actual SVG geometry measures **183 mm**, consistent with the contract.

## Scientific interpretation and boundaries

The plot correctly depicts no statistically demonstrated overall superiority of Stacking-42 over RF-42 in Macro-F1/MCC (CI includes zero). FPR decreases and FNR increases on the frozen official test. This neither establishes statistical equivalence nor a causal operational advantage. Existing protocol limitations persist: feature selection before development CV, non-fully-nested meta tuning, overlapping feature vectors between splits, dependent benchmark rows and no independent temporal/external validation.

**Not yet checked here:** independent PDF font/glyph/collision preflight, PDF rendering, inclusion in a rendered manuscript, accessibility at final printed size, TeX compilation or full P16 coverage. Do not upgrade canonical P16 to DONE based on this note.

## Next safe work

Pair this scoped QA with `docs/research/R05_INDEPENDENT_AUDIT_2026-10-16.md`. Before closing P16, audit remaining figures/tables and actual assembled report page renders. Continue manuscript source work independently if a safe PDF/TeX runtime is not available. No retraining, no tuning, no official-test reopening for selection.
