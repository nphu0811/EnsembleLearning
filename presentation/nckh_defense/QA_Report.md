# QA Report — 19/10/2026

**Trạng thái: PASS cho bộ sản phẩm đã kiểm tra.** Không đồng nghĩa hội đồng đã chấm/duyệt hay nghiên cứu đã được kiểm chứng ngoài benchmark.

## Sản phẩm thực tế

| Artifact | Kiểm tra | Kết quả |
|---|---|---|
| PowerPoint chính |32 slide;20 keyframe chính/8 cảnh,12 Q&A ẩn;828 native shapes/text/connectors; notes và liên kết | PASS |
| MP4 cuối |360.000s;1920×1080;H.26430fps;AAC48kHz;12,519,165 bytes | PASS |
| PDF tĩnh |20 trang chính, text selectable, font dấu Việt; word bounding boxes trong trang | PASS |
| Kịch bản |20 voice clip thật, tổng lời đọc299.112s; slot tổng360s | PASS |
| Bằng chứng |P9 counts/CI;P21 5 seed×5 arm read-only verifier;V6 SHA đúng | PASS |
| QA độc lập |Toàn32 qua contact sheet; chi tiết2,10,12,13,16,18,24; sửa và review lại5 trang lỗi | Gate3 PASS |

Automated delivery validation: **48/48 PASS** (`audit/delivery_validation.json`). Không dùng log tự tuyên bố thay artifact; các kiểm tra đọc trực tiếp PPTX/PDF/MP4 và nguồn trên đĩa.

## Độ chính xác khoa học

- Official TEST giữ RF42 Macro-F1=0.863343, Stacking42=0.863840; MCC lần lượt0.750910 và0.750497. Chênh F1 nhỏ, CI ΔF1/ΔMCC chứa0. Không nói tương đương/vượt trội.
- −142 FP và+118 FN đối chiếu trực tiếp confusion counts. Chart phân biệt hai thang FP/FN, không dùng độ dài thanh để đánh đồng chi phí.
- P21 tách riêng từ TRAIN, hậu nghiệm;5 FIT seed dùng1 validation cố định35.069 dòng. Không gọi5 TEST độc lập hay external validation.
- P21 RF17 model-only84.600s; selector225.250s; cộng309.850s, soRF42fit241.119s. Không đánh đồng số này với end-to-end.
- Normal là minority TRAIN. Balanced/Oversample giảm FPR nhưng tăng FNR; không tuyên bố cân bằng lớp tự tăng detection.
- Giới hạn selection bias trướcCV và chưa fully nested trong lịch sử được nêu; P21 không sửa hồi tố. Không training, tuning hay đọc raw TEST trong lượt sản xuất này.9 nguồn quan trọng được hash kiểm tra giữ nguyên.

## Chuyển động và video engine

Microsoft PowerPoint16.0 COM đặt12 chuyển tiếp Morph native (3954),7 fade và một slide đầu không transition;20 slide chính có auto timing. Các cặp trong cảnh kiến trúc giữ `!!actor-*` và biến đổi vị trí/màu;FN bars được resize giữa12→13. Engine xuất `intermediate/PowerPoint_native_silent.mp4`,20slide vật lý (Q&A bị loại khỏi bản sao trong RAM, finalPPTX vẫn32slide).

Bản native dài361.3503s do timing/timebase của exporter. FFmpeg chuẩn hóa timestamp video với hệ số0.996263182845 về360s, chuyển30fps cố định rồi ghép voice-over. Chuyển động xuất từ PowerPoint, **không mô phỏng bằng Manim**. Audio không bị tăng tốc/time-stretch. Ghi rõ thao tác hậu kỳ này thay vì nói MP4 byte-identical với export PowerPoint nguyên thủy.

Giải mã toàn bộ MP4 tới null sạch lỗi. So sánh1.800 frame tại5fps với32 render cho đúng20 trạng thái chính theo thứ tự, không có trạng thái Q&A ổn định. Có một nearest-image false candidate0.2s tại20.0s: đã mở ảnh `video_frames/transient_candidate_00.jpg`, đó là cover đang fade tối, không phải appendix24. Bằng chứng loại phụ lục còn có bản xuất native chỉ20slide. Midpoint chuyển trạng thái lệch0–0.6s so đầu slot là do thời gian transition, nằm trước lời đọc sau chuyển vào. Đã mở và xem5 frame thực của chuyển động kiến trúc và5 frameFN-grow; chấm dịch vị trí và thanh tăng đúng cơ chế. Không dùng screenshot tĩnh để tuyên bố đã kiểm chứng motion.

## Lỗi đã sửa và kiểm tra lại

1. Slide2 có sơ đồ dễ đọc thành Normal→Attack: đổi thành đầu vào bản ghi, hai nhánh Normal/Attack.
2. Slide10 đoạn OOF chồng RF: nâng khối mô hình và ngắt tiêu đề2dòng.
3. Slide12–13 nhãn/số thanh chồng: tách số căn phải phía trên từng thanh, tăng khoảng cách hàng.
4. Slide18 có từ tiếng Pháp: sửa sang “Trung bình”.
5. Đo voice-over phát hiện các đoạn sát slot: rút lời5,6,7,9,14,16; không tăng tốc giọng. Khoảng nghỉ nhỏ nhất sau lời0.712s, đã có khoảng nghỉ dài hơn ở những chỗ chốt ý.
6. COM phát hiện6 line-box vượt khung editable vài pt dù glyph render không bị cắt: tăng tối thiểu line-box trong builder, kiểm tra lại cả6PASS.32PNG trước/sau **SHA giống hệt**, nên không làm lệch video đã xuất.
7. Kiểm tra PDF ban đầu đòi>150ký tự/trang thất bại ở trang8 (sơ đồ cây,138ký tự selectable). Đây là kiểm tra sai cho slide ít chữ. Giữ log thất bại, thay bằng kiểm tra nội dung: tiêu đề của từng slide phải selectable trên đúng trang; không thêm chữ cho đủ test.

## Tự phản biện theo trọng số

| Tiêu chí | Trọng số | Bằng chứng và giới hạn |
|---|---:|---|
| Chính xác khoa học |30% | Map nguồn/hash, kiểm tra số học, QA độc lập; không suy diễn ra mạng thực |
| Mạch kể chuyện |20% | Hook→câu hỏi→pipeline→kết quả→đối chứng→chi phí→kết luận; mỗi cảnh1ý |
| Thiết kế |15% | Trắng–navy–cyan; native vector; bố cục đã review; chưa kiểm thử máy chiếu thật |
| Animation có ý nghĩa |15% | Morph flow/node/bar; runtime frames đã xem. Không có mô phỏng bắt gói hoặc huấn luyện giả |
| Tiếng Việt và thời lượng |10% | Giọng tổng hợp thực đo và video360s; chưa đo giọng thật của sinh viên hoặc hội đồng |
| Chỉnh sửa/ổn định |10% | Native828objects,32notes, jump links; PowerPoint reopen/render/export; viewer khác có thể mất Morph |

Không tự gán điểm hội đồng hoặc chứng nhận chuyên gia. Các ghi chú nguồn/trục nhỏ hơn body là để tra cứu; luận điểm và số chính hiển thị cỡ lớn. Khi bảo vệ, nên mở bằng PowerPoint desktop hỗ trợ Morph và tập2lượt bằng giọng thật để giữ nhịp, đặc biệt tên thuật toán tiếng Anh. Chưa có xác nhận nghe duyệt voice-over bởi người Việt hoặc kiểm thử trên thiết bị hội trường; không ghi các việc đó là PASS.

## Tái lập và phạm vi

`README.md` ghi thứ tự lệnh. Code dựng/artifact đặt trong thư mục riêng. Không thay template gốc, reportV6, protocol, CSV/JSON nghiên cứu. Memory entry STATE19/10 được đối chiếu với STATE18/10 đã lỗi thời và evidence mới, không âm thầm viết lại phase khoa học. Không có công việc nền tiếp tục sau phiên; handoff lưu trên đĩa.
