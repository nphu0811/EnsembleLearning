# Chẩn đoán đường xuất DOCX ngày 16 tháng 10 năm 2026

Trạng thái: **BLOCKED**. Chưa tạo DOCX, chưa render, chưa kiểm định bố cục. Không chạy lại nghiên cứu, không sửa số liệu, roadmap hoặc bản thảo nguồn.

## Kết quả kiểm tra

1. Registry tools của phiên đã được kiểm tra và lưu tại `tool_inventory.json`. Không có callable tool `load_workspace_dependencies` hoặc resolver workspace dependencies tương đương được mô tả trong registry. Không gọi tên tool suy đoán. Các tool quản lý plugin và Document Control có mặt.
2. Documents skill có ở `C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/documents/26.1013.11914/skills/documents/SKILL.md`. Cấu hình local có `documents@openai-primary-runtime.enabled = true`. Manifest plugin chỉ khai báo skills; không có lệnh bootstrap/runtime resolver. Vì vậy không thể quy nguyên nhân cho việc Documents bị tắt.
3. Managed runtime **đã được cài** ở `C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/`. `runtime.json` xác nhận bundle `26.1013.11914`, Windows x64. Đã chạy read-only `--version` bằng đúng executable trong cache: Node `v24.19.0`, Python `3.12.14`. Thư mục package `dependencies/node/node_modules/docx/` có tồn tại. Không dùng những đường dẫn tự tìm này để thay thế bước resolver bắt buộc.
4. Manifest runtime có `bundledSkills: []`. Không tìm thấy runtime skill/resolver trong các skill roots và plugin bundle đã kiểm tra. Các runtime helpers của Presentations chỉ tiêu thụ biến môi trường, không cung cấp bootstrap/resolver. Các biến `RUNTIME_NODE`, `RUNTIME_PYTHON`, `RUNTIME_NODE_MODULES`, `RUNTIME_BIN_DIR` và các biến `CODEX_PRIMARY_RUNTIME_*` đã kiểm tra đều chưa được thiết lập. Đây là bằng chứng runtime chưa được khởi tạo cho workflow này; không đủ để xác định lỗi nội bộ nào của host.
5. Bundle Windows có `libreOfficeVersion: null`. Native manifest chỉ liệt kê `heif-convert`, `JxrDecApp`, `pdfinfo`, `pdftoppm`; không có LibreOffice. Không tìm thấy `soffice.exe` trong dependencies hoặc PATH. Có Poppler nhưng Poppler không chuyển DOCX thành PDF. Đây là blocker render riêng, ngay cả nếu loader được khôi phục.
6. `render_docx.py` có nhánh Windows tìm LibreOffice native trên PATH, nhưng chính SKILL.md yêu cầu LibreOffice bundled do loader resolve và cấm dùng desktop LibreOffice của người dùng. Không sửa skill, không dùng nhánh triển khai này để bỏ qua hợp đồng. Chưa chạy renderer vì thiếu resolver/renderer, không có output DOCX mới.
7. Document Control trả về không có Word session được kết nối. Không có đường xuất dựa trên phiên Word hiện hành.
8. Tra cứu catalog plugin không tìm được public listed plugin cho `documents@openai-primary-runtime`; kết quả này không phủ nhận plugin built-in đang được bật local. Không có thao tác install/remove/reconfigure plugin nào được thực hiện. Không tìm thấy hướng dẫn công khai xác định endpoint artifact loader có thể tự thêm an toàn.

## Yêu cầu skill đang chặn authoring và bàn giao

Documents SKILL.md ghi: “Use Codex workspace dependencies for docx artifact work: resolve them through the workspace dependency loader or runtime skill”. Skill cũng yêu cầu render bằng `render_docx.py` và kiểm tra PNG của mọi trang trước khi giao DOCX.

Những thành phần còn thiếu trong phiên này là:

- Workspace dependency resolver callable từ host, hoặc runtime skill chính thức được cung cấp cho phiên, trả về executable Node/Python, package directory và native binary paths có thẩm quyền.
- Renderer DOCX đáp ứng hợp đồng Documents, gồm bundled LibreOffice có thể được resolve; hoặc workflow Windows thay thế được hướng dẫn chính thức. Hiện không có thành phần này.

Không kết luận toàn bộ runtime chưa cài. Không kết luận chắc chắn plugin chưa khởi tạo là nguyên nhân gốc: local plugin đã enabled, còn khả năng expose tool/khởi tạo runtime của host không kiểm tra được sâu hơn qua công cụ đang cung cấp.

## Cách khắc phục và tiếp tục

1. Qua phía quản trị/thiết lập hỗ trợ của Codex, kiểm tra hoặc sửa tích hợp primary runtime để phiên nhận được workspace dependency loader hoặc runtime skill chính thức. Cung cấp `diagnostics.json`, phiên bản bundle và mô tả thiếu tool cho bộ phận hỗ trợ. Không thêm một MCP endpoint suy đoán, không cài npm/pip toàn cục, không chỉnh SKILL.md.
2. Bổ sung môi trường renderer được Documents hỗ trợ. Một phiên Codex trên môi trường có loader và bundled LibreOffice đáp ứng cả hai điều kiện; nếu tiếp tục trên Windows, cần hướng dẫn/runtime chính thức giải quyết sự khác nhau giữa hợp đồng skill và nhánh renderer Windows. Chỉ cài desktop LibreOffice không giải quyết điều kiện resolver và không đáp ứng hợp đồng hiện tại.
3. Sau khi phía host sửa/refresh runtime, mở lại phiên nếu thay đổi công cụ yêu cầu, rồi kiểm tra registry thực tế. Mở phiên mới đơn thuần chưa được chứng minh sẽ sửa lỗi. Chỉ tiếp tục khi resolver thực sự callable và renderer thực sự có đường dẫn hợp lệ.
4. Dùng đường dẫn do resolver trả về; đọc các tham chiếu Documents liên quan đến tạo theo mẫu. Chạy marker bằng managed Node đúng một lần ngay trước lệnh authoring đầu tiên. Tạo file trong working/export directory, không ghi đè nguồn. Render bằng runtime hợp lệ, xem tất cả trang, sửa và render lại đến khi đạt QA.

## Nội dung và mẫu đã bảo toàn

`Bao_cao_NCKH_bao_toan.md` là bản sao nguyên byte của `notebook/phase13/phase13_4_manuscript_with_figures_tables.md`, gồm tóm tắt, giới thiệu, công trình liên quan, phương pháp, kết quả, thảo luận, hạn chế, đóng góp, kết luận và tài liệu tham khảo. Sáu hình được sao chép vào `figures/` để các liên kết tương đối vẫn hoạt động. `sources/` giữ các bản thảo lịch sử và tài liệu liên quan; `SOURCE_MANIFEST.csv` lưu nguồn, đích, số byte, SHA-256. 60 mục đã kiểm tra khớp nguồn và bản sao; không viết lại nội dung.

Không gọi bản thảo này là báo cáo hoàn chỉnh đã duyệt: handoff và reclassification hiện hành phân loại các manuscript cũ là premature reporting drafts. Những cách diễn đạt cũ cần QA sau này được giữ nguyên theo giới hạn công việc của người dùng. Phần đề cương r02 mới được sao lưu riêng, không trộn vào báo cáo hay thay thế nội dung báo cáo.

`templates/original/DE-TAI-NCKHSV-15.zip` chứa 15 file, không có DOCX; đây là bộ mẫu LaTeX quyển báo cáo. `Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx` là mẫu đề cương, không phải mẫu báo cáo. Khi xuất DOCX báo cáo sau khi khôi phục runtime, lấy bộ mẫu báo cáo làm tham chiếu và kiểm định bố cục tương ứng; không tự dùng form đề cương làm form báo cáo.

Checkpoint chỉ thuộc tác vụ xuất DOCX. Không thay đổi trạng thái các Phase nghiên cứu hoặc tuyên bố đạt release gate.
