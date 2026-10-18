# NotebookLM follow-up: V4 issue-by-issue disposition (2026-10-19)

Source: the user-supplied NotebookLM text headed "BÁO CÁO PHẢN BIỆN NGHIÊN CỨU KHOA HỌC", giving 7.2/10, MAJOR REVISION, seven categorized comments. This is an **automated review**, not an actual committee's adjudication. Its printed page numbers refer to the previous report; LaTeX labels below are stable and page locations may move in V4.

| Review item | V4 disposition | Manuscript evidence | Scope / remaining limits |
|---|---|---|---|
| Critical 1: 5 seed SD treated as generalization | **Addressed as an interpretation and labelling risk** | In table `tab:p21-five-arm-results`, Macro-F1/MCC mean vs FIT SD displayed on separate lines; bold adjacent notice says all 5 use *same* 35,069-row validation and forbids inferential t-test/ANOVA as 5 independent tests. `tab:p21-by-seed` and methodology explicitly say "có điều kiện". | Conditional SD is a legitimate descriptive measurement; no independent external sample gained. No re-scoring official TEST. |
| Critical 2: FS cost inconsistency | **Addressed with distinct measured cost scenarios** | Historical `tab:chi-phi` footnote identifies fit-only time 57.255 vs 371.244s, unmatched hyperparams and missing selector effort. P21 `tab:p21-cost` gives matched RF17 84.600s, RF42 241.119s, fresh selector 225.250s, combined 309.850s (+28.5% relative to RF42 model fit). RQ2 conclusions correctly distinguish fit after feature choice vs fresh feature-search+fit. | No matched P21 inference latency / production cost measurement; avoid review's unsupported claim "only inference savings." |
| Major 1: historical FS leakage before development CV | **Warning added, history not rewritten** | Note directly under `tab:rev-dev` says historical stable17 global feature selection was done before development CV, and `tab:p21-five-arm-results` is subsequent FIT-only matched analysis. | The displayed development OOF table is a **42-feature track**, not RF17 OOF, so reviewer conflation corrected. Original P9 selection bias cannot be removed retrospectively. |
| Major 2: cost of FP vs FN | **Sensitivity model added; not a real-world cost estimate** | Discussion subsection `sec:v4-fp-fn-cost` and `tab:v4-cost-sensitivity`; loss L=FP+r FN; `Stack minus RF=-142+118r`; threshold 142/118≈1.2034; table r∈{1,5,10,50,100}. | "RF better" only among these two historical candidates at same threshold on official TEST; not any deployment scenario's universal optimum. Cost ratios are illustrative, not measured. |
| Major 3: novel-vector is a misleading name | **Terminology made precise throughout V4** | `exact-duplicate-filtered view`, explicitly defined as exact overlap of all 42 original predictor values, not duplication of source record, time, host, IP or session. | 73,791-row view still part of official TEST; does not address temporal/session dependence. Historical metric values unchanged. |
| Minor 1: Attack family table unreadable | **Split and enlarged** | `tab:attack-family`: 9 families × 3 models FN/FNR; `tab:attack-family-wilson`: all original Wilson CI limits; both A4 portrait, `\small` text and wide name columns. | Verify actual rendered pages visually before print; note re-numbering of downstream tables is automatic. |
| Minor 2: historical hardware unknown | **Transparent footnote** | Under `tab:chi-phi`, acknowledge historical original CPU/RAM/parallelism and original software environment not fully logged; no invented CPU model or execution mode. | Not recovered by editorial changes. |

## Numerical invariants

- Historic official TEST RF42 vs Stacking42: 10003 vs 9861 FP, 734 vs 852 FN; reviewed loss differences are arithmetically deterministic from these frozen values.
- P21 remains 5/5 matched FIT seeds × 5 arms on shared 35069-row TRAIN-derived internal validation, checksum-verified by the original completed experiments; new PDF build never loads TRAIN or TEST. No retraining was carried out as part of these fixes.
- Original 9 family FN/FNR/Wilson 95% endpoints transcribed without modifications when splitting a dense layout into two tables.
- V3 and all earlier frozen outputs remain intact; V4 sources and outputs are separate paths.

## What an honest new NotebookLM review can still flag

1. Re-used internal validation and post-hoc hypothesis status: disclosed, but not cured by additional editorial text.
2. Historical FS-before-CV procedure: disclosed; only P21 fit-only path is safer.
3. Session/time-independent evidence and production drift data: not available.
4. Observational class-specific misclassification costs and new decision thresholds: hypothetical sensitivity, not an actual SOC study.
5. Original precise historical CPU/RAM setup: cannot be invented.
6. Proof of novelty and source rights: requires further external bibliographic and submission checks.

**Release gate:** Refer to `docs/research/REPORT_REVISION_V4_QA_2026-10-19.md` and separately rendered `docs/research/v4_visual_samples_2026_10_19/QA.md` for their observed status; do not treat this checklist as PDF build confirmation.
