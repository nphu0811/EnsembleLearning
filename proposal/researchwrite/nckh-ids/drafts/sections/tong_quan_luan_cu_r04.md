# Tổng quan và luận cứ khoa học — bản thảo nội bộ r04

Phạm vi: nội dung cho mục 33–38 của mẫu DOCX năm 2026 và luận cứ dẫn tới mục tiêu đã khóa. Hồ sơ được phục hồi từ nghiên cứu đã có kết quả; không gọi đây là đề cương được duyệt trước thực nghiệm. Metadata được đối chiếu độc lập với độ sâu đọc; không dùng điểm review làm chứng nhận nghiên cứu hoàn thành.

## Luận cứ chọn đề tài

Thiết kế một mô hình học kết hợp cho phát hiện xâm nhập mạng cần làm rõ hai vấn đề: cách kết hợp các mô hình và điều kiện để đánh giá kết quả. Tổng quan của Tama và Lim xác định việc chọn bộ phân loại nền và cách kết hợp là những nội dung thiết kế quan trọng [L01, abstract]. Các nghiên cứu dùng voting, stacking và lựa chọn đặc trưng đã có [L04–L06]. Vì vậy, đề tài này không nhận việc ghép các thành phần đó là thuật toán mới.

Đối với case study đã thực hiện, câu hỏi cần trả lời là các pipeline đã khóa đem lại lợi ích và đánh đổi nào trong điều kiện benchmark đang xét, cùng những giới hạn nào của phép đánh giá. Các RQ được giữ từ hồ sơ nghiên cứu gốc; kết quả đã biết được diễn giải hậu kiểm, không viết lại thành giả thuyết tiên nghiệm. Việc hoàn thiện hồ sơ tập trung vào truy vết nguồn, đối chiếu hiệu năng với sai số và chi phí, và xác định phần bằng chứng còn thiếu [N1,N2].

## Sơ lược tình hình nghiên cứu trong nước

Thông báo chính thức của Trường Đại học Lạc Hồng về lịch bảo vệ luận án của Hoàng Ngọc Thanh nêu chủ đề học máy phối hợp và tiền xử lý dữ liệu cho hệ thống phát hiện xâm nhập mạng [D01]. Nguồn này xác nhận sự hiện diện của hướng nghiên cứu tại Việt Nam. Đây là thông báo lịch bảo vệ, không phải bằng chứng về kết quả luận án hoặc việc bảo vệ đã hoàn tất.

Tóm tắt luận án của Võ Văn Hoàng tại Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội, có bìa năm 2025 và các mục tiêu về chất lượng dữ liệu, suy luận kết hợp, lấy mẫu; phần mục tiêu đề cập soft voting và stacking [D02, bìa và mục Mục tiêu nghiên cứu]. Trong phạm vi đã đọc, nguồn này hỗ trợ bối cảnh phương pháp. Chưa đủ cơ sở so sánh trực tiếp kết quả, protocol hoặc khả năng triển khai của luận án với NCKH này. Hai nguồn trong nước trên có loại hình khác nhau và chưa tạo thành khảo sát đầy đủ; không dùng chúng để nhận đề tài là nghiên cứu đầu tiên trong nước.

## Sơ lược tình hình nghiên cứu ngoài nước

Các hướng liên quan có thể chia theo chức năng trong pipeline. Doreswamy và cộng sự nghiên cứu kết hợp các tập đặc trưng; cần phân biệt hướng ensemble feature selection này với ensemble classifier kết hợp các dự đoán [L04, abstract]. Khan và cộng sự mô tả AutoML với soft voting [L05, abstract/preview]. Thockchom và cộng sự trình bày stacking dùng GNB, DT, LR và bộ học ở tầng kết hợp (meta learner) SGD, với dự đoán từ cross-validation làm đầu vào meta; bài mô tả phép chia ngẫu nhiên 80/20 [L06, Proposed model]. Cấu hình này khác thiết kế và official split của NCKH, nên số liệu trong bài không được đưa vào bảng matched baselines của đề tài. Những đoạn đã đọc cũng chưa đủ để chứng nhận mọi bước fitted preprocessing của bài đều nested đúng.

Lựa chọn đặc trưng và tiền xử lý cần được xem trong quan hệ với mô hình và dữ liệu. Các nguồn liên quan gồm khảo sát filter-based selection của Zouhri và cộng sự [L08, abstract], nghiên cứu FS/normalization của Umar và cộng sự [L11, abstract], và kết hợp correlation/embedded selection của Nassreddine và cộng sự [L12, selected publisher-indexed Methods]. Chúng giúp xác định các thành phần đã có trong prior work; không chứng minh hiệu quả nhân quả của riêng feature selection trong so sánh RF-17/RF-42 của NCKH, vốn còn khác cấu hình mô hình [N1]. Với mất cân bằng, DUEN nghiên cứu dynamic undersampling trong ensemble [L07, abstract/preview]; đề tài chưa có matched resampling comparison nên chưa thể rút ra kết luận về hiệu quả của các can thiệp đó.

Tính hợp lệ của dữ liệu và phạm vi đánh giá là một trục riêng. Engelen và cộng sự kiểm tra các khâu tạo dữ liệu và pipeline của CICIDS2017 [L02, selected audit passages]. Không chuyển các phát hiện cụ thể của CIC sang UNSW-NB15. Cantone và cộng sự phân biệt within-dataset với cross-dataset trong thiết kế nghiên cứu [L09, indexed Introduction, tr. 144490]. Trong khi đó, official/novel-vector views của NCKH đều thuộc một benchmark; chúng không thay đánh giá temporal hoặc trên mạng độc lập [N1].

## Khoảng thiếu bằng chứng và vị trí của đề tài

Ma trận gap hiện hành ghi riêng điều đã biết, giới hạn còn thiếu và hệ quả đối với từng RQ [N3]. Với RQ1–RQ3 đã khóa, phép đối chiếu cần làm rõ lợi ích quan sát của ensemble so với mô hình đơn, khác biệt hiệu năng–chi phí giữa các pipeline và mối liên hệ mô tả giữa lỗi của mô hình nền với kết quả kết hợp. Các artifact hiện có không chứng minh hiệu quả nhân quả của riêng feature selection hoặc độ ổn định qua tái huấn luyện độc lập [N1].

Trong phạm vi hiện có, giá trị đề xuất là một case study so sánh các pipeline đóng băng, có truy vết số liệu và công khai đánh đổi giữa báo động giả, bỏ sót và chi phí. Chưa có căn cứ nhận novelty trên toàn lĩnh vực hoặc ưu thế tổng thể của stacking. Phần chọn đặc trưng ngoài development folds, meta tuning chưa fully nested, giới hạn của RQ4/RQ5 và thiếu tái lập huấn luyện vẫn phải được nêu rõ [N1,N2].

Tổng quan này phục vụ lập luận có giới hạn của hồ sơ phục hồi; chưa phải systematic review hoặc khảo sát literature cập nhật đầy đủ đến 2026. Việc kiểm chứng 11 metadata records không đồng nghĩa đã đọc toàn bộ 11 bài. L03 còn conflict trang, được giữ trong ledger để xử lý tiếp và không cần dùng cho luận điểm của phần thảo này.

## Nguồn và reading boundary

Các nhãnL là ID nội bộ ổn định, không phải số thứ tự bibliography cuối. Full title/authors/venue/DOI ở `literature/resume_r04_2026_10_16/legacy_verification_ledger.csv`; subset metadata-verified ở `literature/refs_verified_subset.bib`. Phần này dùngL01,L02,L04,L05,L06,L07,L08,L09,L11,L12; không cầnL03/L10. Độ sâu đọc ở `literature/resume_r04_2026_10_16/SCOPED_READING_NOTES.md` và notes r02/r03, không suy thêm từ title.

- D01: [Thông báo Lạc Hồng về lịch bảo vệ luận án Hoàng Ngọc Thanh](https://lhu.edu.vn/783/41967/Lich-bao-ve-luan-an-tien-si-cap-Truong-nganh-Khoa-hoc-may-tinh-NCS-Hoang-Ngoc-Thanh-thang-12-nam-2022.html), lịch31/12/2022; chưa luận án đầy đủ.
- D02: [Võ Văn Hoàng, tóm tắt luận án, UET,2025](https://uet-test.uet.edu.vn/wp-content/uploads/2025/11/Tom-tat-LATS-cua-NCS-Vo-Van-Hoang_QH-20-HTTT-tieng-Viet-1.pdf), bìa/PDF1 và mục tiêu/PDF3; chưa toàn bộ 27 trang hoặc luận án gốc.
- N1: `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md`.
- N2: `docs/CLAIM_EVIDENCE_MATRIX.md` và `.research_memory/RESEARCH_CANON.md`.
- N3: `literature/gap_matrix.md`.
