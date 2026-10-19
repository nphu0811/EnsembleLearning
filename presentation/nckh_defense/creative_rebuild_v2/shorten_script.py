from pathlib import Path
from creative_content import MAIN
changes={
3:'Nhóm dùng bộ dữ liệu UNSW-NB15: hơn một trăm bảy mươi lăm nghìn dòng huấn luyện và tám mươi hai nghìn dòng kiểm thử chính thức. Nhóm muốn biết Voting và Stacking có tốt hơn mô hình tham chiếu Random Forest không.',
4:'Đây là pipeline ngoại tuyến trong mã nguồn. Nhóm loại mã định danh, nhãn và tên nhóm tấn công khỏi đầu vào, giữ bốn mươi hai đặc trưng gốc. Biến phân loại được mã hóa; hồi quy logistic có thêm chuẩn hóa. Các phép biến đổi phải học tham số từ phần huấn luyện tương ứng.',
5:'Cùng một bản ghi sau xử lý đi đến hồi quy logistic, cây quyết định và Random Forest. Các mô hình tạo xác suất cho bộ kết hợp ra quyết định, với ngưỡng không phẩy năm đã khóa. Đây là đường suy luận ngoại tuyến; nhóm chưa triển khai bắt gói trực tiếp trên mạng.',
6:'Để huấn luyện Stacking, mỗi mô hình cơ sở học trên một số fold rồi dự đoán fold được giữ lại. Ghép các dự đoán ngoài fold này để huấn luyện tầng kết hợp. Nhờ vậy, tầng cuối không học từ dự đoán trên chính những dòng mà mô hình cơ sở vừa học.',
7:'Random Forest đã kết hợp nhiều cây quyết định. Các cây học từ mẫu và tập đặc trưng ngẫu nhiên rồi tổng hợp dự đoán. Nhóm chọn nó làm mốc mạnh. Thêm một tầng kết hợp phải cho thấy lợi ích cụ thể; nhiều mô hình hơn chưa chắc tốt hơn.',
8:'Voting gộp đầu ra của ba mô hình theo luật cố định. Hard Voting lấy đa số phiếu; Soft Voting lấy trung bình xác suất. Các mô hình có cách học khác nhau, nhưng nếu cùng sai ở những bản ghi khó, phép gộp vẫn có thể giữ nguyên lỗi.',
9:'Stacking dùng hồi quy logistic ở tầng cuối. Tầng này học cách gộp từ dự đoán ngoài fold. Sau đó, mô hình cơ sở được học lại trên dữ liệu huấn luyện để dự đoán bản ghi mới. Ngoài fold phục vụ huấn luyện tầng cuối; đường đang sáng minh họa lúc suy luận.',
}
p=Path(__file__).with_name('creative_content.py');s=p.read_text(encoding='utf-8')
for i,t in changes.items():s=s.replace(repr(MAIN[i-1][4]),repr(t))
p.write_text(s,encoding='utf-8')
print('Shortened',len(changes),'spoken passages; slide values unchanged.')
