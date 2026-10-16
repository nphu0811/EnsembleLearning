# Original Phase 11 — Evaluation Protocol: CHECKPOINT

**Trạng thái: DONE (trong phạm vi binary UNSW-NB15 đã khóa).**

## Nguồn và tính toàn vẹn

- Chỉ đọc `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv` và `cost_metrics.csv`.
- Không huấn luyện/tune/reselect model, không dùng raw data hoặc official-test predictions ở mức từng mẫu.
- Phát sinh Weighted-F1, precision/recall/F1/support của từng lớp và explicit confusion counts từ aggregate TN/FP/FN/TP đã lưu.
- Kiểm lại tám chỉ số từ confusion counts (Accuracy, Balanced Accuracy, Attack Precision/Recall/F1, Macro-F1, FPR/FNR) và tất cả khớp với nguồn gốc.
- AUC/MCC, runtime và model size **sao chép từ bảng đã khóa**, không suy ra lại từ confusion counts.

## Official test (82,332 mẫu)

| Pipeline | Weighted F1 | Macro-F1 | MCC | Normal recall | Attack recall |
| --- | --- | --- | --- | --- | --- |
| RF-42 | 0.866300 | 0.863343 | 0.750910 | 72.96% | 98.38% |
| Stacking-42 | 0.866742 | 0.863840 | 0.750497 | 73.35% | 98.12% |
| RF-17 | 0.863730 | 0.860673 | 0.746881 | 72.37% | 98.44% |

## Confusion matrix — actual labels theo hàng, predicted labels theo cột

| Pipeline | TN | FP | FN | TP |
| --- | --- | --- | --- | --- |
| RF-42 | 26997 | 10003 | 734 | 44598 |
| Stacking-42 | 27139 | 9861 | 852 | 44480 |
| RF-17 | 26776 | 10224 | 708 | 44624 |

Với nhãn Attack = 1:
- TN: Normal dự đoán Normal.
- FP: Normal dự đoán Attack (báo động giả).
- FN: Attack dự đoán Normal (bỏ sót tấn công).
- TP: Attack dự đoán Attack.

Chi tiết official + novel-vector: ba CSV cùng thư mục.

## Computational complexity

Số feature, training time, inference ms/sample và serialized model size có trong `phase11_final_evaluation_complete.csv`.
Chi phí đo được chỉ áp dụng cho môi trường thử nghiệm hiện có. Không tuyên bố benchmark phần cứng phổ quát hoặc đã đo memory/energy/real-time throughput. Random Forest có nhiều cây; Stacking có thêm base learners và meta learner nên computation phức tạp hơn một pipeline RF đơn, nhưng runtime thực nghiệm mới là evidence so sánh chính.

## Giới hạn và cách diễn giải

- Weighted F1 bị ảnh hưởng bởi support của từng lớp; không dùng để thay thế Macro-F1, MCC hay FPR/FNR.
- `precision`, `recall`, `f1` nguyên bản trong `final_metrics.csv` là của **Attack (class 1)**, không phải của Normal.
- Per-attack-family miss rate chỉ là phân tích lỗi của binary detector, không phải multiclass precision/recall.
- Novel-vector subset là cùng benchmark, không phải external validation.
- Không có bằng chứng tổng thể Stacking-42 vượt RF-42 rõ ràng: paired CI của chênh lệch Macro-F1 chứa 0 (Phase 12).

## Research Decisions Log

**Decision:** Đóng Phase 11 bằng cách bổ sung derived metrics từ confusion counts đã lưu.  
**Reason:** Checklist roadmap gốc còn thiếu Weighted F1, per-class P/R/F1/support và ma trận nhầm lẫn trình bày tường minh.  
**Evidence:** `final_metrics.csv`, `cost_metrics.csv`, ba bảng xuất từ script này, kiểm toán identity số học PASS.  
**Consequence:** Giữ nguyên 3 frozen pipelines, official holdout và mọi kết luận khoa học; không phát sinh tuning hoặc model selection mới.

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| P11-01 | Accuracy, Precision, Recall, F1, Macro-F1, MCC, ROC/PR-AUC | DONE | Original final_metrics.csv + final_evaluation_complete.csv |
| P11-02 | Weighted F1 | DONE | phase11_final_evaluation_complete.csv |
| P11-03 | Per-class P/R/F1/support | DONE | phase11_per_class_metrics.csv |
| P11-04 | Confusion matrices | DONE | phase11_confusion_matrices.csv |
| P11-05 | FPR/FNR, detection rate, balanced accuracy | DONE | final_evaluation_complete.csv |
| P11-06 | Training/inference cost, original feature counts and model size | DONE | final_evaluation_complete.csv |
| P11-07 | Recompute and verify metrics from locked confusion counts | DONE | Assertion checks in close_original_phase11.py |
| P11-08 | Hardware-independent complexity claims | NOT CLAIMED | Qualitative limitation above |

**Bước tiếp theo:** Original Phase 12 statistical validation đã có artifact từ trước; đối chiếu và dùng lại. Original Phase 13 có retrospective ablation tổng hợp, không coi là full factorial. Sau đó bắt đầu **Original Phase 14 — Error Analysis**, chỉ dùng frozen predictions và không thay model.
