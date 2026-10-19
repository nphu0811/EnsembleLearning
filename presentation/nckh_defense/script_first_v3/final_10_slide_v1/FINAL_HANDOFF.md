# NCKH Ensemble IDS — Bàn giao 10 slide / 6 phút

**Bản mới:** Dựa trên nội dung báo cáo V7, không dùng bộ 29 slide Creative V2 trước đó làm deck trình chiếu. Giữ nguyên tất cả kết quả train và báo cáo khoa học.

## Các file

- [PowerPoint 10 slide, native shapes](NCKH_Ensemble_IDS_10_Slides_Final.pptx)
- [Video 6 phút chuyển động (TTS offline dự phòng)](NCKH_Ensemble_IDS_10_Slides_Preview.mp4)
- [Video giọng nữ Neural tiếng Việt, nếu đã được publish thành công](NCKH_Ensemble_IDS_10_Slides_Preview_NeuralVoice.mp4)
- [PDF 10 slide](NCKH_Ensemble_IDS_10_Slides_Static.pdf)
- [Storyboard, timeline, toàn bộ lời nói và nguồn PDF](CONTENT_PACK_VA_KICH_BAN_10_SLIDE.md)
- [Số liệu/nội dung có cấu trúc để chỉnh sửa](deck_plan.json)
- [Contact sheet 10 slide](visual_qa/contact_sheet_10_slides.jpg)
- [Kiểm tra số trang, hiệu ứng, thời lượng và so sánh frame](technical_qa.json)

## Cấu trúc 10 slide đúng 360 giây

| # | Từ → đến | Ý chính |
|---:|---|---|
| 1 | 00:00–00:12 | Logo PTIT, thông tin đề tài và GVHD |
| 2 | 00:12–00:35 | Câu hỏi: ít cảnh báo, an toàn hơn? |
| 3 | 00:35–01:15 | UNSW-NB15: TRAIN, TEST, 42 predictor |
| 4 | 01:15–02:05 | Pipeline/OOF/Stacking có kiểm soát |
| 5 | 02:05–02:35 | Hai loại lỗi FP và FN |
| 6 | 02:35–03:36 | Official TEST: −142 FP / +118 FN |
| 7 | 03:36–04:19 | P21: 5 FIT seeds, 1 validation |
| 8 | 04:19–05:27 | P21: Macro-F1, FS cost và FPR/FNR |
| 9 | 05:27–05:46 | Kết luận học thuật |
| 10 | 05:46–06:00 | Hướng phát triển và lời cảm ơn |

Các con số tham chiếu có trong `CONTENT_PACK_VA_KICH_BAN_10_SLIDE.md` và `deck_plan.json`.

## Phương thức animation

- PPTX: 10 transition PowerPoint, 10 vùng timeline native đã retarget các hiệu ứng lên marker đồ họa; infographic dựng bằng 308 đối tượng PowerPoint chỉnh sửa được.
- MP4: dựng từ trang PDF xuất từ CHÍNH PPTX, bổ sung chuyển cảnh dissolve, network packet/flow, vòng node và biểu đồ nhấn số liệu động bằng khung hình, 1920×1080/30 fps/360s. **MP4 là mô phỏng nội dung và chuyển động thiết kế, không phải quay trực tiếp engine PowerPoint**; không nên tuyên bố kỹ thuật của PPTX và MP4 giống từng khung hình.
- Kiểm thử tự động: xác minh đủ 10 slide, shape editable, timing + transition, đúng 360 giây, có 4 cặp frame trong cùng scene thay đổi; render contact sheet từng trang.

## Các bước cần làm trước khi bảo vệ

1. `git pull --ff-only origin main`. Mở đúng PPTX `final_10_slide_v1/` thay vì dùng file `creative_rebuild_v2/`.
2. Xem video từ đầu đến cuối bằng tai người Việt. Giọng Neural là bản **thuyết minh tập thử**, phải kiểm tra cách đọc UNSW-NB15, OOF, FPR, FNR và các con số.
3. Mở PPTX bằng Microsoft PowerPoint desktop (không chỉ LibreOffice/Google Slides), thử các chuyển động và chuyển trang. Đối chiếu khả năng trình chiếu trên máy phòng thi.
4. Tập nói bằng giọng thật trong 6 phút theo content pack. Dành 4 phút còn lại cho Q&A; có thể tham khảo [bộ Q&A từ bản nghiên cứu](../../creative_rebuild_v2/QnA_Humanized.md).
5. Không chỉnh số liệu trong slide sau khi đã nghiệm thu trừ khi kèm chứng cứ đối chiếu báo cáo V7 và cập nhật video theo bản sửa.

**Ghi chú phạm vi khoa học:** official TEST lịch sử khác validation TRAIN-derived P21; năm FIT seed dùng chung validation không phải năm TEST độc lập. Đây là thuyết trình nghiên cứu offline, không phải demo hệ thống giám sát lưu lượng live.
