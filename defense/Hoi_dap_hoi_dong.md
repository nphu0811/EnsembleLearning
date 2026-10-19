# Hỏi đáp hội đồng dựa trên bằng chứng hiện có

Bản nháp nội bộ ngày16/10/2026.20 câu hỏi phục vụ chuẩn bị bảo vệ; chưa phải reviewer report, chưa thay phê duyệt GVHD và chưa xác nhận defense-ready. Câu trả lời giữ phạm vi binary UNSW-NB15 đã thực hiện. Evidence paths tính từ root workspace.

## 1. Đề tài có đóng góp gì nếu stacking đã có từ trước?

Đóng góp hiện có là so sánh các pipeline trong một benchmark, kiểm toán quá trình lựa chọn/đánh giá và phân tích đánh đổi hiệu quả, chi phí, báo động giả, bỏ sót. Chúng tôi chưa chứng minh novelty thuật toán. Literature mới đối chiếu cho thấy stacking, voting và kết hợp FS đã có prior work; không đặt tên mới cho tổ hợp quen thuộc để nhận là thuật toán mới.

Evidence: `docs/CLAIM_EVIDENCE_MATRIX.md`, `literature/gap_matrix.md`.

## 2. Stacking có tốt hơn Random Forest không?

Không có đủ bằng chứng để kết luận Stacking-42 vượt RF-42 tổng thể trên holdout đã lưu. Chênh lệch Macro-F1 khoảng0,000497, CI95% từ−0,000312 đến0,001309 chứa0. Điều được quan sát rõ là giảm báo động giả cùng tăng bỏ sót. Không biến kết quả này thành tuyên bố hai mô hình tương đương thống kê.

Evidence: `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`.

## 3. Đánh đổi cụ thể là gì?

Trên cùng official TEST, RF-42 có10.003 FP và734 FN; Stacking-42 có9.861 FP và852 FN. Stacking giảm142 báo động giả và tăng118 mẫu tấn công bị bỏ sót. Tính phù hợp thực tế còn phụ thuộc chi phí nghiệp vụ của hai loại lỗi; nghiên cứu chưa có cost matrix do đơn vị vận hành cung cấp.

Evidence: `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`.

## 4. Vì sao không chỉ báo cáo Accuracy?

Accuracy không tách FP và FN hoặc hiệu năng hai lớp. Chúng tôi báo cáo Macro-F1, MCC, FPR/FNR, per-class precision/recall/F1, AUC và chi phí. Cùng Accuracy gần nhau có thể che các sai khác nghiệp vụ quan trọng, như số FP/FN của hai pipeline trên.

Evidence: `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`.

## 5. Nhãn dương là gì và FPR/FNR tính ra sao?

Attack là1, Normal là0. FPR=FP/(TN+FP), tức tỷ lệ Normal bị báo tấn công. FNR=FN/(TP+FN), tức tỷ lệ Attack bị bỏ sót. Detection Rate là Recall của Attack. Không dùng Recall của Normal thay cho Detection Rate mà không ghi rõ lớp.

Evidence: `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/PHASE11_CHECKPOINT.md`.

## 6. Weighted-F1 và Macro-F1 khác nhau thế nào?

Macro-F1 trung bình F1 hai lớp với trọng số bằng nhau. Weighted-F1 dùng support từng lớp nên lớp nhiều mẫu có ảnh hưởng lớn hơn. Hai metric bổ sung nhau; Weighted-F1 không thay phân tích per-class hoặc attack-family misses.

Evidence: `src/analysis/close_original_phase11.py`, `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_per_class_metrics.csv`.

## 7. Có đánh giá phân loại đa lớp tấn công không?

Chuỗi thực nghiệm được kiểm chứng hiện tại là binary. Các bảng theo attack_cat phân tích mẫu tấn công nào binary detector bỏ sót; đó không phải multiclass precision/recall hay mô hình nhận diện đúng từng attack category. Chưa có bằng chứng thực nghiệm để kết luận về chất lượng multiclass model.

Evidence: `docs/research/ERROR_ANALYSIS_CLOSURE.md`.

## 8. Tập dữ liệu và cách chia được xác định thế nào?

Nghiên cứu dùng official preset TRAIN175.341 dòng và TEST82.332 dòng của UNSW-NB15. Ba CSV local khớp hash lịch sử; đây là kiểm định local integrity, không xác nhận URL tải gốc hoặc checksum do nhà cung cấp công bố. Không tự tạo random split mới sau khi xem TEST.

Evidence: `results/reproducibility/resume_2026_10_16/p15_03_dataset.json`, `docs/research/DATASET_PROVENANCE.md`.

## 9. Có thể khẳng định hoàn toàn không leakage không?

Không. Preprocessing nằm trong pipeline và TEST không được dùng để tune theo cấu hình đã kiểm tra. Tuy nhiên feature selection học trên toàn bộ TRAIN trước development CV, nên CV có thể lạc quan do selection. Official split còn có feature-vector overlap; static source checks không chứng minh mọi leakage mode đã bị loại trừ. Những giới hạn này được công khai.

Evidence: `results/reproducibility/resume_2026_10_16/protocol/P15_04_PROTOCOL_REPORT.md`.

## 10. Tại sao không sửa feature selection rồi chạy lại cho đẹp hơn?

Sau khi đã xem TEST, thay feature/config rồi dùng lại TEST để chọn mô hình sẽ làm sai vai trò holdout. Chúng tôi giữ kết quả lịch sử và nêu giới hạn. Một protocol cải tiến cần được thiết kế và kiểm định riêng với cơ chế đánh giá phù hợp; không dùng nó để sửa lại lịch sử thí nghiệm đã khóa.

Evidence: `.research_memory/RESEARCH_CANON.md`, `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`.

## 11. Meta learner của stacking có học trên dự đoán in-sample không?

Cấu hình source dùng StackingClassifier với internal CV để tạo meta inputs, không đơn thuần train meta learner trên dự đoán in-sample của base learners. Tuy vậy quá trình chọn hyperparameters và tái sử dụng OOF features chưa fully nested; chúng tôi không gọi development score là ước lượng không thiên lệch sau selection.

Evidence: `docs/research/ENSEMBLE_FRAMEWORK.md`, `src/models/run_unsw_phase8_controlled_tuning.py`.

## 12. Vì sao chọn LR, DT và RF làm base learners?

Đó là các mô hình có cơ chế biểu diễn khác nhau để khảo sát error complementarity. Sự khác nhau về thuật toán tự nó không chứng minh ensemble gain. Chúng tôi có OOF diversity evidence và so sánh ensemble; kết quả voting kém vẫn được giữ. Không kết luận cứ đa dạng là stacking sẽ thắng.

Evidence: `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`.

## 13. RF-17 có chứng minh bỏ25 feature làm mô hình hiệu quả hơn không?

RF-17 là pipeline trade-off với17 features. Nó còn khác RF-42 về số cây và min_samples_leaf nên final comparison không cô lập tác động riêng của số feature. Chi phí có trong bảng đã lưu, nhưng không diễn đạt thành causal feature-only ablation.

Evidence: `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`, `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`.

## 14. Novel-vector subset có phải external validation không?

Không. Đó là view thuộc cùng benchmark TEST, được xây dựng để xem kết quả trên vectors không xuất hiện trong TRAIN theo quy tắc đã lưu. Nó không phải dữ liệu từ mạng hoặc thời điểm độc lập mới. Vì vậy RQ4 chỉ được trả lời một phần, chưa chứng minh generalization qua mạng thực.

Evidence: `results/data_audit/unsw_nb15_views/view_summary.json`, `src/data/build_unsw_experiment_views.py`.

## 15. Bootstrap10.000 lần có phải huấn luyện10.000 lần không?

Không. Đây là số resamples dùng tính uncertainty từ bằng chứng dự đoán đã lưu. CI này không đo đầy đủ biến thiên khi huấn luyện lại hoặc đổi môi trường mạng. Các mẫu network flow có thể phụ thuộc nhau; phải nêu giới hạn đó khi diễn giải CI.

Evidence: `src/analysis/run_unsw_phase10_statistics.py`, `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`.

## 16. McNemar p≈0,468 có phải p-value cho Macro-F1 không?

Không. Bảng McNemar so sánh paired overall correctness/error rate. Chênh lệch Macro-F1 có bảng paired bootstrap riêng. Không gán p-value của correctness cho Macro-F1 hoặc suy “không khác biệt có ý nghĩa” thành “hai mô hình tương đương”.

Evidence: `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`.

## 17. Nghiên cứu đã chứng minh SMOTE không cần thiết chưa?

Chưa. Scope hiện tại có no-resampling/class-weight diagnostics nhưng không matched resampling ablation. RQ5 phải giữ một phần. Literature về sampling không thay bằng chứng thực nghiệm cho pipeline của chúng tôi; chưa có cơ sở nói sampling luôn tốt hoặc luôn kém.

Evidence: `docs/research/ENSEMBLE_FRAMEWORK.md`, `literature/gap_matrix.md`.

## 18. Những gì đã được tái lập thật?

Đã chạy kiểm raw hash/schema, source/config consistency, tests và replay hậu xử lý aggregate trong venv stdlib mới. Ba CSV P11 giống từng byte. Chưa replay toàn bộ training trong fresh ML environment, original training environment vẫn UNKNOWN. Import smoke Python3.14 trong lịch sử không chứng minh môi trường huấn luyện gốc.

Evidence: `results/reproducibility/resume_2026_10_16/clean_replay_report.json`, `docs/research/REPRODUCIBILITY_RUNBOOK.md`.

## 19. Hệ thống đã sẵn sàng làm IDS thời gian thực hoặc demo suy luận chưa?

Chưa có model serialized được kiểm định trong workspace và chưa có inference demo end-to-end. Bảng model size lịch sử không thay file model. Hiện có source và evidence offline; để trình diễn inference cần artifact mô hình, schema, môi trường tương thích và kiểm thử đầu vào/đầu ra. Không tự nhận đã triển khai packet capture hay bảo vệ mạng thật.

Evidence: `release/RELEASE_BLOCKERS.md`, `docs/research/DATA_CODE_AVAILABILITY.md`.

## 20. Những thiếu sót nào còn ngăn nộp hồ sơ?

Cần hoàn thiện và render đề cương/báo cáo theo mẫu, kiểm bibliography, ML reproducibility/model demo, slide/script và QA cuối. Các thông tin tác giả/GVHD/ngày/chữ ký và điều kiện hành chính cần được xác nhận. Có artifact mới không đồng nghĩa tất cả G0–G6 đã đạt; hiện chưa đủ điều kiện nộp.

Evidence: `release/RELEASE_BLOCKERS.md`, `docs/TEMPLATE_REQUIREMENTS_MATRIX.md`.
