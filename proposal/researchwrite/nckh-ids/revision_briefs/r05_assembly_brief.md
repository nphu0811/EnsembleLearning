# R05 — targeted revision brief

Input bất biến `drafts/De_cuong_noi_dung_review_r04.md`, SHA-256 `dfef1dffa3fdd8efbb558b65a02cb13c443da8529c5efba169d6b7dc7ad47bac`. Review độc lập `qa_logs/r05_assembled_argument_review.md`, SHA-256 `368996924d05576ad2d740ad3c4c7f395f93c1b97474be7e9b15f2051dfebdc0`. Review chỉ AI ở context riêng, không được trình bày như hội đồng con người.

Disposition trước sửa: targeted revision, chưa đủ nộp. Evidence review R04 không có P0/P1 trong scope nguồn; argument review R05 có P1 về self-contained RQ map, operational feasibility và stale software/model status. Hai nhận định không xung đột vì phạm vi khác nhau. Không dùng điểm trung bình reviewer làm gate.

Sửa theo thứ tự ARG-R05-03 → 01 → 02 → 04/05. Tạo `drafts/De_cuong_noi_dung_review_r05.md`; giữ r04 và các section lịch sử nguyên vẹn. Cập nhật foundation07 bằng checkpoint supplement có nhãn r05, không giả lịch sử r02 đã biết smoke.

| ID | Sửa | Kiểm nhận |
|---|---|---|
| ARG-R05-03 | Nêu replay PASS, smoke45/45 scoped, chưa final/fullTRAIN/demo; thêm source hiện hành | Actual metadata/validation; không rerun fit, không nâng SMOKE_ONLY |
| ARG-R05-01 | Thêm RQ1–5 nguyên văn, bảng thao tác/giới hạn và O1–O4 trong Nội dung | Exact frozen RQ comparison; mỗi RQ có method/output/status và giữ các phần chưa trả lời |
| ARG-R05-02 | Phụ lục remaining-work có dependency, vai trò chưa giao, tài nguyên/gate/stop action | Không cam kết ngày/ngân sách chưa duyệt; không full training; demo vẫn dependency thật |
| ARG-R05-04 | Một current metadata ledger, historical notes ghi đúng scope | Resolve labels/path và đối chiếu cited IDs/DOI/metadata verified |
| ARG-R05-05 | Glossary ngắn/diễn giải positive class và metric chính; acceptance cụ thể hơn | Không thay metric, threshold hoặc giả thuyết |
| ARG-R05-00A/B | Giữ pending admin và DOCX/render | OPEN, không đóng bằng prose/tests |

Không sửa scientific RQ, threshold0.5, models, raw, frozen results, prior negative findings, original form. Không mở rộng thí nghiệm. Acceptance là giải quyết các lỗi nội dung có thể chứng minh cộng với reviewer recheck; chưa là proposal submission acceptance. English/Chinese anti-slop automation không áp dụng cho tiếng Việt; rà tay giọng điệu, tránh claim novelty/superiority/real-time không chứng cứ.
