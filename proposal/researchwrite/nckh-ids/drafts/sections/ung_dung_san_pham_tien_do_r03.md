# Nhu cầu, sản phẩm và tiến độ — bản thảo nội bộ r03

Phạm vi: bổ sung các mục 39–55 của form đề cương 2026; chưa merge thành đề cương đầy đủ, chưa điền DOCX hoặc kiểm định hình thức. Nội dung ánh xạ từ contracts 04/06/07; thông tin hành chính và tính áp dụng mẫu còn [CẦN XÁC NHẬN].

## Nhu cầu thực tế và khả năng áp dụng kết quả đề tài

Trong phạm vi đề tài, nhu cầu ứng dụng là hỗ trợ người nghiên cứu và người học đánh giá các mô hình phát hiện xâm nhập mạng từ dữ liệu luồng đã được trích xuất. Một chỉ số tổng hợp không mô tả đầy đủ sự đánh đổi giữa báo động giả, bỏ sót tấn công và chi phí tính toán. Các bảng kết quả đóng băng và phân tích sai số của đề tài cung cấp trường hợp cụ thể để xem xét đồng thời các yếu tố này; kết luận chỉ có giá trị trong điều kiện benchmark đã khảo sát. [S1,S2]

Kết quả dự kiến dùng làm tài liệu thực hành và nghiên cứu: xem lại nguồn dữ liệu, tái tạo bảng tổng hợp, đối chiếu cấu hình mô hình và nhận diện giới hạn của một phép so sánh. Đây là mục đích sử dụng đề xuất, chưa có bằng chứng đã được một đơn vị tiếp nhận hoặc triển khai. Phần mềm suy luận từ tệp CSV chỉ được giới thiệu sau khi có mô hình đã lưu, bộ tiền xử lý tương ứng và kiểm thử đầu vào/đầu ra đạt yêu cầu. Hiện chưa có artifact mô hình để đáp ứng điều kiện đó. [S3,S4]

Khả năng áp dụng vào một mạng vận hành cần được đánh giá bằng dữ liệu và điều kiện của mạng đó. Đề tài hiện chưa kiểm chứng thu thập gói tin, xử lý trực tuyến, tích hợp hệ thống hoặc độ khái quát trên mạng bên ngoài. Kết quả trên một benchmark và phần phân tích các vector chưa xuất hiện trong tập huấn luyện không thay thế các bước đánh giá này. [S1,S4]

## Sản phẩm giao nộp và tiêu chí chất lượng

Ánh xạ dự kiến vào dạng III của form: chương trình máy tính; phương pháp/giải pháp; sơ đồ/bảng số liệu. Chưa có căn cứ chọn sản phẩm vật liệu hoặc thiết bị. Việc đánh dấu ô phân loại chính thức cần [CẦN XÁC NHẬN]. Báo cáo kết quả giữ số lượng **03 quyển theo mẫu**, chưa khẳng định đây là quy định nộp hiện hành. [S5]

| Sản phẩm dự kiến | Tiêu chí nghiệm thu đề xuất | Trạng thái hiện tại |
|---|---|---|
| Báo cáo nghiên cứu và nguồn LaTeX | Số liệu truy được tới artifact/config; nêu giới hạn; build PDF và kiểm từng trang; references/cross-reference hợp lệ | Có bản thảo và evidence lịch sử; chưa báo cáo IDS build/render đạt |
| Mã nguồn, cấu hình, hướng dẫn tái lập | Ghi dữ liệu/môi trường/seed; kiểm thử; lệnh chạy ghi log và output riêng; phân biệt replay bảng với tái dựng huấn luyện | Replay bảng aggregate đã đạt; huấn luyện trong môi trường sạch chưa được kiểm định |
| Bảng, sơ đồ và biểu đồ | Source-data map; phép tính và nhãn đúng; xuất file rõ nét, kiểm tra bố cục; giữ cả kết quả không có lợi cho ensemble | Có saved tables và một figure đã QA; bộ hình đầy đủ còn thiếu |
| Demo suy luận và thuyết minh | Load mô hình thật cùng preprocessing/schema; thử CSV hợp lệ/không hợp lệ; mô tả input/output và giới hạn | Phụ thuộc mô hình đã lưu; chưa đạt. Không dùng viewer kết quả thay demo |
| Hồ sơ bảo vệ | Slide và PDF mở/render đạt; kịch bản phù hợp thời lượng; ít nhất 15 câu hỏi có evidence; demo runbook và kiểm tra cuối | Q&A nội bộ có 20 câu; các thành phần khác chưa đủ |

Các tiêu chí trên là đề xuất cho hồ sơ này, không phải kết quả nghiệm thu hoặc yêu cầu bổ sung đã được nhà trường ban hành. Không đặt ngưỡng Accuracy hay yêu cầu ensemble phải thắng để nghiệm thu. Đánh giá phải trình bày đồng thời hiệu quả phát hiện, tỷ lệ báo động giả, tỷ lệ bỏ sót và chi phí; công khai phần chọn feature ngoài development folds cùng các giới hạn khác. [S1,S2,S6]

Form còn ghi đĩa CD chứa nội dung báo cáo, bài báo và phần mềm nếu có. File báo cáo phải có trang bìa như bản cứng; file bài báo, nếu có, là bản cuối cùng đã sửa theo góp ý của Hội đồng khoa học Khoa; thuyết minh phần mềm không quá 02 trang A4. Giữ các nội dung đó khi điền bản sao form và xác nhận tính áp dụng; không biến điều kiện “bài báo nếu có” thành cam kết đã có bài được chấp nhận. Bộ dữ liệu gốc không mặc nhiên đưa vào gói nộp: tuân điều kiện truy cập/chia sẻ của nguồn và cung cấp hướng dẫn lấy dữ liệu. [S5,S7]

## Tiến độ thực hiện các nội dung

| Chặng theo form | Thời lượng theo form | Nội dung dự kiến ánh xạ | Kết quả/gate để kiểm |
|---|---|---|---|
| Xây dựng và duyệt đề cương | 4 tuần | Hoàn thiện tổng quan, RQ–evidence, nội dung form và thông tin hành chính | Bản đề cương được người có thẩm quyền xem xét; AI không xác nhận đã duyệt |
| Chuyên đề 1 | 11 tuần | Kiểm toán dữ liệu, protocol, chọn feature và các mô hình đơn đã thực hiện | Artifact và kiểm định truy vết được; ghi giới hạn preprocessing/selection |
| Chuyên đề 2 | 11 tuần | Phương pháp kết hợp, đánh giá, phân tích sai số và đánh đổi chi phí | Bảng/hình từ frozen results; không mở lại chọn mô hình bằng TEST |
| Báo cáo và tổng hợp nhiệm vụ | 4 tuần | Hoàn thiện DOCX/LaTeX, phần mềm, bộ bảo vệ và release QA | Render/test và kiểm G0–G6; phần chưa đạt tiếp tục ghi blocker |

Hồ sơ này đang được phục hồi từ nghiên cứu đã có kết quả, chưa có căn cứ xem là đề cương được lập hoặc phê duyệt trước thực nghiệm. Tính chấp nhận của hồ sơ phục hồi cần tác giả/GVHD xác nhận. Bảng trên ánh xạ vào thời lượng có sẵn trong mẫu, không phải thời gian thực tế đã diễn ra hoặc lịch còn lại tính từ ngày hiện tại. Ngày bắt đầu/kết thúc, lịch được duyệt và nguồn lực thực hiện: [CẦN XÁC NHẬN]. Trước khi tái dựng huấn luyện cần đánh giá tài nguyên và output isolation theo gate B; nếu chưa đạt, giữ trạng thái tái lập một phần và không xác nhận đã có demo. [S3,S5]

## Kinh phí và phần xác nhận

Bản sao form sẽ bảo toàn các khoản mẫu: nhân công chuyên đề 1 là 3.000.000 VND; chuyên đề 2 là 3.500.000 VND; hội thảo 500.000 VND; tổng 7.000.000 VND. Các ô chưa ghi tiền và ghi chú nguồn kinh phí giữ nguyên. Đây là số liệu **dự toán trong mẫu**, chưa xác nhận áp dụng, phê duyệt hay thực chi cho đề tài. Không tự bổ sung chi phí điện toán, mua thiết bị hoặc thuê dịch vụ vào bảng. [S5]

Nhân sự, MSSV/lớp, đơn vị, GVHD, người đại diện, mã đề tài, ngày và chữ ký: [CẦN XÁC NHẬN]. Không dùng tên in sẵn trong mẫu làm thông tin đã xác thực. [S5]

## Nguồn nội bộ phục vụ review — không phải danh mục trích dẫn cuối

- S1: `.research_memory/RESEARCH_CANON.md`.
- S2: `docs/CLAIM_EVIDENCE_MATRIX.md`.
- S3: `proposal/researchwrite/nckh-ids/07_remaining_work_feasibility.md`.
- S4: `docs/research/ENSEMBLE_FRAMEWORK.md`.
- S5: `templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx` và `docs/TEMPLATE_REQUIREMENTS_MATRIX.md`; đã đọc trực tiếp OOXML body39–55 trong r03.
- S6: `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md`.
- S7: `docs/research/DATA_CODE_AVAILABILITY.md`.
- Status sản phẩm: `.research_memory/TASK_BOARD.md`, `release/RELEASE_BLOCKERS.md`, `defense/qa_validation_r02.json`.
