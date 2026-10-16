# PHASE 12.3 — LIMITATIONS + CONTRIBUTIONS

> Trạng thái: bản nháp học thuật dùng cho báo cáo.  
> Phạm vi: tổng hợp những giới hạn thực sự của thiết kế hiện tại và những đóng góp có bằng chứng.  
> Nguyên tắc: không biến “contribution” thành claim novelty vượt quá dữ liệu.

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

# 8. Cách trình bày Contributions trong báo cáo

Không nên viết:

> “Đề tài đề xuất một phương pháp ensemble mới vượt trội so với các phương pháp hiện có.”

Vì nghiên cứu hiện tại không phát minh một ensemble algorithm mới và Stacking cũng không chứng minh overall superiority.

Nên viết:

> “Đóng góp của nghiên cứu chủ yếu nằm ở thiết kế và đánh giá thực nghiệm: xây dựng protocol kiểm soát leakage, lựa chọn ensemble dựa trên complementary errors, định lượng performance–cost trade-off của Feature Selection, và sử dụng paired statistical analysis để đánh giá sự khác biệt giữa các pipeline.”

Một phiên bản ngắn hơn để đặt ở Introduction:

> “Nghiên cứu đóng góp một đánh giá thực nghiệm có kiểm soát về Ensemble Learning cho NIDS trên UNSW-NB15, tập trung vào ba khía cạnh thường bị gộp chung trong báo cáo hiệu năng: error complementarity giữa base learners, trade-off giữa predictive performance và computational cost, và độ bất định của chênh lệch giữa ensemble với strong individual baseline.”

---

# 9. Limitations-to-future-work mapping

| Limitation | Future work phù hợp |
|---|---|
| Chỉ có final evidence trên UNSW-NB15 | External validation trên corrected CIC-IDS2017 hoặc dataset khác |
| Binary classification | Multiclass / hierarchical attack classification |
| RQ4 chưa có temporal split | Dataset có timestamp/day/scenario rõ để temporal evaluation |
| Chưa có operational cost function | Cost-sensitive threshold / calibration study trên validation data mới |
| Classical ML scope | DES, online learning, DL chỉ như extension độc lập |
| Compute measurement giới hạn | RAM, energy, throughput, deployment latency |
| Rare attack uncertainty | Dataset lớn hơn hoặc targeted minority-class evaluation |
| Flow dependence | Grouped/session-level resampling khi metadata hỗ trợ |

---

# 10. Research Decisions Log — Phase 12.3

## Decision 1
Không claim algorithmic novelty.

**Reason:** Voting, Stacking, Random Forest và Feature Selection đều là phương pháp đã tồn tại trong literature.

**Consequence:** Contribution được trình bày như methodological + empirical contribution.

## Decision 2
Không claim Stacking superiority.

**Reason:** Macro-F1/MCC paired CI giữa Stacking-42 và RF-42 chứa 0; McNemar-Holm không cho thấy khác biệt overall correctness.

**Consequence:** Stacking được thảo luận như FP/FN trade-off.

## Decision 3
Không gọi novel-vector view là external validation.

**Reason:** Novel-vector subset vẫn thuộc official UNSW-NB15 test.

**Consequence:** Chỉ gọi đây là sensitivity analysis.

## Decision 4
Không coi per-attack miss rate là multiclass performance.

**Reason:** Model được train cho binary target.

**Consequence:** `attack_cat` chỉ dùng cho post-hoc error analysis.

---

# CHECKPOINT — PHASE 12.3

| ID | Task | Status | Evidence |
|---|---|---|---|
| P12-04 | Limitations | DONE | Section 6 |
| P12-05 | Evidence-grounded contributions | DONE | Section 7 |
| P12-06 | Safe contribution wording | DONE | Section 8 |
| P12-07 | Future-work mapping | DONE | Section 9 |
| P12-08 | Contribution decision log | DONE | Section 10 |
| P12-09 | Final Conclusion | TODO | Phase 12.4 |
