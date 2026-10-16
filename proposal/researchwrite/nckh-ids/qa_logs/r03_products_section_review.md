# Section QA r03 — nhu cầu, sản phẩm, tiến độ và kinh phí

Ngày: 16/10/2026. Vai trò: feasibility/template-evidence reviewer; AI internal review, không phải phê duyệt của tác giả, GVHD hoặc đơn vị. Đối tượng duy nhất: `drafts/sections/ung_dung_san_pham_tien_do_r03.md`, 55 dòng tại thời điểm đọc. Không review toàn proposal, không sửa draft hoặc memory, không chạy lại nghiên cứu.

## Căn cứ và cách kiểm

Đã đọc đầy đủ draft trước khi chấm; áp dụng `C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md`, `references/evaluation-rubric.md` và `references/research-anti-slop.md`. Đọc contracts04,06,07, evidence_table02, canon, claim–evidence matrix, template matrix, framework, availability, task board, release blockers và `defense/qa_validation_r02.json`. Đối chiếu trực tiếp OOXML body39–55 của DOCX gốc, chỉ đọc, không chỉnh template. Lệnh đọc OOXML đầu tiên lỗi encoding stdout cp1252; chạy lại với `python -X utf8` thành công. Không web, không fit/predict, không render DOCX/PDF.

Tám chiều rubric được thích nghi cho phần nhu cầu–deliverable–lịch, không buộc phần này viết lại tổng quan/RQ/phương pháp. Điểm chỉ nói về partial sections trong bối cảnh foundation đã cung cấp, không cấp điểm cho toàn đề cương.

## Findings

P0: Không phát hiện trong phạm vi đã đọc.

P1: Không phát hiện trong phạm vi đã đọc. Bản thảo không nhận đã có demo, train replay, deployment, phê duyệt hoặc bài báo; không dùng TEST để sửa mô hình. Các số 4/11/11/4 tuần, 03 quyển và 3.000.000 + 3.500.000 + 500.000 = 7.000.000 VND khớp mẫu đọc trực tiếp. Dạng III có đúng các nhãn chương trình máy tính/phương pháp, giải pháp/sơ đồ, bảng số liệu. Tất cả được giữ là thông tin mẫu cần xác nhận.

P2-01 — Dòng27, mô tả yêu cầu CD chưa mang đủ chi tiết bắt buộc của body49. OOXML còn yêu cầu file báo cáo có trang bìa như bản cứng, và file bài báo, nếu có, là bản cuối đã sửa theo góp ý Hội đồng khoa học Khoa. Câu “Giữ nội dung đó khi điền bản sao form” tránh xóa yêu cầu, nhưng bảng tiêu chí của partial draft chưa thể hiện các tiêu chí này để kiểm. Bổ sung chính xác hai điều kiện vào mapping/tiêu chí, vẫn giữ nhãn “theo mẫu, tính áp dụng cần xác nhận”; không biến chúng thành bằng chứng đã có review hoặc bài báo.

P2-02 — Dòng33–38, cần làm rõ hồ sơ phục hồi. Việc phân biệt lịch mẫu với thời gian thực tế ở dòng38 là đúng; tuy nhiên contract07 còn yêu cầu nói rõ hồ sơ đang phục hồi sau khi đã có kết quả và AI không cấp phê duyệt hồi tố. Dòng34 “đã thực hiện” cho thấy chronology này nhưng chưa nêu trực tiếp. Khi ghép thành đề cương, thêm một câu bối cảnh phục hồi và điều kiện tác giả/GVHD xác nhận tính chấp nhận nếu đơn vị yêu cầu đề cương trước thực nghiệm. Không tự gán ngày quá khứ hoặc đổi lịch mẫu.

P2-03 — Dòng3,15,23,27,33–38,42 có nhiều chỗ dính chữ/số: “mục39”, “dạngIII”, “ít nhất15”, “quá02”, “chuyên đề1”, “là3.000.000”. Sửa khoảng trắng trước khi chuyển DOCX. Đây là lỗi đọc/biên tập, không thay nội dung khoa học.

## Điểm rubric

| Chiều | Điểm /10 | Lý do trong phạm vi partial section |
|---|---:|---|
| 1. Problem clarity | 7.5 | Người dùng kết quả và bài toán đánh giá từ flow CSV rõ ở dòng7–11; RQ chính thuộc phần khác, không yêu cầu lặp ở đây. |
| 2. Scientific tension | 7.5 | Nêu trade-off FPR/FNR/chi phí và giới hạn benchmark; không có literature synthesis tại đây vì ngoài contract phần này. |
| 3. Evidence matching | 8.5 | S1–S7 và status ledger truy được; số mẫu khớp OOXML, 20 Q&A khớp JSON; không nâng historical artifact thành release-ready. Chưa tái kiểm mọi artifact scientific hoặc render trong review này. |
| 4. Logic chain | 8.0 | Nhu cầu → sản phẩm → tiêu chí → chặng lịch liên kết; A/B/C không bị đánh đồng. Thiếu hai tiêu chí CD tại P2-01. |
| 5. Feasibility | 7.5 | Dependencies model/preprocessing/schema và capacity/output isolation rõ; tài nguyên, ngày và lịch áp dụng vẫn pending có nhãn. Chưa đủ để cam kết hoàn tất trong chặng4 tuần. |
| 6. Specific contribution | 7.0 | Giá trị cụ thể là tài liệu đánh giá benchmark, bảng và pipeline có kiểm toán; không slogan novelty. So sánh prior work/novelty nằm ngoài phần này và chưa được chứng nhận. |
| 7. Risk boundaries | 8.5 | Không external/live claims; không lấy viewer thay inference; demo phụ thuộc model, clean training chưa đạt, dữ liệu raw không tự bundle. Context phục hồi nên nói trực tiếp hơn theo P2-02. |
| 8. Language quality | 7.5 | Văn bản cụ thể, không intensifier thiếu chứng cứ; không có cơ cấu “đầu tiên/tiếp theo” máy móc hoặc lời hứa superiority. Lỗi khoảng trắng P2-03 và jargon nội bộ cần làm sạch khi merge. |

Trung bình số học: **7.75/10**. Không chiều nào dưới7 nên không phát sinh giải trình chiều dưới ngưỡng. Anti-slop áp dụng thủ công theo ý nghĩa tiếng Việt, không giả nhận đã chạy bộ dò tiếng Anh/tiếng Trung.

## Khuyến nghị

**KEEP_SCOPED_DRAFT / giữ phần thảo để ghép sau sửa P2.** Section score >6.5 đạt điều kiện giữ phần theo rubric. Bản thân partial section nằm trong dải có thể dùng để trao đổi với GVHD sau sửa; kết quả này không nâng toàn proposal thành supervisor-facing, không xác nhận form hoàn chỉnh và không đóng G0–G6. Trạng thái cuối vẫn nội bộ, chưa DOCX/PDF/render, còn thông tin hành chính và tính áp dụng mẫu chưa xác nhận.

Một sửa đổi có hệ quả lớn nhất: **bổ sung hai tiêu chí CD còn thiếu ở dòng27 theo đúng body49** để bản mapping không làm rơi yêu cầu trang bìa bản điện tử/bản bài báo sau góp ý khi chuyển từ MD vào DOCX. Đây là bổ sung tiêu chí cần kiểm, không phải tuyên bố đã hoàn thành.

Review không chỉnh bất kỳ file nào khác. Nếu áp dụng sửa, ghi validation riêng; không tự coi điểm7.75 là điểm chấm lại sau sửa.
