# Storyboard Cinematic

17slide chính,8cảnh/360s;12phụlụcẩn. Mỗi slide chính có internal timeline. Transitionnone, không dựa vào page transition để giả animation.

|Slide|Cảnh|Slot|Thông điệp|Motion|

|---|---:|---|---|---|

|1|1|00:00–00:20|Bớt cảnh báo. Có an toàn hơn?|Fly hero và packet; nhịp câu hỏi|

|2|2|00:20–00:40|Một bản ghi. Hai khả năng.|Network graph: path drawing, node activation, packet cycles, Normal/Attack labels|

|3|2|00:40–00:55|Dữ liệu cố định. Câu hỏi mở.|Typography TRAIN/TEST và progressive reveal|

|4|3|00:55–01:15|Từ bản ghi đến đầu vào mô hình.|Cột identifier/target gạch/dịch;42 biến và vector tạo tuần tự|

|5|3|01:15–01:35|Khi dự đoán, dữ liệu đi theo đường nào?|Feature vector fan-out LR/DT/RF, bộ gộp, hai đầu ra|

|6|3|01:35–01:55|Huấn luyện tầng kết hợp phải dùng dự đoán OOF.|3lượt fold học/giữ, ghép OOF matrix, fit metaLR|

|7|4|01:55–02:13|Mô hình tham chiếu đã là một ensemble.|Cây bootstrap vector, packet hội tụ|

|8|4|02:13–02:30|Voting có luật gộp cố định.|3 learner → luật gộp cố định, reveal Hard/Soft|

|9|4|02:30–02:50|Stacking học cách gộp xác suất.|Base đã học → xác suất → meta, packet suy luận|

|10|5|02:50–03:10|Điểm tổng hợp gần như ngang nhau.|Hai F1, Δ và CI chứa0|

|11|5|03:10–03:30|142 cảnh báo giả đã giảm đi.|Thanh FP0–11000 grow, giảm142|

|12|5|03:30–03:55|118 bản ghi tấn công bị bỏ sót thêm.|Kinetic+118, thanh FN0–1000 grow|

|13|6|03:55–04:20|Năm lượt FIT. Một validation chung.|5seed×5arm activation→1validation chung|

|14|6|04:20–04:45|Bớt biến. Chưa chắc bớt chi phí.|Selector+RF17 stackbar so RF42fit;F1giảm|

|15|7|04:45–05:10|Ít cảnh báo giả hơn. Bỏ sót nhiều hơn.|FPR/FNR scatter, Balanced/Oversample reveal theo cue|

|16|7|05:10–05:35|Một tỷ lệ chi phí có thể đổi thứ hạng.|Ba cột r=1, r=142/118, r=5; bars cùng thang, hiện theo bước|

|17|8|05:35–06:00|Chọn mô hình từ loại lỗi cần giảm.|Typography kết luận, cue đóng góp/giới hạn/dữ liệu mới|