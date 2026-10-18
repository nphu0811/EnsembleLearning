# P21 full five-seed result acceptance — 2026-10-19

Status: 5/5 author-host seed runs PASS; 25/25 five-arm confusion-matrix reports independently reconciled in read-only review. See source author commit https://github.com/nphu0811/EnsembleLearning/commit/6806542 and the canonical five-seed aggregate in results/controlled_extensions/p21_train_only_science_summary_20261019_022655/aggregate.json.

This is post-hoc reused-official-TRAIN internal validation, not official TEST or independent external confirmation. The five 60k-row FIT source samples differ by seed, but share one fixed grouped internal validation of 35069 rows (11200 Normal and 23869 Attack). Never infer five independent benchmark tests, claim preregistration of historical study, or recalculate historical P9 TEST results.

## Matched summary: five FIT seeds (mean)

| Arm | Macro-F1 | MCC | FPR | FNR | Model fit seconds |
|---|---:|---:|---:|---:|---:|
| A0 RF42-Lite | 0.945220 | 0.890971 | 9.6196% | 2.3989% | 241.119 |
| A1 RF17-Lite | 0.936751 | 0.874032 | 10.7589% | 2.9327% | 84.600 |
| A2 RF42 Balanced | 0.943877 | 0.887909 | 6.4554% | 4.1870% | 230.247 |
| A3 RF42 Oversample | 0.944886 | 0.889776 | 7.4107% | 3.5670% | 355.197 |
| A4 Stacking-Lite | 0.944731 | 0.889864 | 9.4071% | 2.5715% | 652.913 |

Contrast means vs A0 (arm minus baseline):
- RQ1 Stacking: Macro-F1 -0.000488, MCC -0.001107, FPR -0.2125 percentage points, FNR +0.1726 percentage points.
- RQ2 matched RF17: Macro-F1 -0.008468, MCC -0.016939, FPR +1.1393 points, FNR +0.5337 points.
- RQ5 class weighting: Macro-F1 -0.001343, FPR -3.1643 points, FNR +1.7881 points.
- RQ5 FIT-only minority oversampling: Macro-F1 -0.000334, FPR -2.2089 points, FNR +1.1680 points.

Important cost correction: selector mean fit 225.250 seconds, RF17 model-only fit 84.600 seconds, total 309.850 seconds; RF42 model-only 241.119 seconds. RF17 is faster after selection but the measured selector plus fit is around 28.5% slower than RF42 fit. Selected original 17 features vary by seed; 14 occur in all five feature subsets.

## Read-only evidence QA performed in this session

For each seed 1103, 2207, 3301, 4409, 5501:
- Run report PASS, exit 0, no stop reason, process RSS under 2 GiB, no full wall-time deadline.
- Original official TRAIN SHA, frozen protocol hash and worker/supervisor source identity consistent.
- Exact five predeclared arms and one FIT ID digest per seed.
- Outer fixed group-disjoint split, 60000 FIT source rows per seed, 35069 validation rows.
- All 25 confusion matrices sum to class support (11200 Normal, 23869 Attack).
- All reported Macro-F1/MCC/FPR/FNR recalculated from confusion counts within 1e-10.
- Per-seed Macro-F1 reproduces published aggregate. Meta-OFF flag official_test_opened=false is source-reported, not independent OS attestation.

One field split.validation_evaluation_performed=false describes pre-fit SPLIT QA. P21 scientific arms DID score TRAIN-derived internal validation; avoid conflating this with official TEST never accessed in P21.

## Manuscript follow-through

Added versioned V3 five-chapter source, methodology, RQ results, tradeoffs, and conclusion. PDF V2 and frozen P9/P15 are unchanged. A dedicated V3 XeLaTeX/BibTeX workflow includes a read-only five-seed evidence gate. Source inputs, brace nesting and environments passed structural checks. An actual PDF build, rendering and layout audit still must be confirmed before marking V3 as delivered.

The original NotebookLM criticism transcript with precise 10 comments/page anchors is unavailable in GitHub; the edits address the documented themes only, not unverifiable literal comments.
