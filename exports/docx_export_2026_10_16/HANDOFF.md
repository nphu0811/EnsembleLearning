# Tiếp tục tác vụ xuất DOCX

Đọc `DOCX_RUNTIME_DIAGNOSTIC.md` và `diagnostics.json` trước. Kiểm tra các SHA-256 trong `SOURCE_MANIFEST.csv`; script `preserve_and_diagnose.py` chỉ phục vụ lưu nguồn/chẩn đoán, không tạo DOCX. Không cần chạy lại nghiên cứu.

Nội dung chính được lưu nguyên byte tại `Bao_cao_NCKH_bao_toan.md`, có 6 hình hoạt động. Các bản nguồn và tài liệu đối chiếu ở `sources/`. Đây là bảo toàn bản thảo hiện có, không phải xác nhận bản báo cáo hoàn chỉnh. Không tự sửa số liệu, câu chữ đã có hoặc roadmap trong tác vụ xuất file.

Hai blocker độc lập còn mở: không có dependency loader/runtime skill chính thức được expose; Windows bundle không có LibreOffice. Documents local đã enabled, managed Node/Python/docx package tồn tại. Không dùng runtime cache tự dò thay cho resolver. Không cài global package hoặc sửa skill. Chưa chạy authoring marker, chưa tạo DOCX, chưa render.

Sau khi host cung cấp resolver và renderer đúng hợp đồng: khởi tạo từ paths do resolver trả về, đọc Documents create/template guidance, dùng mẫu LaTeX báo cáo làm tham chiếu (DOCX 2026 chỉ là đề cương), chạy marker ngay trước authoring, xuất DOCX rồi render/kiểm tra mọi trang. Chỉ bàn giao sau QA. Giữ nguyên nguồn, output vào thư mục mới.
