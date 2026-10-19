# QA Report — Creative Rebuild V2

Kết quả kỹ thuật: **PASS** cho PPTX có timeline thật, MP4 có motion và dữ liệu truy vết được. Các giới hạn tham khảo website và thẩm âm TTS được ghi riêng bên dưới; không tuyên bố đã hoàn tất những kiểm tra không thực hiện được.

## Ba điều kiện loại trực tiếp

|Gate|Kết quả|Bằng chứng|
|---|---|---|
|FAIL1: chỉ transition|Không vi phạm|17/17 main có p:timing;439 effects,59 motion paths,15 scale;0 Morph,0 page transition effect.568 native shape instances toàn29slide|
|FAIL2: slideshow tĩnh|Không vi phạm|PowerPoint CreateVideo; hero frame sequences cùng slide có packet/node/path/bar/kinetic changes; source và7clip đi kèm|
|FAIL3: sai số/phạm vi|Không phát hiện trong audit|CSV confusion counts đối chiếu, mean P21 đã truy vết; TEST/P21 tách;5 FITseed cùng1validation; cost giả định|

## Kiểm tra thực tế

- V7:38 đoạn biên tập ở LaTeX, XeLaTeX/BibTeX/2pass;49trang so V6 50trang.13 nguồn thành phần, bib, số, công thức và block bảo vệ kiểm tra bằng invariants. Đã render tất cả49trang và xem contact sheets; không missing glyph/ref/overfull. Xem Scientific_Integrity_QA và PDF_Comparison_V6_V7.
- PowerPoint: mở bằng Microsoft PowerPoint COM, render29trang, independent screenshot reviewer PASS sau2vòng sửa. Phụ lục mới được kiểm tra lại riêng. Source không flatten slide thành ảnh; font hỗ trợ tiếng Việt. Có hyperlink A1–A12 và quay về kết luận.
- Bounds:0 flag vượt ngưỡng height2pt/width6pt; 2 text box có glyph overhang nhỏ2–6pt, vẫn trong canvas, đã được visual QA. Sửa kích thước box của các trường hợp lớn; main renders sau save trùng byte với renders đã dùng khi kiểm tra video.
- Main17slide/8cảnh.12Q&Aẩn và bản copy xuất video xóa vật lý12trang này trước CreateVideo; không ghép Q&A vào MP4. PDF tĩnh có29trang gồm phụ lục.
- MP4:1920×1080,30fps,360.000000giây. Native duration 360.393300s; PTS factor 0.998908692. Chỉ chuẩn hóa timestamp nhỏ và ghép audio; không mô phỏng motion ngoài PowerPoint. Full stream decode không báo lỗi.
- Lời đọc17MP3: tổng319.056s, voice HoaiMy−5%. Không tăng tốc audio. Mỗi slot bắt đầu sau0,55s, mọi file kết thúc trước slide kế; khoảng nghỉ thực tế ghi trong script/timeline. Đã rút14 đoạn sau lần đo đầu. Đây là đo TTS thực tế, chưa phải đọc thử của thành viên nhóm.
- V6, code nghiên cứu, frozen CSV/P21/protocol, PPTX/MP4cũ đều giữ nguyênSHA. Không fit/retrain, không mởrawTEST để thiết kế kết quả. Đối chiếu chi tiết ở audit/scientific_verification.json.

## Tự phản biện theo trọng số

|Tiêu chí|Trọng số|Tự đánh giá /10|Nhận xét|
|---|---:|---:|---|
|Khoa học|25%|9,5|Scope rõ, số chính xác; còn giới hạn historical selection trong chính nghiên cứu|
|Graphic design|25%|8,3|Giant type, color arc và graph thủ công; hình học vẫn được giản lược để chiếu phòng thi|
|Motion|20%|8,8|Native paths,scale,progressive chart; dùng fixed camera, không dựng3D|
|Storytelling/Việt|15%|8,4|Một luận điểm xuyên suốt, đo lời đọc; TTS chưa được người Việt nghe duyệt|
|Typography|10%|8,8|Hero150–185pt,body khoảng21–30pt; nguồn chân trang nhỏ để truy vết|
|Chỉnh sửa/ổn định|5%|9,2|Native objects và source; cần PowerPoint desktop và fonts tương ứng|

Điểm có trọng số tự đánh giá:8,81/10; là nhận định của người dựng, không phải điểm hội đồng hay chứng nhận độc lập.

## Giới hạn chưa được xác nhận

1. Lollypop/Designathon trả CAPTCHA; Locomotive/Behance bị chặn; ActiveTheory không hỗ trợ browser. Đã lưu ảnh thật và ledger, không nhận đã quan sát các hiệu ứng scroll của các trang bị chặn. Awwwards quan sát được2vị trí cuộn. Concept được tự dựng, không sao chép template.
2. TTS là giọng luyện tập. Đã kiểm tra thời lượng, decode và đối chiếu ASR tự động: các số FP/FN chính được nhận dạng; ASR base sai nhiều dấu và tên tiếng Anh. Môi trường này không cung cấp khả năng nghe audio cho reviewer, nên **chưa chứng nhận thẩm âm/phát âm tên mô hình**. Cần người trình bày nghe duyệt trước khi dùng voice-over ở buổi bảo vệ. Script chữ và số trên slide là chuẩn đối chiếu, không lấy transcript ASR làm nội dung khoa học.
3. Phụ lục15–25giây là mục tiêu câu trả lời chính, chưa đo giọng cho toàn bộ12đoạn. Hội đồng chọn câu hỏi trong4phút, không đọc lần lượt12câu.
4. Kiểm tra mở/render thực hiện trên PowerPoint của máy này. Không chứng nhận Morph/animation tương đương trên Google Slides, LibreOffice hoặc bản web. Không có narration nhúng trong PPTX; MP4 chứa voice, speaker notes chứa lời nói.

## Hồ sơ chứng cứ

audit/native_structure.json; main_render_identity.json; text_bounds.json; independent_v2_visual_qa.md; motion_frame_evidence.json; video_metadata.json; full_video_decode.log; voice_asr.json; scientific_verification.json; report_v7_qa.json; scientific_source_invariants.json. Contact_Sheet.jpg và hero_animations/*_frames.jpg phục vụ kiểm tra nhanh. `checksums.sha256` bao phủ nội dung release, ZIP được kiểm traCRC.
