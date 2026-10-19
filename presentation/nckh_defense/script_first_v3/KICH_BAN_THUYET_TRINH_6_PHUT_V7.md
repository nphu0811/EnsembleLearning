# KỊCH BẢN THUYẾT TRÌNH NCKH — V7 / PHIÊN BẢN ƯU TIÊN NỘI DUNG
**Thời lượng:** 06:00 bao gồm chuyển slide và ngắt nhịp. **Hình thức:** 1 người thuyết trình trước hội đồng; 8 cảnh chính. **Nguồn duy nhất:** PDF V7 49 trang và bản trích xuất V7_full_text.txt đã lưu cùng release; tài liệu người dùng yêu cầu đọc lại. **Trạng thái:** bản kịch bản để duyệt trước khi làm lại PPTX, không phải bản đã đo bằng giọng nói thật.

**Luận điểm xuyên suốt:** Ensemble Learning không mặc nhiên tốt hơn mô hình đơn; khi triển khai IDS phải xem tổng chất lượng, FP, FN và chi phí/lệch đánh giá.

## Cảnh 1 — Một cảnh báo ít hơn có chắc tốt hơn? | 00:00–00:25 (25 giây)
> Thưa quý thầy cô, ít cảnh báo hơn có đồng nghĩa hệ thống phát hiện xâm nhập an toàn hơn không? Chưa chắc. Hệ thống có thể giảm báo động giả nhưng đồng thời bỏ sót thêm tấn công. Đó là câu hỏi dẫn dắt nghiên cứu của nhóm em.

**Nội dung chính trên slide:** “Ít cảnh báo hơn ≠ Ít tấn công bị bỏ sót”. Không công bố ngay số liệu để dành cho cảnh 5.  
**Nguồn PDF:** Chương 1, mục 1.1.2 (trang in 1); Chương 4, Bảng 4.1 và Hình 4.1 (trang in 20–21).

## Cảnh 2 — Bài toán và dữ liệu | 00:25–01:05 (40 giây)
> Đề tài của nhóm em nghiên cứu Ensemble Learning cho phát hiện xâm nhập mạng. Với UNSW-NB15, mỗi dòng lưu lượng được phân thành Normal hoặc Attack. Nhóm sử dụng hai phần dữ liệu chính thức: 175.341 dòng TRAIN và 82.332 dòng TEST, với 42 đặc trưng dự báo. Thay vì chỉ nhìn Accuracy, nhóm muốn biết các phương pháp kết hợp dự đoán có thực sự cải thiện chất lượng, và ảnh hưởng ra sao đến từng loại lỗi.

**Nội dung chính trên slide:** 175.341 TRAIN / 82.332 TEST / 42 predictors / Normal – Attack.  
**Nguồn PDF:** Chương 2, mục 2.1, Bảng 2.1 và Hình 2.1 (trang in 10); Chương 3, mục 3.1 (trang in 15).

## Cảnh 3 — Nhóm đã triển khai và so sánh mô hình như thế nào? | 01:05–01:55 (50 giây)
> Trước hết, nhóm giữ Random Forest với 42 đặc trưng làm mô hình đối chứng. Sau đó nhóm khảo sát các cách kết hợp Logistic Regression, Decision Tree và Random Forest. Với Stacking, các mô hình cơ sở tạo dự đoán ngoài fold; một Logistic Regression ở tầng sau học từ những dự đoán đó để đưa ra kết quả cuối. Nhóm cũng đánh giá Random Forest với 17 đặc trưng đã lựa chọn. Những cấu hình cuối được khóa trước khi đánh giá trên TEST chính thức, với cùng ngưỡng quyết định 0,5. Cách làm này giúp so sánh những pipeline cụ thể, chứ không chứng minh rằng mọi phương pháp Ensemble đều tốt hơn.

**Nội dung chính trên slide:** Sơ đồ luồng và hai nhánh RF-42 vs Stacking-42; chú thích RF-17 là pipeline đối chứng thứ ba. Phân biệt fit OOF với suy luận.  
**Nguồn PDF:** Chương 3, mục 3.2–3.4 và Bảng 3.1 (trang in 15–17).

## Cảnh 4 — Đúng nhiều chưa đủ | 01:55–02:25 (30 giây)
> Trong hệ thống IDS, báo động giả, hay False Positive, là lưu lượng bình thường bị báo thành tấn công. Ngược lại, False Negative là lưu lượng tấn công bị nhận nhầm thành bình thường. Một lỗi làm tăng công kiểm tra; lỗi kia có thể khiến sự cố bị bỏ qua. Vì vậy, nhóm xem đồng thời Macro-F1, MCC, FPR và FNR.

**Nội dung chính trên slide:** Hai ví dụ FP/FN song song, dưới là Macro-F1, MCC, FPR và FNR với giải nghĩa ngắn.  
**Nguồn PDF:** Chương 1, mục 1.2.1 và 1.2.6 (trang in 3, 6); Chương 4, mục 4.1 và công thức (4.1) (trang in 20).

## Cảnh 5 — Official TEST: Stacking tốt hơn hay chỉ đổi loại lỗi? | 02:25–03:20 (55 giây)
> Đây là kết quả trên cùng 82.332 mẫu TEST chính thức. Random Forest 42 đặc trưng đạt Macro-F1 là 0,863343; Stacking đạt 0,863840. Mức chênh rất nhỏ, và khoảng tin cậy của hiệu số chứa số không. Vì vậy, nhóm chưa có đủ bằng chứng để nói Stacking vượt trội về chỉ số tổng hợp. Nhưng khi nhìn vào từng lỗi, một khác biệt rõ hơn xuất hiện: Stacking giảm số cảnh báo giả từ 10.003 xuống 9.861, tức ít hơn 142 trường hợp; đổi lại, số tấn công bị bỏ sót tăng từ 734 lên 852, tức thêm 118 trường hợp. Đây là phát hiện quan trọng nhất của phần đánh giá TEST.

**Nội dung chính trên slide:** Macro-F1 RF-42 0,863343 vs Stacking-42 0,863840; hai thanh so sánh FP: −142 / FN: +118, gắn nhãn “official TEST, 82.332 dòng”.  
**Nguồn PDF:** Chương 4, Bảng 4.1, Bảng 4.2, Hình 4.1 và Hình 4.2 (trang in 20–22).

## Cảnh 6 — Vì sao còn phải làm thí nghiệm P21? | 03:20–04:05 (45 giây)
> Thực nghiệm lịch sử còn hai hạn chế. Bộ 17 đặc trưng được chọn trước development cross-validation, và hai Random Forest không chỉ khác số đặc trưng mà còn khác siêu tham số. Nhóm vì vậy bổ sung P21 để đối chứng có kiểm soát. Từ TRAIN, nhóm tạo năm tập FIT, mỗi tập 60.000 dòng theo seed khác nhau. Cả năm seed và năm cấu hình cùng đánh giá trên một validation 35.069 dòng. Đây là thí nghiệm nội bộ hậu nghiệm, không phải năm tập TEST độc lập.

**Nội dung chính trên slide:** TRAIN → FIT pool / một validation cố định → năm FIT seed × năm nhánh A0–A4. Ghi nổi bật “P21: TRAIN-derived validation, không phải external TEST”.  
**Nguồn PDF:** Chương 3, mục 3.2, 3.6.1–3.6.3 và Bảng 3.2 (trang in 15–19); Chương 4, mục 4.9 (trang in 28).

## Cảnh 7 — P21 cho chúng ta biết điều gì? | 04:05–05:13 (68 giây)
> Kết quả P21 tiếp tục cho thấy Stacking không mặc nhiên thắng Random Forest. Macro-F1 trung bình của RF42-Lite là 0,945220, trong khi Stacking-Lite là 0,944731. Khi giữ cùng siêu tham số Random Forest, bản 17 đặc trưng đạt 0,936751, thấp hơn bản 42 đặc trưng. Đúng là riêng bước fit mô hình 17 đặc trưng nhanh hơn: 84,6 giây so với 241,1 giây. Nhưng nếu tính thêm khoảng 225,3 giây để chọn lại đặc trưng, tổng chi phí đo được là khoảng 309,9 giây. Hai cách cân bằng lớp cũng giảm báo động giả nhưng làm tăng tỷ lệ bỏ sót tấn công. Như vậy, muốn chọn một pipeline, chúng ta phải xem cả chất lượng, chi phí và hướng thay đổi của sai số.

**Nội dung chính trên slide:** RF42-Lite 0,945220 vs Stacking-Lite 0,944731; RF17-Lite 0,936751; cost selector+RF17 = 309,850s vs RF42 fit 241,119s; “weighting: FPR −3,164 đpp / FNR +1,788 đpp”. Các kết quả đều thuộc P21 internal validation.  
**Nguồn PDF:** Chương 4, Bảng 4.8, 4.9, 4.11 và mục 4.9.2–4.9.4 (trang in 28–30).

## Cảnh 8 — Đóng góp và giới hạn | 05:13–06:00 (47 giây)
> Điều nhóm rút ra là: kết hợp nhiều mô hình chưa chắc giúp phát hiện xâm nhập tốt hơn. Điều quan trọng là biết mô hình giảm loại lỗi nào, tăng loại lỗi nào, và chi phí phải trả. Đóng góp của đề tài là đối chiếu có kiểm soát, phân tích sai số và công khai giới hạn bằng chứng. Nghiên cứu vẫn chỉ trên UNSW-NB15; P21 dùng chung một validation, chưa thử trên mạng độc lập. Bước tiếp theo là đánh giá với dữ liệu mới, tách theo thời gian hoặc phiên mạng và đo chi phí vận hành thực tế. Em xin cảm ơn quý thầy cô.

**Nội dung chính trên slide:** Ba dòng “Đối chiếu có kiểm soát / Phân tích sai số / Minh bạch giới hạn” và một dòng “Bước tiếp theo: đánh giá dữ liệu mạng độc lập”.  
**Nguồn PDF:** Chương 5, mục 5.4–5.9 (trang in 33–36).

---

## Dặn dò khi tập nói

- Các khoảng thời gian là **khung mục tiêu**, chưa được đo bằng giọng nói của người trình bày. Nếu bản thu trên 6 phút, ưu tiên giảm phần 3, 6 và 7 nhưng không bỏ cảnh 5.
- Ngắt một nhịp sau câu hỏi mở đầu, và sau cặp số “−142 FP / +118 FN”.
- Không đọc từng ô trong bảng, không đọc dài công thức McNemar hoặc Bootstrap.
- Đọc số thập phân theo cách người Việt dễ hiểu; có thể làm tròn **trong lời nói** nhưng giữ số gốc đầy đủ trên slide.
- Không gọi P21 là kiểm định TEST độc lập và không gọi Stacking là phương pháp tốt nhất.
- Slide 8 kết thúc bằng lời cảm ơn; không phát tiếp phụ lục nếu chưa có câu hỏi.

**Gate trước khi dựng slide:** duyệt lời nói thật, luyện thử với đồng hồ và chốt 8 thông điệp. Bước tiếp theo mới tạo storyboard/motion từ bảng Evidence Map, tránh quay lại tình trạng slide đẹp nhưng không phục vụ nội dung.
