# Humanizer Change Log

Humanizer3.1.0, exact SKILL.md saved in audit/. File-mode workflow: whole-text review → marked patterns → rewrite → claim/numeric review → final source. This is a style edit, not a detector or assertion of human authorship. Technical Vietnamese remains neutral. Cover/declaration/acknowledgements, questions, tables, figures, equations, citations and defined code terms are preserved. Changes are scoped to38 supported passages.

## H01 · chapters/introduction_revision_v3_2026_10_19.tex

**Lý do:** Tách câu dài; làm rõ chủ thể và các yếu tố ảnh hưởng. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Các bộ phân loại học máy có thể phát hiện những mẫu phức tạp trong dữ liệu flow, nhưng điểm số cao trên một benchmark không tự bảo đảm hiệu quả trong các bối cảnh triển khai khác nhau. Cách tạo và làm sạch dữ liệu, lựa chọn đặc trưng, chia tập và các loại sai số có thể ảnh hưởng đáng kể đến diễn giải thí nghiệm.

Sau:
> Các bộ phân loại học máy có thể nhận ra những mẫu phức tạp trong dữ liệu flow. Tuy nhiên, điểm số cao trên một benchmark chưa bảo đảm mô hình sẽ hoạt động tốt ở môi trường khác. Kết quả còn phụ thuộc vào cách tạo, làm sạch và chia dữ liệu, cách chọn đặc trưng, cũng như loại lỗi được xem xét.

## H02 · chapters/introduction_revision_v3_2026_10_19.tex

**Lý do:** Thay danh từ hóa và lời đánh giá giá trị bằng yêu cầu cụ thể. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Vì vậy, giá trị của nghiên cứu phụ thuộc vào giao thức có thể truy vết, cách mô tả đúng các loại lỗi, sự đối chiếu chi phí và diễn giải thận trọng độ bất định.

Sau:
> Nghiên cứu vì thế cần một giao thức có thể kiểm tra lại, mô tả rõ từng loại lỗi, đối chiếu chi phí và nêu đúng mức độ bất định của kết quả.

## H03 · chapters/introduction_revision_v3_2026_10_19.tex

**Lý do:** Viết câu hỏi nghiên cứu trực tiếp, giảm cấu trúc danh từ trừu tượng. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Vấn đề trung tâm là liệu các mô hình cơ sở có dạng sai số bổ sung giúp ensemble cải thiện kết quả so với một mô hình đơn mạnh hay chủ yếu làm thay đổi đánh đổi giữa báo động giả (FP) và tấn công bị bỏ sót (FN).

Sau:
> Câu hỏi chính là: sai số khác nhau giữa các mô hình cơ sở có giúp ensemble dự đoán tốt hơn một mô hình đơn mạnh, hay chủ yếu chuyển đổi giữa báo động giả (FP) và tấn công bị bỏ sót (FN)?

## H04 · chapters/introduction_revision_v3_2026_10_19.tex

**Lý do:** Bỏ tự đánh giá giá trị; giữ đủ ba giới hạn kết luận. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Những kết quả này có giá trị thực nghiệm trong phạm vi một nghiên cứu trường hợp, nhưng chưa đủ cơ sở để khẳng định thuật toán Ensemble Learning mới, ưu thế tổng thể của Stacking hay khả năng khái quát ngoài UNSW-NB15.

Sau:
> Các kết quả chỉ được diễn giải trong phạm vi nghiên cứu trường hợp này. Chúng chưa chứng minh một thuật toán Ensemble Learning mới, ưu thế tổng thể của Stacking hay khả năng khái quát ngoài UNSW-NB15.

## H05 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Làm rõ dữ liệu nào thiếu thông tin; tách hai ý. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Những biến này làm dữ liệu có thể biểu diễn bằng bảng để áp dụng học máy, nhưng không chứa mọi thông tin của payload hoặc ngữ cảnh vận hành.

Sau:
> Các biến này cho phép biểu diễn lưu lượng dưới dạng bảng để áp dụng học máy. Tuy vậy, bảng đặc trưng không chứa đầy đủ payload và ngữ cảnh vận hành.

## H06 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Bỏ lời dẫn nhấn mạnh; giữ quy tắc fit trong phần huấn luyện. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Một nguyên tắc phương pháp quan trọng là mọi tham số học được từ dữ liệu, như thống kê chuẩn hóa, danh mục encoding hoặc cấu hình Feature Selection, phải được tính từ tập huấn luyện được phép dùng trong từng bước validation rồi áp dụng cho tập còn lại.

Sau:
> Mọi tham số học từ dữ liệu, gồm thống kê chuẩn hóa, danh mục encoding và cấu hình Feature Selection, phải được tính trên phần huấn luyện được phép dùng ở từng bước validation, rồi mới áp dụng cho phần còn lại.

## H07 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Thay nhận xét về cách trình bày bằng ý nghĩa của chỉ số. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Việc đọc riêng FPR và FNR giúp trình bày đánh đổi này minh bạch hơn một chỉ số Accuracy duy nhất.

Sau:
> FPR và FNR cho biết riêng hai phía của đánh đổi mà Accuracy tổng thể có thể che khuất.

## H08 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Đưa cách kiểm tra lên trước, giữ giới hạn về LR. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Vai trò này không chứng minh LR riêng lẻ tối ưu; sự hữu ích phải quan sát qua OOF predictions, độ đa dạng lỗi, và hiệu quả cuối trong protocol thống nhất.

Sau:
> Để biết LR có đóng góp hay không, cần xem dự đoán OOF, độ đa dạng lỗi và kết quả cuối trong cùng protocol; việc dùng LR ở hai tầng chưa chứng minh LR riêng lẻ là tối ưu.

## H09 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Đổi đại từ mơ hồ thành tên mô hình; tách câu dài. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Khi nó được chọn vào Stacking, lý do phương pháp hợp lệ là kiểm tra liệu một mô hình có cấu trúc sai số khác biệt có đóng góp hiệu quả hay không, thay vì giả định mô hình yếu kết hợp với mô hình mạnh luôn làm kết quả tốt hơn.

Sau:
> Khi đưa Decision Tree vào Stacking, nghiên cứu cần kiểm tra xem sai số khác biệt của nó có giúp bộ kết hợp hay không. Không thể mặc định rằng ghép mô hình yếu với mô hình mạnh sẽ cải thiện kết quả.

## H10 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Bỏ từ tiếng Anh gượng ép, giữ nguyên giới hạn của diversity. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Do đó diversity là biến quan sát có ý nghĩa, chứ không phải bằng chứng bắt buộc cho superiority.

Sau:
> Do đó, diversity là một đặc điểm cần quan sát; riêng nó chưa chứng minh bộ kết hợp có hiệu năng cao hơn.

## H11 · chapters/theoretical_foundations_revision_v2_2026_10_17.tex

**Lý do:** Nêu khác biệt cụ thể thay cho cụm ưu nhược điểm chung. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Các phương pháp có ưu nhược điểm khác nhau về chi phí, tương tác biến và thiên lệch theo model.

Sau:
> Mỗi phương pháp có chi phí, khả năng xét tương tác biến và mức phụ thuộc vào model khác nhau.

## H12 · chapters/related_work_revision_v4_2026_10_19.tex

**Lý do:** Tách câu và làm rõ giới hạn suy luận từ tổng quan. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Kết quả tổng quan này là cơ sở lựa chọn câu hỏi so sánh thực nghiệm, không thể thay bằng nhận định đơn giản rằng kết hợp nhiều classifier chắc chắn làm hiệu năng tăng.

Sau:
> Tổng quan này giúp hình thành câu hỏi so sánh thực nghiệm. Nó không cho phép kết luận rằng cứ kết hợp nhiều classifier thì hiệu năng sẽ tăng.

## H13 · chapters/related_work_revision_v4_2026_10_19.tex

**Lý do:** Thay cách nói vay mượn và danh từ hóa; giữ giới hạn tính mới. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Việc tồn tại những công trình này giới hạn tuyên bố novelty: đóng góp được định vị ở kiểm toán case study, sự minh bạch về loại lỗi, bằng chứng cặp và chi phí, \emph{không} phải tạo ra Stacking hay Feature Selection.

Sau:
> Các công trình này cho thấy Stacking và Feature Selection đã có tiền lệ. Đóng góp của đề tài nằm ở việc kiểm toán case study, báo cáo rõ loại lỗi, đối chiếu theo cặp và xem xét chi phí; \emph{không} phải tạo ra hai kỹ thuật đó.

## H14 · chapters/related_work_revision_v4_2026_10_19.tex

**Lý do:** Bỏ mô tả hiển nhiên về danh mục; giữ căn cứ và giới hạn so sánh. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Các nhận xét tổng quan ở đây dựa trên những bài báo được trích dẫn trong danh mục tài liệu tham khảo; do khác biệt dữ liệu và giao thức, không sử dụng kết quả từ các nghiên cứu đó như đối chứng trực tiếp cho ba mô hình của đề tài.

Sau:
> Phần tổng quan dựa trên các bài báo đã trích dẫn. Vì dữ liệu và giao thức khác nhau, kết quả của các công trình đó không được dùng làm đối chứng trực tiếp cho ba mô hình của đề tài.

## H15 · chapters/revision_prior_work_v5_2026_10_19.tex

**Lý do:** Bỏ phân loại đóng góp gượng ép; giữ đầy đủ phạm vi đóng góp và các đại lượng. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Ba khái niệm đóng góp cần được phân biệt. Nghiên cứu này không đề xuất methodological novelty cho Stacking hay Feature Selection; các thành phần đó đã có tiền lệ trong tài liệu. Đóng góp nghiên cứu ở đây là case study theo split chính thức, còn empirical contribution là cách đối chiếu cùng các pipeline trên các mẫu holdout bằng metric tổng hợp, sai số theo lớp, độ bất định và chi phí đã lưu.

Sau:
> Stacking và Feature Selection đã được nghiên cứu trước đây, nên đề tài không đề xuất phương pháp mới cho hai kỹ thuật này. Đề tài thực hiện một case study theo split chính thức. Phần đóng góp thực nghiệm là đối chiếu các pipeline trên cùng mẫu holdout qua chỉ số tổng hợp, sai số theo lớp, độ bất định và chi phí đã lưu.

## H16 · chapters/dataset_eda_revision_v4_2026_10_19.tex

**Lý do:** Rút lời dẫn, diễn đạt quan hệ giữa phân bố và chỉ số trực tiếp. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Điều này cho thấy tổng Accuracy và Weighted-F1 có thể chịu ảnh hưởng của cách phân bố lớp; đọc Macro-F1, MCC và chỉ số riêng từng lớp sẽ rõ ràng hơn khi so sánh các pipeline.

Sau:
> Vì Accuracy và Weighted-F1 chịu ảnh hưởng của phân bố lớp, khi so sánh pipeline cần đọc thêm Macro-F1, MCC và chỉ số của từng lớp.

## H17 · chapters/dataset_eda_revision_v4_2026_10_19.tex

**Lý do:** Thay dịch máy support bằng số mẫu; giữ ý nghĩa mẫu số. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Quy mô hỗ trợ không đồng đều có thể làm độ chính xác theo từng nhóm biến động mạnh; một số đếm FN cần được đọc cùng mẫu số của chính nhóm Attack tương ứng.

Sau:
> Số mẫu giữa các nhóm chênh lệch lớn, nên độ chính xác theo nhóm có thể biến động mạnh. Số FN cần được đọc cùng tổng số mẫu của nhóm Attack tương ứng.

## H18 · chapters/dataset_eda_revision_v4_2026_10_19.tex

**Lý do:** Làm tự nhiên câu giải thích chức năng EDA; giữ39. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> EDA của TRAIN đã kiểm tra 39 biến số. Các tiêu chí thống kê dùng để khám phá không đồng nghĩa phép thử nhân quả.

Sau:
> EDA trên TRAIN khảo sát 39 biến số. Các thống kê mô tả dùng trong bước này không phải phép kiểm tra quan hệ nhân quả.

## H19 · chapters/dataset_eda_revision_v4_2026_10_19.tex

**Lý do:** Bỏ cách đánh giá quy mô mơ hồ, giữ khả năng đối chiếu và phân tích. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> UNSW-NB15 hỗ trợ một case study IDS nhị phân có quy mô vừa đủ cho đối chiếu nhiều pipeline và có nhãn Attack để phân tích sai số.

Sau:
> Với quy mô của UNSW-NB15 và nhãn Attack đi kèm, nghiên cứu có thể đối chiếu nhiều pipeline IDS nhị phân và phân tích sai số.

## H20 · chapters/methodology_revision_v4_2026_10_19.tex

**Lý do:** Tách cấu trúc danh sách dài thành hai câu có chủ ngữ. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Thiết kế hướng tới so sánh một baseline Random Forest với Stacking, một cấu hình Random Forest có ít đặc trưng hơn, đồng thời khảo sát lỗi, độ bất định và chi phí quan sát được.

Sau:
> Nghiên cứu lấy Random Forest làm baseline để đối chiếu với Stacking và một cấu hình Random Forest ít đặc trưng hơn. Các phép so sánh xét cả sai số, độ bất định và chi phí quan sát được.

## H21 · chapters/methodology_revision_v4_2026_10_19.tex

**Lý do:** Tách cơ chế và giới hạn; không hứa loại bỏ mọi leakage. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Cách tạo đầu vào OOF làm giảm việc meta learner học trực tiếp từ dự đoán in-sample của tầng cơ sở; nó không tự loại bỏ mọi nguồn lạc quan trong quá trình chọn cấu hình.

Sau:
> Đầu vào OOF giúp meta learner tránh học trực tiếp từ dự đoán in-sample của tầng cơ sở. Dù vậy, quá trình chọn cấu hình vẫn có thể tạo ra các nguồn lạc quan khác.

## H22 · chapters/methodology_revision_v4_2026_10_19.tex

**Lý do:** Bỏ dấu gạch ngang đóng khung và lời mô tả về tuyên bố; giữ ba phạm vi. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Ba phạm vi này — khả năng tái lập trong môi trường xác định, tái huấn luyện từ TRAIN và triển khai — được xem là các tuyên bố riêng biệt.

Sau:
> Vì vậy, cần đánh giá riêng khả năng tái lập trong môi trường xác định, tái huấn luyện từ TRAIN và triển khai.

## H23 · chapters/methodology_revision_v4_2026_10_19.tex

**Lý do:** Tách hai quy tắc, giữ nguyên mọi hạn chế kiểm định. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Không đưa p-value hay khoảng tin cậy suy diễn được hiểu như năm lần kiểm tra độc lập, và không thực hiện t-test hoặc ANOVA với năm seed này; cũng không hiệu chỉnh kết quả sau khi thấy seed đầu tiên.

Sau:
> Năm seed này không được dùng như năm lần kiểm tra độc lập để tính p-value, khoảng tin cậy suy diễn, t-test hoặc ANOVA. Kết quả cũng không được hiệu chỉnh sau khi xem seed đầu tiên.

## H24 · chapters/results_discussion_revision_v4_2026_10_19.tex

**Lý do:** Tách điều kiện khỏi kết luận để người đọc theo dõi dễ hơn. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Khi chưa có hàm chi phí vận hành để quy đổi cảnh báo giả và bỏ sót thành cùng một thang đo, kết quả này không xác định được cấu hình phù hợp hơn cho mọi bối cảnh sử dụng.

Sau:
> Chưa có hàm chi phí vận hành để quy đổi hai loại lỗi về cùng thang đo. Vì vậy, kết quả này chưa xác định được cấu hình phù hợp hơn cho mọi bối cảnh sử dụng.

## H25 · chapters/results_discussion_revision_v4_2026_10_19.tex

**Lý do:** Thay đại từ mơ hồ, giữ giới hạn thời gian đo. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Chúng mô tả các cấu hình và môi trường lịch sử cụ thể; không phải benchmark lặp lại trên thiết bị triển khai.

Sau:
> Các số đo chỉ mô tả những cấu hình trong môi trường lịch sử đó; đây chưa phải benchmark lặp lại trên thiết bị triển khai.

## H26 · chapters/results_discussion_revision_v4_2026_10_19.tex

**Lý do:** Giải thích hậu nghiệm bằng thao tác cụ thể, không đổi mục tiêu nhị phân. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Phân tích hậu nghiệm theo họ nhãn thật làm rõ khác biệt mà chỉ số tổng thể gộp lại.

Sau:
> Phân nhóm theo nhãn Attack thật sau dự đoán cho thấy những khác biệt bị gộp trong chỉ số tổng thể.

## H27 · chapters/revision_rq_answers_v4_2026_10_19.tex

**Lý do:** Bỏ kết cấu dài và qualifier chồng, giữ tính khả dĩ và giới hạn. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Mức bổ sung lỗi này tạo điều kiện để một bộ kết hợp có thể khai thác khác biệt giữa các learner, nhưng tự nó không bảo đảm Voting hoặc Stacking sẽ cải thiện dự đoán.

Sau:
> Bộ kết hợp có thể khai thác khác biệt lỗi giữa các learner. Tuy nhiên, riêng mức bổ sung lỗi quan sát được chưa bảo đảm Voting hoặc Stacking sẽ cải thiện dự đoán.

## H28 · chapters/revision_rq_answers_v4_2026_10_19.tex

**Lý do:** Nêu rõ đại lượng bất đồng, giữ phạm vi McNemar. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Hai loại bất đồng gần cân bằng, phù hợp với kết quả McNemar không cho thấy khác biệt rõ về tính đúng tổng thể.

Sau:
> Số bất đồng theo hai hướng gần cân bằng. Kết quả này phù hợp với việc McNemar chưa phát hiện khác biệt rõ về tính đúng tổng thể.

## H29 · chapters/p21_results_v5_2026_10_19.tex

**Lý do:** Nói về thí nghiệm thay cho quá trình tạo văn bản; thời điểm đã được nguồn xác nhận. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Báo cáo kết quả bổ sung này được tạo \emph{sau} quá trình đánh giá official TEST lịch sử.

Sau:
> Thực nghiệm bổ sung được thực hiện \emph{sau} giai đoạn đánh giá official TEST lịch sử.

## H30 · chapters/p21_results_v5_2026_10_19.tex

**Lý do:** Nêu rõ mô hình nhỉnh hơn; không thêm mức hay kết quả mới. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Có một seed nhỉnh hơn rất nhỏ nhưng không làm đảo dấu hiệu số trung bình.

Sau:
> Ở một seed, Stacking nhỉnh hơn rất ít; hiệu số trung bình vẫn giữ nguyên dấu.

## H31 · chapters/p21_results_v5_2026_10_19.tex

**Lý do:** Tách câu liệt kê dài, giữ đủ các khoản chi phí chưa đo. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Cả hai tổng này chưa cộng thời gian xử lý dữ liệu ngoài các lời gọi đã đo, lưu artifact, giám sát hay latency phục vụ nên không được gọi là tổng chi phí triển khai end-to-end. Vì vậy không thể dựa vào thời gian fit RF17 để tuyên bố Feature Selection đã làm giảm \emph{tổng} chi phí training.

Sau:
> Các số này chưa tính thời gian xử lý dữ liệu ngoài những lời gọi đã đo, lưu artifact, giám sát và latency phục vụ. Chúng chưa phản ánh chi phí triển khai end-to-end. Thời gian fit RF17 vì thế chưa đủ để kết luận Feature Selection làm giảm \emph{tổng} chi phí training.

## H32 · chapters/p21_results_v5_2026_10_19.tex

**Lý do:** Sửa câu ghép thiếu ranh giới, làm rõ đối tượng kiểm tra. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Mỗi seed có năm cấu hình trùng digest FIT source và cùng nhãn true 35\,069 dòng validation, các kiểm tra kết quả phát hiện tổng TN+FP+FN+TP đúng support, khớp các chỉ số Macro-F1/MCC/FPR/FNR và không cho thấy lệch dữ liệu trong metadata.

Sau:
> Trong mỗi seed, năm cấu hình dùng cùng digest FIT source và cùng nhãn thật của 35\,069 dòng validation. Kiểm tra xác nhận tổng TN+FP+FN+TP khớp support, các chỉ số Macro-F1/MCC/FPR/FNR nhất quán và metadata không cho thấy lệch dữ liệu.

## H33 · chapters/validity_discussion_revision_v4_2026_10_19.tex

**Lý do:** Tách câu ba dấu chấm phẩy; giữ giả định và phạm vi tối ưu. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Giá trị thực tế của thay đổi này phụ thuộc vào chi phí tương đối của cảnh báo giả và bỏ sót trong môi trường vận hành; chưa có dữ liệu thật về chi phí đó; phần phân tích độ nhạy giả định phía dưới chỉ minh họa điều kiện để hai pipeline đổi thứ hạng theo chi phí, không xếp một cấu hình là tối ưu cho mọi NIDS.

Sau:
> Ý nghĩa vận hành của thay đổi này phụ thuộc vào chi phí tương đối giữa cảnh báo giả và bỏ sót. Đề tài chưa có dữ liệu thực về các chi phí đó. Phân tích độ nhạy dưới đây dùng các tỷ lệ giả định để chỉ ra khi nào hai pipeline đổi thứ hạng; nó chưa xác định cấu hình tối ưu cho mọi NIDS.

## H34 · chapters/validity_discussion_revision_v4_2026_10_19.tex

**Lý do:** Bỏ lời dẫn giải thích điều người đọc vừa thấy; giữ hệ quả. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Việc đọc đồng thời các chỉ số này cho thấy lý do một điểm tổng hợp duy nhất chưa đủ để quyết định triển khai.

Sau:
> Một điểm tổng hợp duy nhất vì thế chưa đủ để quyết định triển khai.

## H35 · chapters/validity_discussion_revision_v4_2026_10_19.tex

**Lý do:** Thay kết cấu đối xứng máy móc bằng hai mệnh đề rõ chức năng. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Như vậy, diversity là một thuộc tính quan sát được của các dự đoán, còn lợi ích của ensemble phải được xác lập trực tiếp bằng hiệu năng và loại lỗi của bộ kết hợp.

Sau:
> Diversity mô tả khác biệt giữa các dự đoán. Để xác định lợi ích của ensemble, vẫn phải đo trực tiếp hiệu năng và từng loại lỗi của bộ kết hợp.

## H36 · chapters/validity_discussion_revision_v4_2026_10_19.tex

**Lý do:** Bỏ câu mô tả phương thức biên tập và tự đánh giá, không bỏ kết quả. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Bảng~\ref{tab:rq-evidence} tóm tắt kết quả thực nghiệm có thể bảo vệ cùng phần còn chưa được xác định. Các khoảng trống được nêu trong mối liên hệ với kết quả, thay vì thay thế câu trả lời bằng danh sách giới hạn.

Sau:
> Bảng~\ref{tab:rq-evidence} tóm tắt kết quả đã có cho từng câu hỏi nghiên cứu và những bằng chứng còn thiếu.

## H37 · chapters/conclusion_revision_v4_2026_10_19.tex

**Lý do:** Bỏ ẩn dụ lớp bằng chứng; giữ hai phạm vi thực nghiệm. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Nghiên cứu đánh giá học tổ hợp và mô hình đơn cho phân loại nhị phân Normal/Attack trên UNSW-NB15 bằng hai lớp bằng chứng được tách biệt về thời điểm thiết kế và bộ dữ liệu đánh giá.

Sau:
> Nghiên cứu so sánh học tổ hợp và mô hình đơn cho phân loại Normal/Attack trên UNSW-NB15. Hai phần thực nghiệm được trình bày riêng vì khác thời điểm thiết kế và bộ dữ liệu đánh giá.

## H38 · chapters/conclusion_revision_v4_2026_10_19.tex

**Lý do:** Tách danh sách đóng góp quá dài; giữ đầy đủ từng đóng góp có căn cứ. **Mức:** diễn đạt, không đổi mệnh đề khoa học.

Trước:
> Đóng góp kiểm chứng của công trình là đối chiếu nhiều thuật toán theo các chỉ số Macro-F1, MCC, FPR, FNR và ma trận nhầm lẫn; thảo luận đa dạng sai số, nguồn bất định, so sánh pipeline có kiểm soát siêu tham số, lựa chọn đặc trưng lặp trên FIT và kiểm soát rò rỉ vector trùng trong inner Stacking.

Sau:
> Công trình đối chiếu nhiều thuật toán bằng Macro-F1, MCC, FPR, FNR và ma trận nhầm lẫn; phân tích đa dạng sai số và nguồn bất định. Các đối chứng kiểm soát siêu tham số, lặp lựa chọn đặc trưng trên FIT và kiểm soát rò rỉ do vector trùng trong inner Stacking.