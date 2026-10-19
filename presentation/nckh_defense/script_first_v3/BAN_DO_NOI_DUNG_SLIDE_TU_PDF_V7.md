# BẢN ĐỒ TRÍCH XUẤT SLIDE TỪ BÁO CÁO NCKH V7
**Nguyên tắc:** Kịch bản đã chốt thông điệp → chọn bằng chứng từ PDF → dựng trực quan; không chọn template hay hiệu ứng trước rồi điền nội dung. Đây **không phải PPTX**.

**Nguồn đọc:** `presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf` (49 trang); đối chiếu văn bản trích xuất `creative_rebuild_v2/audit/V7_full_text.txt`. **Số trang dưới đây là trang đánh số của phần nội dung trong chính báo cáo**, không phải chỉ số trang PDF viewer (trước Chương 1 còn bìa, cam đoan, mục lục, danh mục...).

## 1. Slide chính — chính xác 8 cảnh cho 360 giây

| Cảnh | Thời gian | Một luận điểm duy nhất | Lấy từ PDF V7 | Cần đưa lên slide | Cách thể hiện và giới hạn |
|---|---|---|---|---|---|
| **S1. Bớt cảnh báo, liệu an toàn hơn?** | 0:00–0:25 | Ít cảnh báo chưa chắc ít rủi ro | Chương 1 §1.1.2, trang in **1**; Chương 4 Bảng **4.1**, Hình **4.1**, trang in **20–21** | Chỉ một câu hỏi lớn: **“Ít cảnh báo hơn = An toàn hơn?”** | Tạo câu hỏi trực quan, không dùng thống kê hack/attack giả. **Chưa bật mí −142/+118** ở cảnh này |
| **S2. Bài toán và dữ liệu** | 0:25–1:05 | Đối chiếu phân loại nhị phân trên split chính thức | Chương 2 §2.1, Bảng **2.1**, Hình **2.1** trang in **10**; §3.1 trang **15** | 175.341 TRAIN; 82.332 TEST; 42 predictor; Normal (0) / Attack (1). Nếu muốn biểu đồ: TRAIN 56.000 Normal / 119.341 Attack; TEST 37.000 / 45.332 | Hai thanh phân bố rõ số hàng, không dùng traffic live. Ghi **UNSW-NB15 — bộ dữ liệu, không phải mạng thực đã triển khai** |
| **S3. Kiến trúc nghiên cứu** | 1:05–1:55 | So sánh RF mạnh với cơ chế Stacking trên dữ liệu đã xử lý | Chương 3 §3.2–3.4, Bảng **3.1**, trang in **15–17** | 42 predictor sau loại `id`, `label`, `attack_cat`; baseline RF-42; Stacking base LR/DT/RF-42 → meta LR từ OOF; RF-17 là pipeline so sánh; ngưỡng 0,5 | Dựng **pipeline mới bằng native shapes/vector**, không chụp ảnh trang PDF. **OOF chỉ tạo meta-training ở bước fit**, không lấy xác suất từ TEST để train meta. Voting chỉ là development, KHÔNG ghi Voting là một trong ba pipeline final |
| **S4. Thước đo lỗi** | 1:55–2:25 | FP và FN quan trọng hơn mỗi Accuracy | Chương 1 §1.2.1 & §1.2.6 trang **3, 6**; Chương 4 §4.1, công thức **(4.1)** trang **20** | FP: Normal → Attack; FN: Attack → Normal; FPR=FP/(TN+FP); FNR=FN/(TP+FN); Macro-F1 và MCC là chỉ số đi kèm | Hai thẻ đối xứng, không phải hình cán cân chung chung. Nhấn trực quan *loại lỗi* thay vì bày toàn bộ ma trận 2×2. Không gọi mọi FP “một cuộc tấn công” |
| **S5. Kết quả official TEST** | 2:25–3:20 | Stacking đổi cơ cấu lỗi, chưa chứng minh ưu thế tổng thể | Bảng **4.1** trang **20**, Bảng **4.2** và Hình **4.1** trang **21**, Hình **4.2** trang **22** | RF-42 Macro-F1 **0,863343** / Stack-42 **0,863840** (Δ **+0,000497**); CI hiệu số **[−0,000312; +0,001309]**, chứa 0. FP **10.003 → 9.861** (**−142**); FN **734 → 852** (**+118**) | Làm **hai so sánh FP và FN tách biệt**, đúng đơn vị “số trường hợp” trên cùng 82.332 TEST. Đọc từ biểu đồ lấy số, không phóng đại chênh lệch Macro-F1. Caption “**official TEST lịch sử**”; không dùng đồ thị P21 tại đây |
| **S6. Vì sao thêm P21?** | 3:20–4:05 | Đối chứng matched khắc phục một số confound lịch sử | Chương 3 §3.2 và §3.6.1–3.6.3, Bảng **3.2**, trang in **15–19**; §4.9 trang **28** | Historical stable17 được chọn trước development CV; RF17 và RF42 lịch sử có số cây/lá khác. P21 chỉ dùng TRAIN **175.341** → FIT pool **140.272** + validation chung **35.069**, 5 FIT seed × 60.000 FIT rows, 5 arm (A0–A4) | Diagram nhánh có nhãn đúng: **5 tập FIT, cùng một validation**. A0 RF42-Lite; A1 RF17-Lite FIT-only FS; A2 Balanced; A3 Normal FIT-only Oversample; A4 Stacking-Lite. **Không mô tả 5 independent TEST; không gộp pipeline Lite với mô hình official TEST** |
| **S7. Kết quả P21 và chi phí** | 4:05–5:13 | Ensemble/FS/cân bằng lớp có đánh đổi | Bảng **4.8**/**4.9** trang **28**, Bảng **4.11** trang **29**, §4.9.4 trang **30** | Macro-F1 A0 **0,945220**, A4 **0,944731**, A1 **0,936751**. FIT: RF42 **241,119s**, RF17 **84,600s**; FS **225,250s**; FS+RF17 **309,850s**. Balanced so với A0: FPR **−3,1643 điểm phần trăm**, FNR **+1,7881 điểm phần trăm** | Ba khối ngắn: **Chất lượng / Chi phí / Loại lỗi**. Không dùng 0,945 của P21 để tuyên bố tốt hơn 0,863 official TEST; P21 là validation khác và cấu hình Lite. Chi phí là các bước **được đo**, chưa phải latency triển khai end-to-end |
| **S8. Kết luận** | 5:13–6:00 | Giá trị là phép kiểm chứng minh bạch, không phải thuật toán mới | Chương 5 §5.4–5.9, trang in **33–36** (đặc biệt §5.9 trang **35–36**) | Đối chiếu có kiểm soát / phân tích FP–FN / công khai giới hạn; hướng sau: external data, temporal/session split, chi phí SOC thực | Slide closing một thông điệp: **“Chọn mô hình theo loại lỗi và chi phí, không chỉ theo điểm tổng hợp.”** Không nói đã triển khai NIDS real-time hoặc hệ thống sản xuất |

### Ba nhãn phạm vi nghiên cứu phải luôn đúng

1. **Historical official TEST:** 82.332 dòng, pipeline RF42 / Stacking42 / RF17 lịch sử; Macro-F1 khoảng 0,86. Không trộn với P21.
2. **P21 TRAIN-derived internal validation:** 35.069 dòng validation cố định, năm tập FIT độc lập có kiểm soát (mỗi tập 60.000 dòng) nhưng *không phải* năm validation độc lập; Macro-F1 quanh 0,94 trong protocol Lite. Thí nghiệm hậu nghiệm.
3. **Báo cáo giới hạn:** không có external temporal/session holdout ngoài benchmark, chưa định lượng chi phí SOC thực, chưa có triển khai NIDS vận hành.

## 2. Các số liệu gốc cần kiểm tra trước khi dựng chart

| Nhóm | Trích PDF V7 | Đơn vị và phạm vi |
|---|---|---|
| Dữ liệu | TRAIN 175.341; TEST 82.332 | Bảng 2.1, trang in 10 |
| Chia lớp TRAIN | 56.000 Normal; 119.341 Attack | Bảng 2.1 |
| Chia lớp TEST | 37.000 Normal; 45.332 Attack | Bảng 2.1 |
| RF42 TEST | Macro-F1 0,863343; MCC 0,750910; FPR 27,0351%; FNR 1,6192%; FP 10.003; FN 734 | Bảng 4.1, trang in 20 |
| Stack42 TEST | Macro-F1 0,863840; MCC 0,750497; FPR 26,6514%; FNR 1,8795%; FP 9.861; FN 852 | Bảng 4.1 |
| Paired Macro-F1 TEST | Δ +0,000497; bootstrap 95% CI [−0,000312; +0,001309] | Bảng 4.2, trang in 21; CI chứa 0 |
| P21 A0 | Macro-F1 0,945220 (SD FIT 0,000399) | Bảng 4.8, trang in 28; same validation |
| P21 A4 | Macro-F1 0,944731 (SD FIT 0,000340) | Bảng 4.8 |
| P21 A1 | Macro-F1 0,936751 | Bảng 4.8 |
| P21 A2 Balanced | ΔFPR −3,1643 đpp; ΔFNR +1,7881 đpp (so với A0) | Bảng 4.9; không hiểu là % tương đối |
| P21 A3 Oversample | ΔFPR −2,2089 đpp; ΔFNR +1,1680 đpp | Bảng 4.9 |
| Chi phí P21 | RF42 241,119s; RF17 84,600s; selector 225,250s; selector + RF17 309,850s | Bảng 4.11 trang in 29; không phải end-to-end đầy đủ |

**Quy tắc làm tròn:** Giữ 6 chữ số thập phân trong các số Macro-F1 trên slide bằng chứng; trong lời nói có thể diễn giải “khoảng 0,863” nếu không đọc từng chữ số. Dấu phẩy thập phân và dấu chấm ngăn nghìn cần nhất quán theo tiếng Việt.

## 3. Những bằng chứng cần đưa vào Q&A, không nhồi trong 6 phút

| Phụ lục | Nội dung | Lấy từ PDF V7 |
|---|---|---|
| **Q1. Tính mới** | Case-study audit có kiểm soát, không thuật toán mới | §1.1.2–1.1.4 trang 1–2; §5.9 trang 35–36 |
| **Q2. Pipeline & OOF** | Stacking LR/DT/RF, meta LR, khác Voting; inner OOF và leakage | §1.2.4 trang 5; §3.3–3.4, Bảng 3.1 trang 16–17 |
| **Q3. Kiểm định cặp** | Paired bootstrap 95% Macro-F1/MCC CI chứa 0; McNemar kiểm tra đúng/sai tổng thể, không trực tiếp Macro-F1 | §4.3, Bảng 4.2, Hình 4.2 trang 21–22; §5.4 trang 33 |
| **Q4. Voting & diversity** | Bảng development pooled OOF: RF 0,950387; Hard Voting 0,947325; Soft Voting 0,946758; Stack 0,951484. Không phải kết quả TEST | §4.7, Bảng 4.6 trang 24–25 |
| **Q5. Sai số theo họ tấn công** | Fuzzers: Stack FN 754/6062; RF42 FN 621/6062; Generic: Stack 14 so với RF42 57; binary task, phân nhóm sau dự đoán | §4.5 Bảng 4.4–4.5 trang 23 |
| **Q6. Vector trùng** | 8.541 TEST vectors trùng chính xác 42 predictor với TRAIN; view còn 73.791 TEST; không chứng minh session/temporal độc lập | §2.5, Bảng 2.3 trang 13; §4.6, Bảng 4.7 trang 24, 26 |
| **Q7. Vì sao RF17 không chứng minh FS tốt hơn?** | Historical RF17 dùng 150 cây, leaf=2; RF42 300 cây, leaf=1. P21 sửa matched, selector FIT-only; chi phí FS tổng | §3.2–3.3 trang 15–16; §4.9.3 Bảng 4.11 trang 29 |
| **Q8. Cost ratio FP/FN** | Loss giả định L=FP+rFN, hòa vốn hai historical pipelines tại r=142/118≈1,2034; dữ liệu chi phí SOC thật chưa có | §5.1.1, Bảng 5.2 trang 31–32 |
| **Q9. P21 là 5 independent tests?** | Không: 5 FIT seed dùng chung validation 35.069. Không t-test/ANOVA như 5 independent benchmark | §3.6 trang 17–19; Bảng 4.8, 4.10 trang 28–29; §5.8 trang 34–35 |

## 4. Những thứ trong PDF không cần đưa lên slide chính

- Danh sách đầy đủ 17 feature, bảng tương quan SMD/Spearman, toàn bộ chín họ Attack, bảng Wilson CI 95% và các công thức LR/Gini: **dùng phụ lục khi hội đồng hỏi**, trừ khi câu chuyện đổi trọng tâm.
- Toàn bộ lịch sử phase, provenance SHA, version scikit-learn và log RAM/CPU: chỉ cần khi câu hỏi nhắm tái lập; tránh làm loãng 6 phút.
- Không dùng ảnh hacker/robot/cán cân sinh bởi AI thay thế bằng chứng.
- Không bê nguyên trang báo cáo hoặc ảnh bảng chữ nhỏ; **dựng lại chart/vector từ số thật**. Ghi nhãn nguồn bảng, tập dữ liệu, đơn vị.
- Không ghép RF42 historical với RF42-Lite P21 thành một trục trước/sau; không suy ra model tốt lên do P21.
- Không tạo mô phỏng thu thập lưu lượng mạng thời gian thực rồi nói đó là hệ thống đã triển khai.

## 5. Trình tự sản xuất slide sau khi duyệt kịch bản

1. Người thuyết trình đọc thử từng đoạn với đồng hồ; nếu dài, cắt chữ trước khi cắt bằng chứng. Kịch bản hiện ~750 từ; có nhiều thuật ngữ và số thập phân nên **chưa xác nhận đã nói đúng 360 giây**.
2. Duyệt **8 thông điệp và số liệu** của phần chính. Ghi nhận mọi yêu cầu thầy cần thêm/bớt.
3. Tạo storyboard trắng đen: câu chính, figure/chart và thời gian mỗi slide. Người xem phải hiểu trước cả khi có animation.
4. Dựng ba nhóm asset thật: (a) dataset split; (b) RF/Stacking/OOF pipeline; (c) ΔFP/ΔFN + chi phí P21. Không dùng PPT cũ làm mẫu cố định.
5. Gắn lời nói theo slide, sau đó mới thiết kế màu/motion để minh họa lời nói.
6. Tạo PPTX, slide Q&A và video luyện tập từ **bản kịch bản được duyệt**, cuối cùng kiểm tra đúng số liệu và nguồn.

**Trạng thái:** KỊCH BẢN + SOURCE MAP SẴN ĐỂ NGƯỜI DÙNG DUYỆT. Chưa tạo PPTX hoặc MP4 mới theo chiến lược này.
