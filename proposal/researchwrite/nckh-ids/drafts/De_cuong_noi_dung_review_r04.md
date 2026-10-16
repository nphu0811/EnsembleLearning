# Đề cương NCKH 2026 — gói nội dung phục vụ review r04

Đây là bản nội dung Markdown được ghép theo thứ tự trường của DOCX gốc; chưa điền DOCX, chưa render và chưa đủ điều kiện nộp. Hồ sơ đang phục hồi từ nghiên cứu đã có kết quả; tác giả/GVHD cần xác nhận tính chấp nhận. Không có phê duyệt hồi tố hoặc chữ ký do AI xác nhận. Các nhãn M/T/P giúp tách resolver nguồn của từng phần soạn, chưa là bibliography numbering cuối.

## Thông tin đầu biểu mẫu

Mẫu 2: Đề cương đề tài NCKH của sinh viên. Đơn vị/địa danh trong header mẫu: [CẦN XÁC NHẬN tính áp dụng]; ngày/tháng/năm ký: [CẦN XÁC NHẬN]. Không lấy tên hoặc vai trò in sẵn làm danh tính đã xác thực.

Tên đề tài: NGHIÊN CỨU ENSEMBLE LEARNING CHO BÀI TOÁN PHÁT HIỆN XÂM NHẬP MẠNG.

Mã số đề tài: [CẦN XÁC NHẬN]. Thuộc lĩnh vực KHCN: [CẦN XÁC NHẬN mã/tên lĩnh vực hành chính].

## Mục tiêu, nội dung và kết quả

### Mục tiêu

Đánh giá hiệu quả và chi phí của các pipeline học kết hợp trong bài toán phân biệt lưu lượng bình thường với tấn công trên UNSW-NB15, đồng thời làm rõ giới hạn của quy trình và các đánh đổi giữa báo động giả, bỏ sót và chi phí tính toán. Việc đánh giá không đặt điều kiện mô hình kết hợp phải vượt mô hình đơn.

Các mục tiêu cụ thể gồm: đối chiếu kết quả của các pipeline đã khóa cùng khoảng bất định; mô tả khác biệt quan sát được về hiệu năng và chi phí giữa các pipeline có tập đặc trưng và cấu hình khác nhau; khảo sát tính bổ sung của lỗi từ dự đoán ngoài fold huấn luyện (out-of-fold, OOF); xác định phần nào của các câu hỏi về độ bền đánh giá và mất cân bằng đã có bằng chứng, phần nào chưa được trả lời. Toàn bộ RQ gốc và trạng thái tương ứng được giữ trong tài liệu 06_rq_method_output_gates.md [M:N1].

### Nội dung

Tổng hợp các phương pháp ensemble và lựa chọn đặc trưng liên quan, chú ý cách chia dữ liệu, đầu vào meta learner và phạm vi so sánh. Voting, stacking và các cơ chế xử lý mất cân bằng đã xuất hiện trong prior work; nghiên cứu không nhận sự kết hợp các thành phần này là thuật toán mới [M:L05–L07]. Phần tổng quan trong nước sẽ dùng đúng loại nguồn và độ sâu đã đọc, không suy kết quả thực nghiệm từ thông báo bảo vệ luận án [M:D01–D02].

Đối với chuỗi thực nghiệm đã thực hiện, nội dung được trình bày gồm kiểm toán dữ liệu và feature-vector overlap, feature tracks, các mô hình đơn và ensemble, quy trình lựa chọn cấu hình trên TRAIN, đánh giá đóng băng, phân tích thống kê, ablation hồi cứu và lỗi theo nhóm tấn công. Khi diễn giải, phân biệt kết quả binary detector với dự đoán multiclass; giữ các kết quả kém hoặc không kết luận được [M:N2–N3].

Phần công việc còn lại là hoàn thiện nguồn trích dẫn, chuẩn hóa bảng/hình và chú thích, tài liệu tái lập, đánh giá khả năng tái dựng mô hình trong môi trường cô lập, chuẩn bị demo suy luận khi có artifact hợp lệ, hoàn thiện hồ sơ theo mẫu và bộ tài liệu bảo vệ. Đây là công việc cần kiểm định tiếp, không được liệt kê như sản phẩm đã hoàn thành [M:N4].

Phương pháp và giới hạn diễn giải (nội dung bổ sung trong vùng Nội dung, không phải nhãn mới của form gốc):

Nghiên cứu kế thừa official TRAIN gồm 175.341 mẫu và TEST gồm 82.332 mẫu; Attack là lớp dương (1), Normal là lớp 0. Ba pipeline final đã khóa là RF-42, Stacking-42 và RF-17, với ngưỡng quyết định 0,5. Các predictors loại trừ id, label và attack_cat. Preprocessing được triển khai trong pipeline; stacking dùng hồi quy logistic (LR), cây quyết định (DT) và Random Forest (RF) làm base learners, LR làm meta learner với internal cross-validation (CV) [M:N2]. Mô tả này dựa trên source và metadata đã đối chiếu; kiểm tra tĩnh không thay việc tái lập huấn luyện và chưa xác nhận môi trường huấn luyện gốc.

Đánh giá dựa trên các bảng đã lưu gồm Macro-F1, MCC, per-class precision/recall/F1, FPR/FNR, ROC-AUC, PR-AUC và thời gian huấn luyện/suy luận được ghi trong bảng chi phí, với điều kiện đo và giới hạn môi trường được công khai. Khoảng tin cậy paired bootstrap thể hiện bất định có điều kiện trên các dòng benchmark, không thay repeated training; McNemar đánh giá paired correctness, không phải kiểm định trực tiếp Macro-F1. So sánh RF-17/RF-42 được diễn giải như trade-off giữa hai pipeline vì chúng còn khác hyperparameters [M:N1–N3].

Giới hạn đã xác định phải xuất hiện trong báo cáo: feature selection sử dụng toàn bộ TRAIN trước development CV, meta tuning chưa fully nested, official split có overlap và novel-vector view vẫn thuộc cùng benchmark. Vì vậy không gọi CV là ước lượng không thiên lệch sau selection, không khẳng định external/time-independent validation và không dùng TEST để chỉnh features, mô hình hoặc threshold. RQ4 giữ partial; hiệu quả controlled resampling trong RQ5 chưa có đủ bằng chứng [M:N1–N3].

### Kết quả

Đã có source, frozen metrics và các bảng phân tích. Kết quả hiện có không chứng minh Stacking-42 vượt RF-42 tổng thể; giảm FP đi cùng tăng FN. Hồ sơ sẽ trình bày cả hai mặt cùng uncertainty và giới hạn, thay vì chỉ chọn chỉ số có lợi [M:N3].

Sản phẩm cần hoàn thiện gồm đề cương đúng mẫu, báo cáo LaTeX và PDF, source/config/tài liệu tái lập, bảng/hình có nguồn, demo được kiểm thử, slide, kịch bản và hỏi đáp hội đồng. Chất lượng được xác nhận bằng artifact, kiểm tra số liệu, tests và render; không đặt ngưỡng Accuracy tùy ý. Replay bảng aggregate, tái dựng ML và inference demo có ba gate riêng; phần chưa đạt tiếp tục ghi thiếu, không thay bằng một sản phẩm khác có tên tương tự [M:N4].

## Đơn vị, chủ trì, người tham gia và hướng dẫn

- Đơn vị chủ trì: [CẦN XÁC NHẬN tính áp dụng tên đơn vị trong mẫu].
- Đơn vị phối hợp (nếu có): [CẦN XÁC NHẬN có hay không và thông tin].
- Chủ trì: họ tên [CẦN XÁC NHẬN]; MSSV [CẦN XÁC NHẬN]; lớp [CẦN XÁC NHẬN]; điện thoại [CẦN XÁC NHẬN].
- Người tham gia: số lượng, họ tên, MSSV và lớp từng người [CẦN XÁC NHẬN]. Không tự thêm thành viên hoặc xác nhận không có.
- Người hướng dẫn: họ tên, học hàm/học vị [CẦN XÁC NHẬN].

## Sơ lược tình hình nghiên cứu, điều tra trong nước, ngoài nước

Thiết kế một mô hình học kết hợp cho phát hiện xâm nhập mạng cần làm rõ hai vấn đề: cách kết hợp các mô hình và điều kiện để đánh giá kết quả. Tổng quan của Tama và Lim xác định việc chọn bộ phân loại nền và cách kết hợp là những nội dung thiết kế quan trọng [T:L01, abstract]. Các nghiên cứu dùng voting, stacking và lựa chọn đặc trưng đã có [T:L04–L06]. Vì vậy, đề tài này không nhận việc ghép các thành phần đó là thuật toán mới.

Đối với case study đã thực hiện, câu hỏi cần trả lời là các pipeline đã khóa đem lại lợi ích và đánh đổi nào trong điều kiện benchmark đang xét, cùng những giới hạn nào của phép đánh giá. Các RQ được giữ từ hồ sơ nghiên cứu gốc; kết quả đã biết được diễn giải hậu kiểm, không viết lại thành giả thuyết tiên nghiệm. Việc hoàn thiện hồ sơ tập trung vào truy vết nguồn, đối chiếu hiệu năng với sai số và chi phí, và xác định phần bằng chứng còn thiếu [T:N1,N2].

### Trong nước

Thông báo chính thức của Trường Đại học Lạc Hồng về lịch bảo vệ luận án của Hoàng Ngọc Thanh nêu chủ đề học máy phối hợp và tiền xử lý dữ liệu cho hệ thống phát hiện xâm nhập mạng [T:D01]. Nguồn này xác nhận sự hiện diện của hướng nghiên cứu tại Việt Nam. Đây là thông báo lịch bảo vệ, không phải bằng chứng về kết quả luận án hoặc việc bảo vệ đã hoàn tất.

Tóm tắt luận án của Võ Văn Hoàng tại Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội, có bìa năm 2025 và các mục tiêu về chất lượng dữ liệu, suy luận kết hợp, lấy mẫu; phần mục tiêu đề cập soft voting và stacking [T:D02, bìa và mục Mục tiêu nghiên cứu]. Trong phạm vi đã đọc, nguồn này hỗ trợ bối cảnh phương pháp. Chưa đủ cơ sở so sánh trực tiếp kết quả, protocol hoặc khả năng triển khai của luận án với NCKH này. Hai nguồn trong nước trên có loại hình khác nhau và chưa tạo thành khảo sát đầy đủ; không dùng chúng để nhận đề tài là nghiên cứu đầu tiên trong nước.

### Ngoài nước

Các hướng liên quan có thể chia theo chức năng trong pipeline. Doreswamy và cộng sự nghiên cứu kết hợp các tập đặc trưng; cần phân biệt hướng ensemble feature selection này với ensemble classifier kết hợp các dự đoán [T:L04, abstract]. Khan và cộng sự mô tả AutoML với soft voting [T:L05, abstract/preview]. Thockchom và cộng sự trình bày stacking dùng GNB, DT, LR và bộ học ở tầng kết hợp (meta learner) SGD, với dự đoán từ cross-validation làm đầu vào meta; bài mô tả phép chia ngẫu nhiên 80/20 [T:L06, Proposed model]. Cấu hình này khác thiết kế và official split của NCKH, nên số liệu trong bài không được đưa vào bảng matched baselines của đề tài. Những đoạn đã đọc cũng chưa đủ để chứng nhận mọi bước fitted preprocessing của bài đều nested đúng.

Lựa chọn đặc trưng và tiền xử lý cần được xem trong quan hệ với mô hình và dữ liệu. Các nguồn liên quan gồm khảo sát filter-based selection của Zouhri và cộng sự [T:L08, abstract], nghiên cứu FS/normalization của Umar và cộng sự [T:L11, abstract], và kết hợp correlation/embedded selection của Nassreddine và cộng sự [T:L12, selected publisher-indexed Methods]. Chúng giúp xác định các thành phần đã có trong prior work; không chứng minh hiệu quả nhân quả của riêng feature selection trong so sánh RF-17/RF-42 của NCKH, vốn còn khác cấu hình mô hình [T:N1]. Với mất cân bằng, DUEN nghiên cứu dynamic undersampling trong ensemble [T:L07, abstract/preview]; đề tài chưa có matched resampling comparison nên chưa thể rút ra kết luận về hiệu quả của các can thiệp đó.

Tính hợp lệ của dữ liệu và phạm vi đánh giá là một trục riêng. Engelen và cộng sự kiểm tra các khâu tạo dữ liệu và pipeline của CICIDS2017 [T:L02, selected audit passages]. Không chuyển các phát hiện cụ thể của CIC sang UNSW-NB15. Cantone và cộng sự phân biệt within-dataset với cross-dataset trong thiết kế nghiên cứu [T:L09, indexed Introduction, tr. 144490]. Trong khi đó, official/novel-vector views của NCKH đều thuộc một benchmark; chúng không thay đánh giá temporal hoặc trên mạng độc lập [T:N1].

Tổng hợp luận cứ và giới hạn (đoạn kết trong vùng tổng quan):

Ma trận gap hiện hành ghi riêng điều đã biết, giới hạn còn thiếu và hệ quả đối với từng RQ [T:N3]. Với RQ1–RQ3 đã khóa, phép đối chiếu cần làm rõ lợi ích quan sát của ensemble so với mô hình đơn, khác biệt hiệu năng–chi phí giữa các pipeline và mối liên hệ mô tả giữa lỗi của mô hình nền với kết quả kết hợp. Các artifact hiện có không chứng minh hiệu quả nhân quả của riêng feature selection hoặc độ ổn định qua tái huấn luyện độc lập [T:N1].

Trong phạm vi hiện có, giá trị đề xuất là một case study so sánh các pipeline đóng băng, có truy vết số liệu và công khai đánh đổi giữa báo động giả, bỏ sót và chi phí. Chưa có căn cứ nhận novelty trên toàn lĩnh vực hoặc ưu thế tổng thể của stacking. Phần chọn đặc trưng ngoài development folds, meta tuning chưa fully nested, giới hạn của RQ4/RQ5 và thiếu tái lập huấn luyện vẫn phải được nêu rõ [T:N1,N2].

Tổng quan này phục vụ lập luận có giới hạn của hồ sơ phục hồi; chưa phải systematic review hoặc khảo sát literature cập nhật đầy đủ đến 2026. Việc kiểm chứng 11 metadata records không đồng nghĩa đã đọc toàn bộ 11 bài. L03 còn conflict trang, được giữ trong ledger để xử lý tiếp và không cần dùng cho luận điểm của phần thảo này.

## Nhu cầu thực tế và khả năng áp dụng kết quả đề tài

Trong phạm vi đề tài, nhu cầu ứng dụng là hỗ trợ người nghiên cứu và người học đánh giá các mô hình phát hiện xâm nhập mạng từ dữ liệu luồng đã được trích xuất. Một chỉ số tổng hợp không mô tả đầy đủ sự đánh đổi giữa báo động giả, bỏ sót tấn công và chi phí tính toán. Các bảng kết quả đóng băng và phân tích sai số của đề tài cung cấp trường hợp cụ thể để xem xét đồng thời các yếu tố này; kết luận chỉ có giá trị trong điều kiện benchmark đã khảo sát. [P:S1,S2]

Kết quả dự kiến dùng làm tài liệu thực hành và nghiên cứu: xem lại nguồn dữ liệu, tái tạo bảng tổng hợp, đối chiếu cấu hình mô hình và nhận diện giới hạn của một phép so sánh. Đây là mục đích sử dụng đề xuất, chưa có bằng chứng đã được một đơn vị tiếp nhận hoặc triển khai. Phần mềm suy luận từ tệp CSV chỉ được giới thiệu sau khi có mô hình đã lưu, bộ tiền xử lý tương ứng và kiểm thử đầu vào/đầu ra đạt yêu cầu. Hiện chưa có artifact mô hình để đáp ứng điều kiện đó. [P:S3,S4]

Khả năng áp dụng vào một mạng vận hành cần được đánh giá bằng dữ liệu và điều kiện của mạng đó. Đề tài hiện chưa kiểm chứng thu thập gói tin, xử lý trực tuyến, tích hợp hệ thống hoặc độ khái quát trên mạng bên ngoài. Kết quả trên một benchmark và phần phân tích các vector chưa xuất hiện trong tập huấn luyện không thay thế các bước đánh giá này. [P:S1,S4]

## Sản phẩm giao nộp; kết quả, sản phẩm

Ánh xạ dự kiến vào dạng III của form: chương trình máy tính; phương pháp/giải pháp; sơ đồ/bảng số liệu. Chưa có căn cứ chọn sản phẩm vật liệu hoặc thiết bị. Việc đánh dấu ô phân loại chính thức cần [CẦN XÁC NHẬN]. Báo cáo kết quả giữ số lượng **03 quyển theo mẫu**, chưa khẳng định đây là quy định nộp hiện hành. [P:S5]

| Sản phẩm dự kiến | Tiêu chí nghiệm thu đề xuất | Trạng thái hiện tại |
|---|---|---|
| Báo cáo nghiên cứu và nguồn LaTeX | Số liệu truy được tới artifact/config; nêu giới hạn; build PDF và kiểm từng trang; references/cross-reference hợp lệ | Có bản thảo và evidence lịch sử; chưa báo cáo IDS build/render đạt |
| Mã nguồn, cấu hình, hướng dẫn tái lập | Ghi dữ liệu/môi trường/seed; kiểm thử; lệnh chạy ghi log và output riêng; phân biệt replay bảng với tái dựng huấn luyện | Replay bảng aggregate đã đạt; huấn luyện trong môi trường sạch chưa được kiểm định |
| Bảng, sơ đồ và biểu đồ | Source-data map; phép tính và nhãn đúng; xuất file rõ nét, kiểm tra bố cục; giữ cả kết quả không có lợi cho ensemble | Có saved tables và một figure đã QA; bộ hình đầy đủ còn thiếu |
| Demo suy luận và thuyết minh | Load mô hình thật cùng preprocessing/schema; thử CSV hợp lệ/không hợp lệ; mô tả input/output và giới hạn | Phụ thuộc mô hình đã lưu; chưa đạt. Không dùng viewer kết quả thay demo |
| Hồ sơ bảo vệ | Slide và PDF mở/render đạt; kịch bản phù hợp thời lượng; ít nhất 15 câu hỏi có evidence; demo runbook và kiểm tra cuối | Q&A nội bộ có 20 câu; các thành phần khác chưa đủ |

Các tiêu chí trên là đề xuất cho hồ sơ này, không phải kết quả nghiệm thu hoặc yêu cầu bổ sung đã được nhà trường ban hành. Không đặt ngưỡng Accuracy hay yêu cầu ensemble phải thắng để nghiệm thu. Đánh giá phải trình bày đồng thời hiệu quả phát hiện, tỷ lệ báo động giả, tỷ lệ bỏ sót và chi phí; công khai phần chọn feature ngoài development folds cùng các giới hạn khác. [P:S1,S2,S6]

Form còn ghi đĩa CD chứa nội dung báo cáo, bài báo và phần mềm nếu có. File báo cáo phải có trang bìa như bản cứng; file bài báo, nếu có, là bản cuối cùng đã sửa theo góp ý của Hội đồng khoa học Khoa; thuyết minh phần mềm không quá 02 trang A4. Giữ các nội dung đó khi điền bản sao form và xác nhận tính áp dụng; không biến điều kiện “bài báo nếu có” thành cam kết đã có bài được chấp nhận. Bộ dữ liệu gốc không mặc nhiên đưa vào gói nộp: tuân điều kiện truy cập/chia sẻ của nguồn và cung cấp hướng dẫn lấy dữ liệu. [P:S5,S7]

Vùng yêu cầu kỹ thuật dạng I: chưa đề xuất sản phẩm dạng I; bảo toàn bảng gốc và [CẦN XÁC NHẬN cách ghi không áp dụng]. Không xóa nhãn hoặc ghi sản phẩm thiết bị/vật liệu không có căn cứ. Các tiêu chí dạng II/III ở bảng trên là đề xuất nội dung, chưa là kết quả nghiệm thu.

## Tiến độ thực hiện các nội dung

| Chặng theo form | Thời lượng theo form | Nội dung dự kiến ánh xạ | Kết quả/gate để kiểm |
|---|---|---|---|
| Xây dựng và duyệt đề cương | 4 tuần | Hoàn thiện tổng quan, RQ–evidence, nội dung form và thông tin hành chính | Bản đề cương được người có thẩm quyền xem xét; AI không xác nhận đã duyệt |
| Chuyên đề 1 | 11 tuần | Kiểm toán dữ liệu, protocol, chọn feature và các mô hình đơn đã thực hiện | Artifact và kiểm định truy vết được; ghi giới hạn preprocessing/selection |
| Chuyên đề 2 | 11 tuần | Phương pháp kết hợp, đánh giá, phân tích sai số và đánh đổi chi phí | Bảng/hình từ frozen results; không mở lại chọn mô hình bằng TEST |
| Báo cáo và tổng hợp nhiệm vụ | 4 tuần | Hoàn thiện DOCX/LaTeX, phần mềm, bộ bảo vệ và release QA | Render/test và kiểm G0–G6; phần chưa đạt tiếp tục ghi blocker |

Hồ sơ này đang được phục hồi từ nghiên cứu đã có kết quả, chưa có căn cứ xem là đề cương được lập hoặc phê duyệt trước thực nghiệm. Tính chấp nhận của hồ sơ phục hồi cần tác giả/GVHD xác nhận. Bảng trên ánh xạ vào thời lượng có sẵn trong mẫu, không phải thời gian thực tế đã diễn ra hoặc lịch còn lại tính từ ngày hiện tại. Ngày bắt đầu/kết thúc, lịch được duyệt và nguồn lực thực hiện: [CẦN XÁC NHẬN]. Trước khi tái dựng huấn luyện cần đánh giá tài nguyên và output isolation theo gate B; nếu chưa đạt, giữ trạng thái tái lập một phần và không xác nhận đã có demo. [P:S3,S5]

## Các khoản chi phí

Bản sao form sẽ bảo toàn các khoản mẫu: nhân công chuyên đề 1 là 3.000.000 VND; chuyên đề 2 là 3.500.000 VND; hội thảo 500.000 VND; tổng 7.000.000 VND. Các ô chưa ghi tiền và ghi chú nguồn kinh phí giữ nguyên. Đây là số liệu **dự toán trong mẫu**, chưa xác nhận áp dụng, phê duyệt hay thực chi cho đề tài. Không tự bổ sung chi phí điện toán, mua thiết bị hoặc thuê dịch vụ vào bảng. [P:S5]

Nhân sự, MSSV/lớp, đơn vị, GVHD, người đại diện, mã đề tài, ngày và chữ ký: [CẦN XÁC NHẬN]. Không dùng tên in sẵn trong mẫu làm thông tin đã xác thực. [P:S5]

Khi điền DOCX, giữ các dòng xét duyệt đề cương, nhân công chuyên đề 1/chuyên đề 2, viết báo cáo, hội thảo, nghiệm thu; giữ ô tiền đang trống và ghi chú nguồn kinh phí trong mẫu. Chưa có căn cứ điền thêm số tiền hoặc xác nhận đã chi.

## Vùng chữ ký của mẫu

Chủ trì đề tài (ký và ghi rõ họ tên): [CẦN XÁC NHẬN]. Đơn vị chủ trì/người đại diện/chức danh: [CẦN XÁC NHẬN]. Giáo viên hướng dẫn (ký và ghi rõ họ tên): [CẦN XÁC NHẬN]. Chữ ký do người có thẩm quyền thực hiện; bản này không có chữ ký hoặc xác nhận hành chính.

## Resolver nguồn nội bộ cho review

Nguồn M (mục tiêu/nội dung/phương pháp):

[M:N1] `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md` và frozen research design được dẫn trong đó.

[M:N2] `docs/research/ENSEMBLE_FRAMEWORK.md`; `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`; `results/reproducibility/resume_2026_10_16/protocol/P15_04_PROTOCOL_REPORT.md`.

[M:N3] `docs/CLAIM_EVIDENCE_MATRIX.md`, C03–C11 và các bảng gốc được liên kết tại đó.

[M:N4] `proposal/researchwrite/nckh-ids/07_remaining_work_feasibility.md`; `release/RELEASE_BLOCKERS.md`.

[M:L05] Khan và cộng sự, 2023, DOI10.1016/j.jnca.2022.103560. [M:L06] Thockchom và cộng sự, 2023, DOI10.1007/s40747-023-01013-7. [M:L07] Ren và cộng sự, 2023, DOI10.1016/j.eswa.2023.120420. Metadata và reading boundary theo `literature/resume_r02_2026_10_16/legacy_verification_ledger.csv` và `literature/resume_r02_2026_10_16/READING_NOTES.md`; không hàm ý full-paper review.

[M:D01–D02] Nguồn trường đại học và giới hạn sử dụng trong `literature/resume_r02_2026_10_16/DOMESTIC_SOURCES.md`. Các nhãn nguồn là nhãn soạn thảo nội bộ, chưa phải số thứ tự bibliography cuối.

Nguồn T (tổng quan):

Quy ước: [T:Lxx] → ledger row id=Lxx → metadata/reading notes; [T:Dxx] và [T:Nx] → các mục tương ứng dưới đây. [P:Sx] → các mục Sx của nguồn P.

Các nhãn L là ID nội bộ ổn định, không phải số thứ tự bibliography cuối. Full title/authors/venue/DOI ở `literature/resume_r04_2026_10_16/legacy_verification_ledger.csv`; subset metadata-verified ở `literature/refs_verified_subset.bib`. Phần này dùng L01,L02,L04,L05,L06,L07,L08,L09,L11,L12; không cầnL03/L10. Độ sâu đọc ở `literature/resume_r04_2026_10_16/SCOPED_READING_NOTES.md` và notes r02/r03, không suy thêm từ title.

- [T:D01]: [Thông báo Lạc Hồng về lịch bảo vệ luận án Hoàng Ngọc Thanh](https://lhu.edu.vn/783/41967/Lich-bao-ve-luan-an-tien-si-cap-Truong-nganh-Khoa-hoc-may-tinh-NCS-Hoang-Ngoc-Thanh-thang-12-nam-2022.html), lịch 31/12/2022; chưa luận án đầy đủ.
- [T:D02]: [Võ Văn Hoàng, tóm tắt luận án, UET, 2025](https://uet-test.uet.edu.vn/wp-content/uploads/2025/11/Tom-tat-LATS-cua-NCS-Vo-Van-Hoang_QH-20-HTTT-tieng-Viet-1.pdf), bìa/PDF 1 và mục tiêu/PDF 3; chưa toàn bộ 27 trang hoặc luận án gốc.
- [T:N1]: `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md`.
- [T:N2]: `docs/CLAIM_EVIDENCE_MATRIX.md` và `.research_memory/RESEARCH_CANON.md`.
- [T:N3]: `literature/gap_matrix.md`.

Nguồn P (sản phẩm/tiến độ):

- [P:S1]: `.research_memory/RESEARCH_CANON.md`.
- [P:S2]: `docs/CLAIM_EVIDENCE_MATRIX.md`.
- [P:S3]: `proposal/researchwrite/nckh-ids/07_remaining_work_feasibility.md`.
- [P:S4]: `docs/research/ENSEMBLE_FRAMEWORK.md`.
- [P:S5]: `templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx` và `docs/TEMPLATE_REQUIREMENTS_MATRIX.md`; đã đọc trực tiếp OOXML body39–55 trong r03.
- [P:S6]: `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md`.
- [P:S7]: `docs/research/DATA_CODE_AVAILABILITY.md`.
- Status sản phẩm: `.research_memory/TASK_BOARD.md`, `release/RELEASE_BLOCKERS.md`, `defense/qa_validation_r02.json`.

### Metadata các bài được viện dẫn

- L01: Tama, Bayu Adhi and Lim, Sunghoon. Ensemble learning for intrusion detection systems: A systematic mapping study and cross-benchmark evaluation. Computer Science Review, 2021; 39: article 100357. DOI: 10.1016/j.cosrev.2020.100357.
- L02: Engelen, Gints and Rimmer, Vera and Joosen, Wouter. Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study. 2021 IEEE Security and Privacy Workshops (SPW), 2021; pages 7-12. DOI: 10.1109/spw53761.2021.00009.
- L04: Doreswamy and Hooshmand, Mohammad Kazim and Gad, Ibrahim. Feature selection approach using ensemble learning for network anomaly detection. CAAI Transactions on Intelligence Technology, 2020; 5(4): 283-293. DOI: 10.1049/trit.2020.0073.
- L05: Khan, Murad Ali and Iqbal, Naeem and Imran and Jamil, Harun and Kim, Do-Hyeun. An optimized ensemble prediction model using AutoML based on soft voting classifier for network intrusion detection. Journal of Network and Computer Applications, 2023; 212: article 103560. DOI: 10.1016/j.jnca.2022.103560.
- L06: Thockchom, Ngamba and Singh, Moirangthem Marjit and Nandi, Utpal. A novel ensemble learning-based model for network intrusion detection. Complex & Intelligent Systems, 2023; 9(5): 5693-5714. DOI: 10.1007/s40747-023-01013-7.
- L07: Ren, Huajuan and Tang, Yonghe and Dong, Weiyu and Ren, Shuai and Jiang, Liehui. DUEN: Dynamic ensemble handling class imbalance in network intrusion detection. Expert Systems with Applications, 2023; 229: article 120420. DOI: 10.1016/j.eswa.2023.120420.
- L08: Zouhri, Houssam and Idri, Ali and Ratnani, Ahmed. Evaluating the impact of filter-based feature selection in intrusion detection systems. International Journal of Information Security, 2024; 23(2): 759-785. DOI: 10.1007/s10207-023-00767-y.
- L09: Cantone, Marco and Marrocco, Claudio and Bria, Alessandro. Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study. IEEE Access, 2024; 12: pages 144489-144508. DOI: 10.1109/access.2024.3472907.
- L11: Umar, Mubarak Albarka and Chen, Zhanfang and Shuaib, Khaled and Liu, Yan. Effects of feature selection and normalization on network intrusion detection. Data Science and Management, 2025; 8(1): 23-39. DOI: 10.1016/j.dsm.2024.08.001.
- L12: Nassreddine, Ghalia and Nassereddine, Mohamad and Al-Khatib, Obada. Ensemble Learning for Network Intrusion Detection Based on Correlation and Embedded Feature Selection Techniques. Computers, 2025; 14(3): article 82. DOI: 10.3390/computers14030082.

D01/D02 là thông báo/tóm tắt luận án theo source types vàURLs trong resolver T, không được gọi là journal articles. Full field audit: template_audit_r04/field_coverage.csv. G5 vẫn mở.
