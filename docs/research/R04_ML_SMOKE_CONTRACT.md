# R04 — isolated TRAIN-only smoke contract

Purpose: kiểm tra source builders, preprocessing, fit, serialization và reload trong môi trường sạch trên một mẫu nhỏ chỉ lấy từ official TRAIN. Đây là software smoke, không tái lập số liệu final, không model selection hoặc benchmark mới. Không truy cập official TEST/novel TEST.

Inputs: source `src/models/run_unsw_phase9_final_holdout.py` chỉ import functions (không gọi main); frozen manifest và17feature list giữ nguyên; raw TRAIN đã được preservation audit xác nhận. Không sửa source lịch sử hoặc hyperparameters. Random sampling/split chỉ phục vụ smoke, không protocol nghiên cứu mới.

Resources kiểm thực tế r04:8 logical CPUs;RAM12.554.305.536 bytes;C:free31.273.279.488 bytes tại preflight. Dữ liệu smoke gồm2.000 training rows và500 validation rows, disjoint theo index trong official TRAIN. Ba frozen model builders giữ seed/hyperparameters; budget hữu hạn là một smoke batch, không CV/tuning search. Không chạy main lịch sử vì có output cố định và đọc TEST. Giới hạn BLAS threads2; source RF n_jobs giữ nguyên.

Môi trường: tạo venv mới không system-site-packages, install6 direct versions đang quan sát ởPython3.11 qua publicPyPI. Ghi rõ đây không phải original training environment. Nếu pin unavailable, lưu pip failure và chuyển task; không đổi dependency rồi nhận là original. Thực hiện pip check/freeze và versions. Requirements chưa hash-lock cho tới khi có wheel manifest đủ; không gọi reproducibility bitwise.

Outputs riêng: results/reproducibility/r04_ml_smoke/ gồm run metadata, model smoke artifacts, schema, validation vàinput hashes; venv riêng results/reproducibility/r04_ml_smoke_runtime/. Output dir không được tồn tại trước run. Model chỉ là SMOKE_ONLY_TRAIN_SUBSET, không đưa vào demo sản phẩm hoặc đặt model_artifact_available=true cho final model.

Acceptance: no TEST read; manifest/feature count guards; both binary classes; parameter/source hashes; probability shape/range/sums; reload prediction agreement; negative CSV schema cases; pip check; exit/code logs thật. Không tính/chọn theo Accuracy hoặc final TEST metric. Không dùng smoke để đóng repeatedtraining, FS optimism, full reconstruction hoặcG0–G6. Chỉ sau fullTRAIN reconstruction vàevaluation policy được kiểm mới có model/demo final hợp lệ.
