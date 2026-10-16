# Review độc lập r04 — lập luận, định vị và tính khả thi

Ngày: 16/10/2026. Phạm vi: phần tổng quan/luận cứ và Research Gap Matrix; đây là nhận xét nội bộ của AI, không phải phê duyệt GVHD, full-proposal review, P20 hoặc quyết định đạt release gate. Điểm dưới đây là đánh giá chủ quan theo rubric được điều chỉnh cho đề tài NCKH sinh viên về IDS; không phải số liệu thực nghiệm hay bằng chứng hoàn thành sản phẩm.

## Đầu vào và cách kiểm tra

Đã đọc `MASTER_PROMPT.md`, `AGENTS.md`; researchwrite tại `C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md`, các references `evaluation-rubric.md` và `research-anti-slop.md`; foundation 00–07, `qa_logs/foundation_review_r02.md`, bản thảo `drafts/sections/tong_quan_luan_cu_r04.md`, `literature/resume_r04_2026_10_16/GAP_MATRIX_R04.md` và bản hiện hành `literature/gap_matrix.md`. Đối chiếu thêm canon, handoff và template matrix. Không đọc review của reviewer r04 khác, không thực hiện web search, không sửa nghiên cứu hoặc kết quả.

Đã đọc trực tiếp OOXML của DOCX gốc `templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx` bằng ZIP/XML read-only. Chỉ số body trong project là zero-based: body33 là tiêu đề “Sơ lược tình hình nghiên cứu, điều tra trong nước, ngoài nước”, body34 ghi bắt buộc điền, body35/37 là nhãn trong nước/ngoài nước, body36/38 là vùng trống điền nội dung. Hai mục địa lý của bản thảo phù hợp yêu cầu nội dung này. Đó là kiểm tra cấu trúc/nội dung, chưa phải kiểm tra file DOCX đã điền hoặc render.

## Findings

Không phát hiện P0 hoặc P1 chặn việc giữ bản thảo nội bộ trong phạm vi đã khóa. Không phát hiện thay RQ, trình bày kết quả hậu kiểm thành giả thuyết tiên nghiệm, hoặc biến thiếu bằng chứng thành claim novelty.

- **P2 — Bản thảo, “Khoảng thiếu bằng chứng và vị trí của đề tài”, đoạn đầu; Gap Matrix, hàng RQ1–RQ3.** Định vị local case study đúng mức, nhưng phần prose chuyển từ tổng quan sang “ma trận gap” khá nhanh. Người đọc form chưa thấy trực tiếp câu hỏi thao tác nào nối giữa thiết kế ensemble, số đặc trưng, lỗi và chi phí. Nên thêm một đoạn tổng hợp ngắn, dẫn về RQ1–RQ3 đã khóa và cách đánh giá trong `06_rq_method_output_gates.md`; giữ nguyên phân biệt association với causal effect. Đây là cải thiện khả năng đọc và truy vết, không phải yêu cầu tạo RQ hoặc thử nghiệm mới.
- **P2 — Bản thảo và Gap Matrix, nhiều vị trí như “năm2026”, “ngẫu nhiên80/20”, “trênTEST”, “kiểm chứng11”.** Thiếu khoảng trắng làm giảm độ rõ của tiếng Việt và gây khó khi chuyển sang form. Chuẩn hóa trước merge DOCX; không thay giá trị, nguồn hoặc trạng thái để làm văn bản gọn hơn.
- **P2 — Bản thảo, hai mục “Luận cứ chọn đề tài” và “Khoảng thiếu bằng chứng”; DOCX body33–38.** Form gốc yêu cầu tổng quan trong/ngoài nước, không có nhãn riêng cho hai mục luận cứ trong vùng này. Khi merge, cần giữ hai nhãn gốc, bố trí luận cứ ngắn thành phần dẫn/kết của tổng quan và ghi mapping rõ. Không tự thêm mục cấp cao rồi gọi đó là cấu trúc gốc. Chưa có artifact merge nên đây là yêu cầu cho bước tiếp theo, không phải lỗi bố cục đã quan sát.

## Tám chiều rubric đã điều chỉnh

| Chiều đánh giá | Điểm /10 | Nhận định trong phạm vi review |
|---|---:|---|
| Câu hỏi nghiên cứu rõ | 8,0 | Câu hỏi lợi ích–đánh đổi của pipeline đóng băng rõ; bản thảo dẫn về RQ gốc thay vì sửa câu hỏi theo kết quả. Có thể đưa liên kết RQ1–RQ3 ra prose rõ hơn. |
| Known → unknown → hệ quả | 7,5 | Prior components đã tồn tại; unknown được định vị là giới hạn bằng chứng của case study. Tension giữa gain, lỗi và chi phí có cơ sở, nhưng câu nối tổng hợp còn gián tiếp. |
| Khớp claim–evidence | 8,5 | Có reading boundaries và phân biệt metadata với đọc nguồn; domestic announcement không bị nâng thành kết quả luận án. Điểm này chỉ đánh giá cách dùng evidence và khai báo giới hạn, không xác minh lại metadata từng nguồn. |
| Chuỗi background → gap → RQ → phương pháp | 8,0 | Gap Matrix nối từng RQ với evidence và inferential limit; foundation 06 giữ đầy đủ các trạng thái. Bản thảo ngắn chưa hiện hết chuỗi nhưng có resolver rõ. |
| Tính khả thi | 7,0 | Tổng hợp/đối chiếu tài liệu hiện thực thi được; foundation 07 giữ gate reporting, ML reconstruction và demo riêng. Thiếu model/original environment và nguồn lực chưa được prose che lấp; phần này không đủ để chấm toàn bộ phương án thực nghiệm. |
| Đóng góp/định vị | 7,0 | Case study kiểm toán benchmark và trade-off cụ thể, không gán thuật toán mới. Corpus kế thừa và domestic sources còn mỏng nên chưa chứng minh field-wide novelty hoặc tổng quan đầy đủ đến 2026. |
| Ranh giới rủi ro | 8,5 | Nêu FS/meta nesting, RQ4/RQ5 partial, không external validation, không matched sampling và thiếu training replay. Chronology phục hồi được nói rõ. |
| Ngôn ngữ | 7,5 | Không có hứa hẹn vượt trội, lấp khoảng trống hoặc kết luận mạnh hơn evidence; cần sửa khoảng trắng và giảm tải tham chiếu quản trị ở bản prose đưa vào form. |

Trung bình số học: **7,75/10**. Mỗi chiều ≥7; không dùng trung bình để che finding nghiêm trọng. Điểm này không thay validation artifact, không nâng foundation gate r02 thành full proposal gate và không đóng G0–G6.

## Quyết định tác giả và dữ kiện khoa học

Các dữ kiện được dùng theo bằng chứng hiện hành: prior work đã có voting/stacking/FS; official/novel views không là hai benchmark độc lập; trạng thái thiếu matched resampling/ML replay và giới hạn FS/meta nesting được canon ghi nhận. Reviewer không tái kiểm định thí nghiệm hoặc suy thêm kết quả của các paper.

Các quyết định vẫn thuộc tác giả/GVHD: chấp nhận hồ sơ phục hồi thay đề cương tiền thực nghiệm; vị trí đặt phần luận cứ bổ sung trong form; mức độ corpus cần mở rộng cho hồ sơ nộp; các thông tin hành chính/phê duyệt. Đề nghị bổ sung đoạn nối là chỉnh sửa diễn đạt trong scope hiện có, không thay đổi scientific contract. Không dùng việc reviewer chấp nhận local positioning để tuyên bố cơ sở quản lý đã chấp nhận đề tài.

## Khuyến nghị và một sửa đổi có tác động

**KEEP_SCOPED_INTERNAL_DRAFT**, sửa P2 trước merge. Sau sửa có thể đưa phần này vào gói nội dung để GVHD xem cùng các phần khác; chưa đủ nhãn supervisor-approved, final proposal hoặc submission-ready. Không cần mở lại foundation r02 chỉ vì review này.

Sửa có tác động nhất: thêm sau câu mở đầu mục “Khoảng thiếu bằng chứng và vị trí của đề tài” đoạn theo nghĩa sau, dẫn N1/N3: “Với RQ1–RQ3 đã khóa, việc đối chiếu cần làm rõ lợi ích quan sát được của ensemble so với mô hình đơn, trade-off hiệu năng–chi phí giữa các pipeline và mối liên hệ mô tả giữa lỗi của learner nền với kết quả kết hợp. Các nội dung này được đánh giá bằng artifact hiện có theo protocol đã khóa; chúng không chứng minh hiệu quả nhân quả của riêng feature selection hoặc độ ổn định qua tái huấn luyện độc lập.” Đây là gợi ý biên tập, chưa phải nội dung đã sửa trong draft.

Bước tiếp theo: sửa đoạn nối và khoảng trắng, kiểm lại source/path mapping, sau đó merge nội dung theo hai vùng trong/ngoài nước của form; phần DOCX/render và tính đầy đủ toàn hồ sơ phải có kiểm định riêng.
