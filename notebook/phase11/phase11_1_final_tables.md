# PHASE 11.1 — Chốt bảng kết quả cuối

## Mục tiêu

Chỉ chọn các bảng thật sự cần cho báo cáo. Không tạo figure và không thay đổi mô hình.

## Bảng 1 — Kết quả dự đoán cuối trên official test

**Vai trò:** bảng kết quả chính của toàn bộ thực nghiệm UNSW-NB15.  
**Đặt trong thân bài:** CÓ.

| Pipeline    | Accuracy | Balanced Accuracy | Macro-F1 | Macro-F1 95% CI  | MCC    | MCC 95% CI       | FPR    | FNR    | FP    | FN  |
| ----------- | -------- | ----------------- | -------- | ---------------- | ------ | ---------------- | ------ | ------ | ----- | --- |
| Stacking-42 | 0.8699   | 0.8573            | 0.8638   | [0.8615, 0.8661] | 0.7505 | [0.7465, 0.7545] | 0.2665 | 0.0188 | 9861  | 852 |
| RF-42       | 0.8696   | 0.8567            | 0.8633   | [0.8610, 0.8657] | 0.7509 | [0.7469, 0.7549] | 0.2704 | 0.0162 | 10003 | 734 |
| RF-17       | 0.8672   | 0.8540            | 0.8607   | [0.8583, 0.8630] | 0.7469 | [0.7429, 0.7508] | 0.2763 | 0.0156 | 10224 | 708 |

Ghi chú:
- 95% CI dùng bootstrap từ Phase 10.
- Không dùng bảng này để tuyên bố Stacking “tốt nhất”; Macro-F1/MCC của Stacking-42 và RF-42 rất sát nhau.
- FPR/FNR phải được đọc cùng nhau vì hai pipeline có trade-off rõ.

## Bảng 2 — So sánh thống kê theo cặp

**Vai trò:** trả lời xem chênh lệch giữa pipeline có thực sự rõ hay chỉ là vài chữ số thập phân.  
**Đặt trong thân bài:** CÓ, nhưng có thể rút gọn nếu giới hạn trang.

| Comparison          | Δ Macro-F1 | Δ Macro-F1 95% CI  | Δ MCC     | Δ MCC 95% CI       | Δ FPR     | Δ FPR 95% CI       | Δ FNR     | Δ FNR 95% CI       | McNemar Holm p |
| ------------------- | ---------- | ------------------ | --------- | ------------------ | --------- | ------------------ | --------- | ------------------ | -------------- |
| Stacking-42 − RF-42 | +0.000497  | [-0.0003, +0.0013] | -0.000413 | [-0.0019, +0.0011] | -0.003838 | [-0.0052, -0.0024] | +0.002603 | [+0.0019, +0.0034] | 0.4684         |
| Stacking-42 − RF-17 | +0.003167  | [+0.0014, +0.0050] | +0.003616 | [+0.0006, +0.0068] | -0.009811 | [-0.0133, -0.0064] | +0.003177 | [+0.0020, +0.0043] | 0.0049         |
| RF-42 − RF-17       | +0.002670  | [+0.0009, +0.0045] | +0.004029 | [+0.0009, +0.0073] | -0.005973 | [-0.0095, -0.0026] | +0.000574 | [-0.0006, +0.0018] | 0.0112         |

Cách đọc:
- Δ = model bên trái trừ model bên phải.
- CI chứa 0 → chưa có bằng chứng rõ về chênh lệch metric đó.
- McNemar kiểm tra overall paired correctness, không phải Macro-F1/MCC.

## Bảng 3 — Performance–cost trade-off

**Vai trò:** trả lời RQ2 và chứng minh Feature Selection đem lại lợi ích tính toán.  
**Đặt trong thân bài:** CÓ.

| Pipeline    | Features | Macro-F1 | Train time (s) | Inference (ms/sample) | Model size (MB) |
| ----------- | -------- | -------- | -------------- | --------------------- | --------------- |
| Stacking-42 | 42       | 0.8638   | 980.2          | 0.0124                | 206.2           |
| RF-42       | 42       | 0.8633   | 371.2          | 0.0087                | 205.5           |
| RF-17       | 17       | 0.8607   | 57.3           | 0.0036                | 105.0           |

Điểm cần nêu:
- RF-17 mất một ít predictive performance nhưng giảm rất mạnh thời gian train/inference và kích thước model.
- Stacking-42 tốn compute hơn RF-42 đáng kể nhưng không có bằng chứng về lợi ích tổng thể tương ứng.

## Bảng 4 — Novel-vector sensitivity

**Vai trò:** sensitivity analysis, hỗ trợ RQ4 một phần.  
**Đặt trong thân bài:** TÙY GIỚI HẠN TRANG; nếu thiếu chỗ có thể đưa phụ lục và giữ một figure trong thân bài.

| Pipeline    | Official Macro-F1 | Novel Macro-F1 | Δ Macro-F1 (novel-official) | Official MCC | Novel MCC | Δ MCC   | Official FNR | Novel FNR | Δ FNR   |
| ----------- | ----------------- | -------------- | --------------------------- | ------------ | --------- | ------- | ------------ | --------- | ------- |
| Stacking-42 | 0.8638            | 0.8581         | -0.0057                     | 0.7505       | 0.7407    | -0.0098 | 0.0188       | 0.0218    | +0.0030 |
| RF-42       | 0.8633            | 0.8575         | -0.0059                     | 0.7509       | 0.7410    | -0.0099 | 0.0162       | 0.0187    | +0.0025 |
| RF-17       | 0.8607            | 0.8557         | -0.0049                     | 0.7469       | 0.7384    | -0.0084 | 0.0156       | 0.0183    | +0.0027 |

Không được suy diễn bảng này thành bằng chứng causal về temporal drift/domain shift.

## Table S1 — Attack-family miss rates

**Vai trò:** error analysis chi tiết.  
**Đặt trong thân bài:** KHÔNG. Nên để phụ lục/supplement vì có nhiều dòng và rare classes.

File: `tableS1_attack_family_miss_rates.csv`

Sau này figure attack-family chỉ nên chọn các family đủ lớn để không làm rare class trông quan trọng quá mức.

## Chốt cấu trúc bảng cho báo cáo

**Thân bài nên giữ 3 bảng chính:**
1. Final official-test performance.
2. Pairwise statistical comparison.
3. Performance–cost trade-off.

**Sensitivity / phụ lục:**
4. Novel-vector sensitivity — giữ trong thân bài nếu còn chỗ.
5. Attack-family miss-rate table — phụ lục.

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| P11-01A | Chọn bảng performance chính | DONE | table11_1_primary_official_test.csv |
| P11-01B | Chọn bảng statistical comparison | DONE | table11_2_pairwise_statistics.csv |
| P11-01C | Chọn bảng performance–cost | DONE | table11_3_performance_cost.csv |
| P11-01D | Chọn sensitivity table | DONE | table11_4_novel_vector_sensitivity.csv |
| P11-01E | Tách attack-family thành supplementary | DONE | tableS1_attack_family_miss_rates.csv |
| P11-02 | Figure Macro-F1/MCC | TODO | — |
