# Animation Manifest

Toàn bộ motion chính do PowerPoint TimeLine.MainSequence thực thi, xuất bằng PowerPoint CreateVideo. Không có Morph, video nhúng hoặc motion giả lập bằng FFmpeg. Wipe/Fade/Fly ở đây là hiệu ứng trên đối tượng trong slide; transition trang bằng none. FFmpeg chỉ chuẩn hóa timestamp video và ghép lời đọc.

|Slide|Cảnh|Slot giây|Native effects|Motion paths|Scale|
|---|---:|---:|---:|---:|---:|
|1|1|20|12|3|1|
|2|2|20|76|13|11|
|3|2|15|2|0|0|
|4|3|20|39|9|0|
|5|3|20|43|8|0|
|6|3|20|25|0|1|
|7|4|18|63|7|0|
|8|4|17|19|3|0|
|9|4|20|27|4|0|
|10|5|20|8|0|0|
|11|5|20|11|2|0|
|12|5|25|7|0|1|
|13|6|25|52|5|1|
|14|6|25|4|0|0|
|15|7|25|14|2|0|
|16|7|25|24|0|0|
|17|8|25|13|3|0|

Tổng: 17 slide có p:timing, 439 effect nodes, 59 p:animMotion, 15 p:animScale. Đối tượng đích đều tồn tại. 12 phụ lục ẩn. XML kiểm tra trong `audit/native_structure.json`; lệnh COM, motion path và repeat nằm trong `motion_engine.py`. Cấu hình riêng từng đối tượng trong `NCKH_Ensemble_IDS_Creative_Final.motion.json`.

Hero 2/network: slide2; feature:4; ensemble inference:5/9, OOF fit:6; FP/FN:11/12, hai thang riêng; P21:13; cost:16. Clip và chuỗi frame cùng slide nằm trong `hero_animations/`, kiểm tra sai biệt pixel trong `audit/motion_frame_evidence.json`. Pixel khác nhau chứng minh frame thay đổi; kết luận cơ chế cần xem chuỗi frame và source.
