# Research canon phục hồi ngày 16/10/2026

Tên đề tài: NGHIÊN CỨU ENSEMBLE LEARNING CHO BÀI TOÁN PHÁT HIỆN XÂM NHẬP MẠNG.

Nguồn RQ bất biến: `notebook/phase01/phase1_frozen_research_design_v1.md`. Không viết lại RQ dựa trên TEST.

- RQ1: Ensemble có cải thiện ổn định so với individual models trong protocol tương ứng không?
- RQ2: Feature selection ảnh hưởng thế nào đến performance, minority detection và chi phí?
- RQ3: Complementarity của lỗi liên quan thế nào tới ensemble gain?
- RQ4: Ranking/performance nhạy thế nào với split protocol, temporal/day/scenario khi dữ liệu hỗ trợ? **Chỉ trả lời một phần** bằng official/novel view, không temporal/external validation.
- RQ5 phụ: Imbalance handling ảnh hưởng recall/Macro-F1/FN thế nào? Chưa có matched resampling comparison; không kết luận sampling vô ích.

Không tìm thấy bộ giả thuyết thống kê tiên nghiệm tách biệt đã xác minh. Không tạo giả thuyết sau test rồi gọi là preregistered.

Scope đã thực hiện là binary Normal=0, Attack=1 trên UNSW-NB15 standard TRAIN 175341 và TEST 82332. 42 predictors sau khi bỏ id/label/attack_cat; track stable 17. Attack-family FN là phân tích của binary detector, không multiclass prediction. CIC là candidate chưa có validation hợp lệ.

Freeze: `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`; final RF-42, Stacking-42, RF-17, thresholds 0.5. Freeze bằng metadata P9 qua kiểm tra P15-04 ngày 16/10. Không retune, reselect, thêm candidate hoặc đổi threshold bằng TEST.

Evidence hiện hành: `docs/RESUME_AUDIT.md`, `docs/research/ENSEMBLE_FRAMEWORK.md`, `docs/CLAIM_EVIDENCE_MATRIX.md`.

Kết luận được hỗ trợ: Stacking-42 không chứng minh ưu thế tổng thể so với RF-42; Δ Macro-F1=0.000496689894, 95% paired CI [-0.000311804213, 0.001308950325], Holm McNemar p=0.468376519. FPR giảm, FNR tăng; 142 FP ít hơn và 118 FN nhiều hơn. Không suy ra statistical equivalence. RF-17 là pipeline performance–cost trade-off, không isolated causal feature ablation.

Giới hạn bắt buộc: FS full TRAIN trước development CV; meta selection không fully nested; overlap/split dependence; bootstrap có điều kiện trên benchmark rows; no external validation; no live deployment; original training environment UNKNOWN; no serialized model local. Không claim fully leakage-free hoặc end-to-end reproducible từ static hashes/import smoke.

Contribution là kiểm toán benchmark và trade-off có evidence; novelty chưa được chứng minh. Danh tính, GVHD, ngày/chữ ký, ngân sách áp dụng dùng [CẦN XÁC NHẬN].
