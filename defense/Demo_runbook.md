# Demo runbook r04

**Final inference demo: BLOCKED dependency.** Chưa có mô hình full TRAIN và bộ tiền xử lý/schema đã được kiểm định. Model r04 có nhãn SMOKE_ONLY, fit trên 2.000 dòng TRAIN để kiểm phần mềm; không dùng làm mô hình sản phẩm hoặc nhận đã tái lập historical metrics.

## Evidence walkthrough có thể chuẩn bị

Gọi đúng là trình bày bằng chứng đã lưu, không phải live inference. Không chạy main của source P9: nó đọc TEST và ghi output lịch sử.

1. Mở `docs/research/ENSEMBLE_FRAMEWORK.md` và freeze để giải thích candidates/ngưỡng.
2. Mở `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`; giải thích lớp dương và FP/FN.
3. Mở `results/figures/p16_paired_effects_2026_10_16/paired_effects.pdf` cùng caption/source-data; không đọc CI chứa 0 thành tương đương.
4. Mở `results/reproducibility/r04_ml_smoke_repaired/validation.json` và `docs/research/R04_ML_SMOKE_REPORT.md`; giải thích 45 kiểm tra phần mềm, không phải performance metrics.

## Điều kiện trước inference thật

Cần full TRAIN reconstruction có hashes dữ liệu/source/config/môi trường, model và fitted transformer, schema xác minh, ngưỡng 0,5, CLI CSV được kiểm end-to-end và các trường hợp lỗi. Chưa có lệnh final inference được xác minh nên không điền command giả. Không nhận packet capture hoặc thời gian thực khi chưa triển khai. Chỉ load artifact tin cậy của project.

Input: đúng predictors; không id/label/attack_cat; không cột trùng, thiếu, thừa, giá trị thiếu, infinity hoặc kiểu sai. Output: giữ thứ tự dòng, ghi định danh dòng, nhãn 0/1, xác suất Attack, ngưỡng và phiên bản model. Chọn ví dụ từ TRAIN hoặc input được tác giả cung cấp; không dùng TEST để chọn ví dụ trình diễn đẹp.

Các lỗi phải thử: thiếu/thừa/trùng header, không phải số, giá trị thiếu/vô hạn, input rỗng; chính sách categorical chưa gặp phải rõ. Không trả nhãn khi schema fail. Smoke r04 đã kiểm các trường hợp này qua wrapper nội bộ; chưa thay CLI sản phẩm.

## Smoke cho developer

Lệnh thực đã chạy ở `docs/research/R04_ML_SMOKE_REPORT.md`. Python 3.11.9 và observed-version requirements là môi trường mới, không original environment hoặc hashed lock. Chỉ rerun khi có thay đổi hay concern; outdir phải mới. Không sửa training config hoặc dữ liệu để che lỗi.

Acceptance cuối: CLI thật chạy valid/invalid; artifact load đạt; số dòng/thứ tự/semantics output đạt; log/hash được lưu; diễn tập offline trên máy dự kiến. Trước đó G6 vẫn NOT_READY. Không có job chạy nền sau phiên.
