# NCKH IDS — Bàn giao tiếp nối phiên Codex bị hết token (19/10/2026)

## Tình trạng thực tế trong GitHub

Đã có toàn bộ artifact Creative Rebuild V2 trong chính thư mục này, commit xuất xứ **3795580**. Người dùng **không cần dựng lại từ đầu** hoặc chạy lại mô hình.

| Sản phẩm | Đường dẫn |
|---|---|
| PowerPoint chỉnh sửa được (29 slide) | [NCKH_Ensemble_IDS_Creative_Final.pptx](NCKH_Ensemble_IDS_Creative_Final.pptx) |
| Video 6 phút có motion + TTS | [NCKH_Ensemble_IDS_Creative_Preview.mp4](NCKH_Ensemble_IDS_Creative_Preview.mp4) |
| Báo cáo humanized V7, 49 trang | [Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf](Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf) |
| Gói file hoàn chỉnh | [NCKH_Ensemble_IDS_Creative_Delivery.zip](NCKH_Ensemble_IDS_Creative_Delivery.zip) |
| Bộ slide tĩnh (có 12 trang Q&A) | [NCKH_Ensemble_IDS_Static.pdf](NCKH_Ensemble_IDS_Static.pdf) |
| Kịch bản và timeline | [Kich_ban_6_phut_Humanized.md](Kich_ban_6_phut_Humanized.md) |
| Bộ đáp án phản biện | [QnA_Humanized.md](QnA_Humanized.md) |
| Chứng cứ kỹ thuật ban đầu | [QA_Report.md](QA_Report.md) |

Không đưa nhầm PPTX/MP4 **bản cũ** ở thư mục cha \`presentation/nckh_defense/\` khi thuyết trình. Bản sáng tạo mới ở \`creative_rebuild_v2/\`.

### 8 cảnh chính / 6 phút

| Cảnh | Mốc phát | Nội dung |
|---|---|---|
| 1 | 00:00–00:20 | Câu hỏi: bớt cảnh báo có an toàn hơn? |
| 2 | 00:20–00:55 | Đặt vấn đề IDS / benchmark |
| 3 | 00:55–01:55 | Pipeline và OOF |
| 4 | 01:55–02:50 | RF, Voting, Stacking |
| 5 | 02:50–03:55 | Official TEST, −142 FP / +118 FN |
| 6 | 03:55–04:45 | P21 matched, 5 FIT seed / 1 validation, chi phí FS |
| 7 | 04:45–05:35 | FPR/FNR và cost sensitivity |
| 8 | 05:35–06:00 | Đóng góp, giới hạn, kết luận |

17 slide phát tự động cho 8 cảnh trên. 12 slide Q&A nằm sau đó, đánh dấu hidden, truy cập bằng A1–A12 từ slide kết luận. Không phát Q&A trong 6 phút.

## Việc người trình bày CẦN thực hiện trước khi bảo vệ

1. **Nghe từ đầu đến cuối MP4 một lần bằng tai người Việt.** Kiểm tra cách đọc của UNSW-NB15, Random Forest, Voting, Stacking, Logistic Regression, Macro-F1/MCC, P21, FPR/FNR, các số 175.341/82.332, 10.003/9.861/734/852, 225,250 s và 309,850 s. Kết quả ASR tự động nhiều chỗ nghe nhầm từ chuyên ngành; không được lấy ASR làm bằng chứng xác nhận phát âm đúng.
2. **Tập thuyết trình bằng giọng thật trong 6 phút.** Bản TTS có 319,056 giây giọng nói trong slot 360 giây; đây chưa phải một phép đo tốc độ của nhóm. Dùng chính [kịch bản](Kich_ban_6_phut_Humanized.md) và không ép nói nhanh đến mức khó nghe.
3. **Chạy slideshow trong PowerPoint desktop trên máy trình chiếu.** Các animation là PowerPoint native timeline, không có Morph. Kiểm tra bật **Use Timings**, slide show 6 phút, đúng thứ tự scene. File PPTX không nhúng narration: MP4 có voice luyện tập, còn lúc thuyết trình cần nói trực tiếp.
4. **Thử nhảy Q&A:** từ slide kết luận bấm A1–A12; quay về kết luận; phải kiểm tra các link trên đúng phiên bản Microsoft PowerPoint sẽ sử dụng. Nếu trình chiếu qua Google Slides hoặc LibreOffice, không mặc định hỗ trợ tương đương.
5. **Lưu bản dự phòng tại máy và USB:** PPTX, MP4, PDF tĩnh, kịch bản, file V7. Không dùng MP4 nếu máy không phát được hoặc kịch bản đã chỉnh sau khi xuất video mà chưa tái đồng bộ.

## Phạm vi QA kỹ thuật và điều chưa thể tuyên bố

Phiên Codex gốc công bố 17/17 slide chính có \`p:timing\`, 439 native animation effects, 59 motion paths, 15 scale events; video được xuất từ PowerPoint với thời lượng 360,000 s/1080p30. Xem thêm [QA_Report.md](QA_Report.md). Chương trình kiểm định độc lập bổ sung ở \`tools/verify_creative_release_portable.py\` và GitHub Actions \`verify-creative-v2-delivery.yml\`; coi kết quả **chính thức** theo kết luận CI gần nhất thay vì tự suy đoán.

Video/slide được thiết kế từ mô hình nghiên cứu offline trên UNSW-NB15; không minh họa một hệ thống bắt gói mạng thật đã triển khai. Báo cáo V7 chỉ thay diễn đạt, không làm mới độ tin cậy external TEST. Tuyên bố nghiên cứu vẫn giữ giới hạn: P21 là TRAIN-derived validation dùng chung năm FIT seed; cảnh cost model chỉ là giả định.

**Handoff:** Khối lượng tạo artifact đã có đủ, phần cần người sử dụng nghiệm thu là phát âm, khả năng trình chiếu trên máy phòng thi và phản hồi thiết kế từ người xem. Không nên tiếp tục chỉnh/đánh bóng file đã đóng gói chỉ vì muốn báo hoàn tất mà không tạo và kiểm tra lại tất cả bản phát hành.
