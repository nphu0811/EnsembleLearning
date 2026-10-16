# PHASE 12.1 — DRAFT PHẦN KẾT QUẢ (RESULTS)

> Trạng thái: bản nháp học thuật đầu tiên.  
> Phạm vi: chỉ trình bày kết quả thực nghiệm trên UNSW-NB15.  
> Chưa bao gồm Discussion, giải thích nguyên nhân sâu, đối chiếu literature hay kết luận tổng quát.

## 4. Kết quả thực nghiệm

### 4.1. Hiệu năng cuối trên official test

Ba pipeline đã được cố định trước khi mở official test gồm Stacking-42, RF-42 và RF-17. Trên tập kiểm thử chính thức, Stacking-42 đạt Macro-F1 = 0.8638 và MCC = 0.7505, trong khi RF-42 đạt Macro-F1 = 0.8633 và MCC = 0.7509. RF-17 đạt Macro-F1 = 0.8607 và MCC = 0.7469. Khoảng tin cậy bootstrap 95% cho Macro-F1 lần lượt là [0.8615, 0.8661] đối với Stacking-42, [0.8610, 0.8657] đối với RF-42 và [0.8583, 0.8630] đối với RF-17.

Mặc dù Stacking-42 có Macro-F1 cao hơn RF-42 một lượng nhỏ, mức chênh lệch chỉ đạt +0.000497. Khoảng tin cậy 95% của chênh lệch này là [-0.000312, +0.001309], bao gồm giá trị 0. Tương tự, chênh lệch MCC giữa hai pipeline không cho thấy lợi thế rõ ràng cho Stacking-42. Kiểm định McNemar sau hiệu chỉnh Holm cho cặp Stacking-42 và RF-42 cho p = 0.4684, do đó chưa có bằng chứng cho thấy hai pipeline khác nhau về tỷ lệ lỗi tổng thể trên cùng tập mẫu kiểm thử.

### 4.2. Trade-off giữa false positive và false negative

Sự khác biệt rõ hơn xuất hiện khi phân tích loại lỗi. Stacking-42 có false-positive rate bằng 26.65%, thấp hơn RF-42 (27.04%). Ngược lại, false-negative rate của Stacking-42 là 1.88%, cao hơn RF-42 (1.62%). Chênh lệch FPR giữa Stacking-42 và RF-42 là -0.003838, với khoảng tin cậy 95% [-0.005243, -0.002432]. Trong khi đó, chênh lệch FNR là +0.002603, với khoảng tin cậy 95% [+0.001853, +0.003375].

Kết quả này cho thấy Stacking-42 chủ yếu thay đổi điểm cân bằng giữa hai dạng lỗi: giảm số cảnh báo giả nhưng đồng thời làm tăng số mẫu tấn công bị bỏ sót. Do đó, khi chỉ xét hiệu năng tổng thể, Stacking-42 và RF-42 gần tương đương; khác biệt nổi bật hơn nằm ở cấu trúc lỗi.

### 4.3. Ảnh hưởng của Feature Selection đến hiệu năng và chi phí

RF-17 sử dụng 17 feature ổn định đạt Macro-F1 = 0.8607, thấp hơn RF-42 (0.8633) một lượng nhỏ. Tuy nhiên, lợi ích tính toán là đáng kể. Thời gian huấn luyện RF-42 là 371.24 giây, trong khi RF-17 chỉ cần 57.26 giây, tương đương nhanh hơn khoảng 6.48 lần. Thời gian suy luận trung bình giảm từ 0.008679 ms/mẫu xuống 0.003562 ms/mẫu. Kích thước model tuần tự hóa cũng giảm từ 205.49 MB xuống 105.04 MB.

Như vậy, việc giảm số feature không cải thiện hiệu năng dự đoán cuối trên official test, nhưng mang lại lợi ích rõ rệt về chi phí huấn luyện, tốc độ suy luận và kích thước mô hình. RF-17 vì thế thể hiện một cấu hình thiên về hiệu quả tính toán hơn là tối đa hóa hiệu năng dự đoán.

### 4.4. Chi phí bổ sung của Stacking

Stacking-42 có thời gian huấn luyện 980.17 giây, cao hơn khoảng 2.64 lần so với RF-42. Thời gian suy luận trung bình của Stacking-42 là 0.012445 ms/mẫu, cũng cao hơn RF-42 (0.008679 ms/mẫu). Tuy nhiên, kích thước model của hai pipeline gần tương đương (206.22 MB so với 205.49 MB).

Kết quả này cho thấy Stacking làm tăng chi phí tính toán đáng kể trong khi mức cải thiện Macro-F1 tổng thể rất nhỏ và không có bằng chứng thống kê rõ ràng về lợi thế tổng thể so với RF-42.

### 4.5. Phân tích lỗi theo attack family

Phân tích false negative theo attack family cho thấy Fuzzers là một trong những nhóm khó phát hiện nhất trong các attack family có số lượng mẫu đủ lớn. Stacking-42 bỏ sót 754/6062 mẫu Fuzzers, tương ứng miss rate = 12.44% (Wilson 95% CI [11.63%, 13.29%]). RF-42 bỏ sót 621/6062 mẫu, tương ứng 10.24%, trong khi RF-17 bỏ sót 623/6062 mẫu, tương ứng 10.28%.

Ngược lại, với nhóm Generic, cả ba pipeline đều có miss rate rất thấp. Stacking-42 bỏ sót 14/18871 mẫu, RF-42 bỏ sót 57/18871 mẫu và RF-17 bỏ sót 3/18871 mẫu. Kết quả này cho thấy không có một pipeline duy nhất đạt ưu thế đồng đều trên mọi attack family.

Các attack family có số lượng mẫu rất nhỏ, chẳng hạn Worms, không được dùng để đưa ra kết luận mạnh chỉ dựa trên tỷ lệ phần trăm, vì độ bất định của ước lượng còn lớn.

### 4.6. Độ nhạy trên novel-vector test

Bên cạnh official test đầy đủ, nghiên cứu còn đánh giá một sensitivity view chỉ gồm các test sample có vector feature chưa từng xuất hiện trong training set. Cả ba pipeline đều giảm Macro-F1 trên novel-vector subset so với official test đầy đủ. Mức giảm lần lượt khoảng 0.0057 đối với Stacking-42, 0.0059 đối với RF-42 và 0.0050 đối với RF-17.

Kết quả này cho thấy hiệu năng của các pipeline có độ nhạy nhất định với các pattern feature chưa xuất hiện trong training set. Tuy nhiên, phân tích này chỉ là sensitivity analysis và không được dùng để khẳng định nguyên nhân của sự suy giảm là temporal drift, domain shift hay một cơ chế cụ thể khác.

## 4.7. Tóm tắt kết quả theo câu hỏi nghiên cứu

RQ1: Stacking-42 không cho thấy lợi thế tổng thể rõ ràng so với RF-42 về Macro-F1, MCC hoặc paired correctness trên official test; khác biệt chính nằm ở trade-off giữa FPR và FNR.

RQ2: Feature Selection làm giảm đáng kể chi phí tính toán nhưng đi kèm một mức giảm nhỏ về hiệu năng dự đoán ở RF-17 so với RF-42.

RQ3: Các model có lỗi bổ sung nhau, nhưng diversity không tự động chuyển thành cải thiện hiệu năng tổng thể; Stacking chủ yếu làm thay đổi phân bố loại lỗi thay vì tạo ra lợi thế rõ ràng về tổng thể.

RQ4: Hiệu năng giảm trên novel-vector subset cho thấy kết quả nhạy với evaluation view, nhưng bằng chứng hiện tại chưa đủ để quy kết nguyên nhân cho temporal hay domain shift.

---

## Ghi chú sử dụng trong báo cáo

- Phần này nên đặt trước Discussion.
- Không giải thích nguyên nhân sâu ở đây; nguyên nhân và đối chiếu literature để sang Discussion.
- Chèn Figure 1–6 và các bảng Phase 11 tại các đoạn tương ứng.
- Không dùng từ “best”, “superior”, “significantly better” cho Stacking-42 so với RF-42.
