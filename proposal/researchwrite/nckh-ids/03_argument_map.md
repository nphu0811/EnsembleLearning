# Bản đồ lập luận

Bổ sung evidence r04: R04C01–05 hỗ trợ prior stacking, audit minh bạch, phân biệt cross-dataset và bối cảnh trong nước. Không đổi scientific tension hoặc central RQ; kết luận vẫn là bounded local benchmark audit/trade-off. Không chuyển findings NCKH hậu kiểm thành hypothesis tiên nghiệm. Gap map hiện hành `literature/gap_matrix.md` ghi riêng known/unknown/consequence vàtrạng thái RQ.

## Scientific tension

L05/L06/L07 đã có voting/stacking, feature reduction và sampling trong IDS, trong giới hạn nguồn đã đọc. Vì vậy sự kết hợp thành phần không tự tạo novelty. Câu hỏi còn cần kiểm tra đối với chính các pipeline đã khóa của NCKH là lợi ích quan sát được đáng tin cậy tới đâu và đi cùng error/cost trade-off nào. Đây là bounded benchmark question, không khẳng định cả lĩnh vực chưa giải quyết nó.

Kết quả đã biết như Macro-F1 CI chứa0 và FPR/FNR đánh đổi là evidence hậu kiểm để diễn giải, không phải motivation/giả thuyết được ghi nhận trước thí nghiệm. Toàn bộ văn bản phân biệt nghiên cứu đã thực hiện với công việc documentation/QA/reconstruction còn lại. So sánh prior work trong07_remaining_work_feasibility.md.

## Câu hỏi trung tâm

Theo RQ1 đã khóa, ensemble có đem lại lợi ích đáng tin cậy so với learner đơn trong protocol đang xét không? Không sửa câu hỏi thành “chứng minh stacking tốt nhất”.

RQ1–RQ5 nguyên văn, mục tiêu thao tác, comparator, output, limits và status được ánh xạ ở06_rq_method_output_gates.md. RQ4/RQ5 giữ partial/unanswered; không thu hẹp tên RQ gốc để giả hoàn thành. Formal drafting phải bám các status này.

## Luận điểm và bằng chứng

1. Đánh giá cần kết hợp hiệu quả, false alarms/misses và chi phí. C03–C05; giới hạn benchmark/offline.
2. Mô hình kết hợp cần kiểm tra complementarity thực tế. C06; không suy ra gain chỉ từ heterogeneous architecture.
3. Tính tin cậy cần provenance và reproducibility. C01, C02, C09, C11; còn thiếu original env và ML replay.

## Phản luận

Selection optimism có thể làm development estimates đẹp hơn thực tế. Official/novel split không loại bỏ mọi dependence. RF17 khác hyperparameter nên không cô lập effect của feature selection. Bootstrap row-level không đại diện mọi mạng thực. Đưa các giới hạn vào phương pháp/tiêu chí, không xóa chúng để đề cương có vẻ mạnh hơn.

## Kết luận hướng tới

Đề xuất/ghi nhận một nghiên cứu so sánh có kiểm toán và báo cáo trade-off; chưa khẳng định thuật toán mới, model vượt trội hoặc khả năng triển khai thật. Không biến kết quả đã biết thành giả thuyết tiên nghiệm.
