# CONTENT PACK & TIMELINE — 10 SLIDE NCKH ENSEMBLE IDS

**Nguồn nội dung:** báo cáo [PDF V7](https://github.com/nphu0811/EnsembleLearning/blob/main/presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf) và [bản đồ bằng chứng](../BAN_DO_NOI_DUNG_SLIDE_TU_PDF_V7.md). Câu chữ trên slide **ít hơn** lời thuyết trình; không sao chép bảng PDF.

**Thời lượng:** 360 giây nội dung gồm animation/chuyển trang; không gồm Q&A 4 phút. **Hình thức:** 1 slide mở đầu, 7 slide nội dung, 2 slide kết thúc. Tất cả con số thuộc phạm vi bằng chứng đã gắn nhãn, không truy cập TEST mới.

| Slide | Timeline | Màu | Ý trên slide & asset cần dựng |
|---|---|---|---|
| 1. HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG | 00:00–00:12 (12s) | cream | Logo PTIT chính thức, tên đề tài, bốn thành viên, lớp và GVHD. Chữ chủ đạo và dải đỏ trường; đèn mạng chuyển động. |
| 2. CÂU HỎI NGHIÊN CỨU | 00:12–00:35 (23s) | ink | Câu hỏi lớn về cảnh báo giả; không công bố trước kết quả. Liên kết dải đỏ từ slide bìa. |
| 3. 01 / PROBLEM & DATA | 00:35–01:15 (40s) | cream | 175.341 TRAIN / 82.332 TEST / 42 predictor / Normal–Attack. Đồ họa số lớn và luồng dữ liệu. |
| 4. 02 / HOW WE TESTED | 01:15–02:05 (50s) | white | Luồng dữ liệu qua tiền xử lý, ba mô hình cơ sở, OOF cho meta-learner; phân biệt fit và inference. |
| 5. 03 / WHAT MATTERS | 02:05–02:35 (30s) | ink | Giải thích FP / FN và nhắc Macro-F1, MCC, FPR, FNR, không dành slide cho công thức phức tạp. |
| 6. 04 / OFFICIAL TEST · 82.332 MẪU | 02:35–03:36 (61s) | coral | Official TEST lịch sử: RF42 vs Stacking42, Macro-F1 gần nhau; giảm 142 FP nhưng tăng 118 FN. |
| 7. 05 / WHY P21? | 03:36–04:19 (43s) | cream | Vì sao P21 cần thiết: selection bias lịch sử và unmatched RF; 5 FIT seed × 5 arm trên chung validation 35.069. |
| 8. 06 / CONTROLLED EVIDENCE | 04:19–05:27 (68s) | white | P21: RF42 0,945220; StackingLite 0,944731; RF17 0,936751; selector+RF17 309,850s; FPR↓/FNR↑ khi balancing. |
| 9. 07 / CONCLUSION | 05:27–05:46 (19s) | ink | Kết luận khoa học: ensemble không tự động vượt trội; chọn mô hình theo loại lỗi và chi phí được đo. |
| 10. 08 / NEXT STEP | 05:46–06:00 (14s) | cream | Hướng phát triển có điều kiện: dữ liệu độc lập, temporal/session split, chi phí SOC; lời cảm ơn, PTIT. |

## Lời nói chính thức (từ `deck_plan.json`)

### Slide 1. ENSEMBLE / LEARNING / / NETWORK IDS (12s)

Kính chào quý thầy cô. Nhóm em xin trình bày đề tài nghiên cứu Ensemble Learning cho bài toán phát hiện xâm nhập mạng, thực nghiệm trên bộ dữ liệu UNSW-NB15.

*Nguồn: PDF V7: trang bìa.*

### Slide 2. ÍT CẢNH BÁO. / AN TOÀN HƠN? (23s)

Nếu hệ thống phát hiện xâm nhập tạo ra ít cảnh báo hơn, liệu chúng ta đã an toàn hơn chưa? Chưa chắc. Mô hình có thể giảm báo động giả, nhưng đổi lại bỏ sót thêm lưu lượng tấn công. Đó là câu hỏi mở đầu nghiên cứu của nhóm.

*Nguồn: V7: Chương 1, mục 1.1.2.*

### Slide 3. MỘT BỘ DỮ LIỆU. / HAI NHÃN. (40s)

Nhóm nghiên cứu bài toán phân loại nhị phân trên UNSW-NB15. Mỗi dòng lưu lượng được dự đoán là Normal hoặc Attack. Bộ dữ liệu có một trăm bảy mươi lăm nghìn ba trăm bốn mươi mốt dòng huấn luyện và tám mươi hai nghìn ba trăm ba mươi hai dòng kiểm thử chính thức. Sau khi loại các cột định danh và nhãn, nhóm sử dụng bốn mươi hai đặc trưng dự đoán. Mục tiêu không chỉ là Accuracy cao, mà là hiểu các kiểu sai của mô hình.

*Nguồn: V7: Bảng 2.1; mục 3.1.*

### Slide 4. TỪ FLOW / ĐẾN QUYẾT ĐỊNH (50s)

Nhóm giữ Random Forest với bốn mươi hai đặc trưng làm đối chứng mạnh. Bên cạnh Random Forest mười bảy đặc trưng, nhóm khảo sát cơ chế Stacking với Logistic Regression, Decision Tree và Random Forest ở tầng cơ sở. Khi huấn luyện Stacking, các dự đoán ngoài fold được dùng để tạo dữ liệu cho Logistic Regression tầng kết hợp. Khi dự đoán, dữ liệu đi qua các mô hình đã huấn luyện để tạo quyết định Normal hoặc Attack. Việc đánh giá trên TEST chính thức chỉ thực hiện với những cấu hình đã khóa.

*Nguồn: V7: mục 3.2–3.4; Bảng 3.1.*

### Slide 5. ĐÚNG NHIỀU / CHƯA ĐỦ. (30s)

Để đọc kết quả IDS, cần phân biệt hai loại lỗi. False Positive là lưu lượng bình thường bị báo nhầm thành tấn công, gây thêm công kiểm tra. False Negative là tấn công bị nhận thành bình thường, có thể khiến sự cố bị bỏ qua. Bởi vậy nhóm xem đồng thời Macro-F1, MCC, tỷ lệ báo động giả FPR và tỷ lệ bỏ sót FNR.

*Nguồn: V7: mục 1.2.1, 1.2.6; công thức 4.1.*

### Slide 6. GIẢM 142 FP. / TĂNG 118 FN. (61s)

Đây là kết quả trên cùng tám mươi hai nghìn ba trăm ba mươi hai dòng TEST chính thức. Macro-F1 của Random Forest bốn mươi hai đặc trưng là không phẩy tám sáu ba ba bốn ba; Stacking là không phẩy tám sáu ba tám bốn không. Hiệu số rất nhỏ và khoảng tin cậy chứa số không, nên chưa có bằng chứng để kết luận Stacking vượt trội về điểm tổng hợp. Nhưng Stacking giảm False Positive từ mười nghìn không trăm lẻ ba xuống chín nghìn tám trăm sáu mươi mốt: ít hơn một trăm bốn mươi hai trường hợp. Đổi lại False Negative tăng từ bảy trăm ba mươi bốn lên tám trăm năm mươi hai: thêm một trăm mười tám trường hợp. Điều này cho thấy ít cảnh báo hơn không nhất thiết đồng nghĩa với khả năng phát hiện tấn công tốt hơn.

*Nguồn: V7: Bảng 4.1, 4.2; Hình 4.1, 4.2.*

### Slide 7. ĐỐI CHỨNG / CÔNG BẰNG HƠN. (43s)

Phần đánh giá lịch sử còn hai hạn chế. Danh sách mười bảy đặc trưng đã được chọn trước development cross-validation; và Random Forest mười bảy với bốn mươi hai đặc trưng không chỉ khác đầu vào mà còn khác siêu tham số. Nhóm vì thế bổ sung P21 để kiểm soát các yếu tố này. P21 chỉ dùng dữ liệu TRAIN, tạo năm tập FIT, mỗi tập sáu mươi nghìn dòng, để kiểm tra năm cấu hình trên cùng một validation ba mươi lăm nghìn không trăm sáu mươi chín dòng. Đó là thí nghiệm nội bộ hậu nghiệm, không phải năm tập TEST độc lập.

*Nguồn: V7: mục 3.2, 3.6; Bảng 3.2.*

### Slide 8. CHẤT LƯỢNG. / CHI PHÍ. SAI SỐ. (68s)

Kết quả P21 tiếp tục cho thấy Stacking không tự động thắng Random Forest. Macro-F1 trung bình của RF42-Lite là không phẩy chín bốn năm hai hai không, còn Stacking-Lite là không phẩy chín bốn bốn bảy ba một. Khi giữ siêu tham số Random Forest tương đồng, phiên bản mười bảy đặc trưng đạt không phẩy chín ba sáu bảy năm một, thấp hơn bản bốn mươi hai. Riêng thời gian fit, bản mười bảy đặc trưng nhanh hơn, khoảng tám mươi lăm giây so với hai trăm bốn mươi mốt giây. Nhưng cộng khoảng hai trăm hai mươi lăm giây để chọn lại đặc trưng, tổng chi phí các công đoạn đo được là ba trăm mười giây. Các can thiệp cân bằng lớp làm giảm báo động giả nhưng tăng tỷ lệ bỏ sót tấn công. Vì vậy, phải xét cả chất lượng, thời gian và hướng dịch chuyển sai số.

*Nguồn: V7: Bảng 4.8, 4.9, 4.11; mục 4.9.*

### Slide 9. KHÔNG CÓ / MÔ HÌNH TỐT NHẤT / CHO MỌI LỖI. (19s)

Điều nhóm rút ra là: kết hợp nhiều mô hình chưa chắc giúp phát hiện xâm nhập tốt hơn. Giá trị của nghiên cứu nằm ở việc so sánh có kiểm soát và chỉ rõ mỗi mô hình giảm loại lỗi nào, tăng loại lỗi nào, cùng chi phí phải trả.

*Nguồn: V7: Chương 5, mục 5.4–5.9.*

### Slide 10. XIN CẢM ƠN / QUÝ THẦY CÔ. (14s)

Nghiên cứu vẫn giới hạn trong UNSW-NB15 và một validation nội bộ dùng lại cho P21. Hướng tiếp theo là thử dữ liệu mạng độc lập và đo chi phí vận hành thực tế. Nhóm em xin cảm ơn quý thầy cô.

*Nguồn: V7: Chương 5, mục 5.8–5.9.*

## Nguyên tắc thiết kế, logo, motion và nội dung dự phòng

- Hình nhận diện PTIT: `presentation/nckh_defense/creative_rebuild_v2/report_v7/source/assets/Logo_PTIT_University.png`. Bìa và trang cảm ơn dùng lớn; các trang nội dung chỉ dùng một dấu hiệu logo nhỏ, nhất quán.
- Cấp độ thông tin: **hero title / một luận điểm / dữ liệu có nguồn**. Không để đoạn văn kịch bản trên slide.
- Mạch liên kết được đề xuất: 01→02 (đỏ PTIT và dấu hỏi); 03→04 (42 predictor thành input); 05→06 (FP/FN thành số); 07→08 (năm FIT seed thành kết quả); 09→10 (đường kết luận dẫn sang cảm ơn).
- Animation PowerPoint gốc: các marker hình tròn có native timeline, transitions fade. Video: chuyển cảnh dissolve, dòng network/packet, thanh dữ liệu và nhịp nhấn thông tin được dựng theo frame. Hai pipeline **có chung nội dung** nhưng không đồng nhất từng frame kỹ thuật; video không phải recording trực tiếp engine PowerPoint.
- Giọng đọc MP4 là **bản thu thử tự động offline** nếu công cụ TTS có sẵn, chưa kiểm duyệt cách đọc tiếng Việt/thuật ngữ. Người bảo vệ nên luyện và thu giọng thật để dùng bản final.
- Các phân tích chi tiết McNemar/Bootstrap, Wilson nhóm Attack, exact-duplicate-filtered view, cost loss `L=FP+rFN`, feature selection multi-method và bảng năm seed thuộc Q&A dự phòng. Không áp dụng thêm model mới hoặc hiệu chỉnh TEST.
- Đối chiếu bắt buộc: RF42 historical ≠ RF42-Lite P21. Các con số FP/FN ở Slide 6 không phải số đo trên mạng live. Chỉ số P21 ở Slide 8 dựa trên internal validation dùng chung.
- Tệp PPTX và MP4 được tự động kiểm định sau build; **không gọi video là bản quay PowerPoint gốc** nếu dựng bằng renderer khung hình riêng.

## Danh sách nghiệm thu người trình bày

- Mở được PPTX trên Microsoft PowerPoint desktop, đúng 10 slide, có native shape/chuyển trang và không mất font.
- Video 6:00 phát liên tục, có chuyển động nội bộ các cảnh quan trọng và không tự bật phụ lục.
- Nghe toàn bộ phần phát âm số học/UNSW-NB15, Logistic Regression, Stacking, OOF, P21. Thay giọng tự động nếu quá máy móc.
- Tập nói 6 phút với người trình bày thực, đảm bảo kết thúc slide 10 trước 4 phút hỏi đáp.
- Nếu thiếu hoặc muốn thầy hỏi sâu: dùng [Q&A bản V7 đã có](../../creative_rebuild_v2/QnA_Humanized.md).

**Chỉ xem bản đã có `technical_qa.json` trạng thái PASS và PDF/MP4/PPTX tồn tại thật là sản phẩm bàn giao hoàn chỉnh.**
