# Storyboard

## Brief và lựa chọn nghệ thuật

Khán giả: hội đồng NCKH Việt Nam, kể cả người không chuyên từng thuật toán. Mục tiêu: hiểu câu hỏi, cách kiểm chứng và đánh đổi; không giới thiệu sản phẩm thương mại. 16:9, 1600×900 render, native shapes/text/connector. Bản chính 20 keyframe = 8 cảnh; 12 phụ lục ẩn.

| Phương án | Rõ ràng /5 | Sáng tạo /5 | Trình chiếu /5 | Công sản xuất tương đối | Quyết định |

|---|---:|---:|---:|---|---|

| Scientific Minimalism | 5 | 3 | 5 | Thấp | Nền, typography và bằng chứng |

| Cinematic Research Storytelling | 4 | 5 | 4 | Cao | Lấy hook, reveal và nhịp nghỉ; không dùng cảnh điện ảnh gây nhiễu |

| Architectural Technology Motion | 5 | 5 | 4 | Vừa | Chọn làm cơ chế chuyển động chính |

Đây là đánh giá thiết kế nội bộ, không phải điểm chấm từ hội đồng. Kết hợp Minimalism + Architecture; dùng cinematic cho nhịp câu chuyện.

## Hệ thống hình ảnh

Trắng #FFFFFF; nền phụ #EFF6FC; navy #0D3560; blue #1769AA; cyan #139DCB; chữ #172B43. Cam nâu #B65B29 chỉ định FN hoặc cấu hình can thiệp, không mã hóa Attack bằng màu đơn độc. Aptos có dấu Việt. Title 36pt; body 18–30pt; số chính 43–64pt. Nguồn và trục nhỏ là chú thích, không mang luận điểm duy nhất.

Signature object: một chấm cyan tượng trưng bản ghi flow. Rail dưới trang giữ nhịp 8 cảnh; trong cảnh kiến trúc chấm đi giữa node có tên !!actor-flow-record. Các node kế thừa tên qua keyframe và đổi trạng thái; thanh FN thay chiều dài giữa slide12–13. Các đối tượng kết thúc scene fade ra; không dùng ghost off-canvas tích lũy.

## Nhịp 8 cảnh

| Cảnh | Khoảng thời gian | Thông điệp |

|---|---|---|

| 1 | 00:00.00–00:20.00 | Cái giá của sai lầm là động lực nghiên cứu. |

| 2 | 00:20.00–01:00.00 | So sánh ensemble với RF mạnh trong đúng phạm vi dữ liệu. |

| 3 | 01:00.00–01:55.00 | Pipeline offline có nhãn/feature/preprocessing tách biệt. |

| 4 | 01:55.00–02:50.00 | Cơ chế gộp quyết định khác nhau; OOF bảo vệ tầng meta. |

| 5 | 02:50.00–04:00.00 | Chênh điểm nhỏ che một đánh đổi FP/FN có ý nghĩa. |

| 6 | 04:00.00–04:55.00 | P21 matched kiểm tra giới hạn; chi phí FS phải được tính. |

| 7 | 04:55.00–05:35.00 | Chọn mô hình theo chi phí lỗi, chưa có giá thiệt hại thực. |

| 8 | 05:35.00–06:00.00 | Đóng góp kiểm chứng trong phạm vi benchmark, giới hạn công khai. |

## Keyframe và chuyển động

| Slide | Cảnh | Slot | Tiêu đề | Choreography |

|---|---:|---|---|---|

| 1 | 1 | 00:00.00–00:20.00 | Một cảnh báo ít hơn. Một rủi ro lớn hơn? | Giữ flow phân nhánh FP/FN; dừng ở câu hỏi mở đầu. |

| 2 | 2 | 00:20.00–00:40.00 | Kết hợp mô hình có giúp IDS tốt hơn? | Fade vào: đầu vào bản ghi, hai nhánh kết quả Normal/Attack. |

| 3 | 2 | 00:40.00–01:00.00 | Một benchmark. Hai phạm vi bằng chứng. | Morph đổi góc nhìn sang hai phạm vi dữ liệu; không gộp điểm. |

| 4 | 3 | 01:00.00–01:10.00 | Mỗi bản ghi đi qua một pipeline rõ ràng | Fade lập toàn cảnh. Chấm cyan ở đầu vào; hình minh họa một flow. |

| 5 | 3 | 01:10.00–01:25.00 | Chỉ giữ thông tin dùng để dự đoán | Morph 0,9 s: chấm flow đi tới feature, node đầu vào đã đi qua giữ màu xanh. |

| 6 | 3 | 01:25.00–01:40.00 | Các mô hình nhận cùng một bản ghi | Morph 0,9 s: chấm tới learner; nhấn quy tắc fit trong phần train. |

| 7 | 3 | 01:40.00–01:55.00 | Một quyết định tạo ra hai loại rủi ro | Morph 0,9 s: chấm tới đầu ra, node phân loại sáng; nêu FP/FN. |

| 8 | 4 | 01:55.00–02:13.00 | Random Forest đã là một ensemble mạnh | Fade: nhiều cây hội tụ vào bộ tổng hợp; không giả lập thuật toán học. |

| 9 | 4 | 02:13.00–02:31.00 | Voting tổng hợp phiếu hoặc xác suất | Morph: LR/DT/RF hội tụ về luật gộp cố định; không dùng xác suất giả làm kết quả. |

| 10 | 4 | 02:31.00–02:50.00 | Stacking học cách kết hợp từ dự đoán OOF | Morph: giữ ba learner có tên trùng, thay tầng gộp thành meta LR; nêu OOF ở training. |

| 11 | 5 | 02:50.00–03:10.00 | Official TEST: khoảng cách rất nhỏ | Fade: hai giá trị Macro-F1 thật, kèm MCC và Δ rõ ràng. |

| 12 | 5 | 03:10.00–03:28.00 | Stacking giảm 142 cảnh báo giả… | Morph sang thanh FP; vùng FN chờ, chưa hiện số. Hai thang riêng có ghi chú. |

| 13 | 5 | 03:28.00–03:45.00 | …nhưng bỏ sót thêm 118 tấn công | Morph: hai thanh FN từ vạch chờ tới chiều dài số liệu thật; FP giữ nguyên. |

| 14 | 5 | 03:45.00–04:00.00 | Lợi thế tổng hợp chưa đủ thuyết phục | Morph về hai hiệu số; CI chứa 0, không nói tương đương. |

| 15 | 6 | 04:00.00–04:20.00 | P21: đối chứng matched trên TRAIN | Fade: 5 chấm FIT hội tụ về một validation, không vẽ thành 5 tập TEST. |

| 16 | 6 | 04:20.00–04:38.00 | P21 chưa cho thấy Stacking-Lite tốt hơn | Morph sang điểm paired của 5 seed; giữ tên seed và ghi rõ trục rút gọn. |

| 17 | 6 | 04:38.00–04:55.00 | Ít đặc trưng chưa chắc ít chi phí hơn | Morph sang thanh cộng selector + model; phép cộng đúng đơn vị giây. |

| 18 | 7 | 04:55.00–05:15.00 | Giảm cảnh báo giả có thể tăng bỏ sót | Fade: tọa độ FPR/FNR từ cùng validation; mọi trục bắt đầu 0. |

| 19 | 7 | 05:15.00–05:35.00 | Mục tiêu vận hành quyết định cách chọn | Morph sang giả định tổn thất trên official TEST lịch sử; nguồn được đổi rõ. |

| 20 | 8 | 05:35.00–06:00.00 | Chọn mô hình bằng bằng chứng và chi phí lỗi | Fade kết luận và giới hạn; liên kết A1–A12 mở phụ lục sau bài chính. |
