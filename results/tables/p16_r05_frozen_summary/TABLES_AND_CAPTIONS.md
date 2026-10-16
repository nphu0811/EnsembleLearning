# P16 — source tables r05, chưa render vào báo cáo

Official holdout binary, Attack=1, n=82.332, threshold0.5. Số thập phân trong phần hiển thị được làm tròn; CSV giữ nguyên token nguồn. Không fit/predict/bootstrap mới.

| Model | Macro-F1 | MCC | FPR | FNR | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| RF-42 | 0.863343 | 0.750910 | 0.270351 | 0.016192 | 10003 | 734 |
| Stacking-42 | 0.863840 | 0.750497 | 0.266514 | 0.018795 | 9861 | 852 |
| RF-17 | 0.860673 | 0.746881 | 0.276324 | 0.015618 | 10224 | 708 |

Bảng A. So sánh đóng băng trên official TEST; Stacking giảm142FP nhưng tăng118FN so với RF42. Các tỷ lệ ở đơn vị0–1. Không có cost matrix để quy hai loại lỗi về một lợi ích tổng thể. Không dùng bảng để đổi threshold hoặc candidate.

| Model | Features | Train s | Inference s / 82.332 rows | ms/row | Size MiB (legacy field mb) |
|---|---:|---:|---:|---:|---:|
| RF-42 | 42 | 371.244 | 0.714540 | 0.008679 | 205.490 |
| Stacking-42 | 42 | 980.170 | 1.024609 | 0.012445 | 206.216 |
| RF-17 | 17 | 57.255 | 0.293305 | 0.003562 | 105.044 |

Bảng B. Chi phí ghi trong run lịch sử, không phải benchmark mới trên máy hiện tại. Original environment UNKNOWN; không có uncertainty/repeated-training cho thời gian. Kích thước được source tính byte/(1024²), nên hiển thị MiB dù tên cột lịch sử là mb. Kích thước lịch sử không chứng minh artifact final còn trên máy. RF17 và RF42 khác hyperparameters; đây là joint pipeline trade-off, không causal feature-only ablation.

| Metric | Δ Stack42−RF42 | 95% CI lower | 95% CI upper |
|---|---:|---:|---:|
| macro_f1 | 0.000496690 | -0.000311804 | 0.001308950 |
| mcc | -0.000413036 | -0.001937876 | 0.001139570 |
| false_positive_rate | -0.003837838 | -0.005243243 | -0.002432432 |
| false_negative_rate | 0.002603018 | 0.001852996 | 0.003375099 |

Bảng C. Paired bootstrap10.000 replicates đã lưu, không bootstrap lại; delta là điểm metric ở đơn vị0–1, không phải phần trăm. CI có điều kiện trên benchmark rows, không thay repeated training hoặc external validation. CI Macro-F1/MCC chứa0: chưa chứng minh superiority, không suy equivalence. McNemar là kiểm paired correctness riêng, không trực tiếp test Macro-F1. FS fullTRAIN trước development CV, meta selection chưa fully nested, overlap/split dependence vẫn là giới hạn.
