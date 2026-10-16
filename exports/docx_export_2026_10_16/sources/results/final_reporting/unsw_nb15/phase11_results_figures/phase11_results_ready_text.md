# PHASE 11 — Results-ready synthesis

## 1. Final official-test performance

Trên official test gồm 82,332 mẫu, Stacking-42 đạt Macro-F1 = 0.8638 (95% CI [0.8615, 0.8661]), trong khi RF-42 đạt 0.8633 (95% CI [0.8610, 0.8657]). Chênh lệch Stacking-42 − RF-42 là +0.000497; CI của chênh lệch chứa 0 nên chưa có bằng chứng rõ rằng Stacking cải thiện Macro-F1 tổng thể.

Trade-off lỗi lại rõ hơn: Stacking-42 giảm FPR từ 27.04% xuống 26.65%, nhưng FNR tăng từ 1.62% lên 1.88%. McNemar sau Holm cho cặp Stacking-42/RF-42 có p = 0.468, nên không có bằng chứng khác biệt về overall paired correctness.

## 2. Feature-selection / efficiency trade-off

RF-17 đạt Macro-F1 = 0.8607, thấp hơn RF-42 (0.8633) một lượng nhỏ, nhưng thời gian train giảm từ 371.2s xuống 57.3s, tương đương RF-17 train nhanh hơn khoảng 6.48×. Kích thước model giảm từ 205.5 MB xuống 105.0 MB.

## 3. Ensemble-complexity trade-off

Stacking-42 cần 980.2s để train, khoảng 2.64× RF-42, trong khi chênh lệch Macro-F1 tổng thể chỉ khoảng +0.0005. Do đó lợi ích chính của Stacking trong thí nghiệm này nằm ở việc thay đổi cân bằng FP/FN hơn là cải thiện tổng thể.

## 4. Novel-vector sensitivity

Macro-F1 giảm trên novel-vector subset ở cả ba pipeline: Stacking-42 -0.0057, RF-42 -0.0059, RF-17 -0.0049. Đây là bằng chứng về độ nhạy với evaluation view, không phải bằng chứng nhân quả cho temporal/domain shift.

## 5. Figure set

- Figure 1: Official-test Macro-F1 với 95% bootstrap CI.
- Figure 2: Official-test MCC với 95% bootstrap CI.
- Figure 3: Trade-off giữa FPR và FNR.
- Figure 4: Macro-F1 so với training cost.
- Figure 5: Official test so với novel-vector test.
- Figure 6: Miss rate theo attack family với Wilson 95% CI.