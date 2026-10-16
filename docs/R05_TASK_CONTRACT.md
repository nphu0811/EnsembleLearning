# R05 — resume và kết thúc review còn thiếu

Ngày 16/10/2026. Branch `codex/r05-proposal-argument-review`, entry commit `c4ed771815675ace26f4df574a691fc67ed00179`; origin HEAD khớp qua `git ls-remote origin HEAD`. Working tree sạch trước khi bắt đầu.

PLAN → EXECUTE → VERIFY → REPAIR → CHECKPOINT áp dụng từng task, không đánh số lại Phase 0–20.

## R05-ASSEMBLY-REVIEW

- Inputs: r04 draft bất biến cho lượt review, foundation 00–07, canon, frozen RQ, claim/gap/source maps, nguyên mẫu DOCX và field snapshot, smoke report, release blockers.
- Independent review: một AI reviewer ở context riêng, không nhận evidence review r04 hoặc findings của người sửa. Đây là independent AI argument/feasibility pass, không phải phản biện con người, review mù ba người hoặc phê duyệt hành chính.
- Outputs: report được đóng băng trước sửa; revision brief; bản r05 riêng để bảo toàn r04; ma trận giải quyết findings và validation.
- Acceptance: từng finding có evidence, biện pháp sửa và test/điều kiện còn mở; chuỗi mục tiêu–RQ–phương pháp–bằng chứng–đóng góp–sản phẩm có đối chiếu; citations resolve trong phạm vi nguồn đã đọc; giữ chronology, original form, frozen limits. Điểm số và kiểm tra từ khóa không thay kết luận nội dung.
- Forbidden: fit/predict/tune mới, sửa raw/freeze/official results/RQ, tự xác nhận lịch/kinh phí/chữ ký, gọi Markdown là filled/rendered DOCX.
- Downstream: chuẩn bị nội dung vào form, P16/P17/P18 và G4/G5. Hoàn tất lượt review không đóng các gate này.

## R05-PUBLIC-SURFACE

- Read-only audit các file Git đang track, inventory, nguyên mẫu và nội dung archive đọc được. Lưu path/line/category và hash, không chép giá trị nghi nhạy cảm vào báo cáo.
- Pattern scan là triage, không chứng nhận không có secrets hoặc xác nhận mọi hit là thông tin riêng. Mẫu có danh tính minh họa phải được phân biệt với danh tính tác giả.
- Không xóa/untrack/sửa history/push. Cleanup cần tác giả quyết định sau khi có finding cụ thể.

## R05-CHECKPOINT

- Entry audit thực: 266/266 manifest, 282/282 preservation; DOCX CRC và ZIP 15 entries/extraction PASS. Không rerun smoke đã PASS.
- Lưu memory, evidence hashes, exact resume command; kiểm thay đổi và tạo commit có scope rõ. Không final release hoặc tác vụ nền sau phiên.
