# Contract hình P16 paired effects

Purpose: một forest plot trả lời RQ1 về trade-off của Stacking-42 so với RF-42 trên official TEST. Core conclusion: FPR giảm và FNR tăng; CI Macro-F1/MCC chứa 0 nên chưa có bằng chứng ưu thế tổng thể.

Evidence: `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv` (24 rows). Chọn đúng 4 rows official_test, model_a=stacking_42, model_b=random_forest_42 cho Macro-F1, MCC, FPR, FNR. 20 rows còn lại là so sánh model/view khác, không bị xóa khỏi source và không được dùng để chọn winner. Không tính bootstrap mới.

Archetype: quantitative single-panel forest plot. Bốn metric là cùng một so sánh; không tạo 4 subplot lặp nội dung. Backend Python/matplotlib theo project source. Kích thước 183 x 100 mm, font >=8 pt, PDF/SVG text editable, PNG 600 dpi. Cấu trúc một panel nên alignment NOT_APPLICABLE; phải lưu manifest và chạy PDF glyph/collision audits.

Center là delta đã lưu, intervals là paired 95% bootstrap CI, 10.000 replicates có điều kiện trên benchmark rows. n=82.332 official rows, không phải 82.332 network sessions độc lập hay 10.000 lần huấn luyện. Cùng hai frozen models, threshold 0.5; không thêm p-value stars. Delta tất cả nhân 100 để hiển thị, FPR/FNR là điểm phần trăm; Macro-F1/MCC là điểm trên thang nhân 100, không relative percent improvement.

Outputs: `results/figures/p16_paired_effects_2026_10_16/paired_effects.{pdf,svg,png}`, `source_data.csv`, source metadata, alignment/text/collision/source QA, caption. Validation: source SHA đúng input P13; đúng 4 rows/metric order; CI lower<=delta<=upper; exported dimensions/font/text/collisions; nhìn thực tế PNG/PDF. Không đánh toàn bộ P16 DONE chỉ từ một figure.
