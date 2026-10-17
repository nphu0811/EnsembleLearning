# Bộ hỏi đáp bảo vệ P20-PRE

DRAFT. 27 câu hỏi, chưa rehearsal hoặc được hội đồng thật xác nhận. Các câu trả lời là đề xuất cho phần bảo vệ, không phải sửa PDF hoặc khẳng định concern đã đóng.

## DQ01 Công trình thực sự giải quyết bài toán nào?

Mức độ MEDIUM. Chủ đề scope.

Phân loại nhị phân Normal=0 và Attack=1 trên UNSW-NB15. attack_cat chỉ dùng phân tích lỗi theo nhãn thật. Chúng tôi không có detector đa lớp, thử nghiệm live IDS hoặc chứng minh thuật toán ensemble mới.

Nguồn trong immutable packet

- `report/chapters/methodology.tex`. Thiết kế và tập dữ liệu.

## DQ02 TRAIN và TEST được tổ chức thế nào, TEST có được dùng chọn ngưỡng không?

Mức độ MEDIUM. Chủ đề split.

Giữ official TRAIN 175.341 dòng và TEST 82.332 dòng. TEST có 37.000 Normal và 45.332 Attack. Cấu hình và threshold 0,5 đã khóa trước final evaluation; vòng phản biện này chỉ đọc summaries, không mở raw TEST hoặc dự đoán từng dòng.

Nguồn trong immutable packet

- `report/chapters/methodology.tex`. Thiết kế và tập dữ liệu.
- `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`. All candidates decision_threshold.

## DQ03 8.541 dòng trùng TRAIN có khiến toàn bộ kết quả vô hiệu không?

Mức độ HARD. Chủ đề overlap.

Đó là overlap theo vector 42 predictors, không tự chứng minh mọi hình thức leakage hay làm mọi hàng TEST vô giá trị. Chúng tôi báo cáo official view và sensitivity view 73.791 novel-vector rows. Hai view phụ thuộc nhau, không phải hai thí nghiệm độc lập. Novel-vector cũng không chứng minh unseen attack families.

Nguồn trong immutable packet

- `results/data_audit/unsw_nb15_views/view_summary.json`. overlapping_test_rows/novel_vector_test_rows.

## DQ04 Feature selection có hoàn toàn nested và leakage-free không?

Mức độ HARD. Chủ đề feature_selection.

Không. Stable features được chọn trên toàn bộ official TRAIN trước development CV. Vì vậy điểm CV có nguy cơ lạc quan. Final TEST không được dùng fit selector theo source, nhưng điều đó không biến development selection thành fully nested. Muốn đo lợi ích quy trình FS phải có nghiên cứu nested mới được phê duyệt, không sửa bảng hiện tại.

Nguồn trong immutable packet

- `report/chapters/methodology.tex`. Feature selection và preprocessing.

## DQ05 OOF stacking khác với meta học từ dự đoán in-sample ở đâu?

Mức độ HARD. Chủ đề stacking.

P9 dựng StackingClassifier với các base pipeline LR, DT, RF và cv=inner_cv; inner StratifiedKFold có 3 folds. predict_proba của các clone trong CV tạo đầu vào meta LR, passthrough=False. OOF tránh để mỗi base dự đoán đúng hàng mà nó fit trong bước tạo meta inputs; nó không tự loại mọi thiên lệch ở bước chọn base/siêu tham số.

Nguồn trong immutable packet

- `src/models/run_unsw_phase9_final_holdout.py`. make_stacking_42.
- `src/models/run_unsw_phase9_final_holdout.py`. make_stacking_42.

## DQ06 Tại sao có OOF vẫn chưa được gọi là fully nested model selection?

Mức độ HARD. Chủ đề selection_bias.

OOF là một ranh giới fit của stacking. Base/config selection và meta hyperparameter search có thể dùng thông tin phát triển chung. Báo cáo đã ghi meta tuning chưa fully nested; không thể coi CV đánh giá lại sau selection là unbiased outer test. Muốn khắc phục phải thiết kế outer/inner selection mới với holdout hợp lệ riêng.

Nguồn trong immutable packet

- `report/chapters/methodology.tex`. Các pipeline được khóa.

## DQ07 Có thể nói giảm 42 xuống 17 feature làm mô hình nhanh hơn 6,48 lần không?

Mức độ HARD. Chủ đề ablation.

Không thể quy riêng cho feature count. RF42 có 300 cây, min_samples_leaf=1; RF17 có 150 cây, min_samples_leaf=2. Kết quả là trade-off giữa hai pipeline cùng thay feature và hyperparameters. Cần matched hoặc factorial experiment để phân biệt các tác động, chưa được phép chạy trong checkpoint này.

Nguồn trong immutable packet

- `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`. random_forest_42/random_forest_17.
- `report/chapters/methodology.tex`. Comparison caveat.

## DQ08 Nghiên cứu đã chứng minh resampling không cần thiết chưa?

Mức độ HARD. Chủ đề imbalance.

Chưa. TRAIN nghiêng về Attack và TEST có prevalence khác. Meta frozen dùng class_weight=None; một trường class_weight hoặc một tìm kiếm meta không là controlled imbalance ablation. RQ5 chưa có đối chứng matched về sampling/weighting trong folds. Không dùng official TEST để lựa chọn SMOTE hay class weight mới.

Nguồn trong immutable packet

- `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`. stacking_42 meta_learner.
- `report/chapters/conclusion.tex`. Công việc còn thiếu.

## DQ09 FPR cao có cho phép hạ hoặc nâng ngưỡng ngay để cứu kết quả không?

Mức độ HARD. Chủ đề threshold.

Không. Threshold hiện là 0,5 cho cả ba candidate. Phân tích hậu nghiệm có thể giải thích hạn chế nhưng không được chọn threshold theo TEST. Một operating point khác cần validation và contract mới; không gắn score mới vào kết quả frozen.

Nguồn trong immutable packet

- `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`. decision_threshold.
- `report/chapters/methodology.tex`. Final evaluation.

## DQ10 Accuracy khoảng 87% đã đủ để gọi IDS tốt chưa?

Mức độ MEDIUM. Chủ đề accuracy.

Chưa. RF42 accuracy=0.869589, attack Recall=0.983808, nhưng FPR=27.0351%. Recall cao đi cùng lượng báo động giả lớn. Chưa có prevalence vận hành, chi phí cảnh báo hoặc điều kiện network thực để kết luận utility.

Nguồn trong immutable packet

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`. random_forest_42 official_test.
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`. random_forest_42 official_test.

## DQ11 Macro F1 và Weighted F1 trả lời các câu hỏi nào?

Mức độ MEDIUM. Chủ đề metrics.

Macro F1 cho hai lớp trọng số bằng nhau; Weighted F1 dùng support của từng lớp. RF42 có Macro F1=0.863343 và Weighted F1=0.866300; Stacking có 0.863840 và 0.866742. Không đổi F1 Attack hoặc F1 không ghi averaging của external paper thành Macro F1.

Nguồn trong immutable packet

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`. official_test macro_f1/weighted_f1.

## DQ12 Giảm 142 FP nhưng tăng 118 FN có phải cải thiện tổng thể?

Mức độ HARD. Chủ đề error_cost.

Đây là trade-off quan sát. RF42 FP=10.003, FN=734; Stacking FP=9.861, FN=852. Không có ma trận chi phí hay trọng số attack-family vận hành nên chưa quy thành lợi ích tổng thể. Ít lỗi tổng cộng hơn về số học không tự đồng nghĩa tốt hơn về an ninh.

Nguồn trong immutable packet

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`. RF42 and stacking official_test.

## DQ13 CI chứa 0 chứng minh hai mô hình tương đương hay Stacking tốt hơn không?

Mức độ HARD. Chủ đề paired_CI.

Không cho cả hai. Delta Macro F1 Stacking-RF42=0.000496689894; CI95% [-0.000311804213, 0.001308950325]. Chưa đủ bằng chứng superiority trên thước đo này. Equivalence cần biên thực tiễn định trước và phép suy luận phù hợp; không được tạo biên hậu nghiệm để hợp thức hóa.

Nguồn trong immutable packet

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`. official_test stacking_42 vs random_forest_42 macro_f1.

## DQ14 McNemar p=0,468377 có phải p-value cho chênh lệch Macro F1?

Mức độ HARD. Chủ đề McNemar.

Không. Exact two-sided McNemar dùng 491 và 515 trường hợp discordant về đúng/sai tổng thể, p Holm=0,46837651914684564. Nó kiểm tra paired correctness, không trực tiếp Macro F1, MCC hoặc equivalence. Cần giữ riêng paired metric CI.

Nguồn trong immutable packet

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`. official_test stacking_42 vs random_forest_42.

## DQ15 Holm có điều chỉnh mọi CI và mọi phân tích hậu nghiệm không?

Mức độ HARD. Chủ đề multiplicity.

Không. Holm ở bảng McNemar áp dụng ba pairwise correctness comparisons trong mỗi evaluation view theo implementation. CI bootstrap metric là pointwise; hai view dùng chung nhiều dòng, attack-family và các profile là exploratory. Không tuyên bố toàn bộ tập phát hiện đã được familywise control.

Nguồn trong immutable packet

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`. three pairs per view.
- `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`. mcnemar.

## DQ16 10.000 bootstrap draws có nghĩa 10.000 lần tái huấn luyện độc lập không?

Mức độ HARD. Chủ đề bootstrap_unit.

Không. Source dùng stratified paired multinomial bootstrap trên joint prediction patterns của benchmark đã khóa, giữ ghép cặp và support theo lớp. CI có điều kiện trên rows và mô hình đã fit. Không định lượng độ bất định do huấn luyện lại, model selection hoặc session/host dependence; không nhân n thực nghiệm lên 10.000.

Nguồn trong immutable packet

- `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`. bootstrap type and interpretation.

## DQ17 Tại sao không gọi bảng Fuzzers/Generic là kết quả multiclass?

Mức độ HARD. Chủ đề attack_family.

Model vẫn dự đoán Normal/Attack. Bảng phân nhóm FN theo nhãn thật attack_cat sau dự đoán binary. Stacking tăng 133 FN ở Fuzzers và giảm 43 ở Generic so RF42, cho thấy tác động không đồng đều. Không đánh giá đúng loại tấn công được dự đoán.

Nguồn trong immutable packet

- `report/chapters/results_discussion.tex`. Phân tích lỗi theo họ tấn công.

## DQ18 RF17 không bỏ sót Worms có chứng minh phát hiện hoàn hảo họ này không?

Mức độ HARD. Chủ đề rare_attack.

Không. Chỉ có 44 Worms trong benchmark; RF17 FN=0 nhưng Wilson95% miss-rate upper=0,08029560375848066. Đây vẫn là row-based interval có giả định, không bảo đảm cho Worms ngoài benchmark hoặc session độc lập.

Nguồn trong immutable packet

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`. official_test Worms random_forest_17.

## DQ19 Novel-vector có tương đương unknown attacks, temporal hay external validation không?

Mức độ HARD. Chủ đề generalization.

Không. Novel-vector chỉ khác đúng vector predictors của TRAIN. Nhãn attack families, môi trường và phân bố có thể cùng nguồn. Cả official và novel-view vẫn thuộc một TEST; chưa có time/session/host split hoặc network mới. Tuyên bố zero-day hay transfer sẽ vượt evidence.

Nguồn trong immutable packet

- `results/data_audit/unsw_nb15_views/view_summary.json`. purpose.

## DQ20 Có thể dùng thời gian lịch sử để cam kết tốc độ real-time không?

Mức độ HARD. Chủ đề runtime.

Không. Các số train lịch sử RF42=371,244s, Stacking=980,170s, RF17=57,255s; inference là thời gian batch chia số mẫu, không latency end-to-end từng flow. Original environment UNKNOWN và chưa đo capture/feature extraction, tải, jitter hoặc hardware vận hành. P15 timings ở môi trường tái dựng là provenance khác.

Nguồn trong immutable packet

- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`. pipeline timing rows.
- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`. inference column.

## DQ21 P15 đã hoàn tất mà trang 33 nói chưa có full TRAIN artifact, trả lời thế nào?

Mức độ HARD. Chủ đề reproducibility.

Trang 33 là snapshot trước reconstruction. P15 hiện có ba reconstructed full-TRAIN artifacts đã qua author-host acceptance 69/69. Chúng không chứng minh giống binary lịch sử hay tái lập TEST scores trong môi trường gốc. Dùng companion status note, không sửa PDF đã duyệt và không gán score lịch sử cho artifact mới.

Nguồn trong immutable packet

- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. scope.
- `report/chapters/conclusion.tex`. Công việc còn thiếu.

## DQ22 L06, L12 và N02 đã đủ để tuyên bố thuật toán của đề tài mới không?

Mức độ HARD. Chủ đề references.

Chưa. Ghi chép nguồn cho thấy L06 có Chi-square và stacking; N02 MI-Boruta, RF/XGB/Catboost tới MLP trên UNSW; L12 hybrid FS/SMOTE-Tomek/stacking nhưng không phải UNSW. Khác learner/config/protocol không tự là methodological novelty. Phần đọc là selected sections; N01/N03 chỉ abstract nên không tự dựng Methods của họ.

Nguồn trong immutable packet

- `literature_reported_facts.csv`. L06 C02/C03;N02 C09/C10;L12 C15.
- `literature_scope.json`. reading_status records.

## DQ23 Tại sao không so điểm đề tài trực tiếp với paper N02?

Mức độ HARD. Chủ đề protocol_comparison.

N02 mô tả gộp TRAIN/TEST rồi random80/20, khác official holdout của đề tài. Task binary/multiclass, averaging, preprocessing và scope đo chi phí còn khác. Chúng tôi dùng bài để xác định prior art và thiết kế, không lập bảng xếp hạng thắng/thua qua score không matched.

Nguồn trong immutable packet

- `literature_reported_facts.csv`. N02 Methodology/Data description C08.

## DQ24 Nếu không có thuật toán mới, đóng góp có thể bảo vệ là gì?

Mức độ HARD. Chủ đề contribution.

Một case study thực nghiệm có kiểm toán trên UNSW-NB15. Điểm có evidence là chuỗi source/config/results đã khóa, đối chiếu RF/ensemble, error complementarity và giới hạn của nó, paired metric uncertainty, FP/FN và cost trade-off, overlap sensitivity và reconstructed-artifact provenance. Chưa đủ để quảng bá SOTA hoặc phương pháp mới; giá trị công bố còn cần đánh giá theo venue và bằng chứng bổ sung.

Nguồn trong immutable packet

- `report/chapters/conclusion.tex`. Đóng góp trong phạm vi đã chứng minh.

## DQ25 Những thiếu sót nào không thể sửa bằng câu chữ?

Mức độ HARD. Chủ đề new_study.

Tính ổn định qua independent training, isolated causal effect của FS, matched imbalance comparison, external/session/time generalization và deployment cost cần nghiên cứu mới. Tài liệu có thể giới hạn claim và ghi đúng status, không tạo dữ liệu cho các câu hỏi này. Mọi nghiên cứu tiếp phải có protocol và holdout hợp lệ được phê duyệt, không tái sử dụng TEST hiện tại để chọn thắng.

Nguồn trong immutable packet

- `report/chapters/conclusion.tex`. Công việc còn thiếu và hướng nghiên cứu.

## DQ26 Vì sao phải giữ Voting không tốt bằng RF và Stacking chưa thắng rõ?

Mức độ MEDIUM. Chủ đề negative_results.

Đó là bằng chứng trả lời RQ1 trong scope đã làm. Chọn chỉ điểm thuận lợi sẽ thay đổi câu hỏi thành tìm mô hình thắng. Báo cáo giữ cả kết quả Voting không thuận lợi và kết luận Stacking không xác lập superiority tổng thể. Development CV không thay final holdout và cũng không phải training-repeat replication.

Nguồn trong immutable packet

- `report/chapters/conclusion.tex`. Đóng góp trong phạm vi đã chứng minh.

## DQ27 Có thể trình diễn live inference bằng official TEST và công bố gói hiện tại chưa?

Mức độ HARD. Chủ đề deployment.

Chưa trong contract này. Không mở official TEST/prediction CSV và không có live demo được nghiệm thu. Demo tương lai cần dữ liệu thử hợp lệ, schema và provenance của reconstructed artifact theo contract riêng. Quyền code/license, data/model và tài liệu bên thứ ba cần quyết định của chủ sở hữu; manifest nội bộ không cấp quyền phát hành.

Nguồn trong immutable packet

- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. scope.
