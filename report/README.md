# P17 — Báo cáo khoa học theo phong cách biểu mẫu PTIT (WORKING / 40 TRANG)

Folder này là **một chỗ duy nhất cho mã nguồn báo cáo IDS mới**, tách khỏi `templates/original/` và bản thảo/bằng chứng lịch sử ở `notebook/`. Không di chuyển hoặc xóa các thư mục hiện có khi chưa có quyết định cleanup từ người dùng.

## Artifact hiện có

- `main.tex`: báo cáo XeLaTeX làm việc có bìa placeholder, tóm tắt, mục lục, 8 chương và bibliography.
- `frontmatter.tex`: Lời cam đoan (chưa ký), lời cảm ơn có placeholder, tóm tắt, bảng viết tắt.
- `chapters/theoretical_foundations.tex`: cơ sở lý thuyết IDS, LR, DT, RF, Voting/Stacking, OOF, FS và metrics.
- `chapters/dataset_eda.tex`: hai tập UNSW-NB15, phân bố lớp, 4 hình EDA gốc, correlation/overlap.
- `chapters/validity_discussion.tex`: paired correctness, error trade-off, giới hạn nested validation và reproducibility.
- `chapters/introduction.tex`: bối cảnh, RQ gốc, động cơ và phạm vi đóng góp.
- `chapters/related_work.tex`: công trình liên quan với claim bị giới hạn theo mức đọc thực tế.
- `chapters/methodology.tex`: UNSW-NB15, protocol, three frozen pipelines, OOF, uncertainty và limitations.
- `chapters/results_discussion.tex`: official/novel results, paired CI, costs, Fuzzers/Generic, RQ1–RQ5; tham chiếu trực tiếp đến hai hình P16 dạng PDF trong `../results/figures/`, đã được render trong PDF P17; layout QA scoped tại `P17_PDF_QA_2026-10-16.md`.
- `chapters/conclusion.tex`: kết luận không khẳng định superiority/novelty, hướng nghiên cứu còn thiếu.
- `references_verified.bib`: 11 legacy entries có verified metadata; L03 còn xung đột số trang.
- `references_dataset_checked.bib`: trích riêng U01 (Moustafa & Slay 2015) từ `literature/verification_2026_10_16/dataset_references.bib`, trang 1–6 đã được đối chiếu từ IEEE/University of Adelaide/DBLP.
- `BUILD.md`: hướng dẫn build, và `P17_SOURCE_QA_2026-10-16.md`: scoped check history (trước cập nhật trích dẫn và hình). Bản QA đọc lại sau cập nhật: 78/78 source checks PASS, chưa PDF-render QA.
- `P17_PDF_QA_2026-10-16.md`: XeLaTeX+BibTeX CI, 22 A4 pages, 12 bibliography entries, 2 figures, 5 results tables, 0 overfull / 0 missing glyph after layout fix; **scoped layout QA PASS**, institutional approval pending.

Đây là **bản nguồn học thuật 40 trang có QA PDF**, lấy tham khảo về hình thức từ báo cáo NetFlow 64 trang do người dùng cung cấp và từ asset/template gốc của dự án. **Chưa được trường/GVHD phê duyệt tính phù hợp biểu mẫu.** Xem `BUILD.md`.

## Provenance bắt buộc

| Nội dung | Nguồn dữ liệu lịch sử bất biến |
|---|---|
| Hiệu năng + official/novel view | `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv` |
| Thời gian + kích thước | `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv` |
| CI paired effects | `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv` |
| McNemar Holm | `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv` |
| Tên/cấu hình mô hình | `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json` |
| Attack-family FN | `docs/research/PHASE14_ERROR_ANALYSIS_CLOSURE.md` + các CSV Phase14 |
| Novel-vector counts | `results/data_audit/unsw_nb15_views/view_summary.json` |
| Phạm vi RQ1–RQ5 | `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md` |
| Hình và bảng được audit | `docs/research/P16_R05_INDEPENDENT_AUDIT_2026-10-16.md`, `docs/research/P16_FOREST_INDEPENDENT_AUDIT_2026-10-16.md` |

## Gate chưa hoàn tất

- Tám chương, tóm tắt và bibliography đã ghép vào bản nguồn làm việc; vẫn cần peer/source review, final citation verification và QA bản PDF render.
- XeLaTeX/BibTeX và PDF QA scoped đã PASS qua GitHub Actions; chưa nhận nghiệm thu/đối chiếu mẫu trường, chưa xác nhận thông tin hành chính.
- P18 chưa đóng nguồn tham khảo L03/U01/U03; không bịa citation hoàn chỉnh.
- Thông tin người thực hiện/GVHD/ngày/chữ ký vẫn cần xác nhận; không được điền theo ví dụ mẫu.
- P17 toàn bộ **IN PROGRESS**, không phải DONE. Dataset/model/test configuration và toàn bộ kết quả frozen giữ nguyên.

## Tính khoa học

Stacking42 không chứng minh ưu thế toàn diện; RF17 có khác biệt hyperparameters; novel-vector vẫn thuộc official TEST; error analysis không causal; môi trường train gốc UNKNOWN; không dùng test để sửa model. File này là báo cáo lại số liệu lịch sử, **không sinh experiment mới**.

## PTIT-style adaptation / length QA (2026-10-16)

- See `P17_PTIT_40PAGE_QA_2026-10-16.md`: reviewed source and actual XeLaTeX/BibTeX PDF (40 physical A4 pages), 7 figures, 10 tables, 12 bibliography entries; 0 overfull, 0 missing glyphs and 0 text blocks outside page bounds.
- Cover double border, PTIT logo sourced from `templates/original/latex/assets/Logo_PTIT_University.png`; carmine and cobalt accents align with original PTIT template. Do not copy sample group's names/ID/content.
- `report/main.tex` is the sole current working entry point. The sample NetFlow PDF is not committed or redistributed.
- CI enforces the requested range of 30–40 pages for future changes. Signed declaration and real student/adviser data still PENDING_HUMAN.
