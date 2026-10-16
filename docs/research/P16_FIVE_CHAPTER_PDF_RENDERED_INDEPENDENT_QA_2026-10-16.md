# P16 — Independent rendered PDF / frozen figures QA (2026-10-16)

**Disposition: DONE_SCOPED (report/figure verification only). Canonical P16: IN_PROGRESS.**

## Version and evidence boundary

- Examined **user-supplied** file: `Bao_cao_NCKH_EnsembleLearning_5_chuong_09-SV-2026-CNTT2.pdf` (37 pages).
- Local PDF SHA-256: `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`.
- Document metadata: PDF 1.7, LaTeX/hyperref producer `xdvipdfmx (20260317)`. Inspected using PyMuPDF and rendered selected pages with the PDF skill's raster-render workflow at **115 dpi**; contact sheet was visually reviewed.
- The supplied PDF was read-only and **was not modified**. This audit does **not** claim a new GitHub Actions build, full-document manual copyedit, complete print certification, or access to the user's physical printer.

## Rendered pages and layout

Selected physical PDF pages reviewed: **19–22, 27–30, 33–34**, covering class/attack distributions, feature separation and heatmap, official results, FP/FN differences, bootstrap forest plot, historical cost and research-question evidence table.

1. All **37** physical pages are A4 (595.28 × 841.89 pt).
2. No nonempty text spans extend beyond media-box boundaries across the 37 pages (tolerance 1 pt), and text extraction contains no Unicode U+FFFD replacement characters. This is a bounding check, **not** an overlap-proof or a glyph-renderer parity test.
3. Physical page **28** contains Hình 4.1 and Bảng 4.2, physical page **29** contains Hình 4.2 and Bảng 4.3; page 27 contains the three-model final performance table. Captions and chart axes are visible in the rendered preview, with no obvious clipped objects on inspected pages.
4. **Print-readability warnings:** Hình 2.2 on physical page 20 contains axis/legend labels of approximately **6.45 pt** (plus 4.51-pt mathematical superscripts). Hình 4.2 on physical page 29 has axis/footnote labels near **6.52 pt** and metric labels approximately **7.34 pt**. Hình 2.4 on page 22 has labels near **7.62 pt**. These are below the P16 standalone-figure guideline of 8 pt; enlarging them would require a separate approved figure/layout revision. The report was deliberately left unchanged.
5. Hình 2.4 includes **two embedded raster images** (468 × 459 pixels heatmap and 23 × 459 pixels colorbar) each placed at approximately **118 dpi** effective resolution on the PDF page. Suitable for casual on-screen preview; **300-dpi print fidelity is not established** for this heatmap. Do not describe all chart content as fully vector or print-ready.
6. Physical page 29 has appreciable whitespace between the forest plot/caption and the cost table. Not a clipping failure, and no layout change was undertaken.

## Numeric QA — independent check against frozen CSV

Inputs fetched read-only from the project GitHub `main` branch:

- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`
- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`
- `results/figures/p16_paired_effects_2026_10_16/source_data.csv`
- `results/figures/p16_r05_error_tradeoff/source_data.csv`
- `results/tables/p16_r05_frozen_summary/official_performance.csv`
- `results/tables/p16_r05_frozen_summary/stack_minus_rf42.csv`

**49/49 independent numerical/source assertions PASS, 0 FAIL:** three official and three novel-vector candidates; frozen threshold 0.5; counts sum to official n=82,332 and class denominators Normal=37,000 / Attack=45,332; FPR/FNR, Macro-F1 and MCC recomputed from TP/TN/FP/FN for each official candidate to 1e-12 tolerance; Stacking minus RF-42 exact FP=-142, FN=+118; four bootstrap deltas match the saved aggregate differences, point estimates lie within interval bounds, CI exclusion flags and 10,000 bootstrap replicates match saved source; forest plot source and companion table tokens match corresponding original CSV rows. This is **not** a new bootstrap or a new model evaluation.

| Pipeline | Macro-F1 | MCC | FP | FN |
|---|---:|---:|---:|---:|
| RF-42 | 0.863343 | 0.750910 | 10,003 | 734 |
| Stacking-42 | 0.863840 | 0.750497 | 9,861 | 852 |
| RF-17 | 0.860673 | 0.746881 | 10,224 | 708 |

Stacking-42 minus RF-42 has Macro-F1 `+0.000496689894` with 95% paired bootstrap CI `[-0.000311804213, +0.001308950325]`, MCC `-0.000413036259` with CI `[-0.001937876021, +0.001139570406]`. **Both intervals include 0**. The FPR CI is wholly negative, the FNR CI wholly positive: an FP/FN trade-off, not proof of better overall IDS performance. RF-17 differs from RF-42 in feature count **and** RF hyperparameters; no isolated feature-selection causal claim.

## Release impact and next action

**PASS within scope:** Source-to-PDF cross-check, sampled render/placement review, A4/page-boundary audit, frozen result integrity. No old results, bibliography or 5-chapter PDF were edited.

**OPEN (P16 / print scope):** chart labels under 8 pt, heatmap effective ~118 dpi, no 300-dpi print proof, and no complete final PDF glyph/print review across a second renderer. These warnings **do not automatically invalidate the frozen research results**. They should be recorded rather than erased by treating a build-success status as full visual QA.

**Next unblocked action:** assess whether to produce a new **standalone high-resolution P16 heatmap/figure asset** from TRAIN-only evidence, with no changes to the completed PDF unless the author asks; or continue P18 bibliography checks. P15/G3 remain PARTIAL/NO_GO on author-reported ~2.01-GiB free RAM, lacking a reviewed watchdog runner.

**Independence disclosure:** Numerical assertions were executed against the repo CSV payloads inside a separate JavaScript review session; PDF checks were executed locally against the user-uploaded PDF with PyMuPDF. This is **not** a fresh Windows fit, not a nature-figure skill execution in the user's installed Codex environment and not a third-party peer review.
