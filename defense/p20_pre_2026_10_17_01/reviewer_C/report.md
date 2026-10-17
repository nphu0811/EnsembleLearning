# Reviewer C

Khuyến nghị **MAJOR_REVISION_REQUIRED**. Đây là phản biện khoa học mô phỏng nội bộ P20-PRE, không phải hội đồng người thật, quyết định tạp chí hoặc xác nhận P20 hoàn tất.

## Phạm vi và kiểm tra đầu vào

Chỉ packet_02/local_contents, manifest.csv, receipt.json, COMMON_REVIEW_RULES.md và BRIEF_C.md; installed skills chỉ là hướng dẫn.

Manifest SHA-256 `c0f0b3828ba16ce8312b489915cc4c56c9fc7c771dbeefe1d7a9bb78938b62b7`. Đã tính lại hash manifest, SHA-256 và kích thước của cả 80 tệp, không có sai khác. Ba source/config/subset hash của mỗi run report P15 trùng các tệp tương ứng trong gói. Hash TRAIN chỉ đối chiếu với checksum record, không xác minh raw bytes.

Đọc nội dung PDF trực tiếp, đối chiếu approved_report_pages.txt; xem trực quan các trang vật lý 11, 17, 25, 28. main.tex xác định các chương đang dùng. PDF không có abstract riêng.

Không truy cập Internet, full text bên ngoài, raw/prediction CSV hoặc model bytes; không chạy/import mã ML, train, bootstrap hoặc sửa packet. Literature notes là tóm lược phụ theo locator, không phải toàn văn hay thí nghiệm được reviewer tái lập.

Invocation riêng với brief C; không đọc báo cáo khác, shared ledger, synthesis, research memory hoặc QA ngoài gói. Cùng filesystem nên đây không phải cách ly bằng quyền OS hoặc xác nhận độc lập của con người.

## Đánh giá khoa học tổng thể

Bản báo cáo có nền tảng để bảo vệ một case study IDS nhị phân có kiểm toán. Kết quả trung tâm là thay đổi FP/FN của Stacking, không phải thuật toán mới, chiến thắng tổng thể hay khả năng triển khai. Các giới hạn phương pháp đã được thừa nhận khá tốt. Tuy nhiên, luận điểm công bố còn thiếu đối chiếu prior art gần nhất, phần bằng chứng development được nhận là đóng góp chưa hiện rõ trong PDF, và trạng thái tái lập chưa đồng bộ với host record P15. Cần sửa lớn về hồ sơ và lập luận trước khi dùng như manuscript hoàn chỉnh; không nhất thiết cần huấn luyện mới để giữ kết luận hẹp hiện tại.

Đối tượng quan tâm chính là nhà nghiên cứu IDS, ML thực nghiệm, người xây benchmark và nghiên cứu tái lập. Bài học có giá trị là một cải thiện số học rất nhỏ của metric gộp có thể đi kèm ít cảnh báo giả hơn và nhiều tấn công bỏ sót hơn. Packet chưa thiết lập tầm quan trọng rộng ở các môi trường vận hành độc lập.

## Điểm mạnh đã có bằng chứng

### C-S1

Định vị đóng góp trung thực. Báo cáo nhận các thành phần ensemble/FS đã có, giữ nhiệm vụ binary và không biến thiếu thí nghiệm của đề tài thành khoảng trống toàn lĩnh vực.

- `report/chapters/introduction.tex`, PDF vật lý 10, mục 1.1.1. Anchor `chỉ áp dụng chúng không thể tự xem là một thuật toán mới`
- `report/chapters/related_work.tex`, PDF vật lý 17 đến 18, mục 1.3.4. Anchor `khoảng thiếu của nghiên cứu này`

### C-S2

Kết quả chính được trình bày qua đánh đổi cụ thể. Đếm RF/Stacking tương thích với bảng confusion matrix, CI Macro-F1 chứa 0, và kết luận không gọi p không có ý nghĩa là bằng chứng tương đương.

- `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv`, official_test, RF-42 và Stacking-42. Anchor `stacking_42,official_test,27139,9861,852,44480`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`, official_test, stacking_42/random_forest_42, macro_f1. Anchor `-0.0003118042125941106,0.0013089503250197615`
- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.1. Anchor `không xác nhận ưu thế tổng thể`
- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.1. Anchor `không chứng minh hai mô hình tương đương`

### C-S3

Các confound và ranh giới đánh giá được khai báo ngay trong phương pháp. FS trước development CV, meta tuning chưa fully nested và RF-17 đổi cả feature lẫn siêu tham số đều được nêu rõ.

- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.2. Anchor `toàn bộ official TRAIN trước development cross-validation`
- `report/chapters/methodology.tex`, PDF vật lý 25, mục 3.3. Anchor `RF-17 khác RF-42 cả số feature`
- `report/chapters/methodology.tex`, PDF vật lý 24 đến 25, mục 3.3. Anchor `phần meta tuning chưa hoàn toàn nested`

### C-S4

Đơn vị dự đoán, overlap và phân nhóm attack được phân biệt hợp lý. Novel-vector không được gọi external validation; attack_cat chỉ dùng nhãn thật hậu nghiệm.

- `report/chapters/dataset_eda.tex`, PDF vật lý 23, mục 2.5. Anchor `Số 8\,541 là \emph{số dòng TEST}`
- `report/chapters/results_discussion.tex`, PDF vật lý 30, mục 4.6. Anchor `Novel-vector \emph{không} phải bộ dữ liệu kiểm thử độc lập.`
- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.1. Anchor `không phải mô hình đa lớp`

## Major Concerns

### C-M1

**Mức độ** MAJOR. **Blocking** No. **Trục** novelty-significance. **Trạng thái bằng chứng** PARTIAL. **Trạng thái xử lý** OPEN.

**Claim được xét**

PDF vật lý 11, mục 1.1.4 và vật lý 17 đến 18, mục 1.3. Đóng góp thực nghiệm và phương pháp luận được định vị bằng kiểm toán case study.

**Bằng chứng**

- `report/chapters/introduction.tex`, PDF vật lý 11, mục 1.1.4. Anchor `Các kết quả đó có thể có giá trị thực nghiệm và phương pháp luận`
- `report/chapters/related_work.tex`, PDF vật lý 17, mục 1.3.1. Anchor `đóng góp được định vị ở kiểm toán case study`
- `literature_reported_facts.csv`, L06, C01 và C02. Anchor `Uses a random80/20 split`
- `literature_reported_facts.csv`, L12, C15, PDF nguồn trang 5 đến 9 theo catalog. Anchor `SMOTE-TOMEK`
- `literature_reported_facts.csv`, N02, C08, Methodology/Data description theo catalog. Anchor `Merges original partitions`
- `literature_reported_facts.csv`, N02, C10, Stacked ensemble theo catalog. Anchor `RF/XGB/Catboost`
- `literature_scope.json`, N02, sections_read. Anchor `MI-Boruta/Stacked ensemble`

**Nhận xét**

Tổng quan hiện chỉ liệt kê các họ phương pháp, chưa cho thấy phần đóng góp thực nghiệm khác gì các công trình gần nhất đã có trong chính catalog. N02 có MI-Boruta và stacked ensemble nhưng không hiện diện trong chương tổng quan hoặc danh mục 12 tài liệu của PDF. Các khác biệt đã biết của L06, L12 và N02 về dữ liệu, split, FS và tầng meta chưa được đặt cạnh protocol hiện tại. Vì vậy giá trị bổ sung cho một bài công bố còn chưa được lập luận rõ. Đây là thiếu đối chiếu cụ thể, không phải bằng chứng rằng tác giả tuyên bố phát minh Stacking hoặc rằng lĩnh vực chưa làm các kiểm toán này.

**Vì sao cần sửa**

Một case study có thể đáng công bố vì bài học thực nghiệm dù không có thuật toán mới. Tuy nhiên người đọc cần biết thông tin nào thực sự bổ sung cho prior art và thông tin nào là thực hành đánh giá đã biết.

**Điều kiện nghiệm thu sửa đổi**

Thêm bảng đối chiếu có phạm vi với L06, L12 và N02, nêu dataset/nhiệm vụ/split/FS/meta learner/phạm vi đọc và bài học riêng của nghiên cứu. Gắn DOI N02 10.1186/s40537-024-00994-7 với mô tả có căn cứ và ghi các trường thư mục chưa xác minh trong gói. Không xếp hạng bằng điểm khác protocol, không chứng nhận nesting của bài trước nếu catalog chưa xác nhận, và không suy ra novelty toàn lĩnh vực từ bảng này.

**Đường xử lý** DOCUMENT. Thiếu mắt xích quan trọng để đánh giá tính mới và vị trí công bố, nhưng không làm sai các đếm lỗi của case study.

### C-M2

**Mức độ** MAJOR. **Blocking** No. **Trục** reproducibility. **Trạng thái bằng chứng** PARTIAL. **Trạng thái xử lý** OPEN.

**Claim được xét**

PDF vật lý 35, mục 5.8.3 nói bản tái dựng full TRAIN chưa thực hiện; vật lý 33, mục 5.5 chỉ mô tả mô hình kiểm thử trên tập con.

**Bằng chứng**

- `report/chapters/conclusion.tex`, PDF vật lý 35, mục 5.8.3. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- `report/chapters/validity_discussion.tex`, PDF vật lý 33, mục 5.5. Anchor `Bản model cuối ở dạng serialized cũng không được xác minh tồn tại.`
- `results/reproducibility/p15_local_rf17_full_01/run_report.json`, worker_checks.train_rows và artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`
- `results/reproducibility/p15_local_rf42_full_02/run_report.json`, worker_checks. Anchor `"train_rows": 175341`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks.no_test_evaluation. Anchor `"no_test_evaluation": true`
- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`, scope. Anchor `P15_LOCAL_ARTIFACT_READONLY_QA; NOT original model or scientific TEST validation`

**Nhận xét**

Trạng thái tái lập trong báo cáo không phản ánh ba run report P15 của máy tác giả. Cả ba hồ sơ ghi mode full, PASS và 175341 dòng TRAIN; hồ sơ QA cũng ghi nhận kiểm tra artifact tái dựng. Không thể giữ nguyên câu khẳng định chưa tái dựng full TRAIN mà thiếu mốc phiên bản hoặc phạm vi. Ngược lại, các record P15 không phải model bytes và không xác nhận môi trường gốc, tính đồng nhất với model lịch sử hay hiệu năng TEST.

**Vì sao cần sửa**

Tái lập là một phần quan trọng của định vị kiểm toán. Gộp model lịch sử chưa có, kiểm thử trên tập con và tái dựng full TRAIN thành một trạng thái làm người đọc đánh giá sai mức bằng chứng đang có.

**Điều kiện nghiệm thu sửa đổi**

Đối chiếu các mục 3.6, 5.5 và 5.8.3 theo cùng mốc dữ liệu. Tách rõ môi trường/model lịch sử chưa xác minh, P15 full-TRAIN reconstruction được host report ghi nhận, QA trên TRAIN-derived probe, và chưa xác nhận tái lập khoa học trên TEST. Ghi P15 là bằng chứng do tác giả lưu; chỉ nâng lên xác minh model bytes khi có quy trình riêng được phê duyệt. Không thay bảng hiệu năng hoặc chi phí lịch sử bằng số P15.

**Đường xử lý** DOCUMENT. Sai khác về trạng thái tái lập ảnh hưởng đáng kể khả năng kiểm chứng và cách định vị đóng góp; chưa bác bỏ các kết quả khoa học đã lưu.

### C-M3

**Mức độ** MAJOR. **Blocking** No. **Trục** claim-moderation. **Trạng thái bằng chứng** VERIFIED. **Trạng thái xử lý** OPEN.

**Claim được xét**

PDF vật lý 11, mục 1.1.4; vật lý 33, Bảng 5.2 RQ3; vật lý 34, mục 5.8.2 nhận Diversity/OOF và kết quả Voting không thuận lợi là phần đóng góp.

**Bằng chứng**

- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.2. Anchor `Kết quả không thuận lợi của Voting`
- `report/chapters/validity_discussion.tex`, PDF vật lý 33, Bảng 5.2, RQ3. Anchor `Diversity, OOF, voting, stacking`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv`, all_features, hard_voting_lrdtrf. Anchor `0.9473245884056625`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv`, all_features, random_forest. Anchor `0.9503873654153012`
- `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, all_features, decision_tree/random_forest, error_correlation. Anchor `0.49892194038858895`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/experiment_metadata.json`, interpretation_warning. Anchor `Development CV only.`

**Nhận xét**

Phần đóng góp nhấn mạnh sai số bổ sung, Diversity/OOF và báo cáo kết quả Voting không thuận lợi, nhưng PDF không trình bày bảng hay giá trị development diversity/voting. Các bảng và hình của Chương 4 tập trung vào ba candidate cuối, còn Bảng 5.1 là paired correctness của RF và Stacking trên TEST, không thay thế diversity giữa các base learners. Gói có sẵn các bảng development nên độc giả không cần chỉ dựa vào một câu khẳng định rằng kết quả không thuận lợi đã được báo cáo.

**Vì sao cần sửa**

RQ3 và việc không chọn lọc kết quả thuận lợi là một phần của giá trị case study. Khi không thấy số liệu development và bước chọn mô hình, người đọc không đánh giá được liên hệ giữa diversity quan sát và quyết định ensemble.

**Điều kiện nghiệm thu sửa đổi**

Thêm bảng tóm tắt development RF/hard voting/soft voting/stacking với thước đo và protocol, kèm ít nhất một đối chiếu diversity thực có và đường dẫn nguồn. Chỉ rõ đây là development configurations trước final tuning, không ghép trực tiếp điểm OOF của chúng với điểm holdout của candidate cuối để suy ra hiệu ứng. Trình bày liên hệ mô tả và không đổi thành kết luận nhân quả.

**Đường xử lý** DOCUMENT. Bằng chứng cho một đóng góp và RQ được nêu ở phần mở đầu chưa được mang vào bản báo cáo; có thể khắc phục từ các bảng đã khóa mà không tạo thí nghiệm mới.

## Minor Comments

### C-m1

**Mức độ** MINOR. **Blocking** No. **Trục** writing-clarity. **Trạng thái bằng chứng** VERIFIED. **Trạng thái xử lý** OPEN.

PDF vật lý 24 đến 25, mục 3.2 và 3.4 mô tả track 17 feature và preprocessing bằng ngôn ngữ tổng quát.

Bản văn chưa định nghĩa ngắn gọn stable 17 được tạo thế nào hoặc chỉ ra danh sách/thứ tự; chưa nêu rõ one-hot cho proto/service/state, xử lý category mới và việc chuẩn hóa số chỉ dùng ở LR. Tên stable có thể bị nhầm với độ ổn định của hiệu năng qua nhiều lần train. Mã và các tập con đã lưu làm các chi tiết này có thể kiểm tra được, nên đây là thiếu trình bày cục bộ.

Độc giả không chuyên cần phân biệt ổn định của selector trên các mẫu TRAIN với ổn định của detector. Một bản mô tả ngắn cũng giúp đối chiếu phương pháp với prior art.

- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.2. Anchor `Track 17 feature ổn định lấy từ danh sách đã lưu`
- `src/features/select_unsw_features_stage2.py`, configuration. Anchor `STABILITY_MIN_FREQUENCY = 0.60`
- `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`, stable_2plus_methods. Anchor `"stable_2plus_methods"`
- `src/models/run_unsw_phase9_final_holdout.py`, make_ohe. Anchor `handle_unknown="ignore"`
- `src/models/run_unsw_phase9_final_holdout.py`, make_lr_pipeline. Anchor `scale_numeric=True`

**Điều kiện nghiệm thu sửa đổi**

Bổ sung công thức/quy tắc stable trong từng phương pháp rồi bỏ phiếu ít nhất hai phương pháp, năm seed và phạm vi TRAIN; dẫn danh sách 17 theo thứ tự, cùng bảng preprocessing theo base learner. Phân biệt số feature gốc với số cột sau one-hot, và giữ cảnh báo FS trước outer CV.

**Đường xử lý** DOCUMENT. Làm phương pháp dễ đọc và tra cứu hơn; nguồn triển khai cần thiết đã có trong gói và không xuất hiện sai kết quả do thiếu đoạn mô tả này.

### C-m2

**Mức độ** MINOR. **Blocking** No. **Trục** statistical-rigor. **Trạng thái bằng chứng** VERIFIED. **Trạng thái xử lý** OPEN.

PDF vật lý 26, mục 3.5; vật lý 28, mục 4.3 và Bảng 4.2 mô tả paired bootstrap 10000 lần và Holm.

Mô tả bootstrap chưa nói rõ phân tầng theo nhãn thật, giữ cố định số Normal/Attack và lấy multinomial trên joint prediction patterns. Chưa nêu percentile CI, seed 20260928 và họ Holm gồm ba cặp trong từng evaluation view. Đây là bổ sung định nghĩa estimand và cách tính, không phải phát hiện sai CI.

Người đọc có thể thực hiện paired row bootstrap không phân tầng rồi chờ tái tạo chính xác các CI đã công bố. Định nghĩa conditional-on-rows hiện có vẫn cần thêm điều kiện cố định số lớp và phạm vi multiplicity.

- `report/chapters/methodology.tex`, PDF vật lý 26, mục 3.5. Anchor `paired bootstrap 10\,000 lần lấy mẫu lại các dòng benchmark`
- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- `src/analysis/run_unsw_phase10_statistics.py`, percentile_ci. Anchor `np.nanpercentile(`
- `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`, bootstrap.random_seed. Anchor `"random_seed": 20260928`
- `src/analysis/run_unsw_phase10_statistics.py`, mcnemar_table, vòng lặp theo view trước holm_adjust. Anchor `for view in EVAL_VIEWS:`

**Điều kiện nghiệm thu sửa đổi**

Bổ sung một đoạn Methods đúng theo bootstrap_metric_arrays, percentile_ci và mcnemar_table, phân biệt CI từng metric chưa hiệu chỉnh đồng thời với McNemar được Holm theo view. Giữ các khoảng và p đã lưu, giữ giới hạn phụ thuộc dòng và không suy ra tương đương từ p không có ý nghĩa.

**Đường xử lý** DOCUMENT. Thiếu chi tiết kỹ thuật cục bộ trong báo cáo; mã và metadata đã cho phép nhận diện đầy đủ quy trình, và kết luận hiện tại đã thận trọng.

## Tuyên bố chưa đủ bằng chứng và ranh giới diễn giải

**bản tái dựng full TRAIN chưa thực hiện**

Không phù hợp với trạng thái được ba host record P15 khai báo; sửa theo C-M2, không nâng host record thành xác minh model bytes.

Phân loại `CURRENT_MANUSCRIPT_STATEMENT_NEEDS_TIME_AND_SCOPE_CORRECTION`.

- `report/chapters/conclusion.tex`, PDF vật lý 35, mục 5.8.3. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- `results/reproducibility/p15_local_rf17_full_01/run_report.json`, worker_checks.train_rows và artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`
- `results/reproducibility/p15_local_rf42_full_02/run_report.json`, worker_checks. Anchor `"train_rows": 175341`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks.no_test_evaluation. Anchor `"no_test_evaluation": true`

**Diversity/OOF và Voting không thuận lợi là phần đóng góp đã trình bày**

Có nguồn bảng tương ứng, nhưng PDF cần đưa bằng chứng định lượng vào theo C-M3.

Phân loại `SUPPORTED_IN_PACKET_BUT_INSUFFICIENTLY_PRESENTED_IN_PDF`.

- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.2. Anchor `Kết quả không thuận lợi của Voting`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv`, all_features, hard_voting_lrdtrf. Anchor `0.9473245884056625`
- `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, all_features, decision_tree/random_forest, error_correlation. Anchor `0.49892194038858895`

**Thuật toán mới, superiority tổng thể, equivalence từ p không có ý nghĩa, field-wide gap, external validation hoặc triển khai thực tế**

Không quy các giả thuyết mở rộng này thành lỗi factual của bản hiện tại. Chúng vẫn chưa được hỗ trợ nếu sau này muốn nâng phạm vi.

Phân loại `NOT_ASSERTED_AS_ESTABLISHED_BY_CURRENT_MANUSCRIPT`.

- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.1. Anchor `không xác nhận ưu thế tổng thể`
- `report/chapters/results_discussion.tex`, PDF vật lý 30, mục 4.6. Anchor `Novel-vector \emph{không} phải bộ dữ liệu kiểm thử độc lập.`
- `report/chapters/related_work.tex`, PDF vật lý 18, mục 1.3.4. Anchor `không được biến thành khẳng định rằng toàn bộ lĩnh vực`
- `report/chapters/conclusion.tex`, PDF vật lý 35, mục 5.8.3. Anchor `chưa thể công bố đã tái lập end-to-end`

Không tìm thấy cơ sở để gán sai sót về abstract vì PDF không có abstract riêng. Không coi những hạn chế đã công khai như thiếu temporal validation, repeated training hoặc matched resampling là kết quả giả. Không đánh đồng ghi nhận P15 trên máy tác giả với xác nhận độc lập về model bytes hoặc model lịch sử.

## Sửa tài liệu không cần thí nghiệm mới

- C-M1. Thêm bảng prior-art có phạm vi đọc, protocol và đóng góp empirical, bao gồm N02 đã có catalog; chỉ dùng facts có locator, không tạo bảng SOTA không matched.
- C-M2. Cập nhật nhất quán trạng thái tái lập ở Methods/Discussion/Conclusion, tách model gốc, P15 reconstruction, host QA và scientific TEST validation.
- C-M3. Đưa development voting/diversity và rationale chọn candidate vào PDF từ bảng đóng băng; phân biệt development và final tuning.
- C-m1, C-m2. Bổ sung selector/preprocessing và chi tiết bootstrap/Holm đã có trong source; giữ mọi bảng frozen và kết luận thống kê.

Ba Major Concerns hiện tại không tự bác bỏ kết quả hẹp của benchmark. Chúng đòi hỏi làm rõ luận điểm và đưa bằng chứng đã có vào bản văn, đồng thời sửa trạng thái tái lập cho đúng phạm vi. Nguồn cần đọc cho L06/L12/N02 là các notes có locator và catalog phạm vi đọc trong gói. Đây không phải yêu cầu giả định đã đọc toàn bộ công trình hoặc tiến hành lại nghiên cứu của họ.

## Việc cần một thí nghiệm mới được phê duyệt

Những mục sau chỉ bắt buộc nếu muốn nâng phạm vi tuyên bố. Chúng không phải điều kiện bắt buộc để giữ case study mô tả hiện tại và không được thực hiện trong lượt phản biện này.

- **Cải thiện ổn định qua các lần huấn luyện, phần chưa trả lời của RQ1**. Chỉ sau phê duyệt protocol mới, nhiều fit được khóa seed/compute, tuning thích hợp và evaluation mới; các fold/10000 bootstrap không là repeated training.

- `report/chapters/introduction.tex`, PDF vật lý 10 đến 11, mục 1.1.3, RQ1. Anchor `Điều kiện ổn định qua nhiều lần huấn luyện vẫn chưa được kiểm chứng.`

- **Tác động nhân quả của riêng Feature Selection, phần chưa trả lời của RQ2**. Matched ablation với siêu tham số còn lại cố định và selector/tuning nested trong training folds; không sửa hoặc chọn lại theo TEST hiện tại.

- `report/chapters/methodology.tex`, PDF vật lý 25, mục 3.3. Anchor `RF-17 khác RF-42 cả số feature`
- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.2. Anchor `toàn bộ official TRAIN trước development cross-validation`

- **Generalization theo host/session/time hoặc external deployment**. Nguồn dữ liệu có metadata và quyền truy cập phù hợp, đơn vị độc lập được định nghĩa trước, split và preprocessing được khóa; không xem novel-vector là phép thử mới.

- `report/chapters/results_discussion.tex`, PDF vật lý 30, mục 4.6. Anchor `Novel-vector \emph{không} phải bộ dữ liệu kiểm thử độc lập.`
- `report/chapters/dataset_eda.tex`, PDF vật lý 23, mục 2.5. Anchor `Số 8\,541 là \emph{số dòng TEST}`

- **Hiệu quả riêng của resampling/class-weight hoặc cơ chế diversity gây gain**. Đối chứng mới có điều kiện khớp, thực hiện trong training folds; kiểm tra trên dữ liệu đánh giá mới phù hợp sau khi phê duyệt. Chỉ quan sát profile lỗi không đủ chứng minh cơ chế.

- `report/chapters/related_work.tex`, PDF vật lý 17, mục 1.3.2. Anchor `không có so sánh matched resampling/no-resampling`
- `report/chapters/validity_discussion.tex`, PDF vật lý 32, mục 5.2. Anchor `việc cùng xuất hiện chưa xác định feature là nguyên nhân`

## Câu hỏi bảo vệ chuyên sâu

### C-Q01

Nếu phải diễn đạt đóng góp công bố bằng một câu, thông tin mới nào của case study vượt việc áp dụng Stacking/FS đã có, và bảng nào chứng minh thông tin đó?

- `report/chapters/introduction.tex`, PDF vật lý 11, mục 1.1.4. Anchor `Các kết quả đó có thể có giá trị thực nghiệm và phương pháp luận`
- `report/chapters/related_work.tex`, PDF vật lý 17, mục 1.3.1. Anchor `đóng góp được định vị ở kiểm toán case study`

### C-Q02

L06 dùng random80/20, L12 dùng NSL-KDD/CICIDS2017 và N02 gộp các partition trước random split. Vì sao các điểm đã công bố của họ không thể xếp hạng trực tiếp với official TEST của đề tài?

- `literature_reported_facts.csv`, L06, C01 và C02. Anchor `Uses a random80/20 split`
- `literature_reported_facts.csv`, L12, C15, PDF nguồn trang 5 đến 9 theo catalog. Anchor `SMOTE-TOMEK`
- `literature_reported_facts.csv`, N02, C08, Methodology/Data description theo catalog. Anchor `Merges original partitions`

### C-Q03

Với N02 đã có MI-Boruta và stacked ensemble, khác biệt phương pháp nào chỉ là lựa chọn thành phần, và bài học thực nghiệm nào của đề tài đáng trình bày riêng?

- `literature_reported_facts.csv`, N02, C10, Stacked ensemble theo catalog. Anchor `RF/XGB/Catboost`
- `literature_reported_facts.csv`, N02, C09. Anchor `MI and Boruta selected sets are intersected`

### C-Q04

Đối với L08 chỉ có abstract, L09 giữ phạm vi Introduction từ lần đọc trước, N01 và N03 chỉ abstract/identity, những câu nào được phép viết và những khẳng định Methods nào phải để chưa xác minh?

- `literature_scope.json`, record L08, sections_read. Anchor `Publisher abstract and access notice only`
- `literature_scope.json`, record L09, sections_read. Anchor `no new full final Methods/results read`
- `literature_scope.json`, N01, sections_read. Anchor `Publisher abstract/identity/access notice only`

### C-Q05

Tại sao -142 FP và +118 FN chưa đủ kết luận lợi ích tác nghiệp tổng thể, và thông tin về chi phí/prevalence nào cần có trước khi chọn pipeline cho một mạng cụ thể?

- `report/chapters/results_discussion.tex`, PDF vật lý 27, mục 4.2. Anchor `đồng thời tăng \textbf{118 FN}`
- `report/chapters/results_discussion.tex`, PDF vật lý 27, mục 4.2. Anchor `chưa có ma trận chi phí tác nghiệp`

### C-Q06

CI Macro-F1 chứa 0 và McNemar không có ý nghĩa trả lời hai câu hỏi khác nhau thế nào, và vì sao chúng không chứng minh RF-42 và Stacking-42 tương đương?

- `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`, official_test, stacking_42/random_forest_42, macro_f1. Anchor `-0.0003118042125941106,0.0013089503250197615`
- `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`, official_test, stacking_42/random_forest_42. Anchor `0.46837651914684564`
- `report/chapters/conclusion.tex`, PDF vật lý 34, mục 5.8.1. Anchor `không xác nhận ưu thế tổng thể`

### C-Q07

Bằng chứng cụ thể nào nối diversity giữa base learners với kết quả Voting/Stacking, và vì sao error correlation thấp hơn hoặc oracle tốt hơn chưa bảo đảm meta learner học được quy tắc sửa lỗi?

- `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, all_features, decision_tree/random_forest, error_correlation. Anchor `0.49892194038858895`
- `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv`, all_features, hard_voting_lrdtrf. Anchor `0.9473245884056625`
- `report/chapters/validity_discussion.tex`, PDF vật lý 33, Bảng 5.2, RQ3. Anchor `Diversity, OOF, voting, stacking`

### C-Q08

Stable 17 nghĩa là ổn định theo selector/mẫu TRAIN hay ổn định hiệu năng detector? Hãy giải thích năm seed, ngưỡng 0.60 và quy tắc chọn ít nhất hai phương pháp mà không gọi chúng là các mạng độc lập.

- `src/features/select_unsw_features_stage2.py`, configuration. Anchor `STABILITY_MIN_FREQUENCY = 0.60`
- `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`, stable_2plus_methods. Anchor `"stable_2plus_methods"`
- `src/features/select_unsw_features_stage2.py`, configuration. Anchor `SEEDS = [11, 23, 42, 71, 101]`

### C-Q09

Vì sao official TEST vẫn là holdout có ích dù FS đã nhìn toàn TRAIN, trong khi development CV của RF-17 không thể được gọi fully nested hoặc unbiased?

- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.2. Anchor `toàn bộ official TRAIN trước development cross-validation`
- `report/chapters/methodology.tex`, PDF vật lý 24, mục 3.2. Anchor `không lặp hoàn toàn bên trong từng outer fold`

### C-Q10

Nếu muốn kết luận riêng về hiệu quả giảm feature, đối chứng tối thiểu nào phải giữ cố định số cây, kích thước lá và quy trình tuning; vì sao số đo lịch sử hiện tại không đủ cho kết luận đó?

- `report/chapters/methodology.tex`, PDF vật lý 25, mục 3.3. Anchor `RF-17 khác RF-42 cả số feature`
- `report/chapters/results_discussion.tex`, PDF vật lý 30, mục 4.4. Anchor `chi phí quan sát của những cấu hình cụ thể trong lần chạy lịch sử`

### C-Q11

Sau khi đọc P15, nhóm sẽ phân biệt model lịch sử, reconstruction full TRAIN, QA trên TRAIN-derived probe và tái lập hiệu năng TEST bằng những nhãn bằng chứng nào?

- `report/chapters/conclusion.tex`, PDF vật lý 35, mục 5.8.3. Anchor `bản tái dựng full TRAIN chưa thực hiện`
- `results/reproducibility/p15_local_rf17_full_01/run_report.json`, worker_checks.train_rows và artifact.scope. Anchor `RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact`
- `results/reproducibility/p15_local_stack_full_01/run_report.json`, worker_checks.no_test_evaluation. Anchor `"no_test_evaluation": true`
- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`, scope. Anchor `P15_LOCAL_ARTIFACT_READONLY_QA; NOT original model or scientific TEST validation`

### C-Q12

Nếu raw hash trong host report trùng checksum record và mã/config trùng manifest, điều gì đã được xác nhận và điều gì vẫn chưa biết khi reviewer không có raw bytes hoặc model bytes?

- `results/data_audit/unsw_nb15/raw_file_checksums.csv`, UNSW_NB15_training-set.csv, sha256. Anchor `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`
- `results/reproducibility/p15_local_rf42_full_02/run_report.json`, source_hashes. Anchor `"source_hashes"`
- `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`, scope. Anchor `P15_LOCAL_ARTIFACT_READONLY_QA; NOT original model or scientific TEST validation`

### C-Q13

Bootstrap phân tầng cố định số Normal/Attack ước lượng bất định gì, bỏ qua nguồn biến thiên nào, và phải đổi thiết kế ra sao nếu sau này muốn suy luận theo host/session?

- `src/analysis/run_unsw_phase10_statistics.py`, bootstrap_metric_arrays. Anchor `Stratified paired bootstrap conditional on observed Normal/Attack counts.`
- `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`, bootstrap.interpretation. Anchor `does not establish independent network-flow sampling.`

### C-Q14

Novel-vector thấp điểm hơn nhưng vẫn thuộc official TEST. Cần thiết kế tương lai nào để phân biệt hiệu ứng thành phần lớp, vector overlap và generalization theo thời gian mà không chọn lại mô hình từ TEST đã dùng?

- `report/chapters/results_discussion.tex`, PDF vật lý 30, mục 4.6. Anchor `Novel-vector \emph{không} phải bộ dữ liệu kiểm thử độc lập.`
- `report/chapters/dataset_eda.tex`, PDF vật lý 23, mục 2.5. Anchor `Số 8\,541 là \emph{số dòng TEST}`
- `report/chapters/validity_discussion.tex`, PDF vật lý 33, mục 5.6. Anchor `có train/test mới`

## Đánh giá năm tiêu chí chung

**originality**

Tính mới thuật toán không được tuyên bố và không được chứng minh. Giá trị khả dĩ là case study kết hợp kiểm toán, paired effects, loại lỗi và chi phí; cần C-M1 để làm rõ giá trị bổ sung so với L06/L12/N02.

**scientific_importance**

Bài học về chênh lệch metric nhỏ che đổi loại lỗi có ý nghĩa trong đánh giá IDS. Tầm quan trọng hiện ở mức thực nghiệm trên một benchmark, chưa có bằng chứng cho kết luận rộng về hệ thống mạng hoặc Ensemble Learning nói chung.

**interdisciplinary_readership**

Phù hợp nhất với độc giả IDS/ML thực nghiệm, người xây benchmark và nghiên cứu reproducibility. Độc giả rộng hơn có thể quan tâm cách đọc FP/FN và bất định; mức quan tâm liên ngành rộng chưa được xác lập.

**technical_soundness**

Các đếm và effect chính khớp bảng đóng băng đã đọc; ranh giới TRAIN/TEST, binary/attack-family, CI/McNemar và confound FS được nêu. Độ phụ thuộc flow, selector/meta tuning chưa fully nested và thiếu repeated training giới hạn suy luận, nhưng đã được khai báo. Không xác nhận model bytes hoặc tái lập end-to-end từ packet này.

**readability_for_nonspecialists**

Bố cục, phương trình và giải thích FP/FN khá rõ. Không có abstract riêng để đánh giá. Các chi tiết preprocessing/stable feature, design bootstrap và bằng chứng development cần đưa gần nhận định chính hơn; các thuật ngữ Anh-Việt có thể được nhất quán thêm.

## Đề xuất có điều kiện

Sửa C-M1, C-M2 và C-M3 để báo cáo có luận điểm công bố kiểm tra được và trạng thái bằng chứng thống nhất. Chưa có căn cứ bác bỏ case study hẹp, nhưng chưa nên xem bản PDF hiện tại là manuscript hoàn chỉnh.

Sau sửa tài liệu, có thể xem xét như case study IDS/ML với hạn chế. Không bắt buộc thí nghiệm mới để giữ kết luận hẹp, nhưng mọi tuyên bố tăng phạm vi cần protocol mới. Không đề xuất quyết định tạp chí cụ thể.

Định vị phù hợp để tiếp tục hoàn thiện là case study đánh giá IDS minh bạch. Giữ tiêu đề/phụ đề nhị phân UNSW-NB15 hoặc làm phụ đề nhấn mạnh đánh đổi lỗi và protocol. Không tự nâng thành phương pháp ensemble mới, SOTA hoặc hệ thống triển khai. Đề xuất này không thay quyết định biên tập và không cấp P20 final closure.

## Hướng dẫn đã đọc và QA

- `C:/Users/admin/.codex/skills/nature-reviewer/SKILL.md` cùng `references/reviewer-workflow.md`, `references/technical-concern-taxonomy.md`, `references/domain-specific-review-gates.md (phần Engineering và nguyên tắc chung)`, `references/qa-checklist.md`, `references/editorial criteria and processes.md`.
- `C:/Users/admin/.codex/skills/nature-statistics/SKILL.md` cùng `references/statistical-reporting.md`, `references/common-failure-modes.md`, `references/reviewer-checklist.md`.

Đã kiểm tra 12 trục kỹ thuật theo taxonomy; trạng thái từng trục nằm trong report.json theo hợp đồng. Báo cáo chỉ có reviewer C, không dùng kết luận của reviewer khác. Mỗi concern có mức độ, blocking, claim pointer, evidence anchor, điều kiện sửa và đường xử lý. Câu hỏi không được tính là phát hiện lỗi. Không có concern được tạo để đạt một số lượng định trước.

