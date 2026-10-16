# P17 — Báo cáo LaTeX đang biên soạn (WORKING, KHÔNG PHẢI BẢN NỘP)

Folder này là **một chỗ duy nhất cho mã nguồn báo cáo IDS mới**, tách khỏi `templates/original/` và bản thảo/bằng chứng lịch sử ở `notebook/`. Không di chuyển hoặc xóa các thư mục hiện có khi chưa có quyết định cleanup từ người dùng.

## Artifact hiện có

- `chapters/results_discussion.tex`: chương kết quả/thảo luận tiếng Việt với bảng official holdout, paired-bootstrap CI, chi phí, attack families, novel-vector view và các giới hạn RQ1–RQ5.

File hiện là **fragment LaTeX dùng lệnh `\\chapter`**, cần được `\\input` từ report `main.tex` trong bản làm việc theo template trước khi biên dịch. Không tự nhận đã build được PDF.

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

- Nội dung các chương khác, abstract và bibliography cần ghép từ canon và nguồn đã kiểm chứng; không copy nguyên văn mẫu Android.
- Chưa có LaTeX `main.tex` working theo template; chưa compile/render hoặc chạy PDF text/visual QA.
- P18 chưa đóng nguồn tham khảo L03/U01/U03; không bịa citation hoàn chỉnh.
- Thông tin người thực hiện/GVHD/ngày/chữ ký vẫn cần xác nhận; không được điền theo ví dụ mẫu.
- P17 toàn bộ **IN PROGRESS**, không phải DONE. Dataset/model/test configuration và toàn bộ kết quả frozen giữ nguyên.

## Tính khoa học

Stacking42 không chứng minh ưu thế toàn diện; RF17 có khác biệt hyperparameters; novel-vector vẫn thuộc official TEST; error analysis không causal; môi trường train gốc UNKNOWN; không dùng test để sửa model. File này là báo cáo lại số liệu lịch sử, **không sinh experiment mới**.
