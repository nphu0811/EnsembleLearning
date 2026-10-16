# ORIGINAL PHASE 9 — CLASS-IMBALANCE CLOSURE NOTE

Ngày: 04/10/2026. Đây là closure note hồi cứu cho original Phase 9; không phải experiment resampling.

## Evidence hiện có

UNSW-NB15 binary label quy ước Normal=0, Attack=1. Trên official TRAIN có 175,341 rows: Attack 119,341 (68.06%); Normal 56,000 (31.94%). Vì Attack không phải lớp minority ở partition này, việc áp dụng SMOTE chỉ theo khẩu hiệu “IDS luôn imbalance” không phù hợp với primary binary split và cần rationale riêng.

Không synthetic oversampling trước/sau split được dùng trong pipeline hiện có. Trong Phase 8, `class_weight=None` và `balanced` được so ở Logistic Regression meta-learner, C=0.5 trên 5-fold CV của global base OOF features. Balanced trừ None: Macro-F1 −0.001804, MCC −0.003708, attack recall −0.014421. Đây chỉ là một contrast meta-model có điều kiện; không chứng minh class weights hoặc resampling vô ích cho mọi learner, partition hay attack-family metric.

## Quyết định và giới hạn

Đóng original Phase 9 bằng nhánh **no synthetic resampling** cho primary binary experiment. Cơ sở: attack là lớp đa số trong TRAIN; protocol ưu tiên giữ phân phối dữ liệu quan sát và có metric nhạy với hai lớp. Không có matched no-resampling-vs-resampling experiment; vì vậy không claim đã chứng minh no-resampling tốt hơn.

Official TEST đã mở. Không chạy bù SMOTE/resampling, không dùng TEST để chọn class weights, không thay đổi frozen models/features/threshold. Secondary questions về rare attack families thuộc phạm vi error analysis/independent future design, không suy ra từ binary overall proportion.

Evidence paths:

- `results/data_audit/unsw_nb15/class_distribution.csv`
- `results/tuning/unsw_nb15/phase8_controlled/tables/stacking42_meta_grid_results.csv`
- `results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json`
- `results/final_evaluation/unsw_nb15/phase9_holdout/experiment_metadata.json`

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| P9-C1 | Report TRAIN binary class counts | DONE | `class_distribution.csv` |
| P9-C2 | Document no-resampling branch | DONE | This closure note |
| P9-C3 | State counterfactual limitation | DONE | No resampling experiment exists; see above |

