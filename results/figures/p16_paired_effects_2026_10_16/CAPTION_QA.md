# Hình P16 đầu tiên và QA

**Chênh lệch chỉ số giữa Stacking-42 và RF-42 trên official UNSW-NB15 TEST.** Điểm biểu diễn Stacking-42 trừ RF-42, thanh ngang là CI 95% paired bootstrap đã lưu với 10.000 resamples trên 82.332 dòng benchmark. Tất cả delta và CI được nhân 100; với FPR/FNR đơn vị là điểm phần trăm, với Macro-F1/MCC là điểm trên thang nhân 100. Đây không phải relative percent improvement. Threshold hai mô hình bằng 0.5. Không train/predict hay bootstrap lại để tạo hình. CI Macro-F1/MCC chứa 0; giảm FPR đi cùng tăng FNR. Các intervals có điều kiện trên benchmark rows, không chứng minh network flows độc lập. Source data được cung cấp trong `source_data.csv` cùng thư mục; nguồn đầy đủ và SHA-256 tại `metadata.json`.

## QA ngày 16/10/2026

| Check | Kết quả |
|---|---|
| Input | SHA-256 khớp frozen input P13; chọn 4/24 rows theo contrast định trước; 20 rows còn lại giữ ở source |
| Source validation | 19 PASS, 0 FAIL, 2 WARN đã xem xét |
| WARN TIFF | PDF/SVG là vector authoritative; PNG 600 dpi dùng preview; không có yêu cầu nộp TIFF cho đề tài này |
| WARN width | Static validator hiểu nhầm biểu thức 183/25.4 là 183 inch. Geometry thực đo là 518.740157 pt = 183 mm; không phải lỗi kích thước |
| Text audit | 25 text runs, min 8 pt, không glyph dưới 5 pt |
| Collision audit | PASS, 0 FAIL, 0 WARN |
| Alignment | NOT APPLICABLE: một plot area; không ghi là multi-panel PASS |
| Visual review | Đã mở PNG thực tế; tiêu đề, nhãn, tick, error bars và footnote rõ, không clipping/overlap |
| Scientific scope | Một frozen contrast, không xác lập superiority, independent flow sampling hoặc causal mechanism |

Trạng thái: **FIGURE_READY_FOR_REVIEW** trong phạm vi contract. Toàn bộ P16 vẫn IN_PROGRESS vì các hình/bảng khác chưa qua publication QA. Plot source: `src/analysis/plot_p16_paired_effects.py`.
