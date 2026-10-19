# NCKH — Canonical Phase 14 / Step 5 — Scientific Synthesis & Closure

**Đề tài:** Ensemble Learning cho bài toán Network Intrusion Detection (binary Normal/Attack)  
**Ngày tổng hợp:** 2026-10-11  
**Nature Skill đang sử dụng (theo nghĩa kỹ năng nghiên cứu):** Scientific evidence synthesis / error-analysis reporting.  
**Trạng thái:** **DONE — Phạm vi phân tích hậu nghiệm trên các dự đoán official TEST đã khóa**. Không đồng nghĩa giải thích cơ chế nhân quả hay xác nhận khả năng triển khai thực tế.

## 1. Mục tiêu, dữ liệu và quy tắc

- Mục tiêu: phát hiện ở đâu và theo cách nào Stacking-42 thay đổi các lỗi FP/FN so với RF-42; phân tích đặc điểm các nhóm mẫu bị dự đoán khác nhau.
- Đầu vào: frozen local Phase 9 official-test predictions (thuộc canonical Phase 11 — Evaluation Protocol), Step 1 paired transitions, Step 3 Normal feature profiles, Step 4 Fuzzers feature profiles, thống kê từ canonical Phase 12 (trước đây được gọi local Phase 10).
- Tập official TEST UNSW-NB15: 82.332 flows = 37.000 Normal + 45.332 Attack. Feature `attack_cat` chỉ để phân nhóm phân tích, không phải biến đầu vào binary model.
- Phân tích read-only trên predictions đã khóa. **Không train, tune, đặt lại threshold, chọn feature hay thay đổi kết quả official TEST.**

## 2. Lỗi tổng thể trên frozen official TEST

| Chỉ số | RF-42 | Stacking-42 | Đánh giá đúng phạm vi |
|---|---:|---:|---|
| FP | 10.003 | 9.861 | Stack giảm ròng 142 báo động giả |
| FN | 734 | 852 | Stack tăng ròng 118 tấn công bỏ sót |
| FPR | 27,0351% | 26,6514% | Stack giảm ~0,384 điểm phần trăm |
| FNR | 1,6192% | 1,8795% | Stack tăng ~0,260 điểm phần trăm |
| Macro-F1 | 0,863343 | 0,863840 | Chênh ~+0,000497; chưa có bằng chứng ưu thế đáng tin cậy |
| MCC | 0,750910 | 0,750497 | Chênh ~−0,000413; chưa có bằng chứng ưu thế đáng tin cậy |

Với **37.000 Normal**: both-correct 26.719; RF-only-correct 278; Stack-only-correct 420; both-wrong 9.583. Như vậy Stack sửa 420 RF false alarms nhưng tạo 278 false alarms mới ⇒ **−142 FP**.

Với **45.332 Attack**: both-correct 44.385; RF-only-correct 213; Stack-only-correct 95; both-wrong 639. Stack cứu 95 RF false negatives nhưng sinh 213 false negatives mới ⇒ **+118 FN**.

## 3. Phân tích theo attack family (binary FN, KHÔNG phải multiclass accuracy)

| Attack family | Support | RF FN | Stack FN | Δ FN Stack−RF |
|---|---:|---:|---:|---:|
| Fuzzers | 6.062 | 621 | 754 | **+133** |
| Generic | 18.871 | 57 | 14 | **−43** |
| Analysis | 677 | 3 | 19 | +16 |
| DoS | 4.089 | 4 | 9 | +5 |
| Exploits | 11.132 | 45 | 49 | +4 |
| Reconnaissance | 3.496 | 1 | 2 | +1 |
| Backdoor | 583 | 0 | 1 | +1 |
| Shellcode | 378 | 2 | 3 | +1 |
| Worms | 44 | 1 | 1 | 0 |
| **Tổng Attack** | **45.332** | **734** | **852** | **+118** |

Cụ thể **Fuzzers**: cả hai phát hiện 5.261; RF phát hiện, Stack bỏ sót 180; RF bỏ sót, Stack phát hiện 47; cả hai bỏ sót 574. Do đó **180−47=+133 FN**. Fuzzers FNR RF = 10,24%, Stacking = 12,44%; các tỉ lệ này có mẫu số 6.062 actual Fuzzers.

**Generic** cải thiện ròng 43 FN, nhưng không bù hết bất lợi ở Fuzzers cùng các family còn lại. Nhóm hiếm, chẳng hạn Worms n=44, không đủ cơ sở để khái quát độ tin cậy cao từ tỉ lệ điểm.

## 4. Phân tích feature của Normal false alarms (Step 3)

- `sttl=254`: có 15.049 actual Normal; Stacking sửa 401 RF-FP và tạo 217 FP mới ⇒ **−184 FP**; nhưng cả hai model vẫn có FPR trong nhóm này >57%.
- `sttl=62`: Stacking tạo thêm ròng **42 FP**, bù một phần mức giảm ở `sttl=254`; cộng toàn bộ strata = −142 FP.
- `state=FIN`: có 24.172 actual Normal. Trong nhóm **420** Stack-correct/RF-wrong, có 327 FIN = **77,86%**. Trong **tất cả 24.172 Normal FIN**, Stacking đúng **70,78%**. **Không đảo chiều xác suất**: P(FIN | Stack-sửa-đúng) ≠ P(Stack-đúng | Normal, FIN).
- `state`, `proto`, `sttl` có thể tương quan; phân tích từng biến **không** phân lập ảnh hưởng độc lập.

## 5. Phân tích feature của Fuzzers FNs (Step 4)

- `proto=tcp` (n=3.713 Fuzzers): RF miss 446 (12,01%); Stack miss 535 (14,41%).
- `proto=udp` (n=1.098 Fuzzers): RF miss 175 (15,94%); Stack miss 219 (19,95%). UDP có FNR cao hơn TCP **trên test này và theo điều kiện đã định**; không thể tự suy ra `proto` là nguyên nhân.
- `sttl=254`: **6.047/6.062 Fuzzers (99,75%)**, bao gồm **cả 180 FN mới và 47 FN được cứu**. Đây là một giá trị rất phổ biến trong Fuzzers nên **không đủ** để phân biệt hướng sai khác giữa hai mô hình.
- Trung vị `dload` của nhóm both-caught = 2.277,79; new Stack FN = 2.403,95; Stack-rescued RF FN = 0; both-missed = 3.368,10. **Không** biến những mô tả hậu nghiệm này thành threshold/rule trên official TEST.

## 6. Kiểm định thống kê, kết luận khoa học và hạn chế

Từ kết quả kiểm định paired đã hoàn thành ở **canonical Phase 12**:

- Stack−RF Macro-F1: **+0,000497**, 95% paired bootstrap CI **[−0,000312; +0,001309]** — bao gồm 0.
- Stack−RF MCC: **−0,000413**, 95% paired bootstrap CI **[−0,001938; +0,001140]** — bao gồm 0.
- Exact McNemar, Holm-adjusted **p = 0,468377** trên correctness toàn test.
- Stack−RF FPR: −0,003838 (95% CI [−0,005243; −0,002432]); Stack−RF FNR: +0,002603 (95% CI [+0,001853; +0,003375]). Các khoảng này không chứa 0 theo thiết kế bootstrap đã lưu.

**Kết luận có thể bảo vệ:** Trên frozen official UNSW-NB15 test, Stacking-42 đạt trade-off **ít FP hơn nhưng nhiều FN hơn** RF-42, đặc biệt bất lợi đối với binary detection của Fuzzers và có lợi hơn đối với Generic. **Không có bằng chứng chắc chắn về ưu thế tổng thể trên Macro-F1/MCC**, vì vậy không nên tuyên bố Stacking tối ưu hay thắng RF. Lựa chọn mô hình phụ thuộc chi phí FN/FP và chi phí tính toán trong bối cảnh sử dụng.

**Không được khẳng định:** `sttl`/`proto`/`dload` gây ra lỗi; Stacking meta learner có cơ chế cụ thể đã được chứng minh; các attack families là dự đoán multiclass; kết quả generalize sang dataset khác; p>0,05 chứng minh hai model bằng nhau; hoặc deployment ở ngân hàng đã được xác minh.

## 7. Giới hạn xác thực nguồn

- Các ZIP của Step 1, 3, 4 đã được kiểm tra tính nhất quán nội bộ, gồm đối chiếu CSV giữa các bước và với snapshot đã lưu của frozen local Phase 9 (canonical Phase 11) / statistical canonical Phase 12. File `evidence_reconciliation.json` ghi các phép kiểm tra.
- Script Step 3/4 **báo** PASS khi nối 82.332 IDs, binary labels, attack categories; gói ZIP người dùng gửi chỉ chứa bảng tổng hợp nên bước tổng hợp này **không độc lập chạy lại phép nối từ raw TEST và saved full predictions**.
- Chưa có bằng chứng nhân quả, external dataset replication, scenario/time stratification tin cậy hoặc kiểm thử deployment. Những gì không có bằng chứng không được tô đậm thành kết luận.

## 8. Research Decisions Log

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Không tuyên bố Stacking vượt RF tổng thể | Macro-F1/MCC effect CI chứa 0; McNemar không bác bỏ H0 | Phase12 paired bootstrap & McNemar | Báo cáo hiệu quả như một trade-off, không phải cải tiến chắc chắn |
| Giữ nguyên frozen pipelines sau test | Tránh test-driven selection/leakage | local Phase9 (canonical Phase11) frozen settings + post-hoc reports | Chỉ phân tích lỗi, không thay đổi mô hình |
| Báo cáo Fuzzers, Generic theo family kèm support | Lỗi không đồng đều, tránh trung bình che khuất | Step1 paired errors và Step4 Fuzzers | Nêu rõ nơi Stack tăng/giảm FN |
| Không suy diễn nhân quả từ feature profiles | Mô tả phân nhóm một biến không cô lập các yếu tố đồng biến | Step3/4 distributions | Chỉ đề xuất kiểm định trong nghiên cứu sau |

## 9. CHECKPOINT & Task Board

| ID | Task | Status | Evidence |
|---|---|---|---|
| P14-01 | Paired error transitions | DONE | Step 1: `class_pairwise_transitions.csv` |
| P14-02 | Attack-family binary FN analysis | DONE | Step 1: `attack_family_transitions.csv` |
| P14-03 | Normal FP feature profiles | DONE | Step 3: state/proto/sttl CSVs, verification |
| P14-04 | Fuzzers FN feature profiles | DONE (descriptive scope) | Step 4: group/features CSVs, verification |
| P14-05 | Scientific synthesis, limitations, provenance | **DONE** | Tài liệu này + `evidence_reconciliation.json` + evidence manifest |

**Canonical Phase 14 = DONE trong phạm vi error analysis từ frozen saved artifacts.** Bước kế tiếp duy nhất là **canonical Phase 15 — Reproducibility**. Không nhầm Phase 15 với Scientific Figures (Phase 16) hay viết báo cáo (Phase 17).
