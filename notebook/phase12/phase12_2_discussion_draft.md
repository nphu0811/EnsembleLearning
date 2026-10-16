# PHASE 12.2 — DRAFT PHẦN THẢO LUẬN (DISCUSSION)

> Trạng thái: bản nháp học thuật.  
> Phạm vi: diễn giải ý nghĩa của kết quả Phase 10–11 và đối chiếu với literature đã rà soát.  
> Không thay đổi mô hình, feature, threshold hoặc kết quả sau khi official test đã được mở.

## 5. Thảo luận

### 5.1. Ensemble không tự động tạo ra lợi thế tổng thể

Kết quả của nghiên cứu cho thấy việc kết hợp nhiều base learner không tự động dẫn đến hiệu năng tổng thể cao hơn một mô hình đơn mạnh. Trong giai đoạn development, các base learner có sai số bổ sung nhau: tồn tại những mẫu Logistic Regression hoặc Decision Tree dự đoán đúng trong khi Random Forest dự đoán sai, và ngược lại. Tuy nhiên, Hard Voting và Soft Voting đều không vượt Random Forest về Macro-F1. Khi chuyển sang Stacking, hiệu năng tổng thể được cải thiện nhẹ trên development CV, nhưng lợi thế này gần như biến mất trên official holdout: chênh lệch Macro-F1 giữa Stacking-42 và RF-42 chỉ là +0.000497 và khoảng tin cậy của chênh lệch chứa 0.

Kết quả này phù hợp với nhận định của Tama và Lim (2021) rằng hiệu quả của ensemble phụ thuộc không chỉ vào sự tồn tại của nhiều classifier, mà còn vào lựa chọn base classifier và cơ chế kết hợp. Nói cách khác, diversity là điều kiện có ích nhưng không phải điều kiện đủ. Trong thí nghiệm này, các model có lỗi không hoàn toàn trùng nhau, nhưng lượng lỗi được “cứu” bởi ensemble gần cân bằng với lượng lỗi mới xuất hiện sau khi kết hợp. Điều đó giải thích vì sao complementary errors có thể quan sát được nhưng không chuyển thành một lợi thế rõ ràng về Macro-F1 hay MCC.

Kết quả của Stacking cũng cần được hiểu theo hướng này. Stacking-42 không cho thấy ưu thế tổng thể rõ ràng so với RF-42, nhưng lại tạo ra một thay đổi có hệ thống trong cấu trúc lỗi: FPR giảm trong khi FNR tăng. Một cách diễn giải phù hợp với dữ liệu là meta learner đã học một quy tắc kết hợp thận trọng hơn đối với việc dự đoán lớp Attack, qua đó giảm cảnh báo giả nhưng đồng thời bỏ sót thêm một số attack. Tuy nhiên, đây chỉ là diễn giải dựa trên pattern đầu ra; nghiên cứu hiện tại không phân tích trực tiếp hệ số hoặc decision surface của meta learner để chứng minh cơ chế nhân quả này.

Các nghiên cứu stacking trong NIDS, chẳng hạn Thockchom, Singh và Nandi (2023), cho thấy heterogeneous ensemble có thể tận dụng thông tin bổ sung giữa các classifier. Kết quả của nghiên cứu hiện tại không phủ nhận lợi ích đó, nhưng bổ sung một điểm quan trọng: khi baseline đơn đã mạnh, mức cải thiện của stacking có thể rất nhỏ và cần được đánh giá cùng uncertainty, FP/FN trade-off và chi phí tính toán thay vì chỉ dựa vào một metric tổng hợp.

### 5.2. Ý nghĩa thực tiễn của trade-off giữa false positive và false negative

Trong NIDS, false positive và false negative không có cùng ý nghĩa vận hành. False positive làm tăng số cảnh báo mà hệ thống hoặc nhân sự an ninh phải xử lý, trong khi false negative tương ứng với traffic tấn công bị bỏ lọt. Vì vậy, việc Stacking-42 giảm FPR nhưng tăng FNR là một trade-off thực tiễn chứ không chỉ là khác biệt thống kê.

Cụ thể, so với RF-42, Stacking-42 giảm FPR khoảng 0.38 điểm phần trăm nhưng tăng FNR khoảng 0.26 điểm phần trăm; cả hai chênh lệch đều có khoảng tin cậy paired bootstrap không chứa 0. Do đó, giá trị của Stacking phụ thuộc vào ưu tiên triển khai. Một môi trường có chi phí xử lý alert giả rất cao có thể quan tâm đến việc giảm FPR, trong khi một môi trường đặt chi phí bỏ lọt attack cao hơn có thể ưu tiên FNR thấp. Nghiên cứu này không gán một hàm chi phí cụ thể cho hai dạng lỗi, nên không đưa ra kết luận rằng một trade-off là “tốt hơn” trade-off còn lại.

Điểm này cũng cho thấy hạn chế của việc chỉ báo cáo Accuracy hoặc ngay cả Macro-F1. Hai pipeline có thể có Macro-F1 gần như bằng nhau nhưng hành vi vận hành khác nhau đáng kể. Vì vậy, FPR và FNR nên được xem là các outcome chính trong đánh giá NIDS, đặc biệt khi ensemble được thiết kế để thay đổi cách kết hợp quyết định của nhiều classifier.

### 5.3. Feature Selection mang lại lợi ích hiệu quả tính toán hơn là tăng hiệu năng

Một kết quả rõ ràng khác là Feature Selection không cải thiện hiệu năng dự đoán cuối trong thiết lập này, nhưng tạo ra lợi ích tính toán đáng kể. RF-17 có Macro-F1 thấp hơn RF-42 một lượng nhỏ, trong khi thời gian train giảm từ khoảng 371 giây xuống 57 giây, inference nhanh hơn khoảng 2.4 lần và kích thước model giảm gần một nửa.

Kết quả này nhất quán về mặt định hướng với literature cho rằng Feature Selection trong IDS cần được đánh giá không chỉ bằng predictive performance mà còn bằng dimensionality và cost. Zouhri, Idri và Ratnani (2024) cho thấy nhiều phương pháp filter-based feature selection có thể thay đổi hiệu năng của classifier trên các benchmark NIDS và nhấn mạnh vai trò của việc loại bỏ feature dư thừa. Nghiên cứu hiện tại bổ sung một góc nhìn cụ thể cho UNSW-NB15: 17 feature ổn định không mang lại metric dự đoán cao hơn RF-42, nhưng tạo ra performance–cost trade-off rất rõ.

Do đó, “Feature Selection tốt” trong nghiên cứu này không nên được hiểu là “accuracy tăng”. Giá trị chính của nó nằm ở khả năng giảm resource requirement với mức mất mát predictive performance tương đối nhỏ. Điều này đặc biệt có ý nghĩa trong các kịch bản cần retrain thường xuyên, triển khai nhiều sensor hoặc bị giới hạn CPU/bộ nhớ. Tuy nhiên, nghiên cứu chưa đo trực tiếp mức sử dụng RAM, năng lượng hoặc throughput mạng thực tế, nên kết luận về deployment efficiency chỉ giới hạn ở train time, inference time và serialized model size.

### 5.4. Khoảng cách giữa development CV và official holdout nhấn mạnh vấn đề generalization

Một trong những quan sát đáng chú ý nhất là performance trên official holdout thấp hơn đáng kể so với development CV. Trong development, RF-42 và Stacking-42 đạt Macro-F1 xấp xỉ 0.95, trong khi trên official test giá trị giảm xuống khoảng 0.86. Điều này cho thấy kết quả cross-validation trên official TRAIN đã lạc quan hơn đáng kể so với performance trên holdout được khóa.

Nghiên cứu hiện tại chưa đủ bằng chứng để quy sự suy giảm này cho một nguyên nhân duy nhất. Một số khác biệt đã được quan sát giữa train và test, bao gồm class-prior shift, sự xuất hiện của các category `state` chưa thấy trong train, và sự tồn tại của các feature vector mới trong test. Các yếu tố này có thể góp phần làm thay đổi độ khó của test set, nhưng thí nghiệm hiện tại không tách riêng tác động nhân quả của từng yếu tố.

Kết quả novel-vector sensitivity củng cố nhận định rằng khả năng tổng quát không nên được suy ra chỉ từ random/development CV. Cả ba pipeline đều giảm Macro-F1 khi chỉ đánh giá trên các test vector chưa từng xuất hiện trong train. Tuy vậy, novel-vector subset vẫn thuộc cùng benchmark UNSW-NB15; nó không tương đương với external validation hoặc cross-dataset testing.

Điểm này có cùng hướng với nghiên cứu cross-dataset của Cantone, Marrocco và Bria (2024), nơi các tác giả nhấn mạnh rằng hiệu năng cao trong một dataset không đảm bảo khả năng tổng quát sang network/dataset khác. Tuy nhiên, hai thiết kế không tương đương: nghiên cứu hiện tại chỉ đánh giá official holdout và novel-vector subset trong UNSW-NB15, còn Cantone và cộng sự thực hiện cross-dataset generalization. Vì vậy, kết quả của họ được dùng để đặt kết quả hiện tại vào bối cảnh generalization rộng hơn, không phải để chứng minh rằng nghiên cứu này đã thực hiện external validation.

### 5.5. Error analysis theo attack family cho thấy metric tổng hợp che giấu khác biệt cục bộ

Phân tích theo attack family cho thấy một pipeline có thể hoạt động tốt với một nhóm attack nhưng kém hơn với nhóm khác. Fuzzers là ví dụ rõ nhất: miss rate của Stacking-42 cao hơn RF-42 và RF-17, trong khi với Generic thì cả ba pipeline đều có miss rate rất thấp và thứ tự giữa chúng khác với Fuzzers.

Điều này giải thích vì sao complementary errors có thể tồn tại dù metric tổng hợp gần như ngang nhau. Một base learner có thể đóng góp mạnh cho một vùng nhỏ của feature space hoặc một attack family nhưng không đủ để thay đổi Macro-F1 toàn cục. Kết quả này cũng phù hợp với literature stacking NIDS trong đó performance trên minority hoặc attack-specific classes vẫn là vấn đề ngay cả khi aggregate performance cao, như được thảo luận trong Thockchom và cộng sự (2023).

Tuy nhiên, cần thận trọng với các attack family rất nhỏ. Ví dụ Worms chỉ có 44 mẫu trong official test. Với sample size như vậy, một vài lỗi thêm hoặc bớt có thể thay đổi tỷ lệ phần trăm rất mạnh. Vì vậy, nghiên cứu sử dụng Wilson confidence interval và không dùng các rare family này để đưa ra kết luận mạnh về thứ hạng giữa model.

### 5.6. Kết quả cũng nhấn mạnh vai trò của dataset audit và protocol đánh giá

Mặc dù dataset chính của nghiên cứu là UNSW-NB15, việc audit dữ liệu ngay từ đầu cho thấy benchmark không nên được xem như một nguồn dữ liệu “hoàn hảo” chỉ vì nó được sử dụng phổ biến. Nghiên cứu phát hiện nhiều feature vector lặp lại trong train/test, một số nhóm duplicate feature vector có conflicting label, và overlap giữa train và test. Vì chưa xác định được nguyên nhân tạo ra các collision này, nghiên cứu không thực hiện blind deduplication hoặc tự động relabel.

Cách tiếp cận thận trọng này phù hợp với bài học phương pháp luận từ Engelen, Rimmer và Joosen (2021) cũng như Liu và cộng sự (2022), những nghiên cứu cho thấy lỗi trong quá trình tạo dataset, feature extraction và labeling có thể ảnh hưởng mạnh đến benchmark NIDS. Hai công trình đó tập trung vào CIC-IDS2017/CSE-CIC-IDS2018 chứ không phải UNSW-NB15, nên chúng không phải bằng chứng rằng UNSW-NB15 có cùng lỗi. Chúng được dùng để hỗ trợ nguyên tắc phương pháp: dataset audit và provenance cần được kiểm tra trước khi diễn giải điểm số mô hình.

Điều này cũng giải thích tại sao nghiên cứu giữ official test khóa cho tới sau khi hoàn thành Feature Selection, model comparison, diversity analysis và tuning. Việc tách development evidence khỏi final holdout giúp giảm nguy cơ chọn model dựa trên test và làm cho khoảng cách giữa CV và final test trở thành một kết quả có ý nghĩa thay vì bị che khuất bởi post-test tuning.

### 5.7. Trả lời các câu hỏi nghiên cứu trong bối cảnh literature

**RQ1 — Ensemble effectiveness.** Kết quả không hỗ trợ một kết luận rằng ensemble luôn cải thiện NIDS. Hard/Soft Voting không vượt RF, còn Stacking chỉ tạo ra chênh lệch rất nhỏ về Macro-F1/MCC so với RF-42 trên holdout. Giá trị chính của Stacking nằm ở việc thay đổi FP/FN trade-off. Điều này phù hợp với literature review về ensemble NIDS: hiệu quả phụ thuộc mạnh vào base learners và combiner, không chỉ vào việc sử dụng ensemble.

**RQ2 — Feature Selection trade-off.** Feature Selection tạo ra lợi ích lớn về computational efficiency nhưng làm giảm nhẹ performance. Vì vậy, tác động của FS nên được báo cáo dưới dạng performance–cost trade-off thay vì chỉ hỏi feature subset nào có Accuracy cao nhất.

**RQ3 — Error complementarity.** Complementary errors được quan sát rõ ở OOF predictions, nhưng diversity không đủ để đảm bảo net improvement. Kết quả này nhấn mạnh sự khác biệt giữa “có diversity” và “ensemble tận dụng diversity hiệu quả”.

**RQ4 — Evaluation robustness.** Official holdout thấp hơn development CV và novel-vector subset tiếp tục làm performance giảm. Điều đó cho thấy kết luận phụ thuộc vào evaluation view. Tuy nhiên, vì UNSW-NB15 split hiện dùng không cung cấp một biến temporal/day/scenario sạch cho experiment so sánh trực tiếp, RQ4 mới được trả lời một phần.

## 5.8. Điều có thể và không thể kết luận từ Discussion này

Các kết quả hiện tại hỗ trợ các kết luận sau:

- Ensemble không tự động vượt một strong baseline.
- Stacking tạo FP/FN trade-off rõ hơn là một overall-performance gain.
- Feature Selection tạo lợi ích computation rõ ràng với một predictive cost nhỏ.
- Complementary errors tồn tại nhưng không đảm bảo ensemble gain.
- Generalization estimate nhạy với evaluation protocol/view.

Các kết quả hiện tại **không** đủ để kết luận:

- Stacking là mô hình tối ưu cho NIDS nói chung.
- Random Forest là mô hình tối ưu cho mọi network.
- Sự giảm performance trên test là do temporal drift.
- UNSW-NB15 có cùng dataset-construction errors với CIC-IDS2017.
- Kết quả binary classification hiện tại đại diện đầy đủ cho multiclass attack-family detection.
- Novel-vector sensitivity tương đương cross-dataset generalization.

---

## Tài liệu dùng trực tiếp trong Discussion

1. Tama, B. A., & Lim, S. (2021). *Ensemble learning for intrusion detection systems: A systematic mapping study and cross-benchmark evaluation*. Computer Science Review, 39, 100357. DOI: 10.1016/j.cosrev.2020.100357.
2. Thockchom, N., Singh, M. M., & Nandi, U. (2023). *A novel ensemble learning-based model for network intrusion detection*. Complex & Intelligent Systems, 9, 5693–5714. DOI: 10.1007/s40747-023-01013-7.
3. Zouhri, H., Idri, A., & Ratnani, A. (2024). *Evaluating the impact of filter-based feature selection in intrusion detection systems*. International Journal of Information Security, 23, 759–785. DOI: 10.1007/s10207-023-00767-y.
4. Cantone, M., Marrocco, C., & Bria, A. (2024). *Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study*. IEEE Access, 12, 144489–144508. DOI: 10.1109/ACCESS.2024.3472907.
5. Engelen, G., Rimmer, V., & Joosen, W. (2021). *Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study*. 2021 IEEE Security and Privacy Workshops (SPW), 7–12. DOI: 10.1109/SPW53761.2021.00009.
6. Liu, L., Engelen, G., Lynar, T., Essam, D., & Joosen, W. (2022). *Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018*. 2022 IEEE Conference on Communications and Network Security (CNS), 254–263. DOI: 10.1109/CNS56114.2022.9947235.

## Ghi chú biên tập

- Phần 5 nên đứng ngay sau Results.
- Không lặp lại toàn bộ số liệu ở Discussion; chỉ nhắc số cần thiết để hỗ trợ diễn giải.
- Các causal explanation phải dùng ngôn ngữ như “có thể”, “phù hợp với quan sát”, “một cách giải thích khả dĩ” nếu chưa có experiment trực tiếp kiểm tra.
- Limitations và Contributions nên tách thành Phase 12.3 để tránh trộn Discussion với self-critique và novelty claims.
