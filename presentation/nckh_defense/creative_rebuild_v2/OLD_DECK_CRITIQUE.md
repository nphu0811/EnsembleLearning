# OLD DECK CRITIQUE

Audit thực trên `../NCKH_Ensemble_IDS_Final.pptx` và `../NCKH_Ensemble_IDS_Preview.mp4`, không dùng PDF thay đầu vào.

| Chỉ tiêu | Đo trực tiếp |
|---|---:|
| Slides |32|
| Cảnh chính / keyframe chính |8 /20|
| Native shape instances toàn deck |828|
| Slide có transition markup |20|
| Morph thật |12 slide: [3, 5, 6, 7, 9, 10, 12, 13, 14, 16, 17, 19]|
| Slide có p:timing |0|
| animMotion nội bộ |0|
| Video |360.000000s,1920×1080,30fps|
| Đoạn gần tĩnh dài nhất ở sampling1fps |23s|

20 slide có transition markup gồm slide đầu không effect; không phải20animation. Morph12slide có thay đổi geometry giữa keyframe, song **không có animation timeline nội bộ**.828đối tượng là số instance qua slide, không phải828ý tưởng hoặc828vật thể độc lập; cùng actor được nhân bản để Morph. Vì vậy, nhận xét trước rằng có chuyển động phải được giới hạn ở chuyển tiếp giữa keyframe, chưa đáp ứng yêu cầu motion trong cảnh.

## Thiết kế và nhịp dựng

Nền trắng và hệ thống Aptos/cỡ tiêu đề36pt được lặp gần toàn bộ. Khoảng trắng lớn giúp đọc nhưng không được tổ chức thành thay đổi tỷ lệ, nhịp editorial hoặc điểm nhấn hình ảnh. Các scene phần lớn có cùng vị trí tiêu đề trên cùng. Bảng màu thiên về navy/blue/cyan với cam cho FN; chưa có color arc. Đổi màu các trang đơn thuần sẽ không sửa vấn đề này.

Sơ đồ pipeline chỉ có5khối chữ nhật và mũi tên. Chấm flow đổi vị trí bằng Morph khoảng0.9s rồi giữ trạng thái lâu. RF/Voting/Stacking chưa giải thích OOF theo fold bằng chuyển động: người nói phải gánh hầu hết cơ chế. Các chart đúng số liệu và có ghi thang riêng/trục rút gọn, nhưng kích thước và bố cục gần slide công sở; mức −142/+118 chưa trở thành một khoảnh khắc có sức nặng. Font chỉ có1họ, phân cấp ít tương phản; source/rail chiếm attention lặp lại.

Kiểm travideo1fps cho 20đoạn gần tĩnh từ3s trở lên, dài nhất23s. Điều này xác nhận phần lớn thời lượng là giữ slide sau transition. Không dùng metric pixel đơn độc làm đánh giá nghệ thuật; các render/video cũ và choreography cũng cho thấy không có packet/path/typography chạy theo timeline nội bộ.

## Yêu cầu sửa có thể kiểm chứng

Thiết kế mới phải dùng typography hero thật, tương phản sáng/tối/vùng màu, bố cục bất đối xứng và timeline nội bộ. Mỗi hero cần packet/path/node/bar/label biến đổi có ý nghĩa, có số giây vàshapeID. OOF fit vàinference phải tách rõ. Animation cần ở PPTX vàMP4 cùng engine; XML vàframe liên tiếp là hai bằng chứng riêng. Có thể giữ dữ liệu đã kiểm chứng, nhưng không giữ template/bố cục cũ.

Nguồn máy đọc: `audit/old_deck_metrics.json`. Không sửa file cũ.
