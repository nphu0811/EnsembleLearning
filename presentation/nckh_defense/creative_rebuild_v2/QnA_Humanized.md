# Vấn đáp — 4 phút

Trả lời phần chính trong 15–25 giây. Chỉ mở một phụ lục sát câu hỏi, bổ sung số liệu khi hội đồng yêu cầu. Từ slide kết luận, nhấn A1–A12; mỗi phụ lục có nút về kết luận. Các phụ lục 18–29 ẩn và không nằm trong video.

## A1 · Slide 18: Nhóm có phát minh thuật toán mới không?

Nhóm không đề xuất thuật toán mới. Nhóm đối chiếu các cấu hình, bổ sung thí nghiệm P21 và chỉ ra mô hình đang giảm loại lỗi nào, tăng loại lỗi nào. Đó là đóng góp trong phạm vi đề tài; nhóm không khẳng định đây là cách làm mới của toàn lĩnh vực.

Nguồn: V6 §3.1, §5.3–5.5; P21 aggregate.

## A2 · Slide 19: Vì sao chọn LR, DT và RF; AdaBoost ở đâu?

LR là mốc tuyến tính; DT học quy tắc phi tuyến; RF kết hợp nhiều cây để giảm phương sai. Nhóm muốn xem các cách học khác nhau có bổ sung cho nhau không. AdaBoost được đối chiếu ở development. Voting chưa hơn RF về Macro-F1 ở giai đoạn đó nên không được đưa thành kết quả TEST cuối.

Nguồn: src/models/run_unsw_ensemble_phase7_2.py; V6 §3.3, §4.5.

## A3 · Slide 20: Vì sao dùng UNSW-NB15?

UNSW-NB15 có nhãn nhị phân và bộ chia chính thức, thuận tiện để đối chiếu lại kết quả. Nhóm giữ 175.341 dòng TRAIN và 82.332 dòng TEST. Tuy nhiên, một benchmark chưa đại diện cho mạng thực; cần kiểm chứng trên nguồn hoặc thời điểm khác.

Nguồn: V6 §2.1, §2.5–2.6, §3.1.

## A4 · Slide 21: Quy trình có hoàn toàn tránh leakage không?

Nhóm đặt preprocessing trong pipeline và dùng dự đoán OOF cho meta learner; TEST không phục vụ tuning. Nhưng stable17 lịch sử được chọn trước CV và meta tuning chưa hoàn toàn nested, nên vẫn có nguy cơ lạc quan. P21 chọn biến trong FIT và dùng inner grouped CV; nó không sửa hồi tố kết quả cũ.

Nguồn: V6 §3.2–3.6; tools/p21_science_core.py.

## A5 · Slide 22: P21 có phải external TEST mới không?

Không. P21 dùng lại official TRAIN. Mỗi seed có 60.000 dòng FIT và cùng validation 35.069 dòng. Các vector 42 predictor trùng nhau được gom nhóm; điều này chưa chứng minh độc lập theo phiên hoặc thời gian. Năm seed phản ánh biến thiên huấn luyện, không phải năm TEST ngoài.

Nguồn: P21 aggregate.json; V6 §3.6, §4.7.

## A6 · Slide 23: Feature Selection hoạt động thế nào và có rẻ hơn?

P21 chọn 17 biến trong FIT bằng MI, L1 và ExtraTrees qua 5 selector seed. RF17 fit mất 84,600 giây; chọn biến mất 225,250 giây. Cộng lại 309,850 giây, cao hơn RF42 fit 241,119 giây. Đây chưa phải chi phí end-to-end. RF17 lịch sử còn đổi cấu hình rừng, nên không dùng để tách riêng tác động chọn biến.

Nguồn: V6 §3.2–3.3, §4.7.3; tools/p21_selector_core.py.

## A7 · Slide 24: OOF được dùng ở đâu?

Voting dùng luật gộp cố định: đa số nhãn hoặc trung bình xác suất. Với Stacking, meta LR học từ xác suất ngoài fold của LR, DT và RF. Sau đó base learner được fit lại trên phần train. Khi dự đoán bản ghi mới, các mô hình đã fit tạo xác suất cho meta; không huấn luyện lại lúc suy luận.

Nguồn: src/models/run_unsw_phase9_final_holdout.py:283–508; tools/p21_science_core.py.

## A8 · Slide 25: Vì sao không chỉ dùng Accuracy?

Macro-F1 cho hai lớp trọng số bằng nhau, còn MCC xét cả bốn ô confusion matrix. Nhóm đọc thêm Precision, Recall, FPR và FNR để biết lỗi nằm ở đâu. Attack là lớp dương: FPR là tỷ lệ Normal bị báo Attack; FNR là tỷ lệ Attack bị bỏ qua. Accuracy một mình không cho thấy hết đánh đổi đó.

Nguồn: V6 §3.4; final_metrics.csv.

## A9 · Slide 26: Vì sao không nói hai mô hình tương đương?

Khoảng tin cậy của chênh lệch Macro-F1 và MCC chứa 0 nên nhóm chưa thấy khác biệt rõ theo các phép đo đó. Điều này không chứng minh hai mô hình tương đương. Bootstrap ở đây lấy mẫu theo dòng dự đoán; nó không đo biến thiên do huấn luyện lại mô hình.

Nguồn: V6 §3.4, §4.2, §5.1.

## A10 · Slide 27: Khi nào RF42 tốt hơn Stacking42?

Với đúng dự đoán official TEST đang xét, nhóm đặt L=FP+r×FN. Chênh lệch Stacking trừ RF là −142+118r. Khi r lớn hơn 142/118, khoảng 1,2034, RF có tổn thất thấp hơn. Kết luận này phụ thuộc giả định chi phí; chưa phải chi phí đo ở SOC hay chứng minh RF tốt hơn mọi mô hình.

Nguồn: V6 §5.1; final_metrics.csv.

## A11 · Slide 28: Tại sao balanced làm tăng FNR?

Normal mới là lớp ít mẫu trong TRAIN. Cấu hình balanced ưu tiên Normal hơn, và trong P21 nhóm quan sát FPR giảm nhưng FNR tăng. Cân bằng không tự động giúp phát hiện Attack tốt hơn. Nhóm giữ nguyên ngưỡng trong phép đối chứng, không chọn ngưỡng mới từ kết quả này.

Nguồn: V6 §4.7.4; P21 aggregate.json.

## A12 · Slide 29: Nhóm đã triển khai IDS mạng thật chưa?

Chưa. Nhóm đang đánh giá pipeline ngoại tuyến. P15 tái dựng theo cấu hình, không chứng minh trùng bit với artifact lịch sử. Nhóm chưa đo drift, tải phục vụ hoặc chi phí SOC. Trước khi triển khai, cần dữ liệu ngoài, kiểm tra ngưỡng trên train-validation mới và đo độ trễ toàn quy trình.

Nguồn: V6 §3.5, §5.4–5.5.
