# Framework thực nghiệm đã thực hiện

Purpose: đóng gap tài liệu canonical P08 bằng mô tả nguồn đã khóa. Không bổ sung thí nghiệm hay đổi cấu hình.

Inputs: `notebook/phase01/phase1_frozen_research_design_v1.md`, `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`, source `src/models/`, P15-04 protocol. Output: design note này dùng cho Methods, proposal và defense. Gate: source hashes/freeze phải khớp; mọi lời mô tả không vượt evidence.

## Chuỗi xử lý

Official TRAIN 175.341 dòng → bỏ `id`, `label`, `attack_cat` khỏi predictors → hai feature tracks (42 features và stable 17) → development baselines/diversity/ensemble → controlled tuning trên TRAIN → freeze ba candidate và threshold 0.5 → fit TRAIN và final evaluation trên official TEST 82.332 dòng. Novel-vector subset 73.791 dòng là sensitivity view thuộc cùng TEST. Không phải tập kiểm thử độc lập mới.

Preprocessing nằm trong sklearn Pipeline. Stacking dùng Logistic Regression, Decision Tree và Random Forest tạo xác suất OOF cho meta Logistic Regression; `passthrough=False`, inner CV 3 folds. Source đặt seed 42, inner stacking seed 137. P15-04 lưu các dòng nguồn và checksum để kiểm tra mô tả này.

| Final candidate | Cấu hình khóa | Vai trò |
|---|---|---|
| RF-42 | 300 trees, max_features=0.5, min_samples_leaf=1 | Reference strong individual learner |
| Stacking-42 | LR C=1.0 liblinear; DT min_samples_leaf=2; RF như RF-42; meta LR C=0.5, class_weight=None, liblinear | Kiểm tra kết hợp heterogeneous learners |
| RF-17 | 150 trees, max_features=0.5, min_samples_leaf=2 | Pipeline giảm feature với trade-off chi phí/hiệu năng |

Sự khác biệt linear/tree/bagged-tree là lý do thiết kế để khảo sát complementarity, không tự chứng minh diversity hoặc superiority. Evidence định lượng phải lấy từ `results/ensemble/unsw_nb15/phase7_1_diversity/` và ensemble OOF; không suy kết luận từ tên thuật toán. Voting kém không được loại khỏi tổng hợp.

## Ranh giới suy luận

- Preprocessing trong pipeline không giải quyết selection optimism do stable features được chọn trên full TRAIN trước outer CV.
- Meta tuning dùng base OOF từ TRAIN; không gọi là fully nested unbiased selection.
- RF-17 và RF-42 khác cả số cây/min leaf; final comparison là pipeline trade-off, không phải causal feature-count ablation.
- Không matched SMOTE/no-SMOTE, không component leave-one-out, không multiclass prediction hoặc deployment evidence.
- Đóng góp phù hợp là benchmark có kiểm toán và phân tích trade-off; không tuyên bố phát minh thuật toán hoặc ưu thế tổng thể của stacking.

Source/freeze check trong `results/reproducibility/resume_2026_10_16/protocol/` đạt PASS với các giới hạn trên. P08 documentation closure không đóng toàn bộ scientific/release gates.
