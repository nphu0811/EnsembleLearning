# Canonical Phase 14 — Kiểm định Step 1 & diễn giải Step 2

**Dữ liệu nguồn:** `phase14_error_analysis_step1.zip` do người nghiên cứu chạy từ script read-only trên frozen Phase-9 prediction.  
**Trạng thái:** Step 1 **PASS**, Step 2 (descriptive attack-family interpretation) **DONE**, Step 3 (feature-level error characterization) **TODO**.  
**Giới hạn:** Không train, không tune, không chọn lại feature/threshold, không gán nguyên nhân chỉ từ error counts.

## 1. Kiểm tra tính nhất quán

- Tổng official TEST: **82,332 = 37,000 Normal + 45,332 Attack**.
- Pairwise correctness: **71,104 cùng đúng + 491 RF-only đúng + 515 Stacking-only đúng + 10,222 cùng sai = 82,332**.
- RF-42: **FP = 10,003; FN = 734**.
- Stacking-42: **FP = 9,861; FN = 852**.
- Deltas Stacking − RF: **FP = −142; FN = +118**.
- Tổng số dòng attack theo 9 family = **45,332**; tổng FN ở family khớp FN toàn test.
- Kiểm tra trong từng family: `RF FN = rescued + both missed` và `Stacking FN = newly missed + both missed`: **PASS**.

### Chuyển đổi lỗi theo lớp thật

| Lớp thật | Hai model cùng đúng | Chỉ RF đúng | Chỉ Stacking đúng | Cùng sai |
|---|---:|---:|---:|---:|
| Normal (n=37,000) | 26,719 | 278 | 420 | 9,583 |
| Attack (n=45,332) | 44,385 | 213 | 95 | 639 |

**Diễn giải:** Trong Normal, Stacking sửa 420 false alarms mà RF tạo ra, nhưng sinh thêm 278 false alarms. Trong Attack, Stacking cứu được 95 ca RF bỏ sót, nhưng đồng thời bỏ sót thêm 213 ca RF phát hiện được.

## 2. Error analysis theo từng attack family

Chú ý: đây là **miss rate của binary detector** phân nhóm theo metadata `attack_cat`, không phải metric của mô hình multiclass.

| Attack family | Số attack | RF FN (tỉ lệ) | Stacking FN (tỉ lệ) | RF sai, Stacking đúng | RF đúng, Stacking sai | Δ FN (Stack−RF) |
|---|---:|---:|---:|---:|---:|---:|
| Fuzzers | 6,062 | 621 (10.24%) | 754 (12.44%) | 47 | 180 | +133 |
| Analysis | 677 | 3 (0.44%) | 19 (2.81%) | 0 | 16 | +16 |
| DoS | 4,089 | 4 (0.10%) | 9 (0.22%) | 0 | 5 | +5 |
| Exploits | 11,132 | 45 (0.40%) | 49 (0.44%) | 5 | 9 | +4 |
| Reconnaissance | 3,496 | 1 (0.03%) | 2 (0.06%) | 0 | 1 | +1 |
| Backdoor | 583 | 0 (0.00%) | 1 (0.17%) | 0 | 1 | +1 |
| Shellcode | 378 | 2 (0.53%) | 3 (0.79%) | 0 | 1 | +1 |
| Worms | 44 | 1 (2.27%) | 1 (2.27%) | 0 | 0 | +0 |
| Generic | 18,871 | 57 (0.30%) | 14 (0.07%) | 43 | 0 | -43 |

### Phát hiện quan trọng

**Fuzzers (6,062 mẫu):** RF-42 bỏ sót **621 (10.24%)**; Stacking-42 bỏ sót **754 (12.44%)**. Giữa hai model có **47 ca được Stacking cứu**, nhưng **180 ca mới bị Stacking bỏ sót** ⇒ Stacking tăng ròng **133 FN** ở Fuzzers. Wilson 95% CI cho riêng miss rate: RF **[9.51%, 11.03%]**, Stacking **[11.63%, 13.29%]**.

**Generic (18,871 mẫu):** RF bỏ sót **57 (0.302%)**; Stacking bỏ sót **14 (0.074%)**. Stacking cứu được **43 ca**, không phát sinh ca Generic bỏ sót mới trong cặp mô hình này ⇒ **giảm ròng 43 FN**.

**Analysis (677 mẫu):** RF bỏ sót **3**, Stacking **19**; Stacking làm xuất hiện thêm **16 FN** và không cứu ca Analysis nào trong hai model. Do nhóm này ít mẫu hơn Fuzzers/Generic, cần thể hiện support và uncertainty trước khi suy rộng.

Toàn bộ chênh lệch theo family cộng lại: **+133 +16 +5 +4 +1 +1 +1 +0 −43 = +118 FN**. Vì Generic và một số family có biến động ngược chiều, riêng Fuzzers tăng **133** còn lớn hơn mức tăng ròng **118** của toàn test.

## 3. Điều có thể và chưa thể kết luận

**Có thể:** Nói Stacking thay đổi lỗi theo từng attack family, đặc biệt tạo bất lợi trên Fuzzers nhưng lại giảm miss đối với Generic; ghi nhận FP/FN trade-off trên official holdout.

**Chưa thể:** Nói Fuzzers bị bỏ sót thêm **do feature X**, **do hệ số meta LR Y**, hoặc là lỗi triển khai thực tế; Step 1 không phân tích input features/probabilities và không chứng minh cơ chế nhân quả. Không dùng kết quả này để tinh chỉnh frozen model.

## 4. CHECKPOINT — Canonical Phase 14

| Task | Status | Evidence |
|---|---|---|
| Step 1 — đọc saved predictions và kiểm đếm cặp | DONE | `class_pairwise_transitions.csv`; `PHASE14_STEP1_SUMMARY.md` |
| Step 1 — kiểm tra khớp Phase 9–12 | DONE | 7 phép đối chiếu số liệu trong phần 1 |
| Step 2 — phân tích chênh lệch FN theo family | DONE | `attack_family_transitions.csv`; phần 2 |
| Step 3 — mô tả đặc điểm Normal traffic gây FP | TODO | Cần join feature rows vào saved predictions, chỉ phân tích |
| Step 4 — mô tả feature patterns của Fuzzers bị bỏ sót | TODO | Chưa thực hiện |
| Step 5 — tổng hợp Phase 14 và giới hạn | TODO | Chưa thực hiện |

**Bước tiếp theo khi đã hiểu Step 2:** xây dựng phân tích mô tả theo feature trên đúng các sample false positives/new false negatives (không train/tune); trước hết xác minh khóa liên kết giữa các hàng của predictions và official TEST input để không gán nhầm flow.
