# P16-R05 — Kiểm toán độc lập bảng và hình (2026-10-16)

**Repository:** `nphu0811/EnsembleLearning`  
**Source commit kiểm tra:** `13cafe08cfb013bd4e765829f3ebf4add6bcd167`  
**Task:** `P16-R05-INDEPENDENT-TABLE-SVG-PREVIEW-QA`  
**Disposition:** **DONE_SCOPED** cho kiểm tra số liệu, SVG cấu trúc và PNG preview. **P16 tổng thể: IN_PROGRESS.**

## Phạm vi / phương pháp

Đọc các file thực qua GitHub connector từ commit nêu trên. Kiểm tra độc lập bằng JavaScript trong phiên ChatGPT, không chạy code project, không đọc raw/test CSV, không train/predict, không bootstrap, không thay đổi các artifact khoa học gốc.

**Historical input sources (read-only):**

1. `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`
2. `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`
3. `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`

**Checked r05 outputs:**

- `results/tables/p16_r05_frozen_summary/official_performance.csv`
- `results/tables/p16_r05_frozen_summary/historical_cost.csv`
- `results/tables/p16_r05_frozen_summary/stack_minus_rf42.csv`
- `results/tables/p16_r05_frozen_summary/TABLES_AND_CAPTIONS.md`
- `results/tables/p16_r05_frozen_summary/official_performance.tex` (source read, **NOT COMPILED**)
- `results/figures/p16_r05_error_tradeoff/source_data.csv`
- `results/figures/p16_r05_error_tradeoff/error_tradeoff.svg`
- `results/figures/p16_r05_error_tradeoff/error_tradeoff.png` (GitHub file bytes decoded and visually inspected)
- `results/figures/p16_r05_error_tradeoff/CAPTION.md`
- `tools/r05_plot_error_tradeoff.py`, figure contract and source-preflight JSON

## QA kết quả

**Table/source cross-check: 141/141 independent assertions PASS, 0 mismatches.** Các assertion kiểm đúng ba pipeline official, so khớp token CSV của toàn bộ trường, số TN/FP/FN/TP và mẫu từng lớp, tính lại Macro-F1/MCC/FPR/FNR từ confusion counts (tolerance `1e-11`), đồng nhất chi phí, 4 paired effect rows và 95% CI, hiệu `FP=-142` và `FN=+118`. Độc lập với `validation.json` sẵn có (repo tự ghi 25/25 PASS). Không tái chạy experiment.

**SVG source/static: 14/14 assertions PASS, 0 mismatches.** SVG có đúng một panel, khung `340.15748 × 184.251969 pt` (= **120 × 65 mm**, sai khác làm tròn dưới 0.02 mm), chữ SVG editable ở các `<text>`, không nhúng `<image>`, tất cả các text anchor nằm trong viewBox. Các label False positives, False negatives, `-142`, `+118`, hướng `Stacking-42 minus RF-42` hiện diện; nguồn generator cấu hình sans-serif 9 pt, `svg.fonttype='none'`, `pdf.fonttype=42`, và khai báo cả PDF/SVG export. Đây là **static structural QA**, không phải test mọi font renderer.

**PNG preview:** Đã mở trực quan ảnh PNG lấy từ commit: trục zero, hai thanh âm/dương, các nhãn FP/FN và chữ số thể hiện đúng; không thấy overlap/clipping ở kích thước preview. Chưa chứng nhận độ dễ đọc trong bản in báo cáo cuối cùng.

**Cảnh báo preflight:** `source_preflight_repaired.json` có WARN `FINAL-WIDTH=3048.0 mm` (heuristic parser). SVG xuất thực tế ghi 120 × 65 mm, khớp contract và `manifest.json`; vì vậy WARN nguồn không phải bằng chứng hình đang rộng 3048 mm. Cần lưu warning, không che hoặc đánh dấu công cụ preflight hoàn toàn PASS.

## Số liệu khoa học được đối chiếu

| Final candidate (official holdout n=82,332; threshold=0.5) | Macro-F1 | MCC | FP | FN |
|---|---:|---:|---:|---:|
| RF-42 | 0.863343 | 0.750910 | 10,003 | 734 |
| Stacking-42 | 0.863840 | 0.750497 | 9,861 | 852 |
| RF-17 | 0.860673 | 0.746881 | 10,224 | 708 |

Stacking−RF42: **FP−142, FN+118**. Bootstrap Macro-F1 Δ `+0.000496689894` với 95% CI `[-0.000311804213, +0.001308950325]`, MCC Δ `-0.000413036259` với 95% CI `[-0.001937876021, +0.001139570406]`. Cả hai CI chứa 0. **Không kết luận superiority hoặc statistical equivalence.** Các rate-CI mang tính conditional theo benchmark rows, không lặp huấn luyện.

Historical train cost và size là số liệu lần chạy gốc, không phải benchmark hiệu năng phần cứng hiện tại. Source dùng `bytes / 1024**2`, vì vậy trường legacy có chữ `mb` được chú thích là **MiB**. RF17/RF42 khác cả hyperparameters: trade-off ở mức pipeline, không phải causal isolated feature ablation.

## Scope exclusions / bước tiếp theo

- **PDF binary/glyph/fonts, PDF rendered output, TIFF print readability, SVG browser/editor rendering, LaTeX compilation/layout và đưa figure vào manuscript:** **NOT VERIFIED IN THIS AUDIT**. Không gọi một PNG preview là QA đủ cho PDF/print.
- **P16 full phase:** **IN_PROGRESS**; cần QA các hình còn lại, caption/source maps, cuối cùng report layout.
- **P15:** PARTIAL; original training env UNKNOWN; R04 TRAIN-only smoke không phải final fullTRAIN model. Plan fullTRAIN trong r05 hiện NO_GO do RAM/runner.
- **P17/P18/P19/P20 và G0-G6:** chưa hoàn tất; kế thừa giới hạn FS trước CV, meta tuning chưa fully nested, overlap và thiếu external validation.
- Không dùng kết quả này để thay frozen score hoặc retune official TEST.

## Task Board checkpoint

| ID | Status | Evidence | Next |
|---|---|---|---|
| P16-R05-INDEPENDENT-TABLE-SVG-PREVIEW-QA | **DONE_SCOPED** | 141/141 independent source assertions; 14/14 SVG checks; inspected PNG; document này | PDF/print QA và report integration |
| P16-RENDERED-DOCUMENT-QA | **TODO** | No independent PDF-glyph or LaTeX render evidence | Khi có compiler/runtime và source report |
| Canonical P16 | **IN_PROGRESS** | Một số bảng và figures có QA scoped | Chưa đóng phase |

**Integrity:** Thêm **file báo cáo mới**; không chỉnh source/model/test/predictions/dataset/freeze hoặc các chứng cứ lịch sử. Các trạng thái ở checkpoint r05 của Codex được kế thừa, không được âm thầm nâng thành DONE.
