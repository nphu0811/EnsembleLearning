# PHASE 13.2 — INTRODUCTION + RELATED WORK + METHODOLOGY

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

# Tài liệu tham khảo dùng trong Sections 1–3

[1] B. A. Tama and S. Lim, “Ensemble learning for intrusion detection systems: A systematic mapping study and cross-benchmark evaluation,” *Computer Science Review*, vol. 39, Art. no. 100357, 2021. doi: 10.1016/j.cosrev.2020.100357.

[2] N. Thockchom, M. M. Singh, and U. Nandi, “A novel ensemble learning-based model for network intrusion detection,” *Complex & Intelligent Systems*, vol. 9, pp. 5693–5714, 2023. doi: 10.1007/s40747-023-01013-7.

[3] H. Zouhri, A. Idri, and A. Ratnani, “Evaluating the impact of filter-based feature selection in intrusion detection systems,” *International Journal of Information Security*, vol. 23, pp. 759–785, 2024. doi: 10.1007/s10207-023-00767-y.

[4] M. Cantone, C. Marrocco, and A. Bria, “Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study,” *IEEE Access*, vol. 12, pp. 144489–144508, 2024. doi: 10.1109/ACCESS.2024.3472907.

[5] G. Engelen, V. Rimmer, and W. Joosen, “Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study,” in *2021 IEEE Security and Privacy Workshops (SPW)*, pp. 7–12, 2021. doi: 10.1109/SPW53761.2021.00009.

[6] L. Liu, G. Engelen, T. Lynar, D. Essam, and W. Joosen, “Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018,” in *2022 IEEE Conference on Communications and Network Security (CNS)*, pp. 254–263, 2022. doi: 10.1109/CNS56114.2022.9947235.

[7] N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set),” in *2015 Military Communications and Information Systems Conference (MilCIS)*, pp. 1–6, 2015. doi: 10.1109/MilCIS.2015.7348942.
