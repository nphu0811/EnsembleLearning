# Phản biện B cho P20-PRE

Phản biện khoa học nội bộ do AI mô phỏng cho P20-PRE, không phải hội đồng người thật, quyết định biên tập hay nghiệm thu P20.

## Phạm vi và xác minh đầu vào

Thống kê và đánh giá IDS.

Chỉ COMMON_REVIEW_RULES.md, BRIEF_B.md, packet_02/manifest.csv, receipt.json, packet_02/local_contents và hướng dẫn kỹ năng đã đọc.

approved_report.pdf, 37 trang vật lý. Đã đọc toàn bộ bản trích trang 1-37 và các chương hoạt động do report/main.tex xác định. Đã xem trực quan trang vật lý 27-30, 33 và 35. Không dùng chương ngoài active inputs để suy ra tuyên bố.

Lời gọi phản biện riêng. Không đọc báo cáo, brief hay ledger của phản biện khác, bộ nhớ nghiên cứu, QA trước hoặc tổng hợp. Đây là ranh giới truy cập theo hợp đồng trên hệ tệp chung, không phải cách ly hệ điều hành hoặc xác nhận độc lập bởi con người.

Không internet, không mở dữ liệu thô hoặc CSV dự đoán từng dòng, không nạp model, không thực thi/import mã ML, không train hoặc bootstrap, không sửa packet.

P15 chỉ là bản ghi phía tác giả. Không có model bytes để xác minh trực tiếp. Ghi chú tài liệu là nguồn thứ cấp có phạm vi đọc hạn chế, không phải toàn văn và không đủ thiết lập novelty toàn lĩnh vực.

Manifest SHA256 `c0f0b3828ba16ce8312b489915cc4c56c9fc7c771dbeefe1d7a9bb78938b62b7`. Đã kiểm tra 80/80 tệp, không có mismatch. PDF SHA256 `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`.

Tính số học thuần từ sáu hàng confusion summary bằng thư viện chuẩn. Macro-F1, weighted F1, MCC, FPR, FNR, Accuracy, Attack Recall và Balanced Accuracy khớp bảng P11, sai khác tối đa quan sát 0.0. Cộng số mẫu/FN của chín attack families khớp cả ba pipeline và hai view. Không tính lại AUC từ dữ liệu dòng và không chạy lại kiểm định hay bootstrap.

## Đánh giá khoa học tổng thể

Kết luận khoa học cốt lõi có thể bảo vệ như một case study nhị phân có kiểm toán. Stacking đổi 142 FP lấy thêm 118 FN; Macro-F1 nhỉnh hơn 0.000497 nhưng MCC thấp hơn 0.000413. CI của cả hai hiệu số tổng thể chứa 0 và bản thảo đã đúng khi không khẳng định superiority hoặc equivalence. Giá trị chính nằm ở việc trình bày loại lỗi, ranh giới suy luận và kết quả không thuận lợi, chưa phải thuật toán mới hoặc hệ thống IDS đã triển khai.

Cần sửa lớn về sự đầy đủ và nhất quán của báo cáo, không vì bảng hiệu năng chính có lỗi số học. Hai Major đều không chặn riêng kết luận hẹp về đánh đổi FP/FN nhưng làm yếu đáng kể đóng góp về kiểm toán và khả năng tự kiểm chứng của báo cáo.

Người nghiên cứu IDS và ML trên dữ liệu bảng, người xây dựng benchmark, sinh viên thực nghiệm và nhóm quan tâm tái lập sẽ quan tâm. Bài học về metric gộp che đánh đổi có thể hữu ích ngoài IDS, nhưng bằng chứng hiện tại chưa chứng minh tầm quan trọng rộng hoặc tác dụng vận hành.

- `report/chapters/conclusion.tex`, §5.8.1, PDF vật lý 34. Anchor `không xác nhận ưu thế tổng thể`
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, official_test, RF-42 và Stacking-42. Anchor `stacking_42,official_test,27139,9861,852,44480,37000,45332,82332`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`, official_test, stacking_42 trừ random_forest_42, Macro-F1. Anchor `official_test,stacking_42,random_forest_42,macro_f1,0.0004966898940774733,0.95,-0.0003118042125941106,0.0013089503250197615,False,10000`

## Điểm mạnh có bằng chứng

### B-S1

Bảng cuối có đủ số lỗi và mẫu số để kiểm tra độc lập. RF-42 có 10003/37000 FP và 734/45332 FN; Stacking có 9861/37000 FP và 852/45332 FN. Macro-F1 là trung bình F1 hai lớp, weighted F1 dùng support. Kiểm tra số học của sáu hàng P11 khớp hoàn toàn.

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, official_test, RF-42. Anchor `random_forest_42,official_test,26997,10003,734,44598,37000,45332,82332`
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`, official_test, RF-42, phần macro/weighted. Anchor `0.863343473727991,0.8662999857580319`
- `report/chapters/theoretical_foundations.tex`, §1.2.6.1, PDF vật lý 16. Anchor `Weighted-F1 lấy trung bình theo support.`

### B-S2

Diễn giải suy luận cặp được tiết chế đúng. CI Macro-F1/MCC chứa 0 không được gọi là superiority hoặc equivalence; McNemar không bị trình bày thành kiểm định Macro-F1.

- `report/chapters/results_discussion.tex`, §4.3, PDF vật lý 28. Anchor `chứng minh hai mô hình tương đương thống kê`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`, official_test, Stacking-42/RF-42. Anchor `491,515,1006,0.46837651914684564,0.46837651914684564,False,paired overall correctness / error rate`

### B-S3

Báo cáo phân biệt đúng tính độc lập của đơn vị lấy mẫu, độ biến thiên train và novel-vector sensitivity. Không gọi 73791 dòng còn lại là external test hoặc quy 8541 overlap rows thành session leakage.

- `report/chapters/dataset_eda.tex`, §2.5, PDF vật lý 23. Anchor `không nhất thiết là số vector riêng biệt hay số session bị giao cắt`
- `report/chapters/validity_discussion.tex`, §5.4, PDF vật lý 32. Anchor `Một phép bootstrap trên dòng không tái tạo sự ngẫu nhiên của quá trình tối ưu mô hình.`

### B-S4

FS trước development CV, meta tuning chưa fully nested, confounding giữa RF-17/RF-42 và tính hậu nghiệm của error analysis đều được công khai. Đây là ranh giới hợp lệ của case study, không phải lý do mặc định bác bỏ counts TEST đã khóa.

- `report/chapters/methodology.tex`, §3.2, PDF vật lý 24. Anchor `trước development cross-validation`
- `report/chapters/validity_discussion.tex`, §5.3, PDF vật lý 32. Anchor `RF-17 dùng 150 trees`
- `report/chapters/results_discussion.tex`, §4.5, PDF vật lý 30. Anchor `Tất cả phân tích lỗi được thực hiện hậu nghiệm`

### B-S5

Bản thảo không dùng các điểm số của prior work dưới split khác để xếp hạng trực tiếp. Phạm vi đọc và thiếu toàn văn trong catalog được giữ rõ, cho phép đánh giá novelty thận trọng.

- `report/chapters/related_work.tex`, §1.3.1, PDF vật lý 17. Anchor `không được coi là baseline matched`
- `literature_scope.json`, L08, sections_read. Anchor `Publisher abstract and access notice only; no new Methods/results full-text reading`

## Major Concerns

### B-M1

Severity MAJOR. Blocking No. Axis `reproducibility`. Issue key `reconstruction-status-mismatch`. Evidence status `PARTIAL`. Status OPEN. Route `DOCUMENT`.

Phần được nhận xét. PDF vật lý 35, §5.8.3 nói bản tái dựng full TRAIN chưa thực hiện; §5.5 ở trang 33 chỉ bàn các mô hình kiểm thử trên tập con.

Trạng thái tái dựng trong bản thảo chưa khớp hồ sơ cung cấp. Cả ba run report tự ghi mode full, 175341 TRAIN rows, artifact hash và kiểm tra roundtrip; acceptance ghi passed. Đây là bằng chứng rằng phía tác giả có bản ghi tái dựng toàn TRAIN, khác với câu phủ định tuyệt đối trong kết luận. Tôi chỉ xác minh nội dung bản ghi, không xác minh model bytes, tính trung thực độc lập của lần chạy hay hiệu năng TEST.

Ý nghĩa. Đóng góp về kiểm toán cần phân biệt bốn mức bằng chứng. Kết quả lịch sử, mô hình lịch sử chưa được xác minh, tái dựng địa phương theo bản ghi, và tái đánh giá khoa học TEST là những trạng thái khác nhau. Câu hiện tại vừa bỏ sót tiến triển có hồ sơ, vừa khiến người đọc khó hiểu giới hạn thật của tái lập.

Điều kiện đóng. Sửa §3.6, §5.5 và §5.8.3 thành một bảng trạng thái nhất quán. Ghi ba bản ghi tái dựng full TRAIN và môi trường của chúng, đồng thời ghi model bytes không nằm trong packet, original environment chưa được thiết lập và chưa có xác nhận hiệu năng TEST của các bản tái dựng. Không thay chi phí P9 bằng timing P15 và không gọi các kiểm tra roundtrip là end-to-end scientific reproduction.

Lý do mức độ. Major không blocking vì trạng thái tái lập là phần quan trọng của đóng góp kiểm toán, nhưng sai lệch mô tả này không làm sai counts và hiệu số TEST lịch sử.

- `report/chapters/conclusion.tex`, §5.8.3, PDF vật lý 35. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- `results/reproducibility/p15_local_rf17_full_01/run_report.json`, worker_checks.train_rows và artifact.scope. Anchor `"train_rows": 175341`
- `results/reproducibility/p15_local_rf42_full_02/run_report.json`, worker_checks.artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks.eval và no_test_evaluation. Anchor `TRAIN-derived sample for roundtrip ONLY; no generalization metric`
- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`, scope. Anchor `P15_LOCAL_ARTIFACT_READONLY_QA; NOT original model or scientific TEST validation`

### B-M2

Severity MAJOR. Blocking No. Axis `figures-and-tables`. Issue key `development-evidence-not-presented`. Evidence status `VERIFIED`. Status OPEN. Route `DOCUMENT`.

Phần được nhận xét. PDF vật lý 11, §1.1.4 và trang 34, §5.8.2 coi Diversity/OOF và kết quả Voting không thuận lợi là đóng góp đã có; Bảng 5.2 ghi RQ3 có Diversity, OOF, voting, stacking.

Bản báo cáo đã đọc không trình bày bảng định lượng development CV của LR/DT/RF, hard/soft voting và stacking, cũng không có các giá trị diversity/OOF. Chương 4 chỉ có ba pipeline cuối, CI, cost, attack-family và novel-vector; Bảng 5.2 chỉ nêu tên bằng chứng. Vì vậy người đọc bản báo cáo không tự kiểm tra được phần đóng góp RQ3 và câu kết quả Voting không bị loại, dù packet thực sự có các bảng đó. Đây là thiếu trình bày bằng chứng, không phải kết luận rằng thí nghiệm chưa tồn tại.

Ý nghĩa. Mạch từ base learner, complementary errors tới lựa chọn stacking là thành phần chính của đề tài. Việc chỉ nói Voting không thuận lợi không cho thấy bất lợi lớn bao nhiêu, có đúng dưới cùng track/folds hay không và có liên hệ mô tả gì với diversity.

Điều kiện đóng. Thêm bảng/phụ lục truy vết từ các bảng đóng băng. Nêu số fold, mean và SD mô tả giữa fold, phân biệt pooled OOF với mean fold, giữ cả hai track và các phương án không thuận lợi. Chỉ rõ đây là development, có selection bias đã biết, không phải ba lần train độc lập hay causal proof của diversity. Tóm tắt ít nhất các số Voting/RF/Stacking và một cặp diversity tại đoạn kết luận RQ3, không chọn lại mô hình theo TEST.

Lý do mức độ. Major không blocking vì thiếu bằng chứng định lượng cho một đóng góp quan trọng trong báo cáo độc lập; bảng frozen đã có nên có thể sửa tài liệu mà không huấn luyện mới, và kết luận hẹp về FP/FN cuối vẫn đứng.

- `report/chapters/introduction.tex`, §1.1.4, PDF vật lý 11. Anchor `kèm Diversity/OOF và cả kết quả Voting không thuận lợi`
- `report/chapters/conclusion.tex`, §5.8.2, PDF vật lý 34. Anchor `không bị loại vì không hỗ trợ một giả thuyết chiến thắng`
- `report/chapters/validity_discussion.tex`, Bảng 5.2, PDF vật lý 33. Anchor `RQ3 & Diversity, OOF, voting, stacking`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, all_features, hard_voting_lrdtrf, macro_f1_mean. Anchor `0.9473237829097595`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, all_features, soft_voting_lrdtrf, macro_f1_mean. Anchor `0.9467575146807178`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, all_features, random_forest, macro_f1_mean. Anchor `0.9503875354115768`
- `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, all_features, LR/DT, n_both_wrong và double_fault_rate. Anchor `all_features,logistic_regression,decision_tree,158508,4267,5425,7141`

## Minor Comments

### B-m1

Severity MINOR. Blocking No. Axis `statistical-rigor`. Issue key `bootstrap-estimand-and-multiplicity-reporting`. Evidence status `VERIFIED`. Status OPEN. Route `DOCUMENT`.

Phần được nhận xét. PDF vật lý 16, §1.2.6.2; trang 26, §3.5; trang 28, Bảng 4.2 và đoạn McNemar chỉ nói bootstrap dòng và Holm.

Mô tả thống kê chưa nêu bootstrap là phân tầng Normal/Attack, giữ cố định tổng từng lớp và lấy multinomial trên joint prediction patterns, với CI percentile. Holm được tính trên ba cặp model riêng trong mỗi view. CI của các metric là các khoảng điểm 95%, không có bằng chứng chúng đã được điều chỉnh đồng thời bằng Holm. Không thấy bản thảo kết luận thắng tổng thể từ nhiều phép thử, nên đây là thiếu chi tiết báo cáo, không phải cáo buộc sai kiểm định.

Ý nghĩa. Giữ cố định class totals thay đổi estimand so với bootstrap không phân tầng cho prevalence thay đổi. Không ghi họ so sánh có thể khiến độc giả hiểu nhầm Holm áp dụng cho mọi metric và mọi view.

Điều kiện đóng. Bổ sung một đoạn phương pháp ghi strata, n Normal/Attack theo view, shared joint resampling, percentile 2.5/97.5, seed 20260928, 10000 draws; ghi rõ Holm cho ba cặp trong từng view và CI pointwise. Giữ giới hạn row dependence; không cần chạy lại phân tích cho kết luận mô tả hiện tại.

Lý do mức độ. Minor vì thuật toán, pairing và giới hạn chính đã kiểm tra được trong nguồn, còn thiếu chi tiết có thể bổ sung cục bộ mà không đổi kết luận.

- `report/chapters/theoretical_foundations.tex`, §1.2.6.2, PDF vật lý 16. Anchor `Paired bootstrap lấy mẫu lại chỉ số dòng`
- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- `src/analysis/run_unsw_phase10_statistics.py`, percentile_ci. Anchor `np.nanpercentile(`
- `src/analysis/run_unsw_phase10_statistics.py`, mcnemar_table, vòng lặp view trước Holm. Anchor `for view in EVAL_VIEWS:`
- `src/analysis/run_unsw_phase10_statistics.py`, mcnemar_table, ba cặp trong từng view. Anchor `for model_a, model_b in combinations(`

### B-m2

Severity MINOR. Blocking No. Axis `figures-and-tables`. Issue key `attack-family-support-uncertainty-completeness`. Evidence status `VERIFIED`. Status OPEN. Route `DOCUMENT`.

Phần được nhận xét. PDF vật lý 30, Bảng 4.4 chỉ tách Fuzzers, Generic và nhóm còn lại; §5.2 nhắc tác động không đồng đều.

Bảng gộp hợp lệ về số học nhưng làm mất khả năng thấy đầy đủ chín họ và sự bất định đã có sẵn. Chẳng hạn Analysis thay 3 FN của RF-42 thành 19 FN của Stacking trên 677 mẫu; Worms chỉ 44 mẫu. RF-17 cũng không xuất hiện trong bảng họ tấn công dù là pipeline cuối. Văn bản đã cảnh báo mẫu hiếm nên không có overclaim cần bác bỏ.

Ý nghĩa. Người đọc IDS cần phân biệt số lỗi tuyệt đối và tỷ lệ bỏ sót trong từng họ. Không có CI, 0 FN ở Worms của RF-17 rất dễ bị hiểu là độ phát hiện hoàn hảo.

Điều kiện đóng. Bổ sung phụ lục cho cả ba pipeline và chín họ với support, FN, FNR và Wilson 95% từ bảng đã lưu. Nêu khoảng Wilson là marginal và phụ thuộc giả định đơn vị dòng; không dùng overlap/nonoverlap của các CI riêng để suy ra kiểm định cặp hoặc cơ chế.

Lý do mức độ. Minor vì kết luận chính đã công khai heterogeneity và không khái quát quá mức; bổ sung bảng làm kết quả chi tiết và kiểm tra được hơn.

- `report/chapters/results_discussion.tex`, Bảng 4.4, PDF vật lý 30. Anchor `Nhóm còn lại  & 20399 & 56  & 84  & +28`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`, official_test, Analysis, Stacking-42. Anchor `official_test,Analysis,stacking_42,677,19,0.028064992614475627`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`, official_test, Worms, RF-42. Anchor `official_test,Worms,random_forest_42,44,1,0.022727272727272728,0.004023252060053224,0.11807709698213287`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`, official_test, Worms, RF-17. Anchor `official_test,Worms,random_forest_17,44,0,0.0,0.0,0.08029560375848066`

### B-m3

Severity MINOR. Blocking No. Axis `writing-clarity`. Issue key `batch-average-inference-time-label`. Evidence status `VERIFIED`. Status OPEN. Route `DOCUMENT`.

Phần được nhận xét. PDF vật lý 29, Bảng 4.3 ghi Inference (ms/mẫu); §4.4 ở trang 30 giới hạn timing lịch sử.

Theo nguồn, ms/mẫu là thời gian predict_proba cho toàn TEST và đổi nhãn, chia 82332, không phải latency của một yêu cầu đơn. Báo cáo đã đúng khi không dự báo thời gian thiết bị triển khai, nhưng tiêu đề bảng vẫn nên làm rõ ý nghĩa batch.

Ý nghĩa. Throughput bình quân trên batch không xác định tail latency, thời gian trích feature mạng hoặc độ trễ cảnh báo ngoài thực tế.

Điều kiện đóng. Đổi nhãn hoặc chú thích thành thời gian batch chia số dòng; ghi batch 82332, một lần đo lịch sử, phạm vi predict_proba và threshold. Giữ cảnh báo môi trường gốc chưa xác định và không diễn giải là latency thời gian thực.

Lý do mức độ. Minor vì giới hạn vận hành đã được nêu và chỉ cần sửa nhãn đo lường cục bộ.

- `report/chapters/results_discussion.tex`, Bảng 4.3, PDF vật lý 29. Anchor `Inference (ms/mẫu)`
- `src/models/run_unsw_phase9_final_holdout.py`, main, predict_proba timed batch. Anchor `model.predict_proba(`
- `src/models/run_unsw_phase9_final_holdout.py`, main, inference_ms_per_sample. Anchor `/ len(test)`
- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`, RF-42, inference_time_seconds và inference_ms_per_sample. Anchor `0.714540399989346,0.008678768886816134`

## Tuyên bố chưa được hỗ trợ và ranh giới

### B-U1

Câu tuyệt đối rằng bản tái dựng full TRAIN chưa thực hiện không được packet hiện tại hỗ trợ.

Chỉ ghi nhận mâu thuẫn tài liệu với bản ghi tác giả. Không nâng các bản ghi thành xác minh model bytes, tái lập lịch sử hoặc hiệu năng TEST.

- `report/chapters/conclusion.tex`, §5.8.3, PDF vật lý 35. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks.artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`

### B-U2

Câu kết quả Voting không bị loại chưa được chứng minh bằng phần số liệu có trong chính báo cáo.

Packet có bằng chứng development ủng hộ nhận định định tính, vì vậy không gọi đây là kết quả bịa. Vấn đề là chưa đưa bằng chứng vào bản báo cáo.

- `report/chapters/conclusion.tex`, §5.8.2, PDF vật lý 34. Anchor `Kết quả không thuận lợi của Voting`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, all_features, hard voting, macro_f1_mean. Anchor `0.9473237829097595`

### B-U3

Không phát hiện trong bản thảo hiện hành tuyên bố superiority tổng thể, equivalence thống kê, multiclass detection, causal effect của FS hoặc external validation đã hoàn thành cần bác bỏ.

Các mở rộng này vượt bằng chứng hiện có, nhưng bản thảo đã chủ động từ chối chúng. Không tính chúng như các lỗi bổ sung.

- `report/chapters/conclusion.tex`, §5.8.4, PDF vật lý 35. Anchor `không phải một cam kết superiority, novelty hoặc deployment chưa được kiểm chứng.`

## Sửa tài liệu không cần thí nghiệm mới

- B-D1 (B-M1). Hòa giải các mức bằng chứng P9/P15 trong toàn văn và thêm bảng trạng thái tái dựng, không sửa frozen metrics.
- B-D2 (B-M2). Đưa số liệu development, Voting và diversity đã lưu vào bảng/phụ lục và gắn trực tiếp với RQ3, giải thích mean-fold/pooled OOF và giới hạn selection.
- B-D3 (B-m1). Hoàn thiện estimand bootstrap, percentile CI, seed và họ Holm theo view; ghi CI pointwise.
- B-D4 (B-m2). Bổ sung bảng attack-family đủ chín họ, ba pipeline, support và Wilson CI đã đóng băng.
- B-D5 (B-m3). Nêu rõ thời gian suy luận là batch average và phạm vi thao tác được bấm giờ.

## Những mở rộng cần thí nghiệm mới được phê duyệt

Không có thí nghiệm mới nào dưới đây là điều kiện bắt buộc để giữ kết luận hẹp hiện tại. Đây là điều kiện cho các tuyên bố mở rộng, không phải kết quả đã thực hiện.

### B-X1

Nếu muốn trả lời phần ổn định của RQ1 hoặc suy rộng CI qua huấn luyện.

Đăng ký trước nhiều lần fit độc lập theo seed, pipeline và compute thống nhất; tách biến thiên train khỏi sampling. Không xem ba fold hay 10000 draws là số lần train độc lập.

- `report/chapters/conclusion.tex`, §5.8.3, PDF vật lý 34. Anchor `nhiều lần huấn luyện độc lập`

### B-X2

Nếu muốn quy lợi ích cho FS, resampling hoặc class-weight.

Thí nghiệm mới matched, nested selector/preprocessing/resampling trong training folds; cố định RF trees và leaf để tách ảnh hưởng số feature. Khóa trước objective và phạm vi so sánh.

- `report/chapters/validity_discussion.tex`, §5.3, PDF vật lý 32. Anchor `giữ các tham số còn lại cố định`
- `report/chapters/conclusion.tex`, §5.8.3, PDF vật lý 35. Anchor `đối chứng resampling/class-weight bên trong training folds`

### B-X3

Nếu muốn phát biểu generalization mạng tương lai, unknown attacks hoặc ý nghĩa thống kê theo session.

Có dữ liệu mới và metadata định nghĩa session/host/time để chia nhóm độc lập, hoặc external benchmark hợp pháp với harmonization đã khóa. Không coi novel-vector subset là phép thử đó.

- `report/chapters/validity_discussion.tex`, §5.6, PDF vật lý 33. Anchor `không mô tả lỗi trên traffic tương lai.`

### B-X4

Nếu muốn chọn pipeline tốt nhất trong vận hành hoặc tuyên bố latency thời gian thực.

Định trước prevalence, chi phí sai số, tải, phần cứng, batch size, feature-extraction path và mục tiêu latency/throughput; đo lặp lại độc lập trong nghiên cứu tiếp. Tối ưu ngưỡng chỉ trên TRAIN/validation mới hợp lệ, không trên TEST đã biết.

- `report/chapters/results_discussion.tex`, §4.2, PDF vật lý 27. Anchor `chưa có ma trận chi phí tác nghiệp`
- `report/chapters/results_discussion.tex`, §4.4, PDF vật lý 30. Anchor `chưa có cơ sở dự báo thời gian trên thiết bị triển khai.`

## Câu hỏi bảo vệ chuyên sâu

### B-Q01

Từ bốn ô confusion của RF-42 và Stacking-42, hãy giải thích vì sao Macro-F1 tăng nhưng MCC giảm. F1 của Normal và Attack đóng góp ra sao, và tại sao weighted F1 không phải macro F1?

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`, official_test, RF-42, các F1. Anchor `0.8925580138692923,0.9735314269229383,0.7296486486486486,0.8341289335866896`
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, official_test, Stacking. Anchor `27139,9861,852,44480`

### B-Q02

Bảng transitions có Normal RF-only đúng 278, Stack-only đúng 420; Attack tương ứng 213 và 95. Tại sao net 24 dòng đúng thêm có thể đi cùng 118 Attack bỏ sót thêm và McNemar không bác bỏ? Vì sao không dùng p này để kiểm định Macro-F1?

- `results/final_analysis/unsw_nb15/phase14_error_analysis_step1/class_pairwise_transitions.csv`, Normal và Attack. Anchor `Normal,37000,26719,278,420,9583`
- `results/final_analysis/unsw_nb15/phase14_error_analysis_step1/class_pairwise_transitions.csv`, Attack. Anchor `Attack,45332,44385,213,95,639`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`, official_test, Stacking/RF42. Anchor `491,515,1006,0.46837651914684564`

### B-Q03

CI Macro-F1 [-0.000312, 0.001309] chứa 0 cho phép phát biểu gì về hiệu ứng và không cho phép phát biểu gì về equivalence? Muốn thiết kế equivalence trong nghiên cứu mới thì cần định trước biên ý nghĩa thực tế như thế nào?

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`, official_test, Macro-F1. Anchor `-0.0003118042125941106,0.0013089503250197615,False,10000`

### B-Q04

Đơn vị quan sát, đơn vị resampling và đơn vị huấn luyện của nghiên cứu là gì? Nếu flows cùng host/session phụ thuộc, 82332 dòng hoặc 10000 bootstrap draws có đại diện số lần lặp độc lập không, và dữ liệu nào còn thiếu để định nghĩa cluster?

- `report/chapters/theoretical_foundations.tex`, §1.2.1, PDF vật lý 12. Anchor `đơn vị dự đoán là một \emph{dòng dữ liệu UNSW-NB15}`
- `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`, bootstrap.interpretation. Anchor `does not establish independent network-flow sampling.`

### B-Q05

Bootstrap multinomial trên joint patterns trong từng nhãn giữ được pairing như thế nào? Khi giữ n Normal/Attack cố định, CI đang có điều kiện trên yếu tố nào và tại sao không bao trùm biến động prevalence hay train seed?

- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `The same resampled joint prediction patterns are used for every model,`
- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`

### B-Q06

Họ Holm thực tế là ba cặp model trong từng view hay tất cả sáu phép thử hai view cùng một họ? Bốn CI metric đang pointwise hay simultaneous, và việc ghi rõ lựa chọn này thay đổi cách độc giả diễn giải FPR/FNR như thế nào?

- `src/analysis/run_unsw_phase10_statistics.py`, mcnemar_table. Anchor `for view in EVAL_VIEWS:`
- `src/analysis/run_unsw_phase10_statistics.py`, mcnemar_table. Anchor `adjusted = holm_adjust(`
- `src/analysis/run_unsw_phase10_statistics.py`, percentile_ci. Anchor `np.nanpercentile(`

### B-Q07

Giả sử chỉ trên benchmark hiện có và chi phí FP/FN là hằng số, hãy lập bất đẳng thức từ -142 FP và +118 FN để tìm tỷ số chi phí hòa vốn của Stacking. Vì sao tỷ số này chưa chọn được detector cho một mạng có prevalence khác?

- `report/chapters/results_discussion.tex`, §4.2, PDF vật lý 27. Anchor `Stacking-42 giảm \textbf{142 FP}`
- `report/chapters/results_discussion.tex`, §4.2, PDF vật lý 27. Anchor `đồng thời tăng \textbf{118 FN}`

### B-Q08

RF-42 có ROC-AUC khoảng 0.978 nhưng FPR tại threshold 0.5 khoảng 27%. Vì sao hai quan sát không mâu thuẫn? Trường pr_auc trong tệp là AP theo thuật toán nào, và vì sao không tối ưu threshold lại trên TEST để làm đẹp FPR?

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`, official_test, RF42, AUC/AP/FPR. Anchor `0.9784251870881735,0.9825430925238847,0.27035135135135135`
- `src/models/run_unsw_phase9_final_holdout.py`, classification_metrics. Anchor `average_precision_score(`
- `report/chapters/methodology.tex`, §3.5, PDF vật lý 26. Anchor `Không dùng TEST để chọn lại mô hình, tối ưu ngưỡng hay sửa feature set.`

### B-Q09

Làm thế nào Fuzzers có tỷ lệ bỏ sót 754/6062 của Stacking nhưng FNR toàn Attack chỉ 852/45332? Nếu tần suất các họ tấn công thay đổi, kết luận tổng thể nào còn giữ được?

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`, official_test, Fuzzers, Stacking. Anchor `official_test,Fuzzers,stacking_42,6062,754,0.12438139227977565`
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, official_test, Stacking. Anchor `852,44480,37000,45332,82332`

### B-Q10

Tại sao RF-17 có 0 FN/44 Worms chưa chứng minh phát hiện Worms hoàn hảo? Hãy diễn giải upper Wilson khoảng 8.03% và giới hạn phụ thuộc dòng; vì sao CI riêng của hai model không thay thế so sánh cặp?

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`, official_test, Worms, RF17. Anchor `official_test,Worms,random_forest_17,44,0,0.0,0.0,0.08029560375848066`

### B-Q11

Novel-vector view đổi support thành 35528 Normal và 38263 Attack, đồng thời dùng mask 42 features cho cả RF-17. Vì sao suy giảm Macro-F1 không cô lập được tác hại nhân quả của overlap, và vì sao mask này không bảo đảm RF-17 cũng chưa thấy vector 17 chiều tương ứng?

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, novel_vector_test, RF17. Anchor `random_forest_17,novel_vector_test,25849,9679,699,37564,35528,38263,73791`
- `results/data_audit/unsw_nb15_views/view_summary.json`, feature_vector_column_count và purpose. Anchor `"feature_vector_column_count": 42`

### B-Q12

RF-17 đổi đồng thời số feature, 300 thành 150 cây và leaf 1 thành 2. Thí nghiệm matched nào mới tách được tác động FS? Vì sao chọn feature toàn TRAIN trước outer CV có thể làm CV lạc quan nhưng không đồng nghĩa TEST được dùng trực tiếp để chọn feature?

- `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`, RF17.hyperparameters. Anchor `"min_samples_leaf": 2`
- `report/chapters/methodology.tex`, §3.2, PDF vật lý 24. Anchor `stable feature selection được thực hiện trên \emph{toàn bộ official TRAIN trước development cross-validation}`

### B-Q13

Các mean/SD của ba development folds và pooled OOF khác estimand như thế nào? Vì sao SD nhỏ giữa folds không xác nhận stable gain qua train độc lập, đặc biệt khi feature selection và meta tuning chưa fully nested?

- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/experiment_metadata.json`, outer_cv. Anchor `"n_splits": 3`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, header. Anchor `macro_f1_mean,macro_f1_std`
- `report/chapters/methodology.tex`, §3.3, PDF vật lý 24-25. Anchor `meta tuning chưa hoàn toàn nested`

### B-Q14

Với cặp LR/DT toàn feature có 4267 lỗi chung, oracle accuracy và double-fault giúp nhận xét tiềm năng bổ sung sai số thế nào? Vì sao oracle không phải model triển khai và kết quả hard/soft voting thấp hơn RF không bác bỏ mọi phương án ensemble?

- `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, LR/DT, all_features. Anchor `0.024335437804050394,0.9756645621959497`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`, hard voting macro F1. Anchor `0.9473237829097595`
- `report/chapters/theoretical_foundations.tex`, §1.2.4.3, PDF vật lý 15. Anchor `Oracle là cận mô tả dưới thông tin nhãn thật`

### B-Q15

Ba bản ghi P15 full TRAIN, roundtrip tolerance 1e-12 và no_test_evaluation chứng minh điều gì, và còn thiếu gì để nối chúng với metrics P9? Cần sửa câu chưa thực hiện full TRAIN như thế nào mà không nhận nhầm tái dựng thành mô hình lịch sử?

- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks. Anchor `"no_test_evaluation": true`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, roundtrip_numeric_atol_rtol. Anchor `"roundtrip_numeric_atol_rtol": 1e-12`
- `report/chapters/conclusion.tex`, §5.8.3, PDF vật lý 35. Anchor `bản tái dựng full TRAIN chưa thực hiện`

### B-Q16

Số 0.008679 ms/mẫu của RF-42 được suy từ một batch như thế nào? Muốn đánh giá thời gian thực phải bổ sung phép đo và operating envelope nào, và vì sao không dùng timing hoặc dung lượng bản tái dựng P15 để thay trực tiếp số P9?

- `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`, RF42 timing. Anchor `0.714540399989346,0.008678768886816134`
- `src/models/run_unsw_phase9_final_holdout.py`, main, cost_rows. Anchor `/ len(test)`
- `results/reproducibility/p15_local_rf42_full_02/run_report.json`, worker_checks.fit_seconds. Anchor `"fit_seconds": 1867.234`

## Đánh giá năm tiêu chí chung

### originality

Tính mới được giới hạn hợp lý ở chuỗi so sánh và kiểm toán một case study. Không có cơ sở xác nhận thuật toán mới hoặc đầu tiên trong lĩnh vực, và bản thảo không đòi tuyên bố đó.

- `report/chapters/introduction.tex`, §1.1.4, PDF vật lý 11. Anchor `\emph{không} đủ cơ sở để khẳng định một thuật toán Ensemble Learning mới`

### scientific_importance

Có giá trị học thuật trong phạm vi benchmark và giảng dạy thực nghiệm. Chưa thiết lập lợi ích vận hành, khả năng chuyển mạng hoặc phát hiện tấn công chưa biết. Những giới hạn đã công khai không tự động trở thành lỗi thực nghiệm.

- `report/chapters/results_discussion.tex`, §4.2, PDF vật lý 27. Anchor `chưa có ma trận chi phí tác nghiệp`

### interdisciplinary_readership

Phù hợp với độc giả IDS, ML và reproducibility. Thông điệp cần nhìn cả FP/FN thay vì một điểm gộp có thể chuyển sang bài toán phát hiện hiếm, nhưng đây là suy luận phương pháp của phản biện, chưa phải kết quả cross-domain đã đo.

- `report/chapters/validity_discussion.tex`, §5.1, PDF vật lý 31. Anchor `không gọi một pipeline là tốt nhất cho mọi tình huống`

### technical_soundness

Các counts, định nghĩa lớp dương, averaging và chiều hiệu số kiểm tra được đều nhất quán. Nguồn bootstrap giữ cặp và phân tầng nhãn; McNemar kiểm tra correctness và Holm theo từng view. Cần mô tả rõ hơn chi tiết này, đưa bằng chứng development vào báo cáo và hòa giải trạng thái P15. Không suy sự độc lập session từ số dòng hoặc sự ổn định train từ 10000 bootstrap draws.

- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`, header. Anchor `macro_f1,weighted_f1,balanced_accuracy,mcc,roc_auc,pr_auc,fpr,fnr`

### readability_for_nonspecialists

Định nghĩa FP/FN và phân biệt binary với attack-family được giải thích tốt; các bảng chính đọc được qua kiểm tra trực quan. Nhiều thuật ngữ tiếng Anh và tuyên bố về development chưa gắn số liệu làm người đọc khó theo mạch lựa chọn mô hình. Nhãn ms/mẫu nên nêu rõ đo trên một batch.

- `report/chapters/theoretical_foundations.tex`, §1.2.1.2, PDF vật lý 12. Anchor `False positive (FP) là Normal bị báo Attack`
- `report/chapters/results_discussion.tex`, Bảng 4.3, PDF vật lý 29. Anchor `Inference (ms/mẫu)`

## Phủ các trục kỹ thuật

| Trục | Áp dụng | Nhận xét |
|---|---|---|
| novelty-significance | applicable | Đóng góp case study được giới hạn; không xác lập novelty toàn lĩnh vực từ catalog chưa đầy đủ. |
| mechanism-evidence | applicable | RQ3 và profile lỗi chỉ mô tả; không có causal mechanism claim cần bác bỏ. |
| experimental-design | applicable | Official split/freeze và confounding RF được công khai; thiếu nested/repeated/group validation chỉ chặn các mở rộng tương ứng. |
| statistical-rigor | applicable | Kiểm tra averaging, counts, pairing, CI, McNemar và multiplicity; B-m1 cần hoàn thiện mô tả. |
| reproducibility | applicable | B-M1 phản ánh trạng thái hồ sơ không thống nhất; model bytes và môi trường lịch sử không xác minh được. |
| clinical-validity | not applicable | Không có cohort hoặc tuyên bố lâm sàng. |
| ethical-governance | not assessable | Packet đủ xem benchmark công khai được dẫn nguồn nhưng không xác minh toàn bộ điều kiện quyền phân phối dữ liệu/model. Không suy ra vi phạm hoặc yêu cầu phê duyệt người tham gia. |
| data-resource-quality | applicable | Đối chiếu support, overlap và view summaries; không mở raw để xác nhận provenance từng dòng. |
| figures-and-tables | applicable | B-M2 và B-m2 là khoảng thiếu trình bày; bảng chính kiểm tra số học và hình đã xem không cho thấy mâu thuẫn. |
| writing-clarity | applicable | B-m3 cần làm rõ batch average; các giới hạn và thuật ngữ cốt lõi tương đối rõ. |
| claim-moderation | applicable | Không suy superiority, equivalence, multiclass hoặc external validation. Hai unsupported statements cục bộ là B-U1/B-U2. |
| causal-vs-correlative | applicable | FS, diversity và feature-error associations được giới hạn mô tả. Không yêu cầu causal experiment để giữ kết luận hiện tại. |

## Khuyến nghị có điều kiện

**MAJOR_REVISION_REQUIRED**

Ưu tiên sửa B-M1 và B-M2 để báo cáo thể hiện đúng bằng chứng tái dựng và phần development đã có. Đây là sửa tài liệu có nội dung đáng kể, không phải yêu cầu train lại để cứu một kết quả tính sai. B-m1 đến B-m3 nên đóng trước bản nộp. Không có Major nào được đánh dấu blocking đối với kết luận hẹp về đánh đổi FP/FN trên benchmark đã khóa.

Sau khi các sửa tài liệu được kiểm chứng và vẫn giữ phạm vi một case study, có thể xem xét ACCEPTABLE_WITH_LIMITATIONS cho phạm vi khoa học nội bộ. Không điều kiện hóa việc này vào việc hoàn tất mọi thí nghiệm tương lai; mọi tuyên bố về stability, FS causality, cross-network hoặc deployment mới đòi thiết kế mới được phê duyệt.

Không cấp nghiệm thu P20 cuối, không xác nhận release hay mô hình triển khai; không phải quyết định của tạp chí.

## Hướng dẫn kỹ năng thực sự đã đọc

- `C:/Users/admin/.codex/skills/nature-reviewer/SKILL.md`. Quy trình phản biện mô phỏng và phân loại mức độ.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/reviewer-workflow.md`. Lời gọi tách biệt và dừng ghi sau khi hoàn tất.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/technical-concern-taxonomy.md`. Đối chiếu đủ 12 trục.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/domain-specific-review-gates.md`. Phần Engineering, kiểm tra operating envelope và matched evaluation.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/qa-checklist.md`. Grounding, severity, blocking, giới hạn và không bịa.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/review-axes.md`. Đánh giá năm tiêu chí chung.
- `C:/Users/admin/.codex/skills/nature-reviewer/references/editorial criteria and processes.md`. Nền tiêu chí Nature-style, không áp dụng như quyết định biên tập.
- `C:/Users/admin/.codex/skills/nature-statistics/SKILL.md`. Ranh giới audit thống kê, đơn vị độc lập và diễn giải.
- `C:/Users/admin/.codex/skills/nature-statistics/references/statistical-reporting.md`. Estimand, n, giả định và multiplicity.
- `C:/Users/admin/.codex/skills/nature-statistics/references/common-failure-modes.md`. Pseudoreplication, significance-only và multiple comparisons.
- `C:/Users/admin/.codex/skills/nature-statistics/references/reviewer-checklist.md`. QA thống kê trước giao.
- `C:/Users/admin/.codex/skills/nature-statistics/references/figure-statistics.md`. Mẫu số, uncertainty và caption.
- `C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md`. Đọc và render trực quan PDF trong bộ nhớ; không sửa/tạo PDF.

Báo cáo này được hoàn tất riêng trước tổng hợp. Không tham khảo hoặc điều chỉnh theo báo cáo khác.
