from pathlib import Path
from creative_content import MAIN
changes={
10:'Trên tập kiểm thử chính thức, Macro F một của hai mô hình đều gần không phẩy tám sáu ba. Stacking chỉ nhỉnh hơn rất ít, còn MCC thấp hơn một chút. Khoảng tin cậy của cả hai hiệu số đều chứa số không. Chưa có bằng chứng rõ rằng Stacking vượt trội.',
11:'Về cảnh báo giả, Random Forest báo nhầm mười nghìn không trăm lẻ ba bản ghi bình thường. Stacking còn chín nghìn tám trăm sáu mươi mốt. Mức giảm là một trăm bốn mươi hai. Nhưng trên cùng tập kiểm thử, đây mới chỉ là một phía của kết quả.',
13:'Nhóm bổ sung P hai mươi mốt để kiểm tra có đối chứng. Năm seed huấn luyện, mỗi seed dùng sáu mươi nghìn dòng FIT. Năm nhánh gồm rừng bốn mươi hai biến, rừng mười bảy biến, trọng số lớp, lấy mẫu bổ sung và Stacking Lite. Tất cả dùng chung một validation cố định từ TRAIN; không phải năm tập kiểm thử độc lập.',
14:'Trong P hai mươi mốt, Random Forest Lite vẫn có Macro F một trung bình nhỉnh hơn Stacking Lite. Rừng mười bảy biến học nhanh hơn sau khi chọn biến. Nhưng cộng bước chọn, thời gian lên khoảng ba trăm mười giây, cao hơn hai trăm bốn mươi mốt giây của rừng bốn mươi hai biến. Chất lượng dự đoán cũng giảm. Vì vậy phải tính cả bước chọn biến.',
15:'Trong P hai mươi mốt, tăng trọng số lớp và lấy mẫu bổ sung đều giảm tỷ lệ cảnh báo giả, nhưng tăng tỷ lệ bỏ sót. Bình thường mới là lớp ít mẫu trong TRAIN này. Can thiệp cân bằng vì thế ưu tiên lớp bình thường hơn. Đây là hướng dịch chuyển lỗi trong các cấu hình đã thử, không có nghĩa cân bằng lớp luôn có hại.',
16:'Nhóm giả định một cảnh báo giả tốn một đơn vị, còn một lần bỏ sót tốn r đơn vị. Với dự đoán kiểm thử lịch sử, hai mô hình hòa nhau khi r khoảng một phẩy hai. Khi bỏ sót đắt hơn mức này, Random Forest có tổn thất thấp hơn Stacking. Đây là giả định để đọc kết quả, chưa phải thiệt hại đo tại trung tâm vận hành.',
17:'Qua các thí nghiệm, nhóm thấy ghép thêm mô hình chưa chắc giúp phát hiện tấn công tốt hơn. Cần đọc kết quả cùng loại lỗi và chi phí của nó. Nhóm đã đối chiếu cấu hình, bổ sung đối chứng và nêu giới hạn chọn đặc trưng lịch sử. Bước tiếp theo là kiểm chứng trên dữ liệu mạng mới và đo chi phí thực tế. Nhóm xin cảm ơn hội đồng.',
}
p=Path(__file__).with_name('creative_content.py');s=p.read_text(encoding='utf-8')
for i,t in changes.items():s=s.replace(repr(MAIN[i-1][4]),repr(t))
p.write_text(s,encoding='utf-8');print('Shortened',len(changes),'passages')
