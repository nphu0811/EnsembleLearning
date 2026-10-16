# Vòng r04 — dependency graph và tiêu chí

Giữ nguyên dữ liệu, source huấn luyện, kết quả, RQ và ngưỡng đã khóa. Mục tiêu là hoàn thiện evidence và sản phẩm còn thiếu; không dùng điểm reviewer thay artifact/test.

| Task | Inputs / lý do | Output | VERIFY / lỗi cần tránh | Downstream |
|---|---|---|---|---|
| R04-RESUME | r03 STATE + preservation manifest | audit máy r04 |174/174 trước sửa;282/282 bảo toàn;ZIP/DOCX integrity | Tất cả task |
| R04-REF |6 pending legacy +U01/U03, saved DOI records | fresh API ledger, field/source report, current matrix/BibTeX | Multi-source field comparisons; không xác nhận conflict; lưu lỗi nguồn; không full-text claim từ metadata | Gap/tổng quan |
| R04-READ | Nguồn có truy cập, câu hỏi cụ thể về phương pháp/validation | Source-linked reading notes và claim map | Chỉ đoạn thực đọc; không suy missing method details | Gap/tổng quan |
| R04-GAP | Paper/source notes +frozen RQ +canon | Gap matrix có comparator/known/unknown/consequence | Không field-wide novelty/không đổ lỗi prior work chưa audit | Đề cương/báo cáo |
| R04-LIT | Foundation đã review +source notes/gap | Tổng quan trong/ngoài nước và lý do chọn đề tài | Citation-claim checks; review nội dung; sửa findings có căn cứ | Ghép nội dung đề cương |
| R04-FORM | DOCX gốc read-only +mọi section | Full field coverage map +content assembly chưa điền form | Trích từng paragraph/cell, metadata placeholders, budget/schedule; chưa render không đạt QA hình thức | Full-proposal review/DOCX |
| R04-SOFTWARE | Source/config/env/capacity thực tế | Feasibility/path isolation +safe runnable entrypoint khi đủ | Không model selection bằng TEST; không ghi historical outputs; smoke phải dùngTRAIN | G3/demo |
| R04-DEFENSE | Frozen evidence +Q&A | Kịch bản/runbook/checklist trung thực | Source links/count/status checks; không gọi viewer là inference | G6 |

Thứ tự: RESUME→REF→READ→GAP→LIT→FORM; khi nguồn bị chặn, ghi field/status và chuyển sang nguồn hoặc task khác. FORM content không phụ thuộc danh tính để draft, nhưng G5 final phụ thuộc xác nhận. Tool/runtime blocker không chặn chuẩn bị nguồn, nội dung, QA và tài liệu độc lập. Checkpoint sau task với `tools/r04_checkpoint.py`, output task JSON không overwrite; cuối phiên post-audit toàn manifest/preservation.
