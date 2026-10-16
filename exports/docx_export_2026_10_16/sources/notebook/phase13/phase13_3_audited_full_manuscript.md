# Nghiên cứu Ensemble Learning cho bài toán phát hiện xâm nhập mạng

## Tóm tắt

Nghiên cứu này đánh giá Ensemble Learning cho bài toán phát hiện xâm nhập mạng trên UNSW-NB15 theo một protocol kiểm soát leakage và giữ official test độc lập với feature selection, model selection và tuning. Các baseline và ensemble được đánh giá không chỉ bằng Accuracy mà còn bằng Macro-F1, MCC, false-positive rate (FPR), false-negative rate (FNR), chi phí tính toán và paired statistical analysis. Out-of-Fold predictions được sử dụng để phân tích error complementarity trước khi xây dựng Voting và Stacking. Trên official test gồm 82.332 mẫu, Stacking-42 đạt Macro-F1 = 0,8638, còn Random Forest 42 feature (RF-42) đạt 0,8633; paired bootstrap cho chênh lệch Macro-F1 có khoảng tin cậy 95% chứa 0 và McNemar sau hiệu chỉnh Holm không cho thấy khác biệt về overall paired correctness. Tuy nhiên, Stacking-42 giảm FPR nhưng đồng thời tăng FNR so với RF-42, cho thấy lợi ích chính nằm ở sự thay đổi trade-off giữa hai loại lỗi hơn là cải thiện tổng thể. Random Forest 17 feature (RF-17) có Macro-F1 thấp hơn nhẹ nhưng train nhanh hơn khoảng 6,48 lần và giảm kích thước model gần 49%. Cả ba frozen pipeline đều suy giảm trên novel-vector subset. Kết quả cho thấy diversity giữa base learners là hữu ích nhưng không đủ để bảo đảm ensemble superiority; đồng thời nhấn mạnh vai trò của evaluation protocol, uncertainty và performance–cost trade-off khi đánh giá NIDS.

**Từ khóa:** Network Intrusion Detection; Ensemble Learning; Stacking; Random Forest; Feature Selection; Error Diversity; UNSW-NB15.

> Đây chưa phải bản format nộp cuối; nội dung khoa học từ Introduction đến Conclusion đã được nối thành một manuscript thống nhất.

> Bản manuscript nửa đầu, được dựng từ các quyết định đã khóa ở Phase 1–9.  
> Không thay đổi RQ, model, feature set, hyperparameter hoặc evaluation protocol sau khi đã biết final test results.

# 1. Giới thiệu

Network Intrusion Detection System (NIDS) là một thành phần quan trọng trong giám sát an ninh mạng, với nhiệm vụ phân biệt traffic bình thường và traffic có dấu hiệu tấn công. Các phương pháp Machine Learning đã được sử dụng rộng rãi cho bài toán này nhờ khả năng học pattern từ dữ liệu network flow. Tuy nhiên, hiệu năng cao trên benchmark không tự động đồng nghĩa với khả năng tổng quát tốt hoặc giá trị triển khai thực tế. Kết quả NIDS có thể bị ảnh hưởng bởi lựa chọn dataset, cách chia dữ liệu, preprocessing, feature selection, class imbalance và cách báo cáo metric.

Ensemble Learning là một hướng phổ biến nhằm kết hợp nhiều classifier để tận dụng các điểm mạnh khác nhau. Tổng quan hệ thống của Tama và Lim cho thấy hai thành phần quan trọng của ensemble IDS là lựa chọn base classifier và phương pháp kết hợp prediction [1]. Tuy nhiên, việc sử dụng Voting, Bagging, Boosting hoặc Stacking bản thân nó không còn là novelty. Các nghiên cứu gần đây đã áp dụng heterogeneous stacking, feature selection và nhiều benchmark IDS khác nhau [2]. Vì vậy, câu hỏi thực tiễn không chỉ là “ensemble có điểm số cao hơn hay không”, mà còn là liệu phần cải thiện có ổn định, có xuất phát từ complementary errors giữa base learners, và có đáng đổi lấy chi phí tính toán hay không.

Một thách thức khác là độ tin cậy của protocol đánh giá. Các nghiên cứu về dataset quality trên CIC-IDS2017 và CSE-CIC-IDS2018 đã chỉ ra rằng lỗi trong quá trình tạo flow, trích xuất feature hoặc gán nhãn có thể làm thay đổi kết luận benchmark [5], [6]. Các nghiên cứu cross-dataset cũng cho thấy performance rất cao trong một dataset chưa chắc duy trì được khi chuyển sang một dataset hoặc distribution khác [4]. Những kết quả này tạo động lực cho một protocol thận trọng hơn, trong đó data audit, leakage control, final holdout và uncertainty analysis được xem là một phần của thiết kế nghiên cứu thay vì chỉ là bước kỹ thuật phụ.

Nghiên cứu này tập trung vào bài toán binary intrusion detection trên UNSW-NB15. Dataset này được xây dựng tại UNSW Canberra với traffic bình thường hiện đại kết hợp các hành vi tấn công tổng hợp, gồm chín attack families; official partition gồm 175,341 training records và 82,332 testing records [7]. Nghiên cứu sử dụng official split làm benchmark chính và không gộp train/test để random split lại.

Mục tiêu của nghiên cứu không phải đề xuất một ensemble algorithm mới. Thay vào đó, nghiên cứu xây dựng một evaluation workflow nhằm trả lời bốn câu hỏi chính:

**RQ1 — Ensemble effectiveness.** Dưới cùng một leakage-aware protocol, ensemble learning có tạo ra cải thiện ổn định so với các individual/reference model hay không?

**RQ2 — Feature-selection trade-off.** Feature Selection ảnh hưởng thế nào đến predictive performance và computational cost?

**RQ3 — Error complementarity.** Mức cải thiện của ensemble có liên quan đến complementary error patterns giữa base learners hay không?

**RQ4 — Evaluation robustness.** Model ranking và reported performance nhạy thế nào với evaluation protocol/view?

Từ các câu hỏi này, nghiên cứu tập trung vào các đóng góp methodological và empirical: tách rõ development evidence khỏi final holdout evidence; đánh giá Feature Selection dưới góc nhìn performance–cost; lựa chọn ensemble member dựa trên OOF error complementarity; và sử dụng paired statistical analysis để tránh diễn giải quá mức các chênh lệch số học nhỏ.

# 2. Công trình liên quan

## 2.1. Ensemble Learning trong Network Intrusion Detection

Tama và Lim thực hiện systematic mapping và cross-benchmark evaluation về Ensemble Learning cho IDS, nhấn mạnh rằng hiệu quả ensemble phụ thuộc mạnh vào lựa chọn base classifiers và combiner [1]. Kết quả này cho thấy không có cơ sở để giả định rằng chỉ cần kết hợp nhiều model là sẽ tạo ra một classifier tốt hơn.

Thockchom, Singh và Nandi đề xuất một stacking ensemble cho NIDS với Gaussian Naive Bayes, Logistic Regression và Decision Tree ở tầng base, cùng Stochastic Gradient Descent ở tầng meta; mô hình được đánh giá trên KDD99, UNSW-NB15 và CIC-IDS2017 [2]. Nghiên cứu đó cho thấy heterogeneous stacking có thể tận dụng thông tin bổ sung giữa các learner, nhưng đồng thời cũng nhấn mạnh khó khăn của các attack/minority classes.

Trong nghiên cứu hiện tại, ensemble không được chọn chỉ dựa trên individual score. Thay vào đó, OOF predictions được dùng để đo disagreement, double-fault, Q-statistic, error correlation và probability correlation trước khi hình thành heterogeneous ensemble. Cách tiếp cận này nhằm kiểm tra trực tiếp giả thuyết rằng complementary errors có thể tạo giá trị cho ensemble.

## 2.2. Feature Selection và trade-off hiệu năng–chi phí

Feature Selection là một hướng đã được sử dụng rộng rãi trong IDS và không được xem là novelty tự thân. Zouhri, Idri và Ratnani đánh giá nhiều filter-based Feature Selection methods trên các IDS benchmark và cho thấy dimensionality reduction có thể giữ lại hiệu năng trong khi giảm số feature [3].

Nghiên cứu hiện tại mở rộng góc nhìn này bằng cách coi Feature Selection là một experimental factor, không phải một preprocessing step mặc định. Các subset được đánh giá bằng cùng baseline models và cùng validation protocol; ngoài predictive metrics, nghiên cứu đo training time, inference time và serialized model size. Điều này cho phép đánh giá Feature Selection dưới dạng performance–cost trade-off.

## 2.3. Dataset quality và evaluation validity

Engelen, Rimmer và Joosen phân tích CICIDS2017 và chỉ ra nhiều vấn đề trong attack simulation, flow construction, feature extraction và labeling [5]. Liu và cộng sự mở rộng hướng này sang CIC-IDS2017 và CSE-CIC-IDS2018, cho thấy dataset-generation errors có thể xuất hiện ở nhiều giai đoạn của data lifecycle [6].

Các công trình này không chứng minh rằng UNSW-NB15 có cùng loại lỗi, nhưng cung cấp một bài học phương pháp quan trọng: benchmark cần được audit trước khi sử dụng, và các quyết định như deduplication hoặc relabeling không nên thực hiện tự động nếu chưa hiểu nguyên nhân.

Vì vậy, nghiên cứu hiện tại audit UNSW-NB15 trước modeling, kiểm tra missing values, infinity, schema, categorical levels, duplicate feature vectors và train/test overlap. Những collision có conflicting label được giữ nguyên thay vì blind deduplication.

## 2.4. Generalization và độ nhạy của evaluation

Cantone, Marrocco và Bria cho thấy performance của NIDS có thể giảm mạnh trong cross-dataset evaluation, nhấn mạnh khoảng cách giữa within-dataset benchmark score và generalization [4]. Nghiên cứu hiện tại không thực hiện cross-dataset transfer, nhưng sử dụng kết quả đó làm động lực cho việc giữ official holdout độc lập và bổ sung novel-vector sensitivity view.

Do UNSW-NB15 files đang sử dụng không cung cấp một temporal/day/scenario identifier sạch cho direct temporal-split experiment, RQ4 được thiết kế theo hướng “khi dataset hỗ trợ”. Trong implementation cuối, RQ4 được đánh giá một phần bằng cách so sánh development CV, official holdout và novel-vector subset.

# 3. Phương pháp nghiên cứu

## 3.1. Dataset và bài toán

Dataset chính là UNSW-NB15 [7]. Theo nguồn chính thức của UNSW Canberra, dataset bao gồm chín attack families: Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode và Worms. Nghiên cứu sử dụng official predefined partition:

- Training set: 175,341 records.
- Testing set: 82,332 records.

Bài toán chính là binary classification:
- `0`: Normal.
- `1`: Attack.

Cột `label` được dùng làm target. Cột `attack_cat` không được đưa vào model input để tránh target leakage; nó chỉ được giữ làm metadata cho post-hoc attack-family error analysis. Cột `id` cũng bị loại khỏi feature matrix.

Sau khi loại `id`, `attack_cat` và `label`, có 42 modeling features. Ba feature categorical là `proto`, `service` và `state`; các feature còn lại được xử lý như numeric inputs.

## 3.2. Data audit và cleaning policy

Raw files được giữ nguyên và không bị overwrite. Audit cho thấy:
- không có missing values;
- không có positive/negative infinity;
- train và test có schema nhất quán;
- test chứa một số category `state` chưa xuất hiện trong train;
- duplicate feature vectors xuất hiện với tỷ lệ đáng kể;
- 1,302 unique 42-feature vectors xuất hiện ở cả train và test;
- overlap này liên quan tới 10,279 train rows và 8,541 test rows;
- một số duplicate/cross-split vectors có conflicting binary labels.

Vì identical observed feature vectors không phải lúc nào cũng có cùng target, nghiên cứu không áp dụng `drop_duplicates()` một cách mù quáng và không majority-relabel các collision.

Preprocessing policy được khóa như sau:
- categorical encoding fit trên training data only;
- `OneHotEncoder(handle_unknown="ignore")` để xử lý unseen category;
- numeric scaling chỉ dùng cho model cần scaling;
- không fit preprocessing trên test;
- không dùng test để Feature Selection;
- không resample trước split.

## 3.3. Novel-vector sensitivity view

Ngoài official test, nghiên cứu xây dựng một sensitivity view gồm các test sample có complete 42-feature vector chưa từng xuất hiện trong training set.

Official test có 82,332 samples; sau khi loại 8,541 overlapping test rows, novel-vector subset còn 73,791 samples.

Model vẫn được train trên original official TRAIN. Novel-vector subset chỉ là evaluation view bổ sung, không thay thế official benchmark và không được xem là external validation.

## 3.4. Exploratory Data Analysis

EDA được thực hiện trước Feature Selection để mô tả dataset, không dùng test để rank feature. Phân tích bao gồm:
- binary class distribution;
- attack-category distribution;
- descriptive statistics cho numeric features;
- categorical summaries;
- TRAIN-only Normal–Attack separation;
- TRAIN-only Spearman correlation.

EDA cho thấy class prior giữa train và test khác nhau, attack categories mất cân bằng mạnh, nhiều numeric features có correlation rất cao, và một số categorical feature có attack-rate pattern rõ. Những quan sát này tạo cơ sở để đánh giá Feature Selection và lựa chọn metric ngoài Accuracy.

## 3.5. Feature Selection

Feature Selection được thực hiện trên official TRAIN và gồm hai stage.

### 3.5.1. Stage 1 — Candidate generation

Ba family được sử dụng:
1. Mutual Information kết hợp Spearman redundancy pruning.
2. L1 Logistic Regression, aggregate absolute coefficient về original feature.
3. Extra Trees importance, aggregate one-hot importance về original feature.

Mỗi phương pháp sinh Top-20 features; feature xuất hiện trong ít nhất 2/3 phương pháp tạo thành consensus candidate set.

### 3.5.2. Stage 2 — Stability + RFECV

Stability được đánh giá với seeds 11, 23, 42, 71 và 101. Mỗi run dùng 60,000 stratified training rows. Pairwise Jaccard similarity được dùng để đo mức ổn định của selector.

RFECV sử dụng:
- reduced candidate space từ Stage 1;
- 50,000 stratified training rows;
- Logistic Regression L2 estimator;
- 3-fold Stratified CV;
- Macro-F1 làm scoring;
- step bằng 10% transformed features.

Stage 2 tạo ra nhiều candidate subset, trong đó subset “stable in at least two selector families” có 17 original features. Final feature track không được chọn chỉ từ ranking; Phase 6 đánh giá predictive performance và computational cost của nhiều subset.

## 3.6. Baseline development

Ba baseline được sử dụng:
- Logistic Regression;
- Decision Tree;
- Random Forest.

Random Forest là homogeneous ensemble về mặt kỹ thuật, nhưng trong nghiên cứu nó đóng vai trò strong conventional bagging/reference model cho heterogeneous ensemble comparison.

Năm feature tracks được screening:
- all 42 features;
- stable 17;
- RFECV 13;
- stable ∩ RFECV 12;
- stable across all three selector families 7.

Evaluation dùng 3-fold Stratified CV trên official TRAIN. Preprocessing được fit trong từng fold. Metrics gồm:
- Accuracy;
- Balanced Accuracy;
- Precision;
- Recall / Detection Rate;
- F1;
- Macro-F1;
- MCC;
- ROC-AUC;
- PR-AUC;
- FPR;
- FNR;
- training time;
- inference time;
- serialized model size.

Từ development screening, 42-feature track được giữ làm performance-oriented track và 17-feature stable track làm efficiency-oriented track.

## 3.7. OOF diversity analysis

Để kiểm tra RQ3, nghiên cứu tạo Out-of-Fold predictions trên official TRAIN cho:
- Logistic Regression;
- Decision Tree;
- Random Forest;
- AdaBoost.

Mỗi sample chỉ được dự đoán bởi model không train trên sample đó.

Các diversity metric gồm:
- Disagreement Rate;
- Double-Fault Rate;
- Pairwise Oracle Accuracy;
- Q-statistic;
- Error Correlation;
- Probability Correlation.

Base learner selection không dựa trên diversity một mình. Candidate member phải cân bằng:
1. individual predictive strength;
2. complementary errors;
3. computational cost.

Kết quả OOF được dùng để chọn LR + DT + RF cho heterogeneous ensemble.

## 3.8. Voting và Stacking development

Các configuration được so sánh trên cùng outer folds:
- Random Forest;
- AdaBoost;
- Hard Voting (LR + DT + RF);
- Soft Voting (LR + DT + RF);
- Stacking (LR + DT + RF → Logistic Regression meta learner).

Evaluation sử dụng outer 3-fold Stratified CV. Với Stacking, inner 3-fold CV trên outer-training fold tạo OOF base predictions để fit meta learner; outer-validation fold không được dùng để train meta model.

Hai feature tracks được dùng:
- all 42 features;
- stable 17 features.

Phase này chỉ tạo development evidence; official TEST vẫn bị khóa.

## 3.9. Controlled tuning và configuration freeze

Chỉ ba candidate được tune/freeze trước final test:
1. RF-42;
2. Stacking-42;
3. RF-17.

Random Forest dùng compact grid:
- `n_estimators`: 150, 300;
- `min_samples_leaf`: 1, 2, 4;
- `max_features`: `sqrt`, 0.5.

Primary selection metric là Macro-F1 trên TRAIN-only CV.

Final frozen RF configurations:
- RF-42: 300 trees, `max_features=0.5`, `min_samples_leaf=1`;
- RF-17: 150 trees, `max_features=0.5`, `min_samples_leaf=2`.

Stacking-42 dùng:
- base LR: `C=1`, solver `liblinear`;
- base DT: `min_samples_leaf=2`;
- base RF: tuned RF-42;
- meta Logistic Regression: `C=0.5`, no class weighting;
- inner CV: 3 folds;
- decision threshold: 0.5.

Phase 8 có threshold sensitivity diagnostic nhưng threshold không được auto-select từ sweep; final threshold vẫn freeze ở 0.5.

## 3.10. Final holdout evaluation

Phase 9 là lần đầu official TEST được load. Mỗi frozen pipeline được fit trên toàn bộ official TRAIN và evaluate một lần trên:
1. full official test;
2. novel-vector test.

Sau khi TEST được mở:
- không hyperparameter tuning;
- không feature reselection;
- không threshold tuning;
- không thêm/bớt candidate theo test results.

Final metrics gồm predictive performance, confusion counts, training/inference cost, per-attack false negatives và sample-level predictions.

## 3.11. Statistical analysis

Phase 10 không train model. Nó chỉ đọc saved final predictions.

Uncertainty analysis gồm:
- 10,000 stratified paired bootstrap replicates cho Macro-F1, MCC, FPR và FNR;
- paired bootstrap CI cho metric differences giữa model pairs;
- exact two-sided McNemar test cho paired overall correctness;
- Holm correction cho ba pairwise McNemar tests trong mỗi evaluation view;
- Wilson 95% confidence interval cho attack-family miss rates.

McNemar được diễn giải đúng phạm vi: test paired overall error rate, không phải Macro-F1 hoặc MCC.

Bootstrap CI được xem là uncertainty conditional on benchmark rows; nghiên cứu không giả định network flows hoàn toàn độc lập ở population level.

## 3.12. Reproducibility và artifact trail

Mỗi phase lưu lại script, plan/decision artifact và output table tương ứng. Raw data không bị overwrite. Final predictions được lưu ở sample level để statistical analysis có thể tái lập mà không train lại model.

Workflow chính có dạng:

`data audit → EDA → feature selection → baseline screening → OOF diversity → ensemble comparison → controlled tuning → configuration freeze → official holdout → paired statistics → final reporting`.

Cách tổ chức này giúp phân biệt rõ:
- data-development decision;
- model-selection evidence;
- final holdout evidence;
- post-test analysis.

> Chưa bao gồm Discussion, giải thích nguyên nhân sâu, đối chiếu literature hay kết luận tổng quát.

## 4. Kết quả thực nghiệm

## 4.1. Hiệu năng cuối trên official test

Ba pipeline đã được cố định trước khi mở official test gồm Stacking-42, RF-42 và RF-17. Trên tập kiểm thử chính thức, Stacking-42 đạt Macro-F1 = 0.8638 và MCC = 0.7505, trong khi RF-42 đạt Macro-F1 = 0.8633 và MCC = 0.7509. RF-17 đạt Macro-F1 = 0.8607 và MCC = 0.7469. Khoảng tin cậy bootstrap 95% cho Macro-F1 lần lượt là [0.8615, 0.8661] đối với Stacking-42, [0.8610, 0.8657] đối với RF-42 và [0.8583, 0.8630] đối với RF-17.

Mặc dù Stacking-42 có Macro-F1 cao hơn RF-42 một lượng nhỏ, mức chênh lệch chỉ đạt +0.000497. Khoảng tin cậy 95% của chênh lệch này là [-0.000312, +0.001309], bao gồm giá trị 0. Tương tự, chênh lệch MCC giữa hai pipeline không cho thấy lợi thế rõ ràng cho Stacking-42. Kiểm định McNemar sau hiệu chỉnh Holm cho cặp Stacking-42 và RF-42 cho p = 0.4684, do đó chưa có bằng chứng cho thấy hai pipeline khác nhau về tỷ lệ lỗi tổng thể trên cùng tập mẫu kiểm thử.

## 4.2. Trade-off giữa false positive và false negative

Sự khác biệt rõ hơn xuất hiện khi phân tích loại lỗi. Stacking-42 có false-positive rate bằng 26.65%, thấp hơn RF-42 (27.04%). Ngược lại, false-negative rate của Stacking-42 là 1.88%, cao hơn RF-42 (1.62%). Chênh lệch FPR giữa Stacking-42 và RF-42 là -0.003838, với khoảng tin cậy 95% [-0.005243, -0.002432]. Trong khi đó, chênh lệch FNR là +0.002603, với khoảng tin cậy 95% [+0.001853, +0.003375].

Kết quả này cho thấy Stacking-42 chủ yếu thay đổi điểm cân bằng giữa hai dạng lỗi: giảm số cảnh báo giả nhưng đồng thời làm tăng số mẫu tấn công bị bỏ sót. Do đó, khi chỉ xét hiệu năng tổng thể, Stacking-42 và RF-42 gần tương đương; khác biệt nổi bật hơn nằm ở cấu trúc lỗi.

## 4.3. Ảnh hưởng của Feature Selection đến hiệu năng và chi phí

RF-17 sử dụng 17 feature ổn định đạt Macro-F1 = 0.8607, thấp hơn RF-42 (0.8633) một lượng nhỏ. Tuy nhiên, lợi ích tính toán là đáng kể. Thời gian huấn luyện RF-42 là 371.24 giây, trong khi RF-17 chỉ cần 57.26 giây, tương đương nhanh hơn khoảng 6.48 lần. Thời gian suy luận trung bình giảm từ 0.008679 ms/mẫu xuống 0.003562 ms/mẫu. Kích thước model tuần tự hóa cũng giảm từ 205.49 MB xuống 105.04 MB.

Như vậy, việc giảm số feature không cải thiện hiệu năng dự đoán cuối trên official test, nhưng mang lại lợi ích rõ rệt về chi phí huấn luyện, tốc độ suy luận và kích thước mô hình. RF-17 vì thế thể hiện một cấu hình thiên về hiệu quả tính toán hơn là tối đa hóa hiệu năng dự đoán.

## 4.4. Chi phí bổ sung của Stacking

Stacking-42 có thời gian huấn luyện 980.17 giây, cao hơn khoảng 2.64 lần so với RF-42. Thời gian suy luận trung bình của Stacking-42 là 0.012445 ms/mẫu, cũng cao hơn RF-42 (0.008679 ms/mẫu). Tuy nhiên, kích thước model của hai pipeline gần tương đương (206.22 MB so với 205.49 MB).

Kết quả này cho thấy Stacking làm tăng chi phí tính toán đáng kể trong khi mức cải thiện Macro-F1 tổng thể rất nhỏ và không có bằng chứng thống kê rõ ràng về lợi thế tổng thể so với RF-42.

## 4.5. Phân tích lỗi theo attack family

Phân tích false negative theo attack family cho thấy Fuzzers là một trong những nhóm khó phát hiện nhất trong các attack family có số lượng mẫu đủ lớn. Stacking-42 bỏ sót 754/6062 mẫu Fuzzers, tương ứng miss rate = 12.44% (Wilson 95% CI [11.63%, 13.29%]). RF-42 bỏ sót 621/6062 mẫu, tương ứng 10.24%, trong khi RF-17 bỏ sót 623/6062 mẫu, tương ứng 10.28%.

Ngược lại, với nhóm Generic, cả ba pipeline đều có miss rate rất thấp. Stacking-42 bỏ sót 14/18871 mẫu, RF-42 bỏ sót 57/18871 mẫu và RF-17 bỏ sót 3/18871 mẫu. Kết quả này cho thấy không có một pipeline duy nhất đạt ưu thế đồng đều trên mọi attack family.

Các attack family có số lượng mẫu rất nhỏ, chẳng hạn Worms, không được dùng để đưa ra kết luận mạnh chỉ dựa trên tỷ lệ phần trăm, vì độ bất định của ước lượng còn lớn.

## 4.6. Độ nhạy trên novel-vector test

Bên cạnh official test đầy đủ, nghiên cứu còn đánh giá một sensitivity view chỉ gồm các test sample có vector feature chưa từng xuất hiện trong training set. Cả ba pipeline đều giảm Macro-F1 trên novel-vector subset so với official test đầy đủ. Mức giảm lần lượt khoảng 0.0057 đối với Stacking-42, 0.0059 đối với RF-42 và 0.0050 đối với RF-17.

Kết quả này cho thấy hiệu năng của các pipeline có độ nhạy nhất định với các pattern feature chưa xuất hiện trong training set. Tuy nhiên, phân tích này chỉ là sensitivity analysis và không được dùng để khẳng định nguyên nhân của sự suy giảm là temporal drift, domain shift hay một cơ chế cụ thể khác.

## 4.7. Tóm tắt kết quả theo câu hỏi nghiên cứu

RQ1: Stacking-42 không cho thấy lợi thế tổng thể rõ ràng so với RF-42 về Macro-F1, MCC hoặc paired correctness trên official test; khác biệt chính nằm ở trade-off giữa FPR và FNR.

RQ2: Feature Selection làm giảm đáng kể chi phí tính toán nhưng đi kèm một mức giảm nhỏ về hiệu năng dự đoán ở RF-17 so với RF-42.

RQ3: Các model có lỗi bổ sung nhau, nhưng diversity không tự động chuyển thành cải thiện hiệu năng tổng thể; Stacking chủ yếu làm thay đổi phân bố loại lỗi thay vì tạo ra lợi thế rõ ràng về tổng thể.

RQ4: Hiệu năng giảm trên novel-vector subset cho thấy kết quả nhạy với evaluation view, nhưng bằng chứng hiện tại chưa đủ để quy kết nguyên nhân cho temporal hay domain shift.

---


# 5. Thảo luận

## 5.1. Ensemble không tự động tạo ra lợi thế tổng thể

Kết quả của nghiên cứu cho thấy việc kết hợp nhiều base learner không tự động dẫn đến hiệu năng tổng thể cao hơn một mô hình đơn mạnh. Trong giai đoạn development, các base learner có sai số bổ sung nhau: tồn tại những mẫu Logistic Regression hoặc Decision Tree dự đoán đúng trong khi Random Forest dự đoán sai, và ngược lại. Tuy nhiên, Hard Voting và Soft Voting đều không vượt Random Forest về Macro-F1. Khi chuyển sang Stacking, hiệu năng tổng thể được cải thiện nhẹ trên development CV, nhưng lợi thế này gần như biến mất trên official holdout: chênh lệch Macro-F1 giữa Stacking-42 và RF-42 chỉ là +0.000497 và khoảng tin cậy của chênh lệch chứa 0.

Kết quả này phù hợp với nhận định của Tama và Lim [1] rằng hiệu quả của ensemble phụ thuộc không chỉ vào sự tồn tại của nhiều classifier, mà còn vào lựa chọn base classifier và cơ chế kết hợp. Nói cách khác, diversity là điều kiện có ích nhưng không phải điều kiện đủ. Trong thí nghiệm này, các model có lỗi không hoàn toàn trùng nhau, nhưng lượng lỗi được “cứu” bởi ensemble gần cân bằng với lượng lỗi mới xuất hiện sau khi kết hợp. Điều đó giải thích vì sao complementary errors có thể quan sát được nhưng không chuyển thành một lợi thế rõ ràng về Macro-F1 hay MCC.

Kết quả của Stacking cũng cần được hiểu theo hướng này. Stacking-42 không cho thấy ưu thế tổng thể rõ ràng so với RF-42, nhưng lại tạo ra một thay đổi có hệ thống trong cấu trúc lỗi: FPR giảm trong khi FNR tăng. Một cách diễn giải phù hợp với dữ liệu là meta learner đã học một quy tắc kết hợp thận trọng hơn đối với việc dự đoán lớp Attack, qua đó giảm cảnh báo giả nhưng đồng thời bỏ sót thêm một số attack. Tuy nhiên, đây chỉ là diễn giải dựa trên pattern đầu ra; nghiên cứu hiện tại không phân tích trực tiếp hệ số hoặc decision surface của meta learner để chứng minh cơ chế nhân quả này.

Các nghiên cứu stacking trong NIDS, chẳng hạn Thockchom, Singh và Nandi [2], cho thấy heterogeneous ensemble có thể tận dụng thông tin bổ sung giữa các classifier. Kết quả của nghiên cứu hiện tại không phủ nhận lợi ích đó, nhưng bổ sung một điểm quan trọng: khi baseline đơn đã mạnh, mức cải thiện của stacking có thể rất nhỏ và cần được đánh giá cùng uncertainty, FP/FN trade-off và chi phí tính toán thay vì chỉ dựa vào một metric tổng hợp.

## 5.2. Ý nghĩa thực tiễn của trade-off giữa false positive và false negative

Trong NIDS, false positive và false negative không có cùng ý nghĩa vận hành. False positive làm tăng số cảnh báo mà hệ thống hoặc nhân sự an ninh phải xử lý, trong khi false negative tương ứng với traffic tấn công bị bỏ lọt. Vì vậy, việc Stacking-42 giảm FPR nhưng tăng FNR là một trade-off thực tiễn chứ không chỉ là khác biệt thống kê.

Cụ thể, so với RF-42, Stacking-42 giảm FPR khoảng 0.38 điểm phần trăm nhưng tăng FNR khoảng 0.26 điểm phần trăm; cả hai chênh lệch đều có khoảng tin cậy paired bootstrap không chứa 0. Do đó, giá trị của Stacking phụ thuộc vào ưu tiên triển khai. Một môi trường có chi phí xử lý alert giả rất cao có thể quan tâm đến việc giảm FPR, trong khi một môi trường đặt chi phí bỏ lọt attack cao hơn có thể ưu tiên FNR thấp. Nghiên cứu này không gán một hàm chi phí cụ thể cho hai dạng lỗi, nên không đưa ra kết luận rằng một trade-off là “tốt hơn” trade-off còn lại.

Điểm này cũng cho thấy hạn chế của việc chỉ báo cáo Accuracy hoặc ngay cả Macro-F1. Hai pipeline có thể có Macro-F1 gần như bằng nhau nhưng hành vi vận hành khác nhau đáng kể. Vì vậy, FPR và FNR nên được xem là các outcome chính trong đánh giá NIDS, đặc biệt khi ensemble được thiết kế để thay đổi cách kết hợp quyết định của nhiều classifier.

## 5.3. Feature Selection mang lại lợi ích hiệu quả tính toán hơn là tăng hiệu năng

Một kết quả rõ ràng khác là Feature Selection không cải thiện hiệu năng dự đoán cuối trong thiết lập này, nhưng tạo ra lợi ích tính toán đáng kể. RF-17 có Macro-F1 thấp hơn RF-42 một lượng nhỏ, trong khi thời gian train giảm từ khoảng 371 giây xuống 57 giây, inference nhanh hơn khoảng 2.4 lần và kích thước model giảm gần một nửa.

Kết quả này nhất quán về mặt định hướng với literature cho rằng Feature Selection trong IDS cần được đánh giá không chỉ bằng predictive performance mà còn bằng dimensionality và cost. Zouhri, Idri và Ratnani [3] cho thấy nhiều phương pháp filter-based feature selection có thể thay đổi hiệu năng của classifier trên các benchmark NIDS và nhấn mạnh vai trò của việc loại bỏ feature dư thừa. Nghiên cứu hiện tại bổ sung một góc nhìn cụ thể cho UNSW-NB15: 17 feature ổn định không mang lại metric dự đoán cao hơn RF-42, nhưng tạo ra performance–cost trade-off rất rõ.

Do đó, “Feature Selection tốt” trong nghiên cứu này không nên được hiểu là “accuracy tăng”. Giá trị chính của nó nằm ở khả năng giảm resource requirement với mức mất mát predictive performance tương đối nhỏ. Điều này đặc biệt có ý nghĩa trong các kịch bản cần retrain thường xuyên, triển khai nhiều sensor hoặc bị giới hạn CPU/bộ nhớ. Tuy nhiên, nghiên cứu chưa đo trực tiếp mức sử dụng RAM, năng lượng hoặc throughput mạng thực tế, nên kết luận về deployment efficiency chỉ giới hạn ở train time, inference time và serialized model size.

## 5.4. Khoảng cách giữa development CV và official holdout nhấn mạnh vấn đề generalization

Một trong những quan sát đáng chú ý nhất là performance trên official holdout thấp hơn đáng kể so với development CV. Trong development, RF-42 và Stacking-42 đạt Macro-F1 xấp xỉ 0.95, trong khi trên official test giá trị giảm xuống khoảng 0.86. Điều này cho thấy kết quả cross-validation trên official TRAIN đã lạc quan hơn đáng kể so với performance trên holdout được khóa.

Nghiên cứu hiện tại chưa đủ bằng chứng để quy sự suy giảm này cho một nguyên nhân duy nhất. Một số khác biệt đã được quan sát giữa train và test, bao gồm class-prior shift, sự xuất hiện của các category `state` chưa thấy trong train, và sự tồn tại của các feature vector mới trong test. Các yếu tố này có thể góp phần làm thay đổi độ khó của test set, nhưng thí nghiệm hiện tại không tách riêng tác động nhân quả của từng yếu tố.

Kết quả novel-vector sensitivity củng cố nhận định rằng khả năng tổng quát không nên được suy ra chỉ từ random/development CV. Cả ba pipeline đều giảm Macro-F1 khi chỉ đánh giá trên các test vector chưa từng xuất hiện trong train. Tuy vậy, novel-vector subset vẫn thuộc cùng benchmark UNSW-NB15; nó không tương đương với external validation hoặc cross-dataset testing.

Điểm này có cùng hướng với nghiên cứu cross-dataset của Cantone, Marrocco và Bria [4], nơi các tác giả nhấn mạnh rằng hiệu năng cao trong một dataset không đảm bảo khả năng tổng quát sang network/dataset khác. Tuy nhiên, hai thiết kế không tương đương: nghiên cứu hiện tại chỉ đánh giá official holdout và novel-vector subset trong UNSW-NB15, còn Cantone và cộng sự thực hiện cross-dataset generalization. Vì vậy, kết quả của họ được dùng để đặt kết quả hiện tại vào bối cảnh generalization rộng hơn, không phải để chứng minh rằng nghiên cứu này đã thực hiện external validation.

## 5.5. Error analysis theo attack family cho thấy metric tổng hợp che giấu khác biệt cục bộ

Phân tích theo attack family cho thấy một pipeline có thể hoạt động tốt với một nhóm attack nhưng kém hơn với nhóm khác. Fuzzers là ví dụ rõ nhất: miss rate của Stacking-42 cao hơn RF-42 và RF-17, trong khi với Generic thì cả ba pipeline đều có miss rate rất thấp và thứ tự giữa chúng khác với Fuzzers.

Điều này giải thích vì sao complementary errors có thể tồn tại dù metric tổng hợp gần như ngang nhau. Một base learner có thể đóng góp mạnh cho một vùng nhỏ của feature space hoặc một attack family nhưng không đủ để thay đổi Macro-F1 toàn cục. Kết quả này cũng phù hợp với literature stacking NIDS trong đó performance trên minority hoặc attack-specific classes vẫn là vấn đề ngay cả khi aggregate performance cao, như được thảo luận trong Thockchom và cộng sự [2].

Tuy nhiên, cần thận trọng với các attack family rất nhỏ. Ví dụ Worms chỉ có 44 mẫu trong official test. Với sample size như vậy, một vài lỗi thêm hoặc bớt có thể thay đổi tỷ lệ phần trăm rất mạnh. Vì vậy, nghiên cứu sử dụng Wilson confidence interval và không dùng các rare family này để đưa ra kết luận mạnh về thứ hạng giữa model.

## 5.6. Kết quả cũng nhấn mạnh vai trò của dataset audit và protocol đánh giá

Mặc dù dataset chính của nghiên cứu là UNSW-NB15, việc audit dữ liệu ngay từ đầu cho thấy benchmark không nên được xem như một nguồn dữ liệu “hoàn hảo” chỉ vì nó được sử dụng phổ biến. Nghiên cứu phát hiện nhiều feature vector lặp lại trong train/test, một số nhóm duplicate feature vector có conflicting label, và overlap giữa train và test. Vì chưa xác định được nguyên nhân tạo ra các collision này, nghiên cứu không thực hiện blind deduplication hoặc tự động relabel.

Cách tiếp cận thận trọng này phù hợp với bài học phương pháp luận từ Engelen, Rimmer và Joosen [5] cũng như Liu và cộng sự [6], những nghiên cứu cho thấy lỗi trong quá trình tạo dataset, feature extraction và labeling có thể ảnh hưởng mạnh đến benchmark NIDS. Hai công trình đó tập trung vào CIC-IDS2017/CSE-CIC-IDS2018 chứ không phải UNSW-NB15, nên chúng không phải bằng chứng rằng UNSW-NB15 có cùng lỗi. Chúng được dùng để hỗ trợ nguyên tắc phương pháp: dataset audit và provenance cần được kiểm tra trước khi diễn giải điểm số mô hình.

Điều này cũng giải thích tại sao nghiên cứu giữ official test khóa cho tới sau khi hoàn thành Feature Selection, model comparison, diversity analysis và tuning. Việc tách development evidence khỏi final holdout giúp giảm nguy cơ chọn model dựa trên test và làm cho khoảng cách giữa CV và final test trở thành một kết quả có ý nghĩa thay vì bị che khuất bởi post-test tuning.


# 6. Hạn chế của nghiên cứu

## 6.1. Phạm vi đánh giá tập trung chủ yếu trên một benchmark

Nghiên cứu sử dụng UNSW-NB15 làm dataset chính và toàn bộ kết luận thực nghiệm cuối cùng hiện được rút ra từ benchmark này. Mặc dù official holdout được giữ khóa cho tới sau giai đoạn model selection, kết quả vẫn phản ánh đặc điểm của một dataset cụ thể. Vì vậy, nghiên cứu chưa đủ cơ sở để khẳng định rằng thứ hạng giữa Random Forest, Stacking và các cấu hình giảm feature sẽ giữ nguyên trên các network environment khác.

Một secondary dataset đã được định hướng từ giai đoạn thiết kế, nhưng chưa được dùng để đưa ra kết luận cuối trong chuỗi thí nghiệm hiện tại. Do đó, external validity của kết quả vẫn còn hạn chế.

**Cách viết an toàn:**  
“Kết quả cho thấy hành vi của các pipeline trên UNSW-NB15; khả năng khái quát sang dataset hoặc môi trường mạng khác cần được kiểm chứng thêm.”

---

## 6.2. Bài toán chính là binary intrusion detection

Biến `label` được sử dụng làm target chính, trong khi `attack_cat` chỉ được giữ lại như metadata để phân tích false negative theo từng attack family. Vì vậy, nghiên cứu đánh giá khả năng phân biệt Normal và Attack, chứ không tối ưu trực tiếp cho bài toán multiclass phân biệt từng họ tấn công.

Điều này đặc biệt quan trọng đối với các attack family hiếm như Worms, Shellcode hoặc Backdoor. Mặc dù nghiên cứu có báo cáo miss rate theo từng family, các kết quả đó không tương đương với một multiclass classifier được huấn luyện riêng để nhận diện từng loại tấn công.

**Cách viết an toàn:**  
“Per-attack analysis trong nghiên cứu là error analysis của binary detector, không phải kết quả multiclass attack classification.”

---

## 6.3. RQ4 mới được trả lời một phần

Thiết kế ban đầu mong muốn đánh giá độ nhạy của kết quả với evaluation protocol, bao gồm khả năng so sánh conventional random split với temporal/day/scenario split khi dữ liệu hỗ trợ. Tuy nhiên, các file UNSW-NB15 đang sử dụng không cung cấp một biến temporal/day/scenario đủ sạch để xây dựng thí nghiệm như vậy mà không đưa thêm giả định khó kiểm chứng.

Nghiên cứu vì thế sử dụng official holdout và novel-vector sensitivity view. Kết quả cho thấy cả ba pipeline đều giảm performance trên các vector feature chưa xuất hiện trong training set, nhưng thí nghiệm này không thể xác định nguyên nhân của sự suy giảm là temporal drift, domain shift hay một cơ chế cụ thể khác.

**Cách viết an toàn:**  
“RQ4 được trả lời một phần thông qua official-holdout và novel-vector sensitivity, nhưng chưa có temporal split trực tiếp.”

---

## 6.4. Development CV có thể chịu selection-induced optimism

Feature Selection được thực hiện trên official TRAIN và các candidate subset sau đó được dùng trong development CV. Mặc dù preprocessing bên trong mỗi fold được fit theo cách leakage-safe và official TEST không được dùng cho selection, việc chọn candidate feature subset từ toàn bộ official TRAIN có thể tạo ra một mức optimism ở tầng model-development.

Vì lý do đó, nghiên cứu không xem các điểm development CV là ước lượng cuối cùng của generalization performance. Official TEST chỉ được mở sau khi pipeline đã được freeze, và chính kết quả holdout mới được dùng làm bằng chứng chính trong phần kết luận.

**Cách viết an toàn:**  
“Development CV được xem là model-selection evidence; final claims dựa trên frozen official holdout.”

---

## 6.5. Duplicate/overlap feature vectors chưa được xác định nguyên nhân

Data audit phát hiện nhiều feature vector lặp lại trong train và test, đồng thời có một số collision với conflicting label. Do chưa có bằng chứng đủ để xác định các hàng này là lỗi dữ liệu, duplicate hợp lệ hay hệ quả của cách xây dựng flow, nghiên cứu không thực hiện blind deduplication hoặc majority relabeling.

Quyết định này tránh việc tự ý thay đổi benchmark, nhưng đồng thời có nghĩa là ảnh hưởng chính xác của các feature-vector collision chưa được tách riêng hoàn toàn. Novel-vector test được xây dựng như một sensitivity analysis để đánh giá một phần vấn đề này, không phải để thay thế official benchmark.

---

## 6.6. Phạm vi model family còn giới hạn

Nghiên cứu tập trung vào các classical machine-learning model và ensemble tiêu biểu gồm Logistic Regression, Decision Tree, Random Forest, AdaBoost, Voting và Stacking. Các hướng như deep learning, Dynamic Ensemble Selection, online learning hoặc anomaly-detection architecture chuyên biệt chưa được đánh giá trong final protocol.

Đây là một giới hạn về phạm vi so sánh, nhưng cũng là chủ ý thiết kế nhằm giữ experiment tractable và bảo đảm so sánh leakage-aware, có statistical analysis và cost measurement trong thời gian nghiên cứu.

**Không nên viết:**  
“Random Forest là model tốt nhất cho NIDS.”

**Nên viết:**  
“Trong phạm vi các pipeline được đánh giá, RF-42 là strong individual/reference model.”

---

## 6.7. Threshold và operational cost chưa được tối ưu theo môi trường triển khai

Các final pipeline sử dụng decision threshold = 0.5 đã được freeze trước khi mở TEST. Phase 8 có thực hiện threshold sensitivity analysis, nhưng threshold không được đổi chỉ để tối đa hóa metric development.

Cách làm này bảo vệ tính hợp lệ của final holdout, nhưng đồng thời nghiên cứu chưa tối ưu threshold theo một operational cost function cụ thể, chẳng hạn chi phí của một false negative cao gấp nhiều lần false positive.

Do đó, trade-off FPR/FNR được báo cáo dưới dạng quan sát thực nghiệm, không được chuyển thành một quyết định deployment tối ưu.

---

## 6.8. Computational cost phụ thuộc môi trường chạy

Train time, inference time và serialized model size được đo trong cùng workflow thực nghiệm và hữu ích cho so sánh tương đối giữa các pipeline. Tuy nhiên, các giá trị tuyệt đối sẽ phụ thuộc CPU, RAM, phiên bản thư viện, mức song song hóa và cấu hình hệ thống.

Nghiên cứu cũng chưa đo trực tiếp:
- peak RAM,
- energy consumption,
- network throughput,
- latency dưới tải thực,
- chi phí triển khai phân tán.

Vì vậy, kết luận về efficiency nên được hiểu là relative computational trade-off trong môi trường thí nghiệm, không phải benchmark phần cứng phổ quát.

---

## 6.9. Bootstrap uncertainty không loại bỏ hoàn toàn dependence giữa network flows

Phase 10 sử dụng paired bootstrap và Wilson interval để lượng hóa uncertainty. Các interval này hữu ích cho việc tránh diễn giải quá mức các chênh lệch rất nhỏ giữa model.

Tuy nhiên, các network flow trong một benchmark có thể không hoàn toàn độc lập theo nghĩa thống kê. Vì vậy, bootstrap CI nên được hiểu là uncertainty conditional on the observed benchmark rows, không phải bảo đảm population-level uncertainty cho mọi traffic distribution ngoài thực tế.

---

# 7. Đóng góp của nghiên cứu

## 7.1. Xây dựng một evaluation protocol có kiểm soát leakage và giữ final holdout độc lập với model selection

Đóng góp đầu tiên của nghiên cứu là xây dựng một workflow thực nghiệm trong đó raw data được giữ nguyên, preprocessing/encoding/scaling được fit trên TRAIN, official TEST không được dùng cho Feature Selection, ensemble selection hoặc tuning, và pipeline được freeze trước khi mở holdout.

Điểm này không được trình bày như một thuật toán mới. Giá trị của nó nằm ở methodological rigor: development evidence và final generalization evidence được tách rõ, giúp phát hiện khoảng cách đáng kể giữa CV performance và official-test performance.

**Contribution statement đề xuất:**  
“Nghiên cứu xây dựng và áp dụng một leakage-aware, holdout-preserving evaluation protocol cho so sánh individual và ensemble classifiers trên UNSW-NB15.”

---

## 7.2. Đánh giá ensemble dựa trên error complementarity thay vì chỉ dựa trên sức mạnh từng model

Thay vì chọn base learner chỉ vì từng model có điểm số cao, nghiên cứu sử dụng OOF predictions để phân tích disagreement, double-fault, error correlation và pairwise oracle behavior. Nhờ đó, lựa chọn LR + DT + RF cho heterogeneous ensemble được hỗ trợ bởi evidence về vai trò và pattern lỗi khác nhau.

Kết quả cuối cho thấy complementary errors thực sự tồn tại nhưng không tự động tạo ra ensemble gain. Đây là một empirical finding quan trọng của nghiên cứu.

**Contribution statement đề xuất:**  
“Nghiên cứu liên kết base-learner selection với OOF error complementarity và kiểm chứng rằng diversity là điều kiện hữu ích nhưng không đủ để bảo đảm ensemble superiority.”

---

## 7.3. So sánh Voting và Stacking trong cùng paired protocol và ghi nhận negative result một cách minh bạch

Hard Voting và Soft Voting không vượt strong Random Forest baseline trong development analysis, trong khi Stacking chỉ tạo ra một cải thiện rất nhỏ về metric tổng hợp và chủ yếu thay đổi FP/FN trade-off.

Việc giữ lại negative result này là một đóng góp về bằng chứng thực nghiệm: nghiên cứu không giả định rằng “ensemble phải tốt hơn” và không loại bỏ các kết quả bất lợi cho giả thuyết ban đầu.

**Contribution statement đề xuất:**  
“Kết quả cho thấy cách kết hợp prediction quan trọng hơn bản thân việc sử dụng nhiều classifier; Voting không tạo lợi thế so với RF, còn Stacking chủ yếu thay đổi cấu trúc lỗi.”

---

## 7.4. Đánh giá Feature Selection theo performance–cost trade-off

Nghiên cứu không chỉ hỏi feature subset nào cho metric cao nhất mà còn đo:
- Macro-F1,
- MCC,
- FPR/FNR,
- training time,
- inference time,
- model size.

Kết quả RF-17 cho thấy một cấu hình giảm feature có thể mất một lượng nhỏ predictive performance nhưng giảm rất mạnh compute requirement.

**Contribution statement đề xuất:**  
“Nghiên cứu định lượng trade-off giữa predictive performance và computational efficiency của feature reduction thay vì đánh giá Feature Selection chỉ bằng Accuracy.”

---

## 7.5. Kết hợp point estimates với paired statistical uncertainty

Final comparison không chỉ dựa trên mean score. Nghiên cứu sử dụng:
- bootstrap confidence interval cho metric,
- paired bootstrap cho chênh lệch metric,
- exact McNemar test cho paired correctness,
- Holm correction cho multiple pairwise comparisons,
- Wilson interval cho attack-family miss rate.

Nhờ đó, chênh lệch Macro-F1 rất nhỏ giữa Stacking-42 và RF-42 không bị diễn giải sai thành superiority, trong khi thay đổi FPR/FNR lại được nhận diện rõ hơn.

**Contribution statement đề xuất:**  
“Nghiên cứu bổ sung uncertainty-aware paired comparison để phân biệt giữa chênh lệch số học nhỏ và khác biệt có bằng chứng rõ hơn trong cấu trúc lỗi.”

---

## 7.6. Bổ sung novel-vector sensitivity bên cạnh official benchmark

Do data audit phát hiện overlap của feature vectors giữa train và test, nghiên cứu xây dựng thêm novel-vector test view gồm các test sample có complete feature vector chưa xuất hiện trong TRAIN.

View này không thay thế official test, nhưng cung cấp một robustness/sensitivity check bổ sung. Kết quả cho thấy cả ba pipeline đều giảm performance trên novel vectors.

**Contribution statement đề xuất:**  
“Nghiên cứu bổ sung một novel-vector sensitivity view để đánh giá mức suy giảm khi loại khỏi test các vector đã từng xuất hiện trong training set.”

---

## 7.7. Phân tích attack-specific errors của binary detector thay vì chỉ báo cáo aggregate metric

Bằng cách giữ `attack_cat` làm metadata, nghiên cứu có thể xác định rằng Fuzzers tạo miss rate cao hơn nhiều attack family khác và rằng thứ tự giữa model thay đổi theo từng family.

Điều này cho thấy aggregate Macro-F1 có thể che khuất local failure modes. Tuy nhiên, contribution này được giới hạn đúng phạm vi: đây là error analysis của binary detector, không phải multiclass attack classification.

---

## 7.8. Tạo workflow reproducible từ audit đến final reporting

Toàn bộ pipeline được lưu thành:
- scripts theo phase,
- planning/decision markdown,
- intermediate CSV,
- OOF predictions,
- final predictions,
- statistical tables,
- final figures.

Điều này cho phép tái tạo các bước chính từ data audit, Feature Selection, model comparison, tuning, final holdout đến statistical analysis và reporting.

**Contribution statement đề xuất:**  
“Nghiên cứu cung cấp một reproducible experimental workflow với artifact evidence cho từng quyết định chính.”

---


# 8. Kết luận

Nghiên cứu này khảo sát hiệu quả của Ensemble Learning cho bài toán phát hiện xâm nhập mạng trên UNSW-NB15 theo một quy trình thực nghiệm kiểm soát leakage, giữ official test độc lập với giai đoạn Feature Selection, model comparison và tuning. Thay vì chỉ so sánh Accuracy hoặc chọn mô hình có điểm số cao nhất, nghiên cứu đánh giá đồng thời hiệu năng dự đoán, cấu trúc lỗi, error complementarity giữa các base learner, chi phí tính toán và độ bất định thống kê.

Kết quả cho thấy Random Forest là một strong individual/reference model trong phạm vi các pipeline được khảo sát. Hard Voting và Soft Voting không cải thiện Macro-F1 so với Random Forest trong development analysis. Stacking tận dụng được thông tin bổ sung giữa Logistic Regression, Decision Tree và Random Forest tốt hơn Voting, nhưng trên official holdout không cho thấy ưu thế tổng thể rõ ràng so với RF-42 về Macro-F1, MCC hoặc overall paired correctness.

Sự khác biệt đáng chú ý nhất giữa Stacking-42 và RF-42 nằm ở cấu trúc lỗi. Stacking-42 giảm false-positive rate nhưng đồng thời tăng false-negative rate. Vì vậy, tác động chính của Stacking trong nghiên cứu này không phải là tạo ra một mô hình vượt trội toàn diện, mà là dịch chuyển điểm cân bằng giữa cảnh báo giả và tấn công bị bỏ sót. Kết quả này nhấn mạnh rằng trong NIDS, việc đánh giá ensemble chỉ dựa trên một metric tổng hợp có thể che khuất những khác biệt vận hành quan trọng.

Feature Selection cũng thể hiện một trade-off rõ ràng. RF-17 có hiệu năng dự đoán thấp hơn RF-42 một lượng nhỏ trên official test, nhưng giảm mạnh thời gian huấn luyện, thời gian suy luận và kích thước mô hình. Do đó, lợi ích nổi bật của Feature Selection trong nghiên cứu này nằm ở computational efficiency hơn là cải thiện predictive performance.

Phân tích diversity cho thấy các base learner có complementary errors, nhưng sự tồn tại của diversity không tự động bảo đảm ensemble gain. Kết quả Hard/Soft Voting và Stacking cho thấy hiệu quả cuối cùng phụ thuộc không chỉ vào việc các model mắc lỗi khác nhau, mà còn vào cách các prediction được kết hợp.

Ngoài ra, official-holdout performance thấp hơn đáng kể so với development CV, và cả ba frozen pipeline đều giảm performance trên novel-vector subset. Kết quả này cho thấy đánh giá NIDS nhạy với evaluation protocol/view và nhấn mạnh tầm quan trọng của việc giữ final holdout độc lập. Tuy nhiên, nghiên cứu hiện tại chưa đủ bằng chứng để quy sự suy giảm này cho temporal drift hoặc domain shift cụ thể.

---

## 8.1. Trả lời các câu hỏi nghiên cứu

### RQ1 — Ensemble có cải thiện ổn định so với model đơn mạnh hay không?

**Kết luận:** Chưa có bằng chứng cho thấy Stacking-42 cải thiện tổng thể một cách rõ ràng so với RF-42 trên official test.

Stacking-42 có Macro-F1 cao hơn RF-42 một lượng rất nhỏ, nhưng paired bootstrap CI của chênh lệch chứa 0; MCC cũng không cho thấy lợi thế rõ. Exact McNemar sau Holm correction không cho thấy khác biệt về overall paired correctness.

Tuy nhiên, Stacking-42 tạo ra một trade-off có bằng chứng rõ hơn:
- FPR thấp hơn,
- FNR cao hơn.

Vì vậy, ensemble trong nghiên cứu này không thể được kết luận là “tốt hơn” strong baseline một cách tổng quát.

---

### RQ2 — Feature Selection ảnh hưởng thế nào đến hiệu năng và chi phí?

**Kết luận:** Feature Selection tạo ra computational gain lớn với một predictive cost nhỏ.

RF-17:
- train nhanh hơn đáng kể RF-42,
- inference nhanh hơn,
- model nhỏ hơn gần một nửa,
- nhưng Macro-F1/MCC thấp hơn một lượng nhỏ trên official test.

Vì vậy, Feature Selection nên được xem như một công cụ tối ưu performance–cost trade-off thay vì một cơ chế bảo đảm tăng Accuracy.

---

### RQ3 — Ensemble improvement có liên quan đến complementary errors hay không?

**Kết luận:** Complementary errors tồn tại, nhưng không đủ để bảo đảm ensemble superiority.

OOF analysis cho thấy LR, DT và RF có những vùng lỗi khác nhau và có khả năng “cứu” nhau ở một số sample. Tuy nhiên:
- Voting không vượt RF,
- Stacking chỉ cải thiện rất nhỏ về aggregate metric,
- lợi ích rõ hơn nằm ở việc thay đổi FP/FN trade-off.

Do đó, diversity là điều kiện hữu ích cho ensemble design nhưng không phải điều kiện đủ cho net performance gain.

---

### RQ4 — Kết quả nhạy thế nào với evaluation protocol/view?

**Kết luận:** Performance nhạy với evaluation view, nhưng RQ4 chỉ được trả lời một phần.

Các model đạt điểm development CV cao hơn đáng kể so với official holdout, và performance tiếp tục giảm trên novel-vector test. Điều này cho thấy generalization estimate phụ thuộc vào cách đánh giá.

Tuy nhiên, nghiên cứu chưa thực hiện được temporal/day/scenario split trực tiếp, nên chưa thể kết luận nguyên nhân của sự suy giảm là temporal drift hoặc domain shift.

---

## 8.2. Hàm ý thực tiễn

Nếu mục tiêu là tối đa hóa predictive performance trong các pipeline đã đánh giá, RF-42 là một strong reference với hiệu năng tổng thể gần Stacking-42 nhưng chi phí thấp hơn đáng kể.

Nếu ưu tiên giảm false alarms, Stacking-42 có thể hấp dẫn hơn, nhưng phải chấp nhận FNR cao hơn.

Nếu ưu tiên computational efficiency, RF-17 là lựa chọn hợp lý nhờ giảm đáng kể training/inference cost và model size với mức giảm predictive performance tương đối nhỏ.

Do đó, nghiên cứu không đề xuất một “mô hình tốt nhất tuyệt đối”. Lựa chọn pipeline phụ thuộc vào trade-off giữa:
- detection performance,
- false alarms,
- missed attacks,
- computational cost,
- yêu cầu triển khai.

---

## 8.3. Hướng phát triển tiếp theo

Các hướng nghiên cứu tiếp theo phù hợp nhất gồm:

- external validation trên corrected CIC-IDS2017 hoặc một benchmark độc lập khác;
- multiclass hoặc hierarchical attack classification;
- temporal/scenario-aware evaluation khi dataset hỗ trợ metadata phù hợp;
- cost-sensitive thresholding trên một validation protocol mới, không tái sử dụng official test;
- nghiên cứu Dynamic Ensemble Selection như một extension độc lập;
- đo thêm RAM, throughput, latency và energy cost;
- grouped/session-level statistical resampling nếu có metadata phù hợp;
- đánh giá robustness trên attack family hiếm với sample size lớn hơn.

---

# Tài liệu tham khảo

[1] B. A. Tama and S. Lim, “Ensemble learning for intrusion detection systems: A systematic mapping study and cross-benchmark evaluation,” *Computer Science Review*, vol. 39, Art. no. 100357, 2021. doi: 10.1016/j.cosrev.2020.100357.

[2] N. Thockchom, M. M. Singh, and U. Nandi, “A novel ensemble learning-based model for network intrusion detection,” *Complex & Intelligent Systems*, vol. 9, pp. 5693–5714, 2023. doi: 10.1007/s40747-023-01013-7.

[3] H. Zouhri, A. Idri, and A. Ratnani, “Evaluating the impact of filter-based feature selection in intrusion detection systems,” *International Journal of Information Security*, vol. 23, pp. 759–785, 2024. doi: 10.1007/s10207-023-00767-y.

[4] M. Cantone, C. Marrocco, and A. Bria, “Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study,” *IEEE Access*, vol. 12, pp. 144489–144508, 2024. doi: 10.1109/ACCESS.2024.3472907.

[5] G. Engelen, V. Rimmer, and W. Joosen, “Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study,” in *2021 IEEE Security and Privacy Workshops (SPW)*, pp. 7–12, 2021. doi: 10.1109/SPW53761.2021.00009.

[6] L. Liu, G. Engelen, T. Lynar, D. Essam, and W. Joosen, “Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018,” in *2022 IEEE Conference on Communications and Network Security (CNS)*, pp. 254–263, 2022. doi: 10.1109/CNS56114.2022.9947235.

[7] N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set),” in *2015 Military Communications and Information Systems Conference (MilCIS)*, pp. 1–6, 2015. doi: 10.1109/MilCIS.2015.7348942.
