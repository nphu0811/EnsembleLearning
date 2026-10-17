# Reviewer A

## Phạm vi và kiểm tra tính toàn vẹn

AI-simulated internal scientific criticism; P20-PRE; không phải hội đồng người thật hoặc nghiệm thu cuối.

Chỉ packet_02/local_contents, manifest.csv, receipt.json, COMMON_REVIEW_RULES.md, BRIEF_A.md và skill đã cài. Không đọc báo cáo của người phản biện khác, QA cũ ngoài gói, bộ nhớ nghiên cứu hoặc nguồn Internet.

Một invocation/context riêng; cô lập theo hợp đồng truy cập trên hệ thống tệp dùng chung, không phải rào quyền hệ điều hành hoặc xác nhận người thật.

Học máy và phương pháp, chọn đặc trưng, preprocessing, validation, OOF/stacking, tuning, threshold, công bằng so sánh và tái lập.

Manifest SHA256 `c0f0b3828ba16ce8312b489915cc4c56c9fc7c771dbeefe1d7a9bb78938b62b7`. Đã kiểm tra 80/80 tệp theo SHA256 và kích thước, không có sai lệch. PDF có 37 trang, SHA256 `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`.

Ba source/config/subset input SHA256 trong mỗi run_report P15 khớp byte của tệp tương ứng trong gói. SHA256 TRAIN trong ba record khớp raw_file_checksums.csv ở cấp catalog; không mở hoặc tự hash raw TRAIN. Không có model bytes nên không xác minh artifact SHA256 trong record.

Đọc văn bản bản thảo và các chương active qua report/main.tex, đọc nguồn FS, baseline/ensemble CV, tuning, final holdout và thống kê cùng bảng liên quan. Kiểm tra trực quan PDF các trang vật lý 24, 25, 27, 28, 29, 30, 32 và 35. Số trang trong phản biện là trang vật lý PDF.

Chỉ đọc nguồn, hash tệp và kiểm tra bảng tổng hợp. Không train, bootstrap, import/chạy mã ML, đọc raw/prediction CSV, tải model, hoặc sửa gói.

Catalog và publisher-reported notes là nguồn thứ cấp có phạm vi đọc hạn chế. Không chứng nhận Methods chưa đọc, không suy ra novelty toàn ngành và không đối chiếu điểm số khác protocol như baseline matched.

## Đánh giá khoa học tổng thể

Bằng chứng đóng băng hỗ trợ một case study nhị phân có kết luận thận trọng. Stacking-42 nhỉnh Macro-F1 khoảng 0,000497 nhưng thấp hơn MCC khoảng 0,000413 so với RF-42; hai CI cặp chứa 0. Giảm 142 FP đi cùng tăng 118 FN. Bản thảo đã tránh suy ra tương đương, ưu thế chung, cơ chế nhân quả hoặc triển khai thực tế.

Nguồn final dùng các base Pipeline bên trong StackingClassifier với predict_proba, inner StratifiedKFold 3 fold, shuffle và seed 137, passthrough=False. Đây là OOF thật theo constructor nguồn, không phải pure in-sample meta fitting. Stable 17 được phát hiện trước development CV; tuning meta dùng ma trận OOF cố định sau tuning RF và chưa nested toàn bộ. Những giới hạn này đã được công khai và không chứng minh official TEST đã được dùng để tuning.

RF-42 có 300 cây, leaf=1; RF-17 có 150 cây, leaf=2. Số đặc trưng và siêu tham số thay đổi cùng nhau. So sánh xác định kết quả và chi phí của hai pipeline đã chọn, không xác định tác động nhân quả riêng của Feature Selection. Bản thảo hiện diễn giải đúng điểm này.

Cần sửa lớn về khả năng kiểm tra đường phát triển mô hình, bằng chứng định lượng cho RQ3/Voting, và trạng thái tái dựng P15. Không phát hiện sai số số học làm đảo ngược kết luận hẹp từ các bảng đã đọc. Các Major dưới đây không được gắn Blocking vì chúng chưa phủ định kết luận hẹp về các dự đoán lịch sử đã khóa.

## Độc giả phù hợp

Người nghiên cứu IDS bằng dữ liệu bảng, sinh viên học phương pháp đánh giá ML và người kiểm tra tái lập sẽ quan tâm đến việc một cải thiện metric rất nhỏ che đánh đổi FP/FN và chi phí. Giá trị liên ngành rộng hiện chưa được chứng minh.

## Điểm mạnh có bằng chứng

### A-S1

Diễn giải đúng hiệu ứng cặp, không dùng nonsignificance làm bằng chứng tương đương và không chọn một metric để tuyên bố chiến thắng.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.1, PDF p34. Anchor `không xác nhận ưu thế tổng thể`
- [results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv), official_test, stacking_42 minus random_forest_42, mcc. Anchor `-0.0004130362586621805,0.95,-0.0019378760206115232,0.0011395704058473617`

### A-S2

Nguồn final triển khai OOF qua StackingClassifier, preprocessing nằm trong từng base Pipeline và refit base learners theo constructor, phù hợp mô tả hẹp về OOF.

- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_lr_pipeline. Anchor `return Pipeline([`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_stacking_42. Anchor `cv=inner_cv,`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_stacking_42. Anchor `passthrough=False,`

### A-S3

Công khai cả FS trước development CV và confounding siêu tham số ở RF-17/RF-42 ngay trong Methods và Discussion.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.2, PDF p24. Anchor `Chúng tôi không tuyên bố loại trừ mọi dạng leakage.`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.3, PDF p32. Anchor `RF-42 dùng 300 trees`
- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), random_forest_17.hyperparameters. Anchor `"n_estimators": 150`

### A-S4

Threshold 0,5 và feature tracks được đóng băng trong cấu hình; phase8 tự giới hạn sweep là chẩn đoán. Phân tích hậu nghiệm không được dùng để chọn threshold mới.

- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), all three candidates. Anchor `"decision_threshold": 0.5`
- [results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json), threshold_policy. Anchor `No threshold is auto-selected; candidates remain at 0.5.`
- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.5, PDF p26. Anchor `không dùng để suy ra quan hệ nhân quả hay tạo threshold mới.`

### A-S5

Giữ rõ binary attack-family error analysis và novel-vector subset của cùng TEST; không trình bày chúng thành multiclass hoặc external validation.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.1, PDF p24. Anchor `không phải mô hình đa lớp`
- [results/data_audit/unsw_nb15_views/view_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_views/view_summary.json), purpose. Anchor `Secondary leakage/repetition sensitivity evaluation only; does not replace official test.`
- [results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv), stacking_42 official_test. Anchor `stacking_42,official_test,27139,9861,852,44480,37000,45332,82332`

## Major Concerns

### A-M1

**Major. Blocking No. reproducibility. VERIFIED. OPEN.**

Vị trí yêu cầu đánh giá. PDF pp24-26, §§3.2-3.4; track 17, preprocessing và quá trình chọn cấu hình.

Methods cho biết dùng một danh sách 17 feature đã lưu nhưng chưa cho thuật toán tạo danh sách, tên/thứ tự 17 biến, các seed/mẫu stability, quy tắc bỏ redundancy, hoặc quan hệ với tập RFECV 13 biến. Cũng chưa ghi rõ one-hot cho proto/service/state, handle_unknown, chỉ scale biến số của LR, grid/tập metric chọn RF và ma trận OOF cố định dùng để chọn meta. Câu về mọi biến đổi có tham số nằm trong Pipeline cần giới hạn vào các pipeline model, vì wrapper RFECV fit preprocessing trên toàn sample trước CV nội bộ. Wrapper không phải danh sách stable_2plus_methods cuối; không nên gộp chúng thành một quy trình nested đã được kiểm chứng.

Vì sao cần sửa. Khả năng truy vết quy trình là đóng góp trung tâm. Chỉ có một constructor final và một đường dẫn tới danh sách đã lưu chưa giúp người đọc hiểu RF-17 được hình thành và chọn như thế nào, hoặc vùng validation nào thực sự được bảo vệ.

Tiêu chí giải quyết. Bổ sung một bảng/sơ đồ Methods từ nguồn đã khóa với danh sách 17 biến theo thứ tự; stability 5 seed, sample 60.000, top-k 20, tần suất >=3/5 trong >=2/3 phương pháp; tách RFECV 50.000 mẫu/13 biến; mô tả encoder/scaler và ranh giới fit; nêu RF grid 12 candidate với 3-fold Macro-F1, base OOF 3-fold và meta grid 10 candidate/5-fold. Nêu rõ preprocessing ngoài RFECV nội bộ và FS/meta selection chưa fully nested. Đối chiếu từng ô với source/config, không chạy lại thí nghiệm.

Lộ trình DOCUMENT. Thiếu mô tả có ảnh hưởng đáng kể đến kiểm tra và tái sử dụng đóng góp phương pháp, nhưng các bảng official holdout vẫn diễn giải được; vì vậy Major, không Blocking.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.2, PDF p24. Anchor `Track 17 feature ổn định lấy từ danh sách đã lưu của official TRAIN`
- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), configuration. Anchor `STABILITY_MIN_FREQUENCY = 0.60`
- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), run_stability. Anchor `stable_method_votes`
- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), run_rfecv. Anchor `X = prep.fit_transform(sample[candidate_features])`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), rf_param_grid. Anchor `"model__n_estimators": [150, 300]`
- [results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json), selection design. Anchor `"meta_cv_splits": 5`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), build_preprocessor. Anchor `else "passthrough",`

### A-M2

**Major. Blocking No. experimental-design. VERIFIED. OPEN.**

Vị trí yêu cầu đánh giá. PDF p11, §1.1.4; p25 §3.3; p33 Bảng 5.2; p34 §5.8.2, tuyên bố có Diversity/OOF và kết quả Voting không thuận lợi.

Bản thảo tuyên bố phân tích diversity và giữ kết quả Voting bất lợi, nhưng phần kết quả không trình bày bảng định lượng nào của base OOF, diversity hoặc Voting. Bảng paired correctness cuối RF/Stack không thay được diversity giữa các base learners dùng ở development. Gói có sẵn số liệu cần thiết nên đây là lỗ hổng trình bày bằng chứng, không phải thiếu thí nghiệm đã có.

Vì sao cần sửa. Không có các số này, người đọc không kiểm tra được vì sao LR/DT/RF được giữ, Voting bị loại, hoặc RQ3 đã được trả lời tới đâu. Điểm development và cấu hình final cũng khác nhau nên phải phân biệt trước khi so sánh.

Tiêu chí giải quyết. Thêm bảng development gọn cho các track 42/17 với RF, hard/soft Voting, Stacking, Macro-F1 và FP/FN; đưa một bảng base-diversity có double-fault/oracle kèm định nghĩa, mẫu số và nhãn mô tả. Ghi rõ đây là pooled OOF trên official TRAIN với cấu hình development, không là final test hoặc nhiều lần train độc lập. Kết luận chỉ là liên hệ mô tả; nếu không trình bày, thu hẹp tuyên bố đóng góp và mức trả lời RQ3 cho đúng.

Lộ trình DOCUMENT. RQ3 và báo cáo kết quả không thuận lợi là phần đáng kể của đóng góp đã nêu; thiếu bảng này là Major. Kết luận final hẹp về RF/Stack không bị phủ định nên không Blocking.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.3, PDF p25. Anchor `Diversity và voting được xem xét trong development`
- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.2, PDF p34. Anchor `Kết quả không thuận lợi của Voting`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), Bảng 5.2, PDF p33. Anchor `RQ3 & Diversity, OOF, voting, stacking`
- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features, random_forest row. Anchor `0.9503873654153012`
- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features, hard_voting_lrdtrf row. Anchor `0.9473245884056625`
- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features, soft_voting_lrdtrf row. Anchor `0.946758358270028`
- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features, stacking_lrdtrf row. Anchor `0.9514836270686644`
- [results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv), all_features, logistic_regression/random_forest row. Anchor `0.03081424196280391`

### A-M3

**Major. Blocking No. reproducibility. VERIFIED. OPEN.**

Vị trí yêu cầu đánh giá. PDF p35, §5.8.3, câu bản tái dựng full TRAIN chưa thực hiện; pp32-33 §5.5 chỉ mô tả artifact trên tập con.

Câu phủ định việc tái dựng full TRAIN chưa khớp các record P15 được cung cấp. Cả ba run_report báo mode full, 175.341 dòng, PASS, artifact mang nhãn RECONSTRUCTED_FULL_TRAIN và môi trường hiện tại. Đó là record từ máy tác giả, không phải byte model tôi đã kiểm tra. Chúng chưa xác nhận môi trường lịch sử, model gốc hoặc tái lập metric TEST. Phải sửa trạng thái mà vẫn giữ đúng những giới hạn ấy.

Vì sao cần sửa. Tái lập là một trụ của đóng góp. Gộp tình trạng không có model gốc với tình trạng chưa có bất kỳ tái dựng full TRAIN nào khiến người đọc đánh giá sai cả bằng chứng đã có lẫn phần còn thiếu.

Tiêu chí giải quyết. Thay phần trạng thái bằng ba lớp rõ ràng, kết quả/prediction lịch sử; các bản tái dựng full TRAIN được record P15 báo cáo trong môi trường hiện tại, không TEST; phần chưa xác minh gồm model bytes trong lần phản biện này, môi trường/model gốc và sự trùng khớp dự đoán khoa học. Chỉ dẫn cả ba run_report và acceptance scope, không tuyên bố tôi đã tải model hoặc xác thực end-to-end.

Lộ trình DOCUMENT. Bất nhất liên quan trực tiếp đến tính tái lập được dùng làm giá trị nghiên cứu nên Major, nhưng không sửa số liệu final và không ngăn giữ kết luận benchmark hẹp.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.3, PDF p35. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.5, PDF p33. Anchor `Các mô hình kiểm thử kỹ thuật được xây dựng trên tập con TRAIN`
- [results/reproducibility/p15_local_rf17_full_01/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf17_full_01/run_report.json), worker_checks.train_rows. Anchor `"train_rows": 175341`
- [results/reproducibility/p15_local_rf42_full_02/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf42_full_02/run_report.json), worker_checks.artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`
- [results/reproducibility/p15_local_stack_full_01/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_stack_full_01/run_report.json), worker_checks.no_test_evaluation. Anchor `"no_test_evaluation": true`
- [results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json), scope. Anchor `NOT original model or scientific TEST validation`

## Minor Comments

### A-m1

**Minor. Blocking No. writing-clarity. VERIFIED. OPEN.**

Vị trí. PDF p25, §3.4, bước 1 và bước 4 cùng câu các bước mô tả đúng trình tự.

Danh sách tuyến tính đọc cả TRAIN và TEST trước bước lựa chọn/freeze, trong khi văn bản xung quanh và phase8 nói development chỉ dùng TRAIN. Đây là mâu thuẫn trình bày về mốc mở TEST; nó không phải bằng chứng đã tuning TEST.

Ý nghĩa. Người đọc có thể hiểu sai ranh giới holdout dù các câu bảo vệ protocol khác đã đúng.

Tiêu chí giải quyết. Tách development chỉ đọc TRAIN, freeze, rồi final evaluation mới đọc TEST. Nếu §3.4 chỉ tóm tắt phase9 thì bỏ bước lựa chọn development khỏi chuỗi đó và ghi freeze là đầu vào đã có.

Lộ trình DOCUMENT. Sửa trình tự một đoạn là đủ, không có bằng chứng số liệu bị thay đổi; Minor và không Blocking.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.4, step 1, PDF p25. Anchor `Đọc hai tập TRAIN và TEST chính thức`
- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.4, step 4, PDF p25. Anchor `Lựa chọn và cố định cấu hình theo kết quả phát triển mô hình trên TRAIN`
- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.4, PDF p25. Anchor `Các bước này mô tả đúng trình tự triển khai.`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), load_train. Anchor `def load_train()`
- [results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json), official_test_loaded. Anchor `"official_test_loaded": false`

### A-m2

**Minor. Blocking No. statistical-rigor. VERIFIED. OPEN.**

Vị trí. PDF pp26,28, §3.5 và §4.3, mô tả paired bootstrap và Holm.

Mô tả hiện tại chưa nói bootstrap phân tầng theo nhãn, giữ cố định số Normal/Attack rồi lấy multinomial trên joint prediction patterns của các model, dùng percentile CI. Cũng chưa nêu rõ Holm chạy cho ba cặp model trong từng view, còn các CI theo metric là CI marginal chưa hiệu chỉnh đồng thời.

Ý nghĩa. Điều kiện cố định prevalence và family kiểm định xác định phạm vi bất định; một người đọc không nên phải tự suy ra từ code.

Tiêu chí giải quyết. Thêm các chi tiết trên cùng seed 20260928 vào Methods/chú thích. Giữ cảnh báo về phụ thuộc dòng, không biến CI thành repeated-training/session uncertainty hoặc CI đồng thời.

Lộ trình DOCUMENT. Chi tiết phương pháp còn thiếu có thể bổ sung trực tiếp từ nguồn và không thay kết luận CI hiện tại; Minor.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.5, PDF p26. Anchor `paired bootstrap 10\,000 lần lấy mẫu lại các dòng benchmark`
- [src/analysis/run_unsw_phase10_statistics.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/analysis/run_unsw_phase10_statistics.py), bootstrap_metric_arrays docstring. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- [src/analysis/run_unsw_phase10_statistics.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/analysis/run_unsw_phase10_statistics.py), percentile_ci. Anchor `np.nanpercentile(`
- [src/analysis/run_unsw_phase10_statistics.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/analysis/run_unsw_phase10_statistics.py), mcnemar_table. Anchor `for view in EVAL_VIEWS:`
- [results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json), bootstrap.random_seed. Anchor `"random_seed": 20260928`

### A-m3

**Minor. Blocking No. data-resource-quality. VERIFIED. OPEN.**

Vị trí. PDF p23 §2.5 và p32 §5.3, audit tập trung 8.541 cross-split overlap rows.

Audit có sẵn 84.049 dòng TRAIN nằm trong nhóm vector lặp và 229 nhóm vector có xung đột nhãn; TEST có 34.704 dòng trong nhóm vector lặp. Bản thảo chỉ định lượng cross-split overlap, dù row-stratified CV và suy luận điều kiện theo dòng là trọng tâm phương pháp. Nên công khai thêm các số within-split này. Chúng không tự xác định session trùng hoặc là lỗi nhãn thật.

Ý nghĩa. Các con số cho người đọc đánh giá vì sao OOF ở cấp dòng không chứng minh độc lập traffic và vì sao độ lớn n không bằng số phiên độc lập.

Tiêu chí giải quyết. Bổ sung bảng audit nhỏ, phân biệt rows_inside_duplicate_groups, extra_duplicate_rows và unique groups, ghi định nghĩa 42 predictors và label-conflict. Không gán nhân quả cho khoảng cách CV/TEST; grouped evaluation mới thuộc thí nghiệm tương lai.

Lộ trình DOCUMENT. Phụ thuộc dòng đã được công khai và kết luận hiện tại được giới hạn, nên thiếu định lượng bổ sung này là Minor.

- [report/chapters/dataset_eda.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/dataset_eda.tex), §2.5, PDF p23. Anchor `Có 8\,541 dòng official TEST trùng vector`
- [results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json), within_train.rows_inside_duplicate_groups. Anchor `"rows_inside_duplicate_groups": 84049`
- [results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json), within_train.label_conflict_groups. Anchor `"label_conflict_groups": 229`
- [results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json), within_test.rows_inside_duplicate_groups. Anchor `"rows_inside_duplicate_groups": 34704`

### A-m4

**Minor. Blocking No. figures-and-tables. VERIFIED. OPEN.**

Vị trí. PDF p29, Bảng 4.3, Inference ms/mẫu; p30 §4.4.

Giá trị ms/mẫu là tổng thời gian predict_proba và tạo nhãn cho batch TEST chia cho 82.332, gồm preprocessing theo pipeline. Nó không phải phép đo request đơn, p95 latency hoặc throughput streaming. Bản thảo đã tránh dự báo triển khai nhưng nhãn bảng vẫn nên nói rõ cách lấy trung bình.

Ý nghĩa. Khái niệm latency ở cấp request khác phép chia thời gian batch; nhãn rõ giúp tránh sử dụng nhầm số đo lịch sử.

Tiêu chí giải quyết. Đổi nhãn/chú thích thành thời gian suy luận trung bình quy đổi trên batch TEST, nêu batch size và phạm vi timer. Không cần benchmark lại khi chỉ giữ số đo lịch sử.

Lộ trình DOCUMENT. Đây là cách ghi nhãn số đo có sẵn; không ảnh hưởng thứ hạng hoặc kết luận hẹp nên Minor.

- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), main, inference timing. Anchor `predict_start = (`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), main, prediction batch. Anchor `model.predict_proba(`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), main, amortized per-row time. Anchor `/ len(test)`
- [report/chapters/results_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/results_discussion.tex), Bảng 4.3, PDF p29. Anchor `Inference (ms/mẫu)`

## Tuyên bố chưa được nguồn hỗ trợ và ranh giới kết luận

### bản tái dựng full TRAIN chưa thực hiện

PDF p35, §5.8.3. Không còn phù hợp với mức record P15 được cung cấp; đối chiếu A-M3. Record không nâng thành xác nhận model bytes, model gốc hoặc scientific TEST reproduction.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.3. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- [results/reproducibility/p15_local_stack_full_01/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_stack_full_01/run_report.json), worker_checks.artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`

### Các bước này mô tả đúng trình tự triển khai.

PDF p25, §3.4. Không nhất quán nếu đọc danh sách như thời gian thực của toàn nghiên cứu; đối chiếu A-m1. Không suy ra TEST tuning từ lỗi trình bày này.

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.4. Anchor `Các bước này mô tả đúng trình tự triển khai.`

### Các mở rộng như ensemble superiority ổn định, hiệu ứng riêng Feature Selection, external/unknown-attack deployment hoặc thống kê tương đương

PDF pp32-35, §§5.3-5.8. Chưa được thiết kế hiện tại xác lập, nhưng bản thảo hiện chủ động không khẳng định chúng. Đây là ranh giới bằng chứng, không tính thành overclaim thực tế hay concern riêng.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.1. Anchor `cũng không chứng minh hai mô hình tương đương về mặt thống kê.`
- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.4. Anchor `không phải một cam kết superiority, novelty hoặc deployment chưa được kiểm chứng.`

## Sửa bằng tài liệu và diễn giải

- A-M1. Mở rộng Methods bằng lineage stable17, preprocessing và bảng selection/CV; dùng đúng source/config đóng băng, ghi rõ RFECV riêng và các bước không nested. Không cần train.

- A-M2. Đưa kết quả development OOF/Voting/diversity đã lưu vào Results hoặc phụ lục có dẫn rõ; chỉ mô tả liên hệ và negative result. Không cần train.

- A-M3. Đồng bộ trạng thái P15 theo mức record máy tác giả, tách historical original và reconstructed full TRAIN trong môi trường hiện tại. Không cần train.

- A-m1, A-m2, A-m3, A-m4. Sửa thứ tự mở TEST; mô tả bootstrap/family kiểm định; định lượng within-split audit; nhãn thời gian batch. Không cần train.

## Thí nghiệm mới nếu muốn mở rộng kết luận

Các mục này không là điều kiện để giữ kết luận benchmark hẹp hiện tại. Chúng cần phê duyệt protocol mới và không được dùng TEST đã xem để chọn lại model, feature hoặc threshold.

### A-E1

Muốn trả lời hiệu ứng riêng của Feature Selection và ước lượng generalization của cả quy trình chọn feature.

Một protocol mới được duyệt, lồng toàn bộ selector và preprocessing trong outer training fold, giữ RF hyperparameters/seed/compute matched giữa tập feature. Không retune official TEST hiện tại.

- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.3, PDF p32. Anchor `Một thí nghiệm ablation chuẩn để tách nguyên nhân phải giữ các tham số còn lại cố định`

### A-E2

Muốn kết luận stable ensemble gain hoặc đo lựa chọn/huấn luyện thay vì chỉ dòng benchmark.

Nhiều fit độc lập với môi trường được khóa và đơn vị độc lập được định nghĩa, repeated full-pipeline model selection hoặc nested evaluation đúng mục tiêu; không coi fold hay bootstrap draw là independent repetition.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.3, PDF p34. Anchor `cần một nghiên cứu mới có nhiều lần huấn luyện độc lập`

### A-E3

Muốn kết luận robustness theo thời gian, host/session hoặc traffic bên ngoài.

Thiết kế trước group/temporal hoặc external test có metadata và quyền truy cập thích hợp. Novel-vector 42D của cùng TEST không thay phép này, cũng không đảm bảo vector 17D của RF-17 là mới.

- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.6, PDF p33. Anchor `Novel-vector view là tập con của chính official TEST`

### A-E4

Muốn gán gain cho complementarity hoặc so sánh hiệu ứng xử lý mất cân bằng.

Ablation base membership và matched class-weight/resampling bên trong training folds với protocol mới, đóng băng trước đánh giá. Dùng diversity/threshold sweep hiện có như dữ liệu phát triển, không biến nó thành bằng chứng nhân quả.

- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), Bảng 5.2, PDF p33. Anchor `Chưa có matched controlled resampling`
- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.3. Anchor `không được dựa vào official TEST hiện tại để chọn phương án thắng.`

### A-E5

Muốn chứng nhận tái lập hiệu năng từ model bytes hoặc đưa ra số đo vận hành.

Một gói tái lập/model evaluation được duyệt riêng, xác minh artifact thực, môi trường và inference; nếu đo latency cần batch/request definition, warm-up và lặp phù hợp. Không dùng P15 TRAIN roundtrip để xác nhận khoa học TEST.

- [results/reproducibility/p15_local_rf42_full_02/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf42_full_02/run_report.json), worker_checks.eval. Anchor `TRAIN-derived sample for roundtrip ONLY; no generalization metric`
- [results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json), scope. Anchor `NOT original model or scientific TEST validation`

## Câu hỏi bảo vệ chuyên sâu

### A-Q01

Hãy tái dựng chính xác lineage của stable17. Vì sao quy tắc ít nhất 3/5 lần trong ít nhất 2/3 phương pháp tạo 17 biến, và tập đó khác RFECV 13 biến ở đâu? Vì sao không thể gọi 5 stability seed là 5 lần xác nhận generalization độc lập?

- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), configuration. Anchor `SEEDS = [11, 23, 42, 71, 101]`
- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), configuration. Anchor `STABILITY_MIN_FREQUENCY = 0.60`
- [results/feature_selection/unsw_nb15/stage2/rfecv_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/feature_selection/unsw_nb15/stage2/rfecv_metadata.json), feature count. Anchor `"selected_original_feature_count": 13`

### A-Q02

Với một outer validation fold cụ thể, thao tác nào đã thấy nhãn của fold đó trước khi fit model? Vì sao fit preprocessing trong Pipeline không chữa được selection stable17 trước CV hoặc preprocessing fit trước RFECV nội bộ?

- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.2. Anchor `toàn bộ official TRAIN trước development cross-validation`
- [src/features/select_unsw_features_stage2.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/features/select_unsw_features_stage2.py), run_rfecv. Anchor `X = prep.fit_transform(sample[candidate_features])`

### A-Q03

Đường đi một dòng TRAIN qua base OOF, meta-CV và refit final khác nhau như thế nào? RF hyperparameters được tuning trên toàn TRAIN trước tạo OOF và tái dùng ma trận OOF qua meta-CV gây vấn đề gì cho diễn giải điểm development?

- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), generate_meta_features. Anchor `tuned_rf_params: dict,`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), generate_meta_features. Anchor `prob = cross_val_predict(`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), tune_meta_learner. Anchor `X_meta = meta_features[`

### A-Q04

Phase8 tạo base OOF với seed 42, meta CV với seed 271, còn final inner stacking dùng seed 137. Hãy phân biệt vai trò từng phép chia, giải thích vì sao dùng cùng số fold không làm các ma trận meta giống nhau hoặc tạo fully nested estimate.

- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), generate_meta_features. Anchor `random_state=RANDOM_STATE,`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), tune_meta_learner. Anchor `random_state=271,`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_stacking_42. Anchor `STACKING_INNER_RANDOM_STATE`

### A-Q05

Vì sao LR dùng StandardScaler còn cây dùng numeric passthrough? Với one-hot handle_unknown=ignore, một giá trị proto/service/state chỉ có trong validation được biểu diễn thế nào và giới hạn thông tin là gì? Tệp nào ghi đúng thứ tự predictors?

- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_ohe. Anchor `handle_unknown="ignore",`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_lr_pipeline. Anchor `scale_numeric=True,`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_dt_pipeline. Anchor `scale_numeric=False,`
- [results/reproducibility/p15_local_rf17_full_01/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf17_full_01/run_report.json), worker_checks. Anchor `"ordered_features": [`

### A-Q06

max_features=0.5 được áp dụng vào 42/17 cột gốc hay số cột sau one-hot của Pipeline? Tại sao điều này làm cách kể giảm từ 42 xuống 17 không tương đương một mức giảm tuyến tính về số biến được xét ở mỗi split?

- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), build_preprocessor. Anchor `return ColumnTransformer(`
- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), RF hyperparameters. Anchor `"max_features": 0.5`
- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_rf_pipeline. Anchor `RandomForestClassifier(`

### A-Q07

RF-42 thắng grid theo Macro-F1 ở leaf=1/300 cây, nhưng ứng viên leaf=2/300 có điểm rất gần. Vì sao không nên dùng SD ba fold như CI của hiệu ứng hoặc tự chuyển sang cấu hình có lợi hơn sau khi nhìn TEST?

- [results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv), rank 1. Anchor `0.953325289089792`
- [results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv), rank 2. Anchor `0.9532882892245934`
- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), tune_random_forest. Anchor `refit="macro_f1",`

### A-Q08

Những số cụ thể nào chứng minh Voting không thuận lợi ở development và chúng có được tính với đúng cấu hình RF final hay không? Hãy giải thích vì sao không trộn pooled OOF development với official holdout để tuyên bố một model duy nhất đã cải thiện từ 0,95 xuống/so với 0,86.

- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features hard voting. Anchor `0.9473245884056625`
- [results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv), all_features random forest. Anchor `0.9503873654153012`
- [results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv), random_forest_42 official_test. Anchor `0.863343473727991`

### A-Q09

Double-fault thấp hoặc oracle cao giữa hai base learners cho biết điều gì và không cho biết điều gì về năng lực meta learner? Đối chứng nào mới phân biệt được đóng góp thật của một base với tín hiệu đa dạng chỉ mang tính mô tả?

- [results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv), header. Anchor `double_fault_rate,pairwise_oracle_accuracy`
- [results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv), all_features LR/RF. Anchor `0.03081424196280391`

### A-Q10

RF-17 giảm số cây từ 300 xuống 150 và tăng leaf từ 1 lên 2. Từ tỷ lệ thời gian 6,48, kết luận tối đa nào được phép phát biểu? Hãy đề xuất matched/nested ablation mới để tách feature-count, độ phức tạp cây và tương tác giữa chúng.

- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), random_forest_42.hyperparameters. Anchor `"n_estimators": 300`
- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), random_forest_17.hyperparameters. Anchor `"min_samples_leaf": 2`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.3. Anchor `lợi ích quan sát được có thể do cả số cây, kích thước lá, số feature`

### A-Q11

Attack là đa số trong TRAIN nhưng từng attack family có support rất chênh lệch. class_weight=balanced ở binary meta learner cân bằng cái gì? Vì sao so sánh meta-weight trong grid không xác lập hiệu quả SMOTE hoặc khả năng phát hiện từng họ tấn công hiếm?

- [src/models/run_unsw_phase8_controlled_tuning.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase8_controlled_tuning.py), meta_param_grid. Anchor `"class_weight": [None, "balanced"]`
- [results/eda/unsw_nb15/tables/binary_class_distribution.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/eda/unsw_nb15/tables/binary_class_distribution.csv), header. Anchor `split,label_name,count,percentage`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), Bảng 5.2. Anchor `Chưa có matched controlled resampling`

### A-Q12

Threshold 0,5 được giữ vì protocol nào, và sweep chẩn đoán trên TRAIN có thể được dùng đến đâu? Tại sao giảm 142 FP nhưng tăng 118 FN chưa đủ để chọn Stacking cho vận hành khi chưa có utility và prevalence triển khai?

- [results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json), threshold_policy. Anchor `Threshold sweep is diagnostic only.`
- [results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv), RF-42 official_test. Anchor `random_forest_42,official_test,26997,10003,734,44598,37000,45332,82332`
- [results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv), Stacking-42 official_test. Anchor `stacking_42,official_test,27139,9861,852,44480,37000,45332,82332`

### A-Q13

Bootstrap hiện giữ cố định n Normal và n Attack, đồng thời giữ pairing bằng joint prediction patterns. Điều gì sẽ khác ở estimand nếu cho prevalence biến động? Vì sao 10.000 draw không là 10.000 phép train hoặc 10.000 mạng độc lập?

- [src/analysis/run_unsw_phase10_statistics.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/analysis/run_unsw_phase10_statistics.py), bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- [results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json), bootstrap. Anchor `"replicates": 10000`

### A-Q14

84.049 dòng TRAIN trong nhóm vector lặp và 229 nhóm vector xung đột nhãn ảnh hưởng thế nào đến cách đánh giá row-level OOF? Vì sao không được đồng nhất vector trùng với session trùng hoặc khẳng định chúng gây toàn bộ khoảng cách CV/TEST?

- [results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json), within_train. Anchor `"rows_inside_duplicate_groups": 84049`
- [results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json), within_train. Anchor `"label_conflict_groups": 229`
- [report/chapters/dataset_eda.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/dataset_eda.tex), §2.5. Anchor `không được tuyên bố mọi trường hợp trùng vector đều là leakage cùng phiên.`

### A-Q15

Novel-vector được định nghĩa ở 42D, còn RF-17 chỉ nhận 17D. Tập này có loại trừ mọi vector 17D từng thấy không, và vì sao kết quả trên nó vẫn chưa trả lời temporal/day/session robustness hoặc cross-dataset generalization?

- [results/data_audit/unsw_nb15_views/view_summary.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/data_audit/unsw_nb15_views/view_summary.json), dimension. Anchor `"feature_vector_column_count": 42`
- [results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json), random_forest_17.feature_track. Anchor `"feature_track": "stable_17_features"`
- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.6. Anchor `Novel-vector view là tập con của chính official TEST`

### A-Q16

Phân biệt ba bằng chứng model lịch sử, record tái dựng full TRAIN P15 và một model artifact mà reviewer thực sự tải/kiểm tra. Những record P15 đã đủ cho kết luận nào, còn điều gì vẫn thiếu để tái lập metric official TEST hoặc xác nhận môi trường gốc?

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.3. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- [results/reproducibility/p15_local_rf42_full_02/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf42_full_02/run_report.json), worker_checks.eval. Anchor `TRAIN-derived sample for roundtrip ONLY; no generalization metric`
- [results/reproducibility/p15_local_rf42_full_02/run_report.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/reproducibility/p15_local_rf42_full_02/run_report.json), worker_checks.artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`

## Đánh giá năm tiêu chí chung

### originality

Đóng góp là kiểm toán và trình bày một case study, không phải thuật toán mới. Chính bản thảo xác nhận các thành phần ensemble/FS đã tồn tại. Phạm vi tài liệu được cung cấp không cho phép kết luận độc đáo toàn ngành.

- [report/chapters/introduction.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/introduction.tex), §1.1.4, PDF p11. Anchor `không đủ cơ sở để khẳng định một thuật toán Ensemble Learning mới`
- [literature_scope.json](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/literature_scope.json), record L08, sections_read. Anchor `Publisher abstract and access notice only; no new Methods/results full-text reading`

### scientific_importance

Có ích ở cấp thực nghiệm và đào tạo về protocol, loại lỗi và giới hạn inference. Chưa có bằng chứng cho tầm quan trọng khoa học rộng hoặc lợi ích vận hành vượt benchmark.

- [report/chapters/conclusion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/conclusion.tex), §5.8.4, PDF p35. Anchor `Việc bổ sung Stacking đem lại một đánh đổi FP/FN cụ thể nhưng không xác lập ưu thế tổng thể trước RF-42.`

### technical_soundness

Các kết luận final hẹp nhất quán với confusion matrices và paired CI. Thiết kế development còn FS trước CV và meta tuning không fully nested. Vấn đề cần sửa ngay là trình bày đủ selection path, đưa số liệu development lên bản thảo và sửa trạng thái tái dựng; những giới hạn đã nêu không được tự biến thành cáo buộc tuning TEST.

- [src/models/run_unsw_phase9_final_holdout.py](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/src/models/run_unsw_phase9_final_holdout.py), make_stacking_42. Anchor `stack_method="predict_proba"`
- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.2, PDF p24. Anchor `toàn bộ official TRAIN trước development cross-validation`
- [results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv), official_test, stacking_42 minus random_forest_42, macro_f1. Anchor `0.0004966898940774733,0.95,-0.0003118042125941106,0.0013089503250197615`

### interdisciplinary_readership

Bài học về leakage, số đo chi phí và đánh đổi lỗi có thể hữu ích cho cộng đồng reproducible ML ngoài IDS. Kết quả vẫn là một benchmark và chưa có quy đổi sang utility hoặc dữ liệu vận hành độc lập.

- [report/chapters/validity_discussion.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/validity_discussion.tex), §5.1, PDF p31. Anchor `nghiên cứu không đo chi phí thực tế nên chỉ mô tả đánh đổi`

### readability_for_nonspecialists

Phần giải thích FP/FN, Macro-F1/MCC, OOF và các giới hạn khá rõ; bảng 4.1, 4.2 và hình 4.1, 4.2 dễ theo dõi khi kiểm tra PDF. Tuy vậy, Methods ngắn đến mức người đọc phải tự dựng lại quá trình chọn mô hình từ mã nguồn; nhiều nhãn tiếng Anh được giữ nguyên và chưa có bảng development giúp nối lý thuyết với kết quả.

- [report/chapters/theoretical_foundations.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/theoretical_foundations.tex), §1.2.4.2, PDF pp14-15. Anchor `Out-of-fold`
- [report/chapters/methodology.tex](C:/Users/admin/Documents/ChatGPT/NCKH/defense/p20_pre_2026_10_17_01/packet_02/local_contents/report/chapters/methodology.tex), §3.2, PDF p24. Anchor `Track 17 feature ổn định lấy từ danh sách đã lưu của official TRAIN`

## Kiểm tra phạm vi kỹ thuật

Đã cân nhắc đủ 12 trục kỹ thuật. Clinical validity không áp dụng; ethical governance không thể đánh giá đầy đủ từ gói giới hạn và không được mặc định có vi phạm. Các trục khác áp dụng với nhận xét cụ thể trong report.json. Không dùng taxonomy để đặt quota concern.

## Khuyến nghị có điều kiện

MAJOR_REVISION_REQUIRED cho bản thảo hiện tại. Có thể xem xét ACCEPTABLE_WITH_LIMITATIONS trong phạm vi case study sau khi hoàn thành các sửa tài liệu có tiêu chí dưới đây và kiểm tra lại tính nhất quán. Không cấp P20 final closure; không bắt buộc mở lại TEST hoặc làm thí nghiệm mới để giữ kết luận hẹp hiện có.

Các vấn đề kỹ thuật cần giải quyết trước khi bảo vệ đầy đủ đóng góp kiểm toán là A-M1, A-M2 và A-M3. Không yêu cầu huấn luyện mới để sửa các vấn đề này. Không có Major nào được gắn Blocking cho kết luận final hẹp hiện tại.

## Skill thực sự đã đọc

- [nature-reviewer](C:/Users/admin/.codex/skills/nature-reviewer/SKILL.md). Chỉ hướng dẫn đánh giá, không là bằng chứng manuscript. Tham chiếu đã đọc gồm references/reviewer-workflow.md, references/technical-concern-taxonomy.md, references/domain-specific-review-gates.md (Engineering và shared gate pattern), references/qa-checklist.md, references/review-axes.md.

- [nature-statistics](C:/Users/admin/.codex/skills/nature-statistics/SKILL.md). Chỉ hướng dẫn statistical reporting; không thực hiện reanalysis. Tham chiếu đã đọc gồm references/statistical-reporting.md, references/common-failure-modes.md, references/reviewer-checklist.md.

- [pdf:pdf](C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md). Đọc PDF và kiểm tra trực quan trong bộ nhớ, không tạo/sửa PDF. Tham chiếu đã đọc gồm không có tham chiếu phụ.



Báo cáo được hoàn thiện trong context riêng, không tham khảo kết quả của người phản biện khác. Không tuyên bố xác nhận người thật, quyết định biên tập hoặc P20 final acceptance.
