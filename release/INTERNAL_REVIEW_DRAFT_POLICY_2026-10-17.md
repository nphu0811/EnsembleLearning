# Chính sách gói nháp kiểm tra nội bộ

**INTERNAL_REVIEW_ONLY. NOT_AUTHORIZED_FOR_PUBLIC_RELEASE.** Đây là gói để đọc,
đối chiếu và chuẩn bị phản biện, không phải FINAL_NCKH, không cấp license mới,
không xác nhận đủ điều kiện nộp và không phải môi trường chạy lại training.

Tạo gói bằng allowlist tường minh. Không lấy toàn bộ Git tree hay `git archive`
một cách mặc định: cây hiện còn ba model smoke và tài liệu bên thứ ba. Các bản
copy trong `draft_contents/` và ZIP nháp giữ cục bộ, bị Git ignore; chỉ manifest,
kiểm kê, kết quả QA và các tài liệu tự viết được commit.

Loại khỏi gói: mọi joblib/pickle/model binary, raw/processed dataset, prediction
CSV từng dòng, virtualenv/cache, credential/.env, template original, ZIP lịch sử,
publisher PDF/full text/page image và thư mục `local_sources/`. Không dùng wildcard
để chọn file. Đường dẫn phải ở trong workspace và không thoát qua symlink; tên
trong ZIP không được tuyệt đối hoặc chứa `..`. PDF báo cáo do tác giả cung cấp
là ngoại lệ được chỉ định riêng, giữ nguyên SHA256 đã chấp thuận và chỉ vào gói
**nội bộ cục bộ**, không được tự phát hành công khai.

Một gói allowlist sạch không đòi hỏi xóa/untrack model smoke. Giữ nguyên physical
copies và Git history. `.gitignore` không làm file đã tracked trở thành untracked.
Nếu sau này xóa khỏi index bằng một commit, người khác `git pull` commit đó có
thể bị Git xóa physical file ở đường dẫn tracked cũ. Vì vậy index cleanup không
cần cho task này và không được thực hiện. Nếu chủ sở hữu thực sự muốn cleanup,
phải lập phương án bảo toàn bản copy ở ngoài cây tracked, kiểm hash và hiểu tác
động tới các checkout khác trước khi có thao tác riêng được chấp thuận.

Manifest có path, bytes, SHA256, origin/evidence class và distribution status cho
từng file. ZIP được mở lại để kiểm CRC, đúng allowlist, byte hashes, nhãn nội bộ,
không có loại file cấm và source không đổi sau copy. PASS cơ học không đóng các
gate khoa học/quyền phân phối hoặc bảo đảm archive không chứa một secret mà kiểm
tra pattern không nhận biết. Source đã chọn vẫn phải được chủ sở hữu review
trước bất kỳ bước phát hành công khai nào.
