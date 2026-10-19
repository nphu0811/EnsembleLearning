# Vấn đáp trong 4 phút

Không đọc cả 12 câu liên tiếp. Nghe hết câu hỏi; trả lời trực tiếp trong 15–25 giây; chỉ bổ sung bằng chứng khi được hỏi. Dành tối đa khoảng 45 giây cho một câu khó để còn thời gian cho câu tiếp.

Cuối slide20 có A1–A12 liên kết đến slide21–32 đang ẩn. Trong slide show có thể gõ số slide + Enter. Mỗi phụ lục có “Về kết luận”. Slide show chính giới hạn 1–20, video không chứa phụ lục.

## A1 · slide 21: Nhóm có phát minh thuật toán mới không?

Không. Đóng góp trong phạm vi đề tài là benchmark có truy vết, kiểm toán hạn chế, P21 matched và phân tích chi phí lỗi. Không tuyên bố mới trên toàn lĩnh vực.

Nguồn: V6 §3.1, §5.3–5.5; P21 aggregate

## A2 · slide 22: Vì sao chọn LR, DT và RF; AdaBoost ở đâu?

LR làm mốc tuyến tính; DT học quy tắc phi tuyến; RF giảm phương sai bằng nhiều cây. AdaBoost là đối chiếu boosting ở development. Hard/Soft Voting không hơn RF về Macro-F1 development; không mang Voting thành kết quả TEST cuối.

Nguồn: src/models/run_unsw_ensemble_phase7_2.py; V6 §3.3, §4.5

## A3 · slide 23: Vì sao dùng UNSW-NB15?

Có nhãn nhị phân và official split phù hợp đối chiếu tái lập. Giữ nguyên 175.341 TRAIN / 82.332 TEST. Kết quả chỉ thuộc benchmark; cần validation theo thời gian hoặc nguồn mạng khác trước khi khái quát.

Nguồn: V6 §2.1, §2.5–2.6, §3.1

## A4 · slide 24: Quy trình có hoàn toàn tránh leakage không?

Không tuyên bố tuyệt đối. Preprocessing trong pipeline; meta LR học dự đoán OOF; TEST không dùng tuning. Tuy nhiên stable17 lịch sử chọn trên toàn TRAIN trước CV và meta tuning chưa hoàn toàn nested, có selection optimism. P21 chọn trong FIT và inner grouped CV; không sửa hồi tố lịch sử.

Nguồn: V6 §3.2–3.6; tools/p21_science_core.py

## A5 · slide 25: P21 có phải external TEST mới không?

Không. Hậu nghiệm trên official TRAIN; mỗi seed dùng 60.000 FIT source rows, validation 35.069 dòng (11.200 Normal / 23.869 Attack). Group theo vector 42 predictor trùng chính xác; không chứng minh độc lập session/time. SD có điều kiện trên validation này.

Nguồn: P21 aggregate.json; V6 §3.6, §4.7

## A6 · slide 26: Feature Selection hoạt động thế nào và có rẻ hơn?

P21 chọn stable17 từ FIT qua MI/L1/ExtraTrees, 5 selector seed; 14 biến chung trong 5 bộ. RF17 model fit 84,600 s; selector 225,250 s; cộng 309,850 s, so RF42 fit 241,119 s. Chưa phải chi phí end-to-end. RF17 lịch sử đổi cả số cây và min leaf, không phải FS-only ablation.

Nguồn: V6 §3.2–3.3, §4.7.3; tools/p21_selector_core.py

## A7 · slide 27: OOF được dùng ở đâu?

Hard: đa số nhãn; Soft: trung bình xác suất. Stacking: LR meta học xác suất OOF của LR/DT/RF; passthrough=False. Khi dự đoán, base learner fit lại trên phần train rồi đưa xác suất cho meta. OOF cần giữ cả preprocessing trong fold.

Nguồn: src/models/run_unsw_phase9_final_holdout.py:283–508; tools/p21_science_core.py

## A8 · slide 28: Vì sao không chỉ dùng Accuracy?

Macro-F1 cho hai lớp trọng số bằng nhau; MCC dùng cả TN/FP/FN/TP. Precision Attack = TP/(TP+FP); Recall = TP/(TP+FN). FPR = FP/(TN+FP); FNR = FN/(TP+FN). Attack là lớp dương. Accuracy che được lỗi khi phân bố lớp đổi.

Nguồn: V6 §3.4; final_metrics.csv

## A9 · slide 29: Vì sao không nói hai mô hình tương đương?

CI 95% paired bootstrap của chênh Macro-F1/MCC chứa 0: chưa thấy khác biệt rõ theo phép đo đó. Không phải kiểm định tương đương. McNemar đo đúng/sai tổng thể, không trực tiếp Macro-F1. Bootstrap hàng dữ liệu không ước lượng biến thiên huấn luyện.

Nguồn: V6 §3.4, §4.2, §5.1

## A10 · slide 30: Khi nào RF42 tốt hơn Stacking42?

Trên official TEST cố định, L = FP + r FN, ΔL(Stack−RF)=−142+118r. Khi r>142/118≈1,2034, RF42 có L thấp hơn Stacking42 trong đúng cặp này. Chưa suy ra RF42 tối ưu hơn mọi mô hình hoặc chi phí SOC thực.

Nguồn: V6 §5.1; final_metrics.csv

## A11 · slide 31: Tại sao balanced làm tăng FNR?

Normal là lớp ít mẫu trong TRAIN. P21 class_weight=balanced ưu tiên Normal hơn nên giảm FPR, tăng FNR quan sát được. A2−A0: −3,1643 đpp FPR / +1,7881 đpp FNR; oversample: −2,2089 / +1,1680 đpp. Không chọn lại ngưỡng từ kết quả này.

Nguồn: V6 §4.7.4; P21 aggregate.json

## A12 · slide 32: Nhóm đã triển khai IDS mạng thật chưa?

Chưa. Mã hiện là pipeline offline. P15 tái dựng theo cấu hình, không chứng minh bitwise artifact lịch sử. Chưa đo traffic mới, drift, tải phục vụ hay tổn thất SOC. Cần đánh giá ngoài, calibration/threshold trên train-validation mới và đo latency toàn pipeline.

Nguồn: V6 §3.5, §5.4–5.5
